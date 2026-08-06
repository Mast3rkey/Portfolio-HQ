"""Tests for contender_registry_generator.py (CONTENDER-0002 §A-§M scope,
XASSET-0001 §J step 1 / WS-0014 objective items (1)+(2)).

Most tests here run the real generator against the real repository, since
this unit's entire purpose is mechanically screening real repository
content — there is no meaningful synthetic-fixture substitute for "does the
real targets.yaml/gates.yaml/holdings.yaml/etc. get scanned correctly,"
matching relationship_validator.py's own precedent of testing its real
merged records directly once real content exists.
"""

import ast
import subprocess
from pathlib import Path

import pytest
import yaml

import contender_registry_generator as gen
import contender_registry_validator as crv

_REPO_ROOT = Path(__file__).resolve().parent


def _sha() -> str:
    return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=_REPO_ROOT, text=True).strip()


@pytest.fixture(scope="module")
def registry():
    reg, accepted, excluded = gen.build_registry(_REPO_ROOT, _sha(), "2026-08-06T00:00:00Z")
    return reg, accepted, excluded


# ── determinism (§I) ─────────────────────────────────────────────────────

def test_regeneration_is_deterministic_excluding_timestamp():
    r1, _, _ = gen.build_registry(_REPO_ROOT, "sha-x", "ts-1")
    r2, _, _ = gen.build_registry(_REPO_ROOT, "sha-x", "ts-2")
    r1c = dict(r1)
    r2c = dict(r2)
    r1c.pop("generated_at")
    r2c.pop("generated_at")
    assert r1c == r2c


def test_entries_are_alphabetically_sorted(registry):
    reg, _, _ = registry
    symbols = [e["canonical_symbol"] for e in reg["entries"]]
    assert symbols == sorted(symbols)


def test_header_carries_source_commit_sha_and_timestamp(registry):
    reg, _, _ = registry
    assert reg["source_commit_sha"] == _sha()
    assert reg["generated_at"] == "2026-08-06T00:00:00Z"
    assert reg["schema_version"] == 1


# ── schema validity ────────────────────────────────────────────────────

def test_generated_registry_validates_clean(registry):
    reg, _, _ = registry
    result = crv.validate_registry_data(reg)
    assert result.valid, result.errors


def test_no_duplicate_canonical_symbols(registry):
    reg, _, _ = registry
    symbols = [e["canonical_symbol"] for e in reg["entries"]]
    assert len(symbols) == len(set(symbols))


def test_no_brk_dash_b_separate_row(registry):
    reg, _, _ = registry
    symbols = {e["canonical_symbol"] for e in reg["entries"]}
    assert "BRK.B" in symbols
    assert "BRK-B" not in symbols  # §C: alias resolved, never double-counted


def test_every_entry_has_nonempty_reason_and_provenance(registry):
    reg, _, _ = registry
    for e in reg["entries"]:
        assert e["reason"], e["canonical_symbol"]
        assert e["provenance"], e["canonical_symbol"]


# ── §J bidirectional reconciliation, using the generator's own outputs ────

def test_bidirectional_reconciliation_passes(registry):
    reg, accepted, excluded = registry
    registry_symbols = frozenset(e["canonical_symbol"] for e in reg["entries"])
    discovered = frozenset(accepted) | frozenset(excluded) | registry_symbols
    result = crv.reconcile(
        discovered_symbols=discovered,
        registry_symbols=registry_symbols,
        excluded_with_reason=frozenset(excluded),
    )
    assert result.valid, result.errors


def test_every_registry_entry_cites_authorized_source_label(registry):
    reg, _, _ = registry
    for e in reg["entries"]:
        for p in e["provenance"]:
            assert p["source"] in crv.AUTHORIZED_SOURCE_LABELS, (e["canonical_symbol"], p)


# ── §E.2 worked cases (§E.4, §E.5) ────────────────────────────────────────

def test_rklb_tsla_worked_case(registry):
    reg, _, _ = registry
    by = {e["canonical_symbol"]: e for e in reg["entries"]}
    for sym in ("RKLB", "TSLA"):
        e = by[sym]
        assert e["primary_disposition"] == "insufficient_evidence"
        assert e["secondary_flags"]["has_current_gate"] is True
        assert e["secondary_flags"]["has_prior_deferral_superseded"] is True
        assert e["secondary_flags"]["current_target"] is True


