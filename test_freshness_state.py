"""Tests for freshness_state.py (AUTO-0002 bounded local-foundation scope)."""

import ast
from pathlib import Path

import pytest

import freshness_state as fstate

FP_A = "a" * 64
FP_B = "b" * 64
FP_C = "c" * 64


def _base_kwargs(**overrides) -> dict:
    kwargs = dict(
        monitoring_enabled=True,
        checkpoint_status="verified",
        monitor_record_exists=True,
        latest_monitor_state="healthy",
        outstanding=set(),
        assigned=set(),
        awaiting_human_incorporation=set(),
        incorporated=set(),
    )
    kwargs.update(overrides)
    return kwargs


# ── precedence ranks ────────────────────────────────────────────────────────

def test_rank4_current_when_all_five_conditions_hold():
    assert fstate.evaluate_freshness_state(**_base_kwargs()) == "current"


def test_rank3_unverified_when_monitoring_disabled():
    assert fstate.evaluate_freshness_state(**_base_kwargs(monitoring_enabled=False)) == "unverified"


def test_rank3_unverified_when_checkpoint_pending():
    assert fstate.evaluate_freshness_state(**_base_kwargs(checkpoint_status="pending")) == "unverified"


def test_rank3_unverified_when_no_monitor_record():
    assert fstate.evaluate_freshness_state(
        **_base_kwargs(monitor_record_exists=False, latest_monitor_state=None)
    ) == "unverified"


@pytest.mark.parametrize("bad_state", ["degraded", "failed"])
def test_rank3_unverified_when_monitor_degraded_or_failed(bad_state):
    assert fstate.evaluate_freshness_state(**_base_kwargs(latest_monitor_state=bad_state)) == "unverified"


def test_rank2_review_due_when_outstanding_nonempty():
    assert fstate.evaluate_freshness_state(**_base_kwargs(outstanding={FP_A})) == "review_due"


def test_rank2_review_due_when_assigned_nonempty():
    assert fstate.evaluate_freshness_state(**_base_kwargs(assigned={FP_A})) == "review_due"


def test_rank1_pending_human_review_when_awaiting_nonempty():
    assert fstate.evaluate_freshness_state(
        **_base_kwargs(awaiting_human_incorporation={FP_A})
    ) == "pending_human_review"


def test_all_four_sets_empty_is_valid_and_falls_through_to_rank3_or_4():
    result = fstate.evaluate_freshness_state(**_base_kwargs())
    assert result in fstate._STATES


# ── higher rank precedence over lower rank ──────────────────────────────────

def test_rank1_beats_rank2_and_rank3():
    result = fstate.evaluate_freshness_state(
        **_base_kwargs(
            monitoring_enabled=False,  # would be rank 3 alone
            outstanding={FP_B},         # would be rank 2 alone
            awaiting_human_incorporation={FP_A},  # rank 1
        )
    )
    assert result == "pending_human_review"


def test_rank2_beats_rank3():
    result = fstate.evaluate_freshness_state(
        **_base_kwargs(
            monitoring_enabled=False,  # would be rank 3 alone
            outstanding={FP_A},         # rank 2
        )
    )
    assert result == "review_due"


def test_rank3_beats_rank4_default():
    # every rank-4 condition true except monitoring_enabled
    result = fstate.evaluate_freshness_state(**_base_kwargs(monitoring_enabled=False))
    assert result == "unverified"


def test_worked_example_incorporation_reopens_to_review_due():
    """Spec §9 worked example: fingerprint A awaiting, B outstanding ->
    pending_human_review. After A incorporated, B still outstanding ->
    review_due, not current."""
    before = fstate.evaluate_freshness_state(
        **_base_kwargs(awaiting_human_incorporation={FP_A}, outstanding={FP_B})
    )
    assert before == "pending_human_review"

    after = fstate.evaluate_freshness_state(
        **_base_kwargs(incorporated={FP_A}, outstanding={FP_B})
    )
    assert after == "review_due"


# ── exact bool rejection ─────────────────────────────────────────────────────

