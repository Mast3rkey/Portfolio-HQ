"""
functional_doctrine_validator.py -- read-only schema validator for the
first WS-0014 functional-doctrine (cash/reserve/GLD-defensive-role/
debt-reduction) content batch, authored against the functional-doctrine
framework `governance/decisions/XASSET-0005-functional-doctrine-and-
overlap-concentration-architecture.md`'s supporting artifact
(`governance/audits/WS0014_FUNCTIONAL_DOCTRINE_AND_OVERLAP_CONCENTRATION_
ARCHITECTURE_DESIGN_20260808.md`, SS3) designed, for the one implementation
PR authorized by `governance/decisions/XASSET-0006-ws0014-functional-
doctrine-content-authorization.md`.

Scope, exactly what is validated (functional-doctrine schema only -- the
overlap-model schema SS6 designed in the same supporting artifact is
explicitly out of scope for this module and this implementation; no
`intelligence/overlap_model/` file exists or is validated here):

- Source-of-truth convention: `intelligence/functional_doctrine/
  <CAPITAL_USE_TYPE>.yaml`, one file per capital-use type, single-file (no
  paired Markdown), filesystem is the index, plus `COHORT_MANIFEST.yaml` --
  mirrors the ETF/crypto classification frameworks' own convention exactly.
- Exactly six substantive axis fields plus `evidence_quality` on every
  record (SS3.1's "Result" line): `functional_role`, `hard_constraint_
  status`, `economic_assessment_readiness`, `liquidity_character`,
  `capital_preservation_character`, `freshness_state`, `evidence_quality`
  -- no seventh substantive judgment axis, no numeric field of any kind
  anywhere, with **no** carve-out of any kind (SS3.3's closing statement --
  stricter than the ETF framework's own scoped `expense_ratio_pct`
  exception).
- A shared envelope (SS3.3): `capital_use_type`, `schema_version`,
  `provenance`, `evidence_quality_status`, `uncertainty_summary`,
  `structural_risk_flags`, `record_status`, `structural_reference`
  (present only when `capital_use_type: GLD_DEFENSIVE_ROLE`, forbidden
  otherwise), `later_governance_action`, `abstention_index`, plus one
  `cross_asset_handoff` sub-object carrying six read-only-projection
  fields: `role_summary`, `evidence_quality_summary`, `uncertainty_
  summary`, `liquidity_risk_summary`, `hard_constraint_signal`, `economic_
  assessment_readiness_summary` -- the last two are the two "deliberately
  un-merged projections" SS3.3 requires, never sharing a field or a
  computation with each other.
- `economic_assessment_readiness` is `capital_use_type`-conditional
  (SS3.2, SS3.5): a single-part `{status, rationale}` shape for `CASH`/
  `RESERVE`/`GLD_DEFENSIVE_ROLE`; a two-part shape (`avoided_borrowing_
  cost_readiness`, `survivability_and_buffer_benefit_readiness`, each its
  own independent `{status, rationale}`, never blended into one figure)
  for `DEBT_REDUCTION` only. Every `status` sub-field, in either shape, is
  forced to exactly `assessment_required` on every record, zero exception
  (SS3.2, mirroring `recommendation_validator.py`'s SS G.4/SS G.5 forced-
  value check and `etf_classification_validator.py`'s SS6.3 identical
  design).
- `hard_constraint_status` and `economic_assessment_readiness` are
  validated by fully separate code paths with no shared helper function
  that reads both (SS3.2's "may never be computed from, derived from, or
  overridden by" requirement, SS7 point 5) -- `_validate_hard_constraint_
  status` never inspects `economic_assessment_readiness` and vice versa;
  `test_functional_doctrine_validator.py` includes a dedicated mutation
  test proving this.
- `structural_reference` -- required, all four sub-fields present, when
  and only when `capital_use_type: GLD_DEFENSIVE_ROLE`; forbidden (rejected
  as an unknown key) otherwise. `referenced_content_sha256` is
  independently, live-recomputed via a **read-only** call to
  `etf_classification_validator.canonical_record_hash()` against the
  current sealed `intelligence/etf_classification/GLD.yaml` and must match
  exactly -- a mismatch means the reference is stale and the record is
  rejected until refreshed (SS3.4, SS7 point 8). None of the ETF
  framework's own six axis key names (`structural_role`, `constituent_
  exposure`, `overlap_and_concentration`, `cost_and_tracking_quality`,
  `liquidity`, `structure_and_methodology`) may appear anywhere in a
  `GLD_DEFENSIVE_ROLE` record, at any nesting level.
- Two genuinely distinct abstention semantics per SS3.6, never conflated:
  `not_applicable` (a structurally absent axis -- e.g. `DEBT_REDUCTION`'s
  own `liquidity_character`) versus `unable_to_determine`/`unable_to_
  determine_freshness` (a genuine evidence gap, always paired with a
  required, non-empty `abstention_reason`). Abstention does not cascade
  between axes. `hard_constraint_status` has no abstention path at all --
  it is a citation-backed structural fact, not a judgment (SS3.2).
- Exact four-capital-use-type population enforcement (`CASH`, `RESERVE`,
  `GLD_DEFENSIVE_ROLE`, `DEBT_REDUCTION`), no more, no fewer -- no fifth
  value may be introduced without its own separate schema-amendment
  decision (SS3.2, `XASSET-0006` SS A.1).
- Closed schema at every level (envelope, per-axis, `structural_
  reference`, both `economic_assessment_readiness` shapes, provenance
  source, manifest row) -- an explicit permitted-key set per level,
  rejecting any unknown key, learning directly from `contender_registry_
  validator.py`'s own independent-review-found MAJOR gap (a denylist that
  checked only the missing side of a schema check) and `etf_classification_
  validator.py`'s own disclosed MINOR-1 finding (a required envelope field
  with no independent presence/type check) -- SS7 points 2/8, SS8.1.
- No equity-shaped field leakage (`economic_role`, `capital_priority`,
  `risk_concentration`, `portfolio_role_ref`, `conviction`), no ETF-shaped
  field leakage (the six ETF axis names above), and no crypto-shaped field
  leakage (`network_fundamentals`, `economic_model`, `liquidity_and_
  market_structure`, `custody_and_counterparty_risk`, `correlation_and_
  volatility`, `regulatory_and_structural_uncertainty`) anywhere in the
  document tree (SS7 point 4).
- No numeric score/rank/target/avoided-cost leakage anywhere (SS7 point 6)
  -- `target_pct`, `target_range`, `max_position_size`, `maximum_position_
  size`, `score`, `rank`, `ranking`, `conviction_score`, `recommended_
  target_pct`, `weight`, `avoided_interest`, `avoided_cost`, `expected_
  return`, `basis_points_saved` -- with **no** carve-out of any kind
  (unlike the ETF framework's own scoped `expense_ratio_pct` exception).
- An independent free-text scan (not a self-declared flag) for: forbidden
  recommendation-shaped phrases; directive/trading language -- the shared
  eight words (`buy`/`sell`/`add`/`hold`/`trim`/`exit`/`wait`/`stage`)
  plus four debt/cash-specific verbs (`repay`/`redeploy`/`fund`/`draw`),
  word-boundary matched (SS7 point 10) -- with a targeted exemption for
  `provenance.sources[].source_identifier`/`.limitation` (pure citation
  strings, never judgment prose), since "fund"/"funded" is a legitimate,
  common noun in real ETF/fund citation text (e.g. "SPDR Gold Shares (GLD)
  fund page") that a bare word-boundary match cannot otherwise distinguish
  from the directive verb; chart-domain terminology (seventeen terms) --
  learning directly from `reconciliation_validator.py`'s own disclosed
  MINOR defense-in-depth gap (SS8.1) rather than repeating it.
- Deterministic hashing (`canonical_record_hash`) excludes only the five
  seal fields (`sealed_at`, `governing_decision`, `drafting_session_or_
  shard_id`, `content_sha256`, `cohort_manifest_entry`) -- `content_
  sha256` is independently recomputable and must match on every sealed
  record and every manifest row, bidirectionally.

This module is a validator, not a data producer. It never opens a file in
write/append/update mode, never creates a directory, and has zero import
relationship with `allocate.py` or `margin_state.py` in either direction.
It imports `etf_classification_validator` for exactly one read-only public
function (`canonical_record_hash`) to implement the GLD structural-
reference hash-pin -- no other cross-module coupling.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from hashlib import sha256
from pathlib import Path

import yaml

import etf_classification_validator as _etf

AUTHORIZED_POPULATION = frozenset({"CASH", "RESERVE", "GLD_DEFENSIVE_ROLE", "DEBT_REDUCTION"})
_GLD_ONLY_TYPE = "GLD_DEFENSIVE_ROLE"
_DEBT_REDUCTION_TYPE = "DEBT_REDUCTION"

_ASSESSMENT_REQUIRED_VALUE = "assessment_required"
_UNABLE_TO_DETERMINE_VALUE = "unable_to_determine"
_UNABLE_TO_DETERMINE_FRESHNESS_VALUE = "unable_to_determine_freshness"

# ── functional_role (SS3.2) ─────────────────────────────────────────────────

_FUNCTIONAL_ROLE_CATEGORIES = frozenset({
    "operational_liquidity_float", "capital_preservation_buffer",
    "defensive_offset_or_ballast", "leverage_reduction", "other_functional_role",
    _UNABLE_TO_DETERMINE_VALUE,
})
_FUNCTIONAL_ROLE_ALLOWED_KEYS = frozenset({"role_category", "role_basis", "abstention_reason"})

# ── hard_constraint_status (SS3.2) -- no abstention path ────────────────────

_NONE_CURRENTLY_BINDING = "none_currently_binding"
_HARD_CONSTRAINT_ALLOWED_KEYS = frozenset({"binding", "constraint_source"})

# ── economic_assessment_readiness (SS3.2, SS3.5) ────────────────────────────

_READINESS_SUB_ALLOWED_KEYS = frozenset({"status", "rationale"})
_DEBT_REDUCTION_READINESS_ALLOWED_KEYS = frozenset({
    "avoided_borrowing_cost_readiness", "survivability_and_buffer_benefit_readiness",
})

# ── liquidity_character (SS3.2) ─────────────────────────────────────────────

_LIQUIDITY_CATEGORY_VALUES = frozenset({
    "immediately_liquid", "liquid_via_referenced_structural_asset",
    "not_applicable", _UNABLE_TO_DETERMINE_VALUE,
})
_LIQUIDITY_CHARACTER_ALLOWED_KEYS = frozenset({"liquidity_category", "abstention_reason"})

# ── capital_preservation_character (SS3.2) ──────────────────────────────────

_CAPITAL_PRESERVATION_CATEGORY_VALUES = frozenset({
    "principal_stable_no_market_risk", "market_exposed_via_referenced_structural_asset",
    "reduces_liability_not_an_asset", _UNABLE_TO_DETERMINE_VALUE,
})
_CAPITAL_PRESERVATION_CHARACTER_ALLOWED_KEYS = frozenset({
    "capital_preservation_category", "abstention_reason",
})

# ── freshness_state (SS3.2) ─────────────────────────────────────────────────

_FRESHNESS_STATUS_VALUES = frozenset({
    "current", "stale_needs_refresh", _UNABLE_TO_DETERMINE_FRESHNESS_VALUE,
})
_FRESHNESS_STATE_ALLOWED_KEYS = frozenset({"status", "as_of_reference", "abstention_reason"})

# ── evidence_quality (SS3.2) -- cannot itself abstain ───────────────────────

_PRIMARY_SOURCE_COVERAGE_VALUES = frozenset({"comprehensive", "partial", "limited"})
_EVIDENCE_QUALITY_ALLOWED_KEYS = frozenset({
    "primary_source_coverage", "thesis_uncertainty_statement",
})

# ── provenance (SS3.3) ───────────────────────────────────────────────────────

_SOURCE_TYPE_VALUES = frozenset({"primary", "secondary"})
_ACCESS_STATUS_VALUES = frozenset({
    "directly_inspected", "consulted_via_search_aggregation", "attempted_not_directly_inspected",
})
_SOURCE_ALLOWED_KEYS = frozenset({
    "source_identifier", "source_type", "as_of_date", "access_status", "limitation",
})
_SOURCE_REQUIRED_KEYS = frozenset({"source_identifier", "source_type", "as_of_date", "access_status"})
_PROVENANCE_ALLOWED_KEYS = frozenset({"sources"})
_CITATION_FIELD_NAMES = frozenset({"source_identifier", "limitation"})

# ── structural_reference (SS3.4) -- GLD_DEFENSIVE_ROLE only ────────────────

_STRUCTURAL_REFERENCE_ALLOWED_KEYS = frozenset({
    "source_instrument_id", "source_schema", "source_file", "referenced_content_sha256",
})
_STRUCTURAL_REFERENCE_REQUIRED_KEYS = _STRUCTURAL_REFERENCE_ALLOWED_KEYS
_EXPECTED_SOURCE_INSTRUMENT_ID = "GLD"
_EXPECTED_SOURCE_SCHEMA = "etf_classification"
_EXPECTED_SOURCE_FILE = "intelligence/etf_classification/GLD.yaml"

# ETF framework's own six axis key names -- must never appear anywhere in a
# GLD_DEFENSIVE_ROLE record, at any nesting level (SS3.4 point 3).
_ETF_AXIS_KEY_NAMES = frozenset({
    "structural_role", "constituent_exposure", "overlap_and_concentration",
    "cost_and_tracking_quality", "liquidity", "structure_and_methodology",
})

# ── structural_risk_flags / cross_asset_handoff (SS3.3) ────────────────────

_STRUCTURAL_RISK_FLAGS_ALLOWED_KEYS = frozenset({"binding", "capital_preservation_category"})
_HARD_CONSTRAINT_SIGNAL_ALLOWED_KEYS = frozenset({"binding", "constraint_source"})
_CROSS_ASSET_HANDOFF_ALLOWED_KEYS = frozenset({
    "role_summary", "evidence_quality_summary", "uncertainty_summary",
    "liquidity_risk_summary", "hard_constraint_signal", "economic_assessment_readiness_summary",
})

# ── abstention_index (SS3.3) ────────────────────────────────────────────────

_ABSTENTION_ENTRY_ALLOWED_KEYS = frozenset({"axis", "field", "value", "reason"})

# ── record_status / seal metadata ───────────────────────────────────────────

_RECORD_STATUSES = frozenset({"draft", "sealed"})
_SEAL_REQUIRED_KEYS = frozenset({
    "sealed_at", "governing_decision", "drafting_session_or_shard_id",
    "content_sha256", "cohort_manifest_entry",
})

_AXIS_NAMES = (
    "functional_role", "hard_constraint_status", "economic_assessment_readiness",
    "liquidity_character", "capital_preservation_character", "freshness_state",
    "evidence_quality",
)
_ENVELOPE_ONLY_KEYS = frozenset({
    "schema_version", "capital_use_type", "provenance",
    "uncertainty_summary", "evidence_quality_status", "structural_risk_flags",
    "record_status", "structural_reference", "later_governance_action",
    "cross_asset_handoff", "abstention_index",
})
_ALL_TOP_LEVEL_KEYS = frozenset({*_ENVELOPE_ONLY_KEYS, *_AXIS_NAMES, *_SEAL_REQUIRED_KEYS})
# structural_reference is conditionally present (GLD_DEFENSIVE_ROLE only) --
# excluded from the hashable set exactly like every other envelope field is
# included; it participates in hashing when present, absent otherwise (the
# dict-comprehension in canonical_record_hash naturally handles this via
# data.get(k), which returns None for the other three capital-use types).

# ── forbidden leakage (SS7 points 4/6, SS8.1) ───────────────────────────────

_EQUITY_FIELD_LEAKAGE = frozenset({
    "economic_role", "capital_priority", "risk_concentration",
    "portfolio_role_ref", "conviction", "economic_system_ref",
})
_CRYPTO_FIELD_LEAKAGE = frozenset({
    "network_fundamentals", "economic_model", "liquidity_and_market_structure",
    "custody_and_counterparty_risk", "correlation_and_volatility",
    "regulatory_and_structural_uncertainty",
})
_NUMERIC_LEAKAGE_KEYS = frozenset({
    "target_pct", "target_range", "max_position_size", "maximum_position_size",
    "score", "rank", "ranking", "conviction_score", "recommended_target_pct", "weight",
    "avoided_interest", "avoided_cost", "expected_return", "basis_points_saved",
})
_FORBIDDEN_KEY_NAMES = frozenset({
    *_EQUITY_FIELD_LEAKAGE, *_CRYPTO_FIELD_LEAKAGE, *_ETF_AXIS_KEY_NAMES, *_NUMERIC_LEAKAGE_KEYS,
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

# Word-boundary matched so "hold" never flags the noun "holdings", "exit"
# never flags "exiting", "add" never flags "address", and so on
# (recommendation_validator.py's own established design). The four
# debt/cash-specific verbs are new to this schema (SS7 point 10) -- "fund"
# in particular is a legitimate common noun in real citation text (see the
# module docstring), handled via a targeted citation-field exemption in
# `_scan_free_text_strings`, not a weakened pattern.
_DIRECTIVE_WORDS = (
    "buy", "sell", "add", "hold", "trim", "exit", "wait", "stage",
    "repay", "redeploy", "fund", "draw",
)
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
    """SHA-256 of the record's full content (envelope + all six
    axis-equivalent fields + evidence_quality), canonical sorted-key JSON,
    UTF-8 -- excludes every seal field, avoiding circular self-hashing.
    `structural_reference` naturally participates only when present
    (`CASH`/`RESERVE`/`DEBT_REDUCTION` records simply have no such key, so
    `data.get(...)` returns `None` for it, same as any other absent key)."""
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
            f"closed; only {sorted(allowed)} are permitted (XASSET-0005 supporting artifact SS3)"
        )


def _scan_forbidden_keys(value: object, path: str, errors: list[str]) -> None:
    """Structural scan: a forbidden key name anywhere in the document tree,
    not just at the top level (SS7 point 4/6)."""
    if isinstance(value, dict):
        for k, v in value.items():
            key_str = str(k)
            if key_str in _FORBIDDEN_KEY_NAMES:
                if key_str in _EQUITY_FIELD_LEAKAGE:
                    kind = "an equity-classification-shaped field"
                elif key_str in _CRYPTO_FIELD_LEAKAGE:
                    kind = "a crypto-classification-shaped field"
                elif key_str in _ETF_AXIS_KEY_NAMES:
                    kind = "an ETF-classification-shaped axis field"
                else:
                    kind = "a numeric score/rank/target/avoided-cost-shaped field"
                errors.append(
                    f"{path}.{key_str}: forbidden key name -- {kind} must never appear in a "
                    f"functional-doctrine record (XASSET-0005 supporting artifact SS7 points 4/6)"
                )
            _scan_forbidden_keys(v, f"{path}.{key_str}", errors)
    elif isinstance(value, list):
        for i, item in enumerate(value):
            _scan_forbidden_keys(item, f"{path}[{i}]", errors)


def _scan_free_text_strings(value: object, path: str, errors: list[str], *, in_citation: bool = False) -> None:
    """Recursively scan every free-text string value for forbidden
    recommendation-shaped phrases, directive/trading language, and
    chart-derived terminology -- an independent mechanism from whatever
    accepted this string into the document, not a self-declared flag
    (SS8.1). `provenance.sources[].source_identifier`/`.limitation` are
    pure citation strings (never judgment prose) and are exempted from the
    directive-word check only -- forbidden-phrase and chart-term checks
    still apply to them, since neither is a legitimate citation-text
    concern the way "fund"/"funded" is."""
    if isinstance(value, dict):
        for k, v in value.items():
            child_in_citation = in_citation or (str(k) in _CITATION_FIELD_NAMES)
            _scan_free_text_strings(v, f"{path}.{k}", errors, in_citation=child_in_citation)
    elif isinstance(value, list):
        for i, item in enumerate(value):
            _scan_free_text_strings(item, f"{path}[{i}]", errors, in_citation=in_citation)
    elif isinstance(value, str):
        for pattern in _FORBIDDEN_TEXT_PATTERNS:
            if pattern.search(value):
                errors.append(f"{path}: contains forbidden recommendation-shaped phrase matching {pattern.pattern!r}")
        if not in_citation:
            for pattern in _DIRECTIVE_PATTERNS:
                if pattern.search(value):
                    errors.append(
                        f"{path}: contains directive word {pattern.pattern!r} -- no buy/sell/add/"
                        f"hold/trim/exit/wait/stage/repay/redeploy/fund/draw signal is permitted "
                        f"in any field, under any framing (XASSET-0005 supporting artifact SS3.2 "
                        f"per-axis prohibited-inference statements)"
                    )
        for term, pattern in _CHART_PATTERNS:
            if pattern.search(value):
                errors.append(
                    f"{path}: contains chart-derived terminology {term!r} -- no chart evidence "
                    f"of any kind is permitted (XASSET-0005 supporting artifact SS7 point 9)"
                )


# ── per-axis validators ─────────────────────────────────────────────────

def _validate_functional_role(value: object, errors: list[str]) -> None:
    if not _require_keys(value, "functional_role", frozenset({"role_category"}), errors):
        return
    value = value  # type: dict
    _reject_unknown_keys(value, "functional_role", _FUNCTIONAL_ROLE_ALLOWED_KEYS, errors)

    category = value.get("role_category")
    if category not in _FUNCTIONAL_ROLE_CATEGORIES:
        errors.append(
            f"functional_role.role_category must be one of {sorted(_FUNCTIONAL_ROLE_CATEGORIES)} "
            f"(XASSET-0005 supporting artifact SS3.2) -- got {category!r}"
        )
        return

    role_basis = value.get("role_basis")
    if category == "other_functional_role":
        if not _non_empty_str(role_basis):
            errors.append("functional_role.role_basis is required and non-empty when role_category is 'other_functional_role'")
    elif role_basis is not None:
        errors.append("functional_role.role_basis must be absent unless role_category is 'other_functional_role'")

    abstention_reason = value.get("abstention_reason")
    if category == _UNABLE_TO_DETERMINE_VALUE:
        if not _non_empty_str(abstention_reason):
            errors.append("functional_role.abstention_reason is required and non-empty when role_category is 'unable_to_determine'")
    elif abstention_reason is not None:
        errors.append("functional_role.abstention_reason must be absent unless role_category is 'unable_to_determine'")


def _validate_hard_constraint_status(value: object, errors: list[str]) -> None:
    """SS3.2: no abstention path -- a citation-backed structural fact. This
    function must never inspect `economic_assessment_readiness` in any way
    (SS7 point 5's structural-independence requirement, enforced by keeping
    this a fully separate function with no shared helper)."""
    if not _require_keys(value, "hard_constraint_status", frozenset({"binding"}), errors):
        return
    value = value  # type: dict
    _reject_unknown_keys(value, "hard_constraint_status", _HARD_CONSTRAINT_ALLOWED_KEYS, errors)

    binding = value.get("binding")
    if not isinstance(binding, bool):
        errors.append("hard_constraint_status.binding must be a boolean")
        return

    source = value.get("constraint_source")
    if binding:
        if not _non_empty_str(source) or source == _NONE_CURRENTLY_BINDING:
            errors.append(
                "hard_constraint_status.constraint_source must be a non-empty citation string "
                "when binding is true (XASSET-0005 supporting artifact SS3.2)"
            )
    else:
        if source != _NONE_CURRENTLY_BINDING:
            errors.append(
                f"hard_constraint_status.constraint_source must be exactly {_NONE_CURRENTLY_BINDING!r} "
                f"when binding is false -- got {source!r}"
            )


def _validate_readiness_sub_object(value: object, field_name: str, errors: list[str]) -> None:
    if not _require_keys(value, field_name, _READINESS_SUB_ALLOWED_KEYS, errors):
        return
    value = value  # type: dict
    _reject_unknown_keys(value, field_name, _READINESS_SUB_ALLOWED_KEYS, errors)

    status = value.get("status")
    if status != _ASSESSMENT_REQUIRED_VALUE:
        errors.append(
            f"{field_name}.status must be exactly {_ASSESSMENT_REQUIRED_VALUE!r} on every record, "
            f"zero exception (XASSET-0005 supporting artifact SS3.2) -- got {status!r}"
        )
    if not _non_empty_str(value.get("rationale")):
        errors.append(f"{field_name}.rationale must be a non-empty string")


def _validate_economic_assessment_readiness(value: object, capital_use_type: object, errors: list[str]) -> None:
    """SS3.2/SS3.5: shape is conditional on capital_use_type. This
    function must never inspect `hard_constraint_status` in any way (SS7
    point 5's structural-independence requirement)."""
    if not isinstance(value, dict):
        errors.append(f"economic_assessment_readiness must be a mapping, got {type(value).__name__}")
        return

    if capital_use_type == _DEBT_REDUCTION_TYPE:
        _reject_unknown_keys(value, "economic_assessment_readiness", _DEBT_REDUCTION_READINESS_ALLOWED_KEYS, errors)
        missing = _DEBT_REDUCTION_READINESS_ALLOWED_KEYS - value.keys()
        if missing:
            errors.append(f"economic_assessment_readiness (DEBT_REDUCTION) missing required key(s): {sorted(missing)}")
            return
        _validate_readiness_sub_object(
            value.get("avoided_borrowing_cost_readiness"),
            "economic_assessment_readiness.avoided_borrowing_cost_readiness", errors,
        )
        _validate_readiness_sub_object(
            value.get("survivability_and_buffer_benefit_readiness"),
            "economic_assessment_readiness.survivability_and_buffer_benefit_readiness", errors,
        )
    else:
        overlap_with_debt_shape = set(value.keys()) & _DEBT_REDUCTION_READINESS_ALLOWED_KEYS
        if overlap_with_debt_shape:
            errors.append(
                "economic_assessment_readiness must use the single-part {status, rationale} shape "
                f"for capital_use_type {capital_use_type!r} -- the two-part DEBT_REDUCTION-only "
                f"shape ({sorted(_DEBT_REDUCTION_READINESS_ALLOWED_KEYS)}) is forbidden on this type "
                "(XASSET-0005 supporting artifact SS3.2/SS3.5)"
            )
            return
        _validate_readiness_sub_object(value, "economic_assessment_readiness", errors)


def _validate_liquidity_character(value: object, capital_use_type: object, errors: list[str]) -> None:
    if not _require_keys(value, "liquidity_character", frozenset({"liquidity_category"}), errors):
        return
    value = value  # type: dict
    _reject_unknown_keys(value, "liquidity_character", _LIQUIDITY_CHARACTER_ALLOWED_KEYS, errors)

    category = value.get("liquidity_category")
    if category not in _LIQUIDITY_CATEGORY_VALUES:
        errors.append(f"liquidity_character.liquidity_category must be one of {sorted(_LIQUIDITY_CATEGORY_VALUES)} -- got {category!r}")
        return

    if category == "not_applicable" and capital_use_type != _DEBT_REDUCTION_TYPE:
        errors.append(
            "liquidity_character.liquidity_category 'not_applicable' is reserved for "
            "DEBT_REDUCTION specifically (XASSET-0005 supporting artifact SS3.2) -- got it on "
            f"capital_use_type {capital_use_type!r}"
        )

    abstention_reason = value.get("abstention_reason")
    if category == _UNABLE_TO_DETERMINE_VALUE:
        if not _non_empty_str(abstention_reason):
            errors.append("liquidity_character.abstention_reason is required and non-empty when liquidity_category is 'unable_to_determine'")
    elif abstention_reason is not None:
        errors.append("liquidity_character.abstention_reason must be absent unless liquidity_category is 'unable_to_determine'")


def _validate_capital_preservation_character(value: object, errors: list[str]) -> None:
    if not _require_keys(value, "capital_preservation_character", frozenset({"capital_preservation_category"}), errors):
        return
    value = value  # type: dict
    _reject_unknown_keys(value, "capital_preservation_character", _CAPITAL_PRESERVATION_CHARACTER_ALLOWED_KEYS, errors)

    category = value.get("capital_preservation_category")
    if category not in _CAPITAL_PRESERVATION_CATEGORY_VALUES:
        errors.append(
            f"capital_preservation_character.capital_preservation_category must be one of "
            f"{sorted(_CAPITAL_PRESERVATION_CATEGORY_VALUES)} -- got {category!r}"
        )

    abstention_reason = value.get("abstention_reason")
    if category == _UNABLE_TO_DETERMINE_VALUE:
        if not _non_empty_str(abstention_reason):
            errors.append("capital_preservation_character.abstention_reason is required and non-empty when capital_preservation_category is 'unable_to_determine'")
    elif abstention_reason is not None:
        errors.append("capital_preservation_character.abstention_reason must be absent unless capital_preservation_category is 'unable_to_determine'")


def _validate_freshness_state(value: object, errors: list[str]) -> None:
    required = frozenset({"status", "as_of_reference"})
    if not _require_keys(value, "freshness_state", required, errors):
        return
    value = value  # type: dict
    _reject_unknown_keys(value, "freshness_state", _FRESHNESS_STATE_ALLOWED_KEYS, errors)

    status = value.get("status")
    if status not in _FRESHNESS_STATUS_VALUES:
        errors.append(f"freshness_state.status must be one of {sorted(_FRESHNESS_STATUS_VALUES)} -- got {status!r}")

    if not _non_empty_str(value.get("as_of_reference")):
        errors.append("freshness_state.as_of_reference must be a non-empty string, naming the specific evidence date or event this record's facts are pinned to")

    abstention_reason = value.get("abstention_reason")
    if status == _UNABLE_TO_DETERMINE_FRESHNESS_VALUE:
        if not _non_empty_str(abstention_reason):
            errors.append("freshness_state.abstention_reason is required and non-empty when status is 'unable_to_determine_freshness'")
    elif abstention_reason is not None:
        errors.append("freshness_state.abstention_reason must be absent unless status is 'unable_to_determine_freshness'")


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


def _validate_structural_reference(value: object, *, repo_root: Path | None, errors: list[str]) -> None:
    if not _require_keys(value, "structural_reference", _STRUCTURAL_REFERENCE_REQUIRED_KEYS, errors):
        return
    value = value  # type: dict
    _reject_unknown_keys(value, "structural_reference", _STRUCTURAL_REFERENCE_ALLOWED_KEYS, errors)

    if value.get("source_instrument_id") != _EXPECTED_SOURCE_INSTRUMENT_ID:
        errors.append(f"structural_reference.source_instrument_id must be exactly {_EXPECTED_SOURCE_INSTRUMENT_ID!r} -- got {value.get('source_instrument_id')!r}")
    if value.get("source_schema") != _EXPECTED_SOURCE_SCHEMA:
        errors.append(f"structural_reference.source_schema must be exactly {_EXPECTED_SOURCE_SCHEMA!r} -- got {value.get('source_schema')!r}")
    if value.get("source_file") != _EXPECTED_SOURCE_FILE:
        errors.append(f"structural_reference.source_file must be exactly {_EXPECTED_SOURCE_FILE!r} -- got {value.get('source_file')!r}")

    recorded_hash = value.get("referenced_content_sha256")
    if not _non_empty_str(recorded_hash):
        errors.append("structural_reference.referenced_content_sha256 must be a non-empty string")
        return

    if repo_root is None:
        return  # in-memory validation with no filesystem access -- hash recompute skipped

    gld_path = repo_root / "intelligence" / "etf_classification" / "GLD.yaml"
    if not gld_path.is_file():
        errors.append(
            "structural_reference could not be verified -- intelligence/etf_classification/"
            "GLD.yaml does not exist at the expected path"
        )
        return
    try:
        gld_data = yaml.safe_load(gld_path.read_text())
    except yaml.YAMLError as exc:
        errors.append(f"structural_reference could not be verified -- GLD.yaml is invalid YAML: {exc}")
        return
    if not isinstance(gld_data, dict):
        errors.append("structural_reference could not be verified -- GLD.yaml did not parse to a mapping")
        return

    live_hash = _etf.canonical_record_hash(gld_data)
    if recorded_hash != live_hash:
        errors.append(
            f"structural_reference.referenced_content_sha256 is stale -- recorded {recorded_hash!r}, "
            f"live-recomputed {live_hash!r} against the current sealed GLD.yaml (XASSET-0005 "
            f"supporting artifact SS3.4 point 2: a mismatch means GLD's structural record has "
            f"changed since this functional-doctrine record was last drafted or refreshed)"
        )


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


def _find_abstention_fields(data: dict) -> list[tuple[str, str]]:
    """(axis, field) pairs where a field is literally set to
    'unable_to_determine' or 'unable_to_determine_freshness' -- the two
    closed-vocabulary abstention values every axis unambiguously treats as
    a genuine abstention (SS3.6). Deliberately does NOT treat
    `liquidity_character`'s/`DEBT_REDUCTION`'s separate `not_applicable`
    value as an abstention -- that is a structural fact, not an evidence
    gap (SS3.6)."""
    pairs: list[tuple[str, str]] = []
    for axis in _AXIS_NAMES:
        axis_value = data.get(axis)
        if not isinstance(axis_value, dict):
            continue
        for field_name, field_value in axis_value.items():
            if field_value in (_UNABLE_TO_DETERMINE_VALUE, _UNABLE_TO_DETERMINE_FRESHNESS_VALUE):
                pairs.append((axis, field_name))
    return pairs


def _check_abstention_index_completeness(data: dict, errors: list[str]) -> None:
    """SS3.3: abstention_index is a mechanical rollup a future cross-asset
    synthesis unit can scan "without re-reading every axis" -- that
    guarantee requires every genuine abstention to actually appear in it,
    not merely a self-declared list left unreconciled against the axes it
    claims to summarize (the same defect class SS8.1 names, and
    `etf_classification_validator.py`'s own disclosed v1.1 finding)."""
    actual = _find_abstention_fields(data)
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
                f"abstention_index is missing an entry for {axis}.{field_name} -- every genuine "
                f"unable_to_determine/unable_to_determine_freshness abstention must be represented "
                f"in abstention_index (XASSET-0005 supporting artifact SS3.3), not merely "
                f"self-declared and left unreconciled (SS8.1)"
            )


