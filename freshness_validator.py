"""
freshness_validator.py — read-only schema and cross-file validator for the
Research Freshness Framework's two owned data files (see
docs/FRESHNESS_PLANNER_V1_SPEC.md §3-§5; authorized in bounded scope by
governance/decisions/AUTO-0002-freshness-local-foundation.md):

  - intelligence/freshness_registry.yaml
  - intelligence/freshness_checkpoints.yaml

Scope, exactly what AUTO-0002 authorizes: top-level document schema for
both files, the registry row schema, the checkpoint row schema, the
ordered-channel object schema, and the six cross-file invariants listed in
AUTO-0002's Decision section (mirroring spec §4.1). Replacement-
authorization validation (spec §14) is explicitly out of scope for this
tranche and is not implemented here — `intelligence/freshness_replacements/`
is never read, referenced, or validated against by this module.

This module is a validator, not a data producer. It never opens either
YAML file in write/append/update mode, never creates a directory, and
never touches holdings.yaml, targets.yaml, or any Company/Theme
Intelligence file. It imports neither intelligence_validator.py nor
intelligence_report.py, in either direction (see
test_freshness_validator.py's isolation tests), and has zero import
relationship with allocate.py or margin_state.py.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import date, datetime
from pathlib import Path

import yaml

# ── closed vocabularies ───────────────────────────────────────────────────

_FILING_TRIGGER_PROFILES = {"domestic_issuer_v1", "foreign_private_issuer_v1"}

_CHECKPOINT_STATUSES = {"pending", "verified"}

_DOMESTIC_CHANNELS = (
    "annual_filing",
    "quarterly_filing",
    "event_filing_watermark",
    "earnings_release",
)

_FPI_CHANNELS = (
    "annual_20f",
    "earnings_6k_watermark",
    "earnings_release",
)

_PROFILE_CHANNELS = {
    "domestic_issuer_v1": _DOMESTIC_CHANNELS,
    "foreign_private_issuer_v1": _FPI_CHANNELS,
}

# AUTO-0002 Decision §1: official-form mappings fixed as new precision —
# the specification states only parenthetical labels, never exact literals.
_CHANNEL_OFFICIAL_FORM_TYPE = {
    "annual_filing": "10-K",
    "quarterly_filing": "10-Q",
    "event_filing_watermark": "8-K",
    "annual_20f": "20-F",
    "earnings_6k_watermark": "6-K",
    "earnings_release": "earnings_release",
}

_CHANNEL_REQUIRED_KEYS = {
    "channel_name",
    "official_form_type",
    "stable_source_id",
    "official_source_date",
    "fiscal_period",
    "incorporation_reference",
}

_REGISTRY_ROW_REQUIRED_KEYS = {
    "ticker",
    "company_record_authority",
    "enrollment_authority",
    "enrolled_at",
    "template_version",
    "filing_trigger_profile",
    "refresh_policy",
    "monitoring_enabled",
}

_CHECKPOINT_ROW_REQUIRED_KEYS = {
    "ticker",
    "checkpoint_status",
    "channels",
    "established_by",
}

_ISO_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


@dataclass
class ValidationResult:
    """Report, not an agent — no method here writes anything or triggers
    any action. Mirrors intelligence_validator.py's ValidationResult and
    margin_state.py's MarginStateResult contract."""
    valid: bool
    errors: list[str] = field(default_factory=list)


# ── local ISO-date parser (independent of intelligence_report.py) ──────────

def _is_valid_local_date(value: object) -> bool:
    """AUTO-0002 Decision §1 ISO-date rule: accepts a `datetime.date`
    (PyYAML-native); accepts a strict `YYYY-MM-DD` string; rejects a
    `datetime.datetime` outright (checked before `date`, since `datetime`
    is itself a `date` subclass — never silently truncated); rejects any
    malformed string or any other type. Independently implemented here,
    not imported from or delegated to intelligence_report.py."""
    if isinstance(value, datetime):
        return False
    if isinstance(value, date):
        return True
    if isinstance(value, str):
        if not _ISO_DATE_RE.match(value):
            return False
        try:
            datetime.strptime(value, "%Y-%m-%d")
        except ValueError:
            return False
        return True
    return False


