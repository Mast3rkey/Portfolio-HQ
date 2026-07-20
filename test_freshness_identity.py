"""Tests for freshness_identity.py (AUTO-0002 bounded local-foundation
scope)."""

import ast
import re
from datetime import date, datetime
from pathlib import Path

import pytest

import freshness_identity as fid

FP_A = "a" * 64
FP_B = "b" * 64

_HEX64 = re.compile(r"^[0-9a-f]{64}$")


# ── golden vectors (deterministic, hand-computed via the module itself,
#    pinned here to catch any accidental future drift in the hashing
#    contract) ─────────────────────────────────────────────────────────────

def test_cadence_fingerprint_golden_vector():
    result = fid.compute_cadence_fingerprint(ticker="COST", next_due="2026-07-19", template_version="v1")
    assert _HEX64.match(result)
    # Pinned literal value for the exact canonical payload
    # [["fingerprint_type","cadence_v1"],["ticker","COST"],["next_due","2026-07-19"],["template_version","v1"]]
    import hashlib, json
    expected_payload = json.dumps(
        [
            ["fingerprint_type", "cadence_v1"],
            ["ticker", "COST"],
            ["next_due", "2026-07-19"],
            ["template_version", "v1"],
        ],
        ensure_ascii=True,
        separators=(",", ":"),
    )
    expected = hashlib.sha256(expected_payload.encode("utf-8")).hexdigest()
    assert result == expected


def test_task_instance_id_golden_vector():
    result = fid.compute_task_instance_id(
        ticker="COST", episode_id="ep-1",
        fingerprint_assignments=[(FP_A, 1), (FP_B, 2)],
        template_version="v1",
    )
    assert _HEX64.match(result)
    import hashlib, json
    expected_payload = json.dumps(
        [
            ["fingerprint_type", "task_instance_v1"],
            ["ticker", "COST"],
            ["episode_id", "ep-1"],
            ["fingerprint_assignments", [[FP_A, 1], [FP_B, 2]]],
            ["template_version", "v1"],
        ],
        ensure_ascii=True,
        separators=(",", ":"),
    )
    expected = hashlib.sha256(expected_payload.encode("utf-8")).hexdigest()
    assert result == expected


# ── domain separation ────────────────────────────────────────────────────────

def test_cadence_and_task_instance_never_collide_on_similar_inputs():
    cadence = fid.compute_cadence_fingerprint(ticker="COST", next_due="2026-07-19", template_version="v1")
    # deliberately unrelated inputs -- domain separation alone (fingerprint_type
    # as first field) guarantees no accidental cross-domain equality for any
    # input, which we spot-check here.
    task = fid.compute_task_instance_id(
        ticker="COST", episode_id="2026-07-19", fingerprint_assignments=[(FP_A, 1)], template_version="v1"
    )
    assert cadence != task


# ── order independence / determinism ────────────────────────────────────────

def test_task_instance_id_independent_of_input_pair_order():
    a = fid.compute_task_instance_id(
        ticker="COST", episode_id="ep-1", fingerprint_assignments=[(FP_A, 1), (FP_B, 2)], template_version="v1"
    )
    b = fid.compute_task_instance_id(
        ticker="COST", episode_id="ep-1", fingerprint_assignments=[(FP_B, 2), (FP_A, 1)], template_version="v1"
    )
    assert a == b


def test_task_instance_id_independent_of_outer_container_type():
    as_list = fid.compute_task_instance_id(
        ticker="COST", episode_id="ep-1", fingerprint_assignments=[(FP_A, 1)], template_version="v1"
    )
    as_tuple = fid.compute_task_instance_id(
        ticker="COST", episode_id="ep-1", fingerprint_assignments=((FP_A, 1),), template_version="v1"
    )
    assert as_list == as_tuple


def test_task_instance_id_independent_of_pair_container_type():
    as_tuple_pairs = fid.compute_task_instance_id(
        ticker="COST", episode_id="ep-1", fingerprint_assignments=[(FP_A, 1)], template_version="v1"
    )
    as_list_pairs = fid.compute_task_instance_id(
        ticker="COST", episode_id="ep-1", fingerprint_assignments=[[FP_A, 1]], template_version="v1"
    )
    assert as_tuple_pairs == as_list_pairs


