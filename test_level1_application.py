"""XASSET-0022 -- fixtures and adversarial proof for the Level-1 application
artifact schema, canonical serializer, deterministic generator, and validator.

Every fixture is synthetic. No fixture is, or may become, an application
record or a policy result: nothing is written under `intelligence/`, the real
authorization registry stays empty, and the real artifact directory stays
absent.

Adversarial coverage maps to XASSET-0021 §M items 1-29.
"""

from __future__ import annotations

import copy
import json
from pathlib import Path
from types import MappingProxyType

import pytest

import level1_application_generator as G
import level1_application_schema as S
import level1_application_validator as V

REPO_ROOT = Path(__file__).resolve().parent

# A synthetic authorization decision that exists only inside these tests.
FAKE_AUTHORIZATION = "ZZ-FAKE-APPLICATION-AUTHORIZATION-0001"
FAKE_SCHEMA_HEAD = "0" * 40
FAKE_REGISTRY = MappingProxyType({FAKE_AUTHORIZATION: FAKE_SCHEMA_HEAD})


def _inputs() -> dict:
    return {
        "application_authorization": {
            "decision_id": FAKE_AUTHORIZATION,
            "authorization_status": "granted",
        },
        "schema_accepted_head": FAKE_SCHEMA_HEAD,
    }


def _register(monkeypatch, registry=FAKE_REGISTRY) -> None:
    """Inject a synthetic registry locally. Never persists to production."""
    monkeypatch.setattr(S, "APPLICATION_AUTHORIZATION_REGISTRY", registry)


@pytest.fixture
def authorized(monkeypatch):
    """Temporarily register a synthetic authorization so generation can run."""
    _register(monkeypatch)
    return _inputs()


@pytest.fixture
def document(authorized):
    return G.generate_application_document(authorized)


# ── Canonical artifact identity ──────────────────────────────────────────


def test_exactly_one_schema_identity():
    assert S.SCHEMA_NAME == "level1_application"
    assert S.SCHEMA_VERSION == "1.0"
    assert S.CANONICAL_ARTIFACT_PATH == (
        "intelligence/level1_application/level1_application.json"
    )
    assert S.FILE_FORMAT == "json"
    assert S.ENCODING == "utf-8"
    assert S.NEWLINE == "\n"


def test_canonical_bytes_are_sorted_compact_utf8_lf():
    raw = S.canonical_bytes({"b": 1, "a": None})
    assert raw == b'{"a":null,"b":1}\n'
    assert raw.endswith(b"\n")
    assert not raw.startswith(b"\xef\xbb\xbf")
    assert b"\r" not in raw


def test_canonical_serialization_matches_repository_convention():
    """Reuses the accepted convention rather than inventing a second one."""
    payload = {"z": "é", "a": [3, 1]}
    expected = json.dumps(
        payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ) + "\n"
    assert S.canonical_text(payload) == expected


def test_canonical_serializer_rejects_nan_and_infinity():
    with pytest.raises(ValueError):
        S.canonical_bytes({"x": float("nan")})
    with pytest.raises(ValueError):
        S.canonical_bytes({"x": float("inf")})


# ── Frozen evidence manifest ─────────────────────────────────────────────


def test_frozen_snapshot_is_exactly_thirty_five_sources():
    assert S.FROZEN_EVIDENCE_COUNT == 35
    ids = [row[0] for row in S.FROZEN_EVIDENCE]
    assert len(set(ids)) == 35


def test_frozen_snapshot_hashes_match_the_live_repository_tree():
    """Independent re-verification of the transcribed XASSET-0021 §C table."""
    from hashlib import sha256

    for _eid, path, expected, _content in S.FROZEN_EVIDENCE:
        target = REPO_ROOT / path
        assert target.exists(), f"frozen evidence path missing: {path}"
        assert sha256(target.read_bytes()).hexdigest() == expected, path


def test_evidence_manifest_identity_is_derived_not_authored():
    assert S.EVIDENCE_MANIFEST_SHA256 == S.evidence_manifest_sha256()
    assert len(S.EVIDENCE_MANIFEST_SHA256) == 64


# ── Canonical orders ─────────────────────────────────────────────────────