def _validate_envelope_projection_consistency(data: dict, errors: list[str]) -> None:
    """SS4: every envelope-level field that summarizes an axis is a
    read-only copy, never independently computed -- checked for exact
    consistency against its source axis field."""
    eq = data.get("evidence_quality") or {}
    if isinstance(eq, dict):
        if data.get("uncertainty_summary") != eq.get("thesis_uncertainty_statement"):
            errors.append(
                "uncertainty_summary must exactly equal evidence_quality.thesis_uncertainty_"
                "statement (SS4 read-only-projection rule)"
            )
        if data.get("evidence_quality_status") != eq.get("primary_source_coverage"):
            errors.append(
                "evidence_quality_status must exactly equal evidence_quality."
                "primary_source_coverage (SS4 read-only-projection rule)"
            )

    hard_constraint = data.get("hard_constraint_status") or {}
    capital_preservation = data.get("capital_preservation_character") or {}
    risk_flags = data.get("structural_risk_flags")
    if not isinstance(risk_flags, dict):
        # A required envelope field needs its own independent presence/type
        # check, not merely a downstream consistency comparison that
        # silently no-ops when the field is missing entirely
        # (etf_classification_validator.py's own disclosed MINOR-1 lesson,
        # SS8.1 -- applied here from the start).
        errors.append("structural_risk_flags must be a mapping (SS3.3 required envelope field)")
    else:
        _reject_unknown_keys(risk_flags, "structural_risk_flags", _STRUCTURAL_RISK_FLAGS_ALLOWED_KEYS, errors)
        if isinstance(hard_constraint, dict) and isinstance(capital_preservation, dict):
            expected_flags = {
                "binding": hard_constraint.get("binding"),
                "capital_preservation_category": capital_preservation.get("capital_preservation_category"),
            }
            if risk_flags != expected_flags:
                errors.append(
                    f"structural_risk_flags must exactly project hard_constraint_status.binding "
                    f"and capital_preservation_character.capital_preservation_category (SS3.3) -- "
                    f"expected {expected_flags}, got {risk_flags}"
                )

    functional_role = data.get("functional_role") or {}
    liquidity_character = data.get("liquidity_character") or {}
    readiness = data.get("economic_assessment_readiness")
    capital_use_type = data.get("capital_use_type")
    handoff = data.get("cross_asset_handoff")
    if isinstance(handoff, dict):
        _reject_unknown_keys(handoff, "cross_asset_handoff", _CROSS_ASSET_HANDOFF_ALLOWED_KEYS, errors)
        missing = _CROSS_ASSET_HANDOFF_ALLOWED_KEYS - handoff.keys()
        if missing:
            errors.append(f"cross_asset_handoff missing required key(s): {sorted(missing)}")

        if isinstance(functional_role, dict) and handoff.get("role_summary") != functional_role.get("role_category"):
            errors.append("cross_asset_handoff.role_summary must exactly equal functional_role.role_category (SS3.3)")
        if isinstance(eq, dict) and handoff.get("evidence_quality_summary") != eq.get("primary_source_coverage"):
            errors.append("cross_asset_handoff.evidence_quality_summary must exactly equal evidence_quality.primary_source_coverage (SS3.3)")
        if handoff.get("uncertainty_summary") != data.get("uncertainty_summary"):
            errors.append("cross_asset_handoff.uncertainty_summary must exactly equal the envelope's own uncertainty_summary (SS3.3)")
        if isinstance(liquidity_character, dict) and handoff.get("liquidity_risk_summary") != liquidity_character.get("liquidity_category"):
            errors.append("cross_asset_handoff.liquidity_risk_summary must exactly equal liquidity_character.liquidity_category (SS3.3)")

        signal = handoff.get("hard_constraint_signal")
        if isinstance(hard_constraint, dict):
            expected_signal = {
                "binding": hard_constraint.get("binding"),
                "constraint_source": hard_constraint.get("constraint_source"),
            }
            if not isinstance(signal, dict):
                errors.append("cross_asset_handoff.hard_constraint_signal must be a mapping")
            else:
                _reject_unknown_keys(signal, "cross_asset_handoff.hard_constraint_signal", _HARD_CONSTRAINT_SIGNAL_ALLOWED_KEYS, errors)
                if signal != expected_signal:
                    errors.append(
                        f"cross_asset_handoff.hard_constraint_signal must exactly project "
                        f"hard_constraint_status (SS3.3) -- expected {expected_signal}, got {signal}. "
                        f"This field must never be merged with economic_assessment_readiness_summary."
                    )

        readiness_summary = handoff.get("economic_assessment_readiness_summary")
        if readiness is not None and readiness_summary != readiness:
            errors.append(
                "cross_asset_handoff.economic_assessment_readiness_summary must exactly equal "
                "economic_assessment_readiness, copied verbatim (SS3.3). This field must never "
                "be merged with hard_constraint_signal."
            )
    else:
        errors.append("cross_asset_handoff must be a mapping")

    if _non_empty_str(capital_use_type) and capital_use_type == _GLD_ONLY_TYPE:
        if "structural_reference" not in data:
            errors.append(
                "structural_reference is required when capital_use_type is 'GLD_DEFENSIVE_ROLE' "
                "(XASSET-0005 supporting artifact SS3.4)"
            )
    elif "structural_reference" in data:
        errors.append(
            f"structural_reference is forbidden (rejected as an unknown key) on capital_use_type "
            f"{capital_use_type!r} -- present only when capital_use_type is 'GLD_DEFENSIVE_ROLE' "
            f"(XASSET-0005 supporting artifact SS3.4)"
        )


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
            f"record contains unexpected top-level field(s) {sorted(stray)} -- exactly the six "
            f"axis-equivalent fields plus evidence_quality plus the envelope/seal fields are "
            f"permitted, no seventh substantive judgment axis (XASSET-0005 supporting artifact SS3)"
        )