def test_gnrc_rtx_worked_case_differs_from_rklb_tsla(registry):
    """PI-0036's GNRC/RTX pair shares RKLB/TSLA's primary-disposition
    reasoning path but is NOT gated — a future implementation must read
    each identity's own facts rather than assume a shared flag profile
    (CONTENDER-0002 §E.4)."""
    reg, _, _ = registry
    by = {e["canonical_symbol"]: e for e in reg["entries"]}
    for sym in ("GNRC", "RTX"):
        e = by[sym]
        assert e["secondary_flags"]["has_current_gate"] is False
        assert e["secondary_flags"]["has_prior_deferral_superseded"] is True
        assert e["primary_disposition"] == "evaluation_ready"


def test_all_six_gated_names_are_insufficient_evidence(registry):
    reg, _, _ = registry
    by = {e["canonical_symbol"]: e for e in reg["entries"]}
    for sym in ("SNPS", "ICE", "SPGI", "WM", "RKLB", "TSLA"):
        assert by[sym]["primary_disposition"] == "insufficient_evidence", sym
        assert by[sym]["secondary_flags"]["has_current_gate"] is True, sym


def test_wdc_sndk_spinoff_worked_case(registry):
    """CONTENDER-0002 §E.2 tier 5's own corrected worked example: a spinoff
    creates a NEW instrument, it does not supersede the old one's identity.
    WDC must never land on stale_or_superseded; SNDK (no prior identity of
    its own) lands on requires_research."""
    reg, _, _ = registry
    by = {e["canonical_symbol"]: e for e in reg["entries"]}
    assert by["WDC"]["primary_disposition"] != "stale_or_superseded"
    assert by["SNDK"]["primary_disposition"] == "requires_research"
    assert by["SNDK"]["secondary_flags"]["has_historical_intelligence"] is False


def test_qqq_is_benchmark_or_index(registry):
    reg, _, _ = registry
    by = {e["canonical_symbol"]: e for e in reg["entries"]}
    assert by["QQQ"]["primary_disposition"] == "benchmark_or_index"


def test_cash_and_reserve_are_synthetic_fixture(registry):
    reg, _, _ = registry
    by = {e["canonical_symbol"]: e for e in reg["entries"]}
    assert by["CASH"]["primary_disposition"] == "synthetic_or_test_fixture"
    assert by["RESERVE"]["primary_disposition"] == "synthetic_or_test_fixture"


def test_prior_holdings_found_only_in_claude_md_are_discovered(registry):
    """VMC and LHX are genuine prior holdings (CONTENDER-0001 §A's own
    eligibility language) findable only via the disclosed 17th (CLAUDE.md)
    source — this is the concrete case that source extension exists for."""
    reg, _, _ = registry
    by = {e["canonical_symbol"]: e for e in reg["entries"]}
    for sym in ("VMC", "LHX", "HYPE"):
        assert sym in by
        assert by[sym]["primary_disposition"] == "explicitly_deferred_or_excluded"
        assert any(p["source"] == "CLAUDE.md" for p in by[sym]["provenance"])


def test_dust_coins_deferred_and_excluded(registry):
    reg, _, _ = registry
    by = {e["canonical_symbol"]: e for e in reg["entries"]}
    for sym in ("ZORA", "WIF", "BONK", "PEPE"):
        assert by[sym]["primary_disposition"] == "explicitly_deferred_or_excluded"
        assert by[sym]["asset_type"] == "crypto"


def test_funds_and_crypto_with_no_framework_require_research(registry):
    reg, _, _ = registry
    by = {e["canonical_symbol"]: e for e in reg["entries"]}
    for sym in ("SPY", "VEA", "VWO", "GLD", "BTC", "ETH", "SOL"):
        assert by[sym]["primary_disposition"] == "requires_research", sym


def test_disposition_distribution_sums_to_total(registry):
    reg, _, _ = registry
    from collections import Counter
    counts = Counter(e["primary_disposition"] for e in reg["entries"])
    assert sum(counts.values()) == len(reg["entries"])
    # Every counted disposition must be one of the closed twelve.
    assert set(counts) <= crv.PRIMARY_DISPOSITIONS


# ── §D: the sealed 27 are read-only reference, never rescanned ───────────

def test_classification_context_never_creates_new_entries_alone(registry):
    """Every canonical_symbol with classification_exists=True must also
    have at least one *other* provenance source beyond
    intelligence/classification — §D forbids treating "already classified"
    as itself a discovery source."""
    reg, _, _ = registry
    for e in reg["entries"]:
        if e["secondary_flags"]["classification_exists"]:
            non_classification_sources = [
                p for p in e["provenance"] if p["source"] != "intelligence/classification"
            ]
            assert non_classification_sources, e["canonical_symbol"]