def test_canonical_sleeve_and_pair_orders():
    assert S.CANONICAL_SLEEVE_ORDER == (
        "equity", "fund_broad_market", "fund_gld_defensive", "crypto",
    )
    assert S.CANONICAL_PAIR_ORDER == (
        "equity__fund_broad_market",
        "equity__fund_gld_defensive",
        "equity__crypto",
        "fund_broad_market__fund_gld_defensive",
        "fund_broad_market__crypto",
        "fund_gld_defensive__crypto",
    )
    assert len(set(S.CANONICAL_PAIR_ORDER)) == 6


def test_driver_direction_vocabulary_has_no_not_applicable():
    """XASSET-0021 §D bars marking a driver class inapplicable."""
    assert "not_applicable" not in S.DRIVER_DIRECTION
    assert S.DRIVER_DIRECTION == {
        "favors_self", "favors_counterpart", "unable_to_determine",
    }


def test_trace_and_reopen_trigger_sets_are_closed():
    assert len(S.CANONICAL_TRACE_STEP_ORDER) == 11
    assert len(set(S.CANONICAL_TRACE_STEP_ORDER)) == 11
    assert set(S.TRACE_STEP_REQUIRED_OUTPUT) == set(S.CANONICAL_TRACE_STEP_ORDER)
    assert len(S.CANONICAL_REOPEN_TRIGGER_ORDER) == 7
    assert len(set(S.CANONICAL_REOPEN_TRIGGER_ORDER)) == 7


# ── Application-authority gate (the double gate) ─────────────────────────


def test_real_authorization_registry_is_empty():
    assert len(S.APPLICATION_AUTHORIZATION_REGISTRY) == 0
    assert dict(S.APPLICATION_AUTHORIZATION_REGISTRY) == {}


def test_generation_refuses_without_a_registered_authorization():
    with pytest.raises(G.GeneratorInputError, match="WITHHELD"):
        G.generate_application_document(_inputs())


def test_validation_rejects_an_unregistered_authorization(monkeypatch, document):
    """A structurally perfect artifact still fails under the real empty registry."""
    _register(monkeypatch, MappingProxyType({}))
    result = V.validate_application_document(document)
    assert not result.valid
    assert any("WITHHELD" in e for e in result.errors)


def test_validation_rejects_status_other_than_granted(authorized, document):
    doc = copy.deepcopy(document)
    doc["application_authorization"]["authorization_status"] = "withheld"
    result = V.validate_application_document(doc)
    assert not result.valid


def test_real_artifact_directory_does_not_exist():
    assert not (REPO_ROOT / "intelligence" / "level1_application").exists()


def test_missing_directory_is_a_valid_zero_coverage_state():
    result = V.validate_level1_application_directory(
        REPO_ROOT / "intelligence" / "level1_application"
    )
    assert result.valid
    assert result.record_count == 0


# ── Determinism (§L item 9, §M item 29) ──────────────────────────────────


def test_identical_frozen_inputs_produce_identical_bytes(authorized):
    first = G.generate_application_bytes(copy.deepcopy(authorized))
    second = G.generate_application_bytes(copy.deepcopy(authorized))
    assert first == second


def test_generation_is_invariant_to_input_mapping_insertion_order(authorized):
    baseline = G.generate_application_bytes(copy.deepcopy(authorized))
    shuffled = {
        "schema_accepted_head": authorized["schema_accepted_head"],
        "application_authorization": {
            "authorization_status": "granted",
            "decision_id": FAKE_AUTHORIZATION,
        },
    }
    assert G.generate_application_bytes(shuffled) == baseline


def test_canonical_bytes_contain_no_wall_clock_or_author_metadata(document):
    """Structural check on key names, plus substrings that cannot false-positive.

    Deliberately not a loose substring scan for `author`: the schema's own
    legitimate `governing_authority` / `authority_lifecycle` /
    `authority_boundary` fields contain it.
    """
    keys = {key for _where, key in V._iter_keys(document, "$")}
    assert keys.isdisjoint(V._NONDETERMINISTIC_KEY_NAMES)
    text = S.canonical_text(document).lower()
    for token in ("generated_at", "timestamp", "hostname", "frozen_at", "reviewer"):
        assert token not in text


def test_generated_document_carries_no_float(document):
    assert not S.contains_float(document)


# ── Structural validity of the generated document ────────────────────────


def test_generated_document_passes_every_check_except_the_authority_gate(document):
    result = V.validate_application_document(document)
    non_authority = [e for e in result.errors if "WITHHELD" not in e]
    assert non_authority == []


