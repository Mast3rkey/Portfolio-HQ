"""
crypto_classification_validator.py -- read-only schema validator for the
first WS-0014 cryptocurrency blind-classification content batch (BTC, ETH,
SOL), authored against the crypto framework `governance/decisions/
XASSET-0002-etf-and-crypto-classification-framework-design.md`'s supporting
artifact (`governance/audits/WS0014_ETF_CRYPTO_CLASSIFICATION_FRAMEWORK_
DESIGN_20260807.md`, SS4/SS6/SS8/SS9) designed, for the one implementation PR
authorized by `governance/decisions/XASSET-0004-ws0014-crypto-classification-
content-authorization.md`.

Scope, exactly what is validated:

- Source-of-truth convention: `intelligence/crypto_classification/
  <INSTRUMENT_ID>.yaml`, one file per coin, single-file (no paired
  Markdown), filesystem is the index, plus `COHORT_MANIFEST.yaml` -- the
  identical convention `etf_classification_validator.py` already
  established for the ETF sleeve (SS4/SS9 batching rule: crypto and ETF
  content are separate filings, but nothing in the governing design
  requires a different storage convention).
- Exactly six axis-equivalent fields on every record: `network_fundamentals`,
  `economic_model`, `liquidity_and_market_structure`,
  `custody_and_counterparty_risk`, `correlation_and_volatility`,
  `regulatory_and_structural_uncertainty`, plus `evidence_quality` (SS4.1)
  -- no eighth substantive judgment axis, no `economic_role`/
  `capital_priority` in TIER-0002's company sense, no ETF-only field, no
  numeric score/rank/target field anywhere (SS6.1 -- this framework defines
  no numeric field for crypto at all, unlike the ETF framework's single
  permitted `expense_ratio_pct`).
- A shared cross-asset-handoff envelope (SS6.1/SS6.4): `instrument_id`,
  `asset_type` (must be exactly `"cryptocurrency"`), `schema_version`,
  `provenance`, `evidence_quality_status`, `uncertainty_summary`,
  `structural_risk_flags`, `record_status`,
  `valuation_and_economic_assessment_readiness`, `cross_asset_handoff`,
  `abstention_index` -- every envelope field that summarizes an axis value
  is checked for exact, read-only-projection consistency against its
  source axis field (SS6.2), never independently recomputed by this
  validator either.
- `valuation_and_economic_assessment_readiness.status` forced to exactly
  `valuation_required` on every one of the three records, zero exception
  (SS6.3/XASSET-0004 SS F).
- `correlation_and_volatility.cross_coin_correlation_status` forced to
  exactly `not_yet_measured` on every one of the three records, zero
  exception -- this filing's authorization (XASSET-0004 SS E) does not
  permit a separately-authorized correlation study to exist yet, so the
  second closed-vocabulary value (`measured_elsewhere_cross_reference_
  required`) is rejected outright at this implementation, distinct from
  the schema itself (which reserves that value for a future study this
  batch is not authorized to reference). No numeric correlation
  coefficient field exists anywhere in this schema (SS4.3, XASSET-0004
  SS E) -- structurally enforced by the closed per-axis key set, the
  forbidden-key scan, and a dedicated live check.
- Two genuinely distinct abstention semantics per SS4.4 (identical to
  SS3.3's equity/ETF discipline), never conflated: `not_applicable` (a
  structurally absent mechanism -- e.g. BTC's absent staking/fee-accrual,
  represented as boolean `false` on `economic_model`'s two applicability
  fields, or a genuinely non-programmable base layer's
  `smart_contract_risk_category`) versus `unable_to_determine` (an
  evidence gap, always paired with a required, non-empty
  `abstention_reason`). Abstention does not cascade between axes.
- Exact three-instrument population enforcement (BTC, ETH, SOL), no more,
  no fewer -- `ZORA`, `WIF`, `BONK`, `PEPE`, `HYPE`, and every other coin
  are explicitly rejected if present anywhere (`XASSET-0004` SS A.1/SS
  Preflight).
- Closed schema at every level (envelope, per-axis, provenance-source,
  manifest row) -- an explicit permitted-key set per level, rejecting any
  unknown key, learning directly from `contender_registry_validator.py`'s
  own independent-review-found MAJOR gap and carried forward once already
  by `etf_classification_validator.py` (SS8 point 2, SS9.1).
- No equity-field leakage (`economic_role`, `capital_priority`,
  `risk_concentration`, `portfolio_role_ref`, `conviction`,
  `economic_system_ref`) and no ETF-field leakage (`structural_role`,
  `constituent_exposure`, `overlap_and_concentration`,
  `cost_and_tracking_quality`, `structure_and_methodology`) anywhere in
  the document tree, not just at the top level (SS8 points 4/5).
- No numeric score/rank/target-key leakage (`target_pct`, `target_range`,
  `max_position_size`, `score`, `rank`, `ranking`, `conviction_score`,
  `recommended_target_pct`, `weight`, and -- crypto-specific, since no
  legitimate numeric field exists in this schema at all --
  `expense_ratio_pct`, `correlation_coefficient`,
  `cross_coin_correlation_coefficient`) anywhere in the document tree
  (SS8 point 6, XASSET-0004 SS E).
- An independent free-text scan (not a self-declared flag) for: forbidden
  recommendation-shaped phrases; directive/trading language (buy, sell,
  add, hold, trim, exit, wait, stage -- word-boundary matched so "hold"
  never flags the noun "holdings"); chart-domain terminology (sixteen
  terms) -- applied to every free-text string in the document, learning
  directly from `reconciliation_validator.py`'s own disclosed MINOR
  defense-in-depth gap rather than repeating it (SS8 points 6/7, SS9.1).
- Deterministic hashing (`canonical_record_hash`) excludes only the seal
  fields (`sealed_at`, `governing_decision`, `drafting_session_or_shard_id`,
  `content_sha256`, `cohort_manifest_entry`) -- content_sha256 is
  independently recomputable and must match on every sealed record and
  every manifest row, bidirectionally.

This module is a validator, not a data producer. It never opens a file in
write/append/update mode, never creates a directory, and has zero import
relationship with `allocate.py` or `margin_state.py` in either direction.
It does not import `classification_validator.py`/`relationship_validator.py`
/`etf_classification_validator.py` for schema logic (each schema is
independent), consistent with this repository's "each Intelligence schema
owns its own validator" convention -- deliberately not reusing
`etf_classification_validator.py`'s helpers even though several (canonical
hashing shape, generic key-checking helpers, forbidden-text scanning) are
structurally identical, since `XASSET-0004` SS A.4 leaves that determination
to the implementing session and the two schemas' closed-key sets, axis
names, and forbidden-leakage lists are asset-type-specific enough that a
shared-helper module would need its own asset-type parameterization --
duplication here is the smaller, more auditable choice, matching this
repository's existing per-schema-validator convention throughout
`intelligence/`.

Carries forward, from the start rather than as a later correction, the
three lessons `etf_classification_validator.py`'s own v1.1 bounded
correction (post-PR-#270-independent-review) already paid for once:
(1) every required envelope field (including `structural_risk_flags`) gets
its own independent presence/type check, never masked by being folded only
into a projection-consistency comparison; (2) every forbidden-text pattern
(recommendation-shaped phrases, directive words, chart terms) has its own
dedicated test, not merely an implemented-but-untested scan mechanism; (3)
`abstention_index` is independently cross-checked against every genuine
`unable_to_determine` value actually present in the record, not merely
validated for its own internal shape. This module additionally discloses,
rather than silently resolves, the crypto-specific analogue of the same
`not_yet_measured`-versus-formal-abstention ambiguity `etf_classification_
validator.py`'s docstring already names for the ETF sleeve's
`tracking_quality_category` field: `correlation_and_volatility.
cross_coin_correlation_status`'s `not_yet_measured` value is a determined,
forced value (SS E), not treated as an `abstention_index`-eligible
abstention by this validator -- consistent with how `not_yet_measured` is
treated on the ETF side.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from hashlib import sha256
from pathlib import Path

import yaml

ASSET_TYPE = "cryptocurrency"
AUTHORIZED_POPULATION = frozenset({"BTC", "ETH", "SOL"})

# ── network_fundamentals (SS4.3) ────────────────────────────────────────────

_CONSENSUS_MECHANISM_VALUES = frozenset({"proof_of_work", "proof_of_stake", "other_consensus"})
_ADOPTION_TREND_VALUES = frozenset({
    "established_high_usage", "growing_usage", "declining_or_stagnant_usage", "unable_to_determine",
})
_NETWORK_FUNDAMENTALS_ALLOWED_KEYS = frozenset({
    "consensus_mechanism", "consensus_basis", "adoption_trend_category", "abstention_reason",
})

# ── economic_model (SS4.3) ──────────────────────────────────────────────────

_SUPPLY_MODEL_VALUES = frozenset({
    "fixed_capped_supply", "disinflationary_schedule", "uncapped_or_inflationary", "unable_to_determine",
})
_ECONOMIC_MODEL_ALLOWED_KEYS = frozenset({
    "supply_model", "fee_accrual_applicable", "fee_accrual_basis",
    "staking_applicable", "staking_basis", "abstention_reason",
})

# ── liquidity_and_market_structure (SS4.3) ──────────────────────────────────

_LIQUIDITY_TIER_VALUES = frozenset({
    "high_liquidity", "moderate_liquidity", "low_liquidity", "unable_to_determine",
})
_LIQUIDITY_ALLOWED_KEYS = frozenset({"liquidity_tier", "market_structure_notes", "abstention_reason"})

# ── custody_and_counterparty_risk (SS4.3) ───────────────────────────────────

_CUSTODY_MODEL_VALUES = frozenset({"exchange_custodied", "self_custodied", "mixed_or_unknown"})
_SMART_CONTRACT_RISK_VALUES = frozenset({
    "base_layer_minimal_smart_contract_surface", "smart_contract_platform_material_surface",
    "not_applicable", "unable_to_determine",
})
_CUSTODY_ALLOWED_KEYS = frozenset({
    "custody_model", "smart_contract_risk_category", "abstention_reason",
})

# ── correlation_and_volatility (SS4.3) -- mechanical/forced, XASSET-0004 SS E ─

_HISTORICAL_VOLATILITY_VALUES = frozenset({"high_volatility", "extreme_volatility", "unable_to_determine"})
_CROSS_COIN_CORRELATION_VALUES = frozenset({
    "not_yet_measured", "measured_elsewhere_cross_reference_required",
})
_FORCED_CORRELATION_STATUS = "not_yet_measured"
_CORRELATION_AND_VOLATILITY_ALLOWED_KEYS = frozenset({
    "historical_volatility_category", "cross_coin_correlation_status", "abstention_reason",
})

# ── regulatory_and_structural_uncertainty (SS4.3) ───────────────────────────

_STRUCTURAL_UNCERTAINTY_VALUES = frozenset({
    "none_currently_disclosed", "disclosed_and_unresolved", "unable_to_determine",
})
_REGULATORY_ALLOWED_KEYS = frozenset({
    "disclosed_regulatory_matter_exists", "matter_summary_and_citation",
    "structural_uncertainty_category", "abstention_reason",
})

# ── evidence_quality (SS4.3 -> SS3.2) -- cannot itself abstain ─────────────

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

_STRUCTURAL_RISK_FLAGS_ALLOWED_KEYS = frozenset({
    "custody_model", "smart_contract_risk_category", "cross_coin_correlation_status",
})
_CROSS_ASSET_HANDOFF_ALLOWED_KEYS = frozenset({
    "role_summary", "evidence_quality_summary", "uncertainty_summary",
    "liquidity_risk_summary", "overlap_or_correlation_signal", "valuation_readiness",
})

# ── abstention_index (SS6.1) ────────────────────────────────────────────────

_ABSTENTION_ENTRY_ALLOWED_KEYS = frozenset({"axis", "field", "value", "reason"})

# ── record_status / seal metadata ───────────────────────────────────────────

_RECORD_STATUSES = frozenset({"draft", "sealed"})
_SEAL_REQUIRED_KEYS = frozenset({
    "sealed_at", "governing_decision", "drafting_session_or_shard_id",
    "content_sha256", "cohort_manifest_entry",
})

_AXIS_NAMES = (
    "network_fundamentals", "economic_model", "liquidity_and_market_structure",
    "custody_and_counterparty_risk", "correlation_and_volatility",
    "regulatory_and_structural_uncertainty", "evidence_quality",
)
_ENVELOPE_ONLY_KEYS = frozenset({
    "schema_version", "instrument_id", "asset_type", "provenance",
    "uncertainty_summary", "evidence_quality_status", "structural_risk_flags",
    "record_status", "valuation_and_economic_assessment_readiness",
    "cross_asset_handoff", "abstention_index",
})
_ALL_TOP_LEVEL_KEYS = frozenset({*_ENVELOPE_ONLY_KEYS, *_AXIS_NAMES, *_SEAL_REQUIRED_KEYS})

# ── forbidden leakage (SS8 points 4/5/6, SS9.1, XASSET-0004 SS E) ──────────

_EQUITY_FIELD_LEAKAGE = frozenset({
    "economic_role", "capital_priority", "risk_concentration",
    "portfolio_role_ref", "conviction", "economic_system_ref",
})
_ETF_FIELD_LEAKAGE = frozenset({
    "structural_role", "constituent_exposure", "overlap_and_concentration",
    "cost_and_tracking_quality", "structure_and_methodology",
})
_NUMERIC_LEAKAGE_KEYS = frozenset({
    "target_pct", "target_range", "max_position_size", "maximum_position_size",
    "score", "rank", "ranking", "conviction_score", "recommended_target_pct", "weight",
    # No numeric field of any kind is authorized anywhere in the crypto
    # schema (SS4.3, SS6.1, XASSET-0004 SS E) -- unlike the ETF schema's
    # single permitted expense_ratio_pct, so these are rejected outright
    # rather than scoped-permitted.
    "expense_ratio_pct", "correlation_coefficient", "cross_coin_correlation_coefficient",
})
_FORBIDDEN_KEY_NAMES = frozenset({
    *_EQUITY_FIELD_LEAKAGE, *_ETF_FIELD_LEAKAGE, *_NUMERIC_LEAKAGE_KEYS,
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
# (etf_classification_validator.py's own established design, SS9's own
# required test).
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
            f"closed; only {sorted(allowed)} are permitted (XASSET-0002 supporting artifact SS4/SS6)"
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
                    else "an ETF-classification-shaped field"
                    if key_str in _ETF_FIELD_LEAKAGE
                    else "a numeric score/rank/target/coefficient-shaped field"
                )
                errors.append(
                    f"{path}.{key_str}: forbidden key name -- {kind} must never appear in a "
                    f"crypto classification record (XASSET-0002 supporting artifact SS8 points "
                    f"4/5/6, XASSET-0004 SS E)"
                )
            _scan_forbidden_keys(v, f"{path}.{key_str}", errors)
    elif isinstance(value, list):
        for i, item in enumerate(value):
            _scan_forbidden_keys(item, f"{path}[{i}]", errors)


def _scan_free_text_strings(value: object, path: str, errors: list[str]) -> None:
    """Recursively scan every free-text string value for forbidden
    recommendation-shaped phrases, directive language, and chart-derived
    terminology -- an independent mechanism from whatever accepted this
    string into the document, not a self-declared flag (SS9.1)."""
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
                    f"framing (XASSET-0002 supporting artifact SS4.3 per-axis prohibited-inference statements)"
                )
        for term, pattern in _CHART_PATTERNS:
            if pattern.search(value):
                errors.append(
                    f"{path}: contains chart-derived terminology {term!r} -- no chart evidence "
                    f"of any kind is permitted (XASSET-0002 supporting artifact SS8 point 7)"
                )


# ── per-axis validators ─────────────────────────────────────────────────

def _validate_network_fundamentals(value: object, errors: list[str]) -> None:
    if not _require_keys(value, "network_fundamentals", frozenset({"consensus_mechanism"}), errors):
        return
    value = value  # type: dict
    _reject_unknown_keys(value, "network_fundamentals", _NETWORK_FUNDAMENTALS_ALLOWED_KEYS, errors)

    consensus = value.get("consensus_mechanism")
    if consensus not in _CONSENSUS_MECHANISM_VALUES:
        errors.append(
            f"network_fundamentals.consensus_mechanism must be one of "
            f"{sorted(_CONSENSUS_MECHANISM_VALUES)} (XASSET-0002 supporting artifact SS4.3) -- "
            f"got {consensus!r}"
        )
        return

    basis = value.get("consensus_basis")
    if consensus == "other_consensus":
        if not _non_empty_str(basis):
            errors.append("network_fundamentals.consensus_basis is required and non-empty when consensus_mechanism is 'other_consensus'")
    elif basis is not None:
        errors.append("network_fundamentals.consensus_basis must be absent unless consensus_mechanism is 'other_consensus'")

    # consensus_mechanism has no abstention path (SS4.3) -- always determinable.
    trend = value.get("adoption_trend_category")
    if trend is not None and trend not in _ADOPTION_TREND_VALUES:
        errors.append(f"network_fundamentals.adoption_trend_category must be one of {sorted(_ADOPTION_TREND_VALUES)} -- got {trend!r}")
    elif trend is None:
        errors.append("network_fundamentals.adoption_trend_category is required")

    abstention_reason = value.get("abstention_reason")
    if trend == "unable_to_determine":
        if not _non_empty_str(abstention_reason):
            errors.append("network_fundamentals.abstention_reason is required and non-empty when adoption_trend_category is 'unable_to_determine'")
    elif abstention_reason is not None:
        errors.append("network_fundamentals.abstention_reason must be absent unless adoption_trend_category is 'unable_to_determine'")


def _validate_economic_model(value: object, errors: list[str]) -> None:
    required = frozenset({"supply_model", "fee_accrual_applicable", "staking_applicable"})
    if not _require_keys(value, "economic_model", required, errors):
        return
    value = value  # type: dict
    _reject_unknown_keys(value, "economic_model", _ECONOMIC_MODEL_ALLOWED_KEYS, errors)

    supply = value.get("supply_model")
    if supply not in _SUPPLY_MODEL_VALUES:
        errors.append(f"economic_model.supply_model must be one of {sorted(_SUPPLY_MODEL_VALUES)} -- got {supply!r}")

    fee_applicable = value.get("fee_accrual_applicable")
    stake_applicable = value.get("staking_applicable")
    if not isinstance(fee_applicable, bool):
        errors.append("economic_model.fee_accrual_applicable must be a boolean")
    if not isinstance(stake_applicable, bool):
        errors.append("economic_model.staking_applicable must be a boolean")

    fee_basis = value.get("fee_accrual_basis")
    if fee_applicable is True:
        if not _non_empty_str(fee_basis):
            errors.append("economic_model.fee_accrual_basis is required and non-empty when fee_accrual_applicable is true")
    elif fee_basis is not None:
        errors.append("economic_model.fee_accrual_basis must be absent unless fee_accrual_applicable is true")

    stake_basis = value.get("staking_basis")
    if stake_applicable is True:
        if not _non_empty_str(stake_basis):
            errors.append("economic_model.staking_basis is required and non-empty when staking_applicable is true")
    elif stake_basis is not None:
        errors.append("economic_model.staking_basis must be absent unless staking_applicable is true")

    abstention_reason = value.get("abstention_reason")
    if supply == "unable_to_determine":
        if not _non_empty_str(abstention_reason):
            errors.append("economic_model.abstention_reason is required and non-empty when supply_model is 'unable_to_determine'")
    elif abstention_reason is not None:
        errors.append("economic_model.abstention_reason must be absent unless supply_model is 'unable_to_determine'")


def _validate_liquidity_and_market_structure(value: object, errors: list[str]) -> None:
    if not _require_keys(value, "liquidity_and_market_structure", frozenset({"liquidity_tier"}), errors):
        return
    value = value  # type: dict
    _reject_unknown_keys(value, "liquidity_and_market_structure", _LIQUIDITY_ALLOWED_KEYS, errors)

    tier = value.get("liquidity_tier")
    if tier not in _LIQUIDITY_TIER_VALUES:
        errors.append(f"liquidity_and_market_structure.liquidity_tier must be one of {sorted(_LIQUIDITY_TIER_VALUES)} -- got {tier!r}")

    notes = value.get("market_structure_notes")
    if notes is not None and not _non_empty_str(notes):
        errors.append("liquidity_and_market_structure.market_structure_notes must be a non-empty string when present")

    abstention_reason = value.get("abstention_reason")
    if tier == "unable_to_determine":
        if not _non_empty_str(abstention_reason):
            errors.append("liquidity_and_market_structure.abstention_reason is required and non-empty when liquidity_tier is 'unable_to_determine'")
    elif abstention_reason is not None:
        errors.append("liquidity_and_market_structure.abstention_reason must be absent unless liquidity_tier is 'unable_to_determine'")


def _validate_custody_and_counterparty_risk(value: object, errors: list[str]) -> None:
    required = frozenset({"custody_model", "smart_contract_risk_category"})
    if not _require_keys(value, "custody_and_counterparty_risk", required, errors):
        return
    value = value  # type: dict
    _reject_unknown_keys(value, "custody_and_counterparty_risk", _CUSTODY_ALLOWED_KEYS, errors)

    custody = value.get("custody_model")
    risk_cat = value.get("smart_contract_risk_category")
    if custody not in _CUSTODY_MODEL_VALUES:
        errors.append(f"custody_and_counterparty_risk.custody_model must be one of {sorted(_CUSTODY_MODEL_VALUES)} -- got {custody!r}")
    if risk_cat not in _SMART_CONTRACT_RISK_VALUES:
        errors.append(f"custody_and_counterparty_risk.smart_contract_risk_category must be one of {sorted(_SMART_CONTRACT_RISK_VALUES)} -- got {risk_cat!r}")

    abstention_reason = value.get("abstention_reason")
    if risk_cat == "unable_to_determine":
        if not _non_empty_str(abstention_reason):
            errors.append("custody_and_counterparty_risk.abstention_reason is required and non-empty when smart_contract_risk_category is 'unable_to_determine'")
    elif abstention_reason is not None:
        errors.append("custody_and_counterparty_risk.abstention_reason must be absent unless smart_contract_risk_category is 'unable_to_determine'")


def _validate_correlation_and_volatility(value: object, errors: list[str]) -> None:
    required = frozenset({"historical_volatility_category", "cross_coin_correlation_status"})
    if not _require_keys(value, "correlation_and_volatility", required, errors):
        return
    value = value  # type: dict
    _reject_unknown_keys(value, "correlation_and_volatility", _CORRELATION_AND_VOLATILITY_ALLOWED_KEYS, errors)

    vol = value.get("historical_volatility_category")
    corr = value.get("cross_coin_correlation_status")
    if vol not in _HISTORICAL_VOLATILITY_VALUES:
        errors.append(f"correlation_and_volatility.historical_volatility_category must be one of {sorted(_HISTORICAL_VOLATILITY_VALUES)} -- got {vol!r}")
    if corr not in _CROSS_COIN_CORRELATION_VALUES:
        errors.append(f"correlation_and_volatility.cross_coin_correlation_status must be one of {sorted(_CROSS_COIN_CORRELATION_VALUES)} -- got {corr!r}")
    elif corr != _FORCED_CORRELATION_STATUS:
        errors.append(
            f"correlation_and_volatility.cross_coin_correlation_status must be exactly "
            f"{_FORCED_CORRELATION_STATUS!r} on every record -- this implementation is not "
            f"authorized to reference a separately-authorized correlation study (XASSET-0004 "
            f"SS E: 'this filing does not authorize a new correlation study ... or any market-"
            f"data expansion beyond SS C's evidence standard') -- got {corr!r}"
        )

    abstention_reason = value.get("abstention_reason")
    if vol == "unable_to_determine":
        if not _non_empty_str(abstention_reason):
            errors.append("correlation_and_volatility.abstention_reason is required and non-empty when historical_volatility_category is 'unable_to_determine'")
    elif abstention_reason is not None:
        errors.append("correlation_and_volatility.abstention_reason must be absent unless historical_volatility_category is 'unable_to_determine'")


def _validate_regulatory_and_structural_uncertainty(value: object, errors: list[str]) -> None:
    required = frozenset({"disclosed_regulatory_matter_exists", "structural_uncertainty_category"})
    if not _require_keys(value, "regulatory_and_structural_uncertainty", required, errors):
        return
    value = value  # type: dict
    _reject_unknown_keys(value, "regulatory_and_structural_uncertainty", _REGULATORY_ALLOWED_KEYS, errors)

    exists = value.get("disclosed_regulatory_matter_exists")
    if not isinstance(exists, bool):
        errors.append("regulatory_and_structural_uncertainty.disclosed_regulatory_matter_exists must be a boolean")

    category = value.get("structural_uncertainty_category")
    if category not in _STRUCTURAL_UNCERTAINTY_VALUES:
        errors.append(f"regulatory_and_structural_uncertainty.structural_uncertainty_category must be one of {sorted(_STRUCTURAL_UNCERTAINTY_VALUES)} -- got {category!r}")

    citation = value.get("matter_summary_and_citation")
    if exists is True:
        if not _non_empty_str(citation):
            errors.append("regulatory_and_structural_uncertainty.matter_summary_and_citation is required and non-empty when disclosed_regulatory_matter_exists is true")
    elif citation is not None:
        errors.append("regulatory_and_structural_uncertainty.matter_summary_and_citation must be absent unless disclosed_regulatory_matter_exists is true")

    # "This axis may never contain a predictive regulatory or legal
    # opinion" (SS4.3) is enforced by the free-text forbidden-phrase scan
    # (no dedicated predictive-language list exists yet in this schema
    # beyond the shared directive/recommendation scan) -- SS4.3's own
    # guardrail is a content discipline for the drafting session, not a
    # separately mechanically-testable vocabulary distinct from
    # "none_currently_disclosed" vs "disclosed_and_unresolved" above.

    abstention_reason = value.get("abstention_reason")
    if category == "unable_to_determine":
        if not _non_empty_str(abstention_reason):
            errors.append("regulatory_and_structural_uncertainty.abstention_reason is required and non-empty when structural_uncertainty_category is 'unable_to_determine'")
    elif abstention_reason is not None:
        errors.append("regulatory_and_structural_uncertainty.abstention_reason must be absent unless structural_uncertainty_category is 'unable_to_determine'")


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
            f"supporting artifact SS6.3, XASSET-0004 SS F) -- got {status!r}"
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
    every axis unambiguously treats as a genuine abstention (SS4.4).
    Deliberately does NOT treat correlation_and_volatility.
    cross_coin_correlation_status's 'not_yet_measured' value as an
    abstention here -- that value is a forced, determined default under
    XASSET-0004 SS E, not an evidence-gap abstention, the crypto-specific
    analogue of the same disclosed-not-silently-resolved ambiguity
    etf_classification_validator.py's docstring names for
    tracking_quality_category.not_yet_measured."""
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
    unreconciled against the axes it claims to summarize (SS9.1, and the
    exact defect etf_classification_validator.py's own v1.1 correction
    fixed, carried forward here from the start)."""
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

    custody = data.get("custody_and_counterparty_risk") or {}
    correlation = data.get("correlation_and_volatility") or {}
    risk_flags = data.get("structural_risk_flags")
    if not isinstance(risk_flags, dict):
        # Independent presence/type check, not folded only into the
        # projection-consistency comparison below -- carried forward from
        # etf_classification_validator.py's own v1.1 bounded correction
        # (a required envelope field with no independent absence/wrong-type
        # check was previously masked whenever the comparison below simply
        # no-oped on a missing field).
        errors.append("structural_risk_flags must be a mapping (SS6.1 required envelope field)")
    else:
        _reject_unknown_keys(risk_flags, "structural_risk_flags", _STRUCTURAL_RISK_FLAGS_ALLOWED_KEYS, errors)
        if isinstance(custody, dict) and isinstance(correlation, dict):
            expected_flags = {
                "custody_model": custody.get("custody_model"),
                "smart_contract_risk_category": custody.get("smart_contract_risk_category"),
                "cross_coin_correlation_status": correlation.get("cross_coin_correlation_status"),
            }
            if risk_flags != expected_flags:
                errors.append(
                    f"structural_risk_flags must exactly project custody_and_counterparty_risk's "
                    f"custody_model/smart_contract_risk_category and correlation_and_volatility's "
                    f"cross_coin_correlation_status (SS6.2) -- expected {expected_flags}, got {risk_flags}"
                )

    network = data.get("network_fundamentals") or {}
    liquidity = data.get("liquidity_and_market_structure") or {}
    valuation = data.get("valuation_and_economic_assessment_readiness") or {}
    handoff = data.get("cross_asset_handoff")
    if isinstance(handoff, dict):
        _reject_unknown_keys(handoff, "cross_asset_handoff", _CROSS_ASSET_HANDOFF_ALLOWED_KEYS, errors)
        missing = _CROSS_ASSET_HANDOFF_ALLOWED_KEYS - handoff.keys()
        if missing:
            errors.append(f"cross_asset_handoff missing required key(s): {sorted(missing)}")

        if isinstance(network, dict):
            expected_role_summary = (
                f"{network.get('consensus_mechanism')}"
                f" / {network.get('adoption_trend_category')}"
            )
            if handoff.get("role_summary") != expected_role_summary:
                errors.append(
                    f"cross_asset_handoff.role_summary must exactly equal "
                    f"'{{network_fundamentals.consensus_mechanism}} / "
                    f"{{network_fundamentals.adoption_trend_category}}' (SS6.4) -- expected "
                    f"{expected_role_summary!r}, got {handoff.get('role_summary')!r}"
                )
        if isinstance(eq, dict) and handoff.get("evidence_quality_summary") != eq.get("primary_source_coverage"):
            errors.append("cross_asset_handoff.evidence_quality_summary must exactly equal evidence_quality.primary_source_coverage (SS6.4)")
        if handoff.get("uncertainty_summary") != data.get("uncertainty_summary"):
            errors.append("cross_asset_handoff.uncertainty_summary must exactly equal the envelope's own uncertainty_summary (SS6.4)")
        if isinstance(liquidity, dict) and handoff.get("liquidity_risk_summary") != liquidity.get("liquidity_tier"):
            errors.append("cross_asset_handoff.liquidity_risk_summary must exactly equal liquidity_and_market_structure.liquidity_tier (SS6.4)")
        if isinstance(valuation, dict) and handoff.get("valuation_readiness") != valuation.get("status"):
            errors.append("cross_asset_handoff.valuation_readiness must exactly equal valuation_and_economic_assessment_readiness.status (SS6.4)")

        signal = handoff.get("overlap_or_correlation_signal")
        if isinstance(correlation, dict):
            expected_signal = correlation.get("cross_coin_correlation_status")
            if signal != expected_signal:
                errors.append(
                    f"cross_asset_handoff.overlap_or_correlation_signal must exactly project "
                    f"correlation_and_volatility.cross_coin_correlation_status (SS6.4) -- "
                    f"expected {expected_signal!r}, got {signal!r}"
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
            f"axis-equivalent fields plus the envelope/seal fields are permitted, no eighth "
            f"substantive judgment axis (XASSET-0002 supporting artifact SS4/SS6)"
        )


# ── public API: in-memory record validation ─────────────────────────────

def validate_crypto_classification_data(
    data: object,
    *,
    source: str | None = None,
    authorized_population: frozenset[str] = AUTHORIZED_POPULATION,
) -> ValidationResult:
    """Validate an already-parsed crypto classification mapping. Never
    touches the filesystem -- unlike the ETF validator's
    overlap_and_concentration live recompute against issuer_lookthrough.yaml,
    no equivalent live-recomputed mechanism covers cryptocurrency today
    (XASSET-0002 supporting artifact SS4.2: "no cluster cap or
    issuer-look-through mechanism currently covers cryptocurrency")."""
    errors: list[str] = []

    if not isinstance(data, dict):
        errors.append(f"root document must be a mapping, got {type(data).__name__}")
        return ValidationResult(valid=False, errors=errors, source=source)

    instrument_id = data.get("instrument_id")
    if not _non_empty_str(instrument_id):
        errors.append("instrument_id must be a non-empty string")
    elif authorized_population and instrument_id not in authorized_population:
        errors.append(
            f"instrument_id {instrument_id!r} is not in the authorized three-instrument "
            f"population {sorted(authorized_population)} (XASSET-0004 SS A.1) -- ZORA, WIF, "
            f"BONK, PEPE, HYPE, and every other coin are explicitly excluded from this batch"
        )

    asset_type = data.get("asset_type")
    if asset_type != ASSET_TYPE:
        errors.append(f"asset_type must be exactly {ASSET_TYPE!r} -- got {asset_type!r}")

    if not _non_empty_str(data.get("schema_version")):
        errors.append("schema_version must be a non-empty string")

    for axis, validator in (
        ("network_fundamentals", _validate_network_fundamentals),
        ("economic_model", _validate_economic_model),
        ("liquidity_and_market_structure", _validate_liquidity_and_market_structure),
        ("custody_and_counterparty_risk", _validate_custody_and_counterparty_risk),
        ("correlation_and_volatility", _validate_correlation_and_volatility),
        ("regulatory_and_structural_uncertainty", _validate_regulatory_and_structural_uncertainty),
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


def validate_crypto_classification_file(
    path: str | Path,
    *,
    authorized_population: frozenset[str] = AUTHORIZED_POPULATION,
) -> ValidationResult:
    path = Path(path)
    source = str(path)
    data, read_errors = _read_yaml(path)
    if read_errors:
        return ValidationResult(valid=False, errors=read_errors, source=source)

    result = validate_crypto_classification_data(
        data, source=source, authorized_population=authorized_population,
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


def validate_crypto_classification_directory(
    directory: str | Path,
    *,
    authorized_population: frozenset[str] = AUTHORIZED_POPULATION,
) -> DirectoryValidationResult:
    directory = Path(directory)
    if not directory.exists() or not directory.is_dir():
        return DirectoryValidationResult(valid=True, results=[])

    yaml_paths = sorted(p for p in directory.glob("*.yaml") if p.name != _MANIFEST_FILENAME)
    results = [
        validate_crypto_classification_file(p, authorized_population=authorized_population)
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
    _result = validate_crypto_classification_directory(
        _repo_root / "intelligence" / "crypto_classification",
    )
    if _result.valid:
        print(f"crypto_classification_validator: OK ({_result.record_count} result(s))")
        sys.exit(0)
    else:
        print("crypto_classification_validator: FAILED")
        for _r in _result.results:
            if not _r.valid:
                for _err in _r.errors:
                    print(f"  - [{_r.source}] {_err}")
        sys.exit(1)
