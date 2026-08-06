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

def test_legacy_gap_record_present_and_shape_is_valid(registry):
    """Runs against the REAL environment via the `registry` fixture — which
    may be a shallow local clone (registry_entries_created == 0,
    recovery_status a fixed value) OR a genuinely complete clone, such as
    this repository's own CI (`fetch-depth: 0`), where §G step 2's
    mandatory recovery attempt can — and, against this repository's real
    history, does — succeed and add real recovered entries. Both are
    valid, correctly-behaving outcomes; this test asserts the *shape* is
    internally consistent in either case, never a hardcoded assumption
    about which one the environment happens to produce (CONTENDER-0002
    §G step 1: never assume, always re-verify live)."""
    reg, _, _ = registry
    gap = reg["legacy_gap"]
    assert gap["known_unenumerated_legacy_gap"] is True
    assert gap["source_authority"] == "PHQ-2026-02"
    assert gap["clone_depth_at_generation"] in crv.CLONE_DEPTH_VALUES

    recovered_match = crv.RECOVERED_STATUS_PATTERN.match(gap["recovery_status"])
    if recovered_match:
        # Real recovery succeeded (only reachable with a complete clone) —
        # registry_entries_created must equal the count named in
        # recovery_status, be > 0, and every one of that many entries must
        # actually be present with real §G-step-2 git provenance — never a
        # placeholder, and never an invented count.
        n = int(recovered_match.group(1))
        assert gap["registry_entries_created"] == n
        assert n > 0
        assert gap["clone_depth_at_generation"] == "complete"
        recovered_entries = [
            e for e in reg["entries"]
            if "§G step 2" in (e.get("existing_disposition") or "")
        ]
        assert len(recovered_entries) == n
        for e in recovered_entries:
            assert "PHQ-2026-02 reconciliation commit" in e["existing_disposition"]
    else:
        # No recovery — either shallow (unavailable) or complete-but-
        # ambiguous. Either way, zero entries may be invented.
        assert gap["recovery_status"] in crv.RECOVERY_STATUS_VALUES
        assert gap["registry_entries_created"] == 0


# ── §G clone-depth detection: environment-independent (CONTENDER-0002 §G
# step 1 is a live, per-generation re-verification — the test suite must
# not assume, or require, any particular clone depth in the environment it
# happens to run in; both states are exercised via dependency injection). ──

def _fake_git_output(text: str):
    def runner(args, **kwargs):
        return text
    return runner


def test_detect_clone_depth_normalizes_true_to_shallow():
    assert gen.detect_clone_depth(_REPO_ROOT, runner=_fake_git_output("true\n")) == "shallow"


def test_detect_clone_depth_normalizes_false_to_complete():
    assert gen.detect_clone_depth(_REPO_ROOT, runner=_fake_git_output("false\n")) == "complete"


def test_detect_clone_depth_rejects_unexpected_output():
    with pytest.raises(ValueError):
        gen.detect_clone_depth(_REPO_ROOT, runner=_fake_git_output("garbage\n"))


def test_detect_clone_depth_return_value_is_always_normalized():
    for raw in ("true\n", "false\n"):
        assert gen.detect_clone_depth(_REPO_ROOT, runner=_fake_git_output(raw)) in gen.CLONE_DEPTH_VALUES


def test_legacy_gap_record_shallow_branch():
    gap = gen._legacy_gap_record("shallow", "unavailable_in_current_clone", 0)
    assert gap["clone_depth_at_generation"] == "shallow"
    assert gap["recovery_status"] == "unavailable_in_current_clone"
    assert gap["registry_entries_created"] == 0
    assert gap["next_action"] == "separately_authorized_history_recovery_sub_unit"


def test_legacy_gap_record_rejects_unnormalized_clone_depth():
    with pytest.raises(ValueError):
        gen._legacy_gap_record("shallowish", "unavailable_in_current_clone", 0)