def _valid_bytes(monkeypatch, document):
    """Bytes that validate cleanly once the synthetic authorization is registered."""
    _register(monkeypatch)
    return S.canonical_bytes(document)


def test_canonical_bytes_round_trip_validate(monkeypatch, document):
    raw = _valid_bytes(monkeypatch, document)
    assert V.validate_application_bytes(raw).valid


# ── §M adversarial rejection fixtures ────────────────────────────────────


def _assert_rejected(monkeypatch, document, mutate):
    _register(monkeypatch)
    doc = copy.deepcopy(document)
    mutate(doc)
    result = V.validate_application_document(doc)
    assert not result.valid, "mutation was accepted but must be rejected"
    return result


def _set_methodology_head(doc):
    doc["methodology_identity"]["accepted_head"] = "f" * 40


def _set_evidence_path(doc):
    doc["evidence_snapshot"][0]["path"] = "intelligence/some_other_file.yaml"


def _set_evidence_hash(doc):
    doc["evidence_snapshot"][0]["sha256"] = "0" * 64


def _set_content_hash(doc):
    doc["evidence_snapshot"][0]["source_content_sha256"] = "0" * 64


def _unfrozen_evidence_class(doc):
    doc["evidence_snapshot"][0]["evidence_id"] = "NOT_A_FROZEN_EVIDENCE_ID"


def _drop_sleeve(doc):
    doc["sleeves"].pop()


def _duplicate_pair(doc):
    doc["pairs"][1] = copy.deepcopy(doc["pairs"][0])


def _reverse_pair(doc):
    pair = doc["pairs"][0]
    pair["self_sleeve"], pair["counterpart_sleeve"] = (
        pair["counterpart_sleeve"], pair["self_sleeve"],
    )


def _missing_treated_as_neutral(doc):
    doc["pairs"][3]["driver_ledger"][0]["direction"] = "favors_self"


def _transitive_inference(doc):
    doc["pairs"][3]["conclusion"] = "favors_self"


def _risk_state_as_direction(doc):
    doc["sleeves"][0]["uncertainty_state"] = "determinate"


def _historical_target_as_endpoint(doc):
    doc["sleeves"][0]["point_or_range_or_null"] = {"point": "18.67"}


def _automatic_midpoint(doc):
    doc["sleeves"][1]["outcome_type"] = "point"


def _rounding_float(doc):
    doc["sleeves"][0]["point_or_range_or_null"] = 0.1867


def _unclosed_judgment(doc):
    doc["evidence_snapshot"][0]["governing_authority"] = "material_and_significant"


def _historical_as_current_driver(doc):
    doc["pairs"][0]["driver_ledger"][0]["direction"] = "favors_counterpart"


def _unassigned_becomes_cash(doc):
    doc["portfolio_reconciliation"]["unsized_unassigned_capital"]["symbol"] = "CASH"


def _forced_exhaustion(doc):
    doc["portfolio_reconciliation"]["reconciliation_state"] = "invalid_requires_plug"


def _liquidity_zero(doc):
    doc["normalized_asset_state"]["separately_governed_liquidity_state"][
        "numeric_value"] = 0


def _liquidity_fifth_sleeve(doc):
    doc["sleeves"].append(copy.deepcopy(doc["sleeves"][0]))


def _current_holdings_prior(doc):
    doc["evidence_snapshot"][0]["authority_lifecycle"] = "derived_from_holdings.yaml"


def _hidden_score(doc):
    doc["sleeves"][0]["score"] = "high"


def _level2_leakage(doc):
    doc["evidence_snapshot"][0]["governing_authority"] = "level 2 membership"


def _policy_language(doc):
    doc["evidence_snapshot"][0]["governing_authority"] = "adopt this allocation"


def _extra_top_level_field(doc):
    doc["unexpected_field"] = "x"


def _omitted_required_field(doc):
    del doc["authority_boundary"]


def _wrong_type(doc):
    doc["sleeves"] = "not-a-list"


def _invalid_enum(doc):
    doc["sleeves"][0]["outcome_type"] = "maybe"


def _free_text_for_enum(doc):
    doc["pairs"][0]["conclusion"] = "probably unable to determine"


def _reordered_list(doc):
    doc["sleeves"].reverse()


