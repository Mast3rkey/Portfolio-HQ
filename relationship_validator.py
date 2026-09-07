"""
relationship_validator.py — read-only schema validator for the future
WS-0005 Milestone 4 pairwise relationship-record convention frozen by
`governance/decisions/REL-0001-ws0005-milestone4-relationship-schema-taxonomy-evidence-standard-and-inventory-authorization.md`.

REL-0001 §I authorizes exactly one bounded, inventory-only implementation
unit to create this module. That unit does not itself create any
`intelligence/relationships/*.yaml` or `.md` record — this validator exists
as schema infrastructure for a future, separately authorized relationship-
content batch, exactly mirroring `intelligence_validator.py`'s own
authorized-scope-before-content precedent (`decision_log.yaml`'s PI-0002,
which built the Company Intelligence validator before any company record
existed).

Scope, exactly what REL-0001 authorizes this module to validate:

- Source-of-truth convention (§B): `intelligence/relationships/
  <TICKER-A>_<TICKER-B>.yaml` with a matching `.md` companion; ticker order
  in the filename is deterministic alphabetical (`A_B`, never `B_A`); a pair
  must never exist in both `A_B` and `B_A` form; the filesystem directory
  listing is the index — no `intelligence/relationships/index.yaml` or any
  other stored index file is permitted (same filesystem-as-index doctrine
  `PI-0001`/`PI-0006` already froze for Company/Theme Intelligence, applied
  here per §B).
- Twelve-item closed primitive relationship taxonomy (§C), with
  `duplicate_economic_exposure`, `correlated_loss_mechanism`, and
  `missing_exposure` explicitly rejected as primitive `relationship_type`
  values — those three are derived conclusions only, never a stored
  primitive record type.
- Directionality rules (§D): a directional relationship (supplier/customer/
  manufacturing/technology_platform/capital_spending dependency) requires
  `subject`, `object`, and a `direction` narrative and must not declare
  `symmetric: true`; a normally-symmetric relationship (competitor,
  complement, and the four shared-co-exposure types) must declare
  `symmetric: true` and must not declare `subject`/`object`; `substitute`
  may be either, but must state its own symmetric/directional choice
  explicitly — never left implicit or inferred from filename order.
- Evidence/abstention standard (§E): every evidence entry must carry
  `claim`, `source`, `inspected_source_type`, `source_date`,
  `effective_date`, `evidence_classification`
  (`observed|inferred|modeled|judgmental`), `confidence`, `materiality`,
  `uncertainty`, and `disconfirming_evidence` (the key must be present —
  `null`/empty is allowed when nothing disconfirming is known, but the key
  must never simply be omitted, per §E's "never omitted merely because it
  complicates the record").
- Closed `decision_served` vocabulary (§F): at least one value from the six
  frozen values.
- `relationship_status` (§E): exactly one of
  `current|historical|potential|hypothetical`.
- Reference integrity (§J): both tickers named by a record must exist in
  either the current 27-name canonical roster (`targets.yaml`) or the
  retained governed universe of tickers that already carry a Company
  Intelligence record (`intelligence/companies/*.yaml`) — a live filesystem/
  data check at validation time, not a stored index, same discipline
  `intelligence_validator.py`'s own theme-reference check already uses.
- Markdown companion existence (§B): a `.yaml` record with no matching
  `.md` companion is invalid. This check is one-directional — it scans
  `.yaml` records and requires each to have a matching `.md` companion; it
  does not separately scan for an orphan `.md` file with no matching
  `.yaml` record.

This module is a validator, not a data producer. It never opens a file in
write/append/update mode, never creates a directory, and has zero import
relationship with `allocate.py`, `margin_state.py`, `targets.py`, or any
brokerage code in either direction (see
`test_relationship_validator.py`'s isolation tests) — nothing in this
repository imports it, and it cannot influence any allocator recommendation.
A missing or empty `intelligence/relationships/` directory is valid,
zero-coverage state, per REL-0001's own filesystem-as-index model — never an
error. This unit creates zero records, so the validator is exercised only
against that empty/absent state; every rule above is nonetheless implemented
now, ready for a future, separately authorized content batch.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import yaml

# ── §C: closed twelve-item primitive relationship taxonomy ──────────────────

PRIMITIVE_RELATIONSHIP_TYPES = frozenset({
    "supplier_dependency",
    "customer_dependency",
    "manufacturing_dependency",
    "technology_platform_dependency",
    "capital_spending_dependency",
    "regulatory_or_reimbursement_dependency",
    "commodity_or_energy_dependency",
    "financing_or_interest_rate_dependency",
    "geographic_or_geopolitical_dependency",
    "competitor",
    "substitute",
    "complement",
})

# §C: derived conclusions explicitly excluded as primitive record types —
# never independently assertable as if directly observed.
_DERIVED_ONLY_TYPES = frozenset({
    "duplicate_economic_exposure",
    "correlated_loss_mechanism",
    "missing_exposure",
})

# §D: directional-by-construction dependency types (subject depends on object).
_DIRECTIONAL_TYPES = frozenset({
    "supplier_dependency",
    "customer_dependency",
    "manufacturing_dependency",
    "technology_platform_dependency",
    "capital_spending_dependency",
})

# §D: symmetric-by-construction shared co-exposure types (never directional).
_ALWAYS_SYMMETRIC_TYPES = frozenset({
    "regulatory_or_reimbursement_dependency",
    "commodity_or_energy_dependency",
    "financing_or_interest_rate_dependency",
    "geographic_or_geopolitical_dependency",
    "competitor",
    "complement",
})

# §D: may be either, but the record must state its own choice explicitly —
# never assumed symmetric by default.
_EITHER_TYPES = frozenset({"substitute"})

assert (
    _DIRECTIONAL_TYPES | _ALWAYS_SYMMETRIC_TYPES | _EITHER_TYPES
    == PRIMITIVE_RELATIONSHIP_TYPES
)

# §E: evidence classification, exactly this closed vocabulary.
EVIDENCE_CLASSIFICATIONS = frozenset({"observed", "inferred", "modeled", "judgmental"})

# §E: relationship status, exactly this closed vocabulary.
RELATIONSHIP_STATUSES = frozenset({"current", "historical", "potential", "hypothetical"})

# §F: closed initial decision_served vocabulary.
DECISION_SERVED_VALUES = frozenset({
    "duplicate_exposure_detection",
    "thesis_monitoring",
    "stress_testing",
    "next_dollar_or_opportunity_cost",
    "missing_exposure_review",
    "zero_based_portfolio_review",
})

# §E: required keys on every evidence-list entry.
_EVIDENCE_ENTRY_REQUIRED_KEYS = {
    "claim",
    "source",
    "inspected_source_type",
    "source_date",
    "effective_date",
    "evidence_classification",
    "confidence",
    "materiality",
    "uncertainty",
    "disconfirming_evidence",
}

# §E: required keys on the reused review/freshness block (same shape as the
# frozen Company Intelligence schema's own `review:` block — no new
# freshness mechanism invented).
_REVIEW_REQUIRED_KEYS = {"cadence_days", "last_reviewed", "next_due"}
_REVIEW_LOG_REQUIRED_KEYS = {"date", "note"}

# §B: filename convention.
_FILENAME_TOKEN_SEP = "_"

# §B: no stored index file of any kind is permitted alongside relationship
# records — the directory listing itself is the index.
_PROHIBITED_INDEX_FILENAMES = frozenset({"index.yaml", "index.yml", "index.md"})


@dataclass
class ValidationResult:
    """Report, not an agent — no method here writes anything or triggers
    any action. Mirrors intelligence_validator.py's ValidationResult and,
    behind it, margin_state.py's MarginStateResult contract."""
    valid: bool
    errors: list[str] = field(default_factory=list)
    source: str | None = None
    """Path/identifier of the record this result describes, or None for a
    result produced from an in-memory mapping via validate_relationship_data()."""


