"""Read-only XASSET-0016 Level-1 numeric-sizing validator.

The numeric layer never treats a sealed hash or a stored Stage-4 label as
authority by itself.  It first runs the existing Level-1 profile,
relationship, and policy-adoption validators, then independently recomputes
Axis B/Axis C and both numeric triggers from those validated live sources.
"""
from __future__ import annotations

from decimal import Decimal, ROUND_HALF_EVEN
from pathlib import Path
import re
import yaml

from level1_sleeve_synthesis_validator import (
    SLEEVE_IDS,
    canonical_record_hash,
    compute_axis_b,
    compute_expected_sizing_readiness,
    compute_live_relationship_ledger,
    validate_policy_adoption_directory,
    validate_sleeve_relationship_directory,
    _comparative_superiority_scan,
    _prohibited_content_scan,
    _scan_contender_citation,
    _scan_key_names_recursive,
    _stage4_bounded_conclusion_scan,
)

SCHEMA_VERSION = "1.0"
READY = frozenset({"sizing_conditionally_ready", "sizing_ready"})
BASELINE = Decimal("16.67")
INCREMENT = Decimal("2.00")
PORTFOLIO_TOTAL = Decimal("100.00")
NUMERIC_DIR = "intelligence/level1_sleeve_synthesis/numeric_sizing"
PROFILE_DIR = "intelligence/level1_sleeve_synthesis/profiles"
POLICY_DIR = "intelligence/level1_sleeve_synthesis/policy_adoption"
REL_DIR = "intelligence/level1_sleeve_synthesis/relationships"
STATUS_ASSIGNED = "provisional_target_assigned"
STATUS_BLOCKED = "no_provisional_target_pending_axis_c"
TARGET_CLASS = "provisional_governance_guardrail"
GOVERNING_DECISIONS = ["XASSET-0016", "XASSET-0017"]
GOVERNING_DECISION = "XASSET-0016"
SEALED_AT = "2026-08-12T00:00:00Z"
SHARD_ID = "xasset-0016-level1-numeric-sizing-implementation"
BOUNDARY = "Provisional Level 1 sleeve sizing only; no Level 2 instrument selection or sizing, no adopted policy, and no allocation check is authorized by this record."
REVIEW = "Revisit upon the first governed sizing-challenge risk analysis or targeted backtest, a material sealed-population or relationship-accounting change, or a separately authorized study of the baseline or increment."
UNSIZED_DISCLOSURE = "This residual is capital not yet assigned to any sleeve pending resolution of a blocked sleeve status or additional evidence; it is not the cash_reserve sleeve, not an automatically deployable cash allocation, and is never redistributed without a future governance act."

RECORD_KEYS = frozenset({"schema_version","sleeve_id","policy_adoption_reference","numeric_target_status","provisional_target_pct","starting_baseline_pct","applied_adjustments","governing_rule_ids","target_classification","review_condition","uncertainty_disclosure","comparative_consistency_note","blocking_rationale","sizing_boundary_note","record_status","sealed_at","governing_decisions","drafting_session_or_shard_id","content_sha256","cohort_manifest_entry"})
REF_KEYS = frozenset({"record_path", "referenced_content_sha256"})
ADJ_KEYS = frozenset({"governing_rule_id", "direction", "magnitude_pct", "evidence_ref"})
MANIFEST_KEYS = frozenset({"schema_version","governing_decision","cohort","portfolio_reconciliation"})
ROW_KEYS = frozenset({"sleeve_id","record_path","content_sha256","schema_version","governing_decision","shard_id","sealed_at"})
REC_KEYS = frozenset({"sum_of_assigned_targets_pct","unsized_reserved_capital_pct","reconciliation_identity_holds","unsized_capital_disclosure"})