# ── differing inputs produce differing output ───────────────────────────────

def test_differing_ticker_changes_cadence_fingerprint():
    a = fid.compute_cadence_fingerprint(ticker="COST", next_due="2026-07-19", template_version="v1")
    b = fid.compute_cadence_fingerprint(ticker="XOM", next_due="2026-07-19", template_version="v1")
    assert a != b


def test_differing_next_due_changes_cadence_fingerprint():
    a = fid.compute_cadence_fingerprint(ticker="COST", next_due="2026-07-19", template_version="v1")
    b = fid.compute_cadence_fingerprint(ticker="COST", next_due="2026-07-20", template_version="v1")
    assert a != b


def test_differing_template_version_changes_cadence_fingerprint():
    a = fid.compute_cadence_fingerprint(ticker="COST", next_due="2026-07-19", template_version="v1")
    b = fid.compute_cadence_fingerprint(ticker="COST", next_due="2026-07-19", template_version="v2")
    assert a != b


def test_differing_episode_id_changes_task_instance_id():
    a = fid.compute_task_instance_id(ticker="COST", episode_id="ep-1", fingerprint_assignments=[(FP_A, 1)], template_version="v1")
    b = fid.compute_task_instance_id(ticker="COST", episode_id="ep-2", fingerprint_assignments=[(FP_A, 1)], template_version="v1")
    assert a != b


def test_differing_ordinal_changes_task_instance_id():
    a = fid.compute_task_instance_id(ticker="COST", episode_id="ep-1", fingerprint_assignments=[(FP_A, 1)], template_version="v1")
    b = fid.compute_task_instance_id(ticker="COST", episode_id="ep-1", fingerprint_assignments=[(FP_A, 2)], template_version="v1")
    assert a != b


def test_differing_fingerprint_changes_task_instance_id():
    a = fid.compute_task_instance_id(ticker="COST", episode_id="ep-1", fingerprint_assignments=[(FP_A, 1)], template_version="v1")
    b = fid.compute_task_instance_id(ticker="COST", episode_id="ep-1", fingerprint_assignments=[(FP_B, 1)], template_version="v1")
    assert a != b


# ── Unicode NFC equivalence ──────────────────────────────────────────────────

def test_unicode_nfc_equivalence_for_ticker():
    # "é" as a single codepoint (NFC) vs "e" + combining acute (NFD)
    nfc = "COSTé"
    nfd = "COST" + "é"
    a = fid.compute_cadence_fingerprint(ticker=nfc, next_due="2026-07-19", template_version="v1")
    b = fid.compute_cadence_fingerprint(ticker=nfd, next_due="2026-07-19", template_version="v1")
    assert a == b


def test_unicode_nfc_equivalence_for_episode_id_and_template_version():
    nfc = "épisode"
    nfd = "épisode"
    a = fid.compute_task_instance_id(ticker="COST", episode_id=nfc, fingerprint_assignments=[(FP_A, 1)], template_version="v1")
    b = fid.compute_task_instance_id(ticker="COST", episode_id=nfd, fingerprint_assignments=[(FP_A, 1)], template_version="v1")
    assert a == b


# ── empty strings ────────────────────────────────────────────────────────────

@pytest.mark.parametrize("field", ["ticker", "episode_id", "template_version"])
def test_empty_string_rejected_for_task_instance_string_fields(field):
    kwargs = dict(ticker="COST", episode_id="ep-1", fingerprint_assignments=[(FP_A, 1)], template_version="v1")
    kwargs[field] = ""
    with pytest.raises(ValueError):
        fid.compute_task_instance_id(**kwargs)


@pytest.mark.parametrize("field", ["ticker", "template_version"])
def test_empty_string_rejected_for_cadence_string_fields(field):
    kwargs = dict(ticker="COST", next_due="2026-07-19", template_version="v1")
    kwargs[field] = ""
    with pytest.raises(ValueError):
        fid.compute_cadence_fingerprint(**kwargs)


