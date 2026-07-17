"""Tests for intelligence_validator.py (PI-0002 bounded Phase 1 scope).

All fixtures are synthetic. No real portfolio ticker, real company thesis,
or real investment judgment appears anywhere in this file — per the
authorized scope, only a fictional placeholder ticker ("ZZZZ") is used.
"""

import ast
import os
import textwrap

import pytest

import intelligence_validator as iv


def _valid_company() -> dict:
    """A structurally complete, fully synthetic company record."""
    return {
        "sector": "Fictional Sector",
        "industry": "Fictional Industry",
        "portfolio_role_ref": "T1",
        "competitive_advantages": ["made-up moat"],
        "risks": [
            {"risk": "made-up risk", "severity": "low", "identified": "2026-01-01", "status": "open"},
        ],
        "catalysts": [
            {"catalyst": "made-up catalyst", "expected": "2026-06-01", "status": "pending"},
        ],
        "conviction": {"rating": "Medium", "rationale": "synthetic test rationale"},
        "review": {
            "cadence_days": 90,
            "last_reviewed": "2026-01-01",
            "next_due": "2026-04-01",
            "log": [{"date": "2026-01-01", "note": "synthetic review note"}],
        },
        "sources": [{"note": "synthetic source", "date": "2026-01-01"}],
    }


# ── validate_company_data ─────────────────────────────────────────────────────

def test_valid_synthetic_company_passes():
    result = iv.validate_company_data(_valid_company())
    assert result.valid is True
    assert result.errors == []


def test_non_mapping_root_is_rejected():
    result = iv.validate_company_data(["not", "a", "mapping"])
    assert result.valid is False
    assert any("mapping" in e for e in result.errors)


def test_conviction_rating_without_rationale_is_rejected():
    data = _valid_company()
    data["conviction"] = {"rating": "High"}
    result = iv.validate_company_data(data)
    assert result.valid is False
    assert any("rationale" in e for e in result.errors)


def test_conviction_rationale_without_rating_is_allowed():
    """Spec §9/§12 requires rationale alongside any RATING, but does not
    require a rating to already exist for a rationale to be recorded —
    validated as structurally fine, per the frozen spec, not invented
    doctrine."""
    data = _valid_company()
    data["conviction"] = {"rationale": "thinking about it, no rating yet"}
    result = iv.validate_company_data(data)
    assert result.valid is True


@pytest.mark.parametrize("good_rating", ["Low", "Medium", "High", "Very High"])
def test_conviction_rating_accepts_each_frozen_pi0004_value(good_rating):
    data = _valid_company()
    data["conviction"] = {"rating": good_rating, "rationale": "synthetic test rationale"}
    result = iv.validate_company_data(data)
    assert result.valid is True
    assert result.errors == []


@pytest.mark.parametrize("bad_rating", [
    "Medium-High",   # hyphenated hybrid, explicitly rejected by PI-0004
    "medium",        # lowercase — vocabulary is case-sensitive
    9,                # numeric scale, explicitly rejected by PI-0004
])
def test_conviction_rating_rejects_out_of_vocabulary_values(bad_rating):
    data = _valid_company()
    data["conviction"] = {"rating": bad_rating, "rationale": "synthetic test rationale"}
    result = iv.validate_company_data(data)
    assert result.valid is False
    assert any("PI-0004" in e for e in result.errors)


@pytest.mark.parametrize("bad_value", [
    1.5,                 # numeric
    {"tier": "T1"},       # mapping
    ["T1", "T2"],         # sequence
    "3.35%",              # percentage/weight string
    "0.0335",              # bare numeric string (weight-shaped)
])
def test_invalid_portfolio_role_ref_is_rejected(bad_value):
    data = _valid_company()
    data["portfolio_role_ref"] = bad_value
    result = iv.validate_company_data(data)
    assert result.valid is False
    assert any("portfolio_role_ref" in e for e in result.errors)


def test_valid_portfolio_role_ref_bare_label_passes():
    data = _valid_company()
    data["portfolio_role_ref"] = "band"
    result = iv.validate_company_data(data)
    assert result.valid is True


