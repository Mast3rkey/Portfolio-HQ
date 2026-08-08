"""
valuation_evidence_validator.py -- read-only schema validator for the
roster-agnostic quantitative valuation-evidence companion architecture
governed by `governance/decisions/VALUATION-0004-rq4-evidence-architecture-
governance.md` (RQ4 evidence-architecture governance), authorized for this
one implementation PR by VALUATION-0004 SS A/SS P.

Scope, exactly what is validated:

- Source-of-truth convention (VALUATION-0004 SS B): `intelligence/
  valuation_evidence/<TICKER>.yaml`, one file per equity, single-file (no
  paired Markdown, matching the classification/etf_classification/
  crypto_classification/valuation_archetype convention -- this is
  structured quantitative evidence, not a narrative thesis document),
  filesystem is the index, plus one `COHORT_MANIFEST.yaml`.
- **Roster-agnostic by design (SS B): no closed/authorized population is
  enforced here.** Unlike `etf_classification_validator.py`/
  `crypto_classification_validator.py` (small, fixed, closed populations)
  or `valuation_archetype_validator.py` (the fixed 27-name canonical
  cohort), this schema must be equally usable, without modification, for
  the 27 canonical equities, the 26 already-researched non-canonical
  Company Intelligence contenders, or any future equity contender the
  `CONTENDER-####` registry identifies (SS B) -- so no `AUTHORIZED_
  POPULATION` frozenset exists in this module, and `validate_cohort_
  manifest` performs only internal consistency checks (hash match, no
  duplicate, no orphan), never population-membership enforcement.
- **Zero real-company population (SS A/SS P, absolute).** This module is a
  schema/validator/test scaffold only. No `intelligence/valuation_
  evidence/` directory, `COHORT_MANIFEST.yaml`, or per-ticker record is
  created anywhere in this repository by this implementation -- the
  directory does not exist on disk, which the `validate_valuation_
  evidence_directory()` function treats as a valid, zero-coverage state,
  matching every prior Intelligence validator's own filesystem-as-index
  doctrine (a missing directory is not an error).
- Seven top-level evidence-domain containers (SS C, one reusable structure,
  never seven archetype-specific schemas): `financial_evidence` (SS C.1-3,
  6-8, 10-13 -- dated, period-indexed line items, annual/quarterly/TTM,
  reported-vs-derived, restatement state), `segment_evidence` (SS C.9,
  SS L -- per-segment revenue/profit/cash-flow, shared/unallocated costs,
  intersegment eliminations), `market_observed_evidence` (SS C.14),
  `discount_rate_evidence` (SS C.15, SS I -- individually sourced
  components only, never a single opaque rate, and never an actual ERP
  value/beta window/WACC convention decision), `peer_set_evidence`
  (SS C.16, SS J -- candidate identity/comparability/inclusion status, no
  peer selected), `scenario_evidence` (SS C.17, SS K -- scenario
  variables/evidence, no probability assigned to any real company), and
  `freshness_state` (SS E.6). Every container carries its own first-class
  abstention path (SS C.20, SS E.7), structurally distinguishable from a
  populated one, matching `TIER-0004` SS F's and `VALUATION-0003` SS H's
  identical rule for their own abstention paths -- abstention never
  cascades between containers.
- Provenance vocabulary reused, not invented (SS F): `source_type` --
  `primary`/`secondary`; `access_status` -- `directly_inspected`/
  `consulted_via_search_aggregation`/`attempted_not_directly_inspected`
  (matching `etf_classification_validator.py`/`crypto_classification_
  validator.py` exactly) on every raw financial-statement/market-observed
  fact; the four-label assumption/scenario provenance vocabulary --
  `market_derived`/`historically_observed`/`analyst_consensus_cited`/
  `assumed_for_illustration` (matching `VALUATION-0002` SS 3 exactly) on
  every discount-rate component, peer-set entry, and scenario variable.
- Reported-vs-derived distinction on every individual line item (SS C.10,
  SS E.3), never only at the record level -- a `derived` value requires a
  non-empty `derivation_note` (SS E.4); a `reported` value must not carry
  one.
- Disclosed evidence conflicts (SS E.5) -- a line item may carry
  `disclosed_conflicts`, never silently resolved in one direction.
- **Freshness computed, not merely trusted (SS E.6)**, learning directly
  from `reconciliation_validator.py`'s own disclosed MINOR defense-in-depth
  gap (a self-declared boolean checked without an independent
  recomputation): `most_recent_evidence_date` is independently recomputed
  as the max of every dated fact's own `as_of_date` across the whole
  record and cross-checked against the record's own self-declared value;
  `next_review_due_date` is independently recomputed as `most_recent_
  evidence_date + review_cadence_days` and cross-checked identically. The
  self-declared `stale` boolean's live truthfulness deliberately depends on
  a wall-clock "as of" reference this validator's `valid` boolean must
  never depend on for determinism (this repository's own `Date.now()`-ban
  discipline, applied here to keep validation reproducible) -- a separate
  pure function, `is_overdue_for_review(record, evaluation_date)`, exposes
  that live computation to a downstream reporting layer (matching how
  `intelligence_report.py`/`freshness_validator.py` are deliberately
  separate modules from the structural classification validators in this
  repository), without this validator's own pass/fail check ever reading
  the wall clock.
- **No single opaque discount-rate field (SS E.9, SS I).** `discount_rate_
  evidence` supports only individually sourced, individually provenance-
  labeled components -- `risk_free_rate`, `cost_of_debt`, `tax_rate`,
  `capital_structure`, `beta_observation` -- and forbids, structurally, a
  combined `discount_rate`/`wacc`/`equity_risk_premium` field anywhere
  (SS I: "this decision does not decide... the actual equity-risk-premium
  value to use, the beta estimation window or reference index, the exact
  WACC computation policy, or the capital-structure weighting
  convention").
- **No probability assigned to any scenario for any company (SS K).** The
  scenario schema structurally supports a `probability_weight` field
  (paired with its own SS F.2 provenance label whenever populated) so a
  future, separately authorized population phase has a structural home for
  it -- but this implementation populates none, and every test fixture
  using a probability weight is fictional.
- **No invented minimum time-series length (SS H).** `financial_evidence.
  periods` supports an arbitrary number of periods, including zero
  (pending abstention) -- no hardcoded minimum.
- A methodology-domain completeness self-check (SS Q, mirroring SS D):
  `check_methodology_domain_completeness()` verifies every evidence domain
  `VALUATION-0002` SS 2's own seven-family governed-role table requires for
  at least one `primary candidate`/`adjustment-required` cell has a
  structural home among this schema's own top-level domain keys -- a
  schema-shape self-consistency check, not a per-record judgment, and not
  a re-derivation of the table itself (bound by reference, per SS D).
- Closed schema at every level (envelope, per-domain container, per-period
  entry, per-line-item entry, per-discount-rate-component, per-peer-
  candidate, per-scenario entry, the manifest) -- an explicit
  permitted-key set per level, rejecting any unknown key (learning
  directly from `contender_registry_validator.py`'s own independent-
  review-found MAJOR gap: a denylist that checked only the missing side of
  a schema check).
- **Rejects any fair-value, price-target, expected-return, or opaque
  discount-rate/WACC output field anywhere in the document tree** (SS Q),
  plus equity-classification/ETF/crypto/archetype-layer field-name
  leakage, plus a numeric score/rank/target-key scan, plus an independent
  free-text scan for forbidden recommendation-shaped phrases, directive/
  trading language (buy, sell, add, hold, trim, exit, wait, stage --
  word-boundary matched so "hold" never flags the noun "holdings"), and
  chart-domain terminology -- built as its own materially different
  mechanism from any strip/redaction logic (there is none in this module;
  it is a pure read-only scan), never the same function called twice, per
  `TIER-0004`'s own corrected lesson on false independence claims.
- Zero coupling of any kind to `targets.yaml`, `holdings.yaml`,
  `gates.yaml`, `issuer_lookthrough.yaml`, `allocate.py`, or
  `margin_state.py` -- zero import, zero field.
- Deterministic hashing (`canonical_record_hash`) excludes only the seal
  fields (`sealed_at`, `governing_decision`, `drafting_session_or_shard_id`,
  `content_sha256`, `cohort_manifest_entry`).

This module is a validator, not a data producer. It never opens a file in
write/append/update mode, never creates a directory, and has zero import
relationship with `allocate.py` or `margin_state.py` in either direction.
It does not import any sibling Intelligence validator for schema logic
(each schema is independent), consistent with this repository's "each
Intelligence schema owns its own validator" convention.
"""