# ── shared helpers ──────────────────────────────────────────────────────────

def _is_non_empty_str(value: object) -> bool:
    return isinstance(value, str) and value.strip() != ""


def _validate_top_level_document(data: object, errors: list[str]) -> dict | None:
    """Both files: root must be a mapping; schema_version required and
    must be int 1 exactly; tickers required and must be a list of
    mappings. Missing-key and malformed-value errors are always reported
    as distinct classes. Unexpected top-level keys are permitted."""
    if not isinstance(data, dict):
        errors.append(f"document root must be a mapping, got {type(data).__name__}")
        return None

    if "schema_version" not in data:
        errors.append("missing required top-level key: schema_version")
    else:
        sv = data["schema_version"]
        if not (isinstance(sv, int) and not isinstance(sv, bool) and sv == 1):
            errors.append(
                f"schema_version must be the integer 1 exactly, got {sv!r} "
                f"({type(sv).__name__})"
            )

    if "tickers" not in data:
        errors.append("missing required top-level key: tickers")
        return data

    tickers = data["tickers"]
    if not isinstance(tickers, list):
        errors.append(f"tickers must be a list, got {type(tickers).__name__}")
        return data

    for i, row in enumerate(tickers):
        if not isinstance(row, dict):
            errors.append(f"tickers[{i}] must be a mapping, got {type(row).__name__}")

    return data


# ── registry row schema ─────────────────────────────────────────────────────

def _validate_registry_row(row: dict, errors: list[str]) -> None:
    missing = _REGISTRY_ROW_REQUIRED_KEYS - row.keys()
    if missing:
        errors.append(
            f"registry row {row.get('ticker', '<unknown>')!r} missing required "
            f"key(s): {sorted(missing)}"
        )

    for key in ("ticker", "company_record_authority", "enrollment_authority",
                "template_version", "refresh_policy"):
        if key in row and not _is_non_empty_str(row[key]):
            errors.append(
                f"registry row {row.get('ticker', '<unknown>')!r}: {key!r} must be "
                f"a non-empty string, got {row[key]!r}"
            )

    if "enrolled_at" in row and not _is_valid_local_date(row["enrolled_at"]):
        errors.append(
            f"registry row {row.get('ticker', '<unknown>')!r}: enrolled_at must be "
            f"a date or strict YYYY-MM-DD string, got {row['enrolled_at']!r}"
        )

    if "filing_trigger_profile" in row and row["filing_trigger_profile"] not in _FILING_TRIGGER_PROFILES:
        errors.append(
            f"registry row {row.get('ticker', '<unknown>')!r}: filing_trigger_profile "
            f"must be exactly one of {sorted(_FILING_TRIGGER_PROFILES)}, got "
            f"{row['filing_trigger_profile']!r}"
        )

    if "monitoring_enabled" in row and not isinstance(row["monitoring_enabled"], bool):
        errors.append(
            f"registry row {row.get('ticker', '<unknown>')!r}: monitoring_enabled "
            f"must be bool exactly, got {row['monitoring_enabled']!r} "
            f"({type(row['monitoring_enabled']).__name__})"
        )


# ── channel object schema ───────────────────────────────────────────────────