# ── public API: in-memory record validation ─────────────────────────────

def validate_functional_doctrine_data(
    data: object,
    *,
    source: str | None = None,
    authorized_population: frozenset[str] = AUTHORIZED_POPULATION,
    repo_root: Path | None = None,
) -> ValidationResult:
    """Validate an already-parsed functional-doctrine classification
    mapping. Never touches the filesystem except for the live GLD.yaml
    structural-reference-hash recompute when `repo_root` is supplied."""
    errors: list[str] = []

    if not isinstance(data, dict):
        errors.append(f"root document must be a mapping, got {type(data).__name__}")
        return ValidationResult(valid=False, errors=errors, source=source)

    capital_use_type = data.get("capital_use_type")
    if not _non_empty_str(capital_use_type):
        errors.append("capital_use_type must be a non-empty string")
    elif authorized_population and capital_use_type not in authorized_population:
        errors.append(
            f"capital_use_type {capital_use_type!r} is not in the authorized four-type "
            f"population {sorted(authorized_population)} (XASSET-0006 SS A.1) -- no fifth "
            f"capital_use_type is authorized without its own separate schema-amendment decision"
        )

    if not _non_empty_str(data.get("schema_version")):
        errors.append("schema_version must be a non-empty string")

    for axis in ("functional_role", "hard_constraint_status", "liquidity_character",
                 "capital_preservation_character", "freshness_state", "evidence_quality"):
        if axis not in data:
            errors.append(f"record missing required field: {axis}")

    if "functional_role" in data:
        _validate_functional_role(data["functional_role"], errors)
    if "hard_constraint_status" in data:
        _validate_hard_constraint_status(data["hard_constraint_status"], errors)
    if "economic_assessment_readiness" not in data:
        errors.append("record missing required field: economic_assessment_readiness")
    else:
        _validate_economic_assessment_readiness(data["economic_assessment_readiness"], capital_use_type, errors)
    if "liquidity_character" in data:
        _validate_liquidity_character(data["liquidity_character"], capital_use_type, errors)
    if "capital_preservation_character" in data:
        _validate_capital_preservation_character(data["capital_preservation_character"], errors)
    if "freshness_state" in data:
        _validate_freshness_state(data["freshness_state"], errors)
    if "evidence_quality" in data:
        _validate_evidence_quality(data["evidence_quality"], errors)

    if "provenance" not in data:
        errors.append("record missing required field: provenance")
    else:
        _validate_provenance(data["provenance"], errors)

    if "structural_reference" in data:
        _validate_structural_reference(data["structural_reference"], repo_root=repo_root, errors=errors)

    if "abstention_index" not in data:
        errors.append("record missing required field: abstention_index")
    else:
        _validate_abstention_index(data["abstention_index"], errors)
        _check_abstention_index_completeness(data, errors)

    if "later_governance_action" in data and not _non_empty_str(data.get("later_governance_action")):
        errors.append("later_governance_action must be a non-empty string (use 'none' literally when nothing is implied)")
    elif "later_governance_action" not in data:
        errors.append("record missing required field: later_governance_action")

    _validate_no_stray_top_level_fields(data, errors)
    _validate_envelope_projection_consistency(data, errors)
    _validate_seal(data, errors)
    _scan_forbidden_keys(data, str(capital_use_type) if _non_empty_str(capital_use_type) else "<record>", errors)
    _scan_free_text_strings(data, str(capital_use_type) if _non_empty_str(capital_use_type) else "<record>", errors)

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


