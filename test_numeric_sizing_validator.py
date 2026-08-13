"""Production-path and structural adversarial tests for XASSET-0018."""
from __future__ import annotations

from copy import deepcopy
from hashlib import sha256
from pathlib import Path
import ast
import shutil

import pytest
import yaml

import numeric_sizing_validator as nsv
from level1_sleeve_synthesis_validator import canonical_record_hash

ROOT = Path(__file__).resolve().parent
_REAL_SOURCE_ERRORS = nsv._source_errors
_SOURCE_CACHE: dict[str, list[str]] = {}


def load(path: Path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def write(path: Path, data) -> None:
    path.write_text(yaml.safe_dump(data, sort_keys=False, width=120), encoding="utf-8")


def _cached_source_errors(root: Path) -> list[str]:
    digest = sha256()
    for namespace in (nsv.PROFILE_DIR, nsv.POLICY_DIR, nsv.RELATIONSHIP_DIR):
        for path in sorted((root / namespace).glob("*.yaml")):
            digest.update(path.name.encode())
            digest.update(path.read_bytes())
    key = digest.hexdigest()
    if key not in _SOURCE_CACHE:
        _SOURCE_CACHE[key] = _REAL_SOURCE_ERRORS(root)
    return list(_SOURCE_CACHE[key])


@pytest.fixture(autouse=True)
def cache_source_validation(monkeypatch):
    monkeypatch.setattr(nsv, "_source_errors", _cached_source_errors)


@pytest.fixture
def repo(tmp_path: Path) -> Path:
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


def record_path(repo: Path, sleeve_id: str) -> Path:
    return repo / nsv.NUMERIC_DIR / f"{sleeve_id}.yaml"


def manifest_path(repo: Path) -> Path:
    return repo / nsv.NUMERIC_DIR / "COHORT_MANIFEST.yaml"


def reseal_record(repo: Path, sleeve_id: str) -> None:
    path = record_path(repo, sleeve_id)
    data = load(path)
    data["content_sha256"] = canonical_record_hash(data)
    write(path, data)
    manifest = load(manifest_path(repo))
    row = next(row for row in manifest["cohort"] if row["sleeve_id"] == sleeve_id)
    row["content_sha256"] = data["content_sha256"]
    write(manifest_path(repo), manifest)


def mutate_record(repo: Path, sleeve_id: str, change) -> None:
    path = record_path(repo, sleeve_id)
    data = load(path)
    change(data)
    write(path, data)
    reseal_record(repo, sleeve_id)


def mutate_manifest(repo: Path, change) -> None:
    path = manifest_path(repo)
    data = load(path)
    change(data)
    write(path, data)


def reseal_source(repo: Path, namespace: Path, filename: str) -> None:
    path = repo / namespace / filename
    data = load(path)
    data["content_sha256"] = canonical_record_hash(data)
    write(path, data)
    manifest = load(path.parent / "COHORT_MANIFEST.yaml")
    if namespace == nsv.RELATIONSHIP_DIR:
        pair = data["sleeve_pair"]
        row = next(
            row for row in manifest["cohort"]
            if row["sleeve_a"] == pair["sleeve_a"] and row["sleeve_b"] == pair["sleeve_b"]
        )
    else:
        row = next(row for row in manifest["cohort"] if row["sleeve_id"] == data["sleeve_id"])
    row["content_sha256"] = data["content_sha256"]
    write(path.parent / "COHORT_MANIFEST.yaml", manifest)


def duplicate_source_projection(
    repo: Path, namespace: Path, filename: str, field: str, index: int = 0
) -> None:
    path = repo / namespace / filename
    data = load(path)
    data[field].append(deepcopy(data[field][index]))
    write(path, data)
    reseal_source(repo, namespace, filename)


def rebuild_and_reseal_numeric_corpus(repo: Path) -> None:
    sealed_at = load(record_path(repo, "equity"))["sealed_at"]
    records, manifest = nsv.build_expected_records(repo, sealed_at)
    for sleeve_id, record in records.items():
        write(record_path(repo, sleeve_id), record)
    write(manifest_path(repo), manifest)


def set_all_sealed_at(repo: Path, value: str) -> None:
    manifest = load(manifest_path(repo))
    for sleeve_id in nsv.SLEEVE_ORDER:
        path = record_path(repo, sleeve_id)
        record = load(path)
        record["sealed_at"] = value
        record["content_sha256"] = canonical_record_hash(record)
        write(path, record)
        row = next(row for row in manifest["cohort"] if row["sleeve_id"] == sleeve_id)
        row["content_sha256"] = record["content_sha256"]
        row["sealed_at"] = value
    write(manifest_path(repo), manifest)


def inject_duplicate_yaml_key(path: Path, anchor: str, duplicate: str | None = None) -> None:
    source = path.read_text(encoding="utf-8")
    assert source.count(anchor) >= 1
    path.write_text(source.replace(anchor, anchor + (duplicate or anchor), 1), encoding="utf-8")


def assert_bad(repo: Path, needle: str | None = None) -> list[str]:
    errors = nsv.validate(repo)
    assert errors
    if needle is not None:
        assert any(needle in error for error in errors), errors
    return errors


def test_live_outputs_and_reconciliation_are_rederived():
    state = nsv.derive_numeric_state(ROOT)
    assert state["assigned"] == nsv.PRESERVED_ASSIGNED
    assert state["blocked"] == nsv.PRESERVED_BLOCKED
    assert state["rule_states"] == {
        "crypto": {"R2": "no_fire", "R3": "no_fire"},
        "equity": {"R2": "up", "R3": "no_fire"},
        "fund_broad_market": {"R2": "down", "R3": "no_fire"},
        "fund_gld_defensive": {"R2": "no_fire", "R3": "no_fire"},
    }
    assert state["targets"] == nsv.PRESERVED_TARGETS
    _, manifest = nsv.build_expected_records(ROOT, "2026-08-13T00:00:00Z")
    assert manifest["portfolio_reconciliation"]["sum_of_assigned_targets_pct"] == "66.68"
    assert manifest["portfolio_reconciliation"]["unsized_reserved_capital_pct"] == "33.32"
    assert manifest["portfolio_reconciliation"]["portfolio_total_pct"] == "100.00"


def test_live_schema2_corpus_passes_production_validator():
    assert nsv.validate(ROOT) == []


@pytest.mark.parametrize(
    "relative_path,anchor,duplicate",
    [
        (nsv.NUMERIC_DIR / "equity.yaml", "schema_version: '2.0'\n", None),
        (
            nsv.NUMERIC_DIR / "equity.yaml",
            "  scope_level: level_1_sleeve_only\n",
            None,
        ),
        (
            nsv.NUMERIC_DIR / "COHORT_MANIFEST.yaml",
            "- sleeve_id: cash_reserve\n",
            "  sleeve_id: cash_reserve\n",
        ),
        (
            nsv.NUMERIC_DIR / "equity.yaml",
            "  - source_kind: sleeve_profile\n",
            "    source_kind: sleeve_profile\n",
        ),
        (
            nsv.NUMERIC_DIR / "cash_reserve.yaml",
            "- reason_code: sealed_unresolved_relationship\n",
            "  reason_code: sealed_unresolved_relationship\n",
        ),
        (
            nsv.NUMERIC_DIR / "equity.yaml",
            "- counterpart_sleeve_id: crypto\n",
            "  counterpart_sleeve_id: crypto\n",
        ),
    ],
)
def test_duplicate_yaml_mapping_keys_rejected_at_authoritative_load(
    repo, relative_path, anchor, duplicate
):
    inject_duplicate_yaml_key(repo / relative_path, anchor, duplicate)
    assert_bad(repo, "duplicate key")


def test_duplicate_yaml_key_in_exact_source_rejected_after_valid_value_shadow(repo):
    path = repo / nsv.POLICY_DIR / "equity.yaml"
    inject_duplicate_yaml_key(
        path,
        "sleeve_id: equity\n",
        "sleeve_id: equity\n",
    )
    assert_bad(repo, "duplicate key")


@pytest.mark.parametrize(
    "value",
    [
        "2026-08-13Z",
        "2026-08-13T12Z",
        "2026-08-13T12:30Z",
        "2026-08-13 12:30:00Z",
        "2026-08-13T12:30:00+00:00",
        "2026-08-13T12:30:00.000Z",
        "2026-02-30T12:30:00Z",
        "2026-08-13T24:00:00Z",
    ],
)
def test_noncanonical_or_invalid_sealed_at_rejected_by_production_validation(repo, value):
    set_all_sealed_at(repo, value)
    assert_bad(repo, "RFC-3339 UTC")


def test_canonical_whole_second_utc_timestamp_is_accepted():
    assert nsv._valid_utc_timestamp("2026-08-13T12:30:00Z")
    assert nsv.validate(ROOT) == []


def test_source_authority_is_exact_common_nineteen_row_snapshot():
    records, _ = nsv.build_expected_records(ROOT, "2026-08-13T00:00:00Z")
    snapshots = [record["source_authority"] for record in records.values()]
    assert all(snapshot == snapshots[0] for snapshot in snapshots)
    assert len(snapshots[0]["profile_references"]) == 6
    assert len(snapshots[0]["policy_adoption_references"]) == 6
    assert len(snapshots[0]["relationship_references"]) == 7


@pytest.mark.parametrize(
    "namespace,filename,change",
    [
        (nsv.PROFILE_DIR, "equity.yaml", lambda data: data.__setitem__("evidence_coverage_profile", "invented")),
        (nsv.RELATIONSHIP_DIR, "equity_fund_gld_defensive.yaml", lambda data: data.__setitem__("primary_disposition", "invented")),
        (nsv.POLICY_DIR, "equity.yaml", lambda data: data.__setitem__("capital_eligibility_status", "invented")),
    ],
)
def test_invalid_upstream_record_rejected_even_after_own_rehash(repo, namespace, filename, change):
    path = repo / namespace / filename
    data = load(path)
    change(data)
    write(path, data)
    reseal_source(repo, namespace, filename)
    assert_bad(repo, "source")


@pytest.mark.parametrize(
    "namespace,filename,field",
    [
        (nsv.POLICY_DIR, "equity.yaml", "blocking_evidence"),
        (nsv.POLICY_DIR, "cash_reserve.yaml", "blocking_evidence"),
        (nsv.POLICY_DIR, "equity.yaml", "relationship_coverage_ledger"),
        (nsv.RELATIONSHIP_DIR, "crypto_equity.yaml", "secondary_conditions"),
    ],
)
def test_duplicate_projected_source_identity_rejected_after_source_rehash(
    repo, namespace, filename, field
):
    duplicate_source_projection(repo, namespace, filename, field)
    assert_bad(repo)


def test_coordinated_duplicate_policy_attack_rejected_after_all_numeric_resealed(repo, monkeypatch):
    duplicate_source_projection(
        repo, nsv.POLICY_DIR, "cash_reserve.yaml", "blocking_evidence"
    )
    with monkeypatch.context() as bypass:
        bypass.setattr(nsv, "_validate_projection_identities", lambda sources: None)
        rebuild_and_reseal_numeric_corpus(repo)
    assert_bad(repo, "duplicate governed projection identity")


def test_same_reason_rows_with_distinct_governed_counterparts_remain_valid():
    policy = load(ROOT / nsv.POLICY_DIR / "equity.yaml")
    secondary_rows = [
        row for row in policy["blocking_evidence"]
        if row["reason_type"] == "secondary_condition_present"
    ]
    assert len(secondary_rows) > 1
    assert len({row["other_sleeve_id"] for row in secondary_rows}) == len(secondary_rows)
    assert nsv.validate(ROOT) == []


@pytest.mark.parametrize("namespace", [nsv.PROFILE_DIR, nsv.POLICY_DIR, nsv.RELATIONSHIP_DIR])
@pytest.mark.parametrize("mutation", ["missing", "extra", "duplicate"])
def test_missing_extra_duplicate_upstream_source_rejected(repo, namespace, mutation):
    directory = repo / namespace
    records = sorted(path for path in directory.glob("*.yaml") if path.name != "COHORT_MANIFEST.yaml")
    if mutation == "missing":
        records[0].unlink()
    else:
        extra = directory / ("orphan.yaml" if mutation == "extra" else "duplicate.yaml")
        shutil.copy2(records[0], extra)
    assert_bad(repo)


@pytest.mark.parametrize(
    "values,expected",
    [
        ({"a": 0, "b": 1, "c": 2}, {"a": "up", "b": "no_fire", "c": "down"}),
        ({"a": 0, "b": 2, "c": 2}, {"a": "up", "b": "no_fire", "c": "no_fire"}),
        ({"a": 0, "b": 0, "c": 2}, {"a": "no_fire", "b": "no_fire", "c": "down"}),
        ({"a": 1, "b": 1, "c": 1}, {"a": "no_fire", "b": "no_fire", "c": "no_fire"}),
    ],
)
def test_r2_r3_unique_extreme_and_tie_mechanics(values, expected):
    assert nsv.derive_rule_states(values) == expected


def test_rule_state_derivation_is_order_independent():
    forward = nsv.derive_rule_states({"a": 0, "b": 1, "c": 2})
    reverse = nsv.derive_rule_states({"c": 2, "b": 1, "a": 0})
    assert forward == reverse


def test_r3_counts_distinct_types_not_repeated_occurrences():
    assert nsv.distinct_condition_breadth([["evidence_partial_present"], ["evidence_partial_present"]]) == 1
    assert nsv.distinct_condition_breadth([["evidence_partial_present"], ["forced_abstention_present"]]) == 2


def test_r2_adjustment_uses_exact_four_policy_evidence_rows():
    state = nsv.derive_numeric_state(ROOT)
    adjustment = nsv._adjustments(state, "equity")[0]
    assert adjustment["governing_rule_id"] == "R2"
    assert [row["source_record_id"] for row in adjustment["evidence_refs"]] == list(nsv.PRESERVED_ASSIGNED)
    assert all(row["selector"] == "relationship_coverage_ledger.deferred_disclosed_count" for row in adjustment["evidence_refs"])


def test_r3_adjustment_uses_exact_six_relationship_evidence_rows():
    state = nsv.derive_numeric_state(ROOT)
    synthetic = deepcopy(state)
    synthetic["rule_states"]["crypto"]["R3"] = "up"
    adjustment = next(row for row in nsv._adjustments(synthetic, "crypto") if row["governing_rule_id"] == "R3")
    assert [row["source_record_id"] for row in adjustment["evidence_refs"]] == list(nsv.R3_EVIDENCE_RELATIONSHIPS)
    assert all(row["selector"] == "secondary_conditions.distinct_type_set" for row in adjustment["evidence_refs"])


@pytest.mark.parametrize(
    "sleeve_id,field,value",
    [
        ("cash_reserve", "provisional_target_pct", "0.00"),
        ("cash_reserve", "starting_baseline_pct", "16.67"),
        ("cash_reserve", "target_classification", "provisional_governance_guardrail"),
        ("equity", "provisional_target_pct", None),
        ("equity", "starting_baseline_pct", None),
        ("equity", "review_conditions", []),
    ],
)
def test_assigned_blocked_nullability_is_exact(repo, sleeve_id, field, value):
    mutate_record(repo, sleeve_id, lambda data: data.__setitem__(field, value))
    assert_bad(repo, field)


@pytest.mark.parametrize(
    "sleeve_id,field,value",
    [
        ("equity", "schema_version", "1.0"),
        ("equity", "numeric_target_status", "invented"),
        ("equity", "target_classification", "empirically_calibrated"),
        ("equity", "record_status", "draft"),
        ("cash_reserve", "numeric_target_status", "provisional_target_assigned"),
    ],
)
def test_wrong_schema_or_enum_rejected_after_rehash(repo, sleeve_id, field, value):
    mutate_record(repo, sleeve_id, lambda data: data.__setitem__(field, value))
    assert_bad(repo, field)


def test_mixed_version_cohort_rejected(repo):
    mutate_record(repo, "equity", lambda data: data.__setitem__("schema_version", "1.0"))
    assert_bad(repo, "schema_version")


@pytest.mark.parametrize(
    "mutation",
    [
        lambda row: row.__setitem__("source_kind", "invented"),
        lambda row: row.__setitem__("source_record_id", "instrument_id"),
        lambda row: row.__setitem__("source_path", "arbitrary/path.yaml"),
        lambda row: row.__setitem__("source_content_sha256", "0" * 64),
    ],
)
def test_authority_reference_identity_path_and_hash_are_closed(repo, mutation):
    def change(data):
        mutation(data["source_authority"]["profile_references"][0])
    mutate_record(repo, "equity", change)
    assert_bad(repo)


@pytest.mark.parametrize(
    "field,value",
    [
        ("selector", "ticker"),
        ("selector", "instrument.target_pct"),
        ("selector", "capital_priority"),
        ("projection", "rank_score"),
        ("projection", "deployment_state"),
    ],
)
def test_trigger_selector_projection_vocabulary_is_closed(repo, field, value):
    def change(data):
        data["applied_adjustments"][0]["evidence_refs"][0][field] = value
    mutate_record(repo, "equity", change)
    assert_bad(repo)


@pytest.mark.parametrize(
    "field,value",
    [
        ("selector", "instrument_id"),
        ("projection", "preference"),
        ("counterpart_sleeve_id", "equity"),
    ],
)
def test_uncertainty_reference_vocabulary_and_identity_are_closed(repo, field, value):
    def change(data):
        data["uncertainty_assertions"][0]["source_ref"][field] = value
    mutate_record(repo, "crypto", change)
    assert_bad(repo)


@pytest.mark.parametrize(
    "field,value",
    [
        ("assertion_type", "existing_level2_constraint_context"),
        ("numeric_effect", "up"),
    ],
)
def test_uncertainty_assertions_have_no_hidden_sizing_authority(repo, field, value):
    def change(data):
        data["uncertainty_assertions"][0][field] = value
    mutate_record(repo, "equity", change)
    assert_bad(repo)


def test_uncertainty_assertion_missing_extra_duplicate_and_order_rejected(repo):
    original = load(record_path(repo, "equity"))["uncertainty_assertions"]
    for change in (
        lambda rows: rows.pop(),
        lambda rows: rows.append(deepcopy(rows[0])),
        lambda rows: rows.reverse(),
    ):
        shutil.copy2(ROOT / nsv.NUMERIC_DIR / "equity.yaml", record_path(repo, "equity"))
        def mutate(data):
            change(data["uncertainty_assertions"])
        mutate_record(repo, "equity", mutate)
        assert_bad(repo)
    assert original


def test_all_builder_assertions_follow_xasset0018_canonical_order():
    records, _ = nsv.build_expected_records(ROOT, "2026-08-13T00:00:00Z")
    for sleeve_id in nsv.PRESERVED_ASSIGNED:
        assertions = records[sleeve_id]["uncertainty_assertions"]
        assert assertions == sorted(assertions, key=nsv._assertion_sort_key)


def test_equity_same_type_profile_assertions_sort_by_selector_string():
    records, _ = nsv.build_expected_records(ROOT, "2026-08-13T00:00:00Z")
    selectors = [
        row["source_ref"]["selector"]
        for row in records["equity"]["uncertainty_assertions"]
        if row["assertion_type"] == "level2_valuation_coverage_gap"
    ]
    assert selectors == [
        "profile.abstention.equity_discount_rate_abstained",
        "profile.abstention.equity_valuation_result_partial",
    ]


def test_blocked_records_have_exact_reason_population_and_no_comparisons():
    cash = load(ROOT / nsv.NUMERIC_DIR / "cash_reserve.yaml")
    debt = load(ROOT / nsv.NUMERIC_DIR / "debt_reduction.yaml")
    assert len(cash["blocking_reason_refs"]) == 5
    assert len(debt["blocking_reason_refs"]) == 6
    assert cash["comparative_provenance"] == debt["comparative_provenance"] == []


@pytest.mark.parametrize("mutation", ["missing", "extra", "wrong_reason", "fake_comparison"])
def test_blocked_reason_cardinality_reason_and_comparison_are_exact(repo, mutation):
    def change(data):
        if mutation == "missing":
            data["blocking_reason_refs"].pop()
        elif mutation == "extra":
            data["blocking_reason_refs"].append(deepcopy(data["blocking_reason_refs"][0]))
        elif mutation == "wrong_reason":
            data["blocking_reason_refs"][0]["reason_code"] = "invented"
        else:
            data["comparative_provenance"].append({})
    mutate_record(repo, "cash_reserve", change)
    assert_bad(repo)


@pytest.mark.parametrize("component", ["reason_type", "other_sleeve_id", "reference_mode", "relationship_record_id"])
def test_blocking_source_entry_selector_grammar_is_exact(repo, component):
    def change(data):
        selector = data["blocking_reason_refs"][0]["source_entry_selector"]
        selector[component] = "invented"
    mutate_record(repo, "cash_reserve", change)
    assert_bad(repo)


def test_assigned_comparative_rows_are_all_other_assigned_sleeves_only():
    for sleeve_id in nsv.PRESERVED_ASSIGNED:
        rows = load(ROOT / nsv.NUMERIC_DIR / f"{sleeve_id}.yaml")["comparative_provenance"]
        assert len(rows) == 3
        assert [row["counterpart_sleeve_id"] for row in rows] == [
            other for other in nsv.PRESERVED_ASSIGNED if other != sleeve_id
        ]


@pytest.mark.parametrize("mutation", ["reversed_relation", "reversed_r2", "reversed_r3", "wrong_rule", "self", "blocked", "missing", "extra"])
def test_comparative_provenance_adversarial_matrix(repo, mutation):
    def change(data):
        rows = data["comparative_provenance"]
        if mutation == "reversed_relation":
            rows[0]["target_relation"] = "lower" if rows[0]["target_relation"] != "lower" else "higher"
        elif mutation == "reversed_r2":
            rows[0]["self_rule_states"]["R2"] = "down"
        elif mutation == "reversed_r3":
            rows[0]["counterpart_rule_states"]["R3"] = "up"
        elif mutation == "wrong_rule":
            rows[0]["differing_rule_ids"] = ["R3"]
        elif mutation == "self":
            rows[0]["counterpart_sleeve_id"] = data["sleeve_id"]
        elif mutation == "blocked":
            rows[0]["counterpart_sleeve_id"] = "cash_reserve"
        elif mutation == "missing":
            rows.pop()
        else:
            rows.append(deepcopy(rows[0]))
    mutate_record(repo, "equity", change)
    assert_bad(repo)


def test_differing_rule_ids_are_rule_id_differences_not_tuple_symmetric_difference():
    state = {
        "assigned": ("a", "b"),
        "targets": {"a": "18.00", "b": "14.00"},
        "rule_states": {
            "a": {"R2": "up", "R3": "no_fire"},
            "b": {"R2": "down", "R3": "no_fire"},
        },
    }
    row = nsv._comparative_rows(state, "a")[0]
    assert row["differing_rule_ids"] == ["R2"]


def test_two_rule_cancellation_retains_directions_and_rule_ids():
    state = {
        "assigned": ("a", "b"),
        "targets": {"a": "16.67", "b": "16.67"},
        "rule_states": {
            "a": {"R2": "up", "R3": "down"},
            "b": {"R2": "down", "R3": "up"},
        },
    }
    row = nsv._comparative_rows(state, "a")[0]
    assert row["target_relation"] == "equal"
    assert row["differing_rule_ids"] == ["R2", "R3"]
    assert row["cancellation_status"] == "cancelled_to_equal"


@pytest.mark.parametrize(
    "field,value",
    [
        ("sum_of_assigned_targets_pct", "66.69"),
        ("sum_of_assigned_targets_pct", "100.01"),
        ("unsized_reserved_capital_pct", "-0.01"),
        ("unsized_reserved_capital_pct", "0.00"),
        ("portfolio_total_pct", "99.99"),
        ("assigned_record_count", 5),
        ("blocked_record_count", 1),
    ],
)
def test_residual_and_count_reconciliation_rejects_wrong_values(repo, field, value):
    mutate_manifest(repo, lambda data: data["portfolio_reconciliation"].__setitem__(field, value))
    assert_bad(repo, field)


@pytest.mark.parametrize(
    "field,value",
    [
        ("residual_type", "cash"),
        ("sleeve_id", "cash_reserve"),
        ("cash_reserve_equivalence", "allowed"),
        ("redistribution_status", "automatic"),
        ("policy_target_status", "target"),
    ],
)
def test_residual_cash_and_redistribution_boundary_is_structural(repo, field, value):
    def change(data):
        data["portfolio_reconciliation"]["residual_classification"][field] = value
    mutate_manifest(repo, change)
    assert_bad(repo, field)


@pytest.mark.parametrize(
    "family",
    [
        "ticker", "instrument_id", "instrument_weight", "target", "rank", "score",
        "preference", "capital_priority", "chart_signal", "technical_signal",
        "deployment", "execution", "trade", "order", "auto_redistribution",
    ],
)
def test_level2_and_execution_families_are_structurally_impossible(repo, family):
    mutate_record(repo, "equity", lambda data: data.__setitem__(family, "injected"))
    assert_bad(repo, "key set/order")


def _add_extra(data, location):
    target = {
        "record": data,
        "source_authority": data["source_authority"],
        "authority_ref": data["source_authority"]["profile_references"][0],
        "adjustment": data["applied_adjustments"][0],
        "trigger_ref": data["applied_adjustments"][0]["evidence_refs"][0],
        "assertion": data["uncertainty_assertions"][0],
        "uncertainty_ref": data["uncertainty_assertions"][0]["source_ref"],
        "selector_key": data["uncertainty_assertions"][0]["source_ref"]["selector_key"],
        "comparison": data["comparative_provenance"][0],
        "rule_states": data["comparative_provenance"][0]["self_rule_states"],
        "boundaries": data["authority_boundaries"],
        "review_condition": data["review_conditions"][0],
    }[location]
    target["extra"] = "injected"


@pytest.mark.parametrize(
    "location",
    [
        "record", "source_authority", "authority_ref", "adjustment", "trigger_ref",
        "assertion", "uncertainty_ref", "selector_key", "comparison", "rule_states",
        "boundaries", "review_condition",
    ],
)
def test_extra_key_rejected_at_every_assigned_nested_level(repo, location):
    mutate_record(repo, "equity", lambda data: _add_extra(data, location))
    assert_bad(repo, "key set/order")


@pytest.mark.parametrize("location", ["blocking", "blocking_selector"])
def test_extra_key_rejected_at_every_blocked_nested_level(repo, location):
    def change(data):
        target = data["blocking_reason_refs"][0]
        if location == "blocking_selector":
            target = target["source_entry_selector"]
        target["extra"] = "injected"
    mutate_record(repo, "cash_reserve", change)
    assert_bad(repo, "key set/order")


@pytest.mark.parametrize("location", ["manifest", "row", "reconciliation", "residual"])
def test_extra_key_rejected_at_every_manifest_nested_level(repo, location):
    def change(data):
        target = {
            "manifest": data,
            "row": data["cohort"][0],
            "reconciliation": data["portfolio_reconciliation"],
            "residual": data["portfolio_reconciliation"]["residual_classification"],
        }[location]
        target["extra"] = "injected"
    mutate_manifest(repo, change)
    assert_bad(repo, "key set/order")


def test_manifest_missing_duplicate_extra_orphan_and_wrong_order(repo):
    changes = (
        lambda cohort: cohort.pop(),
        lambda cohort: cohort.append(deepcopy(cohort[0])),
        lambda cohort: cohort.append({**deepcopy(cohort[0]), "sleeve_id": "seventh_sleeve"}),
        lambda cohort: cohort.reverse(),
    )
    for change in changes:
        shutil.copy2(ROOT / nsv.NUMERIC_DIR / "COHORT_MANIFEST.yaml", manifest_path(repo))
        mutate_manifest(repo, lambda data: change(data["cohort"]))
        assert_bad(repo)


def test_manifest_bidirectional_stale_hash_and_status_rejected(repo):
    mutate_manifest(repo, lambda data: data["cohort"][0].__setitem__("content_sha256", "0" * 64))
    assert_bad(repo, "content_sha256")
    shutil.copy2(ROOT / nsv.NUMERIC_DIR / "COHORT_MANIFEST.yaml", manifest_path(repo))
    mutate_manifest(repo, lambda data: data["cohort"][0].__setitem__("numeric_target_status", "provisional_target_assigned"))
    assert_bad(repo, "numeric_target_status")


def test_coordinated_rehash_cannot_legitimize_invalid_structured_content(repo):
    mutate_record(repo, "equity", lambda data: data["authority_boundaries"].__setitem__("allocation_check_authority", "allowed"))
    assert_bad(repo, "allocation_check_authority")


@pytest.mark.parametrize("attack", ["level2_selector", "cash_residual", "comparative_reversal"])
def test_correction_matrix_fresh_structural_attacks_remain_rejected(repo, attack):
    if attack == "level2_selector":
        def change(data):
            data["applied_adjustments"][0]["evidence_refs"][0]["selector"] = "instrument.weight"
        mutate_record(repo, "equity", change)
    elif attack == "cash_residual":
        mutate_manifest(
            repo,
            lambda data: data["portfolio_reconciliation"]["residual_classification"].__setitem__(
                "cash_reserve_equivalence", "cash_reserve"
            ),
        )
    else:
        def change(data):
            relation = data["comparative_provenance"][0]["target_relation"]
            data["comparative_provenance"][0]["target_relation"] = (
                "lower" if relation != "lower" else "higher"
            )
        mutate_record(repo, "equity", change)
    assert_bad(repo)


def test_targets_history_holdings_and_chart_state_have_no_numeric_influence(repo):
    baseline = nsv.derive_numeric_state(repo)["targets"]
    targets = (repo / "targets.yaml").read_text(encoding="utf-8")
    (repo / "targets.yaml").write_text(targets.replace("target_pct: 1.50", "target_pct: 9.99", 1), encoding="utf-8")
    (repo / "holdings.yaml").write_text("invented: true\n", encoding="utf-8")
    (repo / "chart_signal.yaml").write_text("signal: buy\n", encoding="utf-8")
    assert nsv.derive_numeric_state(repo)["targets"] == baseline


def test_stronger_evidence_maturity_is_assertion_only_and_has_no_adjustment():
    records, _ = nsv.build_expected_records(ROOT, "2026-08-13T00:00:00Z")
    equity = records["equity"]
    assert any(row["assertion_type"] == "stronger_evidence_maturity" for row in equity["uncertainty_assertions"])
    assert all(row["governing_rule_id"] in {"R2", "R3"} for row in equity["applied_adjustments"])
    assert all(row["numeric_effect"] == "none" for row in equity["uncertainty_assertions"])


def test_validator_has_no_allocator_margin_network_or_write_path():
    tree = ast.parse((ROOT / "numeric_sizing_validator.py").read_text(encoding="utf-8"))
    imports = {
        alias.name
        for node in ast.walk(tree)
        if isinstance(node, (ast.Import, ast.ImportFrom))
        for alias in node.names
    }
    assert "allocate" not in imports
    assert "margin_state" not in imports
    assert not {"requests", "urllib", "httpx"} & imports
    source = (ROOT / "numeric_sizing_validator.py").read_text(encoding="utf-8")
    assert "write_text(" not in source
    assert ".open(\"w" not in source
    assert ".open('w" not in source


def test_validator_is_read_only_over_numeric_corpus(repo):
    before = {
        path.relative_to(repo): sha256(path.read_bytes()).hexdigest()
        for path in (repo / nsv.NUMERIC_DIR).glob("*.yaml")
    }
    assert nsv.validate(repo) == []
    after = {
        path.relative_to(repo): sha256(path.read_bytes()).hexdigest()
        for path in (repo / nsv.NUMERIC_DIR).glob("*.yaml")
    }
    assert after == before
