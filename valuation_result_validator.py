"""valuation_result_validator.py -- closed-schema validator for the
roster-agnostic Stage-4 valuation-result companion architecture governed by
`governance/decisions/VALUATION-0006-stage4-methodology-application-policy-
and-result-architecture.md`, authorized for this one implementation PR by
VALUATION-0006 SS A.

Scope, exactly what is validated:

- Source-of-truth convention (VALUATION-0006 SS B): `intelligence/
  valuation_results/<TICKER>.yaml`, one file per equity, single-file (no
  paired Markdown -- structured quantitative output, matching the
  classification/etf_classification/crypto_classification/
  valuation_archetype/valuation_evidence convention), filesystem is the
  index, plus one `COHORT_MANIFEST.yaml`.
- **Roster-agnostic by design (SS B): no closed/authorized population is
  enforced here** -- matching `valuation_evidence_validator.py`'s own
  design precedent, not `valuation_archetype_validator.py`'s fixed 27-name
  cohort. A future execution-authorization decision (VALUATION-0006 SS L's
  own final bullet) may opt into a cohort-completeness check via
  `validate_authorized_cohort()`, mirroring
  `valuation_evidence_validator.validate_authorized_cohort()`'s exact
  design (missing/extra-ticker check only).
- **Zero real-company population (SS A/SS S, absolute).** This module is a
  schema/validator/test scaffold only. No `intelligence/valuation_
  results/` directory, `COHORT_MANIFEST.yaml`, or per-ticker record is
  created anywhere in this repository by this implementation -- the
  directory does not exist on disk, which
  `validate_valuation_results_directory()` treats as a valid, zero-
  coverage state, matching every prior Intelligence validator's own
  filesystem-as-index doctrine.
- **A dedicated module, deliberately NOT an extension of
  `valuation_evidence_validator.py`**, which remains evidence-only and
  must continue to reject valuation-output content per its own design
  (VALUATION-0006 SS A).
- **One-way, hash-pinned references only** (SS K.3/K.4, SS L): a result
  record cites its already-sealed `valuation_archetype` and `valuation_
  evidence` records by `{source_file, content_sha256}` -- the referenced
  content hashes are **independently recomputed**, never merely trusted,
  via read-only calls to `valuation_archetype_validator.
  canonical_record_hash()` and `valuation_evidence_validator.
  canonical_record_hash()`. A hash mismatch is a hard validation failure.
  Ticker identity across all three records (result/archetype/evidence)
  must agree.
- **Archetype/methodology compatibility mechanically enforced** (SS M): a
  fixed, closed mapping table transcribing `VALUATION-0002` SS2's own
  unedited per-family governed-role table (seven families x seven
  archetypes) -- a `methodology_families_applied` entry whose declared
  `governed_role` does not match what the table independently produces
  for the ticker's own pinned `primary_archetype`, or whose governed role
  is Prohibited/Insufficient basis for adoption, is a hard validation
  failure, never merely discouraged by prose. If the pinned archetype
  record itself abstained (`primary_archetype ==
  unable_to_determine_archetype`), no family may be applied and
  `result_status` must be `unable_to_determine`.
- **Terminal-growth hard rule, strict inequality** (SS C item 9, SS E,
  SS L): within one family's `assumptions_ledger`, an entry named
  `terminal_growth` and an entry named `applicable_discount_rate` are the
  two recognized markers this rule watches for -- `terminal_growth >=
  applicable_discount_rate` is a hard validation failure at any populated
  precision, including exact equality. This is the one hard,
  mathematically-necessary rule in this schema.
- **Range-not-point, per family** (SS K.7, SS L): every standard family
  (all but family 7) requires `{low, base, high}`, all populated numbers,
  `low <= base <= high` -- a single-point range is rejected. Family 7
  (scenario/probability-weighted) instead requires a non-empty
  `scenario_outcomes[]` list -- the explicit, disclosed exception path for
  a range with no single "base" -- and forbids `low`/`base`/`high`.
- **Peer-set and scenario subset rules, mechanically enforced** (SS C
  items 10-13, SS F, SS G, SS L): `applied_peers` (family 5 only) must be
  a subset of the pinned evidence record's own `peer_set_evidence.
  candidates[]` with `inclusion_status: included`; every
  `scenario_outcomes[].scenario_name` (family 7 only) must appear among
  the pinned evidence record's own `scenario_evidence.scenarios[].
  scenario_name`. Family 5 may reach `family_status: completed` only with
  at least two applied peers (SS C item 11's two-peer minimum). Scenario
  probability-weight coherence (SS C item 13): when every scenario
  outcome in an applied set carries a `probability_weight`, the weights
  must sum within a disclosed +/-0.02 tolerance of 1.0, unless the family
  entry discloses `scenario_set_is_exhaustive: false`.
- **Mandatory, per-family, provenance-labeled assumptions ledger** (SS
  C item 2/K.8): every `assumptions_ledger` entry requires exactly one of
  `VALUATION-0002` SS3's four labels (`market_derived`,
  `historically_observed`, `analyst_consensus_cited`,
  `assumed_for_illustration`) -- reused, not reinvented.
- **Conflict propagation, live cross-checked** (SS C item 16, SS L):
  `conflicts_carried_forward` must be non-empty whenever a required
  evidence domain for an applied family carries a domain-level
  `abstention_reason`, or a non-empty `disclosed_conflicts` list anywhere
  within that domain's own subtree in the pinned evidence record -- a
  live recomputation against the pinned evidence file, never a
  self-declared flag alone, learning directly from
  `reconciliation_validator.py`'s own disclosed MINOR defense-in-depth
  gap. A family whose required domain(s) carry a material bearing
  conflict/abstention may not reach `family_status: completed` (SS I).
- **The closed, three-value `result_status` vocabulary and its exact
  triggering conditions** (SS J): `completed` / `partial` /
  `unable_to_determine`, mechanically cross-checked against the actual
  family-level data rather than trusted as a self-declared summary --
  `abstention_reason` required (non-empty) whenever not `completed`,
  structurally absent when `completed`.
- **`cross_asset_handoff` envelope, read-only-projection consistency**
  (SS K.15, SS L): every summary field checked against its own source
  field elsewhere in the record, never independently computed -- the
  identical discipline `recommendation_validator.py`'s own SS G.6
  live-recompute rule and every subsequent cross-asset-handoff-bearing
  schema in this program already applies.
- Closed schema at every level (envelope, family entry, valuation_range,
  each assumptions-ledger entry, each conflicts_carried_forward entry,
  cross_asset_handoff, the manifest) -- reject extra keys, not merely
  missing ones, learning directly from this repository's own disclosed
  `contender_registry_validator.py` MAJOR finding.
- **Rejects any fair-value/price-target/expected-return/opaque-score
  output field structurally forbidden by SS K**, plus equity-
  classification/ETF/crypto/archetype-layer field-name leakage, plus a
  numeric score/rank/target-key scan, plus an independent free-text scan
  for prohibited recommendation-shaped phrases, chart-domain terminology,
  and word-boundary-matched directive/trading language (`buy`, `sell`,
  `add`, `hold`, `trim`, `exit`, `wait`, `stage`, so "holdings" never
  false-positives on "hold") -- built as its own materially different
  mechanism from any strip/redaction logic elsewhere (there is none in
  this module; it is a pure read-only scan), never the same function
  called twice, per `TIER-0004`'s own corrected lesson on false
  independence claims.
- Zero coupling of any kind to `targets.yaml`, `holdings.yaml`,
  `gates.yaml`, `issuer_lookthrough.yaml`, `allocate.py`, or
  `margin_state.py` -- zero import, zero field.
- Deterministic hashing (`canonical_record_hash`) excludes only the five
  seal fields, matching every prior validator's identical convention.

**Disclosed reconciliation, VALUATION-0006 SS K item 2 vs item 16.**
SS K item 2 names a `governing_decision` **list** ("Governing authority: a
`governing_decision` list citing this decision and, once it exists, the
future execution-authorization decision"). SS K item 16 separately names
`governing_decision` as a **seal field** ("matching the existing
seal-field naming convention"), i.e. a single string, matching every
sibling validator's own `_SEAL_REQUIRED_KEYS`/`canonical_record_hash()`
exclusion set exactly. A literal reading would collide two same-named,
differently-shaped top-level keys. This implementation resolves the
collision the smallest way that preserves both requirements and matches
established convention: item 2's list is named `governing_decisions`
(plural) and item 16's seal field keeps the singular `governing_decision`
name, identical in shape and role to every sibling validator's own seal
field. No authority is invented by this naming choice -- both fields'
substance (a list of authorizing decisions; a single seal-field decision
ID) is exactly what SS K's own text describes.

This module is a validator, not a data producer. It never opens a file in
write/append/update mode, never creates a directory, and has zero import
relationship with `allocate.py` or `margin_state.py` in either direction.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from hashlib import sha256
from pathlib import Path

import yaml

import valuation_archetype_validator as _archetype_mod
import valuation_evidence_validator as _evidence_mod

SCHEMA_VERSION = "1.0"
ASSET_CLASS = "equity"
GOVERNING_DECISION_DEFAULT = "VALUATION-0006"

# ── closed vocabularies ─────────────────────────────────────────────────

_FAMILY_IDS = frozenset({
    "family_1_asset_based_sotp",
    "family_2_fcff_dcf",
    "family_3_fcfe_dcf",
    "family_4_earnings_fcf_yield",
    "family_5_relative_valuation",
    "family_6_roic_reinvestment",
    "family_7_scenario_probability_weighted",
})
_SCENARIO_FAMILY_ID = "family_7_scenario_probability_weighted"
_RELATIVE_VALUATION_FAMILY_ID = "family_5_relative_valuation"

_GOVERNED_ROLES = frozenset({
    "primary_candidate",
    "secondary_corroborative",
    "adjustment_required",
    "prohibited",
    "insufficient_basis_for_adoption",
})
_APPLICABLE_GOVERNED_ROLES = frozenset({
    "primary_candidate", "secondary_corroborative", "adjustment_required",
})

_ARCHETYPE_LETTERS = frozenset({"A", "B", "C", "D", "E", "F", "G"})
_ARCHETYPE_ABSTENTION = "unable_to_determine_archetype"

_FAMILY_STATUSES = frozenset({"completed", "partial", "unable_to_determine"})
_RESULT_STATUSES = frozenset({"completed", "partial", "unable_to_determine"})

_ASSUMPTION_PROVENANCE_LABELS = frozenset({
    "market_derived", "historically_observed", "analyst_consensus_cited", "assumed_for_illustration",
})

_PEER_INCLUSION_STATUS_INCLUDED = "included"

_EVIDENCE_DOMAIN_NAMES = (
    "financial_evidence", "segment_evidence", "market_observed_evidence",
    "discount_rate_evidence", "peer_set_evidence", "scenario_evidence",
)
_ACCESS_STATUS_VALUES = frozenset({
    "directly_inspected", "consulted_via_search_aggregation", "attempted_not_directly_inspected",
})

_CONFLICT_POINTER_TYPES = frozenset({"disclosed_conflict", "domain_abstention"})

# ── VALUATION-0002 SS2's per-family governed-role table -- transcribed,
# never re-derived, from the report's own frozen 49-cell matrix ─────────

_GOVERNED_ROLE_TABLE: dict[str, dict[str, str]] = {
    "family_1_asset_based_sotp": {
        "A": "prohibited", "G": "prohibited",
        "B": "adjustment_required", "C": "adjustment_required",
        "D": "adjustment_required", "E": "adjustment_required",
        "F": "primary_candidate",
    },
    "family_2_fcff_dcf": {
        "A": "primary_candidate", "G": "primary_candidate",
        "B": "adjustment_required", "D": "adjustment_required", "F": "adjustment_required",
        "C": "prohibited", "E": "prohibited",
    },
    "family_3_fcfe_dcf": {
        "A": "primary_candidate", "G": "primary_candidate",
        "B": "adjustment_required", "C": "adjustment_required",
        "D": "adjustment_required", "F": "adjustment_required",
        "E": "prohibited",
    },
    "family_4_earnings_fcf_yield": {
        "G": "secondary_corroborative",
        "A": "adjustment_required", "B": "adjustment_required", "C": "adjustment_required",
        "D": "adjustment_required", "F": "adjustment_required",
        "E": "prohibited",
    },
    "family_5_relative_valuation": {
        "A": "primary_candidate", "B": "primary_candidate",
        "G": "secondary_corroborative",
        "C": "adjustment_required", "D": "adjustment_required",
        "E": "adjustment_required", "F": "adjustment_required",
    },
    "family_6_roic_reinvestment": {
        "B": "secondary_corroborative", "G": "secondary_corroborative",
        "A": "adjustment_required", "C": "adjustment_required",
        "D": "adjustment_required", "F": "adjustment_required",
        "E": "prohibited",
    },
    "family_7_scenario_probability_weighted": {
        "D": "primary_candidate", "E": "primary_candidate",
        "A": "adjustment_required", "B": "adjustment_required", "C": "adjustment_required",
        "F": "adjustment_required", "G": "adjustment_required",
    },
}

for _fam in _FAMILY_IDS:
    assert set(_GOVERNED_ROLE_TABLE[_fam].keys()) == _ARCHETYPE_LETTERS, _fam  # noqa: S101


def governed_role_for(family_id: str, archetype_letter: str) -> str | None:
    """Live lookup against the transcribed VALUATION-0002 SS2 table. Returns
    None if the family_id/archetype_letter pairing is not a recognized
    combination (e.g. archetype abstention) -- callers treat None as "no
    family may be applied"."""
    table = _GOVERNED_ROLE_TABLE.get(family_id)
    if table is None:
        return None
    return table.get(archetype_letter)