def test_risks_missing_required_key_is_rejected():
    data = _valid_company()
    data["risks"] = [{"risk": "made-up risk"}]  # missing severity/identified/status
    result = iv.validate_company_data(data)
    assert result.valid is False
    assert any("risks[0]" in e for e in result.errors)


def test_catalysts_missing_required_key_is_rejected():
    data = _valid_company()
    data["catalysts"] = [{"catalyst": "made-up catalyst"}]
    result = iv.validate_company_data(data)
    assert result.valid is False
    assert any("catalysts[0]" in e for e in result.errors)


def test_review_missing_required_key_is_rejected():
    data = _valid_company()
    data["review"] = {"cadence_days": 90}  # missing last_reviewed/next_due
    result = iv.validate_company_data(data)
    assert result.valid is False
    assert any("review" in e for e in result.errors)


def test_review_log_entry_missing_required_key_is_rejected():
    data = _valid_company()
    data["review"]["log"] = [{"date": "2026-01-01"}]  # missing note
    result = iv.validate_company_data(data)
    assert result.valid is False
    assert any("review.log[0]" in e for e in result.errors)


def test_sources_missing_required_key_is_rejected():
    data = _valid_company()
    data["sources"] = [{"url": "https://example.invalid"}]  # missing note
    result = iv.validate_company_data(data)
    assert result.valid is False
    assert any("sources[0]" in e for e in result.errors)


# ── validate_company_file ─────────────────────────────────────────────────────

def test_valid_company_file_passes(tmp_path):
    p = tmp_path / "ZZZZ.yaml"
    p.write_text(textwrap.dedent("""
        sector: Fictional Sector
        industry: Fictional Industry
        portfolio_role_ref: T2
        conviction:
          rating: Low
          rationale: synthetic test only
    """))
    result = iv.validate_company_file(p)
    assert result.valid is True
    assert result.source == str(p)


def test_malformed_yaml_is_rejected_cleanly(tmp_path):
    p = tmp_path / "ZZZZ.yaml"
    p.write_text("sector: [unclosed list\n")
    result = iv.validate_company_file(p)
    assert result.valid is False
    assert any("invalid YAML" in e for e in result.errors)


def test_empty_file_is_rejected_cleanly(tmp_path):
    p = tmp_path / "ZZZZ.yaml"
    p.write_text("")
    result = iv.validate_company_file(p)
    assert result.valid is False


# ── validate_directory ────────────────────────────────────────────────────────

def test_missing_directory_succeeds_with_zero_companies(tmp_path):
    missing = tmp_path / "does_not_exist"
    result = iv.validate_directory(missing)
    assert result.valid is True
    assert result.company_count == 0


def test_empty_directory_succeeds_with_zero_companies(tmp_path):
    empty_dir = tmp_path / "companies"
    empty_dir.mkdir()
    result = iv.validate_directory(empty_dir)
    assert result.valid is True
    assert result.company_count == 0


def test_directory_scans_multiple_files_one_invalid_does_not_block_others(tmp_path):
    d = tmp_path / "companies"
    d.mkdir()
    (d / "AAAA.yaml").write_text(textwrap.dedent("""
        sector: Fictional Sector
        portfolio_role_ref: T1
    """))
    (d / "BBBB.yaml").write_text("not: [valid yaml\n")
    (d / "CCCC.yaml").write_text(textwrap.dedent("""
        sector: Another Fictional Sector
        portfolio_role_ref: 12.5
    """))

    result = iv.validate_directory(d)

    assert result.company_count == 3
    assert result.valid is False  # at least one file invalid
    by_source = {r.source: r for r in result.results}
    assert by_source[str(d / "AAAA.yaml")].valid is True
    assert by_source[str(d / "BBBB.yaml")].valid is False
    assert by_source[str(d / "CCCC.yaml")].valid is False


# ── read-only guarantees ───────────────────────────────────────────────────────

def test_validate_directory_does_not_mutate_source_files(tmp_path):
    d = tmp_path / "companies"
    d.mkdir()
    p = d / "ZZZZ.yaml"
    original = "sector: Fictional Sector\nportfolio_role_ref: T1\n"
    p.write_text(original)
    before_mtime = p.stat().st_mtime_ns

    iv.validate_directory(d)

    assert p.read_text() == original
    assert p.stat().st_mtime_ns == before_mtime


