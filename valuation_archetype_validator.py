"""valuation_archetype_validator.py -- closed-schema validator for
intelligence/valuation_archetype/<TICKER>.yaml, authorized by
governance/decisions/VALUATION-0003-equity-valuation-archetype-assignment-authorization.md.

Freshly authored (VALUATION-0003 SS I) -- zero import coupling with
allocate.py/margin_state.py, and deliberately zero import coupling with
valuation_archetype_sanitizer.py either: this module's prohibited-language
scan is its own, independently-derived implementation (not a second call
into the sanitizer's own scan), matching this repository's own established
lesson (TIER-0004's corrected design) that a validator sharing its scanning
mechanism with the sanitizer that produced the content is not a genuine
independent check.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from hashlib import sha256
from pathlib import Path

import yaml

SCHEMA_VERSION = "1.0"

_PRIMARY_VALUES = frozenset({"A", "B", "C", "D", "E", "F", "G", "unable_to_determine_archetype"})
_SECONDARY_VALUES = frozenset({"A", "B", "C", "D", "E", "F", "G"})
_ABSTENTION = "unable_to_determine_archetype"

_TOP_LEVEL_REQUIRED = frozenset({
    "schema_version", "ticker", "primary_archetype", "secondary_archetype",
    "rationale", "evidence_quality", "disclosed_evidence_conflicts",
    "evidence_gap_statement", "portfolio_context", "lifecycle_status",
    "sealed_at", "governing_decision", "drafting_session_or_shard_id",
    "cohort_manifest_entry", "content_sha256",
})
# closed -- no other top-level key permitted (VALUATION-0003 SS I: "rejects extra keys at every level")
_TOP_LEVEL_ALL = _TOP_LEVEL_REQUIRED

_EVIDENCE_QUALITY_KEYS = frozenset({"primary_source_coverage", "uncertainty_statement"})
_PRIMARY_SOURCE_COVERAGE_VALUES = frozenset({"comprehensive", "partial", "limited", "blocked"})

_PORTFOLIO_CONTEXT_KEYS = frozenset({"gate_exists", "next_gate_references_valuation", "disclosure_note"})

_SEAL_FIELDS = ("sealed_at", "governing_decision", "drafting_session_or_shard_id",
                "content_sha256", "cohort_manifest_entry")

_LIFECYCLE_VALUES = frozenset({"sealed"})


# ---------------------------------------------------------------------------
# Canonical hashing -- excludes only the seal fields, mirrors
# classification_validator.py / etf_classification_validator.py /
# crypto_classification_validator.py's identical convention.
# ---------------------------------------------------------------------------

def canonical_record_hash(data: dict) -> str:
    hashable = {k: v for k, v in data.items() if k not in _SEAL_FIELDS}
    canonical = json.dumps(hashable, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return sha256(canonical.encode("utf-8")).hexdigest()


# ---------------------------------------------------------------------------
# Independent prohibited-field / prohibited-language scan (VALUATION-0003 SS I)
# -- an entirely separate implementation from valuation_archetype_sanitizer.py.
# ---------------------------------------------------------------------------

_FORBIDDEN_TEXT_PATTERNS = [
    re.compile(p, re.IGNORECASE)
    for p in [
        r"\bconviction\b",
        r"portfolio_role_ref",
        r"target_pct",
        r"targets\.yaml",
        r"holdings\.yaml",
        r"gates\.yaml",
        r"\bnext_gate\b",
        r"\ballow_add\b",
        r"issuer_lookthrough\.yaml",
        r"%\s*of\s+(the\s+)?book",
        r"%\s*of\s+portfolio",
        r"target\s+weight",
        r"destination\s+weight",
        r"primary_disposition",
        r"case_for_review",
        r"maintain_current_weight",
        r"divergence_requires_review",
        r"baseline_assumption_stale",
        r"structural_measurement_gap",
        r"relationship_measurement_required",
    ]
]

_GATE_LEGITIMATE_USE_PATTERNS = [
    re.compile(p, re.IGNORECASE)
    for p in [
        r"technological gate",
        r"gate-all-around",
        r"customer-qualification gate",
        r"qualification gate",
        r"stop-before-drafting gate",
        r"source-readiness gate",
        r"\bci gate\b",
    ]
]

_CHART_DOMAIN_PATTERNS = [
    re.compile(p, re.IGNORECASE)
    for p in [
        r"support\s+level", r"resistance\s+level", r"breakout", r"trend\s*line",
        r"moving\s+average", r"\brsi\b", r"\bmacd\b", r"candlestick",
        r"chart\s+pattern", r"technical\s+analysis", r"oversold", r"overbought",
        r"fibonacci", r"volume\s+profile", r"price\s+target",
    ]
]

_DIRECTIVE_WORDS = ("buy", "sell", "add", "hold", "trim", "exit", "wait", "stage")
_DIRECTIVE_PATTERNS = [re.compile(rf"\b{w}\b", re.IGNORECASE) for w in _DIRECTIVE_WORDS]

# "stage" is also legitimate taxonomy vocabulary as a hyphenated compound
# (archetype E is literally "Early-stage / binary-outcome"; "pipeline-stage",
# "venture-stage" are ordinary business-economics usage) -- whitelisted the
# same way the sanitizer whitelists legitimate technical uses of "gate".
_STAGE_LEGITIMATE_USE_PATTERN = re.compile(r"[a-z]+-stage", re.IGNORECASE)

_ARCHETYPE_LETTER_PATTERN = re.compile(r"^[A-G]$")


def _gate_word_leak(text: str) -> bool:
    scrubbed = text
    for pat in _GATE_LEGITIMATE_USE_PATTERNS:
        scrubbed = pat.sub("", scrubbed)
    return bool(re.search(r"\bgates?\b", scrubbed, re.IGNORECASE))


def independent_prohibited_scan(text: str) -> list[str]:
    """Standalone scan (never reused by the sanitizer, never reusing the
    sanitizer's own scan) for prohibited-field/prohibited-language,
    chart-domain, and directive-language content in a free-text field."""
    findings: list[str] = []
    for pat in _FORBIDDEN_TEXT_PATTERNS:
        if pat.search(text):
            findings.append(f"forbidden-pattern:{pat.pattern}")
    for pat in _CHART_DOMAIN_PATTERNS:
        if pat.search(text):
            findings.append(f"chart-domain:{pat.pattern}")
    stage_scrubbed = _STAGE_LEGITIMATE_USE_PATTERN.sub("", text)
    for pat in _DIRECTIVE_PATTERNS:
        haystack = stage_scrubbed if pat.pattern == r"\bstage\b" else text
        if pat.search(haystack):
            findings.append(f"directive-word:{pat.pattern}")
    if _gate_word_leak(text):
        findings.append("bare-gate-word")
    return findings


def _scan_free_text(value: object, field_name: str, errors: list[str]) -> None:
    if value is None:
        return
    texts: list[str]
    if isinstance(value, str):
        texts = [value]
    elif isinstance(value, list):
        texts = [v for v in value if isinstance(v, str)]
    else:
        return
    for text in texts:
        for finding in independent_prohibited_scan(text):
            errors.append(f"{field_name} contains prohibited content ({finding})")


# ---------------------------------------------------------------------------
# Sub-object validators
# ---------------------------------------------------------------------------

def _reject_unknown_keys(value: dict, field_name: str, allowed: frozenset[str], errors: list[str]) -> None:
    extra = set(value.keys()) - allowed
    if extra:
        errors.append(f"{field_name} has unrecognized key(s): {sorted(extra)}")


def _non_empty_str(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _validate_evidence_quality(value: object, errors: list[str]) -> None:
    if not isinstance(value, dict):
        errors.append("evidence_quality must be a mapping")
        return
    missing = _EVIDENCE_QUALITY_KEYS - value.keys()
    if missing:
        errors.append(f"evidence_quality missing key(s): {sorted(missing)}")
        return
    _reject_unknown_keys(value, "evidence_quality", _EVIDENCE_QUALITY_KEYS, errors)
    cov = value.get("primary_source_coverage")
    if cov not in _PRIMARY_SOURCE_COVERAGE_VALUES:
        errors.append(f"evidence_quality.primary_source_coverage invalid: {cov!r}")
    if not _non_empty_str(value.get("uncertainty_statement")):
        errors.append("evidence_quality.uncertainty_statement must be a non-empty string")
    else:
        _scan_free_text(value["uncertainty_statement"], "evidence_quality.uncertainty_statement", errors)


def _validate_portfolio_context(value: object, errors: list[str]) -> None:
    if value is None:
        return
    if not isinstance(value, dict):
        errors.append("portfolio_context must be null or a mapping")
        return
    _reject_unknown_keys(value, "portfolio_context", _PORTFOLIO_CONTEXT_KEYS, errors)
    if "gate_exists" in value and not isinstance(value["gate_exists"], bool):
        errors.append("portfolio_context.gate_exists must be a boolean")
    if "next_gate_references_valuation" in value and not isinstance(
        value["next_gate_references_valuation"], bool
    ):
        errors.append("portfolio_context.next_gate_references_valuation must be a boolean")
    # SS D/SS E: the literal next_gate text, any peer/comparator name, or price/valuation
    # framing language must never appear here -- scanned identically to any other free text.
    if "disclosure_note" in value:
        _scan_free_text(value["disclosure_note"], "portfolio_context.disclosure_note", errors)


def _validate_disclosed_evidence_conflicts(value: object, errors: list[str]) -> None:
    if value is None:
        return
    if not isinstance(value, list) or not value:
        errors.append("disclosed_evidence_conflicts must be null or a non-empty list")
        return
    for i, item in enumerate(value):
        if not _non_empty_str(item):
            errors.append(f"disclosed_evidence_conflicts[{i}] must be a non-empty string")
    _scan_free_text(value, "disclosed_evidence_conflicts", errors)


# ---------------------------------------------------------------------------
# Archetype-F test disclosure check (VALUATION-0003 SS C / SS I)
# ---------------------------------------------------------------------------

_ARCHETYPE_F_MARKER = re.compile(r"archetype-f test:", re.IGNORECASE)
_SEGMENT_PATTERN = re.compile(r"\bsegments?\b", re.IGNORECASE)
_ARCHETYPE_F_TOKEN = re.compile(
    r"\b(archetype f|diversified|multi-segment|sum-of-the-parts|reportable segments?)\b",
    re.IGNORECASE,
)


def _validate_archetype_f_disclosure(data: dict, errors: list[str]) -> None:
    """Mandatory whenever (a) a secondary archetype is assigned -- checked
    mechanically and strictly (the explicit 'Archetype-F test:' marker is
    required) -- or (b) the record's own rationale discusses segment
    structure at all, in which case at least some F-related reasoning token
    must be present. Condition (b) is disclosed as a best-effort heuristic,
    not a semantic guarantee: no mechanical text scan can fully verify that
    a genuine F-test was performed, only that the record does not stay
    silent on a segment-structure discussion it itself raises."""
    rationale = data.get("rationale")
    if not isinstance(rationale, str):
        return
    secondary = data.get("secondary_archetype")
    if secondary is not None and not _ARCHETYPE_F_MARKER.search(rationale):
        errors.append(
            "rationale must contain an explicit 'Archetype-F test:' disclosure when "
            "secondary_archetype is assigned"
        )
    if _SEGMENT_PATTERN.search(rationale) and not (
        _ARCHETYPE_F_MARKER.search(rationale) or _ARCHETYPE_F_TOKEN.search(rationale)
    ):
        errors.append(
            "rationale discusses segment structure but contains no archetype-F-related "
            "disclosure language (heuristic check, VALUATION-0003 SS C)"
        )


# ---------------------------------------------------------------------------
# Top-level record validation
# ---------------------------------------------------------------------------

@dataclass
class ValidationResult:
    valid: bool
    errors: list[str] = field(default_factory=list)
    source: str | None = None


@dataclass
class DirectoryValidationResult:
    valid: bool
    results: list[ValidationResult] = field(default_factory=list)

    @property
    def record_count(self) -> int:
        return len(self.results)


def validate_archetype_data(data: object, expected_ticker: str | None = None) -> list[str]:
    errors: list[str] = []
    if not isinstance(data, dict):
        return ["record must be a mapping"]

    missing = _TOP_LEVEL_REQUIRED - data.keys()
    if missing:
        errors.append(f"missing top-level key(s): {sorted(missing)}")
    _reject_unknown_keys(data, "<record>", _TOP_LEVEL_ALL, errors)

    if data.get("schema_version") != SCHEMA_VERSION:
        errors.append(f"schema_version must be {SCHEMA_VERSION!r}, got {data.get('schema_version')!r}")

    ticker = data.get("ticker")
    if not _non_empty_str(ticker):
        errors.append("ticker must be a non-empty string")
    elif expected_ticker is not None and ticker != expected_ticker:
        errors.append(f"ticker {ticker!r} does not match filename-derived {expected_ticker!r}")

    primary = data.get("primary_archetype")
    if primary not in _PRIMARY_VALUES:
        errors.append(f"primary_archetype invalid: {primary!r}")

    secondary = data.get("secondary_archetype")
    if secondary is not None:
        if secondary not in _SECONDARY_VALUES:
            errors.append(f"secondary_archetype invalid: {secondary!r}")
        elif secondary == primary:
            errors.append("secondary_archetype must not equal primary_archetype")
        if primary == _ABSTENTION:
            errors.append("secondary_archetype must be null when primary_archetype is the abstention value")

    gap = data.get("evidence_gap_statement")
    if primary == _ABSTENTION:
        if not _non_empty_str(gap):
            errors.append("evidence_gap_statement is required (non-empty) when primary_archetype is the abstention value")
        else:
            _scan_free_text(gap, "evidence_gap_statement", errors)
    else:
        if gap is not None:
            errors.append("evidence_gap_statement must be null for a determined record")

    if not _non_empty_str(data.get("rationale")):
        errors.append("rationale must be a non-empty string")
    else:
        _scan_free_text(data["rationale"], "rationale", errors)
        _validate_archetype_f_disclosure(data, errors)

    _validate_evidence_quality(data.get("evidence_quality"), errors)
    _validate_disclosed_evidence_conflicts(data.get("disclosed_evidence_conflicts"), errors)
    _validate_portfolio_context(data.get("portfolio_context"), errors)

    if data.get("lifecycle_status") not in _LIFECYCLE_VALUES:
        errors.append(f"lifecycle_status invalid: {data.get('lifecycle_status')!r}")
    if not _non_empty_str(data.get("sealed_at")):
        errors.append("sealed_at must be a non-empty string")
    if data.get("governing_decision") != "VALUATION-0003":
        errors.append(f"governing_decision must be 'VALUATION-0003', got {data.get('governing_decision')!r}")
    if not _non_empty_str(data.get("drafting_session_or_shard_id")):
        errors.append("drafting_session_or_shard_id must be a non-empty string")
    if not _non_empty_str(data.get("cohort_manifest_entry")):
        errors.append("cohort_manifest_entry must be a non-empty string")

    recorded_hash = data.get("content_sha256")
    if not _non_empty_str(recorded_hash):
        errors.append("content_sha256 must be a non-empty string")
    elif isinstance(data, dict) and not errors:
        expected = canonical_record_hash(data)
        if recorded_hash != expected:
            errors.append(f"content_sha256 does not reproduce -- recorded {recorded_hash!r}, recomputed {expected!r}")

    return errors


def _read_yaml(path: Path) -> tuple[object, list[str]]:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        return None, [f"could not read file: {exc}"]
    try:
        return yaml.safe_load(text), []
    except yaml.YAMLError as exc:
        return None, [f"YAML parse error: {exc}"]


def validate_archetype_file(path: Path) -> ValidationResult:
    expected_ticker = path.stem
    data, errors = _read_yaml(path)
    if errors:
        return ValidationResult(valid=False, errors=errors, source=str(path))
    errors = validate_archetype_data(data, expected_ticker=expected_ticker)
    return ValidationResult(valid=not errors, errors=errors, source=str(path))


# ---------------------------------------------------------------------------
# Cohort manifest validation
# ---------------------------------------------------------------------------

_MANIFEST_ROW_KEYS = frozenset({
    "ticker", "shard_id", "sealed_at", "content_sha256", "schema_version",
    "governing_decision", "record_path",
})
_MANIFEST_TOP_KEYS = frozenset({"schema_version", "governing_decision", "cohort"})


def validate_cohort_manifest(
    manifest_path: Path, records_dir: Path, canonical_universe: frozenset[str],
) -> ValidationResult:
    errors: list[str] = []
    data, read_errors = _read_yaml(manifest_path)
    if read_errors:
        return ValidationResult(valid=False, errors=read_errors, source=str(manifest_path))
    if not isinstance(data, dict):
        return ValidationResult(valid=False, errors=["manifest must be a mapping"], source=str(manifest_path))

    _reject_unknown_keys(data, "<manifest>", _MANIFEST_TOP_KEYS, errors)
    if data.get("schema_version") != SCHEMA_VERSION:
        errors.append(f"manifest schema_version must be {SCHEMA_VERSION!r}")
    if data.get("governing_decision") != "VALUATION-0003":
        errors.append("manifest governing_decision must be 'VALUATION-0003'")

    cohort = data.get("cohort")
    if not isinstance(cohort, list):
        errors.append("manifest cohort must be a list")
        return ValidationResult(valid=not errors, errors=errors, source=str(manifest_path))

    seen_tickers: set[str] = set()
    for i, row in enumerate(cohort):
        if not isinstance(row, dict):
            errors.append(f"cohort[{i}] must be a mapping")
            continue
        _reject_unknown_keys(row, f"cohort[{i}]", _MANIFEST_ROW_KEYS, errors)
        missing = _MANIFEST_ROW_KEYS - row.keys()
        if missing:
            errors.append(f"cohort[{i}] missing key(s): {sorted(missing)}")
            continue
        ticker = row["ticker"]
        if ticker in seen_tickers:
            errors.append(f"cohort has duplicate ticker: {ticker!r}")
        seen_tickers.add(ticker)

        record_path = records_dir / f"{ticker}.yaml"
        if not record_path.is_file():
            errors.append(f"cohort[{i}] ({ticker!r}) references missing record file {record_path}")
            continue
        record_data, record_read_errors = _read_yaml(record_path)
        if record_read_errors or not isinstance(record_data, dict):
            errors.append(f"cohort[{i}] ({ticker!r}) record file could not be parsed")
            continue
        expected_hash = canonical_record_hash(record_data)
        if row["content_sha256"] != expected_hash:
            errors.append(
                f"cohort[{i}] ({ticker!r}) content_sha256 mismatch -- manifest {row['content_sha256']!r}, "
                f"recomputed {expected_hash!r}"
            )
        if record_data.get("content_sha256") != row["content_sha256"]:
            errors.append(
                f"cohort[{i}] ({ticker!r}) manifest content_sha256 does not match the record's own recorded content_sha256"
            )

    # population completeness -- exact 27-name roster, zero missing, zero extra
    missing_from_manifest = canonical_universe - seen_tickers
    extra_in_manifest = seen_tickers - canonical_universe
    if missing_from_manifest:
        errors.append(f"manifest missing canonical ticker(s): {sorted(missing_from_manifest)}")
    if extra_in_manifest:
        errors.append(f"manifest has non-canonical ticker(s): {sorted(extra_in_manifest)}")

    # orphan sealed records -- every *.yaml in records_dir must appear in the manifest
    if records_dir.is_dir():
        on_disk = {
            p.stem for p in records_dir.glob("*.yaml") if p.name != "COHORT_MANIFEST.yaml"
        }
        orphans = on_disk - seen_tickers
        if orphans:
            errors.append(f"sealed record(s) on disk with no manifest entry: {sorted(orphans)}")

    return ValidationResult(valid=not errors, errors=errors, source=str(manifest_path))


def validate_archetype_directory(
    records_dir: Path, canonical_universe: frozenset[str],
) -> DirectoryValidationResult:
    results: list[ValidationResult] = []
    if not records_dir.is_dir():
        return DirectoryValidationResult(valid=True, results=[])

    for path in sorted(records_dir.glob("*.yaml")):
        if path.name == "COHORT_MANIFEST.yaml":
            continue
        results.append(validate_archetype_file(path))

    manifest_path = records_dir / "COHORT_MANIFEST.yaml"
    if manifest_path.is_file():
        results.append(validate_cohort_manifest(manifest_path, records_dir, canonical_universe))
    else:
        results.append(ValidationResult(valid=False, errors=["COHORT_MANIFEST.yaml is missing"], source=str(manifest_path)))

    # exact population check independent of the manifest's own accounting
    on_disk_tickers = {p.stem for p in records_dir.glob("*.yaml") if p.name != "COHORT_MANIFEST.yaml"}
    missing = canonical_universe - on_disk_tickers
    extra = on_disk_tickers - canonical_universe
    pop_errors = []
    if missing:
        pop_errors.append(f"missing sealed record(s) for canonical ticker(s): {sorted(missing)}")
    if extra:
        pop_errors.append(f"sealed record(s) for non-canonical ticker(s): {sorted(extra)}")
    if pop_errors:
        results.append(ValidationResult(valid=False, errors=pop_errors, source="<population>"))

    return DirectoryValidationResult(valid=all(r.valid for r in results), results=results)


if __name__ == "__main__":
    import sys

    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from relationship_validator import load_canonical_universe  # noqa: E402

    _repo_root = Path(__file__).resolve().parent
    _canonical = load_canonical_universe(_repo_root)
    _result = validate_archetype_directory(
        _repo_root / "intelligence" / "valuation_archetype", canonical_universe=_canonical,
    )
    if _result.valid:
        print(f"valuation_archetype_validator: OK ({_result.record_count} result(s))")
        sys.exit(0)
    else:
        print("valuation_archetype_validator: FAILED")
        for _r in _result.results:
            if not _r.valid:
                for _err in _r.errors:
                    print(f"  - [{_r.source}] {_err}")
        sys.exit(1)