def _reordered_driver_ledger(doc):
    doc["pairs"][0]["driver_ledger"].reverse()


def _trace_step_removed(doc):
    doc["sleeves"][0]["deterministic_derivation_trace"].pop()


def _trace_step_reordered(doc):
    trace = doc["sleeves"][0]["deterministic_derivation_trace"]
    trace[0], trace[1] = trace[1], trace[0]


def _trace_step_free_text(doc):
    doc["sleeves"][0]["deterministic_derivation_trace"][0]["output_recorded"] = "looked fine"


def _reopen_trigger_added(doc):
    doc["reopen_triggers"].append("author_felt_like_it")


def _reopen_trigger_reordered(doc):
    doc["reopen_triggers"].reverse()


def _schema_name_drift(doc):
    doc["schema_identity"]["schema_name"] = "level1_application_v2"


def _schema_version_drift(doc):
    doc["schema_identity"]["schema_version"] = "2.0"


def _self_referential_sha(doc):
    doc["application_authorization"]["exact_head"] = "a" * 40


@pytest.mark.parametrize("mutate,label", [
    (_set_methodology_head, "M1 methodology identity drift"),
    (_set_evidence_path, "M1 path drift"),
    (_set_evidence_hash, "M1 file-hash drift"),
    (_set_content_hash, "M1 content-hash drift"),
    (_unfrozen_evidence_class, "M2 evidence class not frozen"),
    (_drop_sleeve, "M3 missing sleeve"),
    (_duplicate_pair, "M3 duplicate pair"),
    (_reverse_pair, "M3 reversed pair"),
    (_missing_treated_as_neutral, "M4 missing evidence as neutral"),
    (_transitive_inference, "M5 transitive pair inference"),
    (_risk_state_as_direction, "M6 RISK state as direction"),
    (_historical_target_as_endpoint, "M7 historical target as endpoint"),
    (_automatic_midpoint, "M8 automatic point selection"),
    (_rounding_float, "M9 rounding/float"),
    (_unclosed_judgment, "M10 unclosed judgment"),
    (_historical_as_current_driver, "M11 historical as current driver"),
    (_unassigned_becomes_cash, "M12 unassigned becomes cash"),
    (_forced_exhaustion, "M13 forced exhaustion / plug"),
    (_liquidity_zero, "M14 liquidity as numeric zero"),
    (_liquidity_fifth_sleeve, "M14 fifth sleeve"),
    (_current_holdings_prior, "M16 current holdings prior"),
    (_hidden_score, "M17 hidden score"),
    (_level2_leakage, "M18 Level-2 leakage"),
    (_policy_language, "M19 policy language"),
    (_extra_top_level_field, "M20 extra field"),
    (_omitted_required_field, "M20 omitted required field"),
    (_wrong_type, "M21 wrong type"),
    (_invalid_enum, "M21 invalid enum"),
    (_free_text_for_enum, "M21 free text for enum"),
    (_reordered_list, "M22 reordered sleeve list"),
    (_reordered_driver_ledger, "M22 reordered driver ledger"),
    (_trace_step_removed, "M25 trace step removed"),
    (_trace_step_reordered, "M25 trace step reordered"),
    (_trace_step_free_text, "M25 trace free text"),
    (_reopen_trigger_added, "M26 reopen trigger added"),
    (_reopen_trigger_reordered, "M26 reopen trigger reordered"),
    (_schema_name_drift, "M27 schema name drift"),
    (_schema_version_drift, "M27 schema version drift"),
    (_self_referential_sha, "M28 self-referential SHA"),
])
def test_adversarial_mutation_is_rejected(monkeypatch, document, mutate, label):
    _assert_rejected(monkeypatch, document, mutate)


# ── §M items 23/24/29: byte-level rejection ──────────────────────────────


def test_pretty_printed_bytes_are_rejected(monkeypatch, document):
    _register(monkeypatch)
    raw = (json.dumps(document, indent=2, sort_keys=True) + "\n").encode("utf-8")
    result = V.validate_application_bytes(raw)
    assert not result.valid
    assert any("canonical serialization" in e for e in result.errors)


def test_crlf_bytes_are_rejected(monkeypatch, document):
    raw = _valid_bytes(monkeypatch, document).replace(b"\n", b"\r\n")
    result = V.validate_application_bytes(raw)
    assert not result.valid
    assert any("LF only" in e for e in result.errors)