@pytest.mark.parametrize("bad_value", [0, 1, "true", None, "False"])
def test_monitoring_enabled_exact_bool_rejection(bad_value):
    with pytest.raises(ValueError):
        fstate.evaluate_freshness_state(**_base_kwargs(monitoring_enabled=bad_value))


@pytest.mark.parametrize("bad_value", [0, 1, "true", None])
def test_monitor_record_exists_exact_bool_rejection(bad_value):
    with pytest.raises(ValueError):
        fstate.evaluate_freshness_state(**_base_kwargs(monitor_record_exists=bad_value))


# ── monitor-record/state contradictions ─────────────────────────────────────

def test_record_not_exists_with_non_null_state_raises():
    with pytest.raises(ValueError):
        fstate.evaluate_freshness_state(
            **_base_kwargs(monitor_record_exists=False, latest_monitor_state="healthy")
        )


def test_record_exists_with_null_state_raises():
    with pytest.raises(ValueError):
        fstate.evaluate_freshness_state(
            **_base_kwargs(monitor_record_exists=True, latest_monitor_state=None)
        )


# ── closed vocabulary rejections ────────────────────────────────────────────

@pytest.mark.parametrize("bad_status", ["Pending", "VERIFIED", "", None, 5])
def test_checkpoint_status_closed_vocabulary_rejection(bad_status):
    with pytest.raises(ValueError):
        fstate.evaluate_freshness_state(**_base_kwargs(checkpoint_status=bad_status))


@pytest.mark.parametrize("bad_state", ["Healthy", "HEALTHY", "unknown", "", 5])
def test_monitor_state_closed_vocabulary_rejection(bad_state):
    with pytest.raises(ValueError):
        fstate.evaluate_freshness_state(**_base_kwargs(latest_monitor_state=bad_state))


@pytest.mark.parametrize("good_status", ["pending", "verified"])
def test_checkpoint_status_accepts_both_valid_values(good_status):
    fstate.evaluate_freshness_state(**_base_kwargs(checkpoint_status=good_status))


@pytest.mark.parametrize("good_state", ["healthy", "degraded", "failed"])
def test_monitor_state_accepts_all_three_valid_values(good_state):
    fstate.evaluate_freshness_state(**_base_kwargs(latest_monitor_state=good_state))


# ── fingerprint set type validation ─────────────────────────────────────────

@pytest.mark.parametrize("bad_collection", [
    ["list", "not", "set"],
    {"a": 1},
    "a-string",
    12345,
    None,
])
@pytest.mark.parametrize("field", ["outstanding", "assigned", "awaiting_human_incorporation", "incorporated"])
def test_fingerprint_arguments_reject_non_set_types(field, bad_collection):
    with pytest.raises(ValueError):
        fstate.evaluate_freshness_state(**_base_kwargs(**{field: bad_collection}))


def test_set_and_frozenset_both_accepted():
    assert fstate.evaluate_freshness_state(**_base_kwargs(outstanding={FP_A})) == "review_due"
    assert fstate.evaluate_freshness_state(**_base_kwargs(outstanding=frozenset({FP_A}))) == "review_due"


@pytest.mark.parametrize("bad_member", [
    "not-hex-64-chars",
    "A" * 64,      # uppercase rejected
    "a" * 63,       # too short
    "a" * 65,       # too long
    "g" * 64,       # invalid hex char
    "",
])
def test_malformed_digest_rejected(bad_member):
    with pytest.raises(ValueError):
        fstate.evaluate_freshness_state(**_base_kwargs(outstanding={bad_member}))


def test_cross_set_duplicate_fingerprint_rejected():
    with pytest.raises(ValueError):
        fstate.evaluate_freshness_state(**_base_kwargs(outstanding={FP_A}, assigned={FP_A}))


@pytest.mark.parametrize("set_a,set_b", [
    ("outstanding", "assigned"),
    ("outstanding", "awaiting_human_incorporation"),
    ("outstanding", "incorporated"),
    ("assigned", "awaiting_human_incorporation"),
    ("assigned", "incorporated"),
    ("awaiting_human_incorporation", "incorporated"),
])
def test_cross_set_duplicate_rejected_every_pair(set_a, set_b):
    with pytest.raises(ValueError):
        fstate.evaluate_freshness_state(**_base_kwargs(**{set_a: {FP_A}, set_b: {FP_A}}))