from __future__ import annotations

import datetime
import json
import re
from dataclasses import dataclass, field
from hashlib import sha256
from pathlib import Path

import yaml

ASSET_CLASS = "equity"

# ── provenance vocabularies (VALUATION-0004 SS F) -- reused, not invented ──

_SOURCE_TYPE_VALUES = frozenset({"primary", "secondary"})
_ACCESS_STATUS_VALUES = frozenset({
    "directly_inspected", "consulted_via_search_aggregation", "attempted_not_directly_inspected",
})
_ASSUMPTION_PROVENANCE_LABELS = frozenset({
    "market_derived", "historically_observed", "analyst_consensus_cited", "assumed_for_illustration",
})

_SOURCE_ALLOWED_KEYS = frozenset({
    "source_identifier", "source_type", "as_of_date", "access_status", "limitation",
})
_SOURCE_REQUIRED_KEYS = frozenset({"source_identifier", "source_type", "as_of_date", "access_status"})

# ── financial_evidence (SS C.1-3, 6-8, 10-13) ───────────────────────────────

_PERIOD_TYPE_VALUES = frozenset({"annual", "quarterly", "ttm"})
_LINE_ITEM_CATEGORIES = frozenset({
    "revenue", "earnings", "free_cash_flow", "gross_margin", "operating_margin", "net_margin",
    "segment_margin", "capex", "reinvestment", "invested_capital", "roic_related",
    "total_assets", "total_liabilities", "total_equity", "cash", "debt", "net_debt",
    "share_count_basic", "share_count_diluted", "dilutive_instrument", "other",
})
_VALUE_BASIS_VALUES = frozenset({"reported", "derived"})

_LINE_ITEM_ALLOWED_KEYS = frozenset({
    "item_category", "value", "unit", "value_basis", "derivation_note",
    "provenance", "disclosed_conflicts", "abstention_reason",
})
_LINE_ITEM_REQUIRED_KEYS = frozenset({"item_category"})

_CONFLICT_ENTRY_ALLOWED_KEYS = frozenset({
    "value", "source_identifier", "source_type", "access_status", "as_of_date", "note",
})
_CONFLICT_ENTRY_REQUIRED_KEYS = frozenset({
    "value", "source_identifier", "source_type", "access_status", "as_of_date",
})

_PERIOD_ALLOWED_KEYS = frozenset({
    "period_type", "fiscal_period_end_date", "as_of_date", "restated",
    "restated_from_note", "line_items",
})
_PERIOD_REQUIRED_KEYS = frozenset({
    "period_type", "fiscal_period_end_date", "as_of_date", "restated", "line_items",
})

_FINANCIAL_EVIDENCE_ALLOWED_KEYS = frozenset({"periods", "abstention_reason"})

# ── segment_evidence (SS C.9, SS L) ─────────────────────────────────────────

_SEGMENT_ENTRY_ALLOWED_KEYS = frozenset({"segment_name", "revenue", "profit", "cash_flow"})
_SEGMENT_ENTRY_REQUIRED_KEYS = frozenset({"segment_name"})
_SEGMENT_EVIDENCE_ALLOWED_KEYS = frozenset({
    "segments", "shared_unallocated_costs", "intersegment_eliminations", "abstention_reason",
})

# ── market_observed_evidence (SS C.14) ──────────────────────────────────────

_MARKET_OBSERVED_INPUT_ALLOWED_KEYS = frozenset({
    "input_name", "value", "unit", "as_of_date", "provenance", "abstention_reason",
})
_MARKET_OBSERVED_INPUT_REQUIRED_KEYS = frozenset({"input_name"})
_MARKET_OBSERVED_EVIDENCE_ALLOWED_KEYS = frozenset({"inputs", "abstention_reason"})

# ── discount_rate_evidence (SS C.15, SS I) ──────────────────────────────────

_DISCOUNT_COMPONENT_ALLOWED_KEYS = frozenset({
    "value", "provenance_label", "provenance", "note",
})
_DISCOUNT_COMPONENT_REQUIRED_KEYS = frozenset({"value", "provenance_label", "provenance"})

_TAX_RATE_TYPE_VALUES = frozenset({"effective", "statutory"})
_TAX_RATE_COMPONENT_ALLOWED_KEYS = _DISCOUNT_COMPONENT_ALLOWED_KEYS | {"tax_rate_type"}
_TAX_RATE_COMPONENT_REQUIRED_KEYS = _DISCOUNT_COMPONENT_REQUIRED_KEYS | {"tax_rate_type"}

_CAPITAL_STRUCTURE_ALLOWED_KEYS = frozenset({
    "debt_weight", "equity_weight", "provenance_label", "provenance",
})
_CAPITAL_STRUCTURE_REQUIRED_KEYS = frozenset({
    "debt_weight", "equity_weight", "provenance_label", "provenance",
})

_DISCOUNT_RATE_COMPONENT_NAMES = frozenset({
    "risk_free_rate", "cost_of_debt", "tax_rate", "capital_structure", "beta_observation",
})
_DISCOUNT_RATE_EVIDENCE_ALLOWED_KEYS = _DISCOUNT_RATE_COMPONENT_NAMES | {"abstention_reason"}

# Deliberately, structurally absent from every allowed-key set anywhere in
# this module -- SS E.9/SS I forbid a single opaque discount-rate figure and
# forbid this filing from deciding an actual ERP/WACC/beta-window policy.
_FORBIDDEN_DISCOUNT_RATE_KEYS = frozenset({
    "discount_rate", "wacc", "equity_risk_premium", "erp", "cost_of_capital",
})

# ── peer_set_evidence (SS C.16, SS J) ───────────────────────────────────────

_PEER_INCLUSION_STATUS_VALUES = frozenset({"included", "excluded"})
_PEER_CANDIDATE_ALLOWED_KEYS = frozenset({
    "identity", "comparability_rationale", "provenance", "as_of_date",
    "inclusion_status", "inclusion_rationale",
})
_PEER_CANDIDATE_REQUIRED_KEYS = frozenset({
    "identity", "comparability_rationale", "provenance", "as_of_date",
    "inclusion_status", "inclusion_rationale",
})
_PEER_SET_EVIDENCE_ALLOWED_KEYS = frozenset({"candidates", "abstention_reason"})

# ── scenario_evidence (SS C.17, SS K) ───────────────────────────────────────

_SCENARIO_VARIABLE_ALLOWED_KEYS = frozenset({"variable_name", "evidence_basis", "provenance_label"})
_SCENARIO_VARIABLE_REQUIRED_KEYS = _SCENARIO_VARIABLE_ALLOWED_KEYS

_SCENARIO_ENTRY_ALLOWED_KEYS = frozenset({
    "scenario_name", "variables", "probability_weight", "probability_weight_provenance_label",
})
_SCENARIO_ENTRY_REQUIRED_KEYS = frozenset({"scenario_name", "variables"})
_SCENARIO_EVIDENCE_ALLOWED_KEYS = frozenset({"scenarios", "abstention_reason"})

