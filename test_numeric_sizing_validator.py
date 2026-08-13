"""Production-path adversarial tests for XASSET-0016 numeric sizing."""
from pathlib import Path
from hashlib import sha256
import shutil
import yaml
import pytest

import numeric_sizing_validator as nsv
from level1_sleeve_synthesis_validator import canonical_record_hash

ROOT = Path(__file__).resolve().parent
_ORIGINAL_SOURCE_ERRORS = nsv._source_errors
_SOURCE_VALIDATION_CACHE = {}


def _cached_source_errors(root):
    digest = sha256()
    for namespace in (nsv.PROFILE_DIR, nsv.POLICY_DIR, nsv.REL_DIR):
        for path in sorted((root / namespace).glob("*.yaml")):
            digest.update(path.name.encode())
            digest.update(path.read_bytes())
    key = digest.hexdigest()
    if key not in _SOURCE_VALIDATION_CACHE:
        _SOURCE_VALIDATION_CACHE[key] = _ORIGINAL_SOURCE_ERRORS(root)
    return list(_SOURCE_VALIDATION_CACHE[key])


@pytest.fixture(autouse=True)
def cache_unchanged_authoritative_sources(monkeypatch):
    """Keep the large adversarial matrix fast without bypassing validation:
    every distinct profile/policy/relationship source corpus is still run once
    through the real authoritative validators."""
    monkeypatch.setattr(nsv, "_source_errors", _cached_source_errors)