# ── §G step 2: perform_legacy_recovery() — shallow branch (unreachable) ────

def test_perform_legacy_recovery_shallow_never_attempts_recovery():
    """§G step 1/3's existing shallow-clone path: no recovery attempted,
    honest 'unavailable' disclosure, matching the pre-existing behavior
    this correction must not regress."""

    def runner_should_not_be_called(args, **kwargs):
        raise AssertionError(f"no git call should happen for a shallow clone: {args}")

    recovered, gap = gen.perform_legacy_recovery(_REPO_ROOT, "shallow", runner=runner_should_not_be_called)
    assert recovered == []
    assert gap["clone_depth_at_generation"] == "shallow"
    assert gap["recovery_status"] == "unavailable_in_current_clone"
    assert gap["registry_entries_created"] == 0


# ── §G step 2: complete/reachable branch, successful bounded recovery ──────

def _synthetic_recovery_runner(before_holdings: str, after_holdings: str, *, commit_subject="PHQ-2026-02: holdings reconciled"):
    def runner(args, **kwargs):
        if args[:2] == ["git", "log"]:
            return f"COMMITSHA\x1fPARENTSHA\x1f{commit_subject}\n"
        if args[:2] == ["git", "show"]:
            target = args[2]
            if target.startswith("PARENTSHA"):
                return before_holdings
            if target.startswith("COMMITSHA"):
                return after_holdings
        raise AssertionError(f"unexpected call: {args}")
    return runner


def test_perform_legacy_recovery_complete_successful_diff():
    runner = _synthetic_recovery_runner(
        before_holdings="shares:\n  AMZN: 1.0\n  LEGACYCO: 2.5\ncrypto_shares:\n  BTC: 0.1\n  DEADCOIN: 5.0\n",
        after_holdings="shares:\n  AMZN: 1.0\ncrypto_shares:\n  BTC: 0.1\n",
    )
    recovered, gap = gen.perform_legacy_recovery(_REPO_ROOT, "complete", runner=runner)
    recovered_symbols = {sym for sym, _asset_type, _note in recovered}
    assert recovered_symbols == {"LEGACYCO", "DEADCOIN"}
    assert gap["clone_depth_at_generation"] == "complete"
    assert gap["recovery_status"] == "recovered_2_of_41"
    assert gap["registry_entries_created"] == 2
    for sym, asset_type, note in recovered:
        assert "PARENTSHA" in note and "COMMITSHA" in note  # real git provenance, never guessed
    asset_types = {sym: asset_type for sym, asset_type, _note in recovered}
    assert asset_types["LEGACYCO"] == "equity"
    assert asset_types["DEADCOIN"] == "crypto"


def test_perform_legacy_recovery_finds_earliest_matching_commit():
    """History is walked oldest-first so the ORIGINAL reconciliation
    commit is found, not a later commit that merely mentions PHQ-2026-02
    in passing."""
    def runner(args, **kwargs):
        if args[:2] == ["git", "log"]:
            return (
                "OLDSHA\x1fOLDPARENT\x1fPHQ-2026-02: holdings reconciled\n"
                "NEWSHA\x1fNEWPARENT\x1fLane M: reference PHQ-2026-02 for context\n"
            )
        if args[:2] == ["git", "show"]:
            target = args[2]
            if target.startswith("OLDPARENT"):
                return "shares:\n  X: 1.0\ncrypto_shares: {}\n"
            if target.startswith("OLDSHA"):
                return "shares: {}\ncrypto_shares: {}\n"
        raise AssertionError(f"unexpected call: {args}")

    commit_sha, parent_sha = gen.find_phq_2026_02_reconciliation_commit(_REPO_ROOT, runner=runner)
    assert commit_sha == "OLDSHA"
    assert parent_sha == "OLDPARENT"


# ── §G step 2/3: complete history where the boundary cannot be resolved ────