# ── freshness_state (SS E.6) ────────────────────────────────────────────────

_FRESHNESS_STATE_ALLOWED_KEYS = frozenset({
    "most_recent_evidence_date", "review_cadence_days", "next_review_due_date", "stale",
})
_FRESHNESS_STATE_REQUIRED_KEYS = _FRESHNESS_STATE_ALLOWED_KEYS

# ── abstention_index (mirrors etf_classification_validator.py SS6.1) ───────

_ABSTENTION_INDEX_ENTRY_ALLOWED_KEYS = frozenset({"domain", "reason"})
_ABSTAINABLE_DOMAINS = (
    "financial_evidence", "segment_evidence", "market_observed_evidence",
    "discount_rate_evidence", "peer_set_evidence", "scenario_evidence",
)

# ── record_status / seal metadata (mirrors sibling validators) ─────────────

_RECORD_STATUSES = frozenset({"draft", "sealed"})
_SEAL_REQUIRED_KEYS = frozenset({
    "sealed_at", "governing_decision", "drafting_session_or_shard_id",
    "content_sha256", "cohort_manifest_entry",
})

_DOMAIN_NAMES = (
    "financial_evidence", "segment_evidence", "market_observed_evidence",
    "discount_rate_evidence", "peer_set_evidence", "scenario_evidence", "freshness_state",
)
_ENVELOPE_ONLY_KEYS = frozenset({
    "schema_version", "ticker", "asset_class", "uncertainty_summary",
    "abstention_index", "record_status",
})
_ALL_TOP_LEVEL_KEYS = frozenset({*_ENVELOPE_ONLY_KEYS, *_DOMAIN_NAMES, *_SEAL_REQUIRED_KEYS})

# ── methodology-domain completeness self-check (VALUATION-0004 SS D/SS Q) ──
# A schema-shape self-consistency check against VALUATION-0002 SS2's own
# seven-family governed-role table, bound by reference (not re-derived, not
# restated in full) -- confirms every evidence domain at least one
# `primary candidate`/`adjustment-required` cell requires has a structural
# home among this schema's own top-level domain keys. This is NOT a
# per-record judgment; it is a fixed, testable statement about the schema's
# own shape.
_METHODOLOGY_FAMILY_REQUIRED_DOMAINS = {
    "asset_based_nav_sotp": frozenset({"financial_evidence", "segment_evidence"}),
    "fcff_dcf": frozenset({"financial_evidence", "discount_rate_evidence"}),
    "fcfe_dcf_ddm_excess_return": frozenset({"financial_evidence", "discount_rate_evidence"}),
    "earnings_fcf_yield_screens": frozenset({"financial_evidence"}),
    "relative_valuation_multiples": frozenset({"financial_evidence", "peer_set_evidence"}),
    "roic_reinvestment_economics": frozenset({"financial_evidence"}),
    "scenario_probability_weighted": frozenset({"financial_evidence", "scenario_evidence"}),
}

# ── forbidden leakage (SS Q, SS E.9, SS I) ──────────────────────────────────

