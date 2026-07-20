"""Tests for freshness_cadence.py (AUTO-0003 bounded Cadence Trigger Core
scope).

All synthetic fixtures use fictional placeholder tickers ("ZZZZ", "AAAA",
...) — no real portfolio ticker or real investment judgment appears in any
fixture. Section E's equivalence tests exercise the real, unmodified
`intelligence_report.collect_staleness_findings` against synthetic
company records only, never real `intelligence/companies/*.yaml` content.
"""

from __future__ import annotations

import ast
from datetime import date, datetime
from pathlib import Path

import pytest
import yaml

import freshness_cadence as fc
import freshness_identity as fid
import intelligence_report as ir

_HEX64_CHARS = frozenset("0123456789abcdef")


def _is_hex64(value: str) -> bool:
    return len(value) == 64 and value == value.lower() and set(value) <= _HEX64_CHARS


def _valid_company(**overrides) -> dict:
    """Same structurally complete, fully synthetic shape convention as
    test_intelligence_report.py's own _valid_company()."""
    base = {
        "sector": "Fictional Sector",
        "industry": "Fictional Industry",
        "portfolio_role_ref": "T1",
        "review": {
            "cadence_days": 90,
            "last_reviewed": "2026-01-01",
            "next_due": "2026-04-01",
        },
    }
    base.update(overrides)
    return base


def _write_yaml(path: Path, data: dict) -> None:
    path.write_text(yaml.safe_dump(data, sort_keys=False))


# ── A. core outcomes ─────────────────────────────────────────────────────

def test_overdue_date_object_returns_digest():
    result = fc.compute_due_cadence_fingerprint(
        ticker="ZZZZ", monitoring_enabled=True, checkpoint_status="verified",
        next_due=date(2026, 7, 18), as_of_date=date(2026, 7, 19), template_version="v1",
    )
    assert result is not None
    assert _is_hex64(result)


def test_overdue_strict_date_string_returns_digest():
    result = fc.compute_due_cadence_fingerprint(
        ticker="ZZZZ", monitoring_enabled=True, checkpoint_status="verified",
        next_due="2026-07-18", as_of_date="2026-07-19", template_version="v1",
    )
    assert result is not None
    assert _is_hex64(result)


def test_equal_date_returns_none():
    result = fc.compute_due_cadence_fingerprint(
        ticker="ZZZZ", monitoring_enabled=True, checkpoint_status="verified",
        next_due="2026-07-19", as_of_date="2026-07-19", template_version="v1",
    )
    assert result is None


def test_future_date_returns_none():
    result = fc.compute_due_cadence_fingerprint(
        ticker="ZZZZ", monitoring_enabled=True, checkpoint_status="verified",
        next_due="2026-07-20", as_of_date="2026-07-19", template_version="v1",
    )
    assert result is None


def test_disabled_and_verified_returns_none():
    result = fc.compute_due_cadence_fingerprint(
        ticker="ZZZZ", monitoring_enabled=False, checkpoint_status="verified",
        next_due="2026-07-18", as_of_date="2026-07-19", template_version="v1",
    )
    assert result is None


def test_disabled_and_pending_returns_none():
    result = fc.compute_due_cadence_fingerprint(
        ticker="ZZZZ", monitoring_enabled=False, checkpoint_status="pending",
        next_due="2026-07-18", as_of_date="2026-07-19", template_version="v1",
    )
    assert result is None


def test_enabled_and_pending_raises_valueerror():
    with pytest.raises(ValueError):
        fc.compute_due_cadence_fingerprint(
            ticker="ZZZZ", monitoring_enabled=True, checkpoint_status="pending",
            next_due="2026-07-18", as_of_date="2026-07-19", template_version="v1",
        )


# ── B1. ticker / template_version validation ────────────────────────────

_VALID_KWARGS = dict(
    ticker="ZZZZ", monitoring_enabled=True, checkpoint_status="verified",
    next_due="2026-07-18", as_of_date="2026-07-19", template_version="v1",
)


def _call_with(**overrides):
    kwargs = dict(_VALID_KWARGS)
    kwargs.update(overrides)
    return fc.compute_due_cadence_fingerprint(**kwargs)