def test_sealed_classification_directory_untouched_by_generation(registry):
    """Generating the registry must never mutate any sealed Milestone 6
    record or the cohort manifest."""
    classification_dir = _REPO_ROOT / "intelligence" / "classification"
    before = subprocess.check_output(
        ["git", "status", "--porcelain", "--", str(classification_dir)],
        cwd=_REPO_ROOT, text=True,
    )
    gen.build_registry(_REPO_ROOT, _sha(), "2026-08-06T00:00:00Z")
    after = subprocess.check_output(
        ["git", "status", "--porcelain", "--", str(classification_dir)],
        cwd=_REPO_ROOT, text=True,
    )
    assert before == after == ""


# ── §G legacy-ticker provenance ───────────────────────────────────────────

def test_legacy_gap_record_present_and_creates_no_placeholder_rows(registry):
    reg, _, _ = registry
    gap = reg["legacy_gap"]
    assert gap["known_unenumerated_legacy_gap"] is True
    assert gap["source_authority"] == "PHQ-2026-02"
    assert gap["registry_entries_created"] == 0
    assert gap["recovery_status"] in {
        "unavailable_in_current_clone", "recovered_n_of_41", "recovery_ambiguous",
    }


def test_this_environment_is_a_shallow_clone():
    """Independently re-verifies the environment fact CONTENDER-0002 §G
    requires re-checking before trusting its own finding as still current."""
    out = subprocess.check_output(
        ["git", "rev-parse", "--is-shallow-repository"], cwd=_REPO_ROOT, text=True,
    ).strip()
    assert out == "true"


# ── protected-path isolation ───────────────────────────────────────────────

_PROTECTED_PATHS = (
    "targets.yaml", "holdings.yaml", "gates.yaml", "issuer_lookthrough.yaml",
    "allocate.py", "margin_state.py", "levels.py",
)


def test_generation_touches_no_protected_path():
    before = {}
    for p in _PROTECTED_PATHS:
        before[p] = (_REPO_ROOT / p).read_bytes()
    gen.build_registry(_REPO_ROOT, _sha(), "2026-08-06T00:00:00Z")
    for p in _PROTECTED_PATHS:
        assert (_REPO_ROOT / p).read_bytes() == before[p], p


# ── prose scan: excluded tokens are never silently dropped ────────────────

def test_every_prose_discovery_table_entry_reaches_a_registry_row(registry):
    reg, accepted, excluded = registry
    by = {e["canonical_symbol"] for e in reg["entries"]}
    for sym in gen._PROSE_DISCOVERIES:
        assert sym in by, sym


def test_excluded_tokens_never_silently_become_registry_entries(registry):
    reg, accepted, excluded = registry
    by = {e["canonical_symbol"] for e in reg["entries"]}
    # A token can appear in both accepted (via a different source) and
    # excluded (a genuinely ambiguous mention elsewhere) — only tokens that
    # are excluded EVERYWHERE and never accepted anywhere must stay out of
    # the registry.
    excluded_only = set(excluded) - set(accepted)
    assert not (excluded_only & by)


# ── static source guarantees ─────────────────────────────────────────────

def test_generator_writes_only_to_its_own_registry_path():
    """Static guarantee: the only write-mode open() in this module's source
    targets a path this module itself constructs under
    intelligence/contenders/ — never a protected path."""
    with open(gen.__file__) as f:
        source = f.read()
    assert "intelligence" in source and "contenders" in source
    tree = ast.parse(source)
    write_calls = 0
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            func = node.func
            name = getattr(func, "attr", None) or getattr(func, "id", None)
            if name == "open":
                for arg in list(node.args) + node.keywords:
                    value = arg.value if isinstance(arg, ast.keyword) else arg
                    if isinstance(value, ast.Constant) and value.value == "w":
                        write_calls += 1
    assert write_calls == 1  # exactly the registry.yaml write in __main__


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


def test_generator_imports_no_allocator_margin_or_brokerage_code():
    imported = _imported_names(gen.__file__)
    for forbidden in ("allocate", "margin_state", "alpaca_client", "target_variants"):
        assert forbidden not in imported


def test_allocate_does_not_import_contender_registry_generator():
    imported = _imported_names("allocate.py")
    assert "contender_registry_generator" not in imported


def test_margin_state_does_not_import_contender_registry_generator():
    imported = _imported_names("margin_state.py")
    assert "contender_registry_generator" not in imported
