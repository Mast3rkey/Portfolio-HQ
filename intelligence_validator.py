"""
intelligence_validator.py — read-only schema validator for the Portfolio
Intelligence Engine's per-company YAML files (see
docs/PORTFOLIO_INTELLIGENCE_SPEC.md §9/14/16/20/21; authorized in bounded
scope by decision_log.yaml's PI-0002).

This module is a validator, not a data producer. It never opens a file in
write/append/update mode, never creates a directory, and never touches
holdings.yaml or targets.yaml. It has zero import relationship with
allocate.py or margin_state.py in either direction (see
test_intelligence_validator.py's isolation tests) and cannot influence any
allocator recommendation — nothing in this repository imports it.

Scope, exactly what's authorized: validate that a company YAML conforms to
the schema frozen in the spec's §9, enforce the §14/§20 rule that
`portfolio_role_ref` is a bare tier-label string (never a numeric weight),
and treat a missing or empty `intelligence/companies/` directory as valid,
zero-coverage, opt-in state (§16/§20) — never an error. Symbol resolution
(§15) and any cross-check against holdings.yaml/targets.yaml (§14's
"future validator" note) are explicitly deferred, not implemented here.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import yaml

# ── §9 schema: field names and their expected shapes ─────────────────────────

_STRING_FIELDS = ("sector", "industry")
_STRING_LIST_FIELDS = ("competitive_advantages",)

_RISK_REQUIRED_KEYS = {"risk", "severity", "identified", "status"}
_CATALYST_REQUIRED_KEYS = {"catalyst", "expected", "status"}
_REVIEW_LOG_REQUIRED_KEYS = {"date", "note"}
_SOURCE_REQUIRED_KEYS = {"note"}  # url is optional per §9; date is recommended but not enforced as required here — the spec does not mark it required

_REVIEW_REQUIRED_KEYS = {"cadence_days", "last_reviewed", "next_due"}

_PERCENT_MARKERS = ("%",)


@dataclass
class ValidationResult:
    """Report, not an agent — no method here writes anything or triggers
    any action. Mirrors margin_state.py's MarginStateResult contract."""
    valid: bool
    errors: list[str] = field(default_factory=list)
    source: str | None = None
    """Path/identifier of the file this result describes, or None for a
    result produced from an in-memory mapping via validate_company_data()."""


@dataclass
class DirectoryValidationResult:
    """Aggregate result for a directory scan. A missing or empty directory
    is represented here as valid=True, results=[] — not an error (§16/§20)."""
    valid: bool
    results: list[ValidationResult] = field(default_factory=list)

    @property
    def company_count(self) -> int:
        return len(self.results)


# ── field-level checks ────────────────────────────────────────────────────────

def _looks_like_weight_or_percentage(value: object) -> bool:
    """§14/§20: portfolio_role_ref must never carry a numeric weight. A bare
    tier label (e.g. "T1", "band") is fine; a number, a percentage string,
    a mapping, or a sequence is not."""
    if isinstance(value, (int, float)):
        return True
    if isinstance(value, str):
        stripped = value.strip()
        if any(marker in stripped for marker in _PERCENT_MARKERS):
            return True
        try:
            float(stripped)
        except ValueError:
            return False
        return True
    return False


def _validate_portfolio_role_ref(value: object, errors: list[str]) -> None:
    if not isinstance(value, str):
        errors.append(
            f"portfolio_role_ref must be a bare tier-label string, got "
            f"{type(value).__name__}: {value!r}"
        )
        return
    if not value.strip():
        errors.append("portfolio_role_ref must not be empty")
        return
    if _looks_like_weight_or_percentage(value):
        errors.append(
            f"portfolio_role_ref must be a tier/category label only, never a "
            f"numeric weight or percentage — got {value!r} (spec §14/§20)"
        )


def _validate_conviction(value: object, errors: list[str]) -> None:
    if value is None:
        return
    if not isinstance(value, dict):
        errors.append(f"conviction must be a mapping, got {type(value).__name__}")
        return
    rating = value.get("rating")
    rationale = value.get("rationale")
    if rating is not None and not rationale:
        errors.append(
            "conviction.rating is present without conviction.rationale — "
            "required together per spec §9/§12"
        )
    # rationale without rating: the frozen spec requires a rationale
    # "alongside any rating" (§9) but does not itself forbid a rationale
    # recorded with no rating yet set — validated as structurally fine,
    # not flagged as an error.
    if rationale is not None and not isinstance(rationale, str):
        errors.append(f"conviction.rationale must be a string, got {type(rationale).__name__}")