@pytest.mark.parametrize("field", ["ticker", "template_version"])
@pytest.mark.parametrize("bad_value", [123, None, [], {}, 1.5, True])
def test_open_string_field_wrong_type_rejected(field, bad_value):
    with pytest.raises(ValueError):
        _call_with(**{field: bad_value})


@pytest.mark.parametrize("field", ["ticker", "template_version"])
def test_open_string_field_empty_rejected(field):
    with pytest.raises(ValueError):
        _call_with(**{field: ""})


@pytest.mark.parametrize("field", ["ticker", "template_version"])
def test_open_string_field_nfc_normalization_equivalence(field):
    nfc = "AAAAé"
    nfd = "AAAA" + "é"
    a = _call_with(**{field: nfc})
    b = _call_with(**{field: nfd})
    assert a == b
    assert a is not None


@pytest.mark.parametrize("field", ["ticker", "template_version"])
def test_open_string_field_not_implicitly_stripped(field):
    padded = _call_with(**{field: "  AAAA  "})
    unpadded = _call_with(**{field: "AAAA"})
    # No implicit strip/case transform: differing whitespace must not
    # collapse to the same normalized value once fed into the fingerprint.
    assert padded != unpadded
    assert padded is not None
    assert unpadded is not None


@pytest.mark.parametrize("field", ["ticker", "template_version"])
def test_open_string_field_whitespace_only_not_treated_as_empty(field):
    result = _call_with(**{field: "   "})
    assert result is not None


@pytest.mark.parametrize("field", ["ticker", "template_version"])
@pytest.mark.parametrize("code", [0x00, 0x09, 0x1F])
def test_open_string_field_c0_lower_boundary_rejected(field, code):
    with pytest.raises(ValueError):
        _call_with(**{field: f"AAAA{chr(code)}"})


@pytest.mark.parametrize("field", ["ticker", "template_version"])
@pytest.mark.parametrize("code", [0x7F, 0x80, 0x9F])
def test_open_string_field_c0_c1_rejected_ranges(field, code):
    with pytest.raises(ValueError):
        _call_with(**{field: f"AAAA{chr(code)}"})


@pytest.mark.parametrize("field", ["ticker", "template_version"])
@pytest.mark.parametrize("code", [0x20, 0x7E, 0xA0])
def test_open_string_field_chars_just_outside_rejected_ranges_accepted(field, code):
    result = _call_with(**{field: f"AAAA{chr(code)}"})
    assert result is not None


# ── B2. monitoring_enabled validation ────────────────────────────────────

def test_monitoring_enabled_true_and_false_accepted():
    assert _call_with(monitoring_enabled=True) is not None
    assert _call_with(monitoring_enabled=False) is None


@pytest.mark.parametrize("bad_value", [0, 1, "true", "false", None, [], {}, 1.0])
def test_monitoring_enabled_non_bool_rejected(bad_value):
    with pytest.raises(ValueError):
        _call_with(monitoring_enabled=bad_value)


# ── B3. checkpoint_status validation ─────────────────────────────────────

def test_checkpoint_status_pending_and_verified_accepted():
    assert _call_with(checkpoint_status="verified") is not None
    assert _call_with(monitoring_enabled=False, checkpoint_status="pending") is None


@pytest.mark.parametrize("bad_value", ["Pending", "VERIFIED", "Verified", "PENDING"])
def test_checkpoint_status_wrong_case_rejected(bad_value):
    with pytest.raises(ValueError):
        _call_with(checkpoint_status=bad_value)


@pytest.mark.parametrize("bad_value", [" pending", "verified ", " verified", "pending "])
def test_checkpoint_status_whitespace_rejected(bad_value):
    with pytest.raises(ValueError):
        _call_with(checkpoint_status=bad_value)


@pytest.mark.parametrize("bad_value", ["unknown", "", "healthy", "current"])
def test_checkpoint_status_unknown_string_rejected(bad_value):
    with pytest.raises(ValueError):
        _call_with(checkpoint_status=bad_value)