def test_perform_legacy_recovery_no_matching_commit_fails_closed():
    def runner(args, **kwargs):
        if args[:2] == ["git", "log"]:
            return "SHA1\x1fPARENT1\x1funrelated commit, no PHQ mention\n"
        raise AssertionError(f"unexpected call: {args}")

    recovered, gap = gen.perform_legacy_recovery(_REPO_ROOT, "complete", runner=runner)
    assert recovered == []
    assert gap["recovery_status"] == "recovery_ambiguous"
    assert gap["registry_entries_created"] == 0


def test_perform_legacy_recovery_merge_commit_fails_closed():
    """A merge commit (more than one parent) has no single unambiguous
    'before' state — must fail closed, never guess which parent."""
    def runner(args, **kwargs):
        if args[:2] == ["git", "log"]:
            return "SHA1\x1fPARENT1 PARENT2\x1fPHQ-2026-02: merge reconciliation\n"
        raise AssertionError(f"unexpected call: {args}")

    recovered, gap = gen.perform_legacy_recovery(_REPO_ROOT, "complete", runner=runner)
    assert recovered == []
    assert gap["recovery_status"] == "recovery_ambiguous"
    assert gap["registry_entries_created"] == 0


def test_perform_legacy_recovery_empty_diff_fails_closed():
    """A matching commit is found but the diff finds nothing removed —
    treated as ambiguous (a real boundary that didn't remove any ticker is
    not the ~41-ticker reconciliation §G describes), never silently
    reported as a successful zero-ticker recovery."""
    runner = _synthetic_recovery_runner(
        before_holdings="shares:\n  AMZN: 1.0\ncrypto_shares: {}\n",
        after_holdings="shares:\n  AMZN: 1.0\ncrypto_shares: {}\n",
    )
    recovered, gap = gen.perform_legacy_recovery(_REPO_ROOT, "complete", runner=runner)
    assert recovered == []
    assert gap["recovery_status"] == "recovery_ambiguous"
    assert gap["registry_entries_created"] == 0


# ── malformed git output ────────────────────────────────────────────────

def test_perform_legacy_recovery_malformed_show_output_fails_closed():
    def runner(args, **kwargs):
        if args[:2] == ["git", "log"]:
            return "SHA1\x1fPARENT1\x1fPHQ-2026-02: reconciled\n"
        if args[:2] == ["git", "show"]:
            return "{ not: valid: yaml: ][\n"
        raise AssertionError(args)

    recovered, gap = gen.perform_legacy_recovery(_REPO_ROOT, "complete", runner=runner)
    assert recovered == []
    assert gap["recovery_status"] == "recovery_ambiguous"


def test_perform_legacy_recovery_git_show_raising_fails_closed():
    def runner(args, **kwargs):
        if args[:2] == ["git", "log"]:
            return "SHA1\x1fPARENT1\x1fPHQ-2026-02: reconciled\n"
        if args[:2] == ["git", "show"]:
            raise RuntimeError("simulated missing blob")
        raise AssertionError(args)

    recovered, gap = gen.perform_legacy_recovery(_REPO_ROOT, "complete", runner=runner)
    assert recovered == []
    assert gap["recovery_status"] == "recovery_ambiguous"
    assert gap["registry_entries_created"] == 0


def test_detect_clone_depth_malformed_output_never_silently_defaults():
    with pytest.raises(ValueError):
        gen.detect_clone_depth(_REPO_ROOT, runner=_fake_git_output("maybe?\n"))


# ── zero invented placeholders, in every branch ─────────────────────────

def test_perform_legacy_recovery_never_invents_placeholder_rows():
    scenarios = [
        ("shallow", lambda a, **k: (_ for _ in ()).throw(AssertionError("no git call for shallow"))),
        ("complete", lambda a, **k: "SHA1\x1fPARENT1\x1fno phq mention\n" if a[:2] == ["git", "log"] else ""),
    ]
    for depth, runner in scenarios:
        recovered, gap = gen.perform_legacy_recovery(_REPO_ROOT, depth, runner=runner)
        assert recovered == []
        assert gap["registry_entries_created"] == 0