def test_whitespace_only_string_is_not_treated_as_empty():
    # Only emptiness AFTER NFC normalization is rejected (AUTO-0002 Decision
    # §3 step 3) -- no .strip() rule was specified for these fields, unlike
    # the validator's non-empty-string fields, so whitespace-only is valid.
    result = fid.compute_cadence_fingerprint(ticker="   ", next_due="2026-07-19", template_version="v1")
    assert _HEX64.match(result)


# ── exact C0/C1 control-character boundary ──────────────────────────────────

@pytest.mark.parametrize("code", [0x00, 0x09, 0x1F, 0x7F, 0x80, 0x9F])
def test_control_characters_rejected_at_exact_boundary(code):
    bad = f"COST{chr(code)}"
    with pytest.raises(ValueError):
        fid.compute_cadence_fingerprint(ticker=bad, next_due="2026-07-19", template_version="v1")


@pytest.mark.parametrize("code", [0x20, 0x7E, 0xA0])
def test_characters_just_outside_control_ranges_accepted(code):
    ok = f"COST{chr(code)}"
    result = fid.compute_cadence_fingerprint(ticker=ok, next_due="2026-07-19", template_version="v1")
    assert _HEX64.match(result)


def test_char_0x9e_is_within_c1_range_and_rejected():
    bad = f"COST{chr(0x9E)}"
    with pytest.raises(ValueError):
        fid.compute_cadence_fingerprint(ticker=bad, next_due="2026-07-19", template_version="v1")


# ── date object / string equivalence, datetime rejection, malformed dates ──

def test_date_object_and_equivalent_string_produce_same_fingerprint():
    a = fid.compute_cadence_fingerprint(ticker="COST", next_due=date(2026, 7, 19), template_version="v1")
    b = fid.compute_cadence_fingerprint(ticker="COST", next_due="2026-07-19", template_version="v1")
    assert a == b


def test_datetime_rejected_for_next_due():
    with pytest.raises(ValueError):
        fid.compute_cadence_fingerprint(ticker="COST", next_due=datetime(2026, 7, 19, 1, 2, 3), template_version="v1")


@pytest.mark.parametrize("bad_date", ["2026/07/19", "07-19-2026", "2026-13-01", "not-a-date", "2026-7-19", 12345, None])
def test_malformed_or_wrong_type_date_rejected(bad_date):
    with pytest.raises(ValueError):
        fid.compute_cadence_fingerprint(ticker="COST", next_due=bad_date, template_version="v1")


# ── invalid outer-container types for fingerprint_assignments ──────────────

@pytest.mark.parametrize("bad_outer", [
    "a-string",
    b"bytes",
    bytearray(b"bytearray"),
    {FP_A, FP_B},          # set
    frozenset({FP_A}),      # frozenset
    {FP_A: 1},               # mapping
    42,                        # scalar
    None,
])
def test_invalid_outer_container_types_rejected(bad_outer):
    with pytest.raises(ValueError):
        fid.compute_task_instance_id(ticker="COST", episode_id="ep-1", fingerprint_assignments=bad_outer, template_version="v1")


def test_generator_outer_container_rejected():
    def gen():
        yield (FP_A, 1)
    with pytest.raises(ValueError):
        fid.compute_task_instance_id(ticker="COST", episode_id="ep-1", fingerprint_assignments=gen(), template_version="v1")


def test_empty_outer_container_rejected():
    with pytest.raises(ValueError):
        fid.compute_task_instance_id(ticker="COST", episode_id="ep-1", fingerprint_assignments=[], template_version="v1")


# ── invalid pair-container types and lengths ────────────────────────────────

@pytest.mark.parametrize("bad_pair", [
    "ab",           # str
    b"ab",           # bytes
    bytearray(b"ab"),  # bytearray
    42,                 # scalar, not a Sequence
    {FP_A: 1},           # mapping
])
def test_invalid_pair_container_types_rejected(bad_pair):
    with pytest.raises(ValueError):
        fid.compute_task_instance_id(ticker="COST", episode_id="ep-1", fingerprint_assignments=[bad_pair], template_version="v1")


@pytest.mark.parametrize("bad_pair", [(FP_A,), (FP_A, 1, 2), ()])
def test_wrong_pair_lengths_rejected(bad_pair):
    with pytest.raises(ValueError):
        fid.compute_task_instance_id(ticker="COST", episode_id="ep-1", fingerprint_assignments=[bad_pair], template_version="v1")


