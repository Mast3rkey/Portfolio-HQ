"""Tests for relationship_validator.py (REL-0001 §I schema/taxonomy scope,
extended by REL-0002's first real relationship-content batch).

Every schema/taxonomy/behavior test below constructs its own synthetic
fixture — no real portfolio ticker, real company thesis, or real investment
judgment appears in any synthetic fixture in this file, same authorized-
scope discipline test_intelligence_validator.py already follows, per its own
"only a fictional placeholder ticker" convention. The two tests reading the
real repository's intelligence/relationships/ directory (below, under
"validating the real repository never mutates it" and "universe loaders
never touch intelligence/relationships") are the sole exception: they
validate REL-0002's real CEG_MSFT record, added under its own separate
governance authorization, not a synthetic fixture.
"""

import ast
from pathlib import Path

import pytest
import yaml

import relationship_validator as rv


# ── fixtures ─────────────────────────────────────────────────────────────

def _evidence_entry(**overrides) -> dict:
    entry = {
        "claim": "synthetic claim, narrow and falsifiable",
        "source": "synthetic 10-K FY2025",
        "inspected_source_type": "primary",
        "source_date": "2025-12-31",
        "effective_date": "2025-12-31",
        "evidence_classification": "observed",
        "confidence": "medium",
        "materiality": "medium",
        "uncertainty": "synthetic uncertainty statement",
        "disconfirming_evidence": None,
    }
    entry.update(overrides)
    return entry


def _review_block(**overrides) -> dict:
    block = {
        "cadence_days": 90,
        "last_reviewed": "2026-01-01",
        "next_due": "2026-04-01",
        "log": [{"date": "2026-01-01", "note": "synthetic review note"}],
    }
    block.update(overrides)
    return block


def _directional_record(**overrides) -> dict:
    """A valid synthetic directional (customer_dependency) record, ZZZA
    depends on ZZZB."""
    record = {
        "tickers": ["ZZZA", "ZZZB"],
        "relationship_type": "customer_dependency",
        "symmetric": False,
        "subject": "ZZZA",
        "object": "ZZZB",
        "direction": "ZZZA derives material revenue from ZZZB as a customer",
        "relationship_status": "current",
        "decision_served": ["thesis_monitoring"],
        "evidence": [_evidence_entry()],
        "review": _review_block(),
    }
    record.update(overrides)
    return record


def _symmetric_record(**overrides) -> dict:
    """A valid synthetic symmetric (competitor) record, ZZZC/ZZZD."""
    record = {
        "tickers": ["ZZZC", "ZZZD"],
        "relationship_type": "competitor",
        "symmetric": True,
        "relationship_status": "current",
        "decision_served": ["next_dollar_or_opportunity_cost"],
        "evidence": [_evidence_entry(evidence_classification="judgmental")],
        "review": _review_block(),
    }
    record.update(overrides)
    return record


def _write_pair(tmp_path: Path, stem: str, data: dict, *, with_md: bool = True) -> Path:
    yaml_path = tmp_path / f"{stem}.yaml"
    yaml_path.write_text(yaml.safe_dump(data))
    if with_md:
        (tmp_path / f"{stem}.md").write_text(f"# {stem}\n")
    return yaml_path


# ── validate_relationship_data: in-memory schema checks ─────────────────────

def test_valid_synthetic_directional_record_passes():
    result = rv.validate_relationship_data(_directional_record())
    assert result.valid is True
    assert result.errors == []


def test_valid_synthetic_symmetric_competitor_record_passes():
    result = rv.validate_relationship_data(_symmetric_record())
    assert result.valid is True
    assert result.errors == []


def test_non_mapping_root_is_rejected():
    result = rv.validate_relationship_data(["not", "a", "mapping"])
    assert result.valid is False
    assert any("mapping" in e for e in result.errors)


@pytest.mark.parametrize("bad_type", ["duplicate_economic_exposure", "correlated_loss_mechanism", "missing_exposure"])
def test_derived_only_conclusion_types_are_rejected_as_primitives(bad_type):
    data = _directional_record(relationship_type=bad_type)
    result = rv.validate_relationship_data(data)
    assert result.valid is False
    assert any("derived conclusion" in e for e in result.errors)