@pytest.mark.parametrize("bad_value", [1, None, [], {}, ["pending"], {"status": "pending"}])
def test_checkpoint_status_non_string_rejected_as_valueerror_not_typeerror(bad_value):
    with pytest.raises(ValueError):
        _call_with(checkpoint_status=bad_value)


# ── B4. next_due / as_of_date validation ─────────────────────────────────

@pytest.mark.parametrize("field", ["next_due", "as_of_date"])
def test_date_field_date_object_accepted(field):
    assert _call_with(**{field: date(2026, 7, 18) if field == "next_due" else date(2026, 7, 19)}) is not None


@pytest.mark.parametrize("field", ["next_due", "as_of_date"])
def test_date_field_strict_string_accepted(field):
    assert _call_with(**{field: "2026-07-18" if field == "next_due" else "2026-07-19"}) is not None


@pytest.mark.parametrize("field", ["next_due", "as_of_date"])
def test_date_field_datetime_rejected(field):
    with pytest.raises(ValueError):
        _call_with(**{field: datetime(2026, 7, 18, 1, 2, 3)})


@pytest.mark.parametrize("field", ["next_due", "as_of_date"])
@pytest.mark.parametrize("bad_date", ["2026-13-01", "2026-02-30", "2026-00-10", "2026-01-00"])
def test_date_field_malformed_calendar_date_rejected(field, bad_date):
    with pytest.raises(ValueError):
        _call_with(**{field: bad_date})


@pytest.mark.parametrize("field", ["next_due", "as_of_date"])
def test_date_field_compact_date_rejected(field):
    with pytest.raises(ValueError):
        _call_with(**{field: "20260719"})


@pytest.mark.parametrize("field", ["next_due", "as_of_date"])
@pytest.mark.parametrize("bad_date", ["2026-7-19", "2026-07-9", "26-07-19"])
def test_date_field_non_zero_padded_date_rejected(field, bad_date):
    with pytest.raises(ValueError):
        _call_with(**{field: bad_date})


@pytest.mark.parametrize("field", ["next_due", "as_of_date"])
@pytest.mark.parametrize("bad_date", ["2026-07-19T00:00:00", "2026-07-19 00:00:00"])
def test_date_field_timestamp_rejected(field, bad_date):
    with pytest.raises(ValueError):
        _call_with(**{field: bad_date})


@pytest.mark.parametrize("field", ["next_due", "as_of_date"])
@pytest.mark.parametrize("bad_date", [" 2026-07-19", "2026-07-19 ", " 2026-07-19 "])
def test_date_field_whitespace_padded_rejected(field, bad_date):
    with pytest.raises(ValueError):
        _call_with(**{field: bad_date})


@pytest.mark.parametrize("field", ["next_due", "as_of_date"])
def test_date_field_unicode_digit_variant_rejected(field):
    # Full-width (fullwidth ASCII variant) digits -- Python's bare `\d`
    # regex class would match these as Unicode decimal digits unless
    # re.ASCII is set; this parser must reject them regardless.
    fullwidth = "２０２６-０７-１９"  # "2026-07-19" in fullwidth digits
    with pytest.raises(ValueError):
        _call_with(**{field: fullwidth})


@pytest.mark.parametrize("field", ["next_due", "as_of_date"])
@pytest.mark.parametrize("bad_value", [12345, None, [], {}, 20260719, 1.5])
def test_date_field_wrong_type_rejected(field, bad_value):
    with pytest.raises(ValueError):
        _call_with(**{field: bad_value})


# ── C. validation-before-gating ───────────────────────────────────────────