# ── build_registry() end-to-end: recovered identities become real entries ──

def test_build_registry_merges_recovered_identities_into_entries():
    runner = _synthetic_recovery_runner(
        before_holdings="shares:\n  AMZN: 1.0\n  LEGACYCO: 2.5\ncrypto_shares: {}\n",
        after_holdings="shares:\n  AMZN: 1.0\ncrypto_shares: {}\n",
    )

    def combined_runner(args, **kwargs):
        if args[:2] == ["git", "rev-parse"]:
            return "false\n"
        return runner(args, **kwargs)

    reg, accepted, _excluded = gen.build_registry(_REPO_ROOT, "sha-z", "ts-z", runner=combined_runner)
    by = {e["canonical_symbol"]: e for e in reg["entries"]}
    assert "LEGACYCO" in by
    assert by["LEGACYCO"]["primary_disposition"] == "requires_research"
    assert "§G step 2" in by["LEGACYCO"]["existing_disposition"]
    assert "LEGACYCO" in accepted  # bidirectional reconciliation must account for it
    assert reg["legacy_gap"]["recovery_status"] == "recovered_1_of_41"
    assert reg["legacy_gap"]["registry_entries_created"] == 1
    assert len(reg["entries"]) == 85  # 84 baseline + 1 genuinely new recovered identity


def test_build_registry_never_duplicates_an_already_tracked_recovered_symbol():
    """A symbol the mechanical diff finds removed, but that is ALSO
    currently tracked via a live source (e.g. re-added later, or already
    carries a Company Intelligence record), must never be duplicated or
    have its existing, already-provenanced entry overwritten by a bare
    historical recovery stub (§H.3 step 4)."""
    runner = _synthetic_recovery_runner(
        before_holdings="shares:\n  AMZN: 1.0\ncrypto_shares: {}\n",
        after_holdings="shares: {}\ncrypto_shares: {}\n",
    )

    def combined_runner(args, **kwargs):
        if args[:2] == ["git", "rev-parse"]:
            return "false\n"
        return runner(args, **kwargs)

    reg, _accepted, _excluded = gen.build_registry(_REPO_ROOT, "sha-z2", "ts-z2", runner=combined_runner)
    by = {e["canonical_symbol"]: e for e in reg["entries"]}
    amzn_symbols = [e for e in reg["entries"] if e["canonical_symbol"] == "AMZN"]
    assert len(amzn_symbols) == 1  # never duplicated
    assert "§G step 2" not in (by["AMZN"].get("existing_disposition") or "")  # not overwritten
    assert len(reg["entries"]) == 84  # no net-new entry — AMZN was already tracked


# ── deterministic output for the same repository state ─────────────────

def test_perform_legacy_recovery_is_deterministic_for_same_synthetic_state():
    runner = _synthetic_recovery_runner(
        before_holdings="shares:\n  AMZN: 1.0\n  LEGACYCO: 2.5\ncrypto_shares: {}\n",
        after_holdings="shares:\n  AMZN: 1.0\ncrypto_shares: {}\n",
    )
    recovered1, gap1 = gen.perform_legacy_recovery(_REPO_ROOT, "complete", runner=runner)
    recovered2, gap2 = gen.perform_legacy_recovery(_REPO_ROOT, "complete", runner=runner)
    assert recovered1 == recovered2
    assert gap1 == gap2