def _validate_channel_object(
    channel_key: str, value: object, ticker: str, errors: list[str]
) -> None:
    if value is None:
        return
    if not isinstance(value, dict):
        errors.append(
            f"checkpoint row {ticker!r}: channel {channel_key!r} must be a mapping "
            f"or null, got {type(value).__name__}"
        )
        return

    missing = _CHANNEL_REQUIRED_KEYS - value.keys()
    if missing:
        errors.append(
            f"checkpoint row {ticker!r}: channel {channel_key!r} missing required "
            f"key(s): {sorted(missing)}"
        )
        return

    if value["channel_name"] != channel_key:
        errors.append(
            f"checkpoint row {ticker!r}: channel {channel_key!r} has "
            f"channel_name {value['channel_name']!r}, which must exactly equal "
            f"its parent mapping key"
        )

    expected_form = _CHANNEL_OFFICIAL_FORM_TYPE.get(channel_key)
    if expected_form is not None and value["official_form_type"] != expected_form:
        errors.append(
            f"checkpoint row {ticker!r}: channel {channel_key!r} official_form_type "
            f"must be {expected_form!r}, got {value['official_form_type']!r}"
        )

    for key in ("stable_source_id", "incorporation_reference"):
        if not _is_non_empty_str(value[key]):
            errors.append(
                f"checkpoint row {ticker!r}: channel {channel_key!r}: {key!r} must "
                f"be a non-empty string, got {value[key]!r}"
            )

    if not _is_valid_local_date(value["official_source_date"]):
        errors.append(
            f"checkpoint row {ticker!r}: channel {channel_key!r}: "
            f"official_source_date must be a date or strict YYYY-MM-DD string, "
            f"got {value['official_source_date']!r}"
        )

    fp = value["fiscal_period"]
    if fp is not None and not isinstance(fp, str):
        errors.append(
            f"checkpoint row {ticker!r}: channel {channel_key!r}: fiscal_period "
            f"must be null or a string, got {fp!r} ({type(fp).__name__})"
        )


# ── checkpoint row schema ───────────────────────────────────────────────────

def _validate_checkpoint_row(row: dict, errors: list[str]) -> None:
    ticker = row.get("ticker", "<unknown>")

    missing = _CHECKPOINT_ROW_REQUIRED_KEYS - row.keys()
    if missing:
        errors.append(f"checkpoint row {ticker!r} missing required key(s): {sorted(missing)}")

    if "ticker" in row and not _is_non_empty_str(row["ticker"]):
        errors.append(f"checkpoint row {ticker!r}: ticker must be a non-empty string, got {row['ticker']!r}")

    if "checkpoint_status" in row and row["checkpoint_status"] not in _CHECKPOINT_STATUSES:
        errors.append(
            f"checkpoint row {ticker!r}: checkpoint_status must be exactly one of "
            f"{sorted(_CHECKPOINT_STATUSES)}, got {row['checkpoint_status']!r}"
        )

    if "established_by" in row:
        eb = row["established_by"]
        if eb is not None and not _is_non_empty_str(eb):
            errors.append(
                f"checkpoint row {ticker!r}: established_by must be null or a "
                f"non-empty string, got {eb!r}"
            )

    if "channels" not in row:
        return
    channels = row["channels"]
    if not isinstance(channels, dict):
        errors.append(f"checkpoint row {ticker!r}: channels must be a mapping, got {type(channels).__name__}")
        return

    # Determine which profile universe applies for per-channel-name/
    # official_form_type validation. A channel keyed outside either
    # universe is still validated on its own object shape, but its name
    # can't be checked against a profile-specific literal.
    known_names = set(_DOMESTIC_CHANNELS) | set(_FPI_CHANNELS)
    for channel_key, channel_value in channels.items():
        if channel_key in known_names:
            _validate_channel_object(channel_key, channel_value, ticker, errors)
        else:
            # Not one of the two closed profile universes at all — still
            # validate structurally where possible, using its own key as
            # the expected channel_name (form-type check is skipped since
            # there is no known mapping for an unrecognized channel name).
            if channel_value is not None:
                if not isinstance(channel_value, dict):
                    errors.append(
                        f"checkpoint row {ticker!r}: channel {channel_key!r} must be "
                        f"a mapping or null, got {type(channel_value).__name__}"
                    )
                else:
                    missing_ch = _CHANNEL_REQUIRED_KEYS - channel_value.keys()
                    if missing_ch:
                        errors.append(
                            f"checkpoint row {ticker!r}: channel {channel_key!r} "
                            f"missing required key(s): {sorted(missing_ch)}"
                        )