# ── methodology family -> required evidence domain(s), for the conflict-
# propagation live cross-check (SS L) -- mirrors valuation_evidence_
# validator.py's own _METHODOLOGY_FAMILY_REQUIRED_DOMAINS naming/shape,
# translated to this module's own family_id vocabulary. ─────────────────

_FAMILY_REQUIRED_EVIDENCE_DOMAINS: dict[str, frozenset[str]] = {
    "family_1_asset_based_sotp": frozenset({"financial_evidence", "segment_evidence"}),
    "family_2_fcff_dcf": frozenset({"financial_evidence", "discount_rate_evidence"}),
    "family_3_fcfe_dcf": frozenset({"financial_evidence", "discount_rate_evidence"}),
    "family_4_earnings_fcf_yield": frozenset({"financial_evidence"}),
    "family_5_relative_valuation": frozenset({"financial_evidence", "peer_set_evidence"}),
    "family_6_roic_reinvestment": frozenset({"financial_evidence"}),
    "family_7_scenario_probability_weighted": frozenset({"financial_evidence", "scenario_evidence"}),
}

_PROBABILITY_SUM_TOLERANCE = 0.02
_MIN_APPLIED_PEERS_FOR_COMPLETED = 2

# ── seal / envelope shape ────────────────────────────────────────────────

_SEAL_REQUIRED_KEYS = frozenset({
    "sealed_at", "governing_decision", "drafting_session_or_shard_id",
    "content_sha256", "cohort_manifest_entry",
})
_RECORD_STATUSES = frozenset({"draft", "sealed"})

_REFERENCE_KEYS = frozenset({"source_file", "content_sha256"})

_CROSS_ASSET_HANDOFF_KEYS = frozenset({
    "ticker", "asset_class", "result_status", "family_summary", "evidence_quality_summary_echo",
})
_FAMILY_SUMMARY_ENTRY_KEYS = frozenset({"family_id", "governed_role", "family_status"})

_EVIDENCE_QUALITY_SUMMARY_KEYS = frozenset({
    "access_status_values_present", "domain_abstentions_echoed",
})

_CONFLICT_ENTRY_KEYS = frozenset({"domain", "pointer_type", "pointer_note"})

_ASSUMPTION_ENTRY_KEYS = frozenset({
    "assumption_name", "value", "provenance_label", "source_or_derivation_note",
})
_ASSUMPTION_ENTRY_REQUIRED_KEYS = _ASSUMPTION_ENTRY_KEYS

_SCENARIO_OUTCOME_KEYS = frozenset({
    "scenario_name", "value", "probability_weight", "probability_weight_provenance_label",
})
_SCENARIO_OUTCOME_REQUIRED_KEYS = frozenset({"scenario_name", "value"})

_VALUATION_RANGE_KEYS = frozenset({
    "low", "base", "high", "scenario_outcomes", "unit_and_basis",
    "governing_sensitivity", "scenario_set_is_exhaustive",
})

_FAMILY_ENTRY_KEYS = frozenset({
    "family_id", "governed_role", "family_status", "valuation_range",
    "assumptions_ledger", "applied_peers",
})
_FAMILY_ENTRY_REQUIRED_KEYS = frozenset({"family_id", "governed_role", "family_status"})

