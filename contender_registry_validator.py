"""
contender_registry_validator.py — read-only schema and bidirectional-
reconciliation validator for `intelligence/contenders/registry.yaml`, the
structured half of the hybrid output authorized by
`governance/decisions/CONTENDER-0002-contender-normalization-and-readiness-screening-authorization.md`
(§I) under `WS-0014`'s first execution unit (`XASSET-0001` §J step 1 —
contender normalization plus research-readiness screening).

This module validates a governed SNAPSHOT, never investment-policy truth.
`targets.yaml`, `holdings.yaml`, `gates.yaml`, `issuer_lookthrough.yaml`, and
every existing Company/Theme/Relationship/Classification Intelligence record
remain sole authority for their own facts (CONTENDER-0002 §I) — this
validator only checks that the registry faithfully and consistently reports
what those sources already say.

Scope, exactly what CONTENDER-0002 authorizes this module to validate:

- §E.2: exactly one `primary_disposition` per entry, from the closed
  twelve-value vocabulary, in the exact mandatory precedence order defined
  there (the vocabulary is closed; precedence enforcement itself is a
  property of the *generator*, not re-derivable by a validator that only
  sees the finished entry — this module checks membership and single-
  valuedness, not that the generator applied the order correctly).
- §E.3: the eight-flag orthogonal `secondary_flags` schema — booleans only,
  no flag may silently introduce a disposition-shaped value.
- §E.6: required per-entry fields.
- §C: alias/duplicate integrity — every `duplicate_of` reference must
  resolve to a real entry in the same registry, and no canonical symbol may
  appear twice.
- §G: the legacy-gap record, when present, must carry every required key.
  `registry_entries_created` must be exactly 0 unless `recovery_status`
  is a `"recovered_<N>_of_41"`-shaped value, in which case it must equal
  that exact `N` — a real, collision-filtered count of genuinely NEW
  registry rows, never invented. A successful mechanical diff does not,
  by itself, guarantee `N > 0`: every legacy ticker the diff finds may
  already carry its own entry via another governed source, in which case
  the correct outcome is the fixed `"all_recovered_already_tracked"`
  value with `registry_entries_created: 0` — a genuine, clean success
  with zero new rows needed, distinct from `"recovery_ambiguous"` (the
  diff itself could not be resolved).
- §I: header provenance (`source_commit_sha`, `generated_at`) must be
  present; entry ordering must be deterministic (alphabetical by
  `canonical_symbol`).
- §J: bidirectional reconciliation between a supplied "discovered symbol"
  set (produced by the generator's own scan) and the registry — every
  discovered symbol lands in the registry or is named in a supplied
  exclusion set with a reason; every registry entry's `provenance` cites at
  least one of the sixteen (or seventeen, see the generator's own disclosed
  extension) authorized §B source labels.

This module is a validator, not a data producer. It never opens a file in
write/append/update mode. It carries zero import relationship with
`allocate.py` or `margin_state.py` in either direction (see
`test_contender_registry_validator.py`'s isolation tests), and the registry
it validates must never be read by, or coupled to, any allocator or
production decision path (CONTENDER-0002 §I) — it is inventory, not policy.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

import yaml

# ── §E.2: closed twelve-value primary-disposition vocabulary, mandatory
# precedence order (index 0 = highest precedence). The validator enforces
# membership and single-valuedness; the generator is responsible for
# actually applying this order when it assigns a disposition. ──────────────

PRIMARY_DISPOSITIONS_IN_PRECEDENCE_ORDER = (
    "synthetic_or_test_fixture",
    "benchmark_or_index",
    "non_investable",
    "duplicate_or_alias",
    "stale_or_superseded",
    "requires_identity_resolution",
    "explicitly_deferred_or_excluded",
    "abstain_pending_human_decision",
    "requires_research",
    "requires_freshness_review",
    "insufficient_evidence",
    "evaluation_ready",
)

PRIMARY_DISPOSITIONS = frozenset(PRIMARY_DISPOSITIONS_IN_PRECEDENCE_ORDER)
assert len(PRIMARY_DISPOSITIONS) == 12

# ── §E.3: eight orthogonal secondary factual-state flags. ──────────────────

SECONDARY_FLAG_KEYS = frozenset({
    "has_current_gate",
    "has_historical_intelligence",
    "has_prior_deferral_superseded",
    "freshness_due",
    "classification_exists",
    "chart_evidence_exists",
    "current_holding",
    "current_target",
})
assert len(SECONDARY_FLAG_KEYS) == 8

# ── §E.6: asset-type vocabulary — targets.yaml's own asset_class values,
# extended only as needed for non-investable/structural categories. ────────

ASSET_TYPES = frozenset({
    "equity", "fund", "crypto", "reserve", "cash",
    "benchmark", "fixture", "other",
})

# ── §G: clone-depth / legacy-gap recovery-status closed vocabularies.
# Defined here (the schema authority) rather than in
# contender_registry_generator.py, which imports these — the generator
# already imports PRIMARY_DISPOSITIONS_IN_PRECEDENCE_ORDER from this module,
# and defining these the other way around would create a circular import. ──

CLONE_DEPTH_VALUES = frozenset({"shallow", "complete"})

# §G's own YAML comment names three outcomes; this module recognizes four,
# reconciled against real behavior independently observed in this
# repository's own CI:
# - `unavailable_in_current_clone` (shallow — no attempt possible);
# - `recovery_ambiguous` (complete, but the reconciliation commit, a single
#   resolvable parent, or a non-empty diff could not be mechanically
#   established — §G step 3's own "stop and disclose" path);
# - `all_recovered_already_tracked` (complete, diff succeeded and found one
#   or more removed legacy tickers, but EVERY one already carries its own
#   entry via another governed source — a genuine, clean, successful
#   search that legitimately creates zero new rows; deliberately distinct
#   from `recovery_ambiguous`, which describes search *failure*, not
#   success-with-no-new-rows-needed);
# - a dynamic "recovered_<N>_of_41" shape (complete, diff succeeded, and
#   at least one genuinely NEW row was added — `N` is that filing's own
#   placeholder character for the real, collision-filtered count of NEW
#   rows, checked below via RECOVERED_STATUS_PATTERN, not a fixed string;
#   `N` counts new rows, not raw diff hits, which can legitimately differ).
# `perform_legacy_recovery()` (contender_registry_generator.py) ALWAYS
# attempts the §G step 2 diff whenever clone_depth == "complete" — there is
# no "reachable but not attempted" outcome in the current design.
RECOVERY_STATUS_VALUES = frozenset({
    "unavailable_in_current_clone",
    "recovery_ambiguous",
    "all_recovered_already_tracked",
})

# ── §B: the sixteen role-tagged source categories CONTENDER-0002 §B names,
# plus the generator's own disclosed 17th (CLAUDE.md) — see
# contender_registry_generator.py's SOURCE_CATALOG for the full citation
# text. A provenance entry's `source` must match one of these labels (the
# generator emits the exact label string; this validator only checks that
# an emitted label is one of the seventeen it knows about). ────────────────

AUTHORIZED_SOURCE_LABELS = frozenset({
    "targets.yaml",
    "gates.yaml",
    "holdings.yaml",
    "issuer_lookthrough.yaml",
    "intelligence/companies",
    "intelligence/themes",
    "intelligence/relationships",
    "intelligence/classification",
    "governance/decisions",
    "operations/WORKSTREAMS.yaml",
    "intelligence/BATCH_COMPARISON",
    "governance/audits",
    "decision_log.yaml",
    "research_protocols",
    "earnings.py",
    "governance/evidence/CHART-0002",
    "CLAUDE.md",
    "holdings.yaml (historical — CONTENDER-0002 §G step 2 recovery)",
})

_REQUIRED_ENTRY_KEYS = frozenset({
    "canonical_symbol",
    "asset_type",
    "primary_disposition",
    "secondary_flags",
    "provenance",
    "investability_status",
    "research_status",
    "evidence_freshness_status",
    "classification_status",
    "current_policy_status",
    "existing_disposition",
    "duplicate_of",
    "reason",
    "review_trigger",
    "next_required_action",
})

_REQUIRED_HEADER_KEYS = frozenset({
    "schema_version",
    "source_commit_sha",
    "generated_at",
    "governing_authority",
})

# The full top-level document also carries `entries` (required, checked via
# its own dedicated shape check) and `legacy_gap` (optional) — both are
# legitimate top-level keys, not "extra," when checking the document as a
# whole for unrecognized/policy-shaped content.
_TOP_LEVEL_ALLOWED_KEYS = _REQUIRED_HEADER_KEYS | frozenset({"entries", "legacy_gap"})

_REQUIRED_LEGACY_GAP_KEYS = frozenset({
    "known_unenumerated_legacy_gap", "reported_count", "source_authority",
    "clone_depth_at_generation", "recovery_status", "registry_entries_created", "next_action",
})

# §G step 2: when recovery succeeds, `recovery_status` takes the shape
# "recovered_<N>_of_41" (the literal template CONTENDER-0002 §G's own YAML
# comment shows, with `N` — that filing's own placeholder character —
# substituted for the real, mechanically-diffed count). This is checked as
# a pattern, not a closed value, precisely because `N` is not fixed.
RECOVERED_STATUS_PATTERN = re.compile(r"^recovered_(\d+)_of_41$")


@dataclass
class ValidationResult:
    """Report, not an agent — mirrors relationship_validator.py's
    ValidationResult / intelligence_validator.py's own contract."""
    valid: bool
    errors: list[str] = field(default_factory=list)
    source: str | None = None