@dataclass
class DirectoryValidationResult:
    """Aggregate result for a directory scan. A missing or empty directory
    is represented here as valid=True, results=[] — not an error, per
    REL-0001's own filesystem-as-index model (§B), the same treatment
    intelligence_validator.py's §16/§20 zero-coverage state already uses."""
    valid: bool
    results: list[ValidationResult] = field(default_factory=list)

    @property
    def record_count(self) -> int:
        return len(self.results)


# ── field-level checks ────────────────────────────────────────────────────

def _require_keys(value: object, field_name: str, required: set[str], errors: list[str]) -> bool:
    if not isinstance(value, dict):
        errors.append(f"{field_name} must be a mapping, got {type(value).__name__}")
        return False
    missing = required - value.keys()
    if missing:
        errors.append(f"{field_name} missing required key(s): {sorted(missing)}")
        return False
    return True


def _validate_evidence_entry(entry: object, index: int, errors: list[str]) -> None:
    field_name = f"evidence[{index}]"
    if not _require_keys(entry, field_name, _EVIDENCE_ENTRY_REQUIRED_KEYS, errors):
        return
    entry = entry  # type: dict

    classification = entry.get("evidence_classification")
    if classification not in EVIDENCE_CLASSIFICATIONS:
        errors.append(
            f"{field_name}.evidence_classification must be exactly one of "
            f"{sorted(EVIDENCE_CLASSIFICATIONS)} (REL-0001 §E) — got {classification!r}"
        )

    for key in ("claim", "source", "inspected_source_type"):
        val = entry.get(key)
        if not isinstance(val, str) or not val.strip():
            errors.append(f"{field_name}.{key} must be a non-empty string")

    for key in ("source_date", "effective_date"):
        val = entry.get(key)
        # Accept a YAML-parsed date/datetime object or an ISO-formatted string
        # — same looseness the existing review.last_reviewed/next_due fields
        # already tolerate elsewhere in this repository.
        if val is None or (isinstance(val, str) and not val.strip()):
            errors.append(f"{field_name}.{key} must be present and non-empty")

    for key in ("confidence", "materiality"):
        val = entry.get(key)
        # bool is a subclass of int in Python (False == 0, True == 1), so a
        # literal True/False must be rejected explicitly — it is never a
        # genuine stated confidence/materiality value, only an accidental
        # pass-through. 0 itself remains a valid explicit value.
        if val is None or isinstance(val, bool) or (isinstance(val, str) and not val.strip()):
            errors.append(f"{field_name}.{key} must be stated explicitly (REL-0001 §E)")

    uncertainty = entry.get("uncertainty")
    if not isinstance(uncertainty, str) or not uncertainty.strip():
        errors.append(
            f"{field_name}.uncertainty must be a non-empty string stating what specifically "
            f"is not known or could invalidate the claim (REL-0001 §E)"
        )

    # disconfirming_evidence: the key must be present (checked by
    # _require_keys above) but its value may legitimately be None/empty —
    # §E requires it never be silently omitted, not that it always be
    # populated.


