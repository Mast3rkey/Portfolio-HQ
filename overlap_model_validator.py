"""
overlap_model_validator.py -- read-only schema validator for the WS-0014
cross-asset overlap/concentration-model content batch, authored against the
overlap-model framework `governance/decisions/XASSET-0005-functional-
doctrine-and-overlap-concentration-architecture.md`'s supporting artifact
(`governance/audits/WS0014_FUNCTIONAL_DOCTRINE_AND_OVERLAP_CONCENTRATION_
ARCHITECTURE_DESIGN_20260808.md`, S6, as corrected by `XASSET-0007` SS B)
for the one implementation PR authorized by `governance/decisions/
XASSET-0007-ws0014-overlap-model-content-authorization.md`.

Scope, exactly what is validated (overlap-model schema only -- the
functional-doctrine schema S3 designed in the same supporting artifact is
out of scope for this module; `functional_doctrine_validator.py` already
implements and validates it, unmodified and untouched by this module):

- Source-of-truth convention: `intelligence/overlap_model/<DIMENSION_ID>.yaml`,
  one file per dimension, single-file (no paired Markdown), filesystem is
  the index, plus `COHORT_MANIFEST.yaml` -- mirrors every prior
  classification framework's own convention exactly.
- Exactly ten fixed `dimension_id` values, one record each, sharing one flat
  schema shape (S6.1's table, as corrected): `issuer_overlap_etf_lookthrough`,
  `economic_role_overlap`, `correlated_loss_mechanisms`,
  `sleeve_concentration`, `etf_direct_equity_duplication`,
  `crypto_correlation_interface`, `defensive_offset_interface`,
  `leverage_debt_interaction`, `geographic_currency_exposure`,
  `whole_portfolio_volatility_drawdown_concentration` -- no eleventh
  dimension, no ninth record type, no composite.
- Nine substantive fields on every record (S6.2): `dimension_id`,
  `schema_version`, `dimension_type` (`mechanical_rollup` |
  `narrative_evidence` | `interface_placeholder`), `source_mechanism`,
  `computation_status` (`computed_from_existing_mechanism` |
  `not_yet_computable_interface_only` | `requires_future_authorization`),
  `evidence_or_source_refs`, `output_shape`, `uncertainty_or_gap_disclosure`,
  `later_governance_action`, plus `record_status` and (when sealed) the five
  seal fields -- **no** `abstention_index` and **no** `cross_asset_handoff`
  sub-object on this schema (S6.2's own explicit design choices, unlike the
  functional-doctrine schema's envelope) and **zero numeric fields anywhere,
  with no carve-out of any kind** (stricter than the ETF framework's own
  scoped `expense_ratio_pct` exception -- S3.3/S6's zero-numeric-field
  design means this module's forbidden-key scan has nothing to exempt).
- `dimension_type` is fixed per `dimension_id` and mechanically two-way
  locked to `computation_status`: a record whose `dimension_type` is
  `interface_placeholder` must carry `computation_status:
  not_yet_computable_interface_only`, with **no exception, unconditional on
  whether the dimension's own cited `source_mechanism` now points at a
  populated, sealed record** (S6.2, corrected by `XASSET-0007` SS B to name
  all four `interface_placeholder` dimensions, not two) -- and conversely, a
  record carrying that forced value must have `dimension_type:
  interface_placeholder`. A `mechanical_rollup`/`narrative_evidence` record
  may be `computed_from_existing_mechanism` or `requires_future_
  authorization`, never the forced interface-only value (this two-way
  exclusivity is this module's own defensive tightening -- never a
  loosening -- of S6.2's one-way forced-value rule).
- `source_mechanism` is a required, non-empty list of citation strings that
  must equal **exactly** the closed per-`dimension_id` canonical set S6.1's
  table names (`_CANONICAL_SOURCE_MECHANISMS` below) -- no substitution, no
  subset, no addition of an uncited mechanism (S6.2: "a dimension record
  whose `source_mechanism` names a mechanism this artifact did not already
  identify in S6.1 is not authorized").
- `evidence_or_source_refs` is a required, non-empty list of non-empty
  pointer strings -- never a duplicated copy of the referenced values
  (S6.2), and independently free-text-scanned like every other string field.
- `output_shape` is a required, non-empty string describing a *future*
  computed record's shape only -- never a populated comparison value (S6.2).
- Exact ten-`dimension_id` population enforcement, no more, no fewer -- no
  eleventh dimension may be introduced without its own separate schema-
  amendment decision (S6.1, `XASSET-0007` SS A point 1).
- No composite overlap or risk score anywhere, at any level, in any single
  record or across the full ten-record set together (S6.3) -- a dedicated
  forbidden-pattern scan for `composite_score`, `overall_risk`,
  `aggregate_concentration`, `overlap_index`, `risk_rank`, or any bare
  `score`/`rank`/`index` key not already part of this schema's own named
  fields, applied both per-record and across the directory as a set.
- No cross-schema field-name leakage -- no equity- (`economic_role`,
  `capital_priority`, `risk_concentration`, `portfolio_role_ref`,
  `conviction`, `economic_system_ref`), ETF- (`structural_role`,
  `constituent_exposure`, `overlap_and_concentration`, `cost_and_tracking_
  quality`, `liquidity`, `structure_and_methodology`), crypto-
  (`network_fundamentals`, `economic_model`, `liquidity_and_market_
  structure`, `custody_and_counterparty_risk`, `correlation_and_volatility`,
  `regulatory_and_structural_uncertainty`), or functional-doctrine-shaped
  (`capital_use_type`, `functional_role`, `hard_constraint_status`,
  `economic_assessment_readiness`, `liquidity_character`, `capital_
  preservation_character`, `freshness_state`, `structural_reference`,
  `abstention_index`) field name anywhere in an overlap-model record (S7
  point 4) -- a dedicated forbidden-key scan applied at every nesting level.
- Allocator/margin decoupling -- zero import coupling with `allocate.py`/
  `margin_state.py` in either direction (S7 point 12). `leverage_debt_
  interaction`'s own `source_mechanism`/`evidence_or_source_refs` may
  **cite** `margin_state.classify_margin_state`'s existence and closed
  output vocabulary in prose; this validator module never imports it.
- No chart evidence leakage; no directive/trading-language leakage -- an
  independent free-text scan (not a self-declared flag) for the shared
  eight directive words (`buy`/`sell`/`add`/`hold`/`trim`/`exit`/`wait`/
  `stage`, word-boundary matched) and seventeen chart-domain terms (S7
  points 9/10) -- the four functional-doctrine-specific debt/cash verbs
  (`repay`/`redeploy`/`fund`/`draw`) are explicitly not required for this
  schema (`XASSET-0007` SS B's binding table) and are not scanned here.
- Closed schema at every level, rejecting extra keys, not just missing ones
  (the `contender_registry_validator.py` MAJAR-finding lesson, S8.1).
- Deterministic hashing (`canonical_record_hash`) excludes only the five
  seal fields -- `content_sha256` is independently recomputable and must
  match on every sealed record and every manifest row, bidirectionally.

This module is a validator, not a data producer. It never opens a file in
write/append/update mode, never creates a directory, and has zero import
relationship with `allocate.py` or `margin_state.py` in either direction. It
has zero import relationship with `functional_doctrine_validator.py` in
either direction -- the two schemas are validated by two fully independent
sibling modules, mirroring `etf_classification_validator.py`/
`crypto_classification_validator.py`'s own established precedent
(`XASSET-0006` SS A point 3's determination, made by this filing as "the
second content authorization exercised").
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from hashlib import sha256
from pathlib import Path

import yaml

# ── the closed ten-dimension population (XASSET-0005 SS6.1, corrected) ─────

ISSUER_OVERLAP_ETF_LOOKTHROUGH = "issuer_overlap_etf_lookthrough"
ECONOMIC_ROLE_OVERLAP = "economic_role_overlap"
CORRELATED_LOSS_MECHANISMS = "correlated_loss_mechanisms"
SLEEVE_CONCENTRATION = "sleeve_concentration"
ETF_DIRECT_EQUITY_DUPLICATION = "etf_direct_equity_duplication"
CRYPTO_CORRELATION_INTERFACE = "crypto_correlation_interface"
DEFENSIVE_OFFSET_INTERFACE = "defensive_offset_interface"
LEVERAGE_DEBT_INTERACTION = "leverage_debt_interaction"
GEOGRAPHIC_CURRENCY_EXPOSURE = "geographic_currency_exposure"
WHOLE_PORTFOLIO_VOLATILITY_DRAWDOWN_CONCENTRATION = "whole_portfolio_volatility_drawdown_concentration"

AUTHORIZED_POPULATION = frozenset({
    ISSUER_OVERLAP_ETF_LOOKTHROUGH,
    ECONOMIC_ROLE_OVERLAP,
    CORRELATED_LOSS_MECHANISMS,
    SLEEVE_CONCENTRATION,
    ETF_DIRECT_EQUITY_DUPLICATION,
    CRYPTO_CORRELATION_INTERFACE,
    DEFENSIVE_OFFSET_INTERFACE,
    LEVERAGE_DEBT_INTERACTION,
    GEOGRAPHIC_CURRENCY_EXPOSURE,
    WHOLE_PORTFOLIO_VOLATILITY_DRAWDOWN_CONCENTRATION,
})

_MECHANICAL_ROLLUP = "mechanical_rollup"
_NARRATIVE_EVIDENCE = "narrative_evidence"
_INTERFACE_PLACEHOLDER = "interface_placeholder"
_DIMENSION_TYPES = frozenset({_MECHANICAL_ROLLUP, _NARRATIVE_EVIDENCE, _INTERFACE_PLACEHOLDER})

# Fixed dimension_type per dimension_id (XASSET-0005 SS6.1's table) -- not a
# judgment field; a record's own dimension_type must match this mapping
# exactly for its dimension_id.
_DIMENSION_TYPE_BY_ID = {
    ISSUER_OVERLAP_ETF_LOOKTHROUGH: _MECHANICAL_ROLLUP,
    ECONOMIC_ROLE_OVERLAP: _NARRATIVE_EVIDENCE,
    CORRELATED_LOSS_MECHANISMS: _NARRATIVE_EVIDENCE,
    SLEEVE_CONCENTRATION: _MECHANICAL_ROLLUP,
    ETF_DIRECT_EQUITY_DUPLICATION: _MECHANICAL_ROLLUP,
    CRYPTO_CORRELATION_INTERFACE: _INTERFACE_PLACEHOLDER,
    DEFENSIVE_OFFSET_INTERFACE: _INTERFACE_PLACEHOLDER,
    LEVERAGE_DEBT_INTERACTION: _MECHANICAL_ROLLUP,
    GEOGRAPHIC_CURRENCY_EXPOSURE: _INTERFACE_PLACEHOLDER,
    WHOLE_PORTFOLIO_VOLATILITY_DRAWDOWN_CONCENTRATION: _INTERFACE_PLACEHOLDER,
}

INTERFACE_PLACEHOLDER_DIMENSIONS = frozenset({
    CRYPTO_CORRELATION_INTERFACE, DEFENSIVE_OFFSET_INTERFACE,
    GEOGRAPHIC_CURRENCY_EXPOSURE, WHOLE_PORTFOLIO_VOLATILITY_DRAWDOWN_CONCENTRATION,
})
assert INTERFACE_PLACEHOLDER_DIMENSIONS == frozenset(
    d for d, t in _DIMENSION_TYPE_BY_ID.items() if t == _INTERFACE_PLACEHOLDER
)

_MECHANICAL_OR_NARRATIVE_DIMENSIONS = AUTHORIZED_POPULATION - INTERFACE_PLACEHOLDER_DIMENSIONS

# ── computation_status (XASSET-0005 SS6.2, corrected by XASSET-0007 SS B) ──

_COMPUTED_FROM_EXISTING_MECHANISM = "computed_from_existing_mechanism"
_NOT_YET_COMPUTABLE_INTERFACE_ONLY = "not_yet_computable_interface_only"
_REQUIRES_FUTURE_AUTHORIZATION = "requires_future_authorization"
_COMPUTATION_STATUS_VALUES = frozenset({
    _COMPUTED_FROM_EXISTING_MECHANISM, _NOT_YET_COMPUTABLE_INTERFACE_ONLY, _REQUIRES_FUTURE_AUTHORIZATION,
})

# ── source_mechanism -- closed per-dimension canonical citation sets ───────
# (XASSET-0005 SS6.1's table, as corrected by XASSET-0007 SS B; a dimension
# record's source_mechanism must equal this set exactly -- no substitution,
# no subset, no addition of a mechanism the design did not already name.)

_CANONICAL_SOURCE_MECHANISMS: dict[str, frozenset[str]] = {
    ISSUER_OVERLAP_ETF_LOOKTHROUGH: frozenset({
        "issuer_lookthrough.yaml",
    }),
    ECONOMIC_ROLE_OVERLAP: frozenset({
        "intelligence/classification/<TICKER>.yaml:economic_role",
        "intelligence/etf_classification/<TICKER>.yaml:structural_role.role_category",
        "intelligence/crypto_classification/<TICKER>.yaml:network_fundamentals",
    }),
    CORRELATED_LOSS_MECHANISMS: frozenset({
        "intelligence/relationships/",
    }),
    SLEEVE_CONCENTRATION: frozenset({
        "targets.yaml:destination[].asset_class",
    }),
    ETF_DIRECT_EQUITY_DUPLICATION: frozenset({
        "intelligence/etf_classification/<TICKER>.yaml:overlap_and_concentration",
    }),
    CRYPTO_CORRELATION_INTERFACE: frozenset({
        "intelligence/crypto_classification/<TICKER>.yaml:correlation_and_volatility.cross_coin_correlation_status",
    }),
    DEFENSIVE_OFFSET_INTERFACE: frozenset({
        "intelligence/functional_doctrine/GLD_DEFENSIVE_ROLE.yaml:capital_preservation_character",
    }),
    LEVERAGE_DEBT_INTERACTION: frozenset({
        "margin_state.py:classify_margin_state",
        "intelligence/functional_doctrine/DEBT_REDUCTION.yaml:hard_constraint_status",
    }),
    GEOGRAPHIC_CURRENCY_EXPOSURE: frozenset({
        "intelligence/etf_classification/<TICKER>.yaml:constituent_exposure.geographic_concentration",
        "intelligence/etf_classification/<TICKER>.yaml:constituent_exposure.currency_exposure",
    }),
    WHOLE_PORTFOLIO_VOLATILITY_DRAWDOWN_CONCENTRATION: frozenset({
        "intelligence/crypto_classification/<TICKER>.yaml:correlation_and_volatility.historical_volatility_category",
    }),
}
assert set(_CANONICAL_SOURCE_MECHANISMS) == AUTHORIZED_POPULATION

# ── record_status / seal metadata -- same discipline as every prior
#    framework, reused unmodified ─────────────────────────────────────────

_RECORD_STATUSES = frozenset({"draft", "sealed"})
_SEAL_REQUIRED_KEYS = frozenset({
    "sealed_at", "governing_decision", "drafting_session_or_shard_id",
    "content_sha256", "cohort_manifest_entry",
})

_SUBSTANTIVE_FIELDS = frozenset({
    "dimension_id", "schema_version", "dimension_type", "source_mechanism",
    "computation_status", "evidence_or_source_refs", "output_shape",
    "uncertainty_or_gap_disclosure", "later_governance_action",
})
_ALL_TOP_LEVEL_KEYS = frozenset({
    *_SUBSTANTIVE_FIELDS, "record_status", *_SEAL_REQUIRED_KEYS,
})

# ── forbidden leakage (XASSET-0005 SS7 points 4/6, S6.3, SS8.1) ───────────

_EQUITY_FIELD_LEAKAGE = frozenset({
    "economic_role", "capital_priority", "risk_concentration",
    "portfolio_role_ref", "conviction", "economic_system_ref",
})
_ETF_FIELD_LEAKAGE = frozenset({
    "structural_role", "constituent_exposure", "overlap_and_concentration",
    "cost_and_tracking_quality", "liquidity", "structure_and_methodology",
})
_CRYPTO_FIELD_LEAKAGE = frozenset({
    "network_fundamentals", "economic_model", "liquidity_and_market_structure",
    "custody_and_counterparty_risk", "correlation_and_volatility",
    "regulatory_and_structural_uncertainty",
})
_FUNCTIONAL_DOCTRINE_FIELD_LEAKAGE = frozenset({
    "capital_use_type", "functional_role", "hard_constraint_status",
    "economic_assessment_readiness", "liquidity_character",
    "capital_preservation_character", "freshness_state",
    "structural_reference", "abstention_index",
})
_NUMERIC_LEAKAGE_KEYS = frozenset({
    "target_pct", "target_range", "max_position_size", "maximum_position_size",
    "conviction_score", "recommended_target_pct", "weight",
    "avoided_interest", "avoided_cost", "expected_return", "basis_points_saved",
})
# The no-composite-score rule, made structural (S6.3 point 2): a bare
# score/rank/index-shaped key, or an explicit aggregation-suggesting name,
# not already part of this schema's own nine named substantive fields.
_COMPOSITE_SCORE_KEYS = frozenset({
    "composite_score", "overall_risk", "aggregate_concentration",
    "overlap_index", "risk_rank", "score", "rank", "index", "ranking",
})
_FORBIDDEN_KEY_NAMES = frozenset({
    *_EQUITY_FIELD_LEAKAGE, *_ETF_FIELD_LEAKAGE, *_CRYPTO_FIELD_LEAKAGE,
    *_FUNCTIONAL_DOCTRINE_FIELD_LEAKAGE, *_NUMERIC_LEAKAGE_KEYS, *_COMPOSITE_SCORE_KEYS,
})
assert not (_FORBIDDEN_KEY_NAMES & _ALL_TOP_LEVEL_KEYS)

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

# Word-boundary matched so "hold" never flags "holdings", "exit" never
# flags "exiting", "add" never flags "address", and so on
# (recommendation_validator.py's own established design). This schema does
# not carry the four functional-doctrine-specific debt/cash verbs
# (repay/redeploy/fund/draw) -- XASSET-0007 SS B's binding table states
# they are "not required here" for the overlap-model schema, and this
# module shares no helper with functional_doctrine_validator.py that would
# otherwise pull them in.
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
    """SHA-256 of the record's full content (the nine substantive fields
    plus record_status), canonical sorted-key JSON, UTF-8 -- excludes every
    seal field, avoiding circular self-hashing."""
    hashable = {k: data.get(k) for k in sorted(_HASHABLE_KEYS)}
    canonical = json.dumps(hashable, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return sha256(canonical.encode("utf-8")).hexdigest()


# ── generic helpers ──────────────────────────────────────────────────────

def _non_empty_str(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _non_empty_str_list(value: object) -> bool:
    return (
        isinstance(value, list) and len(value) > 0
        and all(_non_empty_str(item) for item in value)
    )


def _reject_unknown_keys(value: dict, field_name: str, allowed: frozenset[str], errors: list[str]) -> None:
    unknown = set(value.keys()) - allowed
    if unknown:
        errors.append(
            f"{field_name} contains unexpected key(s) {sorted(unknown)} -- this schema is "
            f"closed; only {sorted(allowed)} are permitted (XASSET-0005 supporting artifact S6.2)"
        )


def _scan_forbidden_keys(value: object, path: str, errors: list[str]) -> None:
    """Structural scan: a forbidden key name anywhere in the document tree,
    not just at the top level (S7 points 4/6, S6.3 point 2)."""
    if isinstance(value, dict):
        for k, v in value.items():
            key_str = str(k)
            if key_str in _FORBIDDEN_KEY_NAMES:
                if key_str in _EQUITY_FIELD_LEAKAGE:
                    kind = "an equity-classification-shaped field"
                elif key_str in _ETF_FIELD_LEAKAGE:
                    kind = "an ETF-classification-shaped axis field"
                elif key_str in _CRYPTO_FIELD_LEAKAGE:
                    kind = "a crypto-classification-shaped axis field"
                elif key_str in _FUNCTIONAL_DOCTRINE_FIELD_LEAKAGE:
                    kind = "a functional-doctrine-shaped field"
                elif key_str in _COMPOSITE_SCORE_KEYS:
                    kind = "a composite-overlap/risk-score-shaped field (XASSET-0005 supporting artifact S6.3)"
                else:
                    kind = "a numeric target/rank/avoided-cost-shaped field"
                errors.append(
                    f"{path}.{key_str}: forbidden key name -- {kind} must never appear in an "
                    f"overlap-model record (XASSET-0005 supporting artifact SS7 points 4/6, S6.3)"
                )
            _scan_forbidden_keys(v, f"{path}.{key_str}", errors)
    elif isinstance(value, list):
        for i, item in enumerate(value):
            _scan_forbidden_keys(item, f"{path}[{i}]", errors)


def _scan_free_text_strings(value: object, path: str, errors: list[str]) -> None:
    """Recursively scan every free-text string value for forbidden
    recommendation-shaped phrases, directive/trading language, and
    chart-derived terminology -- an independent mechanism from whatever
    accepted this string into the document, not a self-declared flag
    (S8.1). Unlike the functional-doctrine schema, this schema has no
    provenance.sources citation-string exemption -- source_mechanism and
    evidence_or_source_refs are structural pointer strings (file paths and
    field names), not free citation prose, and are scanned identically to
    every other string field."""
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
                    f"{path}: contains directive word {pattern.pattern!r} -- no buy/sell/add/hold/"
                    f"trim/exit/wait/stage signal is permitted in any field, under any framing "
                    f"(XASSET-0005 supporting artifact S9 -- the overlap model computes evidence, "
                    f"not policy)"
                )
        for term, pattern in _CHART_PATTERNS:
            if pattern.search(value):
                errors.append(
                    f"{path}: contains chart-derived terminology {term!r} -- no chart evidence "
                    f"of any kind is permitted (XASSET-0005 supporting artifact SS7 point 9)"
                )


# ── field validators ─────────────────────────────────────────────────────

def _validate_dimension_id(data: dict, authorized_population: frozenset[str], errors: list[str]) -> str | None:
    dimension_id = data.get("dimension_id")
    if not _non_empty_str(dimension_id):
        errors.append("dimension_id must be a non-empty string")
        return None
    if authorized_population and dimension_id not in authorized_population:
        errors.append(
            f"dimension_id {dimension_id!r} is not in the authorized ten-dimension population "
            f"{sorted(authorized_population)} (XASSET-0005 supporting artifact S6.1) -- no "
            f"eleventh dimension is authorized without its own separate schema-amendment decision"
        )
        return None
    return dimension_id


def _validate_dimension_type(data: dict, dimension_id: str | None, errors: list[str]) -> None:
    dimension_type = data.get("dimension_type")
    if dimension_type not in _DIMENSION_TYPES:
        errors.append(f"dimension_type must be one of {sorted(_DIMENSION_TYPES)} -- got {dimension_type!r}")
        return
    if dimension_id is None or dimension_id not in _DIMENSION_TYPE_BY_ID:
        return
    expected = _DIMENSION_TYPE_BY_ID[dimension_id]
    if dimension_type != expected:
        errors.append(
            f"dimension_type must be exactly {expected!r} for dimension_id {dimension_id!r} "
            f"(XASSET-0005 supporting artifact S6.1's fixed dimension-type mapping) -- got "
            f"{dimension_type!r}"
        )


def _validate_source_mechanism(data: dict, dimension_id: str | None, errors: list[str]) -> None:
    value = data.get("source_mechanism")
    if not _non_empty_str_list(value):
        errors.append("source_mechanism must be a non-empty list of non-empty strings")
        return
    if dimension_id is None or dimension_id not in _CANONICAL_SOURCE_MECHANISMS:
        return
    expected = _CANONICAL_SOURCE_MECHANISMS[dimension_id]
    got = frozenset(value)
    if len(value) != len(got):
        errors.append("source_mechanism must not contain duplicate entries")
    if got != expected:
        errors.append(
            f"source_mechanism for dimension_id {dimension_id!r} must equal exactly "
            f"{sorted(expected)} (XASSET-0005 supporting artifact S6.1's own source_mechanism "
            f"citation, S6.2: 'a dimension record whose source_mechanism names a mechanism this "
            f"artifact did not already identify... is not authorized') -- got {sorted(got)}"
        )


def _validate_computation_status(data: dict, dimension_id: str | None, dimension_type: object, errors: list[str]) -> None:
    status = data.get("computation_status")
    if status not in _COMPUTATION_STATUS_VALUES:
        errors.append(f"computation_status must be one of {sorted(_COMPUTATION_STATUS_VALUES)} -- got {status!r}")
        return

    is_interface_placeholder = (
        dimension_type == _INTERFACE_PLACEHOLDER
        or (dimension_id is not None and dimension_id in INTERFACE_PLACEHOLDER_DIMENSIONS)
    )
    if is_interface_placeholder:
        if status != _NOT_YET_COMPUTABLE_INTERFACE_ONLY:
            errors.append(
                f"computation_status must be exactly {_NOT_YET_COMPUTABLE_INTERFACE_ONLY!r} for "
                f"an interface_placeholder dimension, with no exception -- unconditional on "
                f"whether the dimension's own cited source_mechanism now points at a populated, "
                f"sealed record (XASSET-0005 supporting artifact S6.2, corrected by XASSET-0007 "
                f"SS B; XASSET-0007 SS A point 2: 'changing this forced value for any dimension "
                f"requires its own separate, future, explicit schema-amendment decision') -- "
                f"got {status!r}"
            )
    else:
        if status == _NOT_YET_COMPUTABLE_INTERFACE_ONLY:
            errors.append(
                f"computation_status {_NOT_YET_COMPUTABLE_INTERFACE_ONLY!r} is reserved for the "
                f"four interface_placeholder dimensions -- a mechanical_rollup/narrative_evidence "
                f"dimension must be either {_COMPUTED_FROM_EXISTING_MECHANISM!r} or "
                f"{_REQUIRES_FUTURE_AUTHORIZATION!r}"
            )


def _validate_output_shape(data: dict, errors: list[str]) -> None:
    if not _non_empty_str(data.get("output_shape")):
        errors.append(
            "output_shape must be a non-empty string describing a future computed record's "
            "categorical shape -- never a populated comparison value (XASSET-0005 supporting "
            "artifact S6.2)"
        )


def _validate_evidence_or_source_refs(data: dict, errors: list[str]) -> None:
    if not _non_empty_str_list(data.get("evidence_or_source_refs")):
        errors.append("evidence_or_source_refs must be a non-empty list of non-empty strings")


def _validate_uncertainty_or_gap_disclosure(data: dict, errors: list[str]) -> None:
    if not _non_empty_str(data.get("uncertainty_or_gap_disclosure")):
        errors.append("uncertainty_or_gap_disclosure must be a non-empty string")


def _validate_later_governance_action(data: dict, errors: list[str]) -> None:
    if "later_governance_action" not in data:
        errors.append("record missing required field: later_governance_action")
    elif not _non_empty_str(data.get("later_governance_action")):
        errors.append("later_governance_action must be a non-empty string (use 'none' literally when nothing is implied)")


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
            f"record contains unexpected top-level field(s) {sorted(stray)} -- exactly the nine "
            f"substantive fields plus record_status plus the five seal fields are permitted; no "
            f"abstention_index and no cross_asset_handoff sub-object on this schema (XASSET-0005 "
            f"supporting artifact S6.2's own explicit design choices)"
        )


# ── public API: in-memory record validation ─────────────────────────────

def validate_overlap_model_data(
    data: object,
    *,
    source: str | None = None,
    authorized_population: frozenset[str] = AUTHORIZED_POPULATION,
) -> ValidationResult:
    """Validate an already-parsed overlap-model dimension-record mapping.
    Never touches the filesystem."""
    errors: list[str] = []

    if not isinstance(data, dict):
        errors.append(f"root document must be a mapping, got {type(data).__name__}")
        return ValidationResult(valid=False, errors=errors, source=source)

    dimension_id = _validate_dimension_id(data, authorized_population, errors)

    if not _non_empty_str(data.get("schema_version")):
        errors.append("schema_version must be a non-empty string")

    if "dimension_type" not in data:
        errors.append("record missing required field: dimension_type")
    else:
        _validate_dimension_type(data, dimension_id, errors)

    if "source_mechanism" not in data:
        errors.append("record missing required field: source_mechanism")
    else:
        _validate_source_mechanism(data, dimension_id, errors)

    if "computation_status" not in data:
        errors.append("record missing required field: computation_status")
    else:
        _validate_computation_status(data, dimension_id, data.get("dimension_type"), errors)

    if "evidence_or_source_refs" not in data:
        errors.append("record missing required field: evidence_or_source_refs")
    else:
        _validate_evidence_or_source_refs(data, errors)

    if "output_shape" not in data:
        errors.append("record missing required field: output_shape")
    else:
        _validate_output_shape(data, errors)

    if "uncertainty_or_gap_disclosure" not in data:
        errors.append("record missing required field: uncertainty_or_gap_disclosure")
    else:
        _validate_uncertainty_or_gap_disclosure(data, errors)

    _validate_later_governance_action(data, errors)
    _validate_no_stray_top_level_fields(data, errors)
    _validate_seal(data, errors)
    _scan_forbidden_keys(data, str(dimension_id) if dimension_id else "<record>", errors)
    _scan_free_text_strings(data, str(dimension_id) if dimension_id else "<record>", errors)

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


def validate_overlap_model_file(
    path: str | Path,
    *,
    authorized_population: frozenset[str] = AUTHORIZED_POPULATION,
) -> ValidationResult:
    path = Path(path)
    source = str(path)
    data, read_errors = _read_yaml(path)
    if read_errors:
        return ValidationResult(valid=False, errors=read_errors, source=source)

    result = validate_overlap_model_data(data, source=source, authorized_population=authorized_population)

    if isinstance(data, dict) and _non_empty_str(data.get("dimension_id")):
        expected_stem = data["dimension_id"]
        if path.stem != expected_stem:
            result.errors.append(
                f"filename stem {path.stem!r} does not match the record's own dimension_id {expected_stem!r}"
            )
            result.valid = False

    return result


_MANIFEST_FILENAME = "COHORT_MANIFEST.yaml"
_MANIFEST_REQUIRED_ROW_KEYS = frozenset({
    "dimension_id", "sealed_at", "content_sha256", "schema_version", "governing_decision", "record_path",
})
_MANIFEST_ROW_ALLOWED_KEYS = _MANIFEST_REQUIRED_ROW_KEYS
_MANIFEST_TOP_LEVEL_ALLOWED_KEYS = frozenset({"schema_version", "governing_decision", "cohort"})


def validate_cohort_manifest(
    manifest_data: object,
    records_by_dimension_id: dict[str, dict],
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

        dimension_id = row["dimension_id"]
        if dimension_id in seen:
            errors.append(f"cohort manifest lists {dimension_id!r} more than once")
        seen.add(dimension_id)

        record = records_by_dimension_id.get(dimension_id)
        if record is None:
            errors.append(f"cohort[{i}] dimension_id {dimension_id!r} has no corresponding sealed record file")
            continue

        expected_hash = canonical_record_hash(record)
        if row["content_sha256"] != expected_hash:
            errors.append(f"cohort[{i}] ({dimension_id!r}) content_sha256 mismatch -- manifest {row['content_sha256']!r}, recomputed {expected_hash!r}")
        if record.get("content_sha256") != row["content_sha256"]:
            errors.append(f"cohort[{i}] ({dimension_id!r}) manifest content_sha256 does not match the record's own recorded content_sha256")

    if authorized_population:
        missing_from_manifest = authorized_population - seen
        if missing_from_manifest:
            errors.append(f"cohort manifest is missing authorized dimension_id(s): {sorted(missing_from_manifest)}")
        extra = seen - authorized_population
        if extra:
            errors.append(f"cohort manifest lists dimension_id(s) outside the authorized population: {sorted(extra)}")

    orphans = set(records_by_dimension_id) - seen
    if orphans:
        errors.append(f"sealed record(s) exist with no corresponding cohort manifest entry: {sorted(orphans)}")

    return ValidationResult(valid=not errors, errors=errors, source=_MANIFEST_FILENAME)


def validate_overlap_model_directory(
    directory: str | Path,
    *,
    authorized_population: frozenset[str] = AUTHORIZED_POPULATION,
) -> DirectoryValidationResult:
    directory = Path(directory)
    if not directory.exists() or not directory.is_dir():
        return DirectoryValidationResult(valid=True, results=[])

    yaml_paths = sorted(p for p in directory.glob("*.yaml") if p.name != _MANIFEST_FILENAME)
    results = [
        validate_overlap_model_file(p, authorized_population=authorized_population)
        for p in yaml_paths
    ]

    records_by_dimension_id: dict[str, dict] = {}
    for p in yaml_paths:
        data, read_errors = _read_yaml(p)
        if not read_errors and isinstance(data, dict) and _non_empty_str(data.get("dimension_id")):
            records_by_dimension_id[data["dimension_id"]] = data

    manifest_path = directory / _MANIFEST_FILENAME
    if manifest_path.is_file():
        manifest_data, read_errors = _read_yaml(manifest_path)
        if read_errors:
            results.append(ValidationResult(valid=False, errors=read_errors, source=str(manifest_path)))
        else:
            results.append(
                validate_cohort_manifest(manifest_data, records_by_dimension_id, authorized_population=authorized_population)
            )
    elif records_by_dimension_id:
        results.append(
            ValidationResult(
                valid=False,
                errors=[f"{_MANIFEST_FILENAME} is required whenever sealed records exist"],
                source=str(directory),
            )
        )

    # No composite overlap or risk score anywhere across the full set
    # together, not merely within one record (S6.3 point 2) -- each
    # individual record is already scanned by validate_overlap_model_file
    # above; this second pass re-runs the identical forbidden-key scan
    # against the combined document tree of all records read this pass, so
    # a future attempt to smuggle a composite in via a field that happens
    # to validate cleanly in isolation (e.g. split across two records) is
    # still caught when the set is considered together.
    combined_errors: list[str] = []
    _scan_forbidden_keys(list(records_by_dimension_id.values()), "<full ten-record set>", combined_errors)
    if combined_errors:
        results.append(ValidationResult(valid=False, errors=combined_errors, source="<combined ten-record set scan>"))

    return DirectoryValidationResult(valid=all(r.valid for r in results), results=results)


if __name__ == "__main__":
    import sys

    _repo_root = Path(__file__).resolve().parent
    _result = validate_overlap_model_directory(_repo_root / "intelligence" / "overlap_model")
    if _result.valid:
        print(f"overlap_model_validator: OK ({_result.record_count} result(s))")
        sys.exit(0)
    else:
        print("overlap_model_validator: FAILED")
        for _r in _result.results:
            if not _r.valid:
                for _err in _r.errors:
                    print(f"  - [{_r.source}] {_err}")
        sys.exit(1)