_NUMERIC_SPECIFIC_TEXT_PATTERNS = tuple(re.compile(p, re.IGNORECASE) for p in (
    # Level-2 amount/percentage in both ordinary and passive/reversed order.
    r"\b[A-Z]{2,5}(?:'s|s)?\b[^.]{0,60}\b(?:receives?|gets?|is\s+assigned|was\s+assigned|should\s+receive|should\s+get)\b[^.]{0,40}(?:\d+(?:\.\d+)?\s*%|more\s+capital)",
    r"(?:\d+(?:\.\d+)?\s*%|more\s+capital)[^.]{0,60}\b(?:is|was|should\s+be)\s+(?:assigned|allocated|given)\b[^.]{0,40}\b[A-Z]{2,5}(?:'s|s)?\b",
    # Rank/preference/conviction and capital-priority assertions.
    r"\b(?:top[-\s]?ranked|highest[-\s]?ranked|preferred|highest\s+conviction)\b[^.]{0,40}\b(?:instrument|ticker|fund|coin|holding|sleeve)\b",
    r"\b(?:instrument|ticker|fund|coin|holding|sleeve)\b[^.]{0,40}\b(?:is|was|remains?|ranks?)\b[^.]{0,20}\b(?:top[-\s]?ranked|preferred|highest\s+conviction)\b",
    r"\b(?:composite\s+)?(?:score[sd]?|ranking|ranked|capital\s+priority)\b",
    r"\b(?:deserves?|warrants?|merits?|should\s+receive|should\s+get)\b[^.]{0,30}\b(?:more|less|greater|larger|smaller|higher|lower)\s+capital\b",
    # Withdrawn-R1/evidence-quantity reward under forward or reversed order.
    r"\b(?:more|additional|greater)\s+(?:citations?|evidence\s+bases?|documentation|evidence\s+routes?)\b[^.]{0,80}\b(?:deserves?|warrants?|justif(?:y|ies)|earns?|receives?|gets?)\b[^.]{0,30}\b(?:more|larger|higher|additional)\s+(?:capital|target|allocation)\b",
    r"\b(?:more|larger|higher|additional)\s+(?:capital|target|allocation)\b[^.]{0,80}\b(?:because|due\s+to|for)\b[^.]{0,30}\b(?:more|additional|greater)\s+(?:citations?|evidence\s+bases?|documentation|evidence\s+routes?)\b",
    # Explicit attempt to make the prohibited maturity fields numeric inputs.
    r"\b(?:stronger_evidence_maturity|favored_sleeve_id)\b[^.]{0,80}\b(?:increase|decrease|adjust|move|raise|lower|capital|target|allocation)\b",
))


class SourceValidationError(ValueError):
    """Authoritative Stage-4 source corpus is invalid or incomplete."""


def _load(path: Path):
    with path.open(encoding="utf-8") as f:
        return yaml.safe_load(f)


def _two(value) -> Decimal:
    if isinstance(value, (float, int)) or not re.fullmatch(r"\d+\.\d{2}", str(value)):
        raise ValueError(f"expected YAML string with two-decimal precision, got {value!r}")
    return Decimal(str(value))


def _closed(obj, keys, where, errors):
    if not isinstance(obj, dict):
        errors.append(f"{where} must be a mapping")
        return False
    missing, extra = set(keys) - set(obj), set(obj) - set(keys)
    if missing:
        errors.append(f"{where} missing keys: {sorted(missing)}")
    if extra:
        errors.append(f"{where} extra keys: {sorted(extra)}")
    return not missing


def _source_errors(repo_root: Path) -> list[str]:
    checks = (
        ("relationship", validate_sleeve_relationship_directory(repo_root / REL_DIR, repo_root=repo_root)),
        ("policy_adoption", validate_policy_adoption_directory(repo_root / POLICY_DIR, repo_root=repo_root)),
    )
    errors = []
    for kind, result in checks:
        for item in result.results:
            errors.extend(f"{kind} source [{item.source}]: {error}" for error in item.errors)
    return errors


def _validated_sources(repo_root: Path):
    errors = _source_errors(repo_root)
    if errors:
        raise SourceValidationError("\n".join(errors))
    policies = {}
    independently_derived_sizing = {}
    for sid in SLEEVE_IDS:
        policy_path = repo_root / POLICY_DIR / f"{sid}.yaml"
        policy = _load(policy_path)
        profile = _load(repo_root / PROFILE_DIR / f"{sid}.yaml")
        axis_b = compute_axis_b(profile.get("evidence_coverage_profile"))
        ledger = compute_live_relationship_ledger(sid, repo_root)
        sizing = compute_expected_sizing_readiness(
            policy.get("portfolio_function_status"), axis_b, ledger
        )
        # This is deliberately not the stored policy Axis-C field.  The
        # authoritative policy validator above separately rejects any stale
        # stored Axis A/B/C combination.
        independently_derived_sizing[sid] = sizing
        policies[sid] = (policy_path, policy)
    return policies, independently_derived_sizing