def _verified_channel_requirements(row: dict, profile: str | None, errors: list[str]) -> None:
    """AUTO-0002 Decision §1 verified-checkpoint rules, restated from spec
    §4.1(6)/§5's FPI earnings_release nullable-value case. Only meaningful
    once the ticker's registry-side filing_trigger_profile is known — the
    caller supplies it via the merged view built during cross-file
    validation."""
    ticker = row.get("ticker", "<unknown>")
    if row.get("checkpoint_status") != "verified":
        return
    if profile not in _PROFILE_CHANNELS:
        # Profile itself is invalid/unknown — already reported by the
        # registry row check; nothing further to check here.
        return

    channels = row.get("channels")
    if not isinstance(channels, dict):
        return  # already reported by _validate_checkpoint_row

    required_names = set(_PROFILE_CHANNELS[profile])
    actual_keys = set(channels.keys())
    if actual_keys != required_names:
        errors.append(
            f"checkpoint row {ticker!r}: verified checkpoint's channel key set must "
            f"equal exactly {sorted(required_names)} for profile {profile!r}, got "
            f"{sorted(actual_keys)}"
        )

    nullable_names = {"earnings_release"} if profile == "foreign_private_issuer_v1" else set()

    for name in required_names & actual_keys:
        value = channels[name]
        if value is None:
            if name not in nullable_names:
                errors.append(
                    f"checkpoint row {ticker!r}: verified checkpoint's channel "
                    f"{name!r} must not be null for profile {profile!r}"
                )
            continue
        # Non-null value: completeness is already checked by
        # _validate_checkpoint_row's per-channel-object validation.


# ── cross-file invariants ───────────────────────────────────────────────────

def _validate_cross_file_invariants(
    registry_tickers: list[dict], checkpoint_tickers: list[dict], errors: list[str]
) -> None:
    registry_by_ticker: dict[str, dict] = {}
    for row in registry_tickers:
        if not isinstance(row, dict):
            continue
        t = row.get("ticker")
        if not isinstance(t, str):
            continue
        if t in registry_by_ticker:
            errors.append(f"duplicate ticker row in registry: {t!r}")
        else:
            registry_by_ticker[t] = row

    checkpoint_by_ticker: dict[str, dict] = {}
    for row in checkpoint_tickers:
        if not isinstance(row, dict):
            continue
        t = row.get("ticker")
        if not isinstance(t, str):
            continue
        if t in checkpoint_by_ticker:
            errors.append(f"duplicate ticker row in checkpoints: {t!r}")
        else:
            checkpoint_by_ticker[t] = row

    registry_set = set(registry_by_ticker.keys())
    checkpoint_set = set(checkpoint_by_ticker.keys())

    orphan_registry = registry_set - checkpoint_set
    for t in sorted(orphan_registry):
        errors.append(f"ticker {t!r} has a registry row but no checkpoint row")

    orphan_checkpoint = checkpoint_set - registry_set
    for t in sorted(orphan_checkpoint):
        errors.append(f"ticker {t!r} has a checkpoint row but no registry row")

    common = registry_set & checkpoint_set

    for t in sorted(common):
        reg_row = registry_by_ticker[t]
        chk_row = checkpoint_by_ticker[t]

        if reg_row.get("monitoring_enabled") is True and chk_row.get("checkpoint_status") == "pending":
            errors.append(
                f"ticker {t!r}: monitoring_enabled is true while checkpoint_status "
                f"is pending — invalid combination"
            )

        profile = reg_row.get("filing_trigger_profile")
        _verified_channel_requirements(chk_row, profile, errors)

        channels = chk_row.get("channels")
        if isinstance(channels, dict) and profile in _PROFILE_CHANNELS:
            allowed = set(_PROFILE_CHANNELS[profile])
            for channel_key, channel_value in channels.items():
                if channel_value is None:
                    continue
                if channel_key not in allowed:
                    errors.append(
                        f"ticker {t!r}: channel {channel_key!r} is not valid for "
                        f"filing_trigger_profile {profile!r}"
                    )

    # Duplicate stable_source_id claimed under two different tickers.
    source_id_owners: dict[str, str] = {}
    for t in sorted(common):
        channels = checkpoint_by_ticker[t].get("channels")
        if not isinstance(channels, dict):
            continue
        for channel_value in channels.values():
            if not isinstance(channel_value, dict):
                continue
            sid = channel_value.get("stable_source_id")
            if not isinstance(sid, str) or not sid.strip():
                continue
            prior_owner = source_id_owners.get(sid)
            if prior_owner is not None and prior_owner != t:
                errors.append(
                    f"stable_source_id {sid!r} is claimed under two different "
                    f"tickers: {prior_owner!r} and {t!r}"
                )
            else:
                source_id_owners[sid] = t