def test_validate_directory_creates_no_new_files_or_directories(tmp_path):
    d = tmp_path / "companies"
    d.mkdir()
    (d / "ZZZZ.yaml").write_text("sector: Fictional Sector\n")

    before = set(os.listdir(tmp_path))
    iv.validate_directory(d)
    after = set(os.listdir(tmp_path))

    assert before == after


def test_module_source_contains_no_write_mode_file_opens():
    """Static guarantee, not just behavioral: the module's source contains
    no open()/Path.open() call requesting write/append/update mode, and no
    os.mkdir/os.makedirs/Path.mkdir call."""
    with open(iv.__file__) as f:
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


# ── import isolation ───────────────────────────────────────────────────────────

def test_intelligence_validator_does_not_import_allocate_or_margin_state():
    with open(iv.__file__) as f:
        tree = ast.parse(f.read())
    imported_names = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported_names.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported_names.add(node.module)
    assert "allocate" not in imported_names
    assert "margin_state" not in imported_names


def test_allocate_does_not_import_intelligence_validator():
    with open("allocate.py") as f:
        tree = ast.parse(f.read())
    imported_names = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported_names.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported_names.add(node.module)
    assert "intelligence_validator" not in imported_names


def test_margin_state_does_not_import_intelligence_validator():
    with open("margin_state.py") as f:
        tree = ast.parse(f.read())
    imported_names = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported_names.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported_names.add(node.module)
    assert "intelligence_validator" not in imported_names


# ── running the validator against the real directory never mutates it ──────────

def test_validating_the_real_intelligence_directory_does_not_mutate_it():
    """Updated for PI-0003: intelligence/companies/ may now legitimately
    exist and hold committed pilot records. If it does, running the
    real validator against it must not change a single byte -- same
    regression guard as test_validate_directory_does_not_mutate_source_files
    above, applied to the actual repository directory rather than a
    tmp_path fixture, so a future change to the validator can never be
    the thing that mutates a committed company record."""
    real_dir = "intelligence/companies"
    if not os.path.isdir(real_dir):
        return
    before = {}
    for name in os.listdir(real_dir):
        full = os.path.join(real_dir, name)
        with open(full, "rb") as f:
            before[name] = f.read()

    iv.validate_directory(real_dir)

    after = {}
    for name in os.listdir(real_dir):
        full = os.path.join(real_dir, name)
        with open(full, "rb") as f:
            after[name] = f.read()
    assert before == after


# ── the real intelligence/companies/ directory, if present, stays clean ────────

def test_real_intelligence_companies_directory_contains_only_expected_files():
    """Updated for PI-0003: intelligence/companies/ is now expected to
    exist and hold committed pilot company records -- this test
    previously asserted the directory couldn't exist at all, a
    Phase 1 / PI-0002-era invariant made stale by PI-0003's
    authorization of exactly one real company record. Absence is still
    valid (SS16/SS20 opt-in coverage) -- this only guards against
    unintended stray files landing in the directory: every entry must
    be a <TICKER>.yaml with a matching <TICKER>.md, per spec SS7's
    'at most two files per company' rule, nothing else."""
    real_dir = "intelligence/companies"
    if not os.path.isdir(real_dir):
        return
    entries = os.listdir(real_dir)
    for name in entries:
        full = os.path.join(real_dir, name)
        assert os.path.isfile(full), f"unexpected non-file entry in {real_dir}: {full}"
        assert name.endswith(".yaml") or name.endswith(".md"), \
            f"unexpected file type in {real_dir}: {full}"
    yaml_stems = {n[:-5] for n in entries if n.endswith(".yaml")}
    md_stems = {n[:-3] for n in entries if n.endswith(".md")}
    assert yaml_stems == md_stems, (
        "every company in intelligence/companies/ must have exactly a "
        f"matching YAML+Markdown pair (spec SS7) -- yaml-only: "
        f"{yaml_stems - md_stems}, md-only: {md_stems - yaml_stems}"
    )