_ENVELOPE_ONLY_KEYS = frozenset({
    "schema_version", "ticker", "asset_class", "governing_decisions",
    "archetype_reference", "evidence_reference", "as_of_date",
    "methodology_families_applied", "sensitivity_disclosure",
    "uncertainty_summary", "evidence_quality_summary", "conflicts_carried_forward",
    "result_status", "abstention_reason", "cross_asset_handoff", "record_status",
})
_ALL_TOP_LEVEL_KEYS = frozenset({*_ENVELOPE_ONLY_KEYS, *_SEAL_REQUIRED_KEYS})

_HASHABLE_KEYS = tuple(sorted(_ENVELOPE_ONLY_KEYS))

_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def canonical_record_hash(data: dict) -> str:
    """SHA-256 of the record's full content (envelope fields only),
    canonical sorted-key JSON, UTF-8 -- excludes every seal field, matching
    every sibling validator's identical convention."""
    hashable = {k: data.get(k) for k in _HASHABLE_KEYS}
    canonical = json.dumps(hashable, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return sha256(canonical.encode("utf-8")).hexdigest()


# ── generic helpers ──────────────────────────────────────────────────────

def _non_empty_str(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _is_number(value: object) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def _valid_date(value: object) -> bool:
    return isinstance(value, str) and bool(_DATE_RE.match(value))


def _reject_unknown_keys(value: dict, field_name: str, allowed: frozenset[str], errors: list[str]) -> None:
    extra = set(value.keys()) - allowed
    if extra:
        errors.append(f"{field_name} has unrecognized key(s): {sorted(extra)}")


def _require_dict(value: object, field_name: str, errors: list[str]) -> bool:
    if not isinstance(value, dict):
        errors.append(f"{field_name} must be a mapping, got {type(value).__name__}")
        return False
    return True


# ── independent prohibited-content scan -- its own materially different
# mechanism from any strip/redaction logic; there is none in this module,
# it is a pure read-only scan, never the same function called twice
# (TIER-0004's own corrected false-independence lesson). ────────────────

_VALUATION_OUTPUT_LEAKAGE = frozenset({
    "fair_value", "price_target", "expected_return", "intrinsic_value",
    "computed_valuation", "recommended_value", "upside", "downside",
    "buy_price", "sell_price", "opaque_score", "composite_score",
    "blended_valuation", "final_number",
})
_EQUITY_CLASSIFICATION_LEAKAGE = frozenset({
    "portfolio_role_ref", "conviction", "economic_role", "capital_priority",
    "risk_concentration", "economic_system_ref",
})
_ETF_CRYPTO_LEAKAGE = frozenset({
    "structural_role", "constituent_exposure", "cost_and_tracking_quality",
    "structure_and_methodology", "network_fundamentals", "economic_model",
    "custody_and_counterparty_risk", "correlation_and_volatility",
    "regulatory_and_structural_uncertainty",
})
_NUMERIC_SCORE_LEAKAGE = frozenset({
    "target_pct", "target_range", "max_position_size", "maximum_position_size",
    "score", "rank", "ranking", "conviction_score", "recommended_target_pct", "weight",
})
_ALLOCATOR_COUPLING_LEAKAGE = frozenset({
    "target_weight", "destination_weight", "gate_status", "allow_add", "margin_state",
})
_FORBIDDEN_KEY_NAMES = frozenset({
    *_VALUATION_OUTPUT_LEAKAGE, *_EQUITY_CLASSIFICATION_LEAKAGE,
    *_ETF_CRYPTO_LEAKAGE, *_NUMERIC_SCORE_LEAKAGE, *_ALLOCATOR_COUPLING_LEAKAGE,
})


def _scan_forbidden_keys(value: object, path: str, errors: list[str]) -> None:
    if isinstance(value, dict):
        for k, v in value.items():
            key_str = str(k)
            if key_str in _FORBIDDEN_KEY_NAMES:
                if key_str in _VALUATION_OUTPUT_LEAKAGE:
                    kind = "an opaque fair-value/price-target/composite-score-shaped field"
                elif key_str in _EQUITY_CLASSIFICATION_LEAKAGE:
                    kind = "an equity-classification/archetype-layer-shaped field"
                elif key_str in _ETF_CRYPTO_LEAKAGE:
                    kind = "an ETF/crypto-classification-shaped field"
                elif key_str in _NUMERIC_SCORE_LEAKAGE:
                    kind = "a numeric score/rank/target-shaped field"
                else:
                    kind = "an allocator/margin-coupling-shaped field"
                errors.append(
                    f"{path}.{key_str}: forbidden key name -- {kind} must never appear in a "
                    f"valuation-result record (VALUATION-0006 SS K/SS L)"
                )
            _scan_forbidden_keys(v, f"{path}.{key_str}", errors)
    elif isinstance(value, list):
        for i, item in enumerate(value):
            _scan_forbidden_keys(item, f"{path}[{i}]", errors)


_RECOMMENDATION_SHAPED_PATTERNS = [
    re.compile(p, re.IGNORECASE) for p in (
        r"\bshould\s+be\s+(increased|decreased|raised|lowered|set)\s+to\b",
        r"\brecommend(?:ed|s|ing)?\s+(a\s+)?(target|weight|allocation|position\s+size)\s+of\b",
        r"\bnew\s+target\s+(pct|percent|percentage|range)\b",
        r"\bbuy\s+recommendation\b",
        r"\bsell\s+recommendation\b",
        r"\btrim\s+recommendation\b",
        r"\d+(?:\.\d+)?\s*%\s*(?:of\s+book|target|weight|allocation)",
        r"\bworth\s+(?:accumulating|buying|selling|reducing|trimming|adding\s+to)\b",
        r"\b(?:recommend(?:ed|s|ing)?|suggest(?:ed|s|ing)?)\s+(?:buying|selling|accumulating|"
        r"reducing|trimming|holding)\s+(?:the\s+|this\s+)?(?:position|shares?|stock|equity|exposure)\b",
        r"\bundervalued\b", r"\bovervalued\b",
    )
]

_DIRECTIVE_WORDS = ("buy", "sell", "add", "hold", "trim", "exit", "wait", "stage")
_DIRECTIVE_PATTERNS = [re.compile(rf"\b{w}\b", re.IGNORECASE) for w in _DIRECTIVE_WORDS]

_CHART_TERMS = (
    "support", "resistance", "breakout", "trend line", "trendline", "moving average",
    "rsi", "macd", "candlestick", "chart pattern", "technical analysis", "oversold",
    "overbought", "fibonacci", "volume profile", "price target", "momentum",
)


def _chart_pattern(term: str) -> re.Pattern:
    if " " in term:
        return re.compile(re.escape(term), re.IGNORECASE)
    return re.compile(rf"\b{re.escape(term)}\b", re.IGNORECASE)


_CHART_PATTERNS = [(t, _chart_pattern(t)) for t in _CHART_TERMS]


def _scan_free_text_strings(value: object, path: str, errors: list[str]) -> None:
    """Recursively scan every free-text string for prohibited
    recommendation-shaped phrases, chart-domain terminology, and
    word-boundary-matched directive/trading language."""
    if isinstance(value, dict):
        for k, v in value.items():
            _scan_free_text_strings(v, f"{path}.{k}", errors)
    elif isinstance(value, list):
        for i, item in enumerate(value):
            _scan_free_text_strings(item, f"{path}[{i}]", errors)
    elif isinstance(value, str):
        for pattern in _RECOMMENDATION_SHAPED_PATTERNS:
            if pattern.search(value):
                errors.append(f"{path}: contains forbidden recommendation-shaped phrase matching {pattern.pattern!r}")
        for pattern in _DIRECTIVE_PATTERNS:
            if pattern.search(value):
                errors.append(
                    f"{path}: contains directive word {pattern.pattern!r} -- no buy/sell/add/hold/"
                    f"trim/exit/wait/stage signal is permitted in any field, under any framing "
                    f"(VALUATION-0006 SS K)"
                )
        for term, pattern in _CHART_PATTERNS:
            if pattern.search(value):
                errors.append(
                    f"{path}: contains chart-derived terminology {term!r} -- no chart evidence of "
                    f"any kind is permitted (VALUATION-0006 SS H/SS K)"
                )


# ── assumptions ledger ───────────────────────────────────────────────────

def _validate_assumption_entry(value: object, path: str, errors: list[str]) -> dict | None:
    if not _require_dict(value, path, errors):
        return None
    value = value  # type: dict
    missing = _ASSUMPTION_ENTRY_REQUIRED_KEYS - value.keys()
    if missing:
        errors.append(f"{path} missing required key(s): {sorted(missing)}")
    _reject_unknown_keys(value, path, _ASSUMPTION_ENTRY_KEYS, errors)
    if not _non_empty_str(value.get("assumption_name")):
        errors.append(f"{path}.assumption_name must be a non-empty string")
    if not _is_number(value.get("value")):
        errors.append(f"{path}.value must be a number")
    label = value.get("provenance_label")
    if label not in _ASSUMPTION_PROVENANCE_LABELS:
        errors.append(
            f"{path}.provenance_label must be one of {sorted(_ASSUMPTION_PROVENANCE_LABELS)} "
            f"(VALUATION-0002 SS3) -- got {label!r}"
        )
    if not _non_empty_str(value.get("source_or_derivation_note")):
        errors.append(f"{path}.source_or_derivation_note must be a non-empty string")
    return value if not missing else None


def _validate_assumptions_ledger(value: object, path: str, errors: list[str]) -> list[dict]:
    if value is None:
        return []
    if not isinstance(value, list):
        errors.append(f"{path} must be a list")
        return []
    entries: list[dict] = []
    for i, item in enumerate(value):
        v = _validate_assumption_entry(item, f"{path}[{i}]", errors)
        if v is not None:
            entries.append(v)
    return entries


def _check_terminal_growth_hard_rule(ledger: list[dict], path: str, errors: list[str]) -> None:
    """VALUATION-0006 SS C item 9 / SS E / SS L: within one family's own
    assumptions_ledger, if an entry named 'terminal_growth' and an entry
    named 'applicable_discount_rate' are both present, terminal_growth
    must be strictly less than applicable_discount_rate -- g < r, never
    g <= r, at any populated precision including exact equality."""
    terminal_growth = None
    discount_rate = None
    for entry in ledger:
        name = entry.get("assumption_name")
        val = entry.get("value")
        if name == "terminal_growth" and _is_number(val):
            terminal_growth = val
        elif name == "applicable_discount_rate" and _is_number(val):
            discount_rate = val
    if terminal_growth is not None and discount_rate is not None:
        if terminal_growth >= discount_rate:
            errors.append(
                f"{path}: terminal_growth ({terminal_growth!r}) must be strictly less than "
                f"applicable_discount_rate ({discount_rate!r}) -- g < r is a mathematical "
                f"necessity of the perpetuity-growth model, equality is not a permitted boundary "
                f"case (VALUATION-0006 SS E/SS L)"
            )


# ── valuation_range ──────────────────────────────────────────────────────

def _validate_scenario_outcome(value: object, path: str, errors: list[str]) -> dict | None:
    if not _require_dict(value, path, errors):
        return None
    value = value  # type: dict
    missing = _SCENARIO_OUTCOME_REQUIRED_KEYS - value.keys()
    if missing:
        errors.append(f"{path} missing required key(s): {sorted(missing)}")
    _reject_unknown_keys(value, path, _SCENARIO_OUTCOME_KEYS, errors)
    if not _non_empty_str(value.get("scenario_name")):
        errors.append(f"{path}.scenario_name must be a non-empty string")
    if not _is_number(value.get("value")):
        errors.append(f"{path}.value must be a number")
    weight = value.get("probability_weight")
    weight_label = value.get("probability_weight_provenance_label")
    if weight is not None:
        if not _is_number(weight):
            errors.append(f"{path}.probability_weight must be a number when present")
        if weight_label not in _ASSUMPTION_PROVENANCE_LABELS:
            errors.append(
                f"{path}.probability_weight_provenance_label must be one of "
                f"{sorted(_ASSUMPTION_PROVENANCE_LABELS)} (VALUATION-0002 SS3, SS G) when "
                f"probability_weight is populated -- got {weight_label!r}"
            )
    elif weight_label is not None:
        errors.append(f"{path}.probability_weight_provenance_label must be absent unless probability_weight is present")
    return value if not missing else None


def _validate_valuation_range(
    value: object, family_id: str, family_status: str, path: str, errors: list[str],
) -> dict | None:
    if family_status == "unable_to_determine":
        if value is not None:
            errors.append(f"{path} must be absent/null when family_status is 'unable_to_determine'")
        return None
    if not _require_dict(value, path, errors):
        return None
    value = value  # type: dict
    _reject_unknown_keys(value, path, _VALUATION_RANGE_KEYS, errors)

    if not _non_empty_str(value.get("unit_and_basis")):
        errors.append(f"{path}.unit_and_basis must be a non-empty string (VALUATION-0006 SS K.7)")
    if not _non_empty_str(value.get("governing_sensitivity")):
        errors.append(f"{path}.governing_sensitivity must be a non-empty string (VALUATION-0006 SS J)")

    is_scenario = family_id == _SCENARIO_FAMILY_ID
    has_point_fields = any(k in value for k in ("low", "base", "high"))
    has_scenario_outcomes = "scenario_outcomes" in value

    if is_scenario:
        if has_point_fields:
            errors.append(f"{path}: family 7 (scenario/probability-weighted) must not carry low/base/high -- use scenario_outcomes[] (VALUATION-0006 SS K.7)")
        outcomes = value.get("scenario_outcomes")
        if not isinstance(outcomes, list) or not outcomes:
            errors.append(f"{path}.scenario_outcomes must be a non-empty list for family 7")
            outcomes = []
        parsed_outcomes = []
        for i, o in enumerate(outcomes):
            v = _validate_scenario_outcome(o, f"{path}.scenario_outcomes[{i}]", errors)
            if v is not None:
                parsed_outcomes.append(v)

        exhaustive = value.get("scenario_set_is_exhaustive")
        if not isinstance(exhaustive, bool):
            errors.append(f"{path}.scenario_set_is_exhaustive must be a boolean (VALUATION-0006 SS G)")

        weights = [o.get("probability_weight") for o in parsed_outcomes]
        if parsed_outcomes and all(_is_number(w) for w in weights) and isinstance(exhaustive, bool) and exhaustive:
            total = sum(weights)
            if abs(total - 1.0) > _PROBABILITY_SUM_TOLERANCE:
                errors.append(
                    f"{path}: scenario_outcomes probability_weight values sum to {total!r}, "
                    f"outside the disclosed +/-{_PROBABILITY_SUM_TOLERANCE} tolerance of 1.0, and "
                    f"scenario_set_is_exhaustive is true (VALUATION-0006 SS C item 13/SS G)"
                )
        value["_parsed_scenario_outcomes"] = parsed_outcomes
    else:
        if has_scenario_outcomes:
            errors.append(f"{path}: only family 7 may carry scenario_outcomes -- {family_id!r} must use low/base/high")
        low, base, high = value.get("low"), value.get("base"), value.get("high")
        for name, v in (("low", low), ("base", base), ("high", high)):
            if not _is_number(v):
                errors.append(f"{path}.{name} must be a number -- a single point is never a valid range (VALUATION-0006 SS K.7)")
        if _is_number(low) and _is_number(base) and _is_number(high):
            if not (low <= base <= high):
                errors.append(f"{path}: low ({low!r}) <= base ({base!r}) <= high ({high!r}) is required")
        if "scenario_set_is_exhaustive" in value:
            errors.append(f"{path}.scenario_set_is_exhaustive must be absent unless family_id is {_SCENARIO_FAMILY_ID!r}")

    return value


# ── conflicts_carried_forward ────────────────────────────────────────────

def _validate_conflicts_carried_forward(value: object, errors: list[str]) -> list[dict]:
    if value is None:
        return []
    if not isinstance(value, list):
        errors.append("conflicts_carried_forward must be a list")
        return []
    entries: list[dict] = []
    for i, item in enumerate(value):
        path = f"conflicts_carried_forward[{i}]"
        if not _require_dict(item, path, errors):
            continue
        item = item  # type: dict
        missing = _CONFLICT_ENTRY_KEYS - item.keys()
        if missing:
            errors.append(f"{path} missing required key(s): {sorted(missing)}")
            continue
        _reject_unknown_keys(item, path, _CONFLICT_ENTRY_KEYS, errors)
        if item.get("domain") not in _EVIDENCE_DOMAIN_NAMES:
            errors.append(f"{path}.domain must be one of {sorted(_EVIDENCE_DOMAIN_NAMES)}")
        if item.get("pointer_type") not in _CONFLICT_POINTER_TYPES:
            errors.append(f"{path}.pointer_type must be one of {sorted(_CONFLICT_POINTER_TYPES)}")
        if not _non_empty_str(item.get("pointer_note")):
            errors.append(f"{path}.pointer_note must be a non-empty string -- a structured pointer, never a restatement of the referenced content's own text (VALUATION-0006 SS J)")
        else:
            entries.append(item)
    return entries


# ── live cross-checks against the pinned evidence record ────────────────

def _domain_has_disclosed_conflicts(node: object) -> bool:
    """Recursive scan of one evidence-domain subtree for any non-empty
    disclosed_conflicts list anywhere within it."""
    if isinstance(node, dict):
        dc = node.get("disclosed_conflicts")
        if isinstance(dc, list) and dc:
            return True
        return any(_domain_has_disclosed_conflicts(v) for v in node.values())
    if isinstance(node, list):
        return any(_domain_has_disclosed_conflicts(item) for item in node)
    return False


def _domains_bearing_on_family(family_id: str, evidence_data: dict) -> set[str]:
    """Live recompute (never a self-declared flag) of which of a family's
    required evidence domains carry a domain-level abstention_reason or a
    disclosed_conflicts entry anywhere within their own subtree in the
    pinned evidence record."""
    required = _FAMILY_REQUIRED_EVIDENCE_DOMAINS.get(family_id, frozenset())
    bearing: set[str] = set()
    for domain in required:
        node = evidence_data.get(domain)
        if not isinstance(node, dict):
            continue
        if _non_empty_str(node.get("abstention_reason")):
            bearing.add(domain)
        elif _domain_has_disclosed_conflicts(node):
            bearing.add(domain)
    return bearing


def _included_peer_identities(evidence_data: dict) -> set[str]:
    peer_evidence = evidence_data.get("peer_set_evidence")
    if not isinstance(peer_evidence, dict):
        return set()
    candidates = peer_evidence.get("candidates")
    if not isinstance(candidates, list):
        return set()
    return {
        c.get("identity")
        for c in candidates
        if isinstance(c, dict) and c.get("inclusion_status") == _PEER_INCLUSION_STATUS_INCLUDED
        and _non_empty_str(c.get("identity"))
    }


def _named_scenarios(evidence_data: dict) -> set[str]:
    scenario_evidence = evidence_data.get("scenario_evidence")
    if not isinstance(scenario_evidence, dict):
        return set()
    scenarios = scenario_evidence.get("scenarios")
    if not isinstance(scenarios, list):
        return set()
    return {
        s.get("scenario_name")
        for s in scenarios
        if isinstance(s, dict) and _non_empty_str(s.get("scenario_name"))
    }


# ── family entries ───────────────────────────────────────────────────────

def _validate_family_entry(
    value: object, path: str, errors: list[str], *,
    archetype_letter: str | None, evidence_data: dict | None,
) -> dict | None:
    if not _require_dict(value, path, errors):
        return None
    value = value  # type: dict
    missing = _FAMILY_ENTRY_REQUIRED_KEYS - value.keys()
    if missing:
        errors.append(f"{path} missing required key(s): {sorted(missing)}")
        return None
    _reject_unknown_keys(value, path, _FAMILY_ENTRY_KEYS, errors)

    family_id = value.get("family_id")
    if family_id not in _FAMILY_IDS:
        errors.append(f"{path}.family_id must be one of {sorted(_FAMILY_IDS)} -- got {family_id!r}")
        family_id = None

    governed_role = value.get("governed_role")
    if governed_role not in _GOVERNED_ROLES:
        errors.append(f"{path}.governed_role must be one of {sorted(_GOVERNED_ROLES)} -- got {governed_role!r}")

    family_status = value.get("family_status")
    if family_status not in _FAMILY_STATUSES:
        errors.append(f"{path}.family_status must be one of {sorted(_FAMILY_STATUSES)} -- got {family_status!r}")
        family_status = None

    # SS M: mechanical, live compatibility cross-check against the
    # transcribed VALUATION-0002 SS2 table -- never trust a self-declared
    # governed_role string alone, and a Prohibited/Insufficient-basis
    # family (or a role that does not match the table) is a hard failure.
    if family_id is not None and archetype_letter is not None:
        expected_role = governed_role_for(family_id, archetype_letter)
        if expected_role is None:
            errors.append(
                f"{path}: no governed-role table entry for family {family_id!r} against archetype "
                f"{archetype_letter!r} (archetype may be abstained -- SS J: no family may be "
                f"applied when the pinned archetype record itself abstained)"
            )
        elif expected_role not in _APPLICABLE_GOVERNED_ROLES:
            errors.append(
                f"{path}: family {family_id!r} is {expected_role!r} for archetype "
                f"{archetype_letter!r} under VALUATION-0002 SS2's own governed-role table -- a "
                f"Prohibited or Insufficient-basis family may never appear in "
                f"methodology_families_applied (VALUATION-0006 SS M)"
            )
        elif governed_role is not None and governed_role != expected_role:
            errors.append(
                f"{path}.governed_role ({governed_role!r}) does not match the value the "
                f"VALUATION-0002 SS2 table independently produces for family {family_id!r} / "
                f"archetype {archetype_letter!r} ({expected_role!r}) -- never trust a "
                f"self-declared governed_role string alone (VALUATION-0006 SS L)"
            )

    range_value = _validate_valuation_range(
        value.get("valuation_range"), family_id or "<unknown>", family_status or "unable_to_determine",
        f"{path}.valuation_range", errors,
    )

    ledger = _validate_assumptions_ledger(value.get("assumptions_ledger"), f"{path}.assumptions_ledger", errors)
    if family_id is not None:
        _check_terminal_growth_hard_rule(ledger, f"{path}.assumptions_ledger", errors)

    applied_peers = value.get("applied_peers")
    if family_id == _RELATIVE_VALUATION_FAMILY_ID:
        if applied_peers is None:
            applied_peers = []
        if not isinstance(applied_peers, list):
            errors.append(f"{path}.applied_peers must be a list for family 5 (relative valuation)")
            applied_peers = []
        for i, p in enumerate(applied_peers):
            if not _non_empty_str(p):
                errors.append(f"{path}.applied_peers[{i}] must be a non-empty string")
        if evidence_data is not None:
            included = _included_peer_identities(evidence_data)
            invented = {p for p in applied_peers if _non_empty_str(p)} - included
            if invented:
                errors.append(
                    f"{path}.applied_peers contains peer(s) not present among the pinned evidence "
                    f"record's own included candidates: {sorted(invented)} -- an applied set may "
                    f"only be a subset of Stage-3-sourced candidates, never a superset "
                    f"(VALUATION-0006 SS F/SS L)"
                )
        valid_peer_count = len({p for p in applied_peers if _non_empty_str(p)})
        if family_status == "completed" and valid_peer_count < _MIN_APPLIED_PEERS_FOR_COMPLETED:
            errors.append(
                f"{path}: family 5 (relative valuation) requires at least "
                f"{_MIN_APPLIED_PEERS_FOR_COMPLETED} applied peers to reach family_status: "
                f"completed -- got {valid_peer_count} (VALUATION-0006 SS C item 11/SS F)"
            )
    elif applied_peers is not None:
        errors.append(f"{path}.applied_peers must be absent unless family_id is {_RELATIVE_VALUATION_FAMILY_ID!r}")

    # SS G/SS L: every scenario_outcomes[].scenario_name must be a subset
    # of the pinned evidence record's own named scenarios.
    if family_id == _SCENARIO_FAMILY_ID and evidence_data is not None and isinstance(range_value, dict):
        named = _named_scenarios(evidence_data)
        parsed_outcomes = range_value.get("_parsed_scenario_outcomes", [])
        invented_scenarios = {
            o.get("scenario_name") for o in parsed_outcomes
            if _non_empty_str(o.get("scenario_name")) and o.get("scenario_name") not in named
        }
        if invented_scenarios:
            errors.append(
                f"{path}.valuation_range.scenario_outcomes references scenario name(s) not "
                f"present among the pinned evidence record's own named scenarios: "
                f"{sorted(invented_scenarios)} -- inventing a new scenario at execution time is "
                f"prohibited (VALUATION-0006 SS G/SS L)"
            )

    # SS I/SS L: a family whose required evidence domain(s) carry a
    # material bearing conflict/abstention may not reach 'completed', and
    # that domain must appear in conflicts_carried_forward (checked by the
    # caller, which has the full record's conflicts_carried_forward list).
    bearing_domains: set[str] = set()
    if family_id is not None and evidence_data is not None:
        bearing_domains = _domains_bearing_on_family(family_id, evidence_data)
        if bearing_domains and family_status == "completed":
            errors.append(
                f"{path}: family_status may not be 'completed' -- required evidence domain(s) "
                f"{sorted(bearing_domains)} carry a material bearing conflict or abstention in "
                f"the pinned evidence record (VALUATION-0006 SS I)"
            )

    if range_value is not None and "_parsed_scenario_outcomes" in range_value:
        del range_value["_parsed_scenario_outcomes"]

    return {
        "family_id": family_id, "governed_role": governed_role, "family_status": family_status,
        "bearing_domains": bearing_domains,
    }


# ── record_status / result_status (SS J) ─────────────────────────────────

def _validate_result_status(
    data: dict, family_results: list[dict], archetype_abstained: bool, errors: list[str],
) -> None:
    result_status = data.get("result_status")
    if result_status not in _RESULT_STATUSES:
        errors.append(f"result_status must be one of {sorted(_RESULT_STATUSES)} -- got {result_status!r}")
        return

    abstention_reason = data.get("abstention_reason")
    if result_status == "completed":
        if abstention_reason is not None:
            errors.append("abstention_reason must be absent when result_status is 'completed'")
    else:
        if not _non_empty_str(abstention_reason):
            errors.append(f"abstention_reason is required and non-empty when result_status is {result_status!r} (VALUATION-0006 SS J)")

    if archetype_abstained:
        if data.get("methodology_families_applied"):
            errors.append("methodology_families_applied must be empty when the pinned archetype record itself abstained (primary_archetype: unable_to_determine_archetype) -- SS J")
        if result_status != "unable_to_determine":
            errors.append("result_status must be 'unable_to_determine' when the pinned archetype record itself abstained -- SS J")
        return

    has_completed_qualifying_family = any(
        f["governed_role"] in _APPLICABLE_GOVERNED_ROLES - {"adjustment_required"}
        and f["family_status"] == "completed"
        for f in family_results
    )
    has_attempted_family = any(f["family_status"] in ("completed", "partial") for f in family_results)

    if result_status == "completed" and not has_completed_qualifying_family:
        errors.append(
            "result_status is 'completed' but no applied family has governed_role in "
            "{primary_candidate, secondary_corroborative} and family_status: completed "
            "(VALUATION-0006 SS J)"
        )
    if result_status != "completed" and has_completed_qualifying_family:
        errors.append(
            "result_status is not 'completed' but at least one applied family already reaches "
            "the completed bar (governed_role in {primary_candidate, secondary_corroborative}, "
            "family_status: completed) -- result_status should be 'completed' (VALUATION-0006 SS J)"
        )
    if result_status == "unable_to_determine" and has_attempted_family:
        errors.append(
            "result_status is 'unable_to_determine' but at least one applied family reached "
            "family_status 'completed' or 'partial' -- a family was attempted, so 'partial' (not "
            "'unable_to_determine') is the correct status unless the completed bar was reached "
            "(VALUATION-0006 SS J)"
        )
    if result_status == "partial" and not has_attempted_family:
        errors.append(
            "result_status is 'partial' but no applied family reached family_status 'completed' "
            "or 'partial' -- 'unable_to_determine' is the correct status when no family produced "
            "even a partial range (VALUATION-0006 SS J)"
        )


# ── evidence_quality_summary (SS K.11) -- projection, never invented ────

def _true_access_status_values(evidence_data: dict) -> set[str]:
    found: set[str] = set()

    def _walk(node: object) -> None:
        if isinstance(node, dict):
            v = node.get("access_status")
            if v in _ACCESS_STATUS_VALUES:
                found.add(v)
            for val in node.values():
                _walk(val)
        elif isinstance(node, list):
            for item in node:
                _walk(item)

    _walk(evidence_data)
    return found


def _true_domain_abstentions(evidence_data: dict) -> set[str]:
    return {
        d for d in _EVIDENCE_DOMAIN_NAMES
        if isinstance(evidence_data.get(d), dict) and _non_empty_str(evidence_data[d].get("abstention_reason"))
    }


def _validate_evidence_quality_summary(value: object, evidence_data: dict | None, errors: list[str]) -> None:
    if not _require_dict(value, "evidence_quality_summary", errors):
        return
    value = value  # type: dict
    missing = _EVIDENCE_QUALITY_SUMMARY_KEYS - value.keys()
    if missing:
        errors.append(f"evidence_quality_summary missing key(s): {sorted(missing)}")
        return
    _reject_unknown_keys(value, "evidence_quality_summary", _EVIDENCE_QUALITY_SUMMARY_KEYS, errors)

    access = value.get("access_status_values_present")
    if not isinstance(access, list) or any(a not in _ACCESS_STATUS_VALUES for a in access):
        errors.append(f"evidence_quality_summary.access_status_values_present must be a list drawn from {sorted(_ACCESS_STATUS_VALUES)}")
        access = []

    abstentions = value.get("domain_abstentions_echoed")
    if not isinstance(abstentions, list) or any(a not in _EVIDENCE_DOMAIN_NAMES for a in abstentions):
        errors.append(f"evidence_quality_summary.domain_abstentions_echoed must be a list drawn from {sorted(_EVIDENCE_DOMAIN_NAMES)}")
        abstentions = []

    if evidence_data is not None:
        true_access = _true_access_status_values(evidence_data)
        if set(access) != true_access:
            errors.append(
                f"evidence_quality_summary.access_status_values_present ({sorted(set(access))}) "
                f"does not match the set independently recomputed from the pinned evidence record "
                f"({sorted(true_access)}) -- a projection, never a newly invented value "
                f"(VALUATION-0006 SS K.11)"
            )
        true_abstentions = _true_domain_abstentions(evidence_data)
        if set(abstentions) != true_abstentions:
            errors.append(
                f"evidence_quality_summary.domain_abstentions_echoed ({sorted(set(abstentions))}) "
                f"does not match the set independently recomputed from the pinned evidence "
                f"record's own domain-level abstentions ({sorted(true_abstentions)})"
            )


# ── cross_asset_handoff (SS K.15) -- read-only-projection consistency ───

def _validate_cross_asset_handoff(data: dict, family_results: list[dict], errors: list[str]) -> None:
    value = data.get("cross_asset_handoff")
    if not _require_dict(value, "cross_asset_handoff", errors):
        return
    value = value  # type: dict
    missing = _CROSS_ASSET_HANDOFF_KEYS - value.keys()
    if missing:
        errors.append(f"cross_asset_handoff missing key(s): {sorted(missing)}")
        return
    _reject_unknown_keys(value, "cross_asset_handoff", _CROSS_ASSET_HANDOFF_KEYS, errors)

    if value.get("ticker") != data.get("ticker"):
        errors.append("cross_asset_handoff.ticker must echo the record's own ticker exactly")
    if value.get("asset_class") != data.get("asset_class"):
        errors.append("cross_asset_handoff.asset_class must echo the record's own asset_class exactly")
    if value.get("result_status") != data.get("result_status"):
        errors.append("cross_asset_handoff.result_status must echo the record's own result_status exactly")

    summary = value.get("family_summary")
    if not isinstance(summary, list):
        errors.append("cross_asset_handoff.family_summary must be a list")
        summary = []
    expected_summary = [
        {"family_id": f["family_id"], "governed_role": f["governed_role"], "family_status": f["family_status"]}
        for f in family_results
    ]
    for i, entry in enumerate(summary):
        path = f"cross_asset_handoff.family_summary[{i}]"
        if not isinstance(entry, dict) or (_FAMILY_SUMMARY_ENTRY_KEYS - entry.keys()) or (set(entry.keys()) - _FAMILY_SUMMARY_ENTRY_KEYS):
            errors.append(f"{path} must be a mapping with exactly keys {sorted(_FAMILY_SUMMARY_ENTRY_KEYS)}")
    if summary != expected_summary:
        errors.append(
            "cross_asset_handoff.family_summary does not echo methodology_families_applied "
            "exactly (family_id/governed_role/family_status, same order) -- a read-only "
            "projection, never independently computed (VALUATION-0006 SS L)"
        )

    echo = value.get("evidence_quality_summary_echo")
    if echo != data.get("evidence_quality_summary"):
        errors.append("cross_asset_handoff.evidence_quality_summary_echo must echo evidence_quality_summary exactly")


# ── references (archetype_reference / evidence_reference), SS K.3/K.4 ───

def _validate_reference(
    value: object, field_name: str, expected_source_prefix: str, errors: list[str],
) -> str | None:
    """Structural validation only -- returns the declared content_sha256 (or
    None on structural failure) for the caller's own live hash-recompute
    cross-check, which requires the referenced record's own parsed data."""
    if not _require_dict(value, field_name, errors):
        return None
    value = value  # type: dict
    missing = _REFERENCE_KEYS - value.keys()
    if missing:
        errors.append(f"{field_name} missing required key(s): {sorted(missing)}")
    _reject_unknown_keys(value, field_name, _REFERENCE_KEYS, errors)
    source_file = value.get("source_file")
    if not _non_empty_str(source_file):
        errors.append(f"{field_name}.source_file must be a non-empty string")
    elif not source_file.startswith(expected_source_prefix):
        errors.append(f"{field_name}.source_file must live under {expected_source_prefix!r} -- got {source_file!r}")
    digest = value.get("content_sha256")
    if not _non_empty_str(digest):
        errors.append(f"{field_name}.content_sha256 must be a non-empty string")
        return None
    return digest


# ── seal ──────────────────────────────────────────────────────────────────

def _validate_seal(data: dict, errors: list[str]) -> None:
    status = data.get("record_status")
    if status not in _RECORD_STATUSES:
        errors.append(f"record_status must be one of {sorted(_RECORD_STATUSES)} -- got {status!r}")
        return
    if status == "draft":
        return

    missing = _SEAL_REQUIRED_KEYS - data.keys()
    if missing:
        errors.append(f"sealed record missing required seal field(s): {sorted(missing)}")
        return

    for k in ("sealed_at", "governing_decision", "drafting_session_or_shard_id", "cohort_manifest_entry"):
        if not _non_empty_str(data.get(k)):
            errors.append(f"{k} must be a non-empty string")

    recorded_hash = data.get("content_sha256")
    if not _non_empty_str(recorded_hash):
        errors.append("content_sha256 must be a non-empty string")
    else:
        expected = canonical_record_hash(data)
        if recorded_hash != expected:
            errors.append(f"content_sha256 does not reproduce -- recorded {recorded_hash!r}, recomputed {expected!r}")


def _validate_no_stray_top_level_fields(data: dict, errors: list[str]) -> None:
    stray = set(data.keys()) - _ALL_TOP_LEVEL_KEYS
    if stray:
        errors.append(
            f"record contains unexpected top-level field(s) {sorted(stray)} -- exactly the "
            f"envelope and seal fields are permitted (VALUATION-0006 SS K)"
        )


# ── public API: in-memory record validation ──────────────────────────────

@dataclass
class ValidationResult:
    valid: bool
    errors: list[str] = field(default_factory=list)
    source: str | None = None


@dataclass
class DirectoryValidationResult:
    """A missing or empty directory is a valid, zero-coverage state -- the
    same filesystem-as-index doctrine every prior Intelligence validator in
    this repository already applies. VALUATION-0006 SS A/SS S authorizes no
    real-company population, so this directory does not exist anywhere in
    this repository at this implementation's own head."""
    valid: bool
    results: list[ValidationResult] = field(default_factory=list)

    @property
    def record_count(self) -> int:
        return len(self.results)


def validate_result_data(
    data: object, *, archetype_data: dict | None = None, evidence_data: dict | None = None,
    source: str | None = None,
) -> ValidationResult:
    """Validate an already-parsed valuation-result mapping. Never touches
    the filesystem. `archetype_data`/`evidence_data` are the already-parsed
    contents of the referenced sealed archetype/evidence records --
    supplying them enables the full set of live cross-checks (hash
    recomputation, archetype/methodology compatibility, peer/scenario
    subset rules, conflict propagation, evidence-quality-summary
    recomputation); omitting either performs schema-only validation of the
    corresponding cross-checks and is intended for isolated schema tests
    only -- a real sealed record must always supply both."""
    errors: list[str] = []

    if not isinstance(data, dict):
        return ValidationResult(valid=False, errors=["record must be a mapping"], source=source)

    ticker = data.get("ticker")
    if not _non_empty_str(ticker):
        errors.append("ticker must be a non-empty string")

    if data.get("asset_class") != ASSET_CLASS:
        errors.append(f"asset_class must be exactly {ASSET_CLASS!r} -- got {data.get('asset_class')!r}")

    if data.get("schema_version") != SCHEMA_VERSION:
        errors.append(f"schema_version must be {SCHEMA_VERSION!r}, got {data.get('schema_version')!r}")

    governing_decisions = data.get("governing_decisions")
    if not isinstance(governing_decisions, list) or not governing_decisions or not all(_non_empty_str(g) for g in governing_decisions):
        errors.append("governing_decisions must be a non-empty list of non-empty strings (VALUATION-0006 SS K item 2)")
    elif GOVERNING_DECISION_DEFAULT not in governing_decisions:
        errors.append(f"governing_decisions must include {GOVERNING_DECISION_DEFAULT!r}")

    if not _valid_date(data.get("as_of_date")):
        errors.append("as_of_date must be a valid YYYY-MM-DD date (VALUATION-0006 SS K.5)")

    archetype_digest = _validate_reference(
        data.get("archetype_reference"), "archetype_reference", "intelligence/valuation_archetype/", errors,
    )
    evidence_digest = _validate_reference(
        data.get("evidence_reference"), "evidence_reference", "intelligence/valuation_evidence/", errors,
    )

    archetype_letter: str | None = None
    archetype_abstained = False
    if archetype_data is not None:
        if archetype_digest is not None:
            recomputed = _archetype_mod.canonical_record_hash(archetype_data)
            if archetype_digest != recomputed:
                errors.append(
                    f"archetype_reference.content_sha256 ({archetype_digest!r}) does not match "
                    f"the value independently recomputed from the referenced sealed archetype "
                    f"record ({recomputed!r}) -- a hash mismatch is a hard validation failure, "
                    f"never a warning (VALUATION-0006 SS L)"
                )
        if _non_empty_str(ticker) and archetype_data.get("ticker") != ticker:
            errors.append(
                f"archetype_reference points to a record for ticker {archetype_data.get('ticker')!r}, "
                f"which does not match this record's own ticker {ticker!r}"
            )
        primary = archetype_data.get("primary_archetype")
        if primary == _ARCHETYPE_ABSTENTION:
            archetype_abstained = True
        elif primary in _ARCHETYPE_LETTERS:
            archetype_letter = primary

    if evidence_data is not None:
        if evidence_digest is not None:
            recomputed = _evidence_mod.canonical_record_hash(evidence_data)
            if evidence_digest != recomputed:
                errors.append(
                    f"evidence_reference.content_sha256 ({evidence_digest!r}) does not match the "
                    f"value independently recomputed from the referenced sealed evidence record "
                    f"({recomputed!r}) -- a hash mismatch is a hard validation failure, never a "
                    f"warning (VALUATION-0006 SS L)"
                )
        if _non_empty_str(ticker) and evidence_data.get("ticker") != ticker:
            errors.append(
                f"evidence_reference points to a record for ticker {evidence_data.get('ticker')!r}, "
                f"which does not match this record's own ticker {ticker!r}"
            )

    families_raw = data.get("methodology_families_applied")
    if not isinstance(families_raw, list):
        errors.append("methodology_families_applied must be a list")
        families_raw = []

    family_results: list[dict] = []
    all_bearing_domains: set[str] = set()
    for i, entry in enumerate(families_raw):
        result = _validate_family_entry(
            entry, f"methodology_families_applied[{i}]", errors,
            archetype_letter=archetype_letter, evidence_data=evidence_data,
        )
        if result is not None and result["family_id"] is not None and result["governed_role"] is not None and result["family_status"] is not None:
            family_results.append(result)
            all_bearing_domains |= result.get("bearing_domains", set())

    conflicts = _validate_conflicts_carried_forward(data.get("conflicts_carried_forward"), errors)
    if evidence_data is not None and all_bearing_domains:
        carried_domains = {c["domain"] for c in conflicts}
        missing_domains = all_bearing_domains - carried_domains
        if missing_domains:
            errors.append(
                f"conflicts_carried_forward is missing (an) entry(ies) for domain(s) "
                f"{sorted(missing_domains)}, each of which carries a material bearing "
                f"conflict/abstention in the pinned evidence record for an applied family -- a "
                f"live cross-check, not a self-declared flag alone (VALUATION-0006 SS L)"
            )

    if not _non_empty_str(data.get("sensitivity_disclosure")):
        errors.append("sensitivity_disclosure must be a non-empty string (VALUATION-0006 SS J/SS K.9)")
    else:
        _scan_free_text_strings(data["sensitivity_disclosure"], "sensitivity_disclosure", errors)

    if not _non_empty_str(data.get("uncertainty_summary")):
        errors.append("uncertainty_summary must be a non-empty string (VALUATION-0006 SS K.10)")
    else:
        _scan_free_text_strings(data["uncertainty_summary"], "uncertainty_summary", errors)

    if "evidence_quality_summary" not in data:
        errors.append("record missing required field: evidence_quality_summary")
    else:
        _validate_evidence_quality_summary(data["evidence_quality_summary"], evidence_data, errors)

    _validate_result_status(data, family_results, archetype_abstained, errors)
    _validate_cross_asset_handoff(data, family_results, errors)
    _validate_no_stray_top_level_fields(data, errors)
    _validate_seal(data, errors)

    _scan_forbidden_keys(data, str(ticker) if _non_empty_str(ticker) else "<record>", errors)
    _scan_free_text_strings(data, str(ticker) if _non_empty_str(ticker) else "<record>", errors)

    return ValidationResult(valid=not errors, errors=errors, source=source)


# ── public API: file/directory validation ────────────────────────────────

def _read_yaml(path: Path) -> tuple[object, list[str]]:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        return None, [f"could not read file: {exc}"]
    try:
        data = yaml.safe_load(text)
    except yaml.YAMLError as exc:
        return None, [f"invalid YAML: {exc}"]
    if data is None:
        return None, ["file is empty"]
    return data, []


def validate_result_file(path: str | Path, repo_root: str | Path) -> ValidationResult:
    """Read one sealed result file plus its two referenced sealed records
    (resolved relative to `repo_root`) and perform full validation,
    including the live hash/compatibility/peer/scenario cross-checks."""
    path = Path(path)
    repo_root = Path(repo_root)
    source = str(path)
    data, errors = _read_yaml(path)
    if errors:
        return ValidationResult(valid=False, errors=errors, source=source)

    if isinstance(data, dict) and _non_empty_str(data.get("ticker")) and path.stem != data["ticker"]:
        return ValidationResult(
            valid=False,
            errors=[f"filename stem {path.stem!r} does not match the record's own ticker {data['ticker']!r}"],
            source=source,
        )

    archetype_data = None
    evidence_data = None
    if isinstance(data, dict):
        ref = data.get("archetype_reference")
        if isinstance(ref, dict) and _non_empty_str(ref.get("source_file")):
            archetype_data, read_errors = _read_yaml(repo_root / ref["source_file"])
            if read_errors or not isinstance(archetype_data, dict):
                archetype_data = None
        ref = data.get("evidence_reference")
        if isinstance(ref, dict) and _non_empty_str(ref.get("source_file")):
            evidence_data, read_errors = _read_yaml(repo_root / ref["source_file"])
            if read_errors or not isinstance(evidence_data, dict):
                evidence_data = None

    return validate_result_data(data, archetype_data=archetype_data, evidence_data=evidence_data, source=source)


_MANIFEST_FILENAME = "COHORT_MANIFEST.yaml"
_MANIFEST_REQUIRED_ROW_KEYS = frozenset({
    "ticker", "sealed_at", "content_sha256", "schema_version", "governing_decision", "record_path",
})
_MANIFEST_ROW_ALLOWED_KEYS = _MANIFEST_REQUIRED_ROW_KEYS
_MANIFEST_TOP_LEVEL_ALLOWED_KEYS = frozenset({"schema_version", "governing_decision", "cohort"})


def validate_cohort_manifest(manifest_data: object, records_by_ticker: dict[str, dict]) -> ValidationResult:
    """Internal consistency only -- no closed-population enforcement, since
    this schema is roster-agnostic by design (see module docstring, and
    VALUATION-0006 SS L's own final bullet, which defers any cohort scope
    to a future execution-authorization decision)."""
    errors: list[str] = []

    if not isinstance(manifest_data, dict) or not isinstance(manifest_data.get("cohort"), list):
        errors.append("cohort manifest must be a mapping with a 'cohort' list")
        return ValidationResult(valid=False, errors=errors, source=_MANIFEST_FILENAME)

    unknown_top = set(manifest_data.keys()) - _MANIFEST_TOP_LEVEL_ALLOWED_KEYS
    if unknown_top:
        errors.append(f"cohort manifest contains unexpected top-level key(s) {sorted(unknown_top)}")

    rows = manifest_data["cohort"]
    seen: set[str] = set()
    for i, row in enumerate(rows):
        if not isinstance(row, dict) or (_MANIFEST_REQUIRED_ROW_KEYS - row.keys()):
            missing = _MANIFEST_REQUIRED_ROW_KEYS - (row.keys() if isinstance(row, dict) else set())
            errors.append(f"cohort[{i}] missing required key(s): {sorted(missing)}")
            continue
        unknown_row = row.keys() - _MANIFEST_ROW_ALLOWED_KEYS
        if unknown_row:
            errors.append(f"cohort[{i}] contains unexpected key(s) {sorted(unknown_row)}")

        ticker = row["ticker"]
        if ticker in seen:
            errors.append(f"cohort manifest lists {ticker!r} more than once")
        seen.add(ticker)

        record = records_by_ticker.get(ticker)
        if record is None:
            errors.append(f"cohort[{i}] ticker {ticker!r} has no corresponding sealed record file")
            continue

        expected_hash = canonical_record_hash(record)
        if row["content_sha256"] != expected_hash:
            errors.append(f"cohort[{i}] ({ticker!r}) content_sha256 mismatch -- manifest {row['content_sha256']!r}, recomputed {expected_hash!r}")
        if record.get("content_sha256") != row["content_sha256"]:
            errors.append(f"cohort[{i}] ({ticker!r}) manifest content_sha256 does not match the record's own recorded content_sha256")

    orphans = set(records_by_ticker) - seen
    if orphans:
        errors.append(f"sealed record(s) exist with no corresponding cohort manifest entry: {sorted(orphans)}")

    return ValidationResult(valid=not errors, errors=errors, source=_MANIFEST_FILENAME)


def validate_authorized_cohort(
    records_by_ticker: dict[str, dict], authorized_population: frozenset[str],
) -> ValidationResult:
    """Mirrors `valuation_evidence_validator.validate_authorized_cohort()`
    exactly: for a specific authorized population, check exactly that
    population is present -- zero missing, zero extra. An
    `unable_to_determine` record still counts as present. Deliberately
    NOT folded into the schema-level validation, since this schema stays
    roster-agnostic (a future execution-authorization decision opts a
    caller into this check, it is never enforced unconditionally)."""
    errors: list[str] = []
    present = set(records_by_ticker)
    missing = authorized_population - present
    extra = present - authorized_population
    if missing:
        errors.append(f"authorized cohort missing ticker(s): {sorted(missing)}")
    if extra:
        errors.append(f"cohort contains ticker(s) outside the authorized population: {sorted(extra)}")
    return ValidationResult(valid=not errors, errors=errors, source="authorized_cohort")


def validate_valuation_results_directory(directory: str | Path, repo_root: str | Path | None = None) -> DirectoryValidationResult:
    """A missing or empty directory is a valid, zero-coverage state
    (VALUATION-0006 SS A/SS S: this implementation populates zero real
    tickers, so `intelligence/valuation_results/` does not exist anywhere
    in this repository at this implementation's own head)."""
    directory = Path(directory)
    if repo_root is None:
        repo_root = directory.parent.parent
    repo_root = Path(repo_root)

    if not directory.exists() or not directory.is_dir():
        return DirectoryValidationResult(valid=True, results=[])

    yaml_paths = sorted(p for p in directory.glob("*.yaml") if p.name != _MANIFEST_FILENAME)
    results = [validate_result_file(p, repo_root) for p in yaml_paths]

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
            results.append(validate_cohort_manifest(manifest_data, records_by_ticker))
    elif records_by_ticker:
        results.append(
            ValidationResult(
                valid=False,
                errors=[f"{_MANIFEST_FILENAME} is required whenever sealed records exist"],
                source=str(directory),
            )
        )

    return DirectoryValidationResult(valid=all(r.valid for r in results), results=results)


if __name__ == "__main__":
    import sys

    _repo_root = Path(__file__).resolve().parent
    _results_dir = _repo_root / "intelligence" / "valuation_results"
    _result = validate_valuation_results_directory(_results_dir, repo_root=_repo_root)

    if _result.valid:
        print(f"valuation_result_validator: OK ({_result.record_count} result(s))")
        sys.exit(0)
    else:
        print("valuation_result_validator: FAILED")
        for _r in _result.results:
            if not _r.valid:
                for _err in _r.errors:
                    print(f"  - [{_r.source}] {_err}")
        sys.exit(1)