def _validate_evidence_list(value: object, errors: list[str]) -> None:
    if not isinstance(value, list) or not value:
        errors.append("evidence must be a non-empty list of claim entries (REL-0001 §E)")
        return
    for i, entry in enumerate(value):
        _validate_evidence_entry(entry, i, errors)


def _validate_review(value: object, errors: list[str]) -> None:
    if not _require_keys(value, "review", _REVIEW_REQUIRED_KEYS, errors):
        return
    log = value.get("log")  # type: ignore[union-attr]
    if log is not None:
        if not isinstance(log, list):
            errors.append("review.log must be a list")
        else:
            for i, item in enumerate(log):
                if not isinstance(item, dict) or (_REVIEW_LOG_REQUIRED_KEYS - item.keys()):
                    errors.append(
                        f"review.log[{i}] missing required key(s): "
                        f"{sorted(_REVIEW_LOG_REQUIRED_KEYS - (item.keys() if isinstance(item, dict) else set()))}"
                    )


def _validate_decision_served(value: object, errors: list[str]) -> None:
    if not isinstance(value, list) or not value:
        errors.append(
            "decision_served must be a non-empty list naming at least one value from the "
            f"closed REL-0001 §F vocabulary {sorted(DECISION_SERVED_VALUES)}"
        )
        return
    for v in value:
        if v not in DECISION_SERVED_VALUES:
            errors.append(
                f"decision_served contains {v!r}, not in the closed §F vocabulary "
                f"{sorted(DECISION_SERVED_VALUES)}"
            )