_VALUATION_OUTPUT_LEAKAGE = frozenset({
    "fair_value", "price_target", "expected_return", "intrinsic_value", "dcf_value",
    "wacc", "computed_valuation", "valuation_output", "upside", "downside",
    "buy_price", "sell_price", "target_price", "recommended_value", "valuation_range",
    "price_range", "equity_risk_premium", "erp", "cost_of_capital", "discount_rate",
    "sotp_value", "sum_of_the_parts_value",
})
_EQUITY_CLASSIFICATION_LEAKAGE = frozenset({
    "portfolio_role_ref", "conviction", "economic_role", "capital_priority",
    "risk_concentration", "economic_system_ref", "primary_archetype", "secondary_archetype",
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
_FORBIDDEN_KEY_NAMES = frozenset({
    *_VALUATION_OUTPUT_LEAKAGE, *_EQUITY_CLASSIFICATION_LEAKAGE,
    *_ETF_CRYPTO_LEAKAGE, *_NUMERIC_SCORE_LEAKAGE,
})

_FORBIDDEN_TEXT_PATTERNS = [
    re.compile(p, re.IGNORECASE) for p in (
        r"\bshould\s+be\s+(increased|decreased|raised|lowered|set)\s+to\b",
        r"\brecommend(?:ed|s|ing)?\s+(a\s+)?(target|weight|allocation|position\s+size)\s+of\b",
        r"\bnew\s+target\s+(pct|percent|percentage|range)\b",
        r"\bbuy\s+recommendation\b",
        r"\bsell\s+recommendation\b",
        r"\btrim\s+recommendation\b",
        r"\bfair\s+value\s+(is|of|estimate)\b",
        r"\bprice\s+target\s+(is|of)\b",
        r"\d+(?:\.\d+)?\s*%\s*(?:of\s+book|target|weight|allocation)",
    )
]

# Word-boundary matched so "hold" never flags the noun "holdings", and
# "exit"/"add"/"wait"/"stage" never false-positive on unrelated substrings
# (recommendation_validator.py's/etf_classification_validator.py's own
# established design).
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
    """A missing or empty directory is valid, zero-coverage state -- the
    same filesystem-as-index doctrine every prior Intelligence validator in
    this repository already applies. VALUATION-0004 SS A/SS P authorizes no
    real-company population, so this directory does not exist anywhere in
    this repository at this implementation's own head."""
    valid: bool
    results: list[ValidationResult] = field(default_factory=list)

    @property
    def record_count(self) -> int:
        return len(self.results)


# ── canonical hashing -- excludes only the five seal fields ────────────────

_HASHABLE_KEYS = tuple(k for k in _ALL_TOP_LEVEL_KEYS if k not in _SEAL_REQUIRED_KEYS)


def canonical_record_hash(data: dict) -> str:
    """SHA-256 of the record's full content (envelope + all seven evidence-
    domain fields), canonical sorted-key JSON, UTF-8 -- excludes every seal
    field (sealed_at, governing_decision, drafting_session_or_shard_id,
    content_sha256, cohort_manifest_entry), avoiding circular self-hashing."""
    hashable = {k: data.get(k) for k in sorted(_HASHABLE_KEYS)}
    canonical = json.dumps(hashable, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return sha256(canonical.encode("utf-8")).hexdigest()


# ── generic helpers ──────────────────────────────────────────────────────

def _non_empty_str(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _is_number(value: object) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def _parse_date(value: object) -> datetime.date | None:
    if not isinstance(value, str) or not _DATE_RE.match(value):
        return None
    try:
        return datetime.date.fromisoformat(value)
    except ValueError:
        return None


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
            f"closed; only {sorted(allowed)} are permitted (VALUATION-0004 SS C/SS Q)"
        )


def _scan_forbidden_keys(value: object, path: str, errors: list[str]) -> None:
    """Structural scan: a forbidden key name anywhere in the document tree,
    not just at the top level (VALUATION-0004 SS Q, SS E.9, SS I)."""
    if isinstance(value, dict):
        for k, v in value.items():
            key_str = str(k)
            if key_str in _FORBIDDEN_KEY_NAMES:
                if key_str in _VALUATION_OUTPUT_LEAKAGE:
                    kind = "a fair-value/price-target/opaque-discount-rate-shaped field"
                elif key_str in _EQUITY_CLASSIFICATION_LEAKAGE:
                    kind = "an equity-classification/archetype-layer-shaped field"
                elif key_str in _ETF_CRYPTO_LEAKAGE:
                    kind = "an ETF/crypto-classification-shaped field"
                else:
                    kind = "a numeric score/rank/target-shaped field"
                errors.append(
                    f"{path}.{key_str}: forbidden key name -- {kind} must never appear in a "
                    f"valuation evidence record (VALUATION-0004 SS Q, SS E.9, SS I)"
                )
            _scan_forbidden_keys(v, f"{path}.{key_str}", errors)
    elif isinstance(value, list):
        for i, item in enumerate(value):
            _scan_forbidden_keys(item, f"{path}[{i}]", errors)


def _scan_free_text_strings(value: object, path: str, errors: list[str]) -> None:
    """Recursively scan every free-text string value for forbidden
    recommendation-shaped phrases, directive language, and chart-derived
    terminology -- an independent, materially different mechanism from
    whatever accepted this string into the document (there is no strip/
    redaction logic in this module to accidentally share code with), per
    VALUATION-0004 SS Q's "own materially different mechanism" requirement."""
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
                    f"framing (VALUATION-0004 SS R)"
                )
        for term, pattern in _CHART_PATTERNS:
            if pattern.search(value):
                errors.append(
                    f"{path}: contains chart-derived terminology {term!r} -- no chart evidence "
                    f"of any kind is permitted (VALUATION-0004 SS R)"
                )


# ── provenance (VALUATION-0004 SS F.1) ──────────────────────────────────────

def _validate_source_provenance(value: object, field_name: str, errors: list[str]) -> None:
    if not _require_keys(value, field_name, frozenset({"sources"}), errors):
        return
    value = value  # type: dict
    _reject_unknown_keys(value, field_name, frozenset({"sources"}), errors)

    sources = value.get("sources")
    if not isinstance(sources, list) or not sources:
        errors.append(f"{field_name}.sources must be a non-empty list")
        return

    for i, src in enumerate(sources):
        label = f"{field_name}.sources[{i}]"
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
        if _parse_date(src.get("as_of_date")) is None:
            errors.append(f"{label}.as_of_date must be a valid YYYY-MM-DD date")
        if src.get("access_status") not in _ACCESS_STATUS_VALUES:
            errors.append(f"{label}.access_status must be one of {sorted(_ACCESS_STATUS_VALUES)} -- got {src.get('access_status')!r}")


def _validate_assumption_provenance_label(value: object, field_name: str, errors: list[str]) -> None:
    if value not in _ASSUMPTION_PROVENANCE_LABELS:
        errors.append(
            f"{field_name} must be one of {sorted(_ASSUMPTION_PROVENANCE_LABELS)} "
            f"(VALUATION-0004 SS F.2) -- got {value!r}"
        )


# ── line items (financial_evidence periods, segment sub-fields) ────────────

def _validate_line_item(value: object, path: str, errors: list[str]) -> None:
    if not _require_keys(value, path, _LINE_ITEM_REQUIRED_KEYS, errors):
        return
    value = value  # type: dict
    _reject_unknown_keys(value, path, _LINE_ITEM_ALLOWED_KEYS, errors)

    category = value.get("item_category")
    if category not in _LINE_ITEM_CATEGORIES:
        errors.append(f"{path}.item_category must be one of {sorted(_LINE_ITEM_CATEGORIES)} -- got {category!r}")

    has_value = "value" in value and value.get("value") is not None
    raw_value = value.get("value")

    if has_value:
        if not _is_number(raw_value):
            errors.append(f"{path}.value must be a number or null (VALUATION-0004 SS C.20/SS E.7)")
        if not _non_empty_str(value.get("unit")):
            errors.append(f"{path}.unit is required and non-empty when value is populated")
        basis = value.get("value_basis")
        if basis not in _VALUE_BASIS_VALUES:
            errors.append(f"{path}.value_basis must be one of {sorted(_VALUE_BASIS_VALUES)} when value is populated (SS C.10) -- got {basis!r}")
        derivation_note = value.get("derivation_note")
        if basis == "derived":
            if not _non_empty_str(derivation_note):
                errors.append(f"{path}.derivation_note is required and non-empty when value_basis is 'derived' (SS E.4)")
        elif derivation_note is not None:
            errors.append(f"{path}.derivation_note must be absent unless value_basis is 'derived'")
        if "provenance" not in value:
            errors.append(f"{path}.provenance is required when value is populated (SS F.1/SS E.2)")
        else:
            _validate_source_provenance(value["provenance"], f"{path}.provenance", errors)
        if value.get("abstention_reason") is not None:
            errors.append(f"{path}.abstention_reason must be absent when value is populated")
        conflicts = value.get("disclosed_conflicts")
        if conflicts is not None:
            if not isinstance(conflicts, list) or not conflicts:
                errors.append(f"{path}.disclosed_conflicts must be a non-empty list when present (SS E.5)")
            else:
                for i, c in enumerate(conflicts):
                    clabel = f"{path}.disclosed_conflicts[{i}]"
                    if not isinstance(c, dict):
                        errors.append(f"{clabel} must be a mapping")
                        continue
                    missing = _CONFLICT_ENTRY_REQUIRED_KEYS - c.keys()
                    if missing:
                        errors.append(f"{clabel} missing required key(s): {sorted(missing)}")
                    unknown = set(c.keys()) - _CONFLICT_ENTRY_ALLOWED_KEYS
                    if unknown:
                        errors.append(f"{clabel} contains unexpected key(s) {sorted(unknown)}")
                    if not _is_number(c.get("value")):
                        errors.append(f"{clabel}.value must be a number")
                    if not _non_empty_str(c.get("source_identifier")):
                        errors.append(f"{clabel}.source_identifier must be a non-empty string")
                    if c.get("source_type") not in _SOURCE_TYPE_VALUES:
                        errors.append(f"{clabel}.source_type must be one of {sorted(_SOURCE_TYPE_VALUES)}")
                    if c.get("access_status") not in _ACCESS_STATUS_VALUES:
                        errors.append(f"{clabel}.access_status must be one of {sorted(_ACCESS_STATUS_VALUES)}")
                    if _parse_date(c.get("as_of_date")) is None:
                        errors.append(f"{clabel}.as_of_date must be a valid YYYY-MM-DD date")
    else:
        for k in ("unit", "value_basis", "derivation_note", "provenance", "disclosed_conflicts"):
            if value.get(k) is not None:
                errors.append(f"{path}.{k} must be absent when {path}.value is null/absent (an abstained line item)")
        if not _non_empty_str(value.get("abstention_reason")):
            errors.append(f"{path}.abstention_reason is required and non-empty when {path}.value is null/absent (SS C.20/SS E.7)")


def _validate_period(value: object, path: str, errors: list[str]) -> tuple[list[str], list[str]]:
    """Returns (as_of_dates, fiscal_end_dates) found in this period, for the
    caller's own cross-period freshness recompute."""
    as_of_dates: list[str] = []
    fiscal_dates: list[str] = []
    if not _require_keys(value, path, _PERIOD_REQUIRED_KEYS, errors):
        return as_of_dates, fiscal_dates
    value = value  # type: dict
    _reject_unknown_keys(value, path, _PERIOD_ALLOWED_KEYS, errors)

    if value.get("period_type") not in _PERIOD_TYPE_VALUES:
        errors.append(f"{path}.period_type must be one of {sorted(_PERIOD_TYPE_VALUES)} -- got {value.get('period_type')!r}")

    fiscal_end = _parse_date(value.get("fiscal_period_end_date"))
    if fiscal_end is None:
        errors.append(f"{path}.fiscal_period_end_date must be a valid YYYY-MM-DD date (SS C.12)")
    else:
        fiscal_dates.append(value["fiscal_period_end_date"])

    as_of = _parse_date(value.get("as_of_date"))
    if as_of is None:
        errors.append(f"{path}.as_of_date must be a valid YYYY-MM-DD date (SS C.12)")
    else:
        as_of_dates.append(value["as_of_date"])

    if fiscal_end is not None and as_of is not None and as_of < fiscal_end:
        errors.append(
            f"{path}.as_of_date ({value['as_of_date']}) must not precede its own "
            f"fiscal_period_end_date ({value['fiscal_period_end_date']}) (SS Q date-ordering rule)"
        )

    restated = value.get("restated")
    if not isinstance(restated, bool):
        errors.append(f"{path}.restated must be a boolean (SS C.13)")
    restated_note = value.get("restated_from_note")
    if restated is True:
        if not _non_empty_str(restated_note):
            errors.append(f"{path}.restated_from_note is required and non-empty when restated is true")
    elif restated_note is not None:
        errors.append(f"{path}.restated_from_note must be absent unless restated is true")

    items = value.get("line_items")
    if not isinstance(items, list) or not items:
        errors.append(f"{path}.line_items must be a non-empty list")
    else:
        for i, item in enumerate(items):
            _validate_line_item(item, f"{path}.line_items[{i}]", errors)
            if isinstance(item, dict):
                prov = item.get("provenance")
                if isinstance(prov, dict):
                    for src in prov.get("sources") or []:
                        if isinstance(src, dict) and _non_empty_str(src.get("as_of_date")):
                            as_of_dates.append(src["as_of_date"])

    return as_of_dates, fiscal_dates


def _validate_financial_evidence(value: object, errors: list[str]) -> list[str]:
    """Returns every as_of_date found, for the freshness recompute."""
    dates: list[str] = []
    if not _require_keys(value, "financial_evidence", frozenset(), errors):
        return dates
    value = value  # type: dict
    _reject_unknown_keys(value, "financial_evidence", _FINANCIAL_EVIDENCE_ALLOWED_KEYS, errors)

    periods = value.get("periods")
    if not isinstance(periods, list):
        errors.append("financial_evidence.periods must be a list (possibly empty, pending abstention)")
        periods = []

    for i, p in enumerate(periods):
        as_of, _fiscal = _validate_period(p, f"financial_evidence.periods[{i}]", errors)
        dates.extend(as_of)

    abstention_reason = value.get("abstention_reason")
    if not periods:
        if not _non_empty_str(abstention_reason):
            errors.append("financial_evidence.abstention_reason is required and non-empty when periods is empty (SS C.20)")
    elif abstention_reason is not None:
        errors.append("financial_evidence.abstention_reason must be absent when periods is populated")

    return dates


# ── segment_evidence (SS C.9, SS L) ─────────────────────────────────────────

def _validate_segment_entry(value: object, path: str, errors: list[str]) -> list[str]:
    dates: list[str] = []
    if not _require_keys(value, path, _SEGMENT_ENTRY_REQUIRED_KEYS, errors):
        return dates
    value = value  # type: dict
    _reject_unknown_keys(value, path, _SEGMENT_ENTRY_ALLOWED_KEYS, errors)

    if not _non_empty_str(value.get("segment_name")):
        errors.append(f"{path}.segment_name must be a non-empty string")

    for sub in ("revenue", "profit", "cash_flow"):
        if sub in value:
            _validate_line_item(value[sub], f"{path}.{sub}", errors)
            item = value[sub]
            if isinstance(item, dict):
                prov = item.get("provenance")
                if isinstance(prov, dict):
                    for src in prov.get("sources") or []:
                        if isinstance(src, dict) and _non_empty_str(src.get("as_of_date")):
                            dates.append(src["as_of_date"])
    return dates


def _validate_segment_evidence(value: object, errors: list[str]) -> list[str]:
    dates: list[str] = []
    if not _require_keys(value, "segment_evidence", frozenset(), errors):
        return dates
    value = value  # type: dict
    _reject_unknown_keys(value, "segment_evidence", _SEGMENT_EVIDENCE_ALLOWED_KEYS, errors)

    segments = value.get("segments")
    if not isinstance(segments, list):
        errors.append("segment_evidence.segments must be a list (possibly empty, pending abstention)")
        segments = []

    for i, s in enumerate(segments):
        dates.extend(_validate_segment_entry(s, f"segment_evidence.segments[{i}]", errors))

    for sub in ("shared_unallocated_costs", "intersegment_eliminations"):
        if sub in value:
            _validate_line_item(value[sub], f"segment_evidence.{sub}", errors)

    abstention_reason = value.get("abstention_reason")
    if not segments:
        if not _non_empty_str(abstention_reason):
            errors.append(
                "segment_evidence.abstention_reason is required and non-empty when segments is "
                "empty (SS L: 'segment data unavailable or insufficiently granular')"
            )
    elif abstention_reason is not None:
        errors.append("segment_evidence.abstention_reason must be absent when segments is populated")

    return dates


# ── market_observed_evidence (SS C.14) ──────────────────────────────────────

def _validate_market_observed_evidence(value: object, errors: list[str]) -> list[str]:
    dates: list[str] = []
    if not _require_keys(value, "market_observed_evidence", frozenset(), errors):
        return dates
    value = value  # type: dict
    _reject_unknown_keys(value, "market_observed_evidence", _MARKET_OBSERVED_EVIDENCE_ALLOWED_KEYS, errors)

    inputs = value.get("inputs")
    if not isinstance(inputs, list):
        errors.append("market_observed_evidence.inputs must be a list (possibly empty, pending abstention)")
        inputs = []

    for i, entry in enumerate(inputs):
        path = f"market_observed_evidence.inputs[{i}]"
        if not _require_keys(entry, path, _MARKET_OBSERVED_INPUT_REQUIRED_KEYS, errors):
            continue
        entry = entry  # type: dict
        _reject_unknown_keys(entry, path, _MARKET_OBSERVED_INPUT_ALLOWED_KEYS, errors)
        if not _non_empty_str(entry.get("input_name")):
            errors.append(f"{path}.input_name must be a non-empty string")

        has_value = "value" in entry and entry.get("value") is not None
        if has_value:
            if not _is_number(entry.get("value")):
                errors.append(f"{path}.value must be a number or null")
            if not _non_empty_str(entry.get("unit")):
                errors.append(f"{path}.unit is required and non-empty when value is populated")
            if _parse_date(entry.get("as_of_date")) is None:
                errors.append(f"{path}.as_of_date must be a valid YYYY-MM-DD date when value is populated")
            else:
                dates.append(entry["as_of_date"])
            if "provenance" not in entry:
                errors.append(f"{path}.provenance is required when value is populated")
            else:
                _validate_source_provenance(entry["provenance"], f"{path}.provenance", errors)
            if entry.get("abstention_reason") is not None:
                errors.append(f"{path}.abstention_reason must be absent when value is populated")
        else:
            for k in ("unit", "as_of_date", "provenance"):
                if entry.get(k) is not None:
                    errors.append(f"{path}.{k} must be absent when {path}.value is null/absent")
            if not _non_empty_str(entry.get("abstention_reason")):
                errors.append(f"{path}.abstention_reason is required and non-empty when {path}.value is null/absent (SS C.20)")

    abstention_reason = value.get("abstention_reason")
    if not inputs:
        if not _non_empty_str(abstention_reason):
            errors.append("market_observed_evidence.abstention_reason is required and non-empty when inputs is empty (SS C.20)")
    elif abstention_reason is not None:
        errors.append("market_observed_evidence.abstention_reason must be absent when inputs is populated")

    return dates


# ── discount_rate_evidence (SS C.15, SS I) ──────────────────────────────────

def _validate_discount_component(value: object, path: str, errors: list[str], *, required_keys=None, allowed_keys=None) -> list[str]:
    dates: list[str] = []
    required_keys = required_keys or _DISCOUNT_COMPONENT_REQUIRED_KEYS
    allowed_keys = allowed_keys or _DISCOUNT_COMPONENT_ALLOWED_KEYS
    if not _require_keys(value, path, required_keys, errors):
        return dates
    value = value  # type: dict
    _reject_unknown_keys(value, path, allowed_keys, errors)

    if not _is_number(value.get("value")):
        errors.append(f"{path}.value must be a number")
    _validate_assumption_provenance_label(value.get("provenance_label"), f"{path}.provenance_label", errors)
    if "provenance" not in value:
        errors.append(f"{path}.provenance is required")
    else:
        _validate_source_provenance(value["provenance"], f"{path}.provenance", errors)
        prov = value["provenance"]
        if isinstance(prov, dict):
            for src in prov.get("sources") or []:
                if isinstance(src, dict) and _non_empty_str(src.get("as_of_date")):
                    dates.append(src["as_of_date"])
    return dates


def _validate_discount_rate_evidence(value: object, errors: list[str]) -> list[str]:
    dates: list[str] = []
    if not _require_keys(value, "discount_rate_evidence", frozenset(), errors):
        return dates
    value = value  # type: dict
    _reject_unknown_keys(value, "discount_rate_evidence", _DISCOUNT_RATE_EVIDENCE_ALLOWED_KEYS, errors)

    present_components = [c for c in _DISCOUNT_RATE_COMPONENT_NAMES if c in value]

    if "risk_free_rate" in value:
        dates.extend(_validate_discount_component(value["risk_free_rate"], "discount_rate_evidence.risk_free_rate", errors))
    if "cost_of_debt" in value:
        dates.extend(_validate_discount_component(value["cost_of_debt"], "discount_rate_evidence.cost_of_debt", errors))
    if "tax_rate" in value:
        component_dates = _validate_discount_component(
            value["tax_rate"], "discount_rate_evidence.tax_rate", errors,
            required_keys=_TAX_RATE_COMPONENT_REQUIRED_KEYS, allowed_keys=_TAX_RATE_COMPONENT_ALLOWED_KEYS,
        )
        dates.extend(component_dates)
        tax_component = value["tax_rate"]
        if isinstance(tax_component, dict) and tax_component.get("tax_rate_type") not in _TAX_RATE_TYPE_VALUES:
            errors.append(
                f"discount_rate_evidence.tax_rate.tax_rate_type must be one of "
                f"{sorted(_TAX_RATE_TYPE_VALUES)} -- got {tax_component.get('tax_rate_type')!r}"
            )
    if "capital_structure" in value:
        cs = value["capital_structure"]
        if not _require_keys(cs, "discount_rate_evidence.capital_structure", _CAPITAL_STRUCTURE_REQUIRED_KEYS, errors):
            pass
        else:
            _reject_unknown_keys(cs, "discount_rate_evidence.capital_structure", _CAPITAL_STRUCTURE_ALLOWED_KEYS, errors)
            for k in ("debt_weight", "equity_weight"):
                v = cs.get(k)
                if not _is_number(v):
                    errors.append(f"discount_rate_evidence.capital_structure.{k} must be a number")
            _validate_assumption_provenance_label(
                cs.get("provenance_label"), "discount_rate_evidence.capital_structure.provenance_label", errors,
            )
            if "provenance" not in cs:
                errors.append("discount_rate_evidence.capital_structure.provenance is required")
            else:
                _validate_source_provenance(cs["provenance"], "discount_rate_evidence.capital_structure.provenance", errors)
                prov = cs["provenance"]
                if isinstance(prov, dict):
                    for src in prov.get("sources") or []:
                        if isinstance(src, dict) and _non_empty_str(src.get("as_of_date")):
                            dates.append(src["as_of_date"])
    if "beta_observation" in value:
        dates.extend(_validate_discount_component(value["beta_observation"], "discount_rate_evidence.beta_observation", errors))

    abstention_reason = value.get("abstention_reason")
    if not present_components:
        if not _non_empty_str(abstention_reason):
            errors.append(
                "discount_rate_evidence.abstention_reason is required and non-empty when no "
                "component is populated (SS C.20)"
            )
    elif abstention_reason is not None:
        errors.append("discount_rate_evidence.abstention_reason must be absent when at least one component is populated")

    return dates


# ── peer_set_evidence (SS C.16, SS J) ───────────────────────────────────────

def _validate_peer_set_evidence(value: object, errors: list[str]) -> list[str]:
    dates: list[str] = []
    if not _require_keys(value, "peer_set_evidence", frozenset(), errors):
        return dates
    value = value  # type: dict
    _reject_unknown_keys(value, "peer_set_evidence", _PEER_SET_EVIDENCE_ALLOWED_KEYS, errors)

    candidates = value.get("candidates")
    if not isinstance(candidates, list):
        errors.append("peer_set_evidence.candidates must be a list (possibly empty, pending abstention)")
        candidates = []

    for i, c in enumerate(candidates):
        path = f"peer_set_evidence.candidates[{i}]"
        if not _require_keys(c, path, _PEER_CANDIDATE_REQUIRED_KEYS, errors):
            continue
        c = c  # type: dict
        _reject_unknown_keys(c, path, _PEER_CANDIDATE_ALLOWED_KEYS, errors)
        if not _non_empty_str(c.get("identity")):
            errors.append(f"{path}.identity must be a non-empty string")
        if not _non_empty_str(c.get("comparability_rationale")):
            errors.append(f"{path}.comparability_rationale must be a non-empty string")
        if _parse_date(c.get("as_of_date")) is None:
            errors.append(f"{path}.as_of_date must be a valid YYYY-MM-DD date")
        else:
            dates.append(c["as_of_date"])
        if c.get("inclusion_status") not in _PEER_INCLUSION_STATUS_VALUES:
            errors.append(f"{path}.inclusion_status must be one of {sorted(_PEER_INCLUSION_STATUS_VALUES)} -- got {c.get('inclusion_status')!r}")
        if not _non_empty_str(c.get("inclusion_rationale")):
            errors.append(f"{path}.inclusion_rationale must be a non-empty string")
        if "provenance" not in c:
            errors.append(f"{path}.provenance is required")
        else:
            _validate_source_provenance(c["provenance"], f"{path}.provenance", errors)

    abstention_reason = value.get("abstention_reason")
    if not candidates:
        if not _non_empty_str(abstention_reason):
            errors.append(
                "peer_set_evidence.abstention_reason is required and non-empty when candidates is "
                "empty (SS J: 'no valid peer set could be identified')"
            )
    elif abstention_reason is not None:
        errors.append("peer_set_evidence.abstention_reason must be absent when candidates is populated")

    return dates


# ── scenario_evidence (SS C.17, SS K) ───────────────────────────────────────

def _validate_scenario_evidence(value: object, errors: list[str]) -> None:
    if not _require_keys(value, "scenario_evidence", frozenset(), errors):
        return
    value = value  # type: dict
    _reject_unknown_keys(value, "scenario_evidence", _SCENARIO_EVIDENCE_ALLOWED_KEYS, errors)

    scenarios = value.get("scenarios")
    if not isinstance(scenarios, list):
        errors.append("scenario_evidence.scenarios must be a list (possibly empty, pending abstention)")
        scenarios = []

    for i, s in enumerate(scenarios):
        path = f"scenario_evidence.scenarios[{i}]"
        if not _require_keys(s, path, _SCENARIO_ENTRY_REQUIRED_KEYS, errors):
            continue
        s = s  # type: dict
        _reject_unknown_keys(s, path, _SCENARIO_ENTRY_ALLOWED_KEYS, errors)
        if not _non_empty_str(s.get("scenario_name")):
            errors.append(f"{path}.scenario_name must be a non-empty string")

        variables = s.get("variables")
        if not isinstance(variables, list) or not variables:
            errors.append(f"{path}.variables must be a non-empty list")
        else:
            for j, v in enumerate(variables):
                vpath = f"{path}.variables[{j}]"
                if not _require_keys(v, vpath, _SCENARIO_VARIABLE_REQUIRED_KEYS, errors):
                    continue
                v = v  # type: dict
                _reject_unknown_keys(v, vpath, _SCENARIO_VARIABLE_ALLOWED_KEYS, errors)
                if not _non_empty_str(v.get("variable_name")):
                    errors.append(f"{vpath}.variable_name must be a non-empty string")
                if not _non_empty_str(v.get("evidence_basis")):
                    errors.append(f"{vpath}.evidence_basis must be a non-empty string")
                _validate_assumption_provenance_label(v.get("provenance_label"), f"{vpath}.provenance_label", errors)

        # SS K: a probability_weight, wherever populated, must itself carry
        # a provenance label -- structurally present, populated by nobody
        # under this implementation (every test fixture is fictional).
        weight = s.get("probability_weight")
        weight_label = s.get("probability_weight_provenance_label")
        if weight is not None:
            if not _is_number(weight):
                errors.append(f"{path}.probability_weight must be a number when present")
            _validate_assumption_provenance_label(
                weight_label, f"{path}.probability_weight_provenance_label", errors,
            )
        elif weight_label is not None:
            errors.append(f"{path}.probability_weight_provenance_label must be absent unless probability_weight is present")

    abstention_reason = value.get("abstention_reason")
    if not scenarios:
        if not _non_empty_str(abstention_reason):
            errors.append(
                "scenario_evidence.abstention_reason is required and non-empty when scenarios is "
                "empty (SS K: 'unable to determine a defensible scenario set')"
            )
    elif abstention_reason is not None:
        errors.append("scenario_evidence.abstention_reason must be absent when scenarios is populated")


# ── freshness_state (SS E.6) ────────────────────────────────────────────────

def _add_days(d: datetime.date, n: int) -> datetime.date:
    return d + datetime.timedelta(days=n)


def _validate_freshness_state(data: dict, errors: list[str], *, all_dates: list[str]) -> None:
    value = data.get("freshness_state")
    if not _require_keys(value, "freshness_state", _FRESHNESS_STATE_REQUIRED_KEYS, errors):
        return
    value = value  # type: dict
    _reject_unknown_keys(value, "freshness_state", _FRESHNESS_STATE_ALLOWED_KEYS, errors)

    declared_most_recent = _parse_date(value.get("most_recent_evidence_date"))
    if declared_most_recent is None:
        errors.append("freshness_state.most_recent_evidence_date must be a valid YYYY-MM-DD date")

    cadence = value.get("review_cadence_days")
    if not isinstance(cadence, int) or isinstance(cadence, bool) or cadence <= 0:
        errors.append("freshness_state.review_cadence_days must be a positive integer")

    declared_next_due = _parse_date(value.get("next_review_due_date"))
    if declared_next_due is None:
        errors.append("freshness_state.next_review_due_date must be a valid YYYY-MM-DD date")

    if not isinstance(value.get("stale"), bool):
        errors.append("freshness_state.stale must be a boolean")

    # "Compute or verify... rather than trusting a self-declared flag
    # alone" (SS Q, learning from reconciliation_validator.py's own
    # disclosed MINOR gap): independently recompute the most-recent-
    # evidence date from every dated fact actually present in the record,
    # and the expected next-review-due date from that recomputed date plus
    # the record's own disclosed cadence -- both cross-checked against the
    # self-declared values. Deliberately does NOT read the wall clock (this
    # repository's own Date.now()-ban discipline, applied here to keep
    # validation deterministic); see is_overdue_for_review() below for the
    # separate, explicitly wall-clock-taking function.
    parsed_dates = [d for d in (_parse_date(x) for x in all_dates) if d is not None]
    if parsed_dates and declared_most_recent is not None:
        computed_most_recent = max(parsed_dates)
        if declared_most_recent != computed_most_recent:
            errors.append(
                f"freshness_state.most_recent_evidence_date ({value.get('most_recent_evidence_date')}) "
                f"does not match the date independently recomputed as the max as_of_date across "
                f"every fact actually present in this record ({computed_most_recent.isoformat()}) "
                f"(SS E.6 -- verified, not merely trusted)"
            )

    if (
        declared_most_recent is not None
        and isinstance(cadence, int) and not isinstance(cadence, bool) and cadence > 0
        and declared_next_due is not None
    ):
        expected_next_due = _add_days(declared_most_recent, cadence)
        if declared_next_due != expected_next_due:
            errors.append(
                f"freshness_state.next_review_due_date ({value.get('next_review_due_date')}) does "
                f"not match most_recent_evidence_date + review_cadence_days, independently "
                f"recomputed as {expected_next_due.isoformat()} (SS E.6)"
            )


def is_overdue_for_review(data: dict, evaluation_date: str) -> bool | None:
    """Pure function, explicit `evaluation_date` parameter (never a live
    wall-clock read) -- the one live-freshness computation SS E.6 requires,
    deliberately kept out of `validate_valuation_evidence_data`'s own
    deterministic pass/fail check (matching how `intelligence_report.py`/
    `freshness_validator.py` are separate modules from the structural
    classification validators in this repository). Mirrors
    `intelligence_report.collect_staleness_findings`'s own strict
    `next_due < as_of_date` overdue rule by pattern, not by import
    coupling. Returns None if `freshness_state.next_review_due_date` or
    `evaluation_date` is not a valid date."""
    freshness = data.get("freshness_state") if isinstance(data, dict) else None
    if not isinstance(freshness, dict):
        return None
    next_due = _parse_date(freshness.get("next_review_due_date"))
    as_of = _parse_date(evaluation_date)
    if next_due is None or as_of is None:
        return None
    return next_due < as_of


# ── abstention_index ─────────────────────────────────────────────────────

def _find_abstained_domains(data: dict) -> list[str]:
    """Domain-level abstentions only (the six top-level evidence-domain
    containers) -- individual line-item/period/candidate-level abstentions
    are already self-documenting inline via their own required
    `abstention_reason` and are not re-indexed here, a deliberate scoping
    choice disclosed in this function's own name."""
    abstained: list[str] = []
    for domain in _ABSTAINABLE_DOMAINS:
        value = data.get(domain)
        if isinstance(value, dict) and _non_empty_str(value.get("abstention_reason")):
            abstained.append(domain)
    return abstained


def _validate_abstention_index(value: object, errors: list[str]) -> None:
    if not isinstance(value, list):
        errors.append("abstention_index must be a list")
        return
    for i, entry in enumerate(value):
        label = f"abstention_index[{i}]"
        if not isinstance(entry, dict) or (_ABSTENTION_INDEX_ENTRY_ALLOWED_KEYS - entry.keys()):
            errors.append(f"{label} must be a mapping with keys {sorted(_ABSTENTION_INDEX_ENTRY_ALLOWED_KEYS)}")
            continue
        unknown = set(entry.keys()) - _ABSTENTION_INDEX_ENTRY_ALLOWED_KEYS
        if unknown:
            errors.append(f"{label} contains unexpected key(s) {sorted(unknown)}")
        if entry.get("domain") not in _ABSTAINABLE_DOMAINS:
            errors.append(f"{label}.domain must be one of {sorted(_ABSTAINABLE_DOMAINS)}")
        if not _non_empty_str(entry.get("reason")):
            errors.append(f"{label}.reason must be a non-empty string")


def _check_abstention_index_completeness(data: dict, errors: list[str]) -> None:
    """A self-declared abstention_index is not a substitute for an
    independent scan (the same defect class etf_classification_validator.py
    SS9.1's v1.1 bounded correction names): every genuine domain-level
    abstention must actually appear in abstention_index."""
    actual = _find_abstained_domains(data)
    if not actual:
        return
    index = data.get("abstention_index")
    if not isinstance(index, list):
        return  # already flagged by _validate_abstention_index
    indexed_domains = {entry.get("domain") for entry in index if isinstance(entry, dict)}
    for domain in actual:
        if domain not in indexed_domains:
            errors.append(
                f"abstention_index is missing an entry for domain {domain!r}, which carries a "
                f"populated abstention_reason -- every genuine domain-level abstention must be "
                f"represented in abstention_index, not merely self-declared and left unreconciled"
            )


# ── seal / record_status ────────────────────────────────────────────────

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
            f"evidence-domain fields plus the envelope/seal fields are permitted, no eighth "
            f"substantive domain (VALUATION-0004 SS C/SS Q)"
        )


# ── methodology-domain completeness self-check (SS D/SS Q) ─────────────────

def check_methodology_domain_completeness() -> ValidationResult:
    """A schema-shape self-consistency check, not a per-record judgment:
    every evidence domain VALUATION-0002 SS2's own seven-family governed-
    role table requires for at least one `primary candidate`/`adjustment-
    required` cell must have a structural home among this schema's own
    top-level domain keys (VALUATION-0004 SS D, bound by reference -- the
    table itself is not re-derived here)."""
    errors: list[str] = []
    for family, required_domains in _METHODOLOGY_FAMILY_REQUIRED_DOMAINS.items():
        missing = required_domains - set(_DOMAIN_NAMES)
        if missing:
            errors.append(
                f"methodology family {family!r} requires evidence domain(s) {sorted(missing)}, "
                f"which have no structural home in this schema's top-level domain keys "
                f"{sorted(_DOMAIN_NAMES)}"
            )
    return ValidationResult(valid=not errors, errors=errors, source="check_methodology_domain_completeness")


# ── public API: in-memory record validation ─────────────────────────────

def validate_valuation_evidence_data(data: object, *, source: str | None = None) -> ValidationResult:
    """Validate an already-parsed valuation-evidence mapping. Never touches
    the filesystem. Deliberately takes no `authorized_population` parameter
    -- this schema is roster-agnostic by design (VALUATION-0004 SS B); a
    closed-population check does not belong in this validator."""
    errors: list[str] = []

    if not isinstance(data, dict):
        errors.append(f"root document must be a mapping, got {type(data).__name__}")
        return ValidationResult(valid=False, errors=errors, source=source)

    ticker = data.get("ticker")
    if not _non_empty_str(ticker):
        errors.append("ticker must be a non-empty string")

    asset_class = data.get("asset_class")
    if asset_class != ASSET_CLASS:
        errors.append(f"asset_class must be exactly {ASSET_CLASS!r} -- got {asset_class!r}")

    if not _non_empty_str(data.get("schema_version")):
        errors.append("schema_version must be a non-empty string")

    all_dates: list[str] = []

    if "financial_evidence" not in data:
        errors.append("record missing required field: financial_evidence")
    else:
        all_dates.extend(_validate_financial_evidence(data["financial_evidence"], errors))

    if "segment_evidence" not in data:
        errors.append("record missing required field: segment_evidence")
    else:
        all_dates.extend(_validate_segment_evidence(data["segment_evidence"], errors))

    if "market_observed_evidence" not in data:
        errors.append("record missing required field: market_observed_evidence")
    else:
        all_dates.extend(_validate_market_observed_evidence(data["market_observed_evidence"], errors))

    if "discount_rate_evidence" not in data:
        errors.append("record missing required field: discount_rate_evidence")
    else:
        all_dates.extend(_validate_discount_rate_evidence(data["discount_rate_evidence"], errors))

    if "peer_set_evidence" not in data:
        errors.append("record missing required field: peer_set_evidence")
    else:
        all_dates.extend(_validate_peer_set_evidence(data["peer_set_evidence"], errors))

    if "scenario_evidence" not in data:
        errors.append("record missing required field: scenario_evidence")
    else:
        _validate_scenario_evidence(data["scenario_evidence"], errors)

    if not _non_empty_str(data.get("uncertainty_summary")):
        errors.append("uncertainty_summary must be a non-empty string")

    if "abstention_index" not in data:
        errors.append("record missing required field: abstention_index")
    else:
        _validate_abstention_index(data["abstention_index"], errors)
        _check_abstention_index_completeness(data, errors)

    if "freshness_state" not in data:
        errors.append("record missing required field: freshness_state")
    else:
        _validate_freshness_state(data, errors, all_dates=all_dates)

    _validate_no_stray_top_level_fields(data, errors)
    _validate_seal(data, errors)
    _scan_forbidden_keys(data, str(ticker) if _non_empty_str(ticker) else "<record>", errors)
    _scan_free_text_strings(data, str(ticker) if _non_empty_str(ticker) else "<record>", errors)

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


def validate_valuation_evidence_file(path: str | Path) -> ValidationResult:
    path = Path(path)
    source = str(path)
    data, read_errors = _read_yaml(path)
    if read_errors:
        return ValidationResult(valid=False, errors=read_errors, source=source)

    result = validate_valuation_evidence_data(data, source=source)

    if isinstance(data, dict) and _non_empty_str(data.get("ticker")):
        expected_stem = data["ticker"]
        if path.stem != expected_stem:
            result.errors.append(
                f"filename stem {path.stem!r} does not match the record's own ticker {expected_stem!r}"
            )
            result.valid = False

    return result


_MANIFEST_FILENAME = "COHORT_MANIFEST.yaml"
_MANIFEST_REQUIRED_ROW_KEYS = frozenset({
    "ticker", "sealed_at", "content_sha256", "schema_version", "governing_decision", "record_path",
})
_MANIFEST_ROW_ALLOWED_KEYS = _MANIFEST_REQUIRED_ROW_KEYS
_MANIFEST_TOP_LEVEL_ALLOWED_KEYS = frozenset({"schema_version", "governing_decision", "cohort"})


def validate_cohort_manifest(manifest_data: object, records_by_ticker: dict[str, dict]) -> ValidationResult:
    """Internal consistency only -- no closed-population enforcement, since
    this schema is roster-agnostic by design (VALUATION-0004 SS B): every
    manifest row must correspond to a real sealed record with a matching
    hash, every sealed record must have a manifest row, and no ticker may
    be listed twice. Unlike etf_classification_validator.py's/
    crypto_classification_validator.py's `validate_cohort_manifest`, there
    is deliberately no `authorized_population` parameter here."""
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


def validate_valuation_evidence_directory(directory: str | Path) -> DirectoryValidationResult:
    """A missing or empty directory is a valid, zero-coverage state
    (VALUATION-0004 SS A/SS P: this implementation populates zero real
    tickers, so `intelligence/valuation_evidence/` does not exist anywhere
    in this repository at this implementation's own head)."""
    directory = Path(directory)
    if not directory.exists() or not directory.is_dir():
        return DirectoryValidationResult(valid=True, results=[])

    yaml_paths = sorted(p for p in directory.glob("*.yaml") if p.name != _MANIFEST_FILENAME)
    results = [validate_valuation_evidence_file(p) for p in yaml_paths]

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
    _completeness = check_methodology_domain_completeness()
    if not _completeness.valid:
        print("valuation_evidence_validator: FAILED (methodology domain completeness)")
        for _err in _completeness.errors:
            print(f"  - {_err}")
        sys.exit(1)

    _result = validate_valuation_evidence_directory(_repo_root / "intelligence" / "valuation_evidence")
    if _result.valid:
        print(f"valuation_evidence_validator: OK ({_result.record_count} result(s))")
        sys.exit(0)
    else:
        print("valuation_evidence_validator: FAILED")
        for _r in _result.results:
            if not _r.valid:
                for _err in _r.errors:
                    print(f"  - [{_r.source}] {_err}")
        sys.exit(1)