def test_build_registry_uses_live_detected_clone_depth_not_hardcoded(monkeypatch):
    """End-to-end: build_registry()'s own legacy_gap must reflect whatever
    detect_clone_depth() reports for the given repo_root at call time — this
    is what the pre-correction code got wrong (a hardcoded string, never
    actually calling a live detector)."""
    calls = []

    def fake_detect(repo_root, **kwargs):
        calls.append(repo_root)
        return "shallow"

    monkeypatch.setattr(gen, "detect_clone_depth", fake_detect)
    reg, _, _ = gen.build_registry(_REPO_ROOT, "sha-y", "ts-y")
    assert calls, "build_registry() must call detect_clone_depth()"
    assert reg["legacy_gap"]["clone_depth_at_generation"] == "shallow"
    assert reg["legacy_gap"]["recovery_status"] == "unavailable_in_current_clone"


def test_bidirectional_reconciliation_passes_with_recovered_identities_included():
    """§J's own bidirectional check must still pass when §G step 2
    recovery adds genuinely new entries — the recovered symbol must be
    represented in the `accepted` discovery bookkeeping, not just silently
    added to `entries` (which would make it a 'registry-only invented
    identity' from §J's own point of view)."""
    runner = _synthetic_recovery_runner(
        before_holdings="shares:\n  AMZN: 1.0\n  LEGACYCO: 2.5\ncrypto_shares: {}\n",
        after_holdings="shares:\n  AMZN: 1.0\ncrypto_shares: {}\n",
    )

    def combined_runner(args, **kwargs):
        if args[:2] == ["git", "rev-parse"]:
            return "false\n"
        return runner(args, **kwargs)

    reg, accepted, excluded = gen.build_registry(_REPO_ROOT, "sha-recon", "ts-recon", runner=combined_runner)
    registry_symbols = frozenset(e["canonical_symbol"] for e in reg["entries"])
    discovered = frozenset(accepted) | frozenset(excluded) | registry_symbols
    result = crv.reconcile(
        discovered_symbols=discovered,
        registry_symbols=registry_symbols,
        excluded_with_reason=frozenset(excluded),
    )
    assert result.valid, result.errors
    assert "LEGACYCO" in registry_symbols


def test_build_registry_calls_perform_legacy_recovery_with_detected_depth(monkeypatch):
    calls = []

    def fake_recover(repo_root, clone_depth, **kwargs):
        calls.append(clone_depth)
        return [], gen._legacy_gap_record(clone_depth, "recovery_ambiguous", 0)

    monkeypatch.setattr(gen, "detect_clone_depth", lambda repo_root, **kw: "complete")
    monkeypatch.setattr(gen, "perform_legacy_recovery", fake_recover)
    reg, _, _ = gen.build_registry(_REPO_ROOT, "sha-w", "ts-w")
    assert calls == ["complete"]
    assert reg["legacy_gap"]["recovery_status"] == "recovery_ambiguous"


def test_this_environments_clone_depth_is_detected_truthfully():
    """One integration-style test against the REAL environment — but it
    accepts either valid state and cross-checks the detector's own output
    against git's real result directly, rather than hardcoding an
    assumption about which state the runner happens to be in (CONTENDER-0002
    §G step 1: re-verify live, every time, never assume)."""
    real_git_output = subprocess.check_output(
        ["git", "rev-parse", "--is-shallow-repository"], cwd=_REPO_ROOT, text=True,
    ).strip()
    expected = {"true": "shallow", "false": "complete"}[real_git_output]
    assert gen.detect_clone_depth(_REPO_ROOT) == expected


def test_registry_legacy_gap_clone_depth_matches_live_environment(registry):
    """The committed registry's own legacy_gap.clone_depth_at_generation,
    when generated in THIS run, must match this environment's real,
    independently-checked clone depth — not a value carried over from a
    different (e.g. the original author's) environment."""
    reg, _, _ = registry
    real_git_output = subprocess.check_output(
        ["git", "rev-parse", "--is-shallow-repository"], cwd=_REPO_ROOT, text=True,
    ).strip()
    expected = {"true": "shallow", "false": "complete"}[real_git_output]
    assert reg["legacy_gap"]["clone_depth_at_generation"] == expected


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