@dataclass
class ReconciliationResult:
    """§J bidirectional-reconciliation outcome."""
    valid: bool
    errors: list[str] = field(default_factory=list)
    discovered_count: int = 0
    registered_count: int = 0
    excluded_with_reason_count: int = 0


def _err(errors: list[str], msg: str) -> None:
    errors.append(msg)


def _check_closed_keys(value: dict, allowed: frozenset[str], errors: list[str], where: str, cite: str) -> None:
    """Shared closed-schema check — missing AND extra keys both rejected,
    mirroring `_validate_secondary_flags`'s own pattern. A registry level
    that only checks `missing` silently accepts policy-shaped smuggled
    content (e.g. a `conviction_score`/`recommended_target_pct` key) —
    exactly what CONTENDER-0002 §M forbids this registry from ever
    carrying. Used for entry-level, header-level, and legacy_gap-level
    validation so the "closed schema" guarantee actually holds everywhere
    it is claimed, not only for secondary_flags."""
    missing = allowed - value.keys()
    extra = value.keys() - allowed
    if missing:
        _err(errors, f"{where} missing required key(s): {sorted(missing)} ({cite})")
    if extra:
        _err(
            errors,
            f"{where} has unrecognized/extra key(s): {sorted(extra)} — the registry schema is "
            f"closed, never a place for policy-shaped content ({cite})",
        )