def test_bom_is_rejected(monkeypatch, document):
    raw = b"\xef\xbb\xbf" + _valid_bytes(monkeypatch, document)
    result = V.validate_application_bytes(raw)
    assert not result.valid
    assert any("BOM" in e for e in result.errors)


def test_missing_trailing_newline_is_rejected(monkeypatch, document):
    raw = _valid_bytes(monkeypatch, document).rstrip(b"\n")
    assert not V.validate_application_bytes(raw).valid


def test_reordered_keys_are_rejected(monkeypatch, document):
    _register(monkeypatch)
    raw = (json.dumps(document, sort_keys=False, separators=(",", ":"),
                      ensure_ascii=False) + "\n").encode("utf-8")
    if raw != S.canonical_bytes(document):
        assert not V.validate_application_bytes(raw).valid


def test_duplicate_json_key_is_rejected(monkeypatch, document):
    _register(monkeypatch)
    raw = b'{"a":1,"a":2}\n'
    result = V.validate_application_bytes(raw)
    assert not result.valid
    assert any("duplicate key" in e for e in result.errors)


def test_alternate_null_encoding_is_rejected(monkeypatch, document):
    _assert_rejected(
        monkeypatch, document,
        lambda d: d["normalized_asset_state"][
            "separately_governed_liquidity_state"].__setitem__("numeric_value", "null"),
    )


def test_regeneration_is_byte_identical_and_validates(monkeypatch, authorized):
    _register(monkeypatch)
    runs = {G.generate_application_bytes(copy.deepcopy(authorized)) for _ in range(5)}
    assert len(runs) == 1
    assert V.validate_application_bytes(runs.pop()).valid


# ── Generator input discipline ───────────────────────────────────────────


def test_generator_rejects_extra_input_key(authorized):
    bad = dict(authorized)
    bad["surprise"] = 1
    with pytest.raises(G.GeneratorInputError, match="unknown"):
        G.generate_application_document(bad)


def test_generator_rejects_missing_input_key(authorized):
    bad = dict(authorized)
    del bad["schema_accepted_head"]
    with pytest.raises(G.GeneratorInputError, match="missing"):
        G.generate_application_document(bad)


def test_generator_rejects_invalid_schema_head(authorized):
    bad = copy.deepcopy(authorized)
    bad["schema_accepted_head"] = "not-a-sha"
    with pytest.raises(G.GeneratorInputError, match="40-hex"):
        G.generate_application_document(bad)


# ── Isolation ────────────────────────────────────────────────────────────


def test_no_allocator_or_margin_coupling():
    import ast

    for module in ("level1_application_schema.py", "level1_application_generator.py",
                   "level1_application_validator.py"):
        tree = ast.parse((REPO_ROOT / module).read_text())
        imported: list[str] = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported += [a.name for a in node.names]
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported.append(node.module)
        assert "allocate" not in imported, module
        assert "margin_state" not in imported, module
        assert "levels" not in imported, module


def test_modules_never_read_portfolio_configuration():
    for module in ("level1_application_schema.py", "level1_application_generator.py",
                   "level1_application_validator.py"):
        text = (REPO_ROOT / module).read_text()
        for forbidden in ("holdings.yaml", "targets.yaml", "gates.yaml",
                          "issuer_lookthrough.yaml"):
            # Only the validator's forbidden-token list may name these.
            occurrences = text.count(forbidden)
            if module == "level1_application_validator.py":
                assert occurrences <= 1, f"{module} names {forbidden} more than once"
            else:
                assert occurrences == 0, f"{module} names {forbidden}"


# ── Review 4944055540 regressions ────────────────────────────────────────
#
# MAJOR-1: author-discretionary evidence provenance
# MAJOR-2: bool/int type confusion
# MINOR-1: NaN/Infinity crash path
# MINOR-2: schema_accepted_head not bound to the authorization


def test_major1_evidence_ledger_is_fully_derived_zero_caller_discretion():
    """No per-evidence input exists at all, so nothing can be phrased."""
    assert G.GENERATOR_INPUT_KEYS == {"application_authorization", "schema_accepted_head"}
    assert not hasattr(G, "EVIDENCE_ATTRIBUTE_KEYS")