def _validate_directionality(data: dict, errors: list[str]) -> None:
    """§D: directional types require subject/object/direction and must not
    claim symmetric: true; always-symmetric types require symmetric: true
    and must not carry subject/object; substitute must explicitly state its
    own symmetric/directional choice — never inferred from filename order."""
    rel_type = data.get("relationship_type")
    symmetric = data.get("symmetric")

    if not isinstance(symmetric, bool):
        errors.append(
            "symmetric must be an explicit boolean (true/false) — REL-0001 §D requires every "
            "record to state its own symmetric/directional choice explicitly, never inferred "
            "from filename order or relationship_type alone"
        )
        symmetric = None  # can't reason further about directional fields below

    subject = data.get("subject")
    obj = data.get("object")
    direction = data.get("direction")

    if rel_type in _DIRECTIONAL_TYPES:
        if symmetric is True:
            errors.append(
                f"{rel_type!r} is directional-by-construction (REL-0001 §D) and must not "
                f"declare symmetric: true"
            )
        for key, val in (("subject", subject), ("object", obj), ("direction", direction)):
            if not isinstance(val, str) or not val.strip():
                errors.append(
                    f"{key} is required and must be a non-empty string for directional type "
                    f"{rel_type!r} (REL-0001 §D)"
                )
    elif rel_type in _ALWAYS_SYMMETRIC_TYPES:
        if symmetric is False:
            errors.append(
                f"{rel_type!r} is symmetric-by-construction (REL-0001 §D) and must not "
                f"declare symmetric: false"
            )
        if subject is not None or obj is not None:
            errors.append(
                f"{rel_type!r} is a symmetric co-equal-subjects type (REL-0001 §D) and must "
                f"not declare a directional subject/object pair"
            )
    elif rel_type in _EITHER_TYPES:
        # symmetric must be an explicit bool (already checked above); no
        # further shape constraint beyond that explicit declaration.
        if symmetric is True and (subject is not None or obj is not None):
            errors.append(
                f"{rel_type!r} declared symmetric: true and must not also declare a "
                f"directional subject/object pair"
            )
        if symmetric is False:
            for key, val in (("subject", subject), ("object", obj), ("direction", direction)):
                if not isinstance(val, str) or not val.strip():
                    errors.append(
                        f"{key} is required and must be a non-empty string when "
                        f"{rel_type!r} declares symmetric: false (REL-0001 §D)"
                    )


def _validate_tickers_field(data: dict, errors: list[str]) -> tuple[str | None, str | None]:
    """Validates the record's own `tickers: [A, B]` field, alphabetically
    ordered, matching the caller-supplied filename order downstream. Returns
    (ticker_a, ticker_b) if structurally valid, else (None, None)."""
    tickers = data.get("tickers")
    if not isinstance(tickers, list) or len(tickers) != 2:
        errors.append("tickers must be a two-element list [TICKER-A, TICKER-B]")
        return None, None
    a, b = tickers
    if not (isinstance(a, str) and a.strip() and isinstance(b, str) and b.strip()):
        errors.append("tickers[0] and tickers[1] must both be non-empty strings")
        return None, None
    if a == b:
        errors.append(f"tickers must name two distinct companies — got {a!r} twice")
        return None, None
    if sorted((a, b)) != [a, b]:
        errors.append(
            f"tickers must be alphabetically ordered [A, B] (REL-0001 §B) — got [{a!r}, {b!r}]"
        )
        return None, None
    return a, b


def _referenced_tickers_exist(
    a: str, b: str, canonical_universe: frozenset[str], retained_universe: frozenset[str],
    errors: list[str],
) -> None:
    """§J: both referenced tickers must exist in the canonical 27-name
    roster or the retained governed universe of tickers already carrying a
    Company Intelligence record. Callers with no live repository to check
    against (e.g. validate_relationship_data() called on a synthetic
    in-memory mapping) may pass empty frozensets to skip this check."""
    if not canonical_universe and not retained_universe:
        return
    known = canonical_universe | retained_universe
    for ticker in (a, b):
        if ticker not in known:
            errors.append(
                f"ticker {ticker!r} is not in the canonical 27-name roster or the retained "
                f"governed universe of tickers with an existing Company Intelligence record "
                f"(REL-0001 §J)"
            )


# ── public API: in-memory record validation (no filesystem access) ─────────