def _validate_provenance(entries: object, errors: list[str], where: str) -> None:
    if not isinstance(entries, list) or not entries:
        _err(errors, f"{where}.provenance must be a non-empty list (CONTENDER-0002 §E.6)")
        return
    for i, p in enumerate(entries):
        if not isinstance(p, dict) or "source" not in p or "role" not in p:
            _err(errors, f"{where}.provenance[{i}] must be a mapping with 'source' and 'role' keys")
            continue
        if p["source"] not in AUTHORIZED_SOURCE_LABELS:
            _err(
                errors,
                f"{where}.provenance[{i}].source {p['source']!r} is not one of the authorized "
                f"CONTENDER-0002 §B source labels (no registry-only invented identity, §J)",
            )
        if p["role"] not in {"discovery", "corroboration", "context"}:
            _err(
                errors,
                f"{where}.provenance[{i}].role must be one of discovery/corroboration/context "
                f"(CONTENDER-0002 §B) — got {p['role']!r}",
            )


def _validate_secondary_flags(value: object, errors: list[str], where: str) -> None:
    if not isinstance(value, dict):
        _err(errors, f"{where}.secondary_flags must be a mapping (CONTENDER-0002 §E.3)")
        return
    missing = SECONDARY_FLAG_KEYS - value.keys()
    extra = value.keys() - SECONDARY_FLAG_KEYS
    if missing:
        _err(errors, f"{where}.secondary_flags missing required key(s): {sorted(missing)}")
    if extra:
        _err(errors, f"{where}.secondary_flags has unrecognized key(s): {sorted(extra)}")
    for k, v in value.items():
        if k in SECONDARY_FLAG_KEYS and not isinstance(v, bool):
            _err(
                errors,
                f"{where}.secondary_flags.{k} must be an explicit boolean, never a disposition "
                f"substitute (CONTENDER-0002 §E.3) — got {v!r}",
            )