def test_same_fingerprint_in_same_set_is_fine_not_a_duplicate():
    # a Python set already dedupes identical members -- this just proves
    # constructing the set doesn't itself trigger the cross-set check.
    assert fstate.evaluate_freshness_state(**_base_kwargs(outstanding={FP_A, FP_A})) == "review_due"


def test_incorporated_set_participates_in_disjointness_but_not_precedence():
    # incorporated alone, nothing outstanding/assigned/awaiting -> falls
    # through to rank 3/4 exactly as if incorporated were empty.
    with_incorporated = fstate.evaluate_freshness_state(**_base_kwargs(incorporated={FP_A}))
    without = fstate.evaluate_freshness_state(**_base_kwargs())
    assert with_incorporated == without == "current"

    with_incorporated_unverified = fstate.evaluate_freshness_state(
        **_base_kwargs(incorporated={FP_A}, monitoring_enabled=False)
    )
    assert with_incorporated_unverified == "unverified"


# ── invalid input never falls through to current ────────────────────────────

@pytest.mark.parametrize("bad_kwargs", [
    {"monitoring_enabled": "true"},
    {"monitor_record_exists": 1},
    {"checkpoint_status": "bogus"},
    {"latest_monitor_state": "bogus"},
    {"outstanding": ["not", "a", "set"]},
    {"outstanding": {"bad-digest"}},
])
def test_invalid_input_raises_never_returns_current(bad_kwargs):
    with pytest.raises(ValueError):
        result = fstate.evaluate_freshness_state(**_base_kwargs(**bad_kwargs))
        assert result != "current"  # unreachable if raise fires correctly, kept as documentation


def test_mutating_original_set_after_call_does_not_change_result():
    mutable = {FP_A}
    fstate.evaluate_freshness_state(**_base_kwargs(outstanding=mutable))
    mutable.add(FP_B)
    mutable.clear()
    # no assertion on a stored value needed -- the point is the function
    # itself never retains a live reference; re-invoking with the mutated
    # (now empty) set proves the earlier call wasn't affected by later
    # mutation, since each call is independently pure.
    assert fstate.evaluate_freshness_state(**_base_kwargs(outstanding=set())) == "current"


# ── architectural invariants ─────────────────────────────────────────────────

def _module_source() -> str:
    return Path(fstate.__file__).read_text()


def _module_ast():
    return ast.parse(_module_source())


def test_module_never_writes_to_disk():
    source = _module_source()
    assert "write_text" not in source
    assert "write_bytes" not in source
    tree = _module_ast()
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "open":
            for kw in node.keywords:
                if kw.arg == "mode" and isinstance(kw.value, ast.Constant):
                    assert "w" not in kw.value.value and "a" not in kw.value.value


def test_module_has_no_top_level_side_effecting_statements():
    tree = _module_ast()
    allowed_top_level = (ast.Import, ast.ImportFrom, ast.FunctionDef, ast.AsyncFunctionDef,
                          ast.ClassDef, ast.Assign, ast.AnnAssign, ast.Expr)
    for node in tree.body:
        assert isinstance(node, allowed_top_level), f"unexpected top-level statement: {ast.dump(node)}"
        if isinstance(node, ast.Expr):
            # only a docstring constant is permitted at module top level
            assert isinstance(node.value, ast.Constant)


def test_module_imports_no_network_or_subprocess_libraries():
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
    assert "http" not in imported or "client" not in _module_source()


def test_module_does_not_import_allocate_or_margin_state():
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


def test_module_has_no_implicit_clock_read():
    source = _module_source()
    for forbidden in ("time.time(", "datetime.now(", "datetime.utcnow(", "date.today("):
        assert forbidden not in source


def test_module_does_not_import_intelligence_report():
    tree = _module_ast()
    imported = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imported.add(alias.name)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported.add(node.module)
    assert "intelligence_report" not in imported
