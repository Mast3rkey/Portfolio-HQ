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

VERSION 1.1 bounded correction (post-PR-#253-review-4868016198): a fresh
independent exact-head review found the four per-axis validators were a
denylist (a fixed 8-name `_FORBIDDEN_ANSWER_KEY_FIELDS` set), not a closed
schema -- confirmed live by the reviewer's own direct execution: an
arbitrary `score`/`weight`/`recommendation`-shaped key nested inside
`capital_priority`, or forbidden free text (a chart/policy/allocation
reference) inside `risk_concentration.notes`, `economic_role.role_basis`,
or `evidence_quality.thesis_uncertainty_statement`, all validated cleanly.
`_validate_risk_concentration`/`_validate_evidence_quality` ran no
forbidden-key or forbidden-content check of any kind. Mitigating fact
independently reconfirmed by this correction: none of the real 27 sealed
records contains this class of content -- a latent validator gap, not a
demonstrated defect in the delivered batch.

Fixed by making every axis genuinely closed-schema (an explicit permitted-
key set per axis, derived from `TIER-0002`/`TIER-0004`'s controlling text
plus a live scan of all 27 real records' actually-used keys -- never
invented), rejecting any key outside that set, and extending the existing
`capital_priority.rationale`-only content scan (`_RATIONALE_FORBIDDEN_
PATTERNS`) into a single shared, broader `_FORBIDDEN_CONTENT_PATTERNS`
check applied uniformly to every free-text field across all four axes
(`economic_role.company_role`/`role_basis`, `capital_priority.rationale`,
`risk_concentration.notes`, `evidence_quality.thesis_uncertainty_
statement`) -- closing the key-level and content-level bypass together,
since the reviewer's own reproduction demonstrated both classes (a
forbidden field name, and forbidden content inside an otherwise-permitted
field). Top-level record keys were already closed (`_validate_no_stray_
top_level_fields`, pre-existing) -- this correction extends the same
discipline to axis dicts and to the cohort-manifest's own row/top-level
shape, which had the identical required-only (not closed) gap.

Empirically verified against all 27 live `intelligence/classification/`
records and the manifest: zero false positives from the broadened
content scan, zero new validation failures.

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
# v1.1: closed schema -- the only keys ever permitted on economic_role,
# derived from TIER-0002 Sec3.3/TIER-0004 Sec12 plus a live scan of all 27
# real records (which use exactly the three required keys; no record is
# currently abstaining, but the abstention-only pair remains permitted per
# TIER-0004 Sec12.2).
_ECONOMIC_ROLE_ALLOWED_KEYS = frozenset(_ECONOMIC_ROLE_REQUIRED_KEYS | _ECONOMIC_ROLE_ABSTENTION_ONLY_KEYS)

# ── capital_priority (TIER-0002 Sec3.4) ─────────────────────────────────────

CAPITAL_PRIORITY_STATUSES = frozenset({
    "maintain_current_weight", "case_for_review", "no_assessment",
})
_CAPITAL_PRIORITY_REQUIRED_KEYS = {"status"}
_COMPARATOR_SET_MIN, _COMPARATOR_SET_MAX = 2, 5
# v1.1: closed schema. `assessed_date`/`assessing_record` are not required
# by TIER-0002's own text but are present on every one of the 27 real
# records regardless of `status` (including `no_assessment`) -- permitted,
# per this correction's own "derive from the merged decisions and all 27
# live records" instruction, not invented.
_CAPITAL_PRIORITY_ALLOWED_KEYS = frozenset({
    "status", "rationale", "comparator_set", "assessed_date", "assessing_record",
})