def validate_entry(entry: object, *, known_symbols: frozenset[str] = frozenset()) -> ValidationResult:
    """Validate one already-parsed registry entry mapping. `known_symbols`,
    if supplied, is used to check that a `duplicate_of` reference resolves
    to a real entry elsewhere in the same registry (§C)."""
    errors: list[str] = []
    if not isinstance(entry, dict):
        return ValidationResult(valid=False, errors=[f"entry must be a mapping, got {type(entry).__name__}"])

    symbol = entry.get("canonical_symbol")
    where = f"entry[{symbol!r}]" if isinstance(symbol, str) else "entry[<unknown>]"

    _check_closed_keys(entry, _REQUIRED_ENTRY_KEYS, errors, where, "CONTENDER-0002 §E.6")

    if not isinstance(symbol, str) or not symbol.strip():
        _err(errors, f"{where}.canonical_symbol must be a non-empty string")

    asset_type = entry.get("asset_type")
    if asset_type not in ASSET_TYPES:
        _err(errors, f"{where}.asset_type must be one of {sorted(ASSET_TYPES)} — got {asset_type!r}")

    disposition = entry.get("primary_disposition")
    if disposition not in PRIMARY_DISPOSITIONS:
        _err(
            errors,
            f"{where}.primary_disposition must be exactly one of the closed twelve-value "
            f"CONTENDER-0002 §E.2 vocabulary {sorted(PRIMARY_DISPOSITIONS)} — got {disposition!r}",
        )

    if "secondary_flags" in entry:
        _validate_secondary_flags(entry["secondary_flags"], errors, where)

    if "provenance" in entry:
        _validate_provenance(entry["provenance"], errors, where)

    duplicate_of = entry.get("duplicate_of")
    if disposition == "duplicate_or_alias" and not duplicate_of:
        _err(errors, f"{where}: primary_disposition is duplicate_or_alias but duplicate_of is empty (§C)")
    if duplicate_of is not None and known_symbols and duplicate_of not in known_symbols:
        _err(
            errors,
            f"{where}.duplicate_of {duplicate_of!r} does not resolve to any canonical_symbol in "
            f"this registry (§C — no dangling alias reference)",
        )

    reason = entry.get("reason")
    if not isinstance(reason, str) or not reason.strip():
        _err(errors, f"{where}.reason must be a non-empty plain-text string (§E.6)")

    return ValidationResult(valid=not errors, errors=errors, source=symbol if isinstance(symbol, str) else None)


def validate_registry_data(data: object) -> ValidationResult:
    """Validate an already-parsed registry mapping. Never touches the
    filesystem. Checks the header, every entry, no-duplicate-canonical-
    symbol, deterministic alphabetical ordering, and the optional legacy-gap
    record's shape (§G)."""
    errors: list[str] = []
    if not isinstance(data, dict):
        return ValidationResult(valid=False, errors=[f"root document must be a mapping, got {type(data).__name__}"])

    missing_header = _REQUIRED_HEADER_KEYS - data.keys()
    if missing_header:
        _err(errors, f"registry header missing required key(s): {sorted(missing_header)} (§I)")
    extra_top_level = data.keys() - _TOP_LEVEL_ALLOWED_KEYS
    if extra_top_level:
        _err(
            errors,
            f"registry top-level document has unrecognized/extra key(s): {sorted(extra_top_level)} — "
            f"closed schema, never a place for policy-shaped content (§I/§M)",
        )

    entries = data.get("entries")
    if not isinstance(entries, list):
        _err(errors, "'entries' must be a list")
        entries = []

    symbols_seen: dict[str, int] = {}
    known_symbols = frozenset(
        e.get("canonical_symbol") for e in entries if isinstance(e, dict) and isinstance(e.get("canonical_symbol"), str)
    )

    entry_results: list[ValidationResult] = []
    for i, e in enumerate(entries):
        r = validate_entry(e, known_symbols=known_symbols)
        entry_results.append(r)
        if not r.valid:
            errors.extend(f"entries[{i}]: {msg}" for msg in r.errors)
        sym = e.get("canonical_symbol") if isinstance(e, dict) else None
        if isinstance(sym, str):
            symbols_seen[sym] = symbols_seen.get(sym, 0) + 1

    dupes = sorted(s for s, n in symbols_seen.items() if n > 1)
    if dupes:
        _err(errors, f"duplicate canonical_symbol entries found (no ticker may be inventoried twice): {dupes}")

    ordered = [e.get("canonical_symbol") for e in entries if isinstance(e, dict)]
    valid_ordered = [s for s in ordered if isinstance(s, str)]
    if valid_ordered != sorted(valid_ordered):
        _err(errors, "entries must be in deterministic alphabetical order by canonical_symbol (§I)")

    legacy_gap = data.get("legacy_gap")
    if legacy_gap is not None:
        if not isinstance(legacy_gap, dict):
            _err(errors, "'legacy_gap' must be a mapping when present (§G)")
        else:
            _check_closed_keys(legacy_gap, _REQUIRED_LEGACY_GAP_KEYS, errors, "legacy_gap", "§G")

            clone_depth = legacy_gap.get("clone_depth_at_generation")
            if clone_depth not in CLONE_DEPTH_VALUES:
                _err(
                    errors,
                    f"legacy_gap.clone_depth_at_generation must be one of {sorted(CLONE_DEPTH_VALUES)} "
                    f"(§G — live-detected, never assumed) — got {clone_depth!r}",
                )

            recovery_status = legacy_gap.get("recovery_status")
            recovered_match = RECOVERED_STATUS_PATTERN.match(recovery_status) if isinstance(recovery_status, str) else None
            if recovery_status not in RECOVERY_STATUS_VALUES and recovered_match is None:
                _err(
                    errors,
                    f"legacy_gap.recovery_status must be one of {sorted(RECOVERY_STATUS_VALUES)} or match "
                    f"the pattern {RECOVERED_STATUS_PATTERN.pattern!r} (§G) — got {recovery_status!r}",
                )

            entries_created = legacy_gap.get("registry_entries_created")
            if recovered_match is not None:
                expected_n = int(recovered_match.group(1))
                if entries_created != expected_n or expected_n <= 0:
                    _err(
                        errors,
                        f"legacy_gap.registry_entries_created ({entries_created!r}) must equal the "
                        f"recovered count named in recovery_status ({recovery_status!r} implies "
                        f"{expected_n}) and be greater than 0 — no invented count (§G)",
                    )
            elif entries_created != 0:
                _err(
                    errors,
                    "legacy_gap.registry_entries_created must be exactly 0 when recovery_status is not "
                    "a 'recovered_N_of_41'-shaped value — no invented placeholder rows for unrecovered "
                    "legacy tickers (§G)",
                )

    return ValidationResult(valid=not errors, errors=errors, source="intelligence/contenders/registry.yaml")