# ── malformed fingerprint digest ────────────────────────────────────────────

@pytest.mark.parametrize("bad_fp", ["not-hex", "a" * 63, "a" * 65, "g" * 64, "", 12345, None])
def test_malformed_fingerprint_digest_rejected(bad_fp):
    with pytest.raises(ValueError):
        fid.compute_task_instance_id(ticker="COST", episode_id="ep-1", fingerprint_assignments=[(bad_fp, 1)], template_version="v1")


def test_uppercase_digest_rejected():
    with pytest.raises(ValueError):
        fid.compute_task_instance_id(ticker="COST", episode_id="ep-1", fingerprint_assignments=[("A" * 64, 1)], template_version="v1")


def test_fingerprint_digest_not_nfc_normalized():
    # a digest is already constrained to [0-9a-f]; confirm no Unicode
    # normalization path is applied to it (a non-ASCII digest is simply
    # invalid, not normalized-then-checked).
    with pytest.raises(ValueError):
        fid.compute_task_instance_id(
            ticker="COST", episode_id="ep-1",
            fingerprint_assignments=[("a" * 63 + "é", 1)],
            template_version="v1",
        )


# ── ordinal validation ───────────────────────────────────────────────────────

def test_bool_ordinal_rejected():
    with pytest.raises(ValueError):
        fid.compute_task_instance_id(ticker="COST", episode_id="ep-1", fingerprint_assignments=[(FP_A, True)], template_version="v1")
    with pytest.raises(ValueError):
        fid.compute_task_instance_id(ticker="COST", episode_id="ep-1", fingerprint_assignments=[(FP_A, False)], template_version="v1")


@pytest.mark.parametrize("bad_ordinal", ["1", 1.0, None, [1]])
def test_non_int_ordinal_rejected(bad_ordinal):
    with pytest.raises(ValueError):
        fid.compute_task_instance_id(ticker="COST", episode_id="ep-1", fingerprint_assignments=[(FP_A, bad_ordinal)], template_version="v1")


@pytest.mark.parametrize("bad_ordinal", [0, -1, -100])
def test_ordinal_less_than_1_rejected(bad_ordinal):
    with pytest.raises(ValueError):
        fid.compute_task_instance_id(ticker="COST", episode_id="ep-1", fingerprint_assignments=[(FP_A, bad_ordinal)], template_version="v1")


def test_ordinal_exactly_1_accepted():
    result = fid.compute_task_instance_id(ticker="COST", episode_id="ep-1", fingerprint_assignments=[(FP_A, 1)], template_version="v1")
    assert _HEX64.match(result)


# ── duplicate / conflicting pairs ────────────────────────────────────────────

def test_duplicate_identical_pair_rejected():
    with pytest.raises(ValueError):
        fid.compute_task_instance_id(
            ticker="COST", episode_id="ep-1",
            fingerprint_assignments=[(FP_A, 1), (FP_A, 1)],
            template_version="v1",
        )


def test_conflicting_ordinal_for_same_fingerprint_rejected():
    with pytest.raises(ValueError):
        fid.compute_task_instance_id(
            ticker="COST", episode_id="ep-1",
            fingerprint_assignments=[(FP_A, 1), (FP_A, 2)],
            template_version="v1",
        )


def test_every_item_validated_before_duplicate_detection():
    # a malformed later item must raise its own validation error, not a
    # duplicate-detection error, even though an earlier item is a valid
    # duplicate of nothing -- this proves full per-item validation runs
    # before any duplicate/conflict pass.
    with pytest.raises(ValueError):
        fid.compute_task_instance_id(
            ticker="COST", episode_id="ep-1",
            fingerprint_assignments=[(FP_A, 1), ("bad-digest", 1)],
            template_version="v1",
        )


# ── lowercase 64-character digest output ────────────────────────────────────

def test_cadence_fingerprint_output_is_lowercase_64_char_hex():
    result = fid.compute_cadence_fingerprint(ticker="COST", next_due="2026-07-19", template_version="v1")
    assert len(result) == 64
    assert result == result.lower()
    assert _HEX64.match(result)