def test_major1_removed_free_prose_fields_are_not_in_the_schema():
    for removed in ("permitted_question", "representation_scope",
                    "forbidden_implications", "classification", "admission",
                    "freshness_state"):
        assert removed not in S.EVIDENCE_ENTRY_KEYS, removed


def test_major1_source_class_partition_matches_xasset0021_c1():
    """Exactly the six §C.1 source classes, covering all 35 items."""
    from collections import Counter

    counts = Counter(e["source_class"] for e in S.FROZEN_EVIDENCE_LEDGER)
    assert counts == {
        S.SOURCE_CLASS_PROFILES_AND_RELATIONSHIPS: 8,
        S.SOURCE_CLASS_INSTRUMENT_ECONOMICS: 6,
        S.SOURCE_CLASS_GLD: 2,
        S.SOURCE_CLASS_OVERLAP: 4,
        S.SOURCE_CLASS_EQUITY_VALUATION: 1,
        S.SOURCE_CLASS_RISK: 14,
    }
    assert sum(counts.values()) == 35


@pytest.mark.parametrize("field", sorted({
    "evidence_id", "path", "sha256", "source_content_sha256",
    "source_class", "governing_authority", "authority_lifecycle",
}))
def test_major1_every_evidence_field_mutation_is_rejected(monkeypatch, document, field):
    _register(monkeypatch)
    doc = copy.deepcopy(document)
    doc["evidence_snapshot"][0][field] = "MUTATED"
    assert not V.validate_application_document(doc).valid


def test_major1_evidence_field_omission_is_rejected(monkeypatch, document):
    _register(monkeypatch)
    doc = copy.deepcopy(document)
    del doc["evidence_snapshot"][0]["governing_authority"]
    assert not V.validate_application_document(doc).valid


def test_major1_extra_evidence_field_is_rejected(monkeypatch, document):
    _register(monkeypatch)
    doc = copy.deepcopy(document)
    doc["evidence_snapshot"][0]["permitted_question"] = "anything"
    assert not V.validate_application_document(doc).valid


def test_major1_exactly_one_lawful_byte_sequence(monkeypatch, authorized):
    """The reviewer's attack: many valid byte sequences for one governed state."""
    _register(monkeypatch)
    baseline = G.generate_application_bytes(copy.deepcopy(authorized))
    assert V.validate_application_bytes(baseline).valid

    variants = set()
    for value in ("XASSET-0012", "other", "XASSET-0012, XASSET-0013 "):
        for field in ("governing_authority", "authority_lifecycle", "source_class"):
            doc = json.loads(baseline.decode())
            doc["evidence_snapshot"][0][field] = value
            if V.validate_application_document(doc).valid:
                variants.add(S.canonical_bytes(doc))
    assert variants == set(), "more than one lawful byte sequence survives"


def test_major1_reordered_evidence_entries_are_rejected(monkeypatch, document):
    _register(monkeypatch)
    doc = copy.deepcopy(document)
    doc["evidence_snapshot"].reverse()
    assert not V.validate_application_document(doc).valid


@pytest.mark.parametrize("path,substitute", [
    (("normalized_asset_state", "debt_excluded"), 1),
    (("authority_boundary", "provisional_not_adopted"), 1),
    (("authority_boundary", "no_policy_effect"), 1),
    (("authority_boundary", "no_level2_effect"), 1),
    (("authority_boundary", "no_liquidity_or_debt_effect"), 1),
])
def test_major2_true_cannot_be_encoded_as_one(monkeypatch, document, path, substitute):
    _register(monkeypatch)
    doc = copy.deepcopy(document)
    doc[path[0]][path[1]] = substitute
    assert not V.validate_application_document(doc).valid


@pytest.mark.parametrize("substitute", [False, True])
def test_major2_step_index_cannot_be_a_bool(monkeypatch, document, substitute):
    """step_index 0 -> False and 1 -> True must both be rejected."""
    _register(monkeypatch)
    doc = copy.deepcopy(document)
    index = 0 if substitute is False else 1
    doc["sleeves"][0]["deterministic_derivation_trace"][index]["step_index"] = substitute
    assert not V.validate_application_document(doc).valid


def test_major2_source_count_cannot_be_a_bool(monkeypatch, document):
    _register(monkeypatch)
    doc = copy.deepcopy(document)
    doc["evidence_snapshot_identity"]["source_count"] = True
    assert not V.validate_application_document(doc).valid