@pytest.mark.parametrize("otherwise_none_kwargs", [
    dict(monitoring_enabled=False, checkpoint_status="verified"),
    dict(monitoring_enabled=False, checkpoint_status="pending"),
    dict(next_due="2026-07-19", as_of_date="2026-07-19"),  # equal date
    dict(next_due="2026-07-20", as_of_date="2026-07-19"),  # future date
], ids=["disabled", "disabled-pending", "equal-date", "future-date"])
@pytest.mark.parametrize("invalid_field, invalid_value", [
    ("ticker", 123),
    ("template_version", None),
    ("monitoring_enabled", "not-a-bool"),
    ("checkpoint_status", "unknown"),
    ("next_due", "not-a-date"),
    ("as_of_date", "not-a-date"),
])
def test_invalid_input_never_masked_by_otherwise_none_outcome(
    otherwise_none_kwargs, invalid_field, invalid_value
):
    kwargs = dict(_VALID_KWARGS)
    kwargs.update(otherwise_none_kwargs)
    kwargs[invalid_field] = invalid_value
    with pytest.raises(ValueError):
        fc.compute_due_cadence_fingerprint(**kwargs)


def test_true_plus_pending_invariant_raises_valueerror():
    # monitoring_enabled=True together with checkpoint_status="pending" is
    # an invalid combination and must raise ValueError.
    with pytest.raises(ValueError):
        fc.compute_due_cadence_fingerprint(
            ticker="ZZZZ", monitoring_enabled=True, checkpoint_status="pending",
            next_due="2026-07-18", as_of_date="2026-07-19", template_version="v1",
        )


# ── D. delegation and identity ───────────────────────────────────────────

def test_deterministic_repeated_calls():
    a = _call_with()
    b = _call_with()
    assert a == b


def test_overdue_result_equals_direct_call_to_freshness_identity():
    result = fc.compute_due_cadence_fingerprint(
        ticker="ZZZZ", monitoring_enabled=True, checkpoint_status="verified",
        next_due=date(2026, 7, 18), as_of_date=date(2026, 7, 19), template_version="v1",
    )
    direct = fid.compute_cadence_fingerprint(ticker="ZZZZ", next_due=date(2026, 7, 18), template_version="v1")
    assert result == direct


def test_nfc_equivalent_ticker_produces_same_digest_as_direct_call():
    nfc_ticker = "ZZZZé"
    nfd_ticker = "ZZZZ" + "é"
    a = _call_with(ticker=nfc_ticker)
    b = _call_with(ticker=nfd_ticker)
    assert a == b
    direct = fid.compute_cadence_fingerprint(ticker=nfc_ticker, next_due=date(2026, 7, 18), template_version="v1")
    assert a == direct


def test_output_is_exactly_64_lowercase_hex_chars():
    result = _call_with()
    assert result is not None
    assert _is_hex64(result)


def test_delegate_called_only_for_overdue_enabled_verified(monkeypatch):
    calls = []
    original = fc._compute_cadence_fingerprint

    def _spy(**kwargs):
        calls.append(kwargs)
        return original(**kwargs)

    monkeypatch.setattr(fc, "_compute_cadence_fingerprint", _spy)

    # Not overdue: delegate must not be called.
    fc.compute_due_cadence_fingerprint(
        ticker="ZZZZ", monitoring_enabled=True, checkpoint_status="verified",
        next_due="2026-07-19", as_of_date="2026-07-19", template_version="v1",
    )
    assert len(calls) == 0

    # Disabled: delegate must not be called.
    fc.compute_due_cadence_fingerprint(
        ticker="ZZZZ", monitoring_enabled=False, checkpoint_status="verified",
        next_due="2026-07-18", as_of_date="2026-07-19", template_version="v1",
    )
    assert len(calls) == 0

    # Overdue, enabled, verified: delegate must be called exactly once.
    fc.compute_due_cadence_fingerprint(
        ticker="ZZZZ", monitoring_enabled=True, checkpoint_status="verified",
        next_due="2026-07-18", as_of_date="2026-07-19", template_version="v1",
    )
    assert len(calls) == 1


# ── E. PI-0011 strict overdue-boundary equivalence ───────────────────────
#
# Governed scope only: for a schema-valid synthetic company record with a
# valid, parseable next_due and an explicit valid as_of_date, both paths
# must classify the STRICT DATE ORDERING identically. This is never a
# claim of whole-function equivalence with collect_staleness_findings,
# which also handles directory scanning, schema validation, malformed or
# missing review data, UnableToEvaluate reporting, and catalysts -- none
# of that is asserted equivalent here.