def validate_functional_doctrine_file(
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

    result = validate_functional_doctrine_data(
        data, source=source, authorized_population=authorized_population, repo_root=repo_root,
    )

    if isinstance(data, dict) and _non_empty_str(data.get("capital_use_type")):
        expected_stem = data["capital_use_type"]
        if path.stem != expected_stem:
            result.errors.append(
                f"filename stem {path.stem!r} does not match the record's own capital_use_type {expected_stem!r}"
            )
            result.valid = False

    return result


_MANIFEST_FILENAME = "COHORT_MANIFEST.yaml"
_MANIFEST_REQUIRED_ROW_KEYS = frozenset({
    "capital_use_type", "sealed_at", "content_sha256", "schema_version", "governing_decision", "record_path",
})
_MANIFEST_ROW_ALLOWED_KEYS = _MANIFEST_REQUIRED_ROW_KEYS
_MANIFEST_TOP_LEVEL_ALLOWED_KEYS = frozenset({"schema_version", "governing_decision", "cohort"})


def validate_cohort_manifest(
    manifest_data: object,
    records_by_capital_use_type: dict[str, dict],
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

        capital_use_type = row["capital_use_type"]
        if capital_use_type in seen:
            errors.append(f"cohort manifest lists {capital_use_type!r} more than once")
        seen.add(capital_use_type)

        record = records_by_capital_use_type.get(capital_use_type)
        if record is None:
            errors.append(f"cohort[{i}] capital_use_type {capital_use_type!r} has no corresponding sealed record file")
            continue

        expected_hash = canonical_record_hash(record)
        if row["content_sha256"] != expected_hash:
            errors.append(f"cohort[{i}] ({capital_use_type!r}) content_sha256 mismatch -- manifest {row['content_sha256']!r}, recomputed {expected_hash!r}")
        if record.get("content_sha256") != row["content_sha256"]:
            errors.append(f"cohort[{i}] ({capital_use_type!r}) manifest content_sha256 does not match the record's own recorded content_sha256")

    if authorized_population:
        missing_from_manifest = authorized_population - seen
        if missing_from_manifest:
            errors.append(f"cohort manifest is missing authorized capital_use_type(s): {sorted(missing_from_manifest)}")
        extra = seen - authorized_population
        if extra:
            errors.append(f"cohort manifest lists capital_use_type(s) outside the authorized population: {sorted(extra)}")

    orphans = set(records_by_capital_use_type) - seen
    if orphans:
        errors.append(f"sealed record(s) exist with no corresponding cohort manifest entry: {sorted(orphans)}")

    return ValidationResult(valid=not errors, errors=errors, source=_MANIFEST_FILENAME)


def validate_functional_doctrine_directory(
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
        validate_functional_doctrine_file(p, authorized_population=authorized_population, repo_root=repo_root)
        for p in yaml_paths
    ]

    records_by_capital_use_type: dict[str, dict] = {}
    for p in yaml_paths:
        data, read_errors = _read_yaml(p)
        if not read_errors and isinstance(data, dict) and _non_empty_str(data.get("capital_use_type")):
            records_by_capital_use_type[data["capital_use_type"]] = data

    manifest_path = directory / _MANIFEST_FILENAME
    if manifest_path.is_file():
        manifest_data, read_errors = _read_yaml(manifest_path)
        if read_errors:
            results.append(ValidationResult(valid=False, errors=read_errors, source=str(manifest_path)))
        else:
            results.append(
                validate_cohort_manifest(manifest_data, records_by_capital_use_type, authorized_population=authorized_population)
            )
    elif records_by_capital_use_type:
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
    _result = validate_functional_doctrine_directory(
        _repo_root / "intelligence" / "functional_doctrine", repo_root=_repo_root,
    )
    if _result.valid:
        print(f"functional_doctrine_validator: OK ({_result.record_count} result(s))")
        sys.exit(0)
    else:
        print("functional_doctrine_validator: FAILED")
        for _r in _result.results:
            if not _r.valid:
                for _err in _r.errors:
                    print(f"  - [{_r.source}] {_err}")
        sys.exit(1)