# A free-text field must never itself carry a numeric target/allocation
# figure, a direct trade instruction, or (v1.1) any policy/committee/gate/
# chart-domain concept -- capital_priority is explicitly never a
# target_pct/buy-sell channel (TIER-0002 Sec3.4), and no free-text field on
# any axis may carry the answer-key content TIER-0004 Sec11 forbids merely
# because it isn't shaped like one of the eight forbidden *field names*.
# v1.1: broadened from a `capital_priority.rationale`-only check (the
# reviewer's own live reproduction found `risk_concentration.notes`,
# `economic_role.role_basis`, and `evidence_quality.thesis_uncertainty_
# statement` all validated cleanly with chart/policy/conviction content
# inside them) into one shared list applied to every free-text field on
# every axis by `_scan_free_text()` below. Empirically verified: zero false
# positives against all 27 real records' actual free-text content.
_FORBIDDEN_CONTENT_PATTERNS = [
    re.compile(p, re.IGNORECASE) for p in (
        r"\btarget_pct\b",
        r"\d+(?:\.\d+)?\s*%\s*(?:of\s+book|target|weight|allocation)",
        r"\b(?:buy|sell|trim|add to|reduce|increase)\s+(?:it|this|the position|to\b)",
        r"\brecommend(?:ed|ing)?\s+(?:increasing|decreasing|reducing|adding)\b",
        r"\bportfolio_role_ref\b",
        r"\bconviction\b",
        r"\bcommittee review\b",
        r"\bgated\b",
        r"\bgates\.yaml\b",
        r"\bchart[- ]?evidence\b",
        r"\bsupport[/ -]resistance\b",
        r"\btechnical indicator",
        r"\bprice[- ]action\b",
        r"\btradingview\b",
        r"\bCHART-000[12]\b",
    )
]

# ── risk_concentration (TIER-0002 Sec3.5) -- structural shape only ─────────

_RISK_CONCENTRATION_REQUIRED_KEYS = {
    "cluster_cap_membership", "issuer_lookthrough_membership",
    "relationship_record_coverage", "unmeasured_flag",
}
# v1.1: closed schema -- `notes` is present (typically empty-string) on
# every one of the 27 real records; permitted but not required.
_RISK_CONCENTRATION_ALLOWED_KEYS = frozenset(_RISK_CONCENTRATION_REQUIRED_KEYS | {"notes"})

# ── evidence_quality (TIER-0002 Sec3.6) ─────────────────────────────────────

PRIMARY_SOURCE_COVERAGE_VALUES = frozenset({
    "comprehensive", "partial", "limited", "blocked",
})
RISK_SEVERITY_VALUES = frozenset({"low", "moderate", "high"})
_EVIDENCE_QUALITY_REQUIRED_KEYS = {
    "primary_source_coverage", "highest_disclosed_risk_severity",
    "thesis_uncertainty_statement",
}
# v1.1: closed schema -- `review_trigger_notes` is present (typically
# empty-string) on every one of the 27 real records; permitted but not
# required.
_EVIDENCE_QUALITY_ALLOWED_KEYS = frozenset(_EVIDENCE_QUALITY_REQUIRED_KEYS | {"review_trigger_notes"})

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


def _reject_unknown_keys(
    value: dict, field_name: str, allowed: frozenset[str], errors: list[str],
) -> None:
    """v1.1: closed-schema enforcement -- any key on `value` outside
    `allowed` is an error naming the axis and the exact unexpected key(s)
    (the record's own file path is already carried by the enclosing
    `ValidationResult.source`, per this module's existing error-message
    convention -- see the forbidden-answer-key-field errors above, which
    follow the same pattern)."""
    unknown = set(value.keys()) - allowed
    if unknown:
        errors.append(
            f"{field_name} contains unexpected key(s) {sorted(unknown)} -- this axis's schema "
            f"is closed; only {sorted(allowed)} are permitted (TIER-0002/TIER-0004)"
        )