def test_task_instance_id_output_is_lowercase_64_char_hex():
    result = fid.compute_task_instance_id(ticker="COST", episode_id="ep-1", fingerprint_assignments=[(FP_A, 1)], template_version="v1")
    assert len(result) == 64
    assert result == result.lower()
    assert _HEX64.match(result)


# ── no compute_filing_fingerprint public function ───────────────────────────

def test_no_filing_fingerprint_function_exists():
    assert not hasattr(fid, "compute_filing_fingerprint")


def test_public_api_is_exactly_two_functions():
    public_names = sorted(n for n in dir(fid) if not n.startswith("_") and callable(getattr(fid, n)))
    # module-level imports (hashlib, json, re, unicodedata, date, datetime,
    # Sequence) are also public names in dir() -- filter to functions
    # actually defined in this module.
    own_functions = sorted(
        n for n in public_names
        if getattr(getattr(fid, n), "__module__", None) == fid.__name__
    )
    assert own_functions == ["compute_cadence_fingerprint", "compute_task_instance_id"]


# ── architectural invariants ─────────────────────────────────────────────────

def _module_source() -> str:
    return Path(fid.__file__).read_text()


def _module_ast():
    return ast.parse(_module_source())


def test_module_never_writes_to_disk():
    source = _module_source()
    assert "write_text" not in source
    assert "write_bytes" not in source
    tree = _module_ast()
    for node in ast.walk(tree):
        assert not (isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "open")


def test_module_has_no_top_level_side_effecting_statements():
    tree = _module_ast()
    allowed_top_level = (ast.Import, ast.ImportFrom, ast.FunctionDef, ast.AsyncFunctionDef,
                          ast.ClassDef, ast.Assign, ast.AnnAssign, ast.Expr)
    for node in tree.body:
        assert isinstance(node, allowed_top_level), f"unexpected top-level statement: {ast.dump(node)}"
        if isinstance(node, ast.Expr):
            assert isinstance(node.value, ast.Constant)


def test_module_imports_no_network_or_subprocess_or_vcs_libraries():
    tree = _module_ast()
    forbidden = {"requests", "urllib", "socket", "http.client", "subprocess"}
    imported = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imported.add(alias.name.split(".")[0])
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported.add(node.module.split(".")[0])
    assert not (imported & forbidden)


def test_module_does_not_import_allocate_margin_state_or_intelligence_report():
    tree = _module_ast()
    imported = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imported.add(alias.name)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported.add(node.module)
    assert "allocate" not in imported
    assert "margin_state" not in imported
    assert "intelligence_report" not in imported
    assert "intelligence_validator" not in imported


def test_module_has_no_implicit_clock_or_randomness():
    source = _module_source()
    for forbidden in ("time.time(", "datetime.now(", "datetime.utcnow(", "date.today(", "random.", "uuid."):
        assert forbidden not in source


def test_freshness_validator_imports_neither_intelligence_validator_nor_report():
    import freshness_validator as fval
    source = Path(fval.__file__).read_text()
    tree = ast.parse(source)
    imported = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imported.add(alias.name)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported.add(node.module)
    assert "intelligence_validator" not in imported
    assert "intelligence_report" not in imported


def test_allocate_and_margin_state_do_not_import_any_freshness_module():
    repo_root = Path(fid.__file__).resolve().parent
    freshness_module_names = {"freshness_validator", "freshness_state", "freshness_identity"}
    for filename in ("allocate.py", "margin_state.py"):
        path = repo_root / filename
        tree = ast.parse(path.read_text())
        imported = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imported.add(alias.name)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported.add(node.module)
        assert not (imported & freshness_module_names), f"{filename} imports a freshness module: {imported & freshness_module_names}"


def test_no_module_defines_a_tracked_file_mutation_helper():
    repo_root = Path(fid.__file__).resolve().parent
    for filename in ("freshness_validator.py", "freshness_state.py", "freshness_identity.py"):
        source = (repo_root / filename).read_text()
        for forbidden in ("write_text(", "write_bytes(", "yaml.dump(", "yaml.safe_dump("):
            assert forbidden not in source, f"{filename} contains {forbidden!r}"