def test_invalid_relationship_type_is_rejected():
    data = _directional_record(relationship_type="not_a_real_type")
    result = rv.validate_relationship_data(data)
    assert result.valid is False
    assert any("relationship_type" in e for e in result.errors)


@pytest.mark.parametrize("good_type", sorted(rv.PRIMITIVE_RELATIONSHIP_TYPES))
def test_every_frozen_primitive_type_is_accepted_when_shaped_correctly(good_type):
    if good_type in rv._DIRECTIONAL_TYPES:
        data = _directional_record(relationship_type=good_type)
    else:
        data = _symmetric_record(relationship_type=good_type, symmetric=True)
    result = rv.validate_relationship_data(data)
    assert result.valid is True, result.errors


@pytest.mark.parametrize("bad_classification", ["confirmed", "guessed", "Observed", ""])
def test_invalid_evidence_classification_is_rejected(bad_classification):
    data = _directional_record(evidence=[_evidence_entry(evidence_classification=bad_classification)])
    result = rv.validate_relationship_data(data)
    assert result.valid is False
    assert any("evidence_classification" in e for e in result.errors)


@pytest.mark.parametrize("good_classification", sorted(rv.EVIDENCE_CLASSIFICATIONS))
def test_every_frozen_evidence_classification_is_accepted(good_classification):
    data = _directional_record(evidence=[_evidence_entry(evidence_classification=good_classification)])
    result = rv.validate_relationship_data(data)
    assert result.valid is True, result.errors


@pytest.mark.parametrize("bad_status", ["active", "Current", "pending", ""])
def test_invalid_relationship_status_is_rejected(bad_status):
    data = _directional_record(relationship_status=bad_status)
    result = rv.validate_relationship_data(data)
    assert result.valid is False
    assert any("relationship_status" in e for e in result.errors)


@pytest.mark.parametrize("good_status", sorted(rv.RELATIONSHIP_STATUSES))
def test_every_frozen_relationship_status_is_accepted(good_status):
    data = _directional_record(relationship_status=good_status)
    result = rv.validate_relationship_data(data)
    assert result.valid is True, result.errors


def test_invalid_decision_served_value_is_rejected():
    data = _directional_record(decision_served=["make_more_money_fast"])
    result = rv.validate_relationship_data(data)
    assert result.valid is False
    assert any("decision_served" in e for e in result.errors)


def test_empty_decision_served_list_is_rejected():
    data = _directional_record(decision_served=[])
    result = rv.validate_relationship_data(data)
    assert result.valid is False
    assert any("decision_served" in e for e in result.errors)


@pytest.mark.parametrize("good_value", sorted(rv.DECISION_SERVED_VALUES))
def test_every_frozen_decision_served_value_is_accepted(good_value):
    data = _directional_record(decision_served=[good_value])
    result = rv.validate_relationship_data(data)
    assert result.valid is True, result.errors


@pytest.mark.parametrize(
    "missing_key",
    sorted(rv._EVIDENCE_ENTRY_REQUIRED_KEYS - {"disconfirming_evidence"}),
)
def test_missing_required_evidence_field_is_rejected(missing_key):
    entry = _evidence_entry()
    del entry[missing_key]
    data = _directional_record(evidence=[entry])
    result = rv.validate_relationship_data(data)
    assert result.valid is False


def test_disconfirming_evidence_key_must_be_present_even_if_null():
    entry = _evidence_entry()
    del entry["disconfirming_evidence"]
    data = _directional_record(evidence=[entry])
    result = rv.validate_relationship_data(data)
    assert result.valid is False
    assert any("disconfirming_evidence" in e for e in result.errors)


def test_disconfirming_evidence_may_be_explicitly_null():
    """§E: disconfirming_evidence must never be silently omitted, but an
    explicit null (nothing disconfirming known) is a valid, honest value."""
    data = _directional_record(evidence=[_evidence_entry(disconfirming_evidence=None)])
    result = rv.validate_relationship_data(data)
    assert result.valid is True