def _validate_list_of_mappings(
    value: object, field_name: str, required_keys: set[str], errors: list[str]
) -> None:
    if value is None:
        return
    if not isinstance(value, list):
        errors.append(f"{field_name} must be a list, got {type(value).__name__}")
        return
    for i, item in enumerate(value):
        if not isinstance(item, dict):
            errors.append(f"{field_name}[{i}] must be a mapping, got {type(item).__name__}")
            continue
        missing = required_keys - item.keys()
        if missing:
            errors.append(f"{field_name}[{i}] missing required key(s): {sorted(missing)}")


def _validate_review(value: object, errors: list[str]) -> None:
    if value is None:
        return
    if not isinstance(value, dict):
        errors.append(f"review must be a mapping, got {type(value).__name__}")
        return
    missing = _REVIEW_REQUIRED_KEYS - value.keys()
    if missing:
        errors.append(f"review missing required key(s): {sorted(missing)}")
    log = value.get("log")
    _validate_list_of_mappings(log, "review.log", _REVIEW_LOG_REQUIRED_KEYS, errors)


def _validate_sources(value: object, errors: list[str]) -> None:
    # §17: evidence stays attached to the claim it supports — sources is a
    # field on the same company document, not a separate structure. Only
    # structural shape is validated here.
    _validate_list_of_mappings(value, "sources", _SOURCE_REQUIRED_KEYS, errors)


# ── public API ─────────────────────────────────────────────────────────────

def validate_company_data(data: object, *, source: str | None = None) -> ValidationResult:
    """Validate an already-parsed company mapping against the §9 schema.
    Never touches the filesystem. `source` is carried through into the
    result purely for identification in aggregate reports."""
    errors: list[str] = []

    if not isinstance(data, dict):
        errors.append(f"root document must be a mapping, got {type(data).__name__}")
        return ValidationResult(valid=False, errors=errors, source=source)

    for field_name in _STRING_FIELDS:
        if field_name in data and data[field_name] is not None and not isinstance(data[field_name], str):
            errors.append(f"{field_name} must be a string, got {type(data[field_name]).__name__}")

    for field_name in _STRING_LIST_FIELDS:
        if field_name in data and data[field_name] is not None:
            v = data[field_name]
            if not isinstance(v, list) or not all(isinstance(x, str) for x in v):
                errors.append(f"{field_name} must be a list of strings")

    if "portfolio_role_ref" in data and data["portfolio_role_ref"] is not None:
        _validate_portfolio_role_ref(data["portfolio_role_ref"], errors)

    _validate_list_of_mappings(data.get("risks"), "risks", _RISK_REQUIRED_KEYS, errors)
    _validate_list_of_mappings(data.get("catalysts"), "catalysts", _CATALYST_REQUIRED_KEYS, errors)
    _validate_conviction(data.get("conviction"), errors)
    _validate_review(data.get("review"), errors)
    _validate_sources(data.get("sources"), errors)

    return ValidationResult(valid=not errors, errors=errors, source=source)


def validate_company_file(path: str | Path) -> ValidationResult:
    """Read and validate a single company YAML file. Read-only — opens the
    file in text mode for reading only, never write/append/update."""
    path = Path(path)
    source = str(path)
    try:
        text = path.read_text()
    except OSError as exc:
        return ValidationResult(valid=False, errors=[f"could not read file: {exc}"], source=source)

    try:
        data = yaml.safe_load(text)
    except yaml.YAMLError as exc:
        return ValidationResult(valid=False, errors=[f"invalid YAML: {exc}"], source=source)

    if data is None:
        return ValidationResult(valid=False, errors=["file is empty"], source=source)

    return validate_company_data(data, source=source)


def validate_directory(directory: str | Path) -> DirectoryValidationResult:
    """Scan `<directory>/*.yaml` and validate each file found. A missing or
    empty directory is valid, zero-coverage state (§16/§20) — not an error.
    One invalid file never stops the scan; every file is reported."""
    directory = Path(directory)

    if not directory.exists() or not directory.is_dir():
        return DirectoryValidationResult(valid=True, results=[])

    results = [
        validate_company_file(p)
        for p in sorted(directory.glob("*.yaml"))
    ]

    return DirectoryValidationResult(valid=all(r.valid for r in results), results=results)