@pytest.mark.parametrize("next_due, as_of_date, expected_overdue", [
    ("2026-07-18", "2026-07-19", True),   # one day before -> overdue
    ("2026-07-19", "2026-07-19", False),  # equal -> not overdue
    ("2026-07-20", "2026-07-19", False),  # one day after -> not overdue
])
def test_strict_overdue_boundary_equivalence_with_string_dates(tmp_path, next_due, as_of_date, expected_overdue):
    d = tmp_path / "companies"
    d.mkdir()
    _write_yaml(d / "ZZZZ.yaml", _valid_company(review={
        "cadence_days": 90, "last_reviewed": "2026-01-01", "next_due": next_due,
    }))

    report_findings = ir.collect_staleness_findings(d, as_of_date=date.fromisoformat(as_of_date))
    report_says_overdue = any(o.ticker == "ZZZZ" for o in report_findings.overdue_reviews)

    cadence_result = fc.compute_due_cadence_fingerprint(
        ticker="ZZZZ", monitoring_enabled=True, checkpoint_status="verified",
        next_due=next_due, as_of_date=as_of_date, template_version="v1",
    )
    cadence_says_overdue = cadence_result is not None

    assert report_says_overdue == expected_overdue
    assert cadence_says_overdue == expected_overdue
    assert report_says_overdue == cadence_says_overdue


@pytest.mark.parametrize("next_due, as_of_date, expected_overdue", [
    (date(2026, 7, 18), date(2026, 7, 19), True),
    (date(2026, 7, 19), date(2026, 7, 19), False),
    (date(2026, 7, 20), date(2026, 7, 19), False),
])
def test_strict_overdue_boundary_equivalence_with_date_objects(tmp_path, next_due, as_of_date, expected_overdue):
    d = tmp_path / "companies"
    d.mkdir()
    # PyYAML decodes an unquoted YYYY-MM-DD scalar into a date object --
    # write the review block via yaml.safe_dump with an actual date value.
    _write_yaml(d / "ZZZZ.yaml", _valid_company(review={
        "cadence_days": 90, "last_reviewed": date(2026, 1, 1), "next_due": next_due,
    }))

    report_findings = ir.collect_staleness_findings(d, as_of_date=as_of_date)
    report_says_overdue = any(o.ticker == "ZZZZ" for o in report_findings.overdue_reviews)

    cadence_result = fc.compute_due_cadence_fingerprint(
        ticker="ZZZZ", monitoring_enabled=True, checkpoint_status="verified",
        next_due=next_due, as_of_date=as_of_date, template_version="v1",
    )
    cadence_says_overdue = cadence_result is not None

    assert report_says_overdue == expected_overdue
    assert cadence_says_overdue == expected_overdue
    assert report_says_overdue == cadence_says_overdue


# ── F. architectural invariants ───────────────────────────────────────────

def _module_source() -> str:
    return Path(fc.__file__).read_text()


def _module_ast():
    return ast.parse(_module_source())


def test_exactly_one_public_function_defined():
    # The module explicitly declares its export contract via __all__ --
    # dir()/`__module__` alone cannot distinguish an intentional export
    # from an incidentally public-looking imported name (e.g. `date`,
    # `datetime`, `unicodedata` are all module-level names visible via
    # dir(fc), but none of them is authorized as part of this module's
    # public surface merely because their own __module__ differs from
    # freshness_cadence).
    assert hasattr(fc, "__all__")
    assert fc.__all__ == ("compute_due_cadence_fingerprint",)
    assert callable(fc.compute_due_cadence_fingerprint)

    for name in fc.__all__:
        assert not name.startswith("_")
    assert "date" not in fc.__all__
    assert "datetime" not in fc.__all__
    assert "unicodedata" not in fc.__all__
    assert "_compute_cadence_fingerprint" not in fc.__all__
    assert "_normalize_open_string" not in fc.__all__
    assert "_parse_strict_date" not in fc.__all__

    # The only module-level function without a leading underscore remains
    # compute_due_cadence_fingerprint.
    tree = _module_ast()
    top_level_funcs = [n.name for n in tree.body if isinstance(n, ast.FunctionDef)]
    public_funcs = [n for n in top_level_funcs if not n.startswith("_")]
    assert public_funcs == ["compute_due_cadence_fingerprint"]