def test_empty_evidence_list_is_rejected():
    data = _directional_record(evidence=[])
    result = rv.validate_relationship_data(data)
    assert result.valid is False
    assert any("evidence" in e for e in result.errors)


def test_missing_review_block_is_rejected():
    data = _directional_record()
    del data["review"]
    result = rv.validate_relationship_data(data)
    assert result.valid is False


def test_review_block_missing_required_key_is_rejected():
    data = _directional_record(review=_review_block())
    del data["review"]["next_due"]
    result = rv.validate_relationship_data(data)
    assert result.valid is False
    assert any("review" in e for e in result.errors)


# ── directionality (§D) ──────────────────────────────────────────────────

def test_directional_type_missing_subject_object_direction_is_rejected():
    data = _directional_record()
    del data["subject"]
    del data["object"]
    del data["direction"]
    result = rv.validate_relationship_data(data)
    assert result.valid is False
    assert any("subject" in e or "object" in e or "direction" in e for e in result.errors)


def test_directional_type_declaring_symmetric_true_is_rejected():
    data = _directional_record(symmetric=True)
    result = rv.validate_relationship_data(data)
    assert result.valid is False
    assert any("directional-by-construction" in e for e in result.errors)


def test_symmetric_type_declaring_subject_object_is_rejected():
    data = _symmetric_record(subject="ZZZC", object="ZZZD")
    result = rv.validate_relationship_data(data)
    assert result.valid is False
    assert any("co-equal-subjects" in e for e in result.errors)


def test_symmetric_type_declaring_symmetric_false_is_rejected():
    data = _symmetric_record(symmetric=False)
    result = rv.validate_relationship_data(data)
    assert result.valid is False
    assert any("symmetric-by-construction" in e for e in result.errors)


def test_symmetric_field_must_be_explicit_boolean():
    data = _directional_record(symmetric=None)
    result = rv.validate_relationship_data(data)
    assert result.valid is False
    assert any("explicit boolean" in e for e in result.errors)


def test_substitute_type_may_be_declared_symmetric_or_directional():
    symmetric_substitute = _symmetric_record(
        tickers=["ZZZE", "ZZZF"], relationship_type="substitute", symmetric=True,
    )
    result = rv.validate_relationship_data(symmetric_substitute)
    assert result.valid is True, result.errors

    directional_substitute = _directional_record(
        tickers=["ZZZE", "ZZZF"], relationship_type="substitute", symmetric=False,
        subject="ZZZE", object="ZZZF",
        direction="a ZZZF customer could reallocate demand to ZZZE, not necessarily the reverse",
    )
    result2 = rv.validate_relationship_data(directional_substitute)
    assert result2.valid is True, result2.errors


# ── tickers field / filename ordering (§B) ──────────────────────────────────

def test_non_alphabetical_tickers_field_is_rejected():
    data = _directional_record(tickers=["ZZZB", "ZZZA"])
    result = rv.validate_relationship_data(data)
    assert result.valid is False
    assert any("alphabetically ordered" in e for e in result.errors)


def test_duplicate_ticker_in_pair_is_rejected():
    data = _directional_record(tickers=["ZZZA", "ZZZA"])
    result = rv.validate_relationship_data(data)
    assert result.valid is False


def test_invalid_filename_ordering_rejected_at_file_level(tmp_path):
    data = _directional_record()
    # Filename deliberately reversed relative to the record's own tickers field.
    path = _write_pair(tmp_path, "ZZZB_ZZZA", data)
    result = rv.validate_relationship_file(path)
    assert result.valid is False
    assert any("does not match" in e for e in result.errors)


def test_reverse_duplicate_pair_across_two_files_rejected(tmp_path):
    _write_pair(tmp_path, "ZZZA_ZZZB", _directional_record())
    _write_pair(tmp_path, "ZZZB_ZZZA", _directional_record(tickers=["ZZZA", "ZZZB"]))
    result = rv.validate_relationships_directory(tmp_path)
    assert result.valid is False
    assert any(
        "must never be recorded in both A_B and B_A form" in e
        for r in result.results for e in r.errors
    )