def load(path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def write(path, data):
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")


@pytest.fixture
def repo(tmp_path):
    intelligence = tmp_path / "intelligence"
    intelligence.mkdir()
    for child in (ROOT / "intelligence").iterdir():
        if child.name != "level1_sleeve_synthesis":
            (intelligence / child.name).symlink_to(child, target_is_directory=child.is_dir())
            continue
        level1 = intelligence / child.name
        level1.mkdir()
        for namespace in child.iterdir():
            destination = level1 / namespace.name
            if namespace.name in {"numeric_sizing", "profiles", "policy_adoption", "relationships"}:
                shutil.copytree(namespace, destination)
            else:
                destination.symlink_to(namespace, target_is_directory=namespace.is_dir())
    shutil.copy2(ROOT / "targets.yaml", tmp_path / "targets.yaml")
    return tmp_path


def numeric_record(repo, sid):
    return repo / nsv.NUMERIC_DIR / f"{sid}.yaml"


def numeric_manifest(repo):
    return repo / nsv.NUMERIC_DIR / "COHORT_MANIFEST.yaml"


def mutate(path, change):
    data = load(path)
    change(data)
    write(path, data)


def reseal_numeric(repo, sid):
    path = numeric_record(repo, sid)
    data = load(path)
    data["content_sha256"] = canonical_record_hash(data)
    write(path, data)
    manifest = load(numeric_manifest(repo))
    next(row for row in manifest["cohort"] if row["sleeve_id"] == sid)["content_sha256"] = data["content_sha256"]
    write(numeric_manifest(repo), manifest)


def reseal_source(repo, namespace, filename, row_match):
    path = repo / "intelligence/level1_sleeve_synthesis" / namespace / filename
    data = load(path)
    data["content_sha256"] = canonical_record_hash(data)
    write(path, data)
    manifest_path = path.parent / "COHORT_MANIFEST.yaml"
    manifest = load(manifest_path)
    row = next(row for row in manifest["cohort"] if row_match(row))
    row["content_sha256"] = data["content_sha256"]
    write(manifest_path, manifest)
    return data["content_sha256"]


def coordinate_policy_hash(repo, sid):
    new_hash = reseal_source(repo, "policy_adoption", f"{sid}.yaml", lambda row: row["sleeve_id"] == sid)
    data = load(numeric_record(repo, sid))
    data["policy_adoption_reference"]["referenced_content_sha256"] = new_hash
    for adjustment in data["applied_adjustments"]:
        if adjustment["governing_rule_id"] == "R2":
            adjustment["evidence_ref"][0]["referenced_content_sha256"] = new_hash
    write(numeric_record(repo, sid), data)
    reseal_numeric(repo, sid)


def coordinate_profile_hash(repo, sid, *, align_axis=False):
    """Legitimately propagate one changed profile hash through every sealed
    source/reference layer consumed by numeric sizing.  This intentionally
    models the review's strongest coordinated-rehash attack rather than
    leaving a stale dependent reference to trigger an incidental failure."""
    profile_hash = reseal_source(
        repo, "profiles", f"{sid}.yaml", lambda row: row["sleeve_id"] == sid
    )

    relationship_hashes = {}
    relationship_manifest = repo / nsv.REL_DIR / "COHORT_MANIFEST.yaml"
    rel_manifest = load(relationship_manifest)
    for path in sorted((repo / nsv.REL_DIR).glob("*.yaml")):
        if path.name == "COHORT_MANIFEST.yaml":
            continue
        data = load(path)
        changed = False
        for reference in data["profile_references"]:
            if reference["sleeve_id"] == sid:
                reference["referenced_content_sha256"] = profile_hash
                changed = True
        if not changed:
            continue
        data["content_sha256"] = canonical_record_hash(data)
        write(path, data)
        pair = data["sleeve_pair"]
        row = next(
            row for row in rel_manifest["cohort"]
            if row["sleeve_a"] == pair["sleeve_a"] and row["sleeve_b"] == pair["sleeve_b"]
        )
        row["content_sha256"] = data["content_sha256"]
        relationship_hashes[str(path.relative_to(repo))] = data["content_sha256"]
    write(relationship_manifest, rel_manifest)

    policy_hashes = {}
    policy_manifest_path = repo / nsv.POLICY_DIR / "COHORT_MANIFEST.yaml"
    policy_manifest = load(policy_manifest_path)
    for path in sorted((repo / nsv.POLICY_DIR).glob("*.yaml")):
        if path.name == "COHORT_MANIFEST.yaml":
            continue
        data = load(path)
        changed = False
        if data["sleeve_id"] == sid:
            data["profile_reference"]["referenced_content_sha256"] = profile_hash
            changed = True
            if align_axis:
                profile = load(repo / nsv.PROFILE_DIR / f"{sid}.yaml")
                axis_b = nsv.compute_axis_b(profile["evidence_coverage_profile"])
                data["capital_eligibility_status"] = axis_b
                data["sizing_readiness_status"] = nsv.compute_expected_sizing_readiness(
                    data["portfolio_function_status"],
                    axis_b,
                    nsv.compute_live_relationship_ledger(sid, repo),
                )
        reference_groups = [
            data["relationship_references"],
            data["relationship_coverage_ledger"],
            data["blocking_evidence"],
            data["unresolved_relationships"],
        ]
        for group in reference_groups:
            for entry in group:
                reference = entry.get("reference", entry)
                if not isinstance(reference, dict):
                    continue
                record_path = reference.get("record_path")
                if record_path in relationship_hashes:
                    reference["referenced_content_sha256"] = relationship_hashes[record_path]
                    changed = True
        if not changed:
            continue
        data["content_sha256"] = canonical_record_hash(data)
        write(path, data)
        row = next(row for row in policy_manifest["cohort"] if row["sleeve_id"] == data["sleeve_id"])
        row["content_sha256"] = data["content_sha256"]
        policy_hashes[data["sleeve_id"]] = data["content_sha256"]
    write(policy_manifest_path, policy_manifest)

    for policy_sid, policy_hash in policy_hashes.items():
        data = load(numeric_record(repo, policy_sid))
        data["policy_adoption_reference"]["referenced_content_sha256"] = policy_hash
        for adjustment in data["applied_adjustments"]:
            if adjustment["governing_rule_id"] == "R2":
                adjustment["evidence_ref"][0]["referenced_content_sha256"] = policy_hash
        write(numeric_record(repo, policy_sid), data)
        reseal_numeric(repo, policy_sid)


def assert_bad(repo, needle=None):
    errors = nsv.validate(repo)
    assert errors
    if needle:
        assert any(needle in error for error in errors), errors


def bypass_source_validation(monkeypatch):
    monkeypatch.setattr(nsv, "_source_errors", lambda _root: [])


def set_r2_counts(repo, counts):
    for sid, count in counts.items():
        path = repo / nsv.POLICY_DIR / f"{sid}.yaml"
        data = load(path)
        for index, entry in enumerate(data["relationship_coverage_ledger"]):
            entry["coverage_state"] = "deferred_disclosed" if index < count else "sealed_determined"
        write(path, data)


def clear_r3(repo):
    for path in (repo / nsv.REL_DIR).glob("*.yaml"):
        if path.name == "COHORT_MANIFEST.yaml":
            continue
        data = load(path)
        data["secondary_conditions"] = []
        write(path, data)


def set_conditions(repo, stem, conditions):
    path = repo / nsv.REL_DIR / f"{stem}.yaml"
    data = load(path)
    data["secondary_conditions"] = conditions
    write(path, data)


def test_live_candidate_and_outputs():
    assert nsv.validate(ROOT) == []
    _, eligible, output = nsv.derive(ROOT)
    assert eligible == ["crypto", "equity", "fund_broad_market", "fund_gld_defensive"]
    assert {sid: row["target"] for sid, row in output.items()} == {
        "equity": "18.67", "fund_broad_market": "14.67",
        "fund_gld_defensive": "16.67", "crypto": "16.67",
    }


# MAJOR-1: authoritative source validation and independent Axis-C derivation.
@pytest.mark.parametrize("sid,status", [("cash_reserve", "sizing_conditionally_ready"), ("equity", "sizing_blocked")])
def test_stored_axis_c_tampering_rejected_even_when_rehashed(repo, sid, status):
    mutate(repo / nsv.POLICY_DIR / f"{sid}.yaml", lambda data: data.update(sizing_readiness_status=status))
    coordinate_policy_hash(repo, sid)
    assert_bad(repo, "authoritative Stage-4 source validation failed")


@pytest.mark.parametrize("field,value", [
    ("portfolio_function_status", "function_status_unresolved"),
    ("capital_eligibility_status", "not_yet_eligible"),
])
def test_axis_a_or_b_tampering_rejected_after_coordinated_rehash(repo, field, value):
    mutate(repo / nsv.POLICY_DIR / "equity.yaml", lambda data: data.update({field: value}))
    coordinate_policy_hash(repo, "equity")
    assert_bad(repo, "authoritative Stage-4 source validation failed")


def test_internally_invalid_policy_with_valid_hash_rejected(repo):
    mutate(repo / nsv.POLICY_DIR / "crypto.yaml", lambda data: data.update(capital_eligibility_status="invented"))
    coordinate_policy_hash(repo, "crypto")
    assert_bad(repo, "authoritative Stage-4 source validation failed")


def test_internally_invalid_relationship_with_valid_hash_rejected(repo):
    path = repo / nsv.REL_DIR / "crypto_equity.yaml"
    mutate(path, lambda data: data.update(secondary_conditions=["evidence_partial_present", "evidence_partial_present"]))
    reseal_source(repo, "relationships", "crypto_equity.yaml", lambda row: row["sleeve_a"] == "crypto" and row["sleeve_b"] == "equity")
    assert_bad(repo, "relationship source")


def test_substituted_relationship_pair_rejected_after_rehash(repo):
    path = repo / nsv.REL_DIR / "crypto_equity.yaml"
    mutate(path, lambda data: data.update(sleeve_pair={"sleeve_a": "crypto", "sleeve_b": "fund_broad_market"}))
    reseal_source(repo, "relationships", "crypto_equity.yaml", lambda row: row["sleeve_a"] == "crypto" and row["sleeve_b"] == "equity")
    assert_bad(repo, "relationship source")


def test_missing_relationship_record_rejected(repo):
    (repo / nsv.REL_DIR / "crypto_equity.yaml").unlink()
    assert_bad(repo, "relationship source")


def test_duplicate_or_orphan_relationship_record_rejected(repo):
    shutil.copy2(repo / nsv.REL_DIR / "crypto_equity.yaml", repo / nsv.REL_DIR / "crypto_equity_duplicate.yaml")
    assert_bad(repo, "relationship source")


# Round-2 MAJOR: the source chain starts with authoritative profile validity,
# before relationships, policy adoption, Axis B/C, and numeric derivation.
def test_invalid_profile_with_old_hash_rejected(repo):
    mutate(
        repo / nsv.PROFILE_DIR / "equity.yaml",
        lambda data: data.update(evidence_coverage_profile="forced_abstention"),
    )
    assert_bad(repo, "profile source")


def test_coordinated_invalid_profile_rehash_cannot_change_eligibility(repo):
    mutate(
        repo / nsv.PROFILE_DIR / "equity.yaml",
        lambda data: data.update(evidence_coverage_profile="forced_abstention"),
    )
    coordinate_profile_hash(repo, "equity", align_axis=True)

    # Every downstream class has been legitimately resealed and is valid;
    # the profile's internally false live-coverage declaration is the sole
    # authority failure and can no longer influence derive().
    assert nsv.validate_sleeve_relationship_directory(
        repo / nsv.REL_DIR, repo_root=repo
    ).valid
    assert nsv.validate_policy_adoption_directory(
        repo / nsv.POLICY_DIR, repo_root=repo
    ).valid
    profile_result = nsv.validate_sleeve_profile_directory(
        repo / nsv.PROFILE_DIR, repo_root=repo
    )
    assert not profile_result.valid
    assert any("evidence_coverage_profile does not reproduce" in error for result in profile_result.results for error in result.errors)
    with pytest.raises(nsv.SourceValidationError, match="profile source"):
        nsv.derive(repo)


def test_substituted_profile_rejected(repo):
    substituted = load(repo / nsv.PROFILE_DIR / "crypto.yaml")
    substituted["cohort_manifest_entry"] = (
        "intelligence/level1_sleeve_synthesis/profiles/COHORT_MANIFEST.yaml#equity"
    )
    write(repo / nsv.PROFILE_DIR / "equity.yaml", substituted)
    reseal_source(repo, "profiles", "equity.yaml", lambda row: row["sleeve_id"] == "equity")
    assert_bad(repo, "profile source")


def test_missing_profile_rejected(repo):
    (repo / nsv.PROFILE_DIR / "equity.yaml").unlink()
    assert_bad(repo, "profile source")


def test_duplicate_or_orphan_profile_rejected(repo):
    shutil.copy2(
        repo / nsv.PROFILE_DIR / "equity.yaml",
        repo / nsv.PROFILE_DIR / "equity_duplicate.yaml",
    )
    assert_bad(repo, "profile source")


def test_wrong_profile_identity_rejected_after_rehash(repo):
    mutate(
        repo / nsv.PROFILE_DIR / "equity.yaml",
        lambda data: data.update(sleeve_id="crypto"),
    )
    reseal_source(repo, "profiles", "equity.yaml", lambda row: row["sleeve_id"] == "equity")
    assert_bad(repo, "profile source")


def test_invalid_profile_evidence_coverage_state_rejected_after_rehash(repo):
    mutate(
        repo / nsv.PROFILE_DIR / "equity.yaml",
        lambda data: data.update(evidence_coverage_profile="invented"),
    )
    reseal_source(repo, "profiles", "equity.yaml", lambda row: row["sleeve_id"] == "equity")
    assert_bad(repo, "profile source")


def test_valid_cosmetic_profile_change_survives_full_reference_reseal(repo):
    mutate(
        repo / nsv.PROFILE_DIR / "equity.yaml",
        lambda data: data.update(
            drafting_session_or_shard_id="synthetic-valid-cosmetic-profile-change"
        ),
    )
    coordinate_profile_hash(repo, "equity")
    assert nsv.validate(repo) == []


# MAJOR-4: R2 through the real derive() path, with source validation isolated.
@pytest.mark.parametrize("counts,expected", [
    ({"equity": 0, "fund_broad_market": 4, "crypto": 3, "fund_gld_defensive": 3}, {"equity": "up", "fund_broad_market": "down", "crypto": None, "fund_gld_defensive": None}),
    ({"equity": 1, "fund_broad_market": 1, "crypto": 3, "fund_gld_defensive": 2}, {"equity": None, "fund_broad_market": None, "crypto": "down", "fund_gld_defensive": None}),
    ({"equity": 1, "fund_broad_market": 4, "crypto": 4, "fund_gld_defensive": 2}, {"equity": "up", "fund_broad_market": None, "crypto": None, "fund_gld_defensive": None}),
    ({"equity": 2, "fund_broad_market": 3, "crypto": 0, "fund_gld_defensive": 5}, {"equity": None, "fund_broad_market": None, "crypto": "up", "fund_gld_defensive": "down"}),
])
def test_r2_unique_extremes_and_ties_via_derive(repo, monkeypatch, counts, expected):
    bypass_source_validation(monkeypatch)
    set_r2_counts(repo, counts)
    output = nsv.derive(repo)[2]
    assert {sid: row["state"]["R2"] for sid, row in output.items()} == expected


def test_r2_order_independence_via_derive(repo, monkeypatch):
    bypass_source_validation(monkeypatch)
    before = nsv.derive(repo)[2]
    for sid in ("equity", "fund_broad_market", "crypto", "fund_gld_defensive"):
        path = repo / nsv.POLICY_DIR / f"{sid}.yaml"
        mutate(path, lambda data: data["relationship_coverage_ledger"].reverse())
    after = nsv.derive(repo)[2]
    assert {sid: (row["state"], row["target"]) for sid, row in after.items()} == {
        sid: (row["state"], row["target"]) for sid, row in before.items()
    }


# R3 through real relationship-file mutation and derive().
def test_r3_unique_high_via_derive(repo, monkeypatch):
    bypass_source_validation(monkeypatch); clear_r3(repo)
    set_conditions(repo, "cash_reserve_equity", ["evidence_partial_present", "forced_abstention_present", "overlap_or_duplication_disclosed"])
    output = nsv.derive(repo)[2]
    assert output["equity"]["state"]["R3"] == "down"
    assert all(output[s]["state"]["R3"] is None for s in ("crypto", "fund_broad_market", "fund_gld_defensive"))


def test_r3_unique_low_via_derive(repo, monkeypatch):
    bypass_source_validation(monkeypatch); clear_r3(repo)
    for stem in ("crypto_equity", "crypto_fund_gld_defensive", "equity_fund_gld_defensive"):
        set_conditions(repo, stem, ["evidence_partial_present"])
    output = nsv.derive(repo)[2]
    assert output["fund_broad_market"]["state"]["R3"] == "up"


def test_r3_tied_low_and_tied_high_do_not_fire(repo, monkeypatch):
    bypass_source_validation(monkeypatch); clear_r3(repo)
    set_conditions(repo, "equity_fund_broad_market", ["evidence_partial_present"])
    output = nsv.derive(repo)[2]
    assert all(row["state"]["R3"] is None for row in output.values())


def test_r3_repeated_type_does_not_increase_breadth(repo, monkeypatch):
    bypass_source_validation(monkeypatch); clear_r3(repo)
    set_conditions(repo, "cash_reserve_equity", ["evidence_partial_present"])
    set_conditions(repo, "debt_reduction_equity", ["evidence_partial_present"])
    repeated = nsv.derive(repo)[2]["equity"]
    set_conditions(repo, "debt_reduction_equity", ["forced_abstention_present"])
    distinct = nsv.derive(repo)[2]["equity"]
    assert repeated["inputs"]["R3_secondary_condition_breadth"] == 1
    assert distinct["inputs"]["R3_secondary_condition_breadth"] == 2
    assert repeated["state"]["R3"] == distinct["state"]["R3"] == "down"


def test_r3_condition_order_independence(repo, monkeypatch):
    bypass_source_validation(monkeypatch)
    before = nsv.derive(repo)[2]
    for path in (repo / nsv.REL_DIR).glob("*.yaml"):
        if path.name != "COHORT_MANIFEST.yaml":
            mutate(path, lambda data: data["secondary_conditions"].reverse())
    assert nsv.derive(repo)[2] == before


# Arithmetic through validate() plus the production reconciliation function.
@pytest.mark.parametrize("field,value,needle", [
    ("starting_baseline_pct", "16.66", "wrong baseline"),
    ("provisional_target_pct", "17.67", "target does not match"),
    ("provisional_target_pct", "22.67", "outside governed generic range"),
    ("provisional_target_pct", "18.670", "two-decimal precision"),
])
def test_bad_populated_arithmetic_via_validate(repo, field, value, needle):
    mutate(numeric_record(repo, "equity"), lambda data: data.update({field: value}))
    reseal_numeric(repo, "equity")
    assert_bad(repo, needle)


@pytest.mark.parametrize("field,value", [("direction", "down"), ("magnitude_pct", "1.00")])
def test_bad_adjustment_via_validate(repo, field, value):
    mutate(numeric_record(repo, "equity"), lambda data: data["applied_adjustments"][0].update({field: value}))
    reseal_numeric(repo, "equity")
    assert_bad(repo, "adjustments do not match")


def test_retired_r1_adjustment_rejected_with_otherwise_closed_schema(repo):
    mutate(
        numeric_record(repo, "equity"),
        lambda data: (
            data["applied_adjustments"][0].update(governing_rule_id="R1"),
            data.update(governing_rule_ids=["R1"]),
        ),
    )
    reseal_numeric(repo, "equity")
    errors = nsv.validate(repo)
    assert any("applied_adjustments[0]: retired/unknown rule" in error for error in errors)
    assert any("governing_rule_ids contains retired/unknown rule" in error for error in errors)


def test_retired_r1_is_not_only_rejected_by_extra_key_closure(repo):
    mutate(
        numeric_record(repo, "equity"),
        lambda data: data["applied_adjustments"][0].update(
            governing_rule_id="R1", withdrawn_trigger="evidence_quantity"
        ),
    )
    reseal_numeric(repo, "equity")
    errors = nsv.validate(repo)
    assert any("extra keys" in error for error in errors)
    # The companion schema-valid test above separately proves that removing
    # this extra key cannot make the retired rule admissible.


@pytest.mark.parametrize("sum_value,residual", [("100.01", "0.00"), ("66.67", "33.33")])
def test_overshoot_and_rounding_drift_via_validate(repo, sum_value, residual):
    mutate(numeric_manifest(repo), lambda data: data["portfolio_reconciliation"].update(sum_of_assigned_targets_pct=sum_value, unsized_reserved_capital_pct=residual))
    assert_bad(repo, "assigned sum")


def test_negative_residual_via_validate(repo):
    mutate(numeric_manifest(repo), lambda data: data["portfolio_reconciliation"].update(unsized_reserved_capital_pct="-0.01"))
    assert_bad(repo, "two-decimal precision")


def test_exact_100_and_zero_residual_production_reconciliation_path():
    reconciliation = {
        "sum_of_assigned_targets_pct": "100.00",
        "unsized_reserved_capital_pct": "0.00",
        "reconciliation_identity_holds": True,
        "unsized_capital_disclosure": nsv.UNSIZED_DISCLOSURE,
    }
    errors = []
    nsv._validate_reconciliation(reconciliation, nsv.PORTFOLIO_TOTAL, errors)
    assert errors == []


@pytest.mark.parametrize("value", ["0.00", "1.00"])
def test_blocked_null_not_zero_or_numeric(repo, value):
    mutate(numeric_record(repo, "cash_reserve"), lambda data: data.update(provisional_target_pct=value))
    reseal_numeric(repo, "cash_reserve")
    assert_bad(repo, "blocked field provisional_target_pct")


def test_residual_disguised_as_cash_allocation(repo):
    mutate(numeric_manifest(repo), lambda data: data["portfolio_reconciliation"].update(unsized_capital_disclosure="The residual is deployable cash and becomes the cash_reserve allocation."))
    assert_bad(repo, "unsized disclosure")


# MAJOR-2: every probe enters through validate(), with coordinated resealing.
@pytest.mark.parametrize("text", [
    "SPY receives 99.99% of this sleeve.",
    "SPY should receive more capital.",
    "More capital should be allocated to SPY than VEA.",
    "The top-ranked instrument is SPY.",
    "SPY is the preferred instrument.",
    "This instrument deserves more capital.",
    "A composite score is highest.",
    "Capital priority is highest.",
    "SPY is the highest conviction holding.",
    "Instrument SPY was top-ranked.",
    "SPY should not receive 99.99% of this sleeve.",
    "SPY, and VEA, receive 99.99%.",
    "spy receives 99.99%.",
    "SPYs receive 99.99%.",
    "SPY's receives 99.99%.",
    "More citations justify a larger target.",
    "A larger allocation exists because of more evidence bases.",
    "stronger_evidence_maturity increases the target.",
    "CASH and RESERVE serve distinct functions.",
    "The chart shows a breakout above resistance level.",
    "Buy SPY and trim VEA.",
    # Exact fresh round-2 reviewer reproducers.
    "allocate 25 percent to SPY",
    "SPY deserves a larger share",
    "capital should favor BTC",
    "use the chart to size ETH",
    "reserved capital is deployable cash",
    "residual should flow to cash",
    "More evidence supports a larger weight.",
    "SPY should not receive 25 percent.",
    "SPY, and VEA, receive 25 percent.",
    "sPy'S receive 25 percent.",
    # Vulnerability-class coverage: order, voice, punctuation, word forms,
    # numeric forms, chart causality, residual settlement, and withdrawn R1.
    "SPY: allocate twenty-five percent.",
    "Twenty-five percent was allocated to BTC.",
    "ETH warrants a smaller exposure.",
    "The allocation favors SPY while VEA remains secondary.",
    "The technical picture warrants more capital.",
    "Price structure supports a larger weight.",
    "Deploy the residual as cash.",
    "Unsized capital is a cash target.",
    "Broader evidence supports a larger weight.",
    "More bases justify a bigger allocation.",
])
def test_forbidden_free_text_matrix_via_validate(repo, text):
    mutate(numeric_record(repo, "equity"), lambda data: data.update(uncertainty_disclosure=text))
    reseal_numeric(repo, "equity")
    assert_bad(repo, "prohibited")


@pytest.mark.parametrize("text", [
    "The policy record cites intelligence/level1_sleeve_synthesis/policy_adoption/equity.yaml.",
    "XASSET-0016 governs this provisional Level 1 record; no individual instrument allocation is stated.",
    "Evidence is preferred only as a citation-source description, not as an instrument preference.",
    "The chart does not determine sizing.",
    "The technical picture does not warrant a larger weight.",
    "The residual remains unsized and is not a cash allocation.",
    "Reserved capital should not flow to cash.",
    "More evidence does not support a larger weight.",
    "Broader evidence cannot justify a bigger allocation.",
    "Capital should not favor BTC.",
    "SPY is cited as a structural ticker reference; no weight is assigned.",
    "This process does not authorize instrument sizing.",
])
def test_legitimate_citation_and_boundary_prose_allowed(repo, text):
    mutate(numeric_record(repo, "equity"), lambda data: data.update(uncertainty_disclosure=text))
    reseal_numeric(repo, "equity")
    assert nsv.validate(repo) == []


# MAJOR-3: coordinated rehash cannot hide altered governed constants/enums.
@pytest.mark.parametrize("field,value,needle", [
    ("review_condition", "review someday", "review_condition"),
    ("target_classification", "empirically_calibrated", "target_classification"),
    ("governing_decisions", ["XASSET-0016"], "governing_decisions"),
    ("sealed_at", "2099-01-01T00:00:00Z", "sealed_at"),
    ("drafting_session_or_shard_id", "other", "drafting_session"),
    ("cohort_manifest_entry", "wrong#equity", "cohort_manifest_entry"),
    ("record_status", "draft", "record_status"),
])
def test_record_governed_constants_closed(repo, field, value, needle):
    mutate(numeric_record(repo, "equity"), lambda data: data.update({field: value}))
    reseal_numeric(repo, "equity")
    assert_bad(repo, needle)


@pytest.mark.parametrize("field,value", [
    ("schema_version", "2.0"), ("governing_decision", "XASSET-9999"),
    ("shard_id", "other"), ("sealed_at", "2099-01-01T00:00:00Z"),
])
def test_manifest_row_governed_constants_closed(repo, field, value):
    mutate(numeric_manifest(repo), lambda data: data["cohort"][0].update({field: value}))
    assert_bad(repo, "governed constants mismatch")


def test_manifest_top_level_governing_decision_closed(repo):
    mutate(numeric_manifest(repo), lambda data: data.update(governing_decision="XASSET-9999"))
    assert_bad(repo, "manifest governing_decision")


def test_manifest_top_level_schema_version_closed(repo):
    mutate(numeric_manifest(repo), lambda data: data.update(schema_version="2.0"))
    assert_bad(repo, "manifest schema_version")


def test_unknown_numeric_status_rejected_after_rehash(repo):
    mutate(numeric_record(repo, "equity"), lambda data: data.update(numeric_target_status="invented"))
    reseal_numeric(repo, "equity")
    assert_bad(repo, "numeric_target_status")


@pytest.mark.parametrize("location", ["record", "policy_ref", "adjustment", "evidence_ref", "manifest", "row", "reconciliation"])
def test_extra_key_rejected_at_every_nested_level(repo, location):
    if location == "record":
        mutate(numeric_record(repo, "equity"), lambda data: data.update(extra="x")); reseal_numeric(repo, "equity")
    elif location == "policy_ref":
        mutate(numeric_record(repo, "equity"), lambda data: data["policy_adoption_reference"].update(extra="x")); reseal_numeric(repo, "equity")
    elif location == "adjustment":
        mutate(numeric_record(repo, "equity"), lambda data: data["applied_adjustments"][0].update(extra="x")); reseal_numeric(repo, "equity")
    elif location == "evidence_ref":
        mutate(numeric_record(repo, "equity"), lambda data: data["applied_adjustments"][0]["evidence_ref"][0].update(extra="x")); reseal_numeric(repo, "equity")
    elif location == "manifest": mutate(numeric_manifest(repo), lambda data: data.update(extra="x"))
    elif location == "row": mutate(numeric_manifest(repo), lambda data: data["cohort"][0].update(extra="x"))
    else: mutate(numeric_manifest(repo), lambda data: data["portfolio_reconciliation"].update(extra="x"))
    assert_bad(repo, "extra keys")


def test_stale_numeric_policy_hash_rejected(repo):
    mutate(numeric_record(repo, "equity"), lambda data: data["policy_adoption_reference"].update(referenced_content_sha256="0" * 64))
    reseal_numeric(repo, "equity")
    assert_bad(repo, "stale policy_adoption_reference")


def test_manifest_missing_duplicate_and_orphan(repo):
    manifest = load(numeric_manifest(repo)); manifest["cohort"] = manifest["cohort"][:-1] + [manifest["cohort"][0]]; write(numeric_manifest(repo), manifest)
    assert_bad(repo, "manifest population")


# Non-influence through production derive(), isolating intentionally invalid
# counterfactual source masks from the separate authoritative-source tests.
def test_stronger_evidence_maturity_and_favored_id_non_influence(repo, monkeypatch):
    bypass_source_validation(monkeypatch)
    before = nsv.derive(repo)[2]
    for path in (repo / nsv.REL_DIR).glob("*.yaml"):
        if path.name == "COHORT_MANIFEST.yaml": continue
        data = load(path)
        if data.get("favored_sleeve_id") is not None:
            pair = data["sleeve_pair"]
            data["favored_sleeve_id"] = pair["sleeve_b"] if data["favored_sleeve_id"] == pair["sleeve_a"] else pair["sleeve_a"]
            write(path, data)
    assert nsv.derive(repo)[2] == before


def test_evidence_maturity_presence_non_influence(repo, monkeypatch):
    bypass_source_validation(monkeypatch)
    before = nsv.derive(repo)[2]
    path = repo / nsv.REL_DIR / "crypto_equity.yaml"
    mutate(path, lambda data: data.update(primary_disposition="role_preserving", favored_sleeve_id=None))
    after = nsv.derive(repo)[2]
    assert {sid: (row["state"], row["target"]) for sid, row in after.items()} == {
        sid: (row["state"], row["target"]) for sid, row in before.items()
    }


def test_axis_a_evidence_quantity_non_influence(repo, monkeypatch):
    bypass_source_validation(monkeypatch)
    before = nsv.derive(repo)[2]
    mutate(repo / nsv.POLICY_DIR / "equity.yaml", lambda data: data.update(function_rationale=data["function_rationale"] + " Additional citation routes are disclosed without numeric effect."))
    after = nsv.derive(repo)[2]
    assert {sid: (row["state"], row["target"]) for sid, row in after.items()} == {
        sid: (row["state"], row["target"]) for sid, row in before.items()
    }


def test_targets_historical_weights_non_influence(repo):
    before = nsv.derive(repo)[2]
    targets = load(repo / "targets.yaml")
    for row in targets["destination"]:
        row["target_pct"] = 99.99
    write(repo / "targets.yaml", targets)
    assert nsv.derive(repo)[2] == before


def test_manifest_order_and_derivation_determinism(repo):
    first = nsv.derive(repo)[2]
    mutate(numeric_manifest(repo), lambda data: data["cohort"].reverse())
    assert nsv.validate(repo) == []
    assert nsv.derive(repo)[2] == first == nsv.derive(repo)[2]


def test_comparative_consistency_live():
    output = nsv.derive(ROOT)[2]
    assert output["crypto"]["state"] == output["fund_gld_defensive"]["state"]
    assert output["crypto"]["target"] == output["fund_gld_defensive"]["target"] == "16.67"


def test_vacuous_comparative_consistency_note_rejected(repo):
    mutate(
        numeric_record(repo, "equity"),
        lambda data: data.update(comparative_consistency_note="No comment."),
    )
    reseal_numeric(repo, "equity")
    assert_bad(repo, "comparative_consistency_note must identify")


def test_equal_output_peer_requires_no_material_difference_provenance(repo):
    mutate(
        numeric_record(repo, "crypto"),
        lambda data: data.update(
            comparative_consistency_note=(
                "Crypto differs from equity and fund_broad_market only because R2 fires "
                "for those sleeves; fund_gld_defensive is another eligible sleeve."
            )
        ),
    )
    reseal_numeric(repo, "crypto")
    assert_bad(repo, "no material difference from equal-output sleeve fund_gld_defensive")


def test_different_output_peer_requires_live_rule_provenance(repo):
    mutate(
        numeric_record(repo, "equity"),
        lambda data: data.update(
            comparative_consistency_note=(
                "Equity differs from fund_broad_market, crypto, and fund_gld_defensive. "
                "R3 fires for none of the four sleeves."
            )
        ),
    )
    reseal_numeric(repo, "equity")
    assert_bad(repo, "must identify R2 as a difference")
