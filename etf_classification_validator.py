"""
etf_classification_validator.py -- read-only schema validator for the first
WS-0014 ETF blind-classification content batch (SPY, VEA, VWO, GLD),
authored against the ETF framework `governance/decisions/XASSET-0002-etf-
and-crypto-classification-framework-design.md`'s supporting artifact
(`governance/audits/WS0014_ETF_CRYPTO_CLASSIFICATION_FRAMEWORK_DESIGN_
20260807.md`, SS3/SS6/SS8/SS9) designed, for the one implementation PR
authorized by `governance/decisions/XASSET-0003-ws0014-etf-classification-
content-authorization.md`.

Scope, exactly what is validated:

- Source-of-truth convention: `intelligence/etf_classification/
  <INSTRUMENT_ID>.yaml`, one file per fund, single-file (no paired
  Markdown), filesystem is the index, plus `COHORT_MANIFEST.yaml`.
- Exactly seven axis-equivalent fields on every record: `structural_role`,
  `constituent_exposure`, `overlap_and_concentration`,
  `cost_and_tracking_quality`, `liquidity`, `structure_and_methodology`,
  `evidence_quality` (SS3.1) -- no fifth substantive judgment axis beyond
  the six named, no numeric score/rank/target field anywhere except the one
  explicitly permitted `cost_and_tracking_quality.expense_ratio_pct`
  (SS6.1).
- A shared cross-asset-handoff envelope (SS6.1/SS6.4): `instrument_id`,
  `asset_type` (must be exactly `"etf"`), `schema_version`, `provenance`,
  `evidence_quality_status`, `uncertainty_summary`, `structural_risk_flags`,
  `record_status`, `valuation_and_economic_assessment_readiness`,
  `cross_asset_handoff`, `abstention_index` -- every envelope field that
  summarizes an axis value is checked for exact, read-only-projection
  consistency against its source axis field (SS6.2), never independently
  recomputed by this validator either.
- `valuation_and_economic_assessment_readiness.status` forced to exactly
  `valuation_required` on every one of the four records, zero exception
  (SS6.3, mirroring `recommendation_validator.py`'s SS G.4/SS G.5 forced-
  value check).
- `overlap_and_concentration` is independently, live-recomputed from
  `issuer_lookthrough.yaml`'s `funds:` entries (SS3.2, mirroring
  `recommendation_validator.py`'s SS G.6 live-recompute discipline) --
  GLD must resolve `not_applicable: true` (no fund-carrier entry anywhere
  in `issuer_lookthrough.yaml`); SPY/VEA/VWO must resolve
  `not_applicable: false` with `measured_by_existing_mechanism: true`.
- Two genuinely distinct abstention semantics per SS3.3, never conflated:
  `not_applicable` (a structurally absent axis -- GLD's constituent/
  overlap axes) versus `unable_to_determine` (an evidence gap, always
  paired with a required, non-empty `abstention_reason`). Abstention does
  not cascade between axes.
- Exact four-instrument population enforcement (SPY, VEA, VWO, GLD), no
  more, no fewer -- `QQQ` is explicitly rejected if present anywhere
  (`XASSET-0003` SS A.1/SS Preflight).
- Closed schema at every level (envelope, per-axis, provenance-source,
  manifest row) -- an explicit permitted-key set per level, rejecting any
  unknown key, learning directly from `contender_registry_validator.py`'s
  own independent-review-found MAJOR gap (a denylist that checked only the
  missing side of a schema check) -- SS8 point 2, SS9.1.
- No equity-field leakage (`economic_role`, `capital_priority`,
  `risk_concentration`, `portfolio_role_ref`, `conviction`) and no
  crypto-field leakage (`network_fundamentals`, `economic_model`,
  `custody_and_counterparty_risk`, `correlation_and_volatility`,
  `regulatory_and_structural_uncertainty`) anywhere in the document tree,
  not just at the top level (SS8 points 4/5).
- No numeric score/rank/target-key leakage (`target_pct`, `target_range`,
  `max_position_size`, `score`, `rank`, `ranking`, `conviction_score`,
  `recommended_target_pct`, `weight`) anywhere in the document tree (SS8
  point 6) -- `expense_ratio_pct` is a distinct key name and is never
  matched by this list, so no special-case scoping is needed for it.
- An independent free-text scan (not a self-declared flag) for: forbidden
  recommendation-shaped phrases; directive/trading language (buy, sell,
  add, hold, trim, exit, wait, stage -- word-boundary matched so "hold"
  never flags the noun "holdings"); chart-domain terminology (sixteen
  terms); and a numeric-percent-of-book/target/weight/allocation token
  pattern -- applied to every free-text string in the document, learning
  directly from `reconciliation_validator.py`'s own disclosed MINOR
  defense-in-depth gap (a self-declared `chart_evidence_used` flag with no
  independent scan) rather than repeating it (SS8 points 6/7, SS9.1).
- Deterministic hashing (`canonical_record_hash`) excludes only the seal
  fields (`sealed_at`, `governing_decision`, `drafting_session_or_shard_id`,
  `content_sha256`, `cohort_manifest_entry`) -- content_sha256 is
  independently recomputable and must match on every sealed record and
  every manifest row, bidirectionally.

This module is a validator, not a data producer. It never opens a file in
write/append/update mode, never creates a directory, and has zero import
relationship with `allocate.py` or `margin_state.py` in either direction.
It does not import `classification_validator.py`/`relationship_validator.py`
for schema logic (each schema is independent), consistent with this
repository's "each Intelligence schema owns its own validator" convention.

VERSION 1.1 bounded correction (post-PR-#270-independent-review): three
MINOR findings, all independently reproduced live before fixing. (1)
`structural_risk_flags` (a required envelope field, SS6.1) had no
independent presence/type check -- a record with the field omitted
entirely validated clean; fixed by giving absence/wrong-type its own
error, separate from the projection-consistency comparison. (2)
`_FORBIDDEN_TEXT_PATTERNS` (the seven forbidden-recommendation-shaped-
phrase regexes) had zero dedicated test coverage despite being an
explicitly required SS9 test item; fixed in the test file, no validator
change. (3) `abstention_index` was checked only for its own internal
shape, never cross-checked against the axes it claims to summarize -- a
record with a genuine `unable_to_determine` abstention and an empty
`abstention_index` validated clean, the same "self-declared flag, no
independent scan" defect class SS9.1 already names. Fixed with a narrow
cross-check (`_check_abstention_index_completeness`) that requires every
literal `unable_to_determine` value to have a matching `abstention_index`
entry. **Deliberately left unresolved**: whether `cost_and_tracking_
quality.tracking_quality_category`'s separate `not_yet_measured` value
(distinct from `unable_to_determine`, and the value all four real records
in this batch use) should also populate `abstention_index` is a genuine
ambiguity in `XASSET-0002`'s own text, not a defect this implementation
may resolve unilaterally (`XASSET-0003` SS B) -- it is disclosed here,
not silently decided either way.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from hashlib import sha256
from pathlib import Path

import yaml

ASSET_TYPE = "etf"
AUTHORIZED_POPULATION = frozenset({"SPY", "VEA", "VWO", "GLD"})

# ── structural_role (SS3.2) ─────────────────────────────────────────────────

_STRUCTURAL_ROLE_CATEGORIES = frozenset({
    "broad_market_beta", "developed_ex_us_equity", "emerging_market_equity",
    "precious_metals_or_commodity", "fixed_income", "other_structural_role",
    "unable_to_determine",
})
_STRUCTURAL_ROLE_ALLOWED_KEYS = frozenset({"role_category", "role_basis", "abstention_reason"})

# ── constituent_exposure (SS3.2) ────────────────────────────────────────────

_GEOGRAPHIC_CONCENTRATION_VALUES = frozenset({
    "domestic_us", "developed_ex_us", "emerging_markets", "mixed_diversified",
    "not_applicable", "unable_to_determine",
})
_SECTOR_CONCENTRATION_VALUES = frozenset({
    "broad_diversified", "sector_concentrated", "not_applicable", "unable_to_determine",
})
_CURRENCY_EXPOSURE_VALUES = frozenset({
    "usd_only", "foreign_currency_mixed", "not_applicable", "unable_to_determine",
})
_CONSTITUENT_EXPOSURE_ALLOWED_KEYS = frozenset({
    "geographic_concentration", "sector_concentration", "currency_exposure", "abstention_reason",
})

# ── overlap_and_concentration (SS3.2) -- mechanical, computed only ─────────

_OVERLAP_ALLOWED_KEYS = frozenset({
    "not_applicable", "measured_by_existing_mechanism", "unmeasured_flag",
})

# ── cost_and_tracking_quality (SS3.2) ───────────────────────────────────────

_TRACKING_QUALITY_VALUES = frozenset({
    "tight_tracking", "moderate_tracking_deviation", "material_tracking_deviation",
    "not_yet_measured", "unable_to_determine",
})
_COST_AND_TRACKING_ALLOWED_KEYS = frozenset({
    "expense_ratio_pct", "tracking_quality_category", "abstention_reason",
})

# ── liquidity (SS3.2) ────────────────────────────────────────────────────────

_LIQUIDITY_TIER_VALUES = frozenset({
    "high_liquidity", "moderate_liquidity", "low_liquidity", "unable_to_determine",
})
_LIQUIDITY_ALLOWED_KEYS = frozenset({"liquidity_tier", "abstention_reason"})

# ── structure_and_methodology (SS3.2) ───────────────────────────────────────

_REPLICATION_METHOD_VALUES = frozenset({
    "physical_full_replication", "physical_sampling", "synthetic_derivative_based",
    "direct_physical_commodity_holding", "unable_to_determine",
})
_BENCHMARK_TYPE_VALUES = frozenset({
    "published_market_index", "spot_commodity_price", "other_benchmark", "unable_to_determine",
})
_STRUCTURE_AND_METHODOLOGY_ALLOWED_KEYS = frozenset({
    "replication_method", "benchmark_type", "benchmark_basis", "abstention_reason",
})

# ── evidence_quality (SS3.2) -- cannot itself abstain ───────────────────────

_PRIMARY_SOURCE_COVERAGE_VALUES = frozenset({"comprehensive", "partial", "limited"})
_EVIDENCE_QUALITY_ALLOWED_KEYS = frozenset({
    "primary_source_coverage", "thesis_uncertainty_statement",
})

# ── provenance (SS6.1) ──────────────────────────────────────────────────────

_SOURCE_TYPE_VALUES = frozenset({"primary", "secondary"})
_ACCESS_STATUS_VALUES = frozenset({
    "directly_inspected", "consulted_via_search_aggregation", "attempted_not_directly_inspected",
})
_SOURCE_ALLOWED_KEYS = frozenset({
    "source_identifier", "source_type", "as_of_date", "access_status", "limitation",
})
_SOURCE_REQUIRED_KEYS = frozenset({"source_identifier", "source_type", "as_of_date", "access_status"})
_PROVENANCE_ALLOWED_KEYS = frozenset({"sources"})

# ── valuation_and_economic_assessment_readiness (SS6.3) ────────────────────

_VALUATION_REQUIRED_VALUE = "valuation_required"
_VALUATION_ALLOWED_KEYS = frozenset({"status", "rationale"})

# ── structural_risk_flags / cross_asset_handoff (SS6.1/SS6.4) ──────────────

_STRUCTURAL_RISK_FLAGS_ALLOWED_KEYS = frozenset({"unmeasured_flag", "not_applicable"})
_CROSS_ASSET_HANDOFF_ALLOWED_KEYS = frozenset({
    "role_summary", "evidence_quality_summary", "uncertainty_summary",
    "liquidity_risk_summary", "overlap_or_correlation_signal", "valuation_readiness",
})
_OVERLAP_OR_CORRELATION_SIGNAL_ALLOWED_KEYS = frozenset({"unmeasured_flag", "not_applicable"})

# ── abstention_index (SS6.1) ────────────────────────────────────────────────

_ABSTENTION_ENTRY_ALLOWED_KEYS = frozenset({"axis", "field", "value", "reason"})

# ── record_status / seal metadata ───────────────────────────────────────────

_RECORD_STATUSES = frozenset({"draft", "sealed"})
_SEAL_REQUIRED_KEYS = frozenset({
    "sealed_at", "governing_decision", "drafting_session_or_shard_id",
    "content_sha256", "cohort_manifest_entry",
})

_AXIS_NAMES = (
    "structural_role", "constituent_exposure", "overlap_and_concentration",
    "cost_and_tracking_quality", "liquidity", "structure_and_methodology",
    "evidence_quality",
)
_ENVELOPE_ONLY_KEYS = frozenset({
    "schema_version", "instrument_id", "asset_type", "provenance",
    "uncertainty_summary", "evidence_quality_status", "structural_risk_flags",
    "record_status", "valuation_and_economic_assessment_readiness",
    "cross_asset_handoff", "abstention_index",
})
_ALL_TOP_LEVEL_KEYS = frozenset({*_ENVELOPE_ONLY_KEYS, *_AXIS_NAMES, *_SEAL_REQUIRED_KEYS})

# ── forbidden leakage (SS8 points 4/5/6, SS9.1) ─────────────────────────────

_EQUITY_FIELD_LEAKAGE = frozenset({
    "economic_role", "capital_priority", "risk_concentration",
    "portfolio_role_ref", "conviction", "economic_system_ref",
})
_CRYPTO_FIELD_LEAKAGE = frozenset({
    "network_fundamentals", "economic_model", "custody_and_counterparty_risk",
    "correlation_and_volatility", "regulatory_and_structural_uncertainty",
})
_NUMERIC_LEAKAGE_KEYS = frozenset({
    "target_pct", "target_range", "max_position_size", "maximum_position_size",
    "score", "rank", "ranking", "conviction_score", "recommended_target_pct", "weight",
})
_FORBIDDEN_KEY_NAMES = frozenset({
    *_EQUITY_FIELD_LEAKAGE, *_CRYPTO_FIELD_LEAKAGE, *_NUMERIC_LEAKAGE_KEYS,
})

_FORBIDDEN_TEXT_PATTERNS = [
    re.compile(p, re.IGNORECASE) for p in (
        r"\bshould\s+be\s+(increased|decreased|raised|lowered|set)\s+to\b",
        r"\brecommend(?:ed|s|ing)?\s+(a\s+)?(target|weight|allocation|position\s+size)\s+of\b",
        r"\bnew\s+target\s+(pct|percent|percentage|range)\b",
        r"\bbuy\s+recommendation\b",
        r"\bsell\s+recommendation\b",
        r"\btrim\s+recommendation\b",
        r"\d+(?:\.\d+)?\s*%\s*(?:of\s+book|target|weight|allocation)",
    )
]

# Word-boundary matched so "hold" never flags the noun "holdings", and
# "exit"/"add"/"wait"/"stage" never false-positive on unrelated substrings
# (recommendation_validator.py's own established design, SS9's own required
# test).
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


@dataclass
class ValidationResult:
    valid: bool
    errors: list[str] = field(default_factory=list)
    source: str | None = None


@dataclass
class DirectoryValidationResult:
    """A missing or empty directory is valid, zero-coverage state -- same
    filesystem-as-index doctrine every prior Intelligence validator in this
    repository already applies."""
    valid: bool
    results: list[ValidationResult] = field(default_factory=list)

    @property
    def record_count(self) -> int:
        return len(self.results)


# ── canonical hashing -- excludes only the five seal fields ────────────────

_HASHABLE_KEYS = tuple(k for k in _ALL_TOP_LEVEL_KEYS if k not in _SEAL_REQUIRED_KEYS)


def canonical_record_hash(data: dict) -> str:
    """SHA-256 of the record's full content (envelope + all seven
    axis-equivalent fields), canonical sorted-key JSON, UTF-8 -- excludes
    every seal field (sealed_at, governing_decision,
    drafting_session_or_shard_id, content_sha256, cohort_manifest_entry),
    avoiding circular self-hashing."""
    hashable = {k: data.get(k) for k in sorted(_HASHABLE_KEYS)}
    canonical = json.dumps(hashable, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return sha256(canonical.encode("utf-8")).hexdigest()


# ── generic helpers ──────────────────────────────────────────────────────

def _non_empty_str(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _require_keys(value: object, field_name: str, required: frozenset[str], errors: list[str]) -> bool:
    if not isinstance(value, dict):
        errors.append(f"{field_name} must be a mapping, got {type(value).__name__}")
        return False
    missing = required - value.keys()
    if missing:
        errors.append(f"{field_name} missing required key(s): {sorted(missing)}")
        return False
    return True


def _reject_unknown_keys(value: dict, field_name: str, allowed: frozenset[str], errors: list[str]) -> None:
    unknown = set(value.keys()) - allowed
    if unknown:
        errors.append(
            f"{field_name} contains unexpected key(s) {sorted(unknown)} -- this schema is "
            f"closed; only {sorted(allowed)} are permitted (XASSET-0002 supporting artifact SS3/SS6)"
        )


def _scan_forbidden_keys(value: object, path: str, errors: list[str]) -> None:
    """Structural scan: a forbidden key name anywhere in the document tree,
    not just at the top level (SS8 points 4/5/6)."""
    if isinstance(value, dict):
        for k, v in value.items():
            key_str = str(k)
            if key_str in _FORBIDDEN_KEY_NAMES:
                kind = (
                    "an equity-classification-shaped field"
                    if key_str in _EQUITY_FIELD_LEAKAGE
                    else "a crypto-classification-shaped field"
                    if key_str in _CRYPTO_FIELD_LEAKAGE
                    else "a numeric score/rank/target-shaped field"
                )
                errors.append(
                    f"{path}.{key_str}: forbidden key name -- {kind} must never appear in an "
                    f"ETF classification record (XASSET-0002 supporting artifact SS8 points 4/5/6)"
                )
            _scan_forbidden_keys(v, f"{path}.{key_str}", errors)
    elif isinstance(value, list):
        for i, item in enumerate(value):
            _scan_forbidden_keys(item, f"{path}[{i}]", errors)


def _scan_free_text_strings(value: object, path: str, errors: list[str]) -> None:
    """Recursively scan every free-text string value for forbidden
    recommendation-shaped phrases, directive language, chart-derived
    terminology, and a numeric-percent-of-book/target/weight/allocation
    token -- an independent mechanism from whatever accepted this string
    into the document, not a self-declared flag (SS9.1)."""
    if isinstance(value, dict):
        for k, v in value.items():
            _scan_free_text_strings(v, f"{path}.{k}", errors)
    elif isinstance(value, list):
        for i, item in enumerate(value):
            _scan_free_text_strings(item, f"{path}[{i}]", errors)
    elif isinstance(value, str):
        for pattern in _FORBIDDEN_TEXT_PATTERNS:
            if pattern.search(value):
                errors.append(f"{path}: contains forbidden recommendation-shaped phrase matching {pattern.pattern!r}")
        for pattern in _DIRECTIVE_PATTERNS:
            if pattern.search(value):
                errors.append(
                    f"{path}: contains directive word {pattern.pattern!r} -- no buy/sell/add/"
                    f"hold/trim/exit/wait/stage signal is permitted in any field, under any "
                    f"framing (XASSET-0002 supporting artifact SS3.2 per-axis prohibited-inference statements)"
                )
        for term, pattern in _CHART_PATTERNS:
            if pattern.search(value):
                errors.append(
                    f"{path}: contains chart-derived terminology {term!r} -- no chart evidence "
                    f"of any kind is permitted (XASSET-0002 supporting artifact SS8 point 7)"
                )


# ── per-axis validators ─────────────────────────────────────────────────

def _validate_structural_role(value: object, errors: list[str]) -> None:
    if not _require_keys(value, "structural_role", frozenset({"role_category"}), errors):
        return
    value = value  # type: dict
    _reject_unknown_keys(value, "structural_role", _STRUCTURAL_ROLE_ALLOWED_KEYS, errors)

    category = value.get("role_category")
    if category not in _STRUCTURAL_ROLE_CATEGORIES:
        errors.append(
            f"structural_role.role_category must be one of {sorted(_STRUCTURAL_ROLE_CATEGORIES)} "
            f"(XASSET-0002 supporting artifact SS3.2) -- got {category!r}"
        )
        return

    role_basis = value.get("role_basis")
    if category == "other_structural_role":
        if not _non_empty_str(role_basis):
            errors.append("structural_role.role_basis is required and non-empty when role_category is 'other_structural_role'")
    elif role_basis is not None:
        errors.append("structural_role.role_basis must be absent unless role_category is 'other_structural_role'")

    abstention_reason = value.get("abstention_reason")
    if category == "unable_to_determine":
        if not _non_empty_str(abstention_reason):
            errors.append("structural_role.abstention_reason is required and non-empty when role_category is 'unable_to_determine'")
    elif abstention_reason is not None:
        errors.append("structural_role.abstention_reason must be absent unless role_category is 'unable_to_determine'")


def _validate_constituent_exposure(value: object, errors: list[str]) -> None:
    required = frozenset({"geographic_concentration", "sector_concentration", "currency_exposure"})
    if not _require_keys(value, "constituent_exposure", required, errors):
        return
    value = value  # type: dict
    _reject_unknown_keys(value, "constituent_exposure", _CONSTITUENT_EXPOSURE_ALLOWED_KEYS, errors)

    geo = value.get("geographic_concentration")
    sector = value.get("sector_concentration")
    currency = value.get("currency_exposure")

    if geo not in _GEOGRAPHIC_CONCENTRATION_VALUES:
        errors.append(f"constituent_exposure.geographic_concentration must be one of {sorted(_GEOGRAPHIC_CONCENTRATION_VALUES)} -- got {geo!r}")
    if sector not in _SECTOR_CONCENTRATION_VALUES:
        errors.append(f"constituent_exposure.sector_concentration must be one of {sorted(_SECTOR_CONCENTRATION_VALUES)} -- got {sector!r}")
    if currency not in _CURRENCY_EXPOSURE_VALUES:
        errors.append(f"constituent_exposure.currency_exposure must be one of {sorted(_CURRENCY_EXPOSURE_VALUES)} -- got {currency!r}")

    any_unable = "unable_to_determine" in (geo, sector, currency)
    abstention_reason = value.get("abstention_reason")
    if any_unable:
        if not _non_empty_str(abstention_reason):
            errors.append("constituent_exposure.abstention_reason is required and non-empty when any sub-field is 'unable_to_determine'")
    elif abstention_reason is not None:
        errors.append("constituent_exposure.abstention_reason must be absent unless a sub-field is 'unable_to_determine'")


def _validate_overlap_and_concentration(value: object, errors: list[str]) -> None:
    if not _require_keys(value, "overlap_and_concentration", frozenset({"not_applicable"}), errors):
        return
    value = value  # type: dict
    _reject_unknown_keys(value, "overlap_and_concentration", _OVERLAP_ALLOWED_KEYS, errors)

    not_applicable = value.get("not_applicable")
    if not isinstance(not_applicable, bool):
        errors.append("overlap_and_concentration.not_applicable must be a boolean")
        return

    measured = value.get("measured_by_existing_mechanism")
    unmeasured = value.get("unmeasured_flag")
    if not_applicable:
        if measured is not None or unmeasured is not None:
            errors.append(
                "overlap_and_concentration.measured_by_existing_mechanism/unmeasured_flag must "
                "be absent (not merely null) when not_applicable is true (no equity-constituent "
                "look-through mechanism applies to this instrument)"
            )
    else:
        if not isinstance(measured, bool):
            errors.append("overlap_and_concentration.measured_by_existing_mechanism must be a boolean when not_applicable is false")
        if not isinstance(unmeasured, bool):
            errors.append("overlap_and_concentration.unmeasured_flag must be a boolean when not_applicable is false")
        if isinstance(measured, bool) and isinstance(unmeasured, bool) and measured == unmeasured:
            errors.append(
                "overlap_and_concentration.unmeasured_flag must be the logical negation of "
                "measured_by_existing_mechanism"
            )


def _validate_cost_and_tracking_quality(value: object, errors: list[str]) -> None:
    if not _require_keys(value, "cost_and_tracking_quality", frozenset({"tracking_quality_category"}), errors):
        return
    value = value  # type: dict
    _reject_unknown_keys(value, "cost_and_tracking_quality", _COST_AND_TRACKING_ALLOWED_KEYS, errors)

    category = value.get("tracking_quality_category")
    if category not in _TRACKING_QUALITY_VALUES:
        errors.append(f"cost_and_tracking_quality.tracking_quality_category must be one of {sorted(_TRACKING_QUALITY_VALUES)} -- got {category!r}")

    expense_ratio = value.get("expense_ratio_pct")
    abstention_reason = value.get("abstention_reason")
    expense_missing = expense_ratio is None
    tracking_unable = category == "unable_to_determine"

    if not expense_missing and not isinstance(expense_ratio, (int, float)):
        errors.append("cost_and_tracking_quality.expense_ratio_pct must be a number (a real disclosed percentage) or absent when abstaining")
    elif not expense_missing and expense_ratio < 0:
        errors.append("cost_and_tracking_quality.expense_ratio_pct must be non-negative")

    if expense_missing or tracking_unable:
        if not _non_empty_str(abstention_reason):
            errors.append(
                "cost_and_tracking_quality.abstention_reason is required and non-empty when "
                "expense_ratio_pct cannot be sourced or tracking_quality_category is "
                "'unable_to_determine'"
            )
    elif abstention_reason is not None:
        errors.append("cost_and_tracking_quality.abstention_reason must be absent unless abstaining on this axis")


def _validate_liquidity(value: object, errors: list[str]) -> None:
    if not _require_keys(value, "liquidity", frozenset({"liquidity_tier"}), errors):
        return
    value = value  # type: dict
    _reject_unknown_keys(value, "liquidity", _LIQUIDITY_ALLOWED_KEYS, errors)

    tier = value.get("liquidity_tier")
    if tier not in _LIQUIDITY_TIER_VALUES:
        errors.append(f"liquidity.liquidity_tier must be one of {sorted(_LIQUIDITY_TIER_VALUES)} -- got {tier!r}")

    abstention_reason = value.get("abstention_reason")
    if tier == "unable_to_determine":
        if not _non_empty_str(abstention_reason):
            errors.append("liquidity.abstention_reason is required and non-empty when liquidity_tier is 'unable_to_determine'")
    elif abstention_reason is not None:
        errors.append("liquidity.abstention_reason must be absent unless liquidity_tier is 'unable_to_determine'")


def _validate_structure_and_methodology(value: object, errors: list[str]) -> None:
    required = frozenset({"replication_method", "benchmark_type"})
    if not _require_keys(value, "structure_and_methodology", required, errors):
        return
    value = value  # type: dict
    _reject_unknown_keys(value, "structure_and_methodology", _STRUCTURE_AND_METHODOLOGY_ALLOWED_KEYS, errors)

    replication = value.get("replication_method")
    benchmark = value.get("benchmark_type")
    if replication not in _REPLICATION_METHOD_VALUES:
        errors.append(f"structure_and_methodology.replication_method must be one of {sorted(_REPLICATION_METHOD_VALUES)} -- got {replication!r}")
    if benchmark not in _BENCHMARK_TYPE_VALUES:
        errors.append(f"structure_and_methodology.benchmark_type must be one of {sorted(_BENCHMARK_TYPE_VALUES)} -- got {benchmark!r}")

    basis = value.get("benchmark_basis")
    if benchmark == "other_benchmark":
        if not _non_empty_str(basis):
            errors.append("structure_and_methodology.benchmark_basis is required and non-empty when benchmark_type is 'other_benchmark'")
    elif basis is not None:
        errors.append("structure_and_methodology.benchmark_basis must be absent unless benchmark_type is 'other_benchmark'")

    any_unable = "unable_to_determine" in (replication, benchmark)
    abstention_reason = value.get("abstention_reason")
    if any_unable:
        if not _non_empty_str(abstention_reason):
            errors.append("structure_and_methodology.abstention_reason is required and non-empty when replication_method or benchmark_type is 'unable_to_determine'")
    elif abstention_reason is not None:
        errors.append("structure_and_methodology.abstention_reason must be absent unless abstaining on this axis")


def _validate_evidence_quality(value: object, errors: list[str]) -> None:
    required = frozenset({"primary_source_coverage", "thesis_uncertainty_statement"})
    if not _require_keys(value, "evidence_quality", required, errors):
        return
    value = value  # type: dict
    _reject_unknown_keys(value, "evidence_quality", _EVIDENCE_QUALITY_ALLOWED_KEYS, errors)

    coverage = value.get("primary_source_coverage")
    if coverage not in _PRIMARY_SOURCE_COVERAGE_VALUES:
        errors.append(f"evidence_quality.primary_source_coverage must be one of {sorted(_PRIMARY_SOURCE_COVERAGE_VALUES)} -- got {coverage!r}")

    if not _non_empty_str(value.get("thesis_uncertainty_statement")):
        errors.append("evidence_quality.thesis_uncertainty_statement is required and must be a non-empty string")


def _validate_provenance(value: object, errors: list[str]) -> None:
    if not _require_keys(value, "provenance", frozenset({"sources"}), errors):
        return
    value = value  # type: dict
    _reject_unknown_keys(value, "provenance", _PROVENANCE_ALLOWED_KEYS, errors)

    sources = value.get("sources")
    if not isinstance(sources, list) or not sources:
        errors.append("provenance.sources must be a non-empty list")
        return

    for i, src in enumerate(sources):
        label = f"provenance.sources[{i}]"
        if not isinstance(src, dict):
            errors.append(f"{label} must be a mapping")
            continue
        missing = _SOURCE_REQUIRED_KEYS - src.keys()
        if missing:
            errors.append(f"{label} missing required key(s): {sorted(missing)}")
        unknown = set(src.keys()) - _SOURCE_ALLOWED_KEYS
        if unknown:
            errors.append(f"{label} contains unexpected key(s) {sorted(unknown)}")
        if not _non_empty_str(src.get("source_identifier")):
            errors.append(f"{label}.source_identifier must be a non-empty string")
        if src.get("source_type") not in _SOURCE_TYPE_VALUES:
            errors.append(f"{label}.source_type must be one of {sorted(_SOURCE_TYPE_VALUES)} -- got {src.get('source_type')!r}")
        if not _non_empty_str(src.get("as_of_date")):
            errors.append(f"{label}.as_of_date must be a non-empty string")
        if src.get("access_status") not in _ACCESS_STATUS_VALUES:
            errors.append(f"{label}.access_status must be one of {sorted(_ACCESS_STATUS_VALUES)} -- got {src.get('access_status')!r}")


def _validate_valuation_readiness(value: object, errors: list[str]) -> None:
    if not _require_keys(value, "valuation_and_economic_assessment_readiness", frozenset({"status", "rationale"}), errors):
        return
    value = value  # type: dict
    _reject_unknown_keys(value, "valuation_and_economic_assessment_readiness", _VALUATION_ALLOWED_KEYS, errors)

    status = value.get("status")
    if status != _VALUATION_REQUIRED_VALUE:
        errors.append(
            f"valuation_and_economic_assessment_readiness.status must be exactly "
            f"{_VALUATION_REQUIRED_VALUE!r} on every record, zero exception (XASSET-0002 "
            f"supporting artifact SS6.3) -- got {status!r}"
        )
    if not _non_empty_str(value.get("rationale")):
        errors.append("valuation_and_economic_assessment_readiness.rationale must be a non-empty string")


def _validate_abstention_index(value: object, errors: list[str]) -> None:
    if not isinstance(value, list):
        errors.append("abstention_index must be a list")
        return
    for i, entry in enumerate(value):
        label = f"abstention_index[{i}]"
        if not isinstance(entry, dict) or (_ABSTENTION_ENTRY_ALLOWED_KEYS - entry.keys()):
            errors.append(f"{label} must be a mapping with keys {sorted(_ABSTENTION_ENTRY_ALLOWED_KEYS)}")
            continue
        unknown = set(entry.keys()) - _ABSTENTION_ENTRY_ALLOWED_KEYS
        if unknown:
            errors.append(f"{label} contains unexpected key(s) {sorted(unknown)}")
        for k in ("axis", "field", "value", "reason"):
            if not _non_empty_str(entry.get(k)):
                errors.append(f"{label}.{k} must be a non-empty string")


_UNABLE_TO_DETERMINE_VALUE = "unable_to_determine"


def _find_unable_to_determine_fields(data: dict) -> list[tuple[str, str]]:
    """(axis, field) pairs where a field is literally set to
    'unable_to_determine' -- the one closed-vocabulary abstention value
    every axis unambiguously treats as a genuine abstention (SS3.3/SS4.4).
    Deliberately does NOT treat cost_and_tracking_quality.tracking_quality_
    category's separate `not_yet_measured` value as an abstention here --
    XASSET-0002's own text is ambiguous on whether that value should also
    populate abstention_index (see the module docstring's v1.1 note); per
    XASSET-0003 SS B, resolving that ambiguity is not this implementation's
    call to make unilaterally."""
    pairs: list[tuple[str, str]] = []
    for axis in _AXIS_NAMES:
        axis_value = data.get(axis)
        if not isinstance(axis_value, dict):
            continue
        for field_name, field_value in axis_value.items():
            if field_value == _UNABLE_TO_DETERMINE_VALUE:
                pairs.append((axis, field_name))
    return pairs


def _check_abstention_index_completeness(data: dict, errors: list[str]) -> None:
    """SS6.1: abstention_index is described as a mechanical rollup a future
    cross-asset synthesis unit can scan "without re-reading every axis" --
    that guarantee requires every genuine unable_to_determine abstention to
    actually appear in it, not merely a self-declared list left
    unreconciled against the axes it claims to summarize (the same defect
    class SS9.1 names: "a self-declared flag is not a substitute for an
    independent scan"). Independent-review finding, v1.1 bounded
    correction: a synthetic record combining a real unable_to_determine
    abstention with an empty abstention_index previously validated clean."""
    actual = _find_unable_to_determine_fields(data)
    if not actual:
        return
    index = data.get("abstention_index")
    if not isinstance(index, list):
        return  # already flagged by _validate_abstention_index
    indexed = {
        (entry.get("axis"), entry.get("field"))
        for entry in index
        if isinstance(entry, dict)
    }
    for axis, field_name in actual:
        if (axis, field_name) not in indexed:
            errors.append(
                f"abstention_index is missing an entry for {axis}.{field_name}, which is set to "
                f"{_UNABLE_TO_DETERMINE_VALUE!r} -- every genuine unable_to_determine abstention "
                f"must be represented in abstention_index (XASSET-0002 supporting artifact SS6.1), "
                f"not merely self-declared and left unreconciled (SS9.1)"
            )


def _validate_envelope_projection_consistency(data: dict, errors: list[str]) -> None:
    """SS6.2: every envelope-level field that summarizes an axis is a
    read-only copy, never independently computed -- checked for exact
    consistency against its source axis field."""
    eq = data.get("evidence_quality") or {}
    if isinstance(eq, dict):
        if data.get("uncertainty_summary") != eq.get("thesis_uncertainty_statement"):
            errors.append(
                "uncertainty_summary must exactly equal evidence_quality.thesis_uncertainty_"
                "statement (SS6.2 read-only-projection rule)"
            )
        if data.get("evidence_quality_status") != eq.get("primary_source_coverage"):
            errors.append(
                "evidence_quality_status must exactly equal evidence_quality."
                "primary_source_coverage (SS6.2 read-only-projection rule)"
            )

    overlap = data.get("overlap_and_concentration") or {}
    risk_flags = data.get("structural_risk_flags")
    if not isinstance(risk_flags, dict):
        # v1.1 bounded correction (independent-review finding): this branch
        # was previously reached only via the `isinstance(risk_flags, dict)`
        # guard below, which silently no-oped when structural_risk_flags was
        # missing entirely -- a required envelope field (SS6.1) had no
        # independent presence/type check of its own, masked in sealed
        # records only because the field happens to be part of
        # _HASHABLE_KEYS. Fixed by making absence/wrong-type its own error,
        # independent of whether overlap_and_concentration is well-formed.
        errors.append("structural_risk_flags must be a mapping (SS6.1 required envelope field)")
    else:
        _reject_unknown_keys(risk_flags, "structural_risk_flags", _STRUCTURAL_RISK_FLAGS_ALLOWED_KEYS, errors)
        if isinstance(overlap, dict):
            expected_flags = {
                "unmeasured_flag": overlap.get("unmeasured_flag"),
                "not_applicable": overlap.get("not_applicable"),
            }
            if risk_flags != expected_flags:
                errors.append(
                    f"structural_risk_flags must exactly project overlap_and_concentration's "
                    f"unmeasured_flag/not_applicable (SS6.2) -- expected {expected_flags}, got {risk_flags}"
                )

    structural_role = data.get("structural_role") or {}
    liquidity = data.get("liquidity") or {}
    valuation = data.get("valuation_and_economic_assessment_readiness") or {}
    handoff = data.get("cross_asset_handoff")
    if isinstance(handoff, dict):
        _reject_unknown_keys(handoff, "cross_asset_handoff", _CROSS_ASSET_HANDOFF_ALLOWED_KEYS, errors)
        missing = _CROSS_ASSET_HANDOFF_ALLOWED_KEYS - handoff.keys()
        if missing:
            errors.append(f"cross_asset_handoff missing required key(s): {sorted(missing)}")

        if isinstance(structural_role, dict) and handoff.get("role_summary") != structural_role.get("role_category"):
            errors.append("cross_asset_handoff.role_summary must exactly equal structural_role.role_category (SS6.4)")
        if isinstance(eq, dict) and handoff.get("evidence_quality_summary") != eq.get("primary_source_coverage"):
            errors.append("cross_asset_handoff.evidence_quality_summary must exactly equal evidence_quality.primary_source_coverage (SS6.4)")
        if handoff.get("uncertainty_summary") != data.get("uncertainty_summary"):
            errors.append("cross_asset_handoff.uncertainty_summary must exactly equal the envelope's own uncertainty_summary (SS6.4)")
        if isinstance(liquidity, dict) and handoff.get("liquidity_risk_summary") != liquidity.get("liquidity_tier"):
            errors.append("cross_asset_handoff.liquidity_risk_summary must exactly equal liquidity.liquidity_tier (SS6.4)")
        if isinstance(valuation, dict) and handoff.get("valuation_readiness") != valuation.get("status"):
            errors.append("cross_asset_handoff.valuation_readiness must exactly equal valuation_and_economic_assessment_readiness.status (SS6.4)")

        signal = handoff.get("overlap_or_correlation_signal")
        if isinstance(overlap, dict):
            expected_signal = {
                "unmeasured_flag": overlap.get("unmeasured_flag"),
                "not_applicable": overlap.get("not_applicable"),
            }
            if not isinstance(signal, dict):
                errors.append("cross_asset_handoff.overlap_or_correlation_signal must be a mapping")
            else:
                _reject_unknown_keys(signal, "cross_asset_handoff.overlap_or_correlation_signal", _OVERLAP_OR_CORRELATION_SIGNAL_ALLOWED_KEYS, errors)
                if signal != expected_signal:
                    errors.append(
                        f"cross_asset_handoff.overlap_or_correlation_signal must exactly project "
                        f"overlap_and_concentration (SS6.4) -- expected {expected_signal}, got {signal}"
                    )
    else:
        errors.append("cross_asset_handoff must be a mapping")


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
            f"record contains unexpected top-level field(s) {sorted(stray)} -- exactly the seven "
            f"axis-equivalent fields plus the envelope/seal fields are permitted, no fifth "
            f"substantive judgment axis (XASSET-0002 supporting artifact SS3/SS6)"
        )


# ── live mechanical recompute: overlap_and_concentration vs issuer_lookthrough.yaml ─

def _recompute_fund_carriers(repo_root: Path) -> frozenset[str]:
    """Independently re-reads issuer_lookthrough.yaml's own funds: entries
    -- never trusts a record's own cached claim (mirrors
    recommendation_validator.py's _recompute_unmeasured_tickers)."""
    path = repo_root / "issuer_lookthrough.yaml"
    if not path.is_file():
        return frozenset()
    try:
        data = yaml.safe_load(path.read_text())
    except yaml.YAMLError:
        return frozenset()
    carriers: set[str] = set()
    if isinstance(data, dict):
        for issuer_entry in data.get("issuers") or []:
            if not isinstance(issuer_entry, dict):
                continue
            for fund_entry in issuer_entry.get("funds") or []:
                if isinstance(fund_entry, dict) and _non_empty_str(fund_entry.get("fund")):
                    carriers.add(fund_entry["fund"])
    return frozenset(carriers)


def _check_live_overlap_recompute(data: dict, *, repo_root: Path | None, errors: list[str]) -> None:
    if repo_root is None:
        return
    instrument_id = data.get("instrument_id")
    overlap = data.get("overlap_and_concentration")
    if not _non_empty_str(instrument_id) or not isinstance(overlap, dict):
        return

    carriers = _recompute_fund_carriers(repo_root)
    is_carrier = instrument_id in carriers
    recorded_not_applicable = overlap.get("not_applicable")

    if is_carrier and recorded_not_applicable is not False:
        errors.append(
            f"overlap_and_concentration.not_applicable must be false for {instrument_id!r} -- "
            f"live-recomputed from issuer_lookthrough.yaml as a fund carrier with at least one "
            f"constituent-weight entry"
        )
    if not is_carrier and recorded_not_applicable is not True:
        errors.append(
            f"overlap_and_concentration.not_applicable must be true for {instrument_id!r} -- "
            f"live-recomputed from issuer_lookthrough.yaml as carrying zero constituent-weight "
            f"entries (GLD's own structural fact per XASSET-0002 supporting artifact SS5)"
        )
    if is_carrier and overlap.get("measured_by_existing_mechanism") is not True:
        errors.append(
            f"overlap_and_concentration.measured_by_existing_mechanism must be true for "
            f"{instrument_id!r} -- live-recomputed as an issuer_lookthrough.yaml fund carrier"
        )


# ── public API: in-memory record validation ─────────────────────────────

def validate_etf_classification_data(
    data: object,
    *,
    source: str | None = None,
    authorized_population: frozenset[str] = AUTHORIZED_POPULATION,
    repo_root: Path | None = None,
) -> ValidationResult:
    """Validate an already-parsed ETF classification mapping. Never touches
    the filesystem except for the live issuer_lookthrough.yaml recompute
    when `repo_root` is supplied."""
    errors: list[str] = []

    if not isinstance(data, dict):
        errors.append(f"root document must be a mapping, got {type(data).__name__}")
        return ValidationResult(valid=False, errors=errors, source=source)

    instrument_id = data.get("instrument_id")
    if not _non_empty_str(instrument_id):
        errors.append("instrument_id must be a non-empty string")
    elif authorized_population and instrument_id not in authorized_population:
        errors.append(
            f"instrument_id {instrument_id!r} is not in the authorized four-instrument "
            f"population {sorted(authorized_population)} (XASSET-0003 SS A.1) -- QQQ and every "
            f"other fund is explicitly excluded from this batch"
        )

    asset_type = data.get("asset_type")
    if asset_type != ASSET_TYPE:
        errors.append(f"asset_type must be exactly {ASSET_TYPE!r} -- got {asset_type!r}")

    if not _non_empty_str(data.get("schema_version")):
        errors.append("schema_version must be a non-empty string")

    for axis, validator in (
        ("structural_role", _validate_structural_role),
        ("constituent_exposure", _validate_constituent_exposure),
        ("overlap_and_concentration", _validate_overlap_and_concentration),
        ("cost_and_tracking_quality", _validate_cost_and_tracking_quality),
        ("liquidity", _validate_liquidity),
        ("structure_and_methodology", _validate_structure_and_methodology),
        ("evidence_quality", _validate_evidence_quality),
    ):
        if axis not in data:
            errors.append(f"record missing required field: {axis}")
        else:
            validator(data[axis], errors)

    if "provenance" not in data:
        errors.append("record missing required field: provenance")
    else:
        _validate_provenance(data["provenance"], errors)

    if "valuation_and_economic_assessment_readiness" not in data:
        errors.append("record missing required field: valuation_and_economic_assessment_readiness")
    else:
        _validate_valuation_readiness(data["valuation_and_economic_assessment_readiness"], errors)

    if "abstention_index" not in data:
        errors.append("record missing required field: abstention_index")
    else:
        _validate_abstention_index(data["abstention_index"], errors)
        _check_abstention_index_completeness(data, errors)

    _validate_no_stray_top_level_fields(data, errors)
    _validate_envelope_projection_consistency(data, errors)
    _validate_seal(data, errors)
    _scan_forbidden_keys(data, str(instrument_id) if _non_empty_str(instrument_id) else "<record>", errors)
    _scan_free_text_strings(data, str(instrument_id) if _non_empty_str(instrument_id) else "<record>", errors)
    _check_live_overlap_recompute(data, repo_root=repo_root, errors=errors)

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


def validate_etf_classification_file(
    path: str | Path,
    *,
    authorized_population: frozenset[str] = AUTHORIZED_POPULATION,
    repo_root: Path | None = None,
) -> ValidationResult:
    path = Path(path)
    source = str(path)
    data, read_errors = _read_yaml(path)
    if read_errors:
        return ValidationResult(valid=False, errors=read_errors, source=source)

    result = validate_etf_classification_data(
        data, source=source, authorized_population=authorized_population, repo_root=repo_root,
    )

    if isinstance(data, dict) and _non_empty_str(data.get("instrument_id")):
        expected_stem = data["instrument_id"]
        if path.stem != expected_stem:
            result.errors.append(
                f"filename stem {path.stem!r} does not match the record's own instrument_id {expected_stem!r}"
            )
            result.valid = False

    return result


_MANIFEST_FILENAME = "COHORT_MANIFEST.yaml"
_MANIFEST_REQUIRED_ROW_KEYS = frozenset({
    "instrument_id", "sealed_at", "content_sha256", "schema_version", "governing_decision", "record_path",
})
_MANIFEST_ROW_ALLOWED_KEYS = _MANIFEST_REQUIRED_ROW_KEYS
_MANIFEST_TOP_LEVEL_ALLOWED_KEYS = frozenset({"schema_version", "governing_decision", "cohort"})


def validate_cohort_manifest(
    manifest_data: object,
    records_by_instrument: dict[str, dict],
    *,
    authorized_population: frozenset[str] = AUTHORIZED_POPULATION,
) -> ValidationResult:
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

        instrument_id = row["instrument_id"]
        if instrument_id in seen:
            errors.append(f"cohort manifest lists {instrument_id!r} more than once")
        seen.add(instrument_id)

        record = records_by_instrument.get(instrument_id)
        if record is None:
            errors.append(f"cohort[{i}] instrument_id {instrument_id!r} has no corresponding sealed record file")
            continue

        expected_hash = canonical_record_hash(record)
        if row["content_sha256"] != expected_hash:
            errors.append(f"cohort[{i}] ({instrument_id!r}) content_sha256 mismatch -- manifest {row['content_sha256']!r}, recomputed {expected_hash!r}")
        if record.get("content_sha256") != row["content_sha256"]:
            errors.append(f"cohort[{i}] ({instrument_id!r}) manifest content_sha256 does not match the record's own recorded content_sha256")

    if authorized_population:
        missing_from_manifest = authorized_population - seen
        if missing_from_manifest:
            errors.append(f"cohort manifest is missing authorized instrument(s): {sorted(missing_from_manifest)}")
        extra = seen - authorized_population
        if extra:
            errors.append(f"cohort manifest lists instrument(s) outside the authorized population: {sorted(extra)}")

    orphans = set(records_by_instrument) - seen
    if orphans:
        errors.append(f"sealed record(s) exist with no corresponding cohort manifest entry: {sorted(orphans)}")

    return ValidationResult(valid=not errors, errors=errors, source=_MANIFEST_FILENAME)


def validate_etf_classification_directory(
    directory: str | Path,
    *,
    authorized_population: frozenset[str] = AUTHORIZED_POPULATION,
    repo_root: Path | None = None,
) -> DirectoryValidationResult:
    directory = Path(directory)
    if not directory.exists() or not directory.is_dir():
        return DirectoryValidationResult(valid=True, results=[])

    yaml_paths = sorted(p for p in directory.glob("*.yaml") if p.name != _MANIFEST_FILENAME)
    results = [
        validate_etf_classification_file(p, authorized_population=authorized_population, repo_root=repo_root)
        for p in yaml_paths
    ]

    records_by_instrument: dict[str, dict] = {}
    for p in yaml_paths:
        data, read_errors = _read_yaml(p)
        if not read_errors and isinstance(data, dict) and _non_empty_str(data.get("instrument_id")):
            records_by_instrument[data["instrument_id"]] = data

    manifest_path = directory / _MANIFEST_FILENAME
    if manifest_path.is_file():
        manifest_data, read_errors = _read_yaml(manifest_path)
        if read_errors:
            results.append(ValidationResult(valid=False, errors=read_errors, source=str(manifest_path)))
        else:
            results.append(
                validate_cohort_manifest(manifest_data, records_by_instrument, authorized_population=authorized_population)
            )
    elif records_by_instrument:
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
    _result = validate_etf_classification_directory(
        _repo_root / "intelligence" / "etf_classification", repo_root=_repo_root,
    )
    if _result.valid:
        print(f"etf_classification_validator: OK ({_result.record_count} result(s))")
        sys.exit(0)
    else:
        print("etf_classification_validator: FAILED")
        for _r in _result.results:
            if not _r.valid:
                for _err in _r.errors:
                    print(f"  - [{_r.source}] {_err}")
        sys.exit(1)