# ── ticker reference integrity (§J) ──────────────────────────────────────────

def test_ticker_not_in_canonical_or_retained_universe_is_rejected():
    data = _directional_record()
    result = rv.validate_relationship_data(
        data, canonical_universe=frozenset({"UNRELATED"}), retained_universe=frozenset(),
    )
    assert result.valid is False
    assert any("REL-0001 §J" in e for e in result.errors)


def test_ticker_in_canonical_universe_is_accepted():
    data = _directional_record()
    result = rv.validate_relationship_data(
        data, canonical_universe=frozenset({"ZZZA", "ZZZB"}), retained_universe=frozenset(),
    )
    assert result.valid is True, result.errors


def test_ticker_in_retained_universe_only_is_accepted():
    data = _directional_record()
    result = rv.validate_relationship_data(
        data, canonical_universe=frozenset(), retained_universe=frozenset({"ZZZA", "ZZZB"}),
    )
    assert result.valid is True, result.errors


def test_empty_universes_skip_reference_check_entirely():
    """Default (no universe supplied): schema-only validation, matching the
    synthetic-fixture use case throughout this file."""
    data = _directional_record()
    result = rv.validate_relationship_data(data)
    assert result.valid is True


# ── Markdown companion (§B) ──────────────────────────────────────────────────

def test_missing_markdown_companion_is_rejected(tmp_path):
    path = _write_pair(tmp_path, "ZZZA_ZZZB", _directional_record(), with_md=False)
    result = rv.validate_relationship_file(path)
    assert result.valid is False
    assert any("Markdown companion" in e for e in result.errors)


def test_present_markdown_companion_is_accepted(tmp_path):
    path = _write_pair(tmp_path, "ZZZA_ZZZB", _directional_record(), with_md=True)
    result = rv.validate_relationship_file(path)
    assert result.valid is True, result.errors


# ── directory scan: absent / empty / no-index-required (per REL-0001 §B) ────

def test_absent_relationships_directory_is_valid():
    result = rv.validate_relationships_directory("/definitely/does/not/exist/anywhere")
    assert result.valid is True
    assert result.results == []
    assert result.record_count == 0


def test_empty_relationships_directory_is_valid(tmp_path):
    result = rv.validate_relationships_directory(tmp_path)
    assert result.valid is True
    assert result.results == []


def test_no_index_file_is_required_for_a_valid_directory(tmp_path):
    """§B/§I(15): the filesystem directory listing is the only index —
    validating a directory with real records and no index.yaml must not
    itself be flagged as missing anything."""
    _write_pair(tmp_path, "ZZZA_ZZZB", _directional_record())
    result = rv.validate_relationships_directory(tmp_path)
    assert result.valid is True, [e for r in result.results for e in r.errors]
    assert not (tmp_path / "index.yaml").exists()


@pytest.mark.parametrize("index_name", ["index.yaml", "index.yml", "index.md"])
def test_stored_index_file_is_prohibited(tmp_path, index_name):
    _write_pair(tmp_path, "ZZZA_ZZZB", _directional_record())
    (tmp_path / index_name).write_text("not permitted")
    result = rv.validate_relationships_directory(tmp_path)
    assert result.valid is False
    assert any(
        "prohibited stored index file" in e for r in result.results for e in r.errors
    )


def test_one_invalid_file_does_not_stop_the_scan(tmp_path):
    _write_pair(tmp_path, "ZZZA_ZZZB", _directional_record())
    bad = _directional_record(relationship_type="not_a_real_type")
    _write_pair(tmp_path, "ZZZC_ZZZD", bad)
    result = rv.validate_relationships_directory(tmp_path)
    assert result.valid is False
    assert result.record_count == 2
    sources = {r.source for r in result.results}
    assert any("ZZZA_ZZZB" in s for s in sources)
    assert any("ZZZC_ZZZD" in s for s in sources)