def derive(repo_root: Path):
    policies, sizing = _validated_sources(repo_root)
    eligible = sorted(s for s, status in sizing.items() if status in READY)
    # R2's governed field is the policy record's own coverage ledger.  It is
    # safe to read only after the authoritative Stage-4 validator above has
    # proved it byte-for-byte consistent with the live relationship corpus.
    deferred = {
        s: sum(entry["coverage_state"] == "deferred_disclosed" for entry in policies[s][1]["relationship_coverage_ledger"])
        for s in eligible
    }
    breadth = {s: set() for s in eligible}
    rel_refs = {s: [] for s in eligible}
    for path in sorted((repo_root / REL_DIR).glob("*.yaml")):
        if path.name == "COHORT_MANIFEST.yaml":
            continue
        data = _load(path)
        pair = data["sleeve_pair"]
        for sid in (pair["sleeve_a"], pair["sleeve_b"]):
            if sid in breadth:
                breadth[sid].update(data["secondary_conditions"])
                rel_refs[sid].append({
                    "record_path": str(path.relative_to(repo_root)),
                    "referenced_content_sha256": canonical_record_hash(data),
                })
    states = {s: {} for s in eligible}
    for rule, values in (("R2", deferred), ("R3", {s: len(v) for s, v in breadth.items()})):
        lo, hi = min(values.values()), max(values.values())
        for sid, value in values.items():
            states[sid][rule] = (
                "up" if value == lo and list(values.values()).count(lo) == 1
                else "down" if value == hi and list(values.values()).count(hi) == 1
                else None
            )
    output = {}
    for sid in eligible:
        adjustments = []
        for rule in ("R2", "R3"):
            direction = states[sid][rule]
            if direction:
                refs = ([{
                    "record_path": str(policies[sid][0].relative_to(repo_root)),
                    "referenced_content_sha256": canonical_record_hash(policies[sid][1]),
                }] if rule == "R2" else rel_refs[sid])
                adjustments.append({
                    "governing_rule_id": rule,
                    "direction": direction,
                    "magnitude_pct": "2.00",
                    "evidence_ref": refs,
                })
        net = sum(INCREMENT if a["direction"] == "up" else -INCREMENT for a in adjustments)
        output[sid] = {
            "baseline": "16.67",
            "inputs": {
                "R2_deferred_count": deferred[sid],
                "R3_secondary_condition_breadth": len(breadth[sid]),
            },
            "adjustments": adjustments,
            "rules": [a["governing_rule_id"] for a in adjustments],
            "target": str((BASELINE + net).quantize(Decimal("0.01"), rounding=ROUND_HALF_EVEN)),
            "state": states[sid],
        }
    return policies, eligible, output


def _scan_numeric_free_text(text, where, errors, repo_root):
    if not isinstance(text, str):
        return
    for finding in _prohibited_content_scan(text):
        errors.append(f"{where} contains prohibited content ({finding})")
    for finding in _comparative_superiority_scan(text):
        errors.append(f"{where} contains prohibited content ({finding})")
    for finding in _stage4_bounded_conclusion_scan(text, repo_root=repo_root):
        errors.append(f"{where} contains prohibited content ({finding})")
    for finding in _scan_contender_citation(text):
        errors.append(f"{where} contains prohibited content ({finding})")
    for pattern in _NUMERIC_SPECIFIC_TEXT_PATTERNS:
        if pattern.search(text):
            errors.append(f"{where} contains prohibited numeric-sizing content ({pattern.pattern})")


def _validate_reconciliation(reconciliation, live_sum: Decimal, errors: list[str]):
    """Production reconciliation path, including defensive reachable and
    currently-unreachable arithmetic cases required by XASSET-0016."""
    if not _closed(reconciliation, REC_KEYS, "portfolio_reconciliation", errors):
        return
    residual = (PORTFOLIO_TOTAL - live_sum).quantize(Decimal("0.01"), rounding=ROUND_HALF_EVEN)
    try:
        stored_sum = _two(reconciliation["sum_of_assigned_targets_pct"])
        stored_residual = _two(reconciliation["unsized_reserved_capital_pct"])
        if stored_sum != live_sum or stored_sum > PORTFOLIO_TOTAL:
            errors.append("manifest assigned sum mismatch/overshoot")
        if stored_residual < 0 or stored_residual != residual:
            errors.append("manifest residual mismatch/negative")
        if stored_sum + stored_residual != PORTFOLIO_TOTAL or reconciliation["reconciliation_identity_holds"] is not True:
            errors.append("manifest reconciliation identity fails")
    except ValueError as exc:
        errors.append(f"manifest: {exc}")
    if reconciliation["unsized_capital_disclosure"] != UNSIZED_DISCLOSURE:
        errors.append("manifest unsized disclosure invalid")


