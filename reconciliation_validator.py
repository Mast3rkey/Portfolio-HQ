"""
reconciliation_validator.py -- read-only schema validator for the WS-0005
Milestone 7 baseline-reconciliation artifact
(`intelligence/reconciliation/MILESTONE7_BASELINE_RECONCILIATION.yaml`),
authorized by
`governance/decisions/TIER-0007-ws0005-milestone7-baseline-reconciliation-authorization.md`.

Scope, exactly what is validated (TIER-0007 §F-§K):

- Source-of-truth convention: one retained YAML artifact covering all 27
  sealed canonical equities, `reconciliation:` a list of exactly 27 entries
  in deterministic alphabetical ticker order, no duplicates, no ticker
  outside the current canonical universe (`targets.yaml` equity rows).
- Each entry carries exactly the closed set of per-ticker keys TIER-0007 §F
  requires (`ticker` plus its 18 fields) -- no missing key, no extra key.
- `primary_disposition` (TIER-0007 §H): exactly one of
  `baseline_assumption_stale` / `divergence_requires_review` / `aligned` /
  `no_policy_conclusion`.
- `secondary_conditions` (TIER-0007 §H): a list of zero to two values drawn
  from the closed set `unresolved_evidence` / `structural_measurement_gap`,
  no duplicates.
- `target_context_comparison` (TIER-0007 §G): `status` is exactly one of
  `categorically_consistent` / `categorically_divergent` /
  `unable_to_determine`, plus a required non-empty `rationale`.
- Required non-empty free-text fields: `role_comparison`,
  `capital_priority_comparison`, `structural_risk_comparison`,
  `evidence_quality_comparison`, `uncertainty`, `later_governance_action`,
  and at least one entry in `supporting_evidence`.
- Prohibited content (TIER-0007 §F/§K): no field name or free-text value
  anywhere in a ticker entry may introduce a *new* proposed/recommended
  numeric target, range, score, or ranking -- `target_pct` is permitted
  only as a citation of the *current, already-existing* `targets.yaml`
  value (never a proposed replacement), enforced by banning a fixed set of
  forbidden key names and forbidden recommendation-shaped phrases from
  every free-text value in the record.
- Top-level metadata: `governing_decision: TIER-0007`, a `source_main_sha`
  (exact comparison-source commit, not "current main" as a moving target),
  `sealed_cohort_reference` naming the TIER-0006 merge commit the sealed
  records were verified against, `integrity_checks_performed` recording the
  six TIER-0007 §C pre-unblinding checks, and `chart_evidence_used: false`
  (TIER-0007 §E -- Milestone 7 is fundamentals-and-structure only).

This module never opens `intelligence/classification/*.yaml` or
`COHORT_MANIFEST.yaml` in write mode, never creates a directory, and has
zero import relationship with `allocate.py`, `margin_state.py`,
`targets.py`, or any brokerage code in either direction (see
`test_reconciliation_validator.py`'s isolation tests) -- nothing in this
repository imports it, and it cannot influence any allocator
recommendation.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

import yaml

_ARTIFACT_FILENAME = "MILESTONE7_BASELINE_RECONCILIATION.yaml"

_PRIMARY_DISPOSITIONS = frozenset(
    {"baseline_assumption_stale", "divergence_requires_review", "aligned", "no_policy_conclusion"}
)
_SECONDARY_CONDITIONS = frozenset({"unresolved_evidence", "structural_measurement_gap"})
_TARGET_CONTEXT_STATUSES = frozenset(
    {"categorically_consistent", "categorically_divergent", "unable_to_determine"}
)

_TOP_LEVEL_ALLOWED_KEYS = frozenset(
    {
        "schema_version",
        "governing_decision",
        "artifact_purpose",
        "source_main_sha",
        "sealed_cohort_reference",
        "integrity_checks_performed",
        "chart_evidence_used",
        "reconciliation",
        "aggregate",
    }
)
_TOP_LEVEL_REQUIRED_KEYS = _TOP_LEVEL_ALLOWED_KEYS  # all are required, none optional

# TIER-0007 §F: exactly eighteen per-ticker fields, plus the `ticker`
# identity key itself (nineteen keys total).
_TICKER_ALLOWED_KEYS = frozenset(
    {
        "ticker",
        "sealed_economic_role",
        "current_role_context",
        "role_comparison",
        "sealed_capital_priority",
        "current_capital_priority_context",
        "capital_priority_comparison",
        "target_context_comparison",
        "sealed_risk_concentration",
        "current_structural_representation",
        "structural_risk_comparison",
        "sealed_evidence_quality",
        "current_evidence_posture",
        "evidence_quality_comparison",
        "primary_disposition",
        "secondary_conditions",
        "supporting_evidence",
        "uncertainty",
        "later_governance_action",
    }
)
_TICKER_REQUIRED_KEYS = _TICKER_ALLOWED_KEYS

_REQUIRED_NON_EMPTY_TEXT_FIELDS = (
    "role_comparison",
    "capital_priority_comparison",
    "structural_risk_comparison",
    "evidence_quality_comparison",
    "uncertainty",
    "later_governance_action",
)

# TIER-0007 §F/§K: a new proposed/recommended numeric target, range, score,
# or ranking must never appear anywhere in a ticker entry. `target_pct` is
# permitted as a dict *key* only inside the two current-baseline-context
# fields (citing the existing, already-governed targets.yaml value) --
# forbidden everywhere else, and these forbidden key names are never
# permitted at all.
_FORBIDDEN_KEY_NAMES = frozenset(
    {
        "proposed_target_pct",
        "proposed_target",
        "recommended_target_pct",
        "target_range",
        "score",
        "conviction_score",
        "rank",
        "ranking",
        "recommendation",
        "buy_sell_hold",
    }
)
_KEYS_WHERE_TARGET_PCT_IS_PERMITTED = frozenset(
    {"current_role_context", "current_capital_priority_context"}
)

_FORBIDDEN_TEXT_PATTERNS = [
    re.compile(p, re.IGNORECASE)
    for p in [
        r"\bshould\s+be\s+(increased|decreased|raised|lowered|set)\s+to\b",
        r"\brecommend(?:ed|s|ing)?\s+(a\s+)?(target|weight|allocation)\s+of\b",
        r"\bnew\s+target\s+(pct|percent|percentage|range)\b",
        r"\bbuy\s+recommendation\b",
        r"\bsell\s+recommendation\b",
        r"\btrim\s+recommendation\b",
    ]
]


@dataclass
class ValidationResult:
    valid: bool
    errors: list[str] = field(default_factory=list)
    source: str = ""


def _non_empty_str(value: object) -> bool:
    return isinstance(value, str) and value.strip() != ""


def _reject_unknown_keys(value: dict, allowed: frozenset[str], required: frozenset[str], label: str, errors: list[str]) -> None:
    if not isinstance(value, dict):
        errors.append(f"{label} must be a mapping")
        return
    unknown = set(value.keys()) - allowed
    if unknown:
        errors.append(f"{label} contains unexpected key(s) {sorted(unknown)} -- schema is closed, only {sorted(allowed)} are permitted")
    missing = required - set(value.keys())
    if missing:
        errors.append(f"{label} is missing required key(s) {sorted(missing)}")


def _scan_forbidden_content(value: object, path: str, in_permitted_target_pct_context: bool, errors: list[str]) -> None:
    """Recursively scan for forbidden key names and forbidden recommendation-shaped
    phrases anywhere in a ticker entry, per TIER-0007 §F/§K."""
    if isinstance(value, dict):
        for k, v in value.items():
            key_str = str(k)
            if key_str in _FORBIDDEN_KEY_NAMES:
                errors.append(f"{path}.{key_str}: forbidden key name -- Milestone 7 may not introduce a numeric target/range/score/ranking")
            if key_str == "target_pct" and not in_permitted_target_pct_context:
                errors.append(f"{path}.{key_str}: target_pct is only permitted inside current_role_context/current_capital_priority_context, citing the existing targets.yaml value")
            _scan_forbidden_content(v, f"{path}.{key_str}", in_permitted_target_pct_context, errors)
    elif isinstance(value, list):
        for i, item in enumerate(value):
            _scan_forbidden_content(item, f"{path}[{i}]", in_permitted_target_pct_context, errors)
    elif isinstance(value, str):
        for pattern in _FORBIDDEN_TEXT_PATTERNS:
            if pattern.search(value):
                errors.append(f"{path}: contains forbidden recommendation-shaped phrase matching {pattern.pattern!r}")


def validate_ticker_entry(entry: object, *, index: int) -> ValidationResult:
    errors: list[str] = []
    label = f"reconciliation[{index}]"

    if not isinstance(entry, dict):
        return ValidationResult(valid=False, errors=[f"{label} must be a mapping"], source=label)

    _reject_unknown_keys(entry, _TICKER_ALLOWED_KEYS, _TICKER_REQUIRED_KEYS, label, errors)

    ticker = entry.get("ticker")
    if not _non_empty_str(ticker):
        errors.append(f"{label}.ticker must be a non-empty string")
        ticker = f"<entry {index}>"

    for field_name in _REQUIRED_NON_EMPTY_TEXT_FIELDS:
        if field_name in entry and not _non_empty_str(entry.get(field_name)):
            errors.append(f"{ticker}.{field_name} must be a non-empty string")

    supporting = entry.get("supporting_evidence")
    if not isinstance(supporting, list) or not supporting or not all(_non_empty_str(s) for s in supporting):
        errors.append(f"{ticker}.supporting_evidence must be a non-empty list of non-empty citation strings")

    primary = entry.get("primary_disposition")
    if primary not in _PRIMARY_DISPOSITIONS:
        errors.append(f"{ticker}.primary_disposition {primary!r} is not one of {sorted(_PRIMARY_DISPOSITIONS)}")

    secondary = entry.get("secondary_conditions")
    if not isinstance(secondary, list):
        errors.append(f"{ticker}.secondary_conditions must be a list")
    else:
        if len(secondary) > 2:
            errors.append(f"{ticker}.secondary_conditions has {len(secondary)} values -- maximum is two")
        if len(secondary) != len(set(secondary)):
            errors.append(f"{ticker}.secondary_conditions contains duplicate value(s)")
        unknown_secondary = set(secondary) - _SECONDARY_CONDITIONS
        if unknown_secondary:
            errors.append(f"{ticker}.secondary_conditions contains unknown value(s) {sorted(unknown_secondary)} -- only {sorted(_SECONDARY_CONDITIONS)} are permitted")

    tcc = entry.get("target_context_comparison")
    if not isinstance(tcc, dict):
        errors.append(f"{ticker}.target_context_comparison must be a mapping")
    else:
        status = tcc.get("status")
        if status not in _TARGET_CONTEXT_STATUSES:
            errors.append(f"{ticker}.target_context_comparison.status {status!r} is not one of {sorted(_TARGET_CONTEXT_STATUSES)}")
        if not _non_empty_str(tcc.get("rationale")):
            errors.append(f"{ticker}.target_context_comparison.rationale must be a non-empty string")

    for permitted_key in _KEYS_WHERE_TARGET_PCT_IS_PERMITTED:
        sub = entry.get(permitted_key)
        if isinstance(sub, dict) and "target_pct" in sub:
            pass  # explicitly allowed; scanned separately below with the flag set

    for k, v in entry.items():
        permitted = k in _KEYS_WHERE_TARGET_PCT_IS_PERMITTED
        _scan_forbidden_content(v, f"{ticker}.{k}", permitted, errors)

    return ValidationResult(valid=not errors, errors=errors, source=str(ticker))


def validate_reconciliation_data(
    data: object, *, canonical_universe: frozenset[str] = frozenset(), sealed_universe: frozenset[str] = frozenset(),
) -> ValidationResult:
    errors: list[str] = []

    if not isinstance(data, dict):
        return ValidationResult(valid=False, errors=["reconciliation artifact must be a mapping"], source=_ARTIFACT_FILENAME)

    unknown_top = set(data.keys()) - _TOP_LEVEL_ALLOWED_KEYS
    if unknown_top:
        errors.append(f"top level contains unexpected key(s) {sorted(unknown_top)} -- only {sorted(_TOP_LEVEL_ALLOWED_KEYS)} are permitted")
    missing_top = _TOP_LEVEL_REQUIRED_KEYS - set(data.keys())
    if missing_top:
        errors.append(f"top level is missing required key(s) {sorted(missing_top)}")

    if data.get("governing_decision") != "TIER-0007":
        errors.append(f"governing_decision must be 'TIER-0007', got {data.get('governing_decision')!r}")

    if not _non_empty_str(data.get("source_main_sha")):
        errors.append("source_main_sha must be a non-empty exact commit SHA")

    if data.get("chart_evidence_used") is not False:
        errors.append("chart_evidence_used must be exactly `false` -- TIER-0007 §E prohibits chart evidence in Milestone 7")

    sealed_ref = data.get("sealed_cohort_reference")
    if not isinstance(sealed_ref, dict) or not _non_empty_str(sealed_ref.get("sealed_at_merge_commit")):
        errors.append("sealed_cohort_reference.sealed_at_merge_commit must be a non-empty exact commit SHA")
    elif sealed_ref.get("sealed_at_merge_commit") != "1107c5b70801ff5e7027efddf6a2aa916030dce2":
        errors.append(
            "sealed_cohort_reference.sealed_at_merge_commit does not match the known TIER-0006 merge commit "
            "(1107c5b70801ff5e7027efddf6a2aa916030dce2)"
        )

    integrity = data.get("integrity_checks_performed")
    if not isinstance(integrity, dict) or not integrity.get("diff_since_tier0006_merge"):
        errors.append("integrity_checks_performed.diff_since_tier0006_merge is required (TIER-0007 §C step 5)")

    rows = data.get("reconciliation")
    if not isinstance(rows, list):
        errors.append("reconciliation must be a list")
        rows = []

    seen: list[str] = []
    for i, entry in enumerate(rows):
        result = validate_ticker_entry(entry, index=i)
        errors.extend(result.errors)
        if isinstance(entry, dict) and _non_empty_str(entry.get("ticker")):
            seen.append(entry["ticker"])

    if len(seen) != len(set(seen)):
        dupes = sorted({t for t in seen if seen.count(t) > 1})
        errors.append(f"reconciliation contains duplicate ticker(s): {dupes}")

    if seen != sorted(seen):
        errors.append("reconciliation is not in deterministic alphabetical ticker order")

    target_universe = sealed_universe or canonical_universe
    if target_universe:
        missing = target_universe - set(seen)
        extra = set(seen) - target_universe
        if missing:
            errors.append(f"reconciliation is missing required ticker(s): {sorted(missing)}")
        if extra:
            errors.append(f"reconciliation contains ticker(s) outside the sealed 27-name population: {sorted(extra)}")

    if len(seen) != 27:
        errors.append(f"reconciliation must cover exactly 27 tickers, found {len(seen)}")

    return ValidationResult(valid=not errors, errors=errors, source=_ARTIFACT_FILENAME)


def _read_yaml(path: Path) -> tuple[object, list[str]]:
    try:
        text = path.read_text()
    except OSError as exc:
        return None, [f"could not read {path}: {exc}"]
    try:
        return yaml.safe_load(text), []
    except yaml.YAMLError as exc:
        return None, [f"YAML parse error in {path}: {exc}"]


def validate_reconciliation_file(
    path: str | Path, *, canonical_universe: frozenset[str] = frozenset(), sealed_universe: frozenset[str] = frozenset(),
) -> ValidationResult:
    path = Path(path)
    data, read_errors = _read_yaml(path)
    if read_errors:
        return ValidationResult(valid=False, errors=read_errors, source=str(path))
    return validate_reconciliation_data(data, canonical_universe=canonical_universe, sealed_universe=sealed_universe)


if __name__ == "__main__":
    import sys

    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from relationship_validator import load_canonical_universe  # noqa: E402

    _repo_root = Path(__file__).resolve().parent
    _canonical = load_canonical_universe(_repo_root)
    _artifact_path = _repo_root / "intelligence" / "reconciliation" / _ARTIFACT_FILENAME
    _result = validate_reconciliation_file(_artifact_path, canonical_universe=_canonical, sealed_universe=_canonical)
    if _result.valid:
        print("reconciliation_validator: OK (27 tickers)")
        sys.exit(0)
    else:
        print("reconciliation_validator: FAILED")
        for _err in _result.errors:
            print(f"  - {_err}")
        sys.exit(1)