def _scan_free_text(value: object, field_name: str, errors: list[str]) -> None:
    """v1.1: content-level check applied to every free-text field on every
    axis (not merely `capital_priority.rationale`) -- a field can carry
    forbidden answer-key/policy/chart content while still being a
    perfectly permitted *key* under the closed schema above; this closes
    that half of the reviewer's demonstrated bypass."""
    if not isinstance(value, str) or not value:
        return
    for p in _FORBIDDEN_CONTENT_PATTERNS:
        if p.search(value):
            errors.append(
                f"{field_name} contains forbidden content matching {p.pattern!r} -- no free-text "
                f"field may carry a policy/committee/gate/chart-domain/allocation-instruction "
                f"reference (TIER-0004 Sec11)"
            )
            break


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

    _reject_unknown_keys(value, "economic_role", _ECONOMIC_ROLE_ALLOWED_KEYS, errors)
    _scan_free_text(value.get("company_role"), "economic_role.company_role", errors)
    _scan_free_text(value.get("role_basis"), "economic_role.role_basis", errors)

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

    _reject_unknown_keys(value, "capital_priority", _CAPITAL_PRIORITY_ALLOWED_KEYS, errors)

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
    else:
        _scan_free_text(rationale, "capital_priority.rationale", errors)

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

    # No _FORBIDDEN_ANSWER_KEY_FIELDS loop here, deliberately: this
    # module's own docstring states that a cluster/issuer-lookthrough
    # *reference* inside risk_concentration is expected and required,
    # never flagged, since this axis is computed only after both judgment
    # axes seal. The closed-schema check below is the correct mechanism --
    # it rejects any key outside this axis's own four required fields plus
    # `notes`, which already excludes the literal forbidden-field names
    # (`caps`/`clusters`/`issuer_lookthrough`/etc.) without special-casing.
    _reject_unknown_keys(value, "risk_concentration", _RISK_CONCENTRATION_ALLOWED_KEYS, errors)
    _scan_free_text(value.get("notes"), "risk_concentration.notes", errors)

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

    for key in _FORBIDDEN_ANSWER_KEY_FIELDS:
        if key in value:
            errors.append(
                f"evidence_quality.{key} is a forbidden answer-key field (TIER-0004 Sec11) -- "
                f"must never appear inside this axis"
            )

    _reject_unknown_keys(value, "evidence_quality", _EVIDENCE_QUALITY_ALLOWED_KEYS, errors)

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

    statement = value.get("thesis_uncertainty_statement")
    if not _non_empty_str(statement):
        errors.append(
            "evidence_quality.thesis_uncertainty_statement is required and must be a "
            "non-empty string (TIER-0002 Sec3.6)"
        )
    else:
        _scan_free_text(statement, "evidence_quality.thesis_uncertainty_statement", errors)


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
# v1.1: closed schema -- every real manifest row uses exactly these seven
# keys, no more (live-scanned across all 27 rows); required == allowed here.
_MANIFEST_ROW_ALLOWED_KEYS = frozenset(_MANIFEST_REQUIRED_ROW_KEYS)
# v1.1: closed schema for the manifest document itself -- `schema_version`,
# `governing_decision`, `cohort` (live-scanned; matches the manifest's own
# integration-script authoring shape).
_MANIFEST_TOP_LEVEL_ALLOWED_KEYS = frozenset({"schema_version", "governing_decision", "cohort"})


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

    unknown_top = set(manifest_data.keys()) - _MANIFEST_TOP_LEVEL_ALLOWED_KEYS
    if unknown_top:
        errors.append(
            f"cohort manifest contains unexpected top-level key(s) {sorted(unknown_top)} -- "
            f"only {sorted(_MANIFEST_TOP_LEVEL_ALLOWED_KEYS)} are permitted"
        )

    rows = manifest_data["cohort"]
    seen_tickers: set[str] = set()
    for i, row in enumerate(rows):
        if not isinstance(row, dict) or (_MANIFEST_REQUIRED_ROW_KEYS - row.keys()):
            missing = _MANIFEST_REQUIRED_ROW_KEYS - (row.keys() if isinstance(row, dict) else set())
            errors.append(f"cohort[{i}] missing required key(s): {sorted(missing)}")
            continue
        unknown_row = row.keys() - _MANIFEST_ROW_ALLOWED_KEYS
        if unknown_row:
            errors.append(
                f"cohort[{i}] contains unexpected key(s) {sorted(unknown_row)} -- manifest row "
                f"schema is closed, only {sorted(_MANIFEST_ROW_ALLOWED_KEYS)} are permitted"
            )
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