# ── public API ─────────────────────────────────────────────────────────────

def validate_registry_and_checkpoints(
    registry_data: object, checkpoints_data: object
) -> ValidationResult:
    """Validate the two complete, already-parsed documents together,
    enforcing both files' own schemas and all six AUTO-0002 cross-file
    invariants. Never touches the filesystem."""
    errors: list[str] = []

    registry_doc = _validate_top_level_document(registry_data, errors)
    checkpoints_doc = _validate_top_level_document(checkpoints_data, errors)

    registry_tickers: list[dict] = []
    if registry_doc is not None and isinstance(registry_doc.get("tickers"), list):
        for row in registry_doc["tickers"]:
            if isinstance(row, dict):
                _validate_registry_row(row, errors)
                registry_tickers.append(row)

    checkpoint_tickers: list[dict] = []
    if checkpoints_doc is not None and isinstance(checkpoints_doc.get("tickers"), list):
        for row in checkpoints_doc["tickers"]:
            if isinstance(row, dict):
                _validate_checkpoint_row(row, errors)
                checkpoint_tickers.append(row)

    if registry_doc is not None and checkpoints_doc is not None:
        _validate_cross_file_invariants(registry_tickers, checkpoint_tickers, errors)

    return ValidationResult(valid=not errors, errors=errors)


def validate_registry_and_checkpoints_files(
    registry_path: str | Path, checkpoints_path: str | Path
) -> ValidationResult:
    """Read and validate the two files from disk. Read-only — opens each
    file in text mode for reading only, never write/append/update."""
    errors: list[str] = []
    parsed: dict[str, object] = {}

    for label, path in (("registry", Path(registry_path)), ("checkpoints", Path(checkpoints_path))):
        try:
            text = path.read_text()
        except OSError as exc:
            errors.append(f"could not read {label} file {path}: {exc}")
            parsed[label] = None
            continue
        try:
            data = yaml.safe_load(text)
        except yaml.YAMLError as exc:
            errors.append(f"invalid YAML in {label} file {path}: {exc}")
            parsed[label] = None
            continue
        if data is None:
            errors.append(f"{label} file {path} is empty")
            parsed[label] = None
            continue
        parsed[label] = data

    if errors:
        return ValidationResult(valid=False, errors=errors)

    return validate_registry_and_checkpoints(parsed["registry"], parsed["checkpoints"])


if __name__ == "__main__":
    import sys

    _repo_root = Path(__file__).resolve().parent
    _result = validate_registry_and_checkpoints_files(
        _repo_root / "intelligence" / "freshness_registry.yaml",
        _repo_root / "intelligence" / "freshness_checkpoints.yaml",
    )
    if _result.valid:
        print("freshness_validator: OK")
        sys.exit(0)
    else:
        print("freshness_validator: FAILED")
        for _err in _result.errors:
            print(f"  - {_err}")
        sys.exit(1)