def test_every_other_module_level_function_is_private():
    tree = _module_ast()
    top_level_funcs = [n.name for n in tree.body if isinstance(n, ast.FunctionDef)]
    non_public = [n for n in top_level_funcs if n != "compute_due_cadence_fingerprint"]
    assert non_public, "expected at least one private helper"
    assert all(n.startswith("_") for n in non_public)


def test_only_project_internal_import_is_freshness_identity_cadence_fingerprint():
    tree = _module_ast()
    project_internal_from_imports = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module == "freshness_identity":
            for alias in node.names:
                project_internal_from_imports.append((alias.name, alias.asname))
        elif isinstance(node, ast.Import):
            for alias in node.names:
                # only stdlib-ish top-level imports are expected as plain `import X`
                assert alias.name in {"unicodedata"}, f"unexpected plain import: {alias.name}"
    assert project_internal_from_imports == [("compute_cadence_fingerprint", "_compute_cadence_fingerprint")]


def test_imported_helper_is_private_within_module_namespace():
    assert hasattr(fc, "_compute_cadence_fingerprint")
    assert not hasattr(fc, "compute_cadence_fingerprint")


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


def test_module_imports_no_yaml_pathlib_network_github_claude_subprocess_allocator_margin():
    tree = _module_ast()
    forbidden = {
        "yaml", "pathlib", "requests", "urllib", "socket", "http.client",
        "subprocess", "github", "anthropic", "claude", "allocate", "margin_state",
    }
    imported = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imported.add(alias.name.split(".")[0])
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported.add(node.module.split(".")[0])
    assert not (imported & forbidden), imported & forbidden


def test_module_never_writes_to_disk_or_opens_files():
    source = _module_source()
    assert "write_text" not in source
    assert "write_bytes" not in source
    tree = _module_ast()
    for node in ast.walk(tree):
        assert not (isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "open")


def test_module_has_no_implicit_clock_or_randomness():
    source = _module_source()
    for forbidden in ("time.time(", "datetime.now(", "datetime.utcnow(", "date.today(", "random.", "uuid."):
        assert forbidden not in source


def test_module_has_no_main_block_or_operational_entry_point():
    source = _module_source()
    assert "__main__" not in source
    tree = _module_ast()
    for node in ast.walk(tree):
        if isinstance(node, ast.If):
            test = node.test
            if (
                isinstance(test, ast.Compare)
                and isinstance(test.left, ast.Name)
                and test.left.id == "__name__"
            ):
                pytest.fail("module contains an `if __name__ == ...` entry point")


def test_module_has_no_top_level_side_effecting_statements():
    tree = _module_ast()
    allowed_top_level = (
        ast.Import, ast.ImportFrom, ast.FunctionDef, ast.AsyncFunctionDef,
        ast.ClassDef, ast.Assign, ast.AnnAssign, ast.Expr,
    )
    for node in tree.body:
        assert isinstance(node, allowed_top_level), f"unexpected top-level statement: {ast.dump(node)}"
        if isinstance(node, ast.Expr):
            assert isinstance(node.value, ast.Constant)


def _imports_of(path: Path) -> set[str]:
    tree = ast.parse(path.read_text())
    imported = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imported.add(alias.name)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported.add(node.module)
    return imported


def test_allocate_and_margin_state_do_not_import_freshness_cadence():
    repo_root = Path(fc.__file__).resolve().parent
    for filename in ("allocate.py", "margin_state.py"):
        imported = _imports_of(repo_root / filename)
        assert "freshness_cadence" not in imported, f"{filename} imports freshness_cadence"


def test_existing_freshness_and_report_modules_do_not_import_freshness_cadence():
    repo_root = Path(fc.__file__).resolve().parent
    for filename in (
        "freshness_identity.py", "freshness_state.py", "freshness_validator.py",
        "intelligence_report.py",
    ):
        imported = _imports_of(repo_root / filename)
        assert "freshness_cadence" not in imported, f"{filename} imports freshness_cadence"