# ── REL-0001 closed-vocabulary independent pinning (§C/§E/§F) ───────────────
# Hardcoded directly from REL-0001's literal text, not derived from
# relationship_validator.py's own constants — a silent drift in the module's
# constants would not be caught by parametrizing against rv.* itself (as the
# tests above do); these compare the module's constants against an
# independent transcription of the governing document.

REL0001_PRIMITIVE_RELATIONSHIP_TYPES = frozenset({
    "supplier_dependency",
    "customer_dependency",
    "manufacturing_dependency",
    "technology_platform_dependency",
    "capital_spending_dependency",
    "regulatory_or_reimbursement_dependency",
    "commodity_or_energy_dependency",
    "financing_or_interest_rate_dependency",
    "geographic_or_geopolitical_dependency",
    "competitor",
    "substitute",
    "complement",
})

REL0001_EVIDENCE_CLASSIFICATIONS = frozenset({"observed", "inferred", "modeled", "judgmental"})

REL0001_RELATIONSHIP_STATUSES = frozenset({"current", "historical", "potential", "hypothetical"})

REL0001_DECISION_SERVED_VALUES = frozenset({
    "duplicate_exposure_detection",
    "thesis_monitoring",
    "stress_testing",
    "next_dollar_or_opportunity_cost",
    "missing_exposure_review",
    "zero_based_portfolio_review",
})


def test_primitive_relationship_types_match_rel0001_literal_text():
    assert rv.PRIMITIVE_RELATIONSHIP_TYPES == REL0001_PRIMITIVE_RELATIONSHIP_TYPES


def test_evidence_classifications_match_rel0001_literal_text():
    assert rv.EVIDENCE_CLASSIFICATIONS == REL0001_EVIDENCE_CLASSIFICATIONS


def test_relationship_statuses_match_rel0001_literal_text():
    assert rv.RELATIONSHIP_STATUSES == REL0001_RELATIONSHIP_STATUSES


def test_decision_served_values_match_rel0001_literal_text():
    assert rv.DECISION_SERVED_VALUES == REL0001_DECISION_SERVED_VALUES


@pytest.mark.parametrize("good_type", sorted(REL0001_PRIMITIVE_RELATIONSHIP_TYPES))
def test_validator_accepts_every_rel0001_hardcoded_primitive_type(good_type):
    if good_type in rv._DIRECTIONAL_TYPES:
        data = _directional_record(relationship_type=good_type)
    else:
        data = _symmetric_record(relationship_type=good_type, symmetric=True)
    result = rv.validate_relationship_data(data)
    assert result.valid is True, result.errors


@pytest.mark.parametrize("bad_type", ["supplier_dependenc", "Competitor", "vendor_relationship"])
def test_validator_rejects_representative_invalid_primitive_types(bad_type):
    data = _directional_record(relationship_type=bad_type)
    result = rv.validate_relationship_data(data)
    assert result.valid is False


@pytest.mark.parametrize("good_classification", sorted(REL0001_EVIDENCE_CLASSIFICATIONS))
def test_validator_accepts_every_rel0001_hardcoded_evidence_classification(good_classification):
    data = _directional_record(evidence=[_evidence_entry(evidence_classification=good_classification)])
    result = rv.validate_relationship_data(data)
    assert result.valid is True, result.errors


@pytest.mark.parametrize("bad_classification", ["confirmed", "Observed", "estimated"])
def test_validator_rejects_representative_invalid_evidence_classifications(bad_classification):
    data = _directional_record(evidence=[_evidence_entry(evidence_classification=bad_classification)])
    result = rv.validate_relationship_data(data)
    assert result.valid is False


@pytest.mark.parametrize("good_status", sorted(REL0001_RELATIONSHIP_STATUSES))
def test_validator_accepts_every_rel0001_hardcoded_relationship_status(good_status):
    data = _directional_record(relationship_status=good_status)
    result = rv.validate_relationship_data(data)
    assert result.valid is True, result.errors


@pytest.mark.parametrize("bad_status", ["active", "Current", "expired"])
def test_validator_rejects_representative_invalid_relationship_statuses(bad_status):
    data = _directional_record(relationship_status=bad_status)
    result = rv.validate_relationship_data(data)
    assert result.valid is False


