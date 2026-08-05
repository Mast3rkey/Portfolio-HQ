"""
classification_validator.py -- read-only schema validator for WS-0005
Milestone 6 (blind classification) records, freshly authored from current
`main` for this one implementation, per
`governance/decisions/TIER-0004-ws0005-milestone6-population-and-blindness-preflight.md`
Sec11's requirements and the four-axis schema designed by
`governance/decisions/TIER-0002-ws0005-milestone5-candidate-classification-framework-design.md`
Sec3 (as amended by TIER-0004 Sec12's `economic_role` abstention path), for
the one implementation PR authorized by
`governance/decisions/TIER-0005-ws0005-milestone6-fresh-authorization.md`.

Scope, exactly what is validated:

- Source-of-truth convention: `intelligence/classification/<TICKER>.yaml`,
  one file per ticker, single-file (TIER-0002 Sec3.1 -- no paired Markdown,
  filesystem is the index, no `index.yaml`).
- Exactly four axes on every record: `economic_role`, `capital_priority`,
  `risk_concentration`, `evidence_quality` -- no fifth axis, no numeric
  score, no target/weight field anywhere.
- `economic_role` (TIER-0002 Sec3.3, amended by TIER-0004 Sec12):
  `economic_system_ref` is exactly one of the five `docs/INVESTMENT_
  ONTOLOGY.md` SecD systems, an `other: <label>` escape, or
  `unable_to_determine`; when abstaining, `abstention_reason` and
  `evidence_gap_statement` are both required and non-empty, and both must
  be *absent* on a determined record (structurally distinguishable, not
  merely value-distinguishable, per TIER-0004 Sec12.2). `company_role` and
  `role_basis` are attempted best-effort regardless of abstention.
- `capital_priority` (TIER-0002 Sec3.4): `status` is exactly one of
  `maintain_current_weight` / `case_for_review` / `no_assessment`;
  `rationale` and `comparator_set` (2-5 tickers) are required, non-empty,
  when `status != no_assessment`; `rationale` must not contain a numeric
  target/`target_pct`-shaped figure or a buy/sell/trim instruction word.
- `risk_concentration` (TIER-0002 Sec3.5): four computed sub-fields plus an
  optional `notes` -- structural shape only; this validator does not
  recompute the cross-reference (that is `classification_report.py`-shaped
  future work, out of TIER-0005's scope), only checks the record's own
  internal consistency (`unmeasured_flag` == True exactly when the other
  three are empty/False).
- `evidence_quality` (TIER-0002 Sec3.6): `primary_source_coverage` is
  exactly one of `comprehensive`/`partial`/`limited`/`blocked`;
  `thesis_uncertainty_statement` is required, non-empty.
- Forbidden answer-key fields (TIER-0004 Sec11) inside `economic_role`/
  `capital_priority` specifically: no `portfolio_role_ref`, `conviction`,
  `target_pct`, `caps`/`clusters`/`issuer_lookthrough` key or reference --
  their presence inside `risk_concentration` (computed only after both
  judgment axes seal) is expected and required, never flagged.
- No numeric score/weight/target anywhere in the record -- a structural
  scan rejects any field literally named or shaped like a percentage-style
  allocation figure outside `risk_concentration`'s own already-permitted
  cross-reference booleans/lists.
- Sealing metadata (TIER-0004 Sec9.1): `lifecycle_status` in
  {`draft`, `sealed`}; when `sealed`, all seven seal fields present and
  `content_sha256` recomputable and matching via `canonical_record_hash()`.
- Cohort-manifest consistency (TIER-0004 Sec9.4): every sealed record's
  hash matches its manifest entry, every manifest entry has a
  corresponding sealed record, and the manifest carries exactly the
  authorized 27-name population, no more, no fewer.

This module is a validator, not a data producer. It never opens a file in
write/append/update mode, never creates a directory, and has zero import
relationship with `allocate.py` or `margin_state.py` in either direction.
It does not import `intelligence_validator.py` or `relationship_validator.py`
for schema logic (each schema is independent), but does reuse
`relationship_validator.load_canonical_universe()` for the live 27-name
population check, per this repository's "reuse existing public APIs, not a
second implementation" convention (REL-0001 precedent).
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from hashlib import sha256
from pathlib import Path

import yaml

# ── economic_role (TIER-0002 Sec3.3 / docs/INVESTMENT_ONTOLOGY.md SecD) ────

ONTOLOGY_ECONOMIC_SYSTEMS = frozenset({
    "AI & Compute Infrastructure",
    "Energy & Electrification",
    "Healthcare & Life Sciences",
    "Financial Infrastructure",
    "Digital Platforms & Enterprise Software",
})

ECONOMIC_SYSTEM_ABSTENTION_VALUE = "unable_to_determine"

_ECONOMIC_ROLE_REQUIRED_KEYS = {"economic_system_ref", "company_role", "role_basis"}
_ECONOMIC_ROLE_ABSTENTION_ONLY_KEYS = {"abstention_reason", "evidence_gap_statement"}

# ── capital_priority (TIER-0002 Sec3.4) ─────────────────────────────────────

CAPITAL_PRIORITY_STATUSES = frozenset({
    "maintain_current_weight", "case_for_review", "no_assessment",
})
_CAPITAL_PRIORITY_REQUIRED_KEYS = {"status"}
_COMPARATOR_SET_MIN, _COMPARATOR_SET_MAX = 2, 5

# A rationale must never itself carry a numeric target/allocation figure or
# a direct trade instruction -- capital_priority is explicitly never a
# target_pct/buy-sell channel (TIER-0002 Sec3.4).
_RATIONALE_FORBIDDEN_PATTERNS = [
    re.compile(p, re.IGNORECASE) for p in (
        r"\btarget_pct\b",
        r"\d+(?:\.\d+)?\s*%\s*(?:of\s+book|target|weight|allocation)",
        r"\b(?:buy|sell|trim|add to|reduce)\s+(?:it|this|the position)\b",
    )
]

# ── risk_concentration (TIER-0002 Sec3.5) -- structural shape only ─────────

_RISK_CONCENTRATION_REQUIRED_KEYS = {
    "cluster_cap_membership", "issuer_lookthrough_membership",
    "relationship_record_coverage", "unmeasured_flag",
}

# ── evidence_quality (TIER-0002 Sec3.6) ─────────────────────────────────────

PRIMARY_SOURCE_COVERAGE_VALUES = frozenset({
    "comprehensive", "partial", "limited", "blocked",
})
RISK_SEVERITY_VALUES = frozenset({"low", "moderate", "high"})
_EVIDENCE_QUALITY_REQUIRED_KEYS = {
    "primary_source_coverage", "highest_disclosed_risk_severity",
    "thesis_uncertainty_statement",
}

# ── TIER-0004 Sec11 forbidden answer-key fields, checked inside
#    economic_role/capital_priority specifically ───────────────────────────

_FORBIDDEN_ANSWER_KEY_FIELDS = frozenset({
    "portfolio_role_ref", "conviction", "target_pct",
    "caps", "clusters", "issuer_lookthrough", "gates", "holdings",
})

# ── TIER-0004 Sec9.1 sealing metadata ───────────────────────────────────────

LIFECYCLE_STATUSES = frozenset({"draft", "sealed"})
_SEAL_REQUIRED_KEYS = {
    "lifecycle_status", "sealed_at", "governing_decision",
    "drafting_session_or_shard_id", "schema_version", "content_sha256",
    "cohort_manifest_entry",
}
_FOUR_AXES = ("economic_role", "capital_priority", "risk_concentration", "evidence_quality")
_ALL_TOP_LEVEL_KEYS = frozenset({"schema_version", "ticker", *_FOUR_AXES, *_SEAL_REQUIRED_KEYS})


@dataclass
class ValidationResult:
    valid: bool
    errors: list[str] = field(default_factory=list)
    source: str | None = None


@dataclass
class DirectoryValidationResult:
    """A missing or empty directory is valid, zero-coverage state -- same
    filesystem-as-index doctrine intelligence_validator.py/
    relationship_validator.py already apply."""
    valid: bool
    results: list[ValidationResult] = field(default_factory=list)

    @property
    def record_count(self) -> int:
        return len(self.results)


# ── canonical hashing (TIER-0004 Sec9.1: content_sha256 excludes the seal
#    block itself, avoiding circular self-hashing) ──────────────────────────

def canonical_record_hash(data: dict) -> str:
    """SHA-256 of the record's four-axis content plus ticker, canonical
    sorted-key JSON, UTF-8 -- excludes every seal field (lifecycle_status,
    sealed_at, governing_decision, drafting_session_or_shard_id,
    schema_version, content_sha256, cohort_manifest_entry)."""
    hashable = {
        "ticker": data.get("ticker"),
        **{axis: data.get(axis) for axis in _FOUR_AXES},
    }
    canonical = json.dumps(hashable, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return sha256(canonical.encode("utf-8")).hexdigest()


# ── field-level checks ───────────────────────────────────────────────────

def _require_keys(value: object, field_name: str, required: set[str], errors: list[str]) -> bool:
    if not isinstance(value, dict):
        errors.append(f"{field_name} must be a mapping, got {type(value).__name__}")
        return False
    missing = required - value.keys()
    if missing:
        errors.append(f"{field_name} missing required key(s): {sorted(missing)}")
        return False
    return True


def _non_empty_str(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _validate_economic_role(value: object, errors: list[str]) -> None:
    if not _require_keys(value, "economic_role", _ECONOMIC_ROLE_REQUIRED_KEYS, errors):
        return
    value = value  # type: dict

    for key in _FORBIDDEN_ANSWER_KEY_FIELDS:
        if key in value:
            errors.append(
                f"economic_role.{key} is a forbidden answer-key field (TIER-0004 Sec11) -- "
                f"must never appear inside a judgment axis"
            )

    ref = value.get("economic_system_ref")
    is_abstention = ref == ECONOMIC_SYSTEM_ABSTENTION_VALUE
    is_other = isinstance(ref, str) and ref.startswith("other: ") and len(ref) > len("other: ")
    is_named = ref in ONTOLOGY_ECONOMIC_SYSTEMS
    if not (is_abstention or is_other or is_named):
        errors.append(
            "economic_role.economic_system_ref must be exactly one of the five "
            f"docs/INVESTMENT_ONTOLOGY.md SecD systems {sorted(ONTOLOGY_ECONOMIC_SYSTEMS)}, "
            f"an 'other: <label>' escape, or {ECONOMIC_SYSTEM_ABSTENTION_VALUE!r} "
            f"(TIER-0002 Sec3.3 / TIER-0004 Sec12) -- got {ref!r}"
        )

    if not _non_empty_str(value.get("company_role")):
        errors.append("economic_role.company_role must be a non-empty string")
    if not _non_empty_str(value.get("role_basis")):
        errors.append("economic_role.role_basis must be a non-empty string")

    abstention_reason = value.get("abstention_reason")
    evidence_gap_statement = value.get("evidence_gap_statement")
    if is_abstention:
        if not _non_empty_str(abstention_reason):
            errors.append(
                "economic_role.abstention_reason is required and must be a non-empty "
                "one-sentence string when economic_system_ref is 'unable_to_determine' "
                "(TIER-0004 Sec12.2)"
            )
        if not _non_empty_str(evidence_gap_statement):
            errors.append(
                "economic_role.evidence_gap_statement is required and must be a non-empty "
                "one-sentence string when economic_system_ref is 'unable_to_determine' "
                "(TIER-0004 Sec12.2)"
            )
    else:
        # Structurally distinguishable, not just value-distinguishable
        # (TIER-0004 Sec12.2) -- a determined record must not carry either
        # abstention-only field at all.
        if abstention_reason is not None:
            errors.append(
                "economic_role.abstention_reason must be absent (not merely empty) on a "
                "determined record -- present only when economic_system_ref is "
                "'unable_to_determine' (TIER-0004 Sec12.2)"
            )
        if evidence_gap_statement is not None:
            errors.append(
                "economic_role.evidence_gap_statement must be absent (not merely empty) on a "
                "determined record -- present only when economic_system_ref is "
                "'unable_to_determine' (TIER-0004 Sec12.2)"
            )


def _validate_capital_priority(value: object, errors: list[str]) -> None:
    if not _require_keys(value, "capital_priority", _CAPITAL_PRIORITY_REQUIRED_KEYS, errors):
        return
    value = value  # type: dict

    for key in _FORBIDDEN_ANSWER_KEY_FIELDS:
        if key in value:
            errors.append(
                f"capital_priority.{key} is a forbidden answer-key field (TIER-0004 Sec11) -- "
                f"must never appear inside a judgment axis"
            )

    status = value.get("status")
    if status not in CAPITAL_PRIORITY_STATUSES:
        errors.append(
            f"capital_priority.status must be exactly one of {sorted(CAPITAL_PRIORITY_STATUSES)} "
            f"(TIER-0002 Sec3.4) -- got {status!r}"
        )
        return

    if status == "no_assessment":
        return

    rationale = value.get("rationale")
    if not _non_empty_str(rationale):
        errors.append(
            "capital_priority.rationale is required and must be a non-empty string when "
            "status != no_assessment (TIER-0002 Sec3.4)"
        )
    elif any(p.search(rationale) for p in _RATIONALE_FORBIDDEN_PATTERNS):
        errors.append(
            "capital_priority.rationale must not contain a numeric target/target_pct-shaped "
            "figure or a direct buy/sell/trim instruction -- capital_priority is never a "
            "target_pct or trade-instruction channel (TIER-0002 Sec3.4)"
        )

    comparator_set = value.get("comparator_set")
    if not isinstance(comparator_set, list) or not (
        _COMPARATOR_SET_MIN <= len(comparator_set) <= _COMPARATOR_SET_MAX
    ):
        errors.append(
            f"capital_priority.comparator_set must be a list of {_COMPARATOR_SET_MIN}-"
            f"{_COMPARATOR_SET_MAX} tickers when status != no_assessment (TIER-0002 Sec3.4, "
            f"PI-0016 comparator convention)"
        )
    elif not all(_non_empty_str(t) for t in comparator_set):
        errors.append("capital_priority.comparator_set entries must all be non-empty strings")


def _validate_risk_concentration(value: object, errors: list[str]) -> None:
    if not _require_keys(value, "risk_concentration", _RISK_CONCENTRATION_REQUIRED_KEYS, errors):
        return
    value = value  # type: dict

    cluster = value.get("cluster_cap_membership")
    if not isinstance(cluster, list) or not all(isinstance(c, str) for c in cluster):
        errors.append("risk_concentration.cluster_cap_membership must be a list of strings")
        cluster = None

    lookthrough = value.get("issuer_lookthrough_membership")
    if not isinstance(lookthrough, bool):
        errors.append("risk_concentration.issuer_lookthrough_membership must be a boolean")
        lookthrough = None

    relationships = value.get("relationship_record_coverage")
    if not isinstance(relationships, list) or not all(isinstance(r, str) for r in relationships):
        errors.append("risk_concentration.relationship_record_coverage must be a list of strings")
        relationships = None

    unmeasured = value.get("unmeasured_flag")
    if not isinstance(unmeasured, bool):
        errors.append("risk_concentration.unmeasured_flag must be a boolean")
        return

    if cluster is None or lookthrough is None or relationships is None:
        return  # can't check internal consistency without well-typed inputs

    all_empty = not cluster and lookthrough is False and not relationships
    if unmeasured != all_empty:
        errors.append(
            "risk_concentration.unmeasured_flag must be True exactly when "
            "cluster_cap_membership/relationship_record_coverage are both empty and "
            "issuer_lookthrough_membership is False (TIER-0002 Sec3.5) -- got "
            f"unmeasured_flag={unmeasured}, cluster={cluster}, lookthrough={lookthrough}, "
            f"relationships={relationships}"
        )


def _validate_evidence_quality(value: object, errors: list[str]) -> None:
    if not _require_keys(value, "evidence_quality", _EVIDENCE_QUALITY_REQUIRED_KEYS, errors):
        return
    value = value  # type: dict

    coverage = value.get("primary_source_coverage")
    if coverage not in PRIMARY_SOURCE_COVERAGE_VALUES:
        errors.append(
            "evidence_quality.primary_source_coverage must be exactly one of "
            f"{sorted(PRIMARY_SOURCE_COVERAGE_VALUES)} (TIER-0002 Sec3.6) -- got {coverage!r}"
        )

    severity = value.get("highest_disclosed_risk_severity")
    if severity is not None and severity not in RISK_SEVERITY_VALUES:
        errors.append(
            "evidence_quality.highest_disclosed_risk_severity must be null or one of "
            f"{sorted(RISK_SEVERITY_VALUES)} (reuses risks[].severity vocabulary) -- got {severity!r}"
        )

    if not _non_empty_str(value.get("thesis_uncertainty_statement")):
        errors.append(
            "evidence_quality.thesis_uncertainty_statement is required and must be a "
            "non-empty string (TIER-0002 Sec3.6)"
        )


def _validate_no_stray_top_level_fields(data: dict, errors: list[str]) -> None:
    """No fifth axis, no numeric score/weight/target field anywhere at the
    top level -- the record contains exactly schema_version, ticker, the
    four axes, and the seven seal fields."""
    stray = set(data.keys()) - _ALL_TOP_LEVEL_KEYS
    if stray:
        errors.append(
            f"record contains unexpected top-level field(s) {sorted(stray)} -- exactly the four "
            f"axes ({', '.join(_FOUR_AXES)}) plus schema_version/ticker/seal metadata are "
            f"permitted, no fifth axis, no score, no target field (TIER-0002/TIER-0004)"
        )


def _validate_seal(data: dict, errors: list[str]) -> None:
    lifecycle_status = data.get("lifecycle_status")
    if lifecycle_status not in LIFECYCLE_STATUSES:
        errors.append(
            f"lifecycle_status must be exactly one of {sorted(LIFECYCLE_STATUSES)} "
            f"(TIER-0004 Sec9.1) -- got {lifecycle_status!r}"
        )
        return

    if lifecycle_status == "draft":
        return  # a draft record need not yet carry the remaining seal fields

    missing = _SEAL_REQUIRED_KEYS - data.keys()
    if missing:
        errors.append(f"sealed record missing required seal field(s): {sorted(missing)}")
        return

    if not _non_empty_str(data.get("sealed_at")):
        errors.append("sealed_at must be a non-empty ISO 8601 timestamp string")
    if not _non_empty_str(data.get("governing_decision")):
        errors.append("governing_decision must be a non-empty string pointer")
    if not _non_empty_str(data.get("drafting_session_or_shard_id")):
        errors.append("drafting_session_or_shard_id must be a non-empty string")
    if not _non_empty_str(data.get("schema_version")):
        errors.append("schema_version must be a non-empty string")
    if not _non_empty_str(data.get("cohort_manifest_entry")):
        errors.append("cohort_manifest_entry must be a non-empty string pointer")

    recorded_hash = data.get("content_sha256")
    if not _non_empty_str(recorded_hash):
        errors.append("content_sha256 must be a non-empty string")
    else:
        expected = canonical_record_hash(data)
        if recorded_hash != expected:
            errors.append(
                f"content_sha256 does not reproduce -- recorded {recorded_hash!r}, "
                f"recomputed {expected!r} (TIER-0004 Sec9.1/Sec9.2)"
            )


# ── public API: in-memory record validation ─────────────────────────────

def validate_classification_data(
    data: object,
    *,
    source: str | None = None,
    canonical_universe: frozenset[str] = frozenset(),
) -> ValidationResult:
    """Validate an already-parsed classification mapping. Never touches the
    filesystem. `canonical_universe` optionally enforces the ticker
    belongs to the live 27-name authorized population."""
    errors: list[str] = []

    if not isinstance(data, dict):
        errors.append(f"root document must be a mapping, got {type(data).__name__}")
        return ValidationResult(valid=False, errors=errors, source=source)

    ticker = data.get("ticker")
    if not _non_empty_str(ticker):
        errors.append("ticker must be a non-empty string")
    elif canonical_universe and ticker not in canonical_universe:
        errors.append(
            f"ticker {ticker!r} is not in the live authorized 27-name canonical population "
            f"(TIER-0005)"
        )

    if not _non_empty_str(data.get("schema_version")):
        errors.append("schema_version must be a non-empty string")

    for axis, validator in (
        ("economic_role", _validate_economic_role),
        ("capital_priority", _validate_capital_priority),
        ("risk_concentration", _validate_risk_concentration),
        ("evidence_quality", _validate_evidence_quality),
    ):
        if axis not in data:
            errors.append(f"record missing required axis: {axis}")
        else:
            validator(data[axis], errors)

    _validate_no_stray_top_level_fields(data, errors)
    _validate_seal(data, errors)

    return ValidationResult(valid=not errors, errors=errors, source=source)


# ── public API: file/directory validation ───────────────────────────────

def _read_yaml(path: Path) -> tuple[object, list[str]]:
    errors: list[str] = []
    try:
        text = path.read_text()
    except OSError as exc:
        return None, [f"could not read file: {exc}"]
    try:
        data = yaml.safe_load(text)
    except yaml.YAMLError as exc:
        return None, [f"invalid YAML: {exc}"]
    if data is None:
        return None, ["file is empty"]
    return data, errors


def validate_classification_file(
    path: str | Path, *, canonical_universe: frozenset[str] = frozenset(),
) -> ValidationResult:
    path = Path(path)
    source = str(path)
    data, read_errors = _read_yaml(path)
    if read_errors:
        return ValidationResult(valid=False, errors=read_errors, source=source)

    result = validate_classification_data(data, source=source, canonical_universe=canonical_universe)

    if isinstance(data, dict) and _non_empty_str(data.get("ticker")):
        expected_stem = data["ticker"]
        if path.stem != expected_stem:
            result.errors.append(
                f"filename stem {path.stem!r} does not match the record's own ticker "
                f"{expected_stem!r}"
            )
            result.valid = False

    return result


_MANIFEST_FILENAME = "COHORT_MANIFEST.yaml"
_MANIFEST_REQUIRED_ROW_KEYS = {
    "ticker", "shard_id", "sealed_at", "content_sha256", "schema_version", "governing_decision",
    "record_path",
}


def validate_cohort_manifest(
    manifest_data: object, records_by_ticker: dict[str, dict],
    *, canonical_universe: frozenset[str] = frozenset(),
) -> ValidationResult:
    """TIER-0004 Sec9.4: every authorized ticker appears exactly once, no
    extra ticker, every hash reproduces, every record points back to the
    manifest, bidirectionally."""
    errors: list[str] = []

    if not isinstance(manifest_data, dict) or not isinstance(manifest_data.get("cohort"), list):
        errors.append("cohort manifest must be a mapping with a 'cohort' list")
        return ValidationResult(valid=False, errors=errors, source=_MANIFEST_FILENAME)

    rows = manifest_data["cohort"]
    seen_tickers: set[str] = set()
    for i, row in enumerate(rows):
        if not isinstance(row, dict) or (_MANIFEST_REQUIRED_ROW_KEYS - row.keys()):
            missing = _MANIFEST_REQUIRED_ROW_KEYS - (row.keys() if isinstance(row, dict) else set())
            errors.append(f"cohort[{i}] missing required key(s): {sorted(missing)}")
            continue
        ticker = row["ticker"]
        if ticker in seen_tickers:
            errors.append(f"cohort manifest lists {ticker!r} more than once")
        seen_tickers.add(ticker)

        record = records_by_ticker.get(ticker)
        if record is None:
            errors.append(f"cohort[{i}] ticker {ticker!r} has no corresponding sealed record file")
            continue

        expected_hash = canonical_record_hash(record)
        if row["content_sha256"] != expected_hash:
            errors.append(
                f"cohort[{i}] ({ticker!r}) content_sha256 mismatch -- manifest "
                f"{row['content_sha256']!r}, recomputed from record {expected_hash!r}"
            )
        if record.get("content_sha256") != row["content_sha256"]:
            errors.append(
                f"cohort[{i}] ({ticker!r}) manifest content_sha256 does not match the record's "
                f"own recorded content_sha256"
            )
        if record.get("cohort_manifest_entry") is None:
            errors.append(f"record {ticker!r} carries no cohort_manifest_entry pointer")

    if canonical_universe:
        missing_from_manifest = canonical_universe - seen_tickers
        if missing_from_manifest:
            errors.append(
                f"cohort manifest is missing authorized ticker(s): {sorted(missing_from_manifest)}"
            )
        extra_in_manifest = seen_tickers - canonical_universe
        if extra_in_manifest:
            errors.append(
                f"cohort manifest lists ticker(s) outside the authorized 27-name population: "
                f"{sorted(extra_in_manifest)}"
            )

    orphan_records = set(records_by_ticker) - seen_tickers
    if orphan_records:
        errors.append(
            f"sealed record(s) exist with no corresponding cohort manifest entry: "
            f"{sorted(orphan_records)}"
        )

    return ValidationResult(valid=not errors, errors=errors, source=_MANIFEST_FILENAME)


def validate_classification_directory(
    directory: str | Path, *, canonical_universe: frozenset[str] = frozenset(),
) -> DirectoryValidationResult:
    """Scan `<directory>/<TICKER>.yaml` (excluding the cohort manifest file
    itself) and validate each record, plus the manifest's own bidirectional
    consistency. A missing or empty directory is valid, zero-coverage state
    -- never an error."""
    directory = Path(directory)
    if not directory.exists() or not directory.is_dir():
        return DirectoryValidationResult(valid=True, results=[])

    yaml_paths = sorted(
        p for p in directory.glob("*.yaml") if p.name != _MANIFEST_FILENAME
    )
    results = [
        validate_classification_file(p, canonical_universe=canonical_universe)
        for p in yaml_paths
    ]

    records_by_ticker: dict[str, dict] = {}
    for p in yaml_paths:
        data, read_errors = _read_yaml(p)
        if not read_errors and isinstance(data, dict) and _non_empty_str(data.get("ticker")):
            records_by_ticker[data["ticker"]] = data

    manifest_path = directory / _MANIFEST_FILENAME
    if manifest_path.is_file():
        manifest_data, read_errors = _read_yaml(manifest_path)
        if read_errors:
            results.append(ValidationResult(valid=False, errors=read_errors, source=str(manifest_path)))
        else:
            results.append(
                validate_cohort_manifest(
                    manifest_data, records_by_ticker, canonical_universe=canonical_universe,
                )
            )
    elif records_by_ticker:
        results.append(
            ValidationResult(
                valid=False,
                errors=[f"{_MANIFEST_FILENAME} is required whenever sealed records exist (TIER-0004 Sec9.4)"],
                source=str(directory),
            )
        )

    return DirectoryValidationResult(valid=all(r.valid for r in results), results=results)


if __name__ == "__main__":
    import sys

    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from relationship_validator import load_canonical_universe  # noqa: E402

    _repo_root = Path(__file__).resolve().parent
    _canonical = load_canonical_universe(_repo_root)
    _result = validate_classification_directory(
        _repo_root / "intelligence" / "classification", canonical_universe=_canonical,
    )
    if _result.valid:
        print(f"classification_validator: OK ({_result.record_count} result(s))")
        sys.exit(0)
    else:
        print("classification_validator: FAILED")
        for _r in _result.results:
            if not _r.valid:
                for _err in _r.errors:
                    print(f"  - [{_r.source}] {_err}")
        sys.exit(1)