def validate(repo_root: Path) -> list[str]:
    errors = []
    records_dir = repo_root / NUMERIC_DIR
    try:
        policies, eligible, expected = derive(repo_root)
    except (SourceValidationError, OSError, KeyError, TypeError, yaml.YAMLError) as exc:
        return [f"authoritative Stage-4 source validation failed: {exc}"]

    on_disk = {p.stem for p in records_dir.glob("*.yaml") if p.name != "COHORT_MANIFEST.yaml"}
    if on_disk != SLEEVE_IDS:
        errors.append(f"numeric_sizing population mismatch: {sorted(on_disk)}")
    records = {}
    for sid in sorted(on_disk):
        path = records_dir / f"{sid}.yaml"
        data = _load(path)
        records[sid] = data
        if not isinstance(data, dict):
            errors.append(f"{sid}: record must be a mapping")
            continue
        complete = _closed(data, RECORD_KEYS, sid, errors)
        _scan_key_names_recursive(data, sid, errors, allow_keys=frozenset({"provisional_target_pct","starting_baseline_pct","magnitude_pct","target_classification","numeric_target_status"}))
        if sid not in SLEEVE_IDS:
            errors.append(f"{sid}: unauthorized/orphan sleeve_id")
            continue
        if not complete:
            continue
        if data["schema_version"] != SCHEMA_VERSION or data["sleeve_id"] != sid:
            errors.append(f"{sid}: identity/schema mismatch")
        if data["governing_decisions"] != GOVERNING_DECISIONS:
            errors.append(f"{sid}: governing_decisions must be {GOVERNING_DECISIONS!r}")
        if data["sealed_at"] != SEALED_AT:
            errors.append(f"{sid}: sealed_at must be {SEALED_AT!r}")
        if data["drafting_session_or_shard_id"] != SHARD_ID:
            errors.append(f"{sid}: drafting_session_or_shard_id must be {SHARD_ID!r}")
        expected_entry = f"{NUMERIC_DIR}/COHORT_MANIFEST.yaml#{sid}"
        if data["cohort_manifest_entry"] != expected_entry:
            errors.append(f"{sid}: cohort_manifest_entry must be {expected_entry!r}")

        _closed(data["policy_adoption_reference"], REF_KEYS, f"{sid}.policy_adoption_reference", errors)
        policy_path, policy = policies[sid]
        pref = data["policy_adoption_reference"] if isinstance(data["policy_adoption_reference"], dict) else {}
        if pref.get("record_path") != str(policy_path.relative_to(repo_root)) or pref.get("referenced_content_sha256") != canonical_record_hash(policy):
            errors.append(f"{sid}: stale policy_adoption_reference")

        assigned = sid in eligible
        expected_status = STATUS_ASSIGNED if assigned else STATUS_BLOCKED
        if data["numeric_target_status"] != expected_status:
            errors.append(f"{sid}: numeric_target_status not independently live-derived")
        if assigned:
            exp = expected[sid]
            try:
                baseline = _two(data["starting_baseline_pct"])
                target = _two(data["provisional_target_pct"])
                if baseline != BASELINE:
                    errors.append(f"{sid}: wrong baseline")
                if target < Decimal("12.67") or target > Decimal("20.67"):
                    errors.append(f"{sid}: target outside governed generic range")
                if target != Decimal(exp["target"]):
                    errors.append(f"{sid}: target does not match live derivation")
            except ValueError as exc:
                errors.append(f"{sid}: {exc}")
            if data["applied_adjustments"] != exp["adjustments"]:
                errors.append(f"{sid}: adjustments do not match live R2/R3 derivation")
            if data["governing_rule_ids"] != exp["rules"]:
                errors.append(f"{sid}: governing_rule_ids mismatch")
            if not isinstance(data["applied_adjustments"], list):
                errors.append(f"{sid}: applied_adjustments must be a list")
            else:
                for i, adjustment in enumerate(data["applied_adjustments"]):
                    label = f"{sid}.applied_adjustments[{i}]"
                    if not _closed(adjustment, ADJ_KEYS, label, errors):
                        continue
                    if adjustment["governing_rule_id"] not in {"R2", "R3"}:
                        errors.append(f"{label}: retired/unknown rule")
                    if adjustment["direction"] not in {"up", "down"}:
                        errors.append(f"{label}: invalid direction")
                    try:
                        if _two(adjustment["magnitude_pct"]) != INCREMENT:
                            errors.append(f"{label}: wrong adjustment magnitude")
                    except ValueError as exc:
                        errors.append(f"{label}: {exc}")
                    refs = adjustment["evidence_ref"]
                    if not isinstance(refs, list) or not refs:
                        errors.append(f"{label}.evidence_ref must be a non-empty list")
                    else:
                        for j, ref in enumerate(refs):
                            _closed(ref, REF_KEYS, f"{label}.evidence_ref[{j}]", errors)
            if data["target_classification"] != TARGET_CLASS:
                errors.append(f"{sid}: target_classification must be {TARGET_CLASS!r}")
            if data["review_condition"] != REVIEW:
                errors.append(f"{sid}: review_condition must be the governed exact condition")
            for field in ("uncertainty_disclosure", "comparative_consistency_note"):
                if not isinstance(data[field], str) or not data[field].strip():
                    errors.append(f"{sid}: {field} must be non-empty")
                else:
                    _scan_numeric_free_text(data[field], f"{sid}.{field}", errors, repo_root)
            if data["blocking_rationale"] is not None:
                errors.append(f"{sid}: blocking_rationale must be null")
        else:
            nullable = ("provisional_target_pct","starting_baseline_pct","target_classification","review_condition","uncertainty_disclosure","comparative_consistency_note")
            for field in nullable:
                if data[field] is not None:
                    errors.append(f"{sid}: blocked field {field} must be null")
            if data["applied_adjustments"] != [] or data["governing_rule_ids"] != []:
                errors.append(f"{sid}: blocked adjustments/rules must be empty")
            if not isinstance(data["blocking_rationale"], str) or not data["blocking_rationale"].strip():
                errors.append(f"{sid}: blocking_rationale must be non-empty")
            else:
                _scan_numeric_free_text(data["blocking_rationale"], f"{sid}.blocking_rationale", errors, repo_root)
        if data["sizing_boundary_note"] != BOUNDARY:
            errors.append(f"{sid}: sizing_boundary_note must be the governed exact boundary")
        if data["record_status"] != "sealed":
            errors.append(f"{sid}: record_status must be 'sealed'")
        if canonical_record_hash(data) != data["content_sha256"]:
            errors.append(f"{sid}: content_sha256 mismatch")

    manifest_path = records_dir / "COHORT_MANIFEST.yaml"
    manifest = _load(manifest_path) if manifest_path.is_file() else {}
    if _closed(manifest, MANIFEST_KEYS, "manifest", errors):
        if manifest["schema_version"] != SCHEMA_VERSION:
            errors.append("manifest schema_version mismatch")
        if manifest["governing_decision"] != GOVERNING_DECISION:
            errors.append(f"manifest governing_decision must be {GOVERNING_DECISION!r}")
        cohort = manifest["cohort"]
        if not isinstance(cohort, list):
            errors.append("manifest cohort must be a list")
            cohort = []
        seen = []
        for i, row in enumerate(cohort):
            if not _closed(row, ROW_KEYS, f"manifest.cohort[{i}]", errors):
                continue
            sid = row["sleeve_id"]
            seen.append(sid)
            if row["schema_version"] != SCHEMA_VERSION or row["governing_decision"] != GOVERNING_DECISION or row["shard_id"] != SHARD_ID or row["sealed_at"] != SEALED_AT:
                errors.append(f"manifest row {sid}: governed constants mismatch")
            if sid in records and (row["record_path"] != f"{NUMERIC_DIR}/{sid}.yaml" or row["content_sha256"] != canonical_record_hash(records[sid])):
                errors.append(f"manifest row {sid}: path/hash mismatch")
        if set(seen) != SLEEVE_IDS or len(seen) != len(SLEEVE_IDS):
            errors.append("manifest population duplicate/missing/orphan")
        live_sum = sum(Decimal(expected[s]["target"]) for s in eligible)
        _validate_reconciliation(manifest["portfolio_reconciliation"], live_sum, errors)
    return errors


if __name__ == "__main__":
    root = Path(__file__).resolve().parent
    errs = validate(root)
    if errs:
        print("numeric_sizing_validator: FAILED")
        for error in errs:
            print("  -", error)
        raise SystemExit(1)
    print("numeric_sizing_validator: OK (6 record(s), authoritative Stage-4 and live R2/R3 rederived)")