@pytest.mark.parametrize("good_value", sorted(REL0001_DECISION_SERVED_VALUES))
def test_validator_accepts_every_rel0001_hardcoded_decision_served_value(good_value):
    data = _directional_record(decision_served=[good_value])
    result = rv.validate_relationship_data(data)
    assert result.valid is True, result.errors


@pytest.mark.parametrize("bad_value", ["portfolio_optimization", "alpha_generation", "risk_scoring"])
def test_validator_rejects_representative_invalid_decision_served_values(bad_value):
    data = _directional_record(decision_served=[bad_value])
    result = rv.validate_relationship_data(data)
    assert result.valid is False


# ── boolean confidence/materiality edge case (bounded correction) ───────────

def test_confidence_false_is_rejected():
    data = _directional_record(evidence=[_evidence_entry(confidence=False)])
    result = rv.validate_relationship_data(data)
    assert result.valid is False
    assert any("confidence" in e for e in result.errors)


def test_confidence_true_is_rejected():
    data = _directional_record(evidence=[_evidence_entry(confidence=True)])
    result = rv.validate_relationship_data(data)
    assert result.valid is False
    assert any("confidence" in e for e in result.errors)


def test_materiality_false_is_rejected():
    data = _directional_record(evidence=[_evidence_entry(materiality=False)])
    result = rv.validate_relationship_data(data)
    assert result.valid is False
    assert any("materiality" in e for e in result.errors)


def test_materiality_true_is_rejected():
    data = _directional_record(evidence=[_evidence_entry(materiality=True)])
    result = rv.validate_relationship_data(data)
    assert result.valid is False
    assert any("materiality" in e for e in result.errors)


def test_confidence_zero_remains_a_valid_explicit_value():
    """0 is a legitimate explicit confidence value, distinct from the
    boolean False the correction above rejects — bool is a subclass of int
    in Python, but a literal int 0 must not be caught by the bool check."""
    data = _directional_record(evidence=[_evidence_entry(confidence=0)])
    result = rv.validate_relationship_data(data)
    assert result.valid is True, result.errors


def test_materiality_zero_remains_a_valid_explicit_value():
    data = _directional_record(evidence=[_evidence_entry(materiality=0)])
    result = rv.validate_relationship_data(data)
    assert result.valid is True, result.errors


# ── corrected Markdown-companion documentation (bounded correction) ─────────

def test_orphan_markdown_file_without_yaml_is_not_scanned_or_flagged(tmp_path):
    """relationship_validator.py's Markdown-companion check is one-directional
    (.yaml -> .md only) — an orphan .md file with no matching .yaml record is
    not itself scanned or reported as invalid, since
    validate_relationships_directory globs *.yaml only. Locks in the actual
    behavior the corrected module docstring now accurately describes."""
    _write_pair(tmp_path, "ZZZA_ZZZB", _directional_record())
    (tmp_path / "ORPHAN_ZZZQ_ZZZR.md").write_text("# orphan, no matching yaml\n")
    result = rv.validate_relationships_directory(tmp_path)
    assert result.valid is True, [e for r in result.results for e in r.errors]


# ── universe loaders against the real repository (read-only) ────────────────

def test_load_canonical_universe_reads_27_names_from_real_targets_yaml():
    universe = rv.load_canonical_universe(".")
    assert len(universe) == 27
    assert "NVDA" in universe
    assert "SNPS" in universe  # gated names remain in the canonical roster


def test_load_retained_universe_reads_real_company_intelligence_directory():
    universe = rv.load_retained_universe(".")
    assert "NVDA" in universe
    assert len(universe) >= 27  # superset of canonical, includes retained non-canonical names


def test_universe_loaders_never_touch_intelligence_relationships():
    """REL-0001 §I's inventory-only unit created zero relationship records;
    REL-0002 (WS-0005 Milestone 4's first authorized relationship-content
    batch) later added intelligence/relationships/CEG_MSFT.yaml/.md — the
    directory now legitimately exists. The guarantee this test locks in is
    unchanged either way: the universe loaders themselves never create,
    remove, or otherwise touch that directory — before/after existence must
    match, not be unconditionally False."""
    before = Path("intelligence/relationships").exists()
    rv.load_canonical_universe(".")
    rv.load_retained_universe(".")
    after = Path("intelligence/relationships").exists()
    assert before == after