def validate_relationship_data(
    data: object,
    *,
    source: str | None = None,
    canonical_universe: frozenset[str] = frozenset(),
    retained_universe: frozenset[str] = frozenset(),
) -> ValidationResult:
    """Validate an already-parsed relationship mapping against REL-0001's
    frozen schema. Never touches the filesystem. `canonical_universe`/
    `retained_universe` are optional — pass the live roster to enforce §J's
    reference-integrity rule, or leave empty (default) to validate schema
    shape only, e.g. for synthetic fixtures in tests."""
    errors: list[str] = []

    if not isinstance(data, dict):
        errors.append(f"root document must be a mapping, got {type(data).__name__}")
        return ValidationResult(valid=False, errors=errors, source=source)

    rel_type = data.get("relationship_type")
    if rel_type in _DERIVED_ONLY_TYPES:
        errors.append(
            f"relationship_type {rel_type!r} is a derived conclusion (REL-0001 §C), never a "
            f"primitive record type — it must not appear as relationship_type on any "
            f"intelligence/relationships/*.yaml record"
        )
    elif rel_type not in PRIMITIVE_RELATIONSHIP_TYPES:
        errors.append(
            f"relationship_type must be exactly one of the twelve closed REL-0001 §C "
            f"primitives {sorted(PRIMITIVE_RELATIONSHIP_TYPES)} — got {rel_type!r}"
        )

    status = data.get("relationship_status")
    if status not in RELATIONSHIP_STATUSES:
        errors.append(
            f"relationship_status must be exactly one of {sorted(RELATIONSHIP_STATUSES)} "
            f"(REL-0001 §E) — got {status!r}"
        )

    a, b = _validate_tickers_field(data, errors)
    if a is not None and b is not None:
        _referenced_tickers_exist(a, b, canonical_universe, retained_universe, errors)

    if rel_type in PRIMITIVE_RELATIONSHIP_TYPES:
        _validate_directionality(data, errors)

    _validate_decision_served(data.get("decision_served"), errors)
    _validate_evidence_list(data.get("evidence"), errors)
    _validate_review(data.get("review"), errors)

    return ValidationResult(valid=not errors, errors=errors, source=source)


# ── public API: file/directory validation ───────────────────────────────────

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


def validate_relationship_file(
    path: str | Path,
    *,
    canonical_universe: frozenset[str] = frozenset(),
    retained_universe: frozenset[str] = frozenset(),
) -> ValidationResult:
    """Read and validate a single relationship YAML file. Read-only — opens
    the file in text mode for reading only, never write/append/update. Also
    enforces §B's filename-matches-ticker-order convention and the
    matching-Markdown-companion requirement."""
    path = Path(path)
    source = str(path)
    data, read_errors = _read_yaml(path)
    if read_errors:
        return ValidationResult(valid=False, errors=read_errors, source=source)

    result = validate_relationship_data(
        data, source=source,
        canonical_universe=canonical_universe, retained_universe=retained_universe,
    )

    if isinstance(data, dict):
        tickers = data.get("tickers")
        if isinstance(tickers, list) and len(tickers) == 2 and all(isinstance(t, str) for t in tickers):
            expected_stem = _FILENAME_TOKEN_SEP.join(tickers)
            if path.stem != expected_stem:
                result.errors.append(
                    f"filename stem {path.stem!r} does not match the record's own alphabetical "
                    f"tickers field {tickers!r} (expected {expected_stem!r}) — REL-0001 §B"
                )

    md_companion = path.with_suffix(".md")
    if not md_companion.is_file():
        result.errors.append(
            f"missing required Markdown companion {md_companion.name!r} for {path.name!r} "
            f"(REL-0001 §B)"
        )

    result.valid = not result.errors
    return result


def _reverse_pair_key(stem: str) -> str | None:
    parts = stem.split(_FILENAME_TOKEN_SEP)
    if len(parts) != 2:
        return None
    return f"{parts[1]}{_FILENAME_TOKEN_SEP}{parts[0]}"