def reconcile(
    discovered_symbols: frozenset[str],
    registry_symbols: frozenset[str],
    excluded_with_reason: frozenset[str],
) -> ReconciliationResult:
    """§J bidirectional reconciliation, run separately from schema
    validation (it needs the generator's own discovered-symbol set, which
    is not itself part of the committed registry file). (a) every
    discovered symbol must be registered or explicitly excluded with a
    reason; (b) every registered symbol must trace to a discovered symbol
    (no registry-only invented identity)."""
    errors: list[str] = []

    unaccounted = discovered_symbols - registry_symbols - excluded_with_reason
    if unaccounted:
        _err(
            errors,
            f"discovered symbol(s) missing from both the registry and the audit's exclusion "
            f"record, with no disposition: {sorted(unaccounted)} (§J)",
        )

    invented = registry_symbols - discovered_symbols
    if invented:
        _err(
            errors,
            f"registry entry/entries cite no real §B provenance in the discovered set — "
            f"registry-only invented identity: {sorted(invented)} (§J)",
        )

    return ReconciliationResult(
        valid=not errors,
        errors=errors,
        discovered_count=len(discovered_symbols),
        registered_count=len(registry_symbols),
        excluded_with_reason_count=len(excluded_with_reason),
    )


def validate_registry_file(path: str | Path) -> ValidationResult:
    """Read-only. Opens the file in text mode for reading only."""
    path = Path(path)
    try:
        text = path.read_text()
    except OSError as exc:
        return ValidationResult(valid=False, errors=[f"could not read file: {exc}"], source=str(path))
    try:
        data = yaml.safe_load(text)
    except yaml.YAMLError as exc:
        return ValidationResult(valid=False, errors=[f"invalid YAML: {exc}"], source=str(path))
    if data is None:
        return ValidationResult(valid=False, errors=["file is empty"], source=str(path))
    result = validate_registry_data(data)
    result.source = str(path)
    return result


if __name__ == "__main__":
    import sys

    _repo_root = Path(__file__).resolve().parent
    _registry_path = _repo_root / "intelligence" / "contenders" / "registry.yaml"
    if not _registry_path.is_file():
        print("contender_registry_validator: OK (0 entries — registry not yet generated)")
        sys.exit(0)

    _result = validate_registry_file(_registry_path)
    if _result.valid:
        _data = yaml.safe_load(_registry_path.read_text())
        _n = len(_data.get("entries", []))
        print(f"contender_registry_validator: OK ({_n} entries)")
        sys.exit(0)
    else:
        print("contender_registry_validator: FAILED")
        for _e in _result.errors:
            print(f"  - {_e}")
        sys.exit(1)