def test_major2_bool_where_string_expected_is_rejected(monkeypatch, document):
    _register(monkeypatch)
    doc = copy.deepcopy(document)
    doc["schema_identity"]["schema_name"] = True
    assert not V.validate_application_document(doc).valid


def test_major2_require_exact_is_type_strict_directly():
    errors: list[str] = []
    V._require_exact(1, "$.x", True, errors)
    V._require_exact(True, "$.y", 1, errors)
    V._require_exact(0, "$.z", False, errors)
    V._require_exact(False, "$.w", 0, errors)
    assert len(errors) == 4
    ok: list[str] = []
    V._require_exact(True, "$.a", True, ok)
    V._require_exact(0, "$.b", 0, ok)
    V._require_exact(None, "$.c", None, ok)
    assert ok == []


@pytest.mark.parametrize("literal", ["NaN", "Infinity", "-Infinity"])
def test_minor1_non_standard_constants_return_structured_failure(literal):
    raw = ('{"x":%s}\n' % literal).encode("utf-8")
    result = V.validate_application_bytes(raw)
    assert not result.valid
    assert any("non-standard JSON constant" in e for e in result.errors)


@pytest.mark.parametrize("literal", ["NaN", "Infinity", "-Infinity"])
def test_minor1_non_standard_constants_nested_in_a_real_artifact(monkeypatch, document, literal):
    _register(monkeypatch)
    text = S.canonical_text(document).rstrip("\n")
    injected = (text[:-1] + ',"x":%s}\n' % literal).encode("utf-8")
    result = V.validate_application_bytes(injected)
    assert not result.valid


def test_minor2_registry_binds_decision_to_exact_schema_head(monkeypatch, authorized):
    _register(monkeypatch)
    doc = G.generate_application_document(copy.deepcopy(authorized))
    assert V.validate_application_document(doc).valid


def test_minor2_wrong_valid_head_for_registered_id_is_rejected(monkeypatch, authorized):
    _register(monkeypatch)
    doc = G.generate_application_document(copy.deepcopy(authorized))
    doc["prerequisite_identity"]["schema_accepted_head"] = "b" * 40
    result = V.validate_application_document(doc)
    assert not result.valid
    assert any("registry" in e for e in result.errors)


def test_minor2_generator_refuses_wrong_head_for_registered_id(monkeypatch):
    _register(monkeypatch)
    bad = _inputs()
    bad["schema_accepted_head"] = "c" * 40
    with pytest.raises(G.GeneratorInputError, match="does not match the head bound"):
        G.generate_application_document(bad)


def test_minor2_unknown_decision_id_is_rejected(monkeypatch):
    _register(monkeypatch)
    bad = _inputs()
    bad["application_authorization"]["decision_id"] = "ZZ-NOT-REGISTERED"
    with pytest.raises(G.GeneratorInputError, match="not registered"):
        G.generate_application_document(bad)


def test_minor2_correct_head_with_wrong_decision_id_is_rejected(monkeypatch, document):
    _register(monkeypatch)
    doc = copy.deepcopy(document)
    doc["application_authorization"]["decision_id"] = "ZZ-OTHER"
    result = V.validate_application_document(doc)
    assert not result.valid
    assert any("WITHHELD" in e for e in result.errors)


@pytest.mark.parametrize("variant", [
    " ZZ-FAKE-APPLICATION-AUTHORIZATION-0001",
    "ZZ-FAKE-APPLICATION-AUTHORIZATION-0001 ",
    "zz-fake-application-authorization-0001",
    "ZZ-FAKE-APPLICATION-AUTHORIZATION-000",
])
def test_minor2_malformed_decision_ids_are_rejected(monkeypatch, variant):
    _register(monkeypatch)
    bad = _inputs()
    bad["application_authorization"]["decision_id"] = variant
    with pytest.raises(G.GeneratorInputError):
        G.generate_application_document(bad)


def test_minor2_production_registry_refuses_everything(monkeypatch, document):
    """With the real empty registry nothing validates, whatever the head."""
    _register(monkeypatch, MappingProxyType({}))
    for head in ("0" * 40, "a" * 40, S.CLOSURE_IDENTITY["accepted_head"]):
        doc = copy.deepcopy(document)
        doc["prerequisite_identity"]["schema_accepted_head"] = head
        assert not V.validate_application_document(doc).valid