def validate_relationships_directory(
    directory: str | Path,
    *,
    canonical_universe: frozenset[str] = frozenset(),
    retained_universe: frozenset[str] = frozenset(),
) -> DirectoryValidationResult:
    """Scan `<directory>/*.yaml` and validate each relationship record
    found. A missing or empty directory is valid, zero-coverage state
    (REL-0001 §B's filesystem-as-index model) — never an error. One invalid
    file never stops the scan; every file is reported. Also enforces: no
    A_B/B_A reverse-duplicate pair coexists, and no prohibited index file
    (`index.yaml`/`index.yml`/`index.md`) is present — the directory
    listing itself is the only index REL-0001 permits."""
    directory = Path(directory)

    if not directory.exists() or not directory.is_dir():
        return DirectoryValidationResult(valid=True, results=[])

    yaml_paths = sorted(directory.glob("*.yaml"))

    index_hits = [p for p in directory.iterdir() if p.name.lower() in _PROHIBITED_INDEX_FILENAMES]
    index_error_result = None
    if index_hits:
        index_error_result = ValidationResult(
            valid=False,
            errors=[
                f"{p.name!r} is a prohibited stored index file — REL-0001 §B freezes the "
                f"filesystem directory listing itself as the only index; no "
                f"intelligence/relationships/index.* file is ever permitted"
                for p in index_hits
            ],
            source=str(directory),
        )

    results = [
        validate_relationship_file(
            p, canonical_universe=canonical_universe, retained_universe=retained_universe,
        )
        for p in yaml_paths
    ]

    # Reverse-duplicate-pair check (§B): a pair must never exist as both
    # A_B.yaml and B_A.yaml.
    stems = {p.stem for p in yaml_paths}
    seen_pair_errors: set[str] = set()
    for p in yaml_paths:
        reverse = _reverse_pair_key(p.stem)
        if reverse and reverse in stems and reverse != p.stem:
            pair_key = _FILENAME_TOKEN_SEP.join(sorted((p.stem, reverse)))
            if pair_key not in seen_pair_errors:
                seen_pair_errors.add(pair_key)
                results.append(
                    ValidationResult(
                        valid=False,
                        errors=[
                            f"{p.stem}.yaml and {reverse}.yaml both exist — a pair must never "
                            f"be recorded in both A_B and B_A form (REL-0001 §B)"
                        ],
                        source=str(directory),
                    )
                )

    if index_error_result is not None:
        results.append(index_error_result)

    return DirectoryValidationResult(valid=all(r.valid for r in results), results=results)


# ── canonical/retained universe helpers (live filesystem/data reads) ───────

def load_canonical_universe(repo_root: str | Path) -> frozenset[str]:
    """Read the current canonical roster straight from targets.yaml's
    destination: list, equity rows only (§J's "current 27-name canonical
    equity roster"). Read-only; never touches intelligence/relationships/."""
    repo_root = Path(repo_root)
    targets_path = repo_root / "targets.yaml"
    if not targets_path.is_file():
        return frozenset()
    try:
        data = yaml.safe_load(targets_path.read_text())
    except yaml.YAMLError:
        return frozenset()
    if not isinstance(data, dict):
        return frozenset()
    destination = data.get("destination")
    if not isinstance(destination, list):
        return frozenset()
    return frozenset(
        row["ticker"]
        for row in destination
        if isinstance(row, dict) and row.get("asset_class") == "equity" and isinstance(row.get("ticker"), str)
    )


def load_retained_universe(repo_root: str | Path) -> frozenset[str]:
    """Read the retained governed universe: every ticker that currently
    carries a Company Intelligence record under intelligence/companies/,
    canonical or not (PI-0035's "retained/historical-advisory/non-current"
    records included) — a live filesystem check, not a stored index."""
    repo_root = Path(repo_root)
    companies_dir = repo_root / "intelligence" / "companies"
    if not companies_dir.is_dir():
        return frozenset()
    return frozenset(p.stem for p in companies_dir.glob("*.yaml"))


if __name__ == "__main__":
    import sys

    _repo_root = Path(__file__).resolve().parent
    _canonical = load_canonical_universe(_repo_root)
    _retained = load_retained_universe(_repo_root)
    _result = validate_relationships_directory(
        _repo_root / "intelligence" / "relationships",
        canonical_universe=_canonical,
        retained_universe=_retained,
    )
    if _result.valid:
        print(f"relationship_validator: OK ({_result.record_count} record(s))")
        sys.exit(0)
    else:
        print("relationship_validator: FAILED")
        for _r in _result.results:
            if not _r.valid:
                for _err in _r.errors:
                    print(f"  - [{_r.source}] {_err}")
        sys.exit(1)