# ── validating the real repository never mutates it ─────────────────────────

_REAL_RELATIONSHIP_STEMS = [
    "CEG_MSFT",
    "AVGO_GOOGL",
    "AVGO_META",
    "ETN_GNRC",
    "GEV_GNRC",
    "GNRC_PWR",
    "GOOGL_MSFT",
    "AMZN_MSFT",
    "AMZN_GOOGL",
]


def test_validating_the_real_repository_relationships_dir_does_not_mutate_it():
    """REL-0002 authorized the first real intelligence/relationships record
    (CEG_MSFT). REL-0003 added eight further records in the same batch
    (AVGO_GOOGL, AVGO_META, ETN_GNRC, GEV_GNRC, GNRC_PWR, GOOGL_MSFT,
    AMZN_MSFT, AMZN_GOOGL). Validating the real directory must be a clean,
    valid pass over all nine records, and must never mutate the directory or
    any of its contents."""
    assert Path("intelligence/relationships").exists()
    before = {
        stem: {
            "yaml": Path(f"intelligence/relationships/{stem}.yaml").read_text(),
            "md": Path(f"intelligence/relationships/{stem}.md").read_text(),
        }
        for stem in _REAL_RELATIONSHIP_STEMS
    }
    result = rv.validate_relationships_directory("intelligence/relationships")
    assert result.valid is True, [e for r in result.results for e in r.errors]
    assert result.record_count == len(_REAL_RELATIONSHIP_STEMS)
    for stem in _REAL_RELATIONSHIP_STEMS:
        assert Path(f"intelligence/relationships/{stem}.yaml").read_text() == before[stem]["yaml"]
        assert Path(f"intelligence/relationships/{stem}.md").read_text() == before[stem]["md"]


def test_validate_directory_does_not_mutate_source_files(tmp_path):
    path = _write_pair(tmp_path, "ZZZA_ZZZB", _directional_record())
    before_yaml = path.read_text()
    before_md = (tmp_path / "ZZZA_ZZZB.md").read_text()
    rv.validate_relationships_directory(tmp_path)
    assert path.read_text() == before_yaml
    assert (tmp_path / "ZZZA_ZZZB.md").read_text() == before_md


# ── static source guarantees ─────────────────────────────────────────────

def test_module_source_contains_no_write_mode_file_opens():
    """Static guarantee, not just behavioral: the module's source contains
    no open()/Path.open() call requesting write/append/update mode, and no
    os.mkdir/os.makedirs/Path.mkdir call. Mirrors
    test_intelligence_validator.py's identical guarantee."""
    with open(rv.__file__) as f:
        source = f.read()
    tree = ast.parse(source)
    write_modes = {"w", "a", "x", "w+", "a+", "r+", "wb", "ab", "xb"}
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            func = node.func
            name = getattr(func, "attr", None) or getattr(func, "id", None)
            if name in ("open",):
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


def test_relationship_validator_imports_no_allocator_margin_or_brokerage_code():
    imported = _imported_names(rv.__file__)
    for forbidden in ("allocate", "margin_state", "alpaca_client", "target_variants"):
        assert forbidden not in imported


def test_allocate_does_not_import_relationship_validator():
    imported = _imported_names("allocate.py")
    assert "relationship_validator" not in imported


def test_margin_state_does_not_import_relationship_validator():
    imported = _imported_names("margin_state.py")
    assert "relationship_validator" not in imported


def test_intelligence_validator_does_not_import_relationship_validator():
    """Zero coupling in either direction with the existing, separately
    authorized Company/Theme Intelligence validator, too — each domain's
    validator stays independent."""
    imported = _imported_names("intelligence_validator.py")
    assert "relationship_validator" not in imported


def test_relationship_validator_does_not_import_intelligence_validator():
    imported = _imported_names(rv.__file__)
    assert "intelligence_validator" not in imported
