"""
instrument_economic_assessment_validator.py -- read-only schema validator
for the WS-0014 ETF+crypto instrument economic-assessment content batch
(SPY, VEA, VWO, BTC, ETH, SOL), authored against the closed methodology
`governance/decisions/XASSET-0010-etf-crypto-economic-assessment-
methodology.md`'s supporting artifact
(`governance/audits/WS0014_ETF_CRYPTO_INSTRUMENT_ECONOMIC_ASSESSMENT_
METHODOLOGY_DESIGN_20260810.md`, SS3/SS4/SS5/SS6/SS9) designed, for the one
implementation PR authorized by `governance/decisions/XASSET-0011-ws0014-
etf-crypto-economic-assessment-content-authorization.md`.

Scope, exactly what is validated:

- Source-of-truth convention: `intelligence/instrument_economic_assessment/
  <INSTRUMENT_ID>.yaml`, one file per instrument, single-file (no paired
  Markdown), filesystem is the index, plus `COHORT_MANIFEST.yaml` -- the
  identical convention every prior classification/economic-assessment
  framework in this repository already establishes. Deliberately a
  separate directory and a separate schema from
  `intelligence/economic_assessment/` (GLD/CASH_LIKE_CAPITAL,
  `economic_assessment_validator.py`) -- neither module imports the other,
  and this module never touches GLD.yaml/CASH_LIKE_CAPITAL.yaml
  (XASSET-0010 SSG).
- Exactly six `instrument_id` values across two `asset_type` values: `etf`
  (`SPY`, `VEA`, `VWO`) and `cryptocurrency` (`BTC`, `ETH`, `SOL`) -- no
  `GLD`, `CASH_LIKE_CAPITAL`, `DEBT_REDUCTION`, `QQQ`, or any seventh value
  of any kind (AA SS9 point 1).
- One `asset_type`-conditional substantive axis: `cost_and_tracking_
  quality_economic_significance` (`etf` only, forbidden on
  `cryptocurrency`) or `macro_behavioral_characterization` (`cryptocurrency`
  only, forbidden on `etf`, a compound object with two independently-
  abstainable sub-fields) -- plus `evidence_quality` on both (AA SS4.2/
  SS4.3/SS5.2/SS6.2).
- One `structural_reference` object per record -- a single pin (never a
  dual pin like GLD's, never a legacy-reference list like CASH_LIKE_
  CAPITAL's) into the instrument's own already-sealed classification
  record, live-recomputed on every validator run via a **read-only** call
  to `etf_classification_validator.canonical_record_hash()` or
  `crypto_classification_validator.canonical_record_hash()`, selected by
  `asset_type` -- a stale or wrong-schema reference is mechanically
  detected and rejected (AA SS3).
- Zero numeric field anywhere, with **no carve-out of any kind** -- an
  already-sealed numeric structural fact (e.g. an ETF's own expense ratio)
  may be referenced only by the `structural_reference` hash pin, never
  restated as a literal number anywhere in this schema's own free text
  (AA SS5.2, SS9 point 6 -- stricter than the ETF classification
  framework's own scoped `expense_ratio_pct` exception).
- Synthesis handoff -- `cross_asset_handoff` carries exactly three fields
  (`economic_characterization_summary`, `evidence_quality_summary`,
  `uncertainty_summary`) -- no `deployability_summary` field for this
  population, since no `deployability_and_optionality` axis exists here
  (AA SS4.6).
- Crypto/overlap-model non-duplication -- every `BTC`/`ETH`/`SOL` record's
  `historical_equity_market_drawdown_behavior` sub-field must carry a
  non-empty `single_asset_disclosure` and must never assert, anywhere in
  its own free text, a computed whole-portfolio diversification-benefit or
  correlation-to-the-current-portfolio finding -- that remains
  `defensive_offset_interface`'s own, separate, still-forced-abstention
  job (AA SS7, non-duplication boundary).
- Cross-coin-correlation non-leakage -- a dedicated, materially
  independent scan rejecting any claim, anywhere in any field of any
  record, that `BTC`/`ETH`/`SOL` are or are not correlated with each
  other, and any numeric correlation coefficient of any kind -- a genuine
  cross-coin correlation study remains a separate, future, bounded,
  pre-registered research charter's own question (AA SS6.1, SS9 point 11).
- No predictive-language leakage inside `historical_equity_market_
  drawdown_behavior`'s and `historical_inflation_sensitivity_narrative`'s
  own free-text fields specifically (AA SS9 point 9) -- both sub-fields are
  historically-grounded, backward-looking characterizations only, never a
  forecast.
- Closed schema at every level (envelope, structural reference, both
  substantive axes and their sub-fields, `evidence_quality`,
  `cross_asset_handoff`, provenance source, manifest row) -- an explicit
  permitted-key set per level, rejecting any unknown key, not merely
  checking for the presence of required ones (AA SS9 point 2, learning
  directly from `contender_registry_validator.py`'s own independent-
  review-found MAJOR gap).
- No equity-shaped, ETF-classification-shaped, crypto-classification-
  shaped, functional-doctrine-shaped, overlap-model-shaped, or
  `economic_assessment` (GLD/CASH_LIKE_CAPITAL)-shaped field-name leakage
  anywhere in the document tree (AA SS9 point 5).
- Abstention: `unable_to_determine` with a required, non-empty
  `abstention_reason` on every substantive axis/sub-field -- this schema
  defines no `not_applicable` value anywhere in either axis's own closed
  vocabulary (AA SS6.2's own closing paragraph: the crypto axis is simply
  *absent*, not marked `not_applicable`, on `etf` records, and vice versa).
  Abstention does not cascade between the two independently-abstainable
  crypto sub-fields (AA SS6.2).
- `abstention_index` independently reconciled against every genuine
  `unable_to_determine` value actually present -- never a self-declared
  flag trusted alone (AA SS9 point 15, learning directly from
  `etf_classification_validator.py`'s own disclosed MINOR-1 finding and
  `reconciliation_validator.py`'s own disclosed MINOR gap).
- Deterministic hashing (`canonical_record_hash`) excludes only the five
  seal fields (`sealed_at`, `governing_decision`, `drafting_session_or_
  shard_id`, `content_sha256`, `cohort_manifest_entry`) -- `content_sha256`
  is independently recomputable and must match on every sealed record and
  every manifest row, bidirectionally.

This module is a validator, not a data producer. It never opens a file in
write/append/update mode, never creates a directory, and has zero import
relationship with `allocate.py` or `margin_state.py` in either direction.
It imports `etf_classification_validator` and `crypto_classification_
validator` for exactly one read-only public function each
(`canonical_record_hash`) to implement the structural-reference hash pins
-- no other cross-module coupling, and it never imports or is imported by
`economic_assessment_validator.py` (the permanently separate GLD/
CASH_LIKE_CAPITAL schema, XASSET-0010 SSG).
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from hashlib import sha256
from pathlib import Path

import yaml

import crypto_classification_validator as _crypto
import etf_classification_validator as _etf

AUTHORIZED_POPULATION = frozenset({"SPY", "VEA", "VWO", "BTC", "ETH", "SOL"})
ETF_INSTRUMENTS = frozenset({"SPY", "VEA", "VWO"})
CRYPTO_INSTRUMENTS = frozenset({"BTC", "ETH", "SOL"})
_ASSET_TYPE_BY_INSTRUMENT = {
    **{t: "etf" for t in ETF_INSTRUMENTS},
    **{t: "cryptocurrency" for t in CRYPTO_INSTRUMENTS},
}
_ASSET_TYPE_VALUES = frozenset({"etf", "cryptocurrency"})

_UNABLE_TO_DETERMINE_VALUE = "unable_to_determine"

# ── cost_and_tracking_quality_economic_significance (AA SS5.2) -- etf only ─

_COST_TRACKING_SIGNIFICANCE_VALUES = frozenset({
    "in_line_with_category", "elevated_vs_category", "favorable_vs_category",
    _UNABLE_TO_DETERMINE_VALUE,
})
_COST_TRACKING_ALLOWED_KEYS = frozenset({"significance_category", "rationale", "abstention_reason"})

# ── macro_behavioral_characterization (AA SS6.2) -- cryptocurrency only ────

_DRAWDOWN_BEHAVIOR_VALUES = frozenset({
    "historically_uncorrelated_or_negatively_correlated", "historically_mixed",
    "historically_positively_correlated", _UNABLE_TO_DETERMINE_VALUE,
})
_INFLATION_SENSITIVITY_VALUES = frozenset({
    "historically_positively_associated", "historically_mixed_or_inconsistent",
    "historically_weakly_associated", _UNABLE_TO_DETERMINE_VALUE,
})
_DRAWDOWN_BEHAVIOR_ALLOWED_KEYS = frozenset({
    "behavior_category", "rationale", "single_asset_disclosure", "abstention_reason",
})
_INFLATION_SENSITIVITY_ALLOWED_KEYS = frozenset({
    "sensitivity_category", "rationale", "abstention_reason",
})
_MACRO_BEHAVIORAL_SUB_FIELDS = frozenset({
    "historical_equity_market_drawdown_behavior", "historical_inflation_sensitivity_narrative",
})
_MACRO_BEHAVIORAL_ALLOWED_KEYS = _MACRO_BEHAVIORAL_SUB_FIELDS

# ── structural_reference (AA SS3) -- one pin per instrument ────────────────

_STRUCTURAL_REFERENCE_ALLOWED_KEYS = frozenset({
    "source_instrument_id", "source_schema", "source_file", "referenced_content_sha256",
})
_EXPECTED_SOURCE_SCHEMA_BY_ASSET_TYPE = {
    "etf": "etf_classification",
    "cryptocurrency": "crypto_classification",
}
_EXPECTED_SOURCE_FILE_TEMPLATE_BY_ASSET_TYPE = {
    "etf": "intelligence/etf_classification/{ticker}.yaml",
    "cryptocurrency": "intelligence/crypto_classification/{ticker}.yaml",
}
_CANONICAL_HASH_FN_BY_ASSET_TYPE = {
    "etf": _etf.canonical_record_hash,
    "cryptocurrency": _crypto.canonical_record_hash,
}
_SOURCE_DIR_BY_ASSET_TYPE = {
    "etf": ("intelligence", "etf_classification"),
    "cryptocurrency": ("intelligence", "crypto_classification"),
}

# ── evidence_quality (unchanged shape from every prior framework) ──────────

_PRIMARY_SOURCE_COVERAGE_VALUES = frozenset({"comprehensive", "partial", "limited"})
_EVIDENCE_QUALITY_ALLOWED_KEYS = frozenset({"primary_source_coverage", "thesis_uncertainty_statement"})

# ── provenance (unchanged shape) ────────────────────────────────────────

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

# ── cross_asset_handoff (AA SS4.6) -- exactly three fields ─────────────────

_CROSS_ASSET_HANDOFF_ALLOWED_KEYS = frozenset({
    "economic_characterization_summary", "evidence_quality_summary", "uncertainty_summary",
})

# ── abstention_index ─────────────────────────────────────────────────────

_ABSTENTION_ENTRY_ALLOWED_KEYS = frozenset({"axis", "field", "value", "reason"})

# ── record_status / seal metadata ───────────────────────────────────────

_RECORD_STATUSES = frozenset({"draft", "sealed"})
_SEAL_REQUIRED_KEYS = frozenset({
    "sealed_at", "governing_decision", "drafting_session_or_shard_id",
    "content_sha256", "cohort_manifest_entry",
})

_ENVELOPE_ONLY_KEYS = frozenset({
    "schema_version", "instrument_id", "asset_type", "provenance",
    "uncertainty_summary", "evidence_quality_status", "record_status",
    "cross_asset_handoff", "abstention_index",
})
_STRUCTURAL_REFERENCE_KEY = frozenset({"structural_reference"})
_ASSET_TYPE_CONDITIONAL_AXIS_KEYS = frozenset({
    "cost_and_tracking_quality_economic_significance", "macro_behavioral_characterization",
})
_SHARED_AXIS_KEYS = frozenset({"evidence_quality"})
_ALL_TOP_LEVEL_KEYS = frozenset({
    *_ENVELOPE_ONLY_KEYS, *_STRUCTURAL_REFERENCE_KEY, *_ASSET_TYPE_CONDITIONAL_AXIS_KEYS,
    *_SHARED_AXIS_KEYS, *_SEAL_REQUIRED_KEYS,
})

# ── forbidden leakage: cross-schema field names (AA SS9 point 5) ───────────
# Exactly the six named groups XASSET-0010 supporting artifact SS9 point 5
# enumerates -- equity, ETF-classification, crypto-classification,
# functional-doctrine, overlap-model, and economic_assessment
# (GLD/CASH_LIKE_CAPITAL)-shaped key names, none of which may ever appear
# anywhere in an instrument_economic_assessment record.

_EQUITY_FIELD_LEAKAGE = frozenset({
    "economic_role", "capital_priority", "risk_concentration",
    "portfolio_role_ref", "conviction", "economic_system_ref",
})
_ETF_CLASSIFICATION_FIELD_LEAKAGE = frozenset({
    "structural_role", "constituent_exposure", "overlap_and_concentration",
    "cost_and_tracking_quality", "liquidity", "structure_and_methodology",
})
_CRYPTO_CLASSIFICATION_FIELD_LEAKAGE = frozenset({
    "network_fundamentals", "economic_model", "liquidity_and_market_structure",
    "custody_and_counterparty_risk", "correlation_and_volatility",
    "regulatory_and_structural_uncertainty",
})
_FUNCTIONAL_DOCTRINE_FIELD_LEAKAGE = frozenset({
    "functional_role", "hard_constraint_status", "economic_assessment_readiness",
    "liquidity_character", "capital_preservation_character", "freshness_state", "capital_use_type",
})
_OVERLAP_MODEL_FIELD_LEAKAGE = frozenset({
    "dimension_id", "dimension_type", "source_mechanism", "computation_status",
    "evidence_or_source_refs", "output_shape", "uncertainty_or_gap_disclosure",
})
_ECONOMIC_ASSESSMENT_FIELD_LEAKAGE = frozenset({
    "deployability_and_optionality", "instrument_specific_economic_characterization",
    "analytical_subject", "legacy_structural_references",
    "structural_reference_etf_classification", "structural_reference_functional_doctrine",
})
_CROSS_SCHEMA_LEAKAGE_GROUPS = (
    (_EQUITY_FIELD_LEAKAGE, "an equity-classification-shaped field"),
    (_ETF_CLASSIFICATION_FIELD_LEAKAGE, "an ETF-classification-shaped axis field"),
    (_CRYPTO_CLASSIFICATION_FIELD_LEAKAGE, "a crypto-classification-shaped axis field"),
    (_FUNCTIONAL_DOCTRINE_FIELD_LEAKAGE, "a functional-doctrine-shaped field"),
    (_OVERLAP_MODEL_FIELD_LEAKAGE, "an overlap-model-shaped field"),
    (_ECONOMIC_ASSESSMENT_FIELD_LEAKAGE, "a GLD/CASH_LIKE_CAPITAL economic-assessment-shaped field"),
)
_ALL_CROSS_SCHEMA_LEAKAGE_KEYS = frozenset().union(*(g for g, _ in _CROSS_SCHEMA_LEAKAGE_GROUPS))

# ── forbidden leakage: numeric fields (AA SS9 point 6) -- no carve-out ─────

_NUMERIC_LEAKAGE_KEYS = frozenset({
    "expected_return", "hurdle_rate", "price_target", "fair_value",
    "correlation_coefficient", "beta", "target_pct", "target_weight",
    "opportunity_cost_score", "ranking_score", "allocation_pct", "leverage_amount",
})
_FORBIDDEN_KEY_NAMES = frozenset({*_ALL_CROSS_SCHEMA_LEAKAGE_KEYS, *_NUMERIC_LEAKAGE_KEYS})

# Bare numeric-percent-shaped token -- rejected everywhere in free text,
# with NO carve-out of any kind (AA SS9 point 6's own explicit
# instruction, stricter than the ETF classification framework's own
# scoped exception for expense_ratio_pct as a structured field -- this
# schema forbids the literal figure in free text unconditionally, even
# though the pinned structural record it may only be referenced by hash
# already carries the real number as a structured field there).
_NUMERIC_PERCENT_PATTERN = re.compile(r"\d+(?:\.\d+)?\s*%")

# A bare decimal number in the immediate vicinity of "correlat*" is its
# own distinct leakage risk (a correlation coefficient need not be
# percent-shaped, e.g. "0.72" or "-0.41") -- covered by the dedicated
# cross-coin-correlation scan below (check 11), not this general numeric
# scan, since it is about a *claim*, not merely a *number* (AA SS9.1).

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
# (recommendation_validator.py's own established design, reused
# unmodified -- this schema has no operational capital-use verb list,
# since it is a valuation/economic-characterization schema, not an
# operational capital-use schema like functional-doctrine's).
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

# ── predictive-language leakage (AA SS9 point 9) -- scoped to exactly the
#    two crypto sub-fields' own free text, not the whole document ─────────

_PREDICTIVE_TERMS = ("forecast", "predict", "expected to", "will likely", "projected")


def _predictive_pattern(term: str) -> re.Pattern:
    if " " in term:
        return re.compile(re.escape(term), re.IGNORECASE)
    return re.compile(rf"\b{re.escape(term)}\w*", re.IGNORECASE)


_PREDICTIVE_PATTERNS = [(t, _predictive_pattern(t)) for t in _PREDICTIVE_TERMS]
_PREDICTIVE_SCOPED_SUB_FIELDS = frozenset({
    "historical_equity_market_drawdown_behavior", "historical_inflation_sensitivity_narrative",
})

# ── crypto/overlap-model non-duplication (AA SS7, SS9 point 10) -- reject
#    a whole-portfolio diversification/correlation claim anywhere in
#    historical_equity_market_drawdown_behavior's own free text. A
#    materially separate mechanism from check 11's cross-coin-correlation
#    scan below (a "vs the current portfolio" claim, not a "vs another
#    named coin" claim) ────────────────────────────────────────────────

_PORTFOLIO_DIVERSIFICATION_PATTERNS = [
    re.compile(p, re.IGNORECASE) for p in (
        r"diversification\s+benefit\s+to\s+(the\s+)?(current\s+)?portfolio",
        r"correlat(?:ed|ion)\s+with\s+(the\s+)?(current\s+)?portfolio",
        r"portfolio[-\s]level\s+diversification",
        r"reduces?\s+(the\s+)?portfolio(?:'s)?\s+risk",
        r"hedges?\s+(the\s+)?(current\s+)?portfolio",
        r"portfolio-hq's\s+own\s+(current\s+)?holdings",
        r"diversif\w*[^.]{0,60}\bportfolio\b",
        r"\bportfolio\b[^.]{0,60}diversif\w*",
        r"\bportfolio\b[^.]{0,60}correlat(?:ed|ion)\w*",
        r"reduc\w*[^.]{0,60}\bportfolio\b[^.]{0,30}\b(risk|drawdown|volatility)\b",
        r"\bportfolio(?:'s)?\b[^.]{0,30}\b(risk|drawdown|volatility)\b[^.]{0,60}reduc\w*",
        r"\bportfolio\b[^.]{0,20}\bhedge\w*\b",
        r"\boffsets?[a-z]*[^.]{0,60}\bportfolio\b",
    )
]

_REQUIRED_DISCLOSURE_MARKERS = ("single-asset", "single asset")

# `rationale` is scanned unconditionally -- it is never expected to
# discuss the portfolio-level boundary at all, disclaiming or otherwise;
# a positive assertion has nowhere else to hide there, since every other
# field on this sub-object is a closed enum or the disclosure field
# itself. `single_asset_disclosure`'s own required job is to name and
# disclaim the portfolio-level boundary using this same vocabulary, so it
# is scanned with a bounded, sentence-scoped negation exception: a
# _PORTFOLIO_DIVERSIFICATION_PATTERNS match is permitted only when a
# genuine disclaiming-negation cue (a negation word paired with a
# disclaiming verb, or a "no <claim-noun> is established"-shaped
# quantifier negation) appears in the SAME sentence as the match. This is
# a bounded, sentence-level design -- lighter than economic_assessment_
# validator.py's own fully evolved per-claim, clause-boundary-whitelist
# architecture (which required several independent-review-driven
# correction rounds to reach), but tested against this schema's own real
# sealed content and a bounded adversarial matrix (ordering, absent
# negation, punctuation, active/passive wording) below.
_DISCLAIMING_NEGATION_PATTERN = re.compile(
    r"\b(?:does|do|did|is|are|will|can)\s+not\s+"
    r"(?:compute|constitute|imply|substitute|establish|determine|represent|assert|claim|find|show|demonstrate|indicate|prove)\w*"
    r"|\bnever\s+"
    r"(?:compute|constitute|impl\w*|substitute|establish\w*|determine\w*|represent\w*|assert\w*|claim\w*|find\w*|show\w*|demonstrate\w*|indicate\w*|prove\w*)",
    re.IGNORECASE,
)
_QUANTIFIER_NEGATION_CLAIM_PATTERN = re.compile(
    r"\bno\b[^.;:]{0,80}?\b(?:conclusion|finding|determination|benefit)\b[^.;:]{0,30}?"
    r"\b(?:is|are|was|were)\s+(?:established|drawn|made|supported|reached|claimed|found|identified)\w*",
    re.IGNORECASE,
)
_DECLARATIVE_DEFERRAL_PATTERN = re.compile(
    r"remains?\s+(?:separately\s+)?"
    r"(?:governed|unmeasured|unresolved|ungoverned|undetermined|unaddressed)\b",
    re.IGNORECASE,
)
_SENTENCE_SPLIT_PATTERN = re.compile(r"(?<=[.!?])\s+")


def _split_sentences(text: str) -> list[str]:
    return [s for s in _SENTENCE_SPLIT_PATTERN.split(text) if s]


def _sentence_has_disclaiming_cue(sentence: str) -> bool:
    return bool(
        _DISCLAIMING_NEGATION_PATTERN.search(sentence)
        or _QUANTIFIER_NEGATION_CLAIM_PATTERN.search(sentence)
        or _DECLARATIVE_DEFERRAL_PATTERN.search(sentence)
    )


def _scan_portfolio_diversification_claims(
    text: str, path: str, errors: list[str], *, allow_disclaiming_negation: bool
) -> None:
    """Scan `text` for a whole-portfolio diversification/correlation
    claim. When `allow_disclaiming_negation` is False (rationale), any
    match is rejected outright. When True (single_asset_disclosure), a
    match is rejected only when its OWN sentence contains no disclaiming
    negation/deferral cue -- a genuine claim sitting in a sentence with no
    negation anywhere is never accidentally shielded by a negation that
    governs a different sentence."""
    if not isinstance(text, str) or not text:
        return
    if not allow_disclaiming_negation:
        for pattern in _PORTFOLIO_DIVERSIFICATION_PATTERNS:
            if pattern.search(text):
                errors.append(
                    f"{path}: rationale asserts a whole-portfolio diversification-benefit or "
                    f"correlation-to-the-current-portfolio claim -- rationale must characterize "
                    f"only this instrument's own single-asset historical behavior "
                    f"(XASSET-0010 SSH, supporting artifact SS7 non-duplication boundary), "
                    f"matching pattern {pattern.pattern!r}"
                )
        return

    for sentence in _split_sentences(text):
        has_cue = _sentence_has_disclaiming_cue(sentence)
        for pattern in _PORTFOLIO_DIVERSIFICATION_PATTERNS:
            if pattern.search(sentence) and not has_cue:
                errors.append(
                    f"{path}: single_asset_disclosure asserts a whole-portfolio diversification-"
                    f"benefit or correlation-to-the-current-portfolio claim without a disclaiming "
                    f"negation in the same sentence -- this field must only disclaim, never assert, "
                    f"such a finding (XASSET-0010 SSH, supporting artifact SS7 non-duplication "
                    f"boundary), matching pattern {pattern.pattern!r}"
                )


# ── cross-coin-correlation non-leakage (AA SS6.1, SS9 point 11) -- a
#    materially independent mechanism from check 10 above (a claim about
#    another NAMED COIN, not about "the portfolio") and from the general
#    numeric-pattern scan (check 6, which does not target decimals near
#    "correlat*" specifically) ───────────────────────────────────────────

_COIN_NAME_GROUPS = {
    "BTC": ("btc", "bitcoin"),
    "ETH": ("eth", "ethereum"),
    "SOL": ("sol", "solana"),
}
_ALL_COIN_NAME_ALTERNATION = "|".join(
    re.escape(name) for names in _COIN_NAME_GROUPS.values() for name in names
)
_CORRELATION_CLAIM_PATTERNS = [
    re.compile(p, re.IGNORECASE) for p in (
        # Two coin names co-occurring with a correlation/co-movement word
        # within a bounded same-sentence-scale window, either order.
        rf"\b(?:{_ALL_COIN_NAME_ALTERNATION})\b[^.]{{0,80}}\bcorrelat\w*[^.]{{0,80}}\b(?:{_ALL_COIN_NAME_ALTERNATION})\b",
        rf"\bcorrelat\w*[^.]{{0,80}}\b(?:{_ALL_COIN_NAME_ALTERNATION})\b[^.]{{0,80}}\b(?:{_ALL_COIN_NAME_ALTERNATION})\b",
        rf"\b(?:{_ALL_COIN_NAME_ALTERNATION})\b[^.]{{0,60}}\bmove\w*\s+(?:in\s+tandem|together)\b",
        rf"\b(?:{_ALL_COIN_NAME_ALTERNATION})\b[^.]{{0,60}}\btrack\w*\s+(?:each\s+other|one\s+another)\b",
        rf"\b(?:{_ALL_COIN_NAME_ALTERNATION})\b[^.]{{0,60}}\bin\s+lockstep\b",
    )
]
# A bare decimal figure in the vicinity of "correlat*" -- a correlation
# coefficient need not be percent-shaped.
_CORRELATION_COEFFICIENT_PATTERN = re.compile(
    r"correlat\w*[^.]{0,40}[-]?0?\.\d+|[-]?0?\.\d+[^.]{0,40}correlat\w*", re.IGNORECASE,
)


def _mentions_two_distinct_coins(text: str) -> bool:
    mentioned = set()
    lowered = text.lower()
    for canonical, names in _COIN_NAME_GROUPS.items():
        for name in names:
            if re.search(rf"\b{re.escape(name)}\b", lowered):
                mentioned.add(canonical)
                break
    return len(mentioned) >= 2


def _scan_cross_coin_correlation_leakage(value: object, path: str, errors: list[str]) -> None:
    """Recursively scan every free-text string for a claim that two (or
    more) of BTC/ETH/SOL are, or are not, correlated with each other, and
    for a bare numeric correlation coefficient anywhere -- rejected
    unconditionally, no negation exception (unlike check 10, this schema
    has no legitimate reason to ever discuss cross-coin correlation at
    all, disclaiming or otherwise; that discussion belongs exclusively to
    a future, separate, bounded correlation-study charter, never inside
    this record)."""
    if isinstance(value, dict):
        for k, v in value.items():
            _scan_cross_coin_correlation_leakage(v, f"{path}.{k}", errors)
    elif isinstance(value, list):
        for i, item in enumerate(value):
            _scan_cross_coin_correlation_leakage(item, f"{path}[{i}]", errors)
    elif isinstance(value, str):
        if _mentions_two_distinct_coins(value):
            for pattern in _CORRELATION_CLAIM_PATTERNS:
                if pattern.search(value):
                    errors.append(
                        f"{path}: contains a claim that two or more of BTC/ETH/SOL are (or are "
                        f"not) correlated with each other -- a cross-coin correlation study "
                        f"remains a separate, future, bounded, pre-registered research charter's "
                        f"own question, never asserted or implied by this schema "
                        f"(XASSET-0010 SSF, supporting artifact SS6.1/SS9 point 11)"
                    )
        if _CORRELATION_COEFFICIENT_PATTERN.search(value):
            errors.append(
                f"{path}: contains a numeric correlation-coefficient-shaped token -- no "
                f"correlation coefficient of any kind is permitted anywhere in this schema "
                f"(XASSET-0010 supporting artifact SS9 point 11)"
            )


@dataclass
class ValidationResult:
    valid: bool
    errors: list[str] = field(default_factory=list)
    source: str | None = None


@dataclass
class DirectoryValidationResult:
    """A missing or empty directory is valid, zero-coverage state -- same
    filesystem-as-index doctrine every prior Intelligence validator in
    this repository already applies."""
    valid: bool
    results: list[ValidationResult] = field(default_factory=list)

    @property
    def record_count(self) -> int:
        return len(self.results)


# ── canonical hashing -- excludes only the five seal fields ────────────────

_HASHABLE_KEYS = tuple(k for k in _ALL_TOP_LEVEL_KEYS if k not in _SEAL_REQUIRED_KEYS)


def canonical_record_hash(data: dict) -> str:
    """SHA-256 of the record's full content (envelope + structural
    reference + the one asset-type-conditional axis + evidence_quality),
    canonical sorted-key JSON, UTF-8 -- excludes every seal field.
    Asset-type-conditional fields naturally participate only when present
    (`data.get(...)` returns `None` for an absent key, same as any other
    absent key)."""
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
            f"closed; only {sorted(allowed)} are permitted (XASSET-0010 supporting artifact SS4)"
        )


def _scan_forbidden_keys(value: object, path: str, errors: list[str]) -> None:
    """Structural scan: a forbidden key name anywhere in the document
    tree, not just at the top level (AA SS9 points 5/6)."""
    if isinstance(value, dict):
        for k, v in value.items():
            key_str = str(k)
            if key_str in _FORBIDDEN_KEY_NAMES:
                kind = "a numeric score/rank/target/hurdle-rate-shaped field"
                for group, label in _CROSS_SCHEMA_LEAKAGE_GROUPS:
                    if key_str in group:
                        kind = label
                        break
                errors.append(
                    f"{path}.{key_str}: forbidden key name -- {kind} must never appear in an "
                    f"instrument-economic-assessment record (XASSET-0010 supporting artifact "
                    f"SS9 points 5/6)"
                )
            _scan_forbidden_keys(v, f"{path}.{key_str}", errors)
    elif isinstance(value, list):
        for i, item in enumerate(value):
            _scan_forbidden_keys(item, f"{path}[{i}]", errors)


def _scan_free_text_strings(value: object, path: str, errors: list[str], *, in_citation: bool = False) -> None:
    """Recursively scan every free-text string value for forbidden
    recommendation-shaped phrases, directive/trading language, chart-
    derived terminology, and any bare numeric-percent-shaped token (no
    carve-out of any kind, AA SS9 point 6). `provenance.sources[].
    source_identifier`/`.limitation` are pure citation strings (never
    judgment prose) and are exempted from the directive-word check only."""
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
                        f"hold/trim/exit/wait/stage signal is permitted in any field, under any "
                        f"framing (XASSET-0010 SSD.6)"
                    )
        for term, pattern in _CHART_PATTERNS:
            if pattern.search(value):
                errors.append(
                    f"{path}: contains chart-derived terminology {term!r} -- no chart evidence "
                    f"of any kind is permitted (XASSET-0010 supporting artifact SS9 point 7)"
                )
        if _NUMERIC_PERCENT_PATTERN.search(value):
            errors.append(
                f"{path}: contains a bare numeric-percent-shaped token -- no numeric field or "
                f"figure of any kind is permitted anywhere in this schema, with no carve-out "
                f"(XASSET-0010 SSD.3, supporting artifact SS9 point 6)"
            )


def _scan_predictive_language(value: dict, sub_field_name: str, errors: list[str]) -> None:
    """AA SS9 point 9: a dedicated, independent scan for forward-looking
    terms, scoped to exactly historical_equity_market_drawdown_behavior's
    and historical_inflation_sensitivity_narrative's own free-text fields
    -- both sub-fields are backward-looking historical characterizations
    only, never a forecast."""
    if not isinstance(value, dict):
        return
    for key in ("rationale", "single_asset_disclosure"):
        text = value.get(key)
        if not isinstance(text, str):
            continue
        for term, pattern in _PREDICTIVE_PATTERNS:
            if pattern.search(text):
                errors.append(
                    f"{sub_field_name}.{key}: contains predictive/forward-looking language "
                    f"{term!r} -- this sub-field is a historically-grounded, backward-looking "
                    f"characterization only, never a forecast (XASSET-0010 supporting artifact "
                    f"SS9 point 9)"
                )


def _validate_cost_and_tracking(value: object, errors: list[str]) -> None:
    if not isinstance(value, dict):
        errors.append("cost_and_tracking_quality_economic_significance must be a mapping")
        return
    _reject_unknown_keys(
        value, "cost_and_tracking_quality_economic_significance", _COST_TRACKING_ALLOWED_KEYS, errors,
    )
    category = value.get("significance_category")
    if category not in _COST_TRACKING_SIGNIFICANCE_VALUES:
        errors.append(
            f"cost_and_tracking_quality_economic_significance.significance_category must be one "
            f"of {sorted(_COST_TRACKING_SIGNIFICANCE_VALUES)} -- got {category!r}"
        )
    if not _non_empty_str(value.get("rationale")):
        errors.append("cost_and_tracking_quality_economic_significance.rationale must be a non-empty string")
    if category == _UNABLE_TO_DETERMINE_VALUE:
        if not _non_empty_str(value.get("abstention_reason")):
            errors.append(
                "cost_and_tracking_quality_economic_significance.abstention_reason is required "
                "and must be non-empty when significance_category is 'unable_to_determine'"
            )
    elif "abstention_reason" in value:
        errors.append(
            "cost_and_tracking_quality_economic_significance.abstention_reason is only permitted "
            "when significance_category is 'unable_to_determine'"
        )


def _validate_drawdown_behavior(value: object, errors: list[str]) -> None:
    if not isinstance(value, dict):
        errors.append("macro_behavioral_characterization.historical_equity_market_drawdown_behavior must be a mapping")
        return
    field_name = "macro_behavioral_characterization.historical_equity_market_drawdown_behavior"
    _reject_unknown_keys(value, field_name, _DRAWDOWN_BEHAVIOR_ALLOWED_KEYS, errors)
    category = value.get("behavior_category")
    if category not in _DRAWDOWN_BEHAVIOR_VALUES:
        errors.append(f"{field_name}.behavior_category must be one of {sorted(_DRAWDOWN_BEHAVIOR_VALUES)} -- got {category!r}")
    if not _non_empty_str(value.get("rationale")):
        errors.append(f"{field_name}.rationale must be a non-empty string")
    if not _non_empty_str(value.get("single_asset_disclosure")):
        errors.append(f"{field_name}.single_asset_disclosure is required and must be non-empty (XASSET-0010 SSH)")
    else:
        disclosure = value["single_asset_disclosure"].lower()
        if not any(marker in disclosure for marker in _REQUIRED_DISCLOSURE_MARKERS):
            errors.append(
                f"{field_name}.single_asset_disclosure must explicitly state the finding is "
                f"single-asset (XASSET-0010 SSH)"
            )
    if category == _UNABLE_TO_DETERMINE_VALUE:
        if not _non_empty_str(value.get("abstention_reason")):
            errors.append(f"{field_name}.abstention_reason is required and must be non-empty when behavior_category is 'unable_to_determine'")
    elif "abstention_reason" in value:
        errors.append(f"{field_name}.abstention_reason is only permitted when behavior_category is 'unable_to_determine'")

    _scan_portfolio_diversification_claims(
        value.get("rationale"), f"{field_name}.rationale", errors, allow_disclaiming_negation=False,
    )
    _scan_portfolio_diversification_claims(
        value.get("single_asset_disclosure"), f"{field_name}.single_asset_disclosure", errors,
        allow_disclaiming_negation=True,
    )
    _scan_predictive_language(value, field_name, errors)


def _validate_inflation_sensitivity(value: object, errors: list[str]) -> None:
    if not isinstance(value, dict):
        errors.append("macro_behavioral_characterization.historical_inflation_sensitivity_narrative must be a mapping")
        return
    field_name = "macro_behavioral_characterization.historical_inflation_sensitivity_narrative"
    _reject_unknown_keys(value, field_name, _INFLATION_SENSITIVITY_ALLOWED_KEYS, errors)
    category = value.get("sensitivity_category")
    if category not in _INFLATION_SENSITIVITY_VALUES:
        errors.append(f"{field_name}.sensitivity_category must be one of {sorted(_INFLATION_SENSITIVITY_VALUES)} -- got {category!r}")
    if not _non_empty_str(value.get("rationale")):
        errors.append(f"{field_name}.rationale must be a non-empty string")
    if category == _UNABLE_TO_DETERMINE_VALUE:
        if not _non_empty_str(value.get("abstention_reason")):
            errors.append(f"{field_name}.abstention_reason is required and must be non-empty when sensitivity_category is 'unable_to_determine'")
    elif "abstention_reason" in value:
        errors.append(f"{field_name}.abstention_reason is only permitted when sensitivity_category is 'unable_to_determine'")

    _scan_predictive_language(value, field_name, errors)


def _validate_macro_behavioral(value: object, errors: list[str]) -> None:
    if not isinstance(value, dict):
        errors.append("macro_behavioral_characterization must be a mapping")
        return
    _reject_unknown_keys(value, "macro_behavioral_characterization", _MACRO_BEHAVIORAL_ALLOWED_KEYS, errors)
    missing = _MACRO_BEHAVIORAL_SUB_FIELDS - value.keys()
    if missing:
        errors.append(f"macro_behavioral_characterization missing required sub-field(s): {sorted(missing)}")
    if "historical_equity_market_drawdown_behavior" in value:
        _validate_drawdown_behavior(value["historical_equity_market_drawdown_behavior"], errors)
    if "historical_inflation_sensitivity_narrative" in value:
        _validate_inflation_sensitivity(value["historical_inflation_sensitivity_narrative"], errors)


def _validate_evidence_quality(value: object, errors: list[str]) -> None:
    if not _require_keys(value, "evidence_quality", _EVIDENCE_QUALITY_ALLOWED_KEYS, errors):
        return
    value = value  # type: dict
    _reject_unknown_keys(value, "evidence_quality", _EVIDENCE_QUALITY_ALLOWED_KEYS, errors)
    if value.get("primary_source_coverage") not in _PRIMARY_SOURCE_COVERAGE_VALUES:
        errors.append(f"evidence_quality.primary_source_coverage must be one of {sorted(_PRIMARY_SOURCE_COVERAGE_VALUES)} -- got {value.get('primary_source_coverage')!r}")
    if not _non_empty_str(value.get("thesis_uncertainty_statement")):
        errors.append("evidence_quality.thesis_uncertainty_statement must be a non-empty string")


def _validate_provenance(value: object, errors: list[str]) -> None:
    if not _require_keys(value, "provenance", _PROVENANCE_ALLOWED_KEYS, errors):
        return
    value = value  # type: dict
    _reject_unknown_keys(value, "provenance", _PROVENANCE_ALLOWED_KEYS, errors)
    sources = value.get("sources")
    if not isinstance(sources, list) or not sources:
        errors.append("provenance.sources must be a non-empty list")
        return
    for i, src in enumerate(sources):
        label = f"provenance.sources[{i}]"
        if not _require_keys(src, label, _SOURCE_REQUIRED_KEYS, errors):
            continue
        _reject_unknown_keys(src, label, _SOURCE_ALLOWED_KEYS, errors)
        if not _non_empty_str(src.get("source_identifier")):
            errors.append(f"{label}.source_identifier must be a non-empty string")
        if src.get("source_type") not in _SOURCE_TYPE_VALUES:
            errors.append(f"{label}.source_type must be one of {sorted(_SOURCE_TYPE_VALUES)} -- got {src.get('source_type')!r}")
        if not _non_empty_str(src.get("as_of_date")):
            errors.append(f"{label}.as_of_date must be a non-empty string")
        if src.get("access_status") not in _ACCESS_STATUS_VALUES:
            errors.append(f"{label}.access_status must be one of {sorted(_ACCESS_STATUS_VALUES)} -- got {src.get('access_status')!r}")


def _validate_structural_reference(
    value: object, *, instrument_id: object, asset_type: object, repo_root: Path | None, errors: list[str],
) -> None:
    if not _require_keys(value, "structural_reference", _STRUCTURAL_REFERENCE_ALLOWED_KEYS, errors):
        return
    value = value  # type: dict
    _reject_unknown_keys(value, "structural_reference", _STRUCTURAL_REFERENCE_ALLOWED_KEYS, errors)

    if value.get("source_instrument_id") != instrument_id:
        errors.append(
            f"structural_reference.source_instrument_id must equal the record's own "
            f"instrument_id ({instrument_id!r}) -- got {value.get('source_instrument_id')!r}"
        )

    if asset_type not in _ASSET_TYPE_VALUES:
        # Already flagged by the top-level asset_type check; nothing further to verify here.
        return

    expected_schema = _EXPECTED_SOURCE_SCHEMA_BY_ASSET_TYPE[asset_type]
    if value.get("source_schema") != expected_schema:
        errors.append(
            f"structural_reference.source_schema must be exactly {expected_schema!r} for "
            f"asset_type {asset_type!r} -- got {value.get('source_schema')!r}"
        )

    ticker = instrument_id if _non_empty_str(instrument_id) else "<unknown>"
    expected_file = _EXPECTED_SOURCE_FILE_TEMPLATE_BY_ASSET_TYPE[asset_type].format(ticker=ticker)
    if value.get("source_file") != expected_file:
        errors.append(
            f"structural_reference.source_file must be exactly {expected_file!r} -- got "
            f"{value.get('source_file')!r}"
        )

    recorded_hash = value.get("referenced_content_sha256")
    if not _non_empty_str(recorded_hash):
        errors.append("structural_reference.referenced_content_sha256 must be a non-empty string")
        return
    if repo_root is None:
        return

    target_path = repo_root.joinpath(*_SOURCE_DIR_BY_ASSET_TYPE[asset_type], f"{ticker}.yaml")
    if not target_path.is_file():
        errors.append(f"structural_reference could not be verified -- {expected_file} does not exist")
        return
    try:
        target_data = yaml.safe_load(target_path.read_text())
    except yaml.YAMLError as exc:
        errors.append(f"structural_reference could not be verified -- {expected_file} is invalid YAML: {exc}")
        return
    if not isinstance(target_data, dict):
        errors.append(f"structural_reference could not be verified -- {expected_file} did not parse to a mapping")
        return

    hash_fn = _CANONICAL_HASH_FN_BY_ASSET_TYPE[asset_type]
    live_hash = hash_fn(target_data)
    if recorded_hash != live_hash:
        errors.append(
            f"structural_reference.referenced_content_sha256 is stale -- recorded "
            f"{recorded_hash!r}, live-recomputed {live_hash!r} against the current sealed "
            f"{expected_file} (XASSET-0010 supporting artifact SS3)"
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
    'unable_to_determine' -- the one closed-vocabulary abstention value
    this schema's two substantive axes/sub-fields unambiguously treat as
    a genuine abstention. This schema defines no 'not_applicable' value
    anywhere, so no cascading/exemption logic is needed beyond the two
    independently-abstainable crypto sub-fields (AA SS6.2)."""
    pairs: list[tuple[str, str]] = []

    cost_tracking = data.get("cost_and_tracking_quality_economic_significance")
    if isinstance(cost_tracking, dict) and cost_tracking.get("significance_category") == _UNABLE_TO_DETERMINE_VALUE:
        pairs.append(("cost_and_tracking_quality_economic_significance", "significance_category"))

    macro = data.get("macro_behavioral_characterization")
    if isinstance(macro, dict):
        drawdown = macro.get("historical_equity_market_drawdown_behavior")
        if isinstance(drawdown, dict) and drawdown.get("behavior_category") == _UNABLE_TO_DETERMINE_VALUE:
            pairs.append(("macro_behavioral_characterization.historical_equity_market_drawdown_behavior", "behavior_category"))
        inflation = macro.get("historical_inflation_sensitivity_narrative")
        if isinstance(inflation, dict) and inflation.get("sensitivity_category") == _UNABLE_TO_DETERMINE_VALUE:
            pairs.append(("macro_behavioral_characterization.historical_inflation_sensitivity_narrative", "sensitivity_category"))

    return pairs


def _check_abstention_index_completeness(data: dict, errors: list[str]) -> None:
    """AA SS9 point 15: abstention_index is a mechanical rollup a future
    cross-asset synthesis unit can scan without re-reading every axis --
    that guarantee requires every genuine abstention to actually appear
    in it, not merely a self-declared list left unreconciled against the
    axes it claims to summarize (the same defect class etf_classification_
    validator.py's own disclosed v1.1 finding names)."""
    actual = _find_abstention_fields(data)
    index = data.get("abstention_index")
    if not isinstance(index, list):
        return  # already flagged by _validate_abstention_index
    indexed = {(entry.get("axis"), entry.get("field")) for entry in index if isinstance(entry, dict)}
    for axis, field_name in actual:
        if (axis, field_name) not in indexed:
            errors.append(
                f"abstention_index is missing an entry for {axis}.{field_name} -- every genuine "
                f"unable_to_determine abstention must be represented in abstention_index "
                f"(XASSET-0010 supporting artifact SS9 point 15), not merely self-declared and "
                f"left unreconciled"
            )
    actual_set = set(actual)
    for axis, field_name in indexed:
        if (axis, field_name) not in actual_set:
            errors.append(
                f"abstention_index contains an entry for {axis}.{field_name} that does not "
                f"correspond to any genuine 'unable_to_determine' value actually present in the "
                f"record (XASSET-0010 supporting artifact SS9 point 15)"
            )


def _validate_envelope_projection_consistency(data: dict, errors: list[str]) -> None:
    """AA SS4.6: every cross_asset_handoff field is a read-only copy,
    never independently computed -- checked for exact consistency against
    its source. This schema has no structural_risk_flags field (unlike
    the ETF/functional-doctrine schemas) and no deployability_summary
    field (unlike the GLD/CASH_LIKE_CAPITAL schema, which has a
    deployability_and_optionality axis this schema deliberately lacks)."""
    eq = data.get("evidence_quality") or {}
    if isinstance(eq, dict):
        if data.get("uncertainty_summary") != eq.get("thesis_uncertainty_statement"):
            errors.append(
                "uncertainty_summary must exactly equal evidence_quality.thesis_uncertainty_"
                "statement (AA SS4.1 read-only-projection rule)"
            )
        if data.get("evidence_quality_status") != eq.get("primary_source_coverage"):
            errors.append(
                "evidence_quality_status must exactly equal evidence_quality."
                "primary_source_coverage (AA SS4.1 read-only-projection rule)"
            )

    handoff = data.get("cross_asset_handoff")
    if not isinstance(handoff, dict):
        errors.append("cross_asset_handoff must be a mapping")
        return

    _reject_unknown_keys(handoff, "cross_asset_handoff", _CROSS_ASSET_HANDOFF_ALLOWED_KEYS, errors)
    missing = _CROSS_ASSET_HANDOFF_ALLOWED_KEYS - handoff.keys()
    if missing:
        errors.append(f"cross_asset_handoff missing required key(s): {sorted(missing)}")

    if isinstance(eq, dict) and handoff.get("evidence_quality_summary") != eq.get("primary_source_coverage"):
        errors.append(
            "cross_asset_handoff.evidence_quality_summary must exactly equal evidence_quality."
            "primary_source_coverage (AA SS4.6)"
        )
    if handoff.get("uncertainty_summary") != data.get("uncertainty_summary"):
        errors.append(
            "cross_asset_handoff.uncertainty_summary must exactly equal the envelope's own "
            "uncertainty_summary (AA SS4.6)"
        )

    asset_type = data.get("asset_type")
    expected_summary = None
    if asset_type == "etf":
        cost_tracking = data.get("cost_and_tracking_quality_economic_significance")
        if isinstance(cost_tracking, dict):
            expected_summary = cost_tracking.get("significance_category")
    elif asset_type == "cryptocurrency":
        macro = data.get("macro_behavioral_characterization")
        if isinstance(macro, dict):
            drawdown = macro.get("historical_equity_market_drawdown_behavior")
            inflation = macro.get("historical_inflation_sensitivity_narrative")
            if isinstance(drawdown, dict) and isinstance(inflation, dict):
                expected_summary = {
                    "historical_equity_market_drawdown_behavior": drawdown.get("behavior_category"),
                    "historical_inflation_sensitivity_narrative": inflation.get("sensitivity_category"),
                }
    if expected_summary is not None and handoff.get("economic_characterization_summary") != expected_summary:
        errors.append(
            "cross_asset_handoff.economic_characterization_summary must exactly equal the one "
            "populated substantive axis's own categorical determination(s), verbatim (AA SS4.6)"
        )


def _validate_asset_type_conditional_shape(data: dict, asset_type: object, errors: list[str]) -> None:
    """AA SS9 point 3: cost_and_tracking_quality_economic_significance
    required on etf only, forbidden on cryptocurrency; macro_behavioral_
    characterization required on cryptocurrency only, forbidden on etf."""
    has_cost_tracking = "cost_and_tracking_quality_economic_significance" in data
    has_macro = "macro_behavioral_characterization" in data

    if asset_type == "etf":
        if not has_cost_tracking:
            errors.append("record missing required field for asset_type 'etf': cost_and_tracking_quality_economic_significance")
        else:
            _validate_cost_and_tracking(data["cost_and_tracking_quality_economic_significance"], errors)
        if has_macro:
            errors.append("macro_behavioral_characterization is forbidden (rejected as an unknown key) on asset_type 'etf'")
    elif asset_type == "cryptocurrency":
        if not has_macro:
            errors.append("record missing required field for asset_type 'cryptocurrency': macro_behavioral_characterization")
        else:
            _validate_macro_behavioral(data["macro_behavioral_characterization"], errors)
        if has_cost_tracking:
            errors.append("cost_and_tracking_quality_economic_significance is forbidden (rejected as an unknown key) on asset_type 'cryptocurrency'")
    else:
        # asset_type itself invalid -- already flagged elsewhere; still
        # scan whichever axis is present so its own errors surface too.
        if has_cost_tracking:
            _validate_cost_and_tracking(data["cost_and_tracking_quality_economic_significance"], errors)
        if has_macro:
            _validate_macro_behavioral(data["macro_behavioral_characterization"], errors)


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
            f"envelope, structural_reference, the one asset-type-conditional axis, "
            f"evidence_quality, and seal fields are permitted, no third substantive judgment "
            f"axis (XASSET-0010 supporting artifact SS4.1)"
        )


# ── public API: in-memory record validation ─────────────────────────────

def validate_instrument_economic_assessment_data(
    data: object,
    *,
    source: str | None = None,
    authorized_population: frozenset[str] = AUTHORIZED_POPULATION,
    repo_root: Path | None = None,
) -> ValidationResult:
    """Validate an already-parsed instrument-economic-assessment mapping.
    Never touches the filesystem except for the live SPY/VEA/VWO.yaml or
    BTC/ETH/SOL.yaml structural-reference-hash recomputes when
    `repo_root` is supplied."""
    errors: list[str] = []

    if not isinstance(data, dict):
        errors.append(f"root document must be a mapping, got {type(data).__name__}")
        return ValidationResult(valid=False, errors=errors, source=source)

    instrument_id = data.get("instrument_id")
    if not _non_empty_str(instrument_id):
        errors.append("instrument_id must be a non-empty string")
    elif authorized_population and instrument_id not in authorized_population:
        errors.append(
            f"instrument_id {instrument_id!r} is not in the authorized six-instrument "
            f"population {sorted(authorized_population)} (XASSET-0010 SSB) -- no GLD, "
            f"CASH_LIKE_CAPITAL, DEBT_REDUCTION, QQQ, or any seventh instrument is authorized "
            f"without its own separate schema-amendment decision"
        )

    asset_type = data.get("asset_type")
    if asset_type not in _ASSET_TYPE_VALUES:
        errors.append(f"asset_type must be one of {sorted(_ASSET_TYPE_VALUES)} -- got {asset_type!r}")
    elif _non_empty_str(instrument_id) and instrument_id in _ASSET_TYPE_BY_INSTRUMENT:
        expected_asset_type = _ASSET_TYPE_BY_INSTRUMENT[instrument_id]
        if asset_type != expected_asset_type:
            errors.append(
                f"asset_type {asset_type!r} does not match instrument_id {instrument_id!r}'s own "
                f"real classification-layer asset_type {expected_asset_type!r} (XASSET-0010 "
                f"supporting artifact SS4.1)"
            )

    if not _non_empty_str(data.get("schema_version")):
        errors.append("schema_version must be a non-empty string")

    if "structural_reference" not in data:
        errors.append("record missing required field: structural_reference")
    else:
        _validate_structural_reference(
            data["structural_reference"], instrument_id=instrument_id, asset_type=asset_type,
            repo_root=repo_root, errors=errors,
        )

    _validate_asset_type_conditional_shape(data, asset_type, errors)

    if "evidence_quality" not in data:
        errors.append("record missing required field: evidence_quality")
    else:
        _validate_evidence_quality(data["evidence_quality"], errors)

    if "provenance" not in data:
        errors.append("record missing required field: provenance")
    else:
        _validate_provenance(data["provenance"], errors)

    if "abstention_index" not in data:
        errors.append("record missing required field: abstention_index")
    else:
        _validate_abstention_index(data["abstention_index"], errors)
        _check_abstention_index_completeness(data, errors)

    if not _non_empty_str(data.get("uncertainty_summary")):
        errors.append("uncertainty_summary must be a non-empty string")

    _validate_no_stray_top_level_fields(data, errors)
    _validate_envelope_projection_consistency(data, errors)
    _validate_seal(data, errors)

    label = str(instrument_id) if _non_empty_str(instrument_id) else "<record>"
    _scan_forbidden_keys(data, label, errors)
    _scan_free_text_strings(data, label, errors)
    _scan_cross_coin_correlation_leakage(data, label, errors)

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


def validate_instrument_economic_assessment_file(
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

    result = validate_instrument_economic_assessment_data(
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
    "instrument_id", "asset_type", "sealed_at", "content_sha256", "schema_version",
    "governing_decision", "record_path",
})
_MANIFEST_ROW_ALLOWED_KEYS = _MANIFEST_REQUIRED_ROW_KEYS
_MANIFEST_TOP_LEVEL_ALLOWED_KEYS = frozenset({"schema_version", "governing_decision", "cohort"})


def validate_cohort_manifest(
    manifest_data: object,
    records_by_instrument_id: dict[str, dict],
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

        expected_asset_type = _ASSET_TYPE_BY_INSTRUMENT.get(instrument_id)
        if expected_asset_type is not None and row.get("asset_type") != expected_asset_type:
            errors.append(
                f"cohort[{i}] ({instrument_id!r}) asset_type {row.get('asset_type')!r} does not "
                f"match the expected {expected_asset_type!r}"
            )

        record = records_by_instrument_id.get(instrument_id)
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
            errors.append(f"cohort manifest is missing authorized instrument_id(s): {sorted(missing_from_manifest)}")
        extra = seen - authorized_population
        if extra:
            errors.append(f"cohort manifest lists instrument_id(s) outside the authorized population: {sorted(extra)}")

    orphans = set(records_by_instrument_id) - seen
    if orphans:
        errors.append(f"sealed record(s) exist with no corresponding cohort manifest entry: {sorted(orphans)}")

    return ValidationResult(valid=not errors, errors=errors, source=_MANIFEST_FILENAME)


def validate_instrument_economic_assessment_directory(
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
        validate_instrument_economic_assessment_file(p, authorized_population=authorized_population, repo_root=repo_root)
        for p in yaml_paths
    ]

    records_by_instrument_id: dict[str, dict] = {}
    for p in yaml_paths:
        data, read_errors = _read_yaml(p)
        if not read_errors and isinstance(data, dict) and _non_empty_str(data.get("instrument_id")):
            records_by_instrument_id[data["instrument_id"]] = data

    manifest_path = directory / _MANIFEST_FILENAME
    if manifest_path.is_file():
        manifest_data, read_errors = _read_yaml(manifest_path)
        if read_errors:
            results.append(ValidationResult(valid=False, errors=read_errors, source=str(manifest_path)))
        else:
            results.append(
                validate_cohort_manifest(manifest_data, records_by_instrument_id, authorized_population=authorized_population)
            )
    elif records_by_instrument_id:
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
    _result = validate_instrument_economic_assessment_directory(
        _repo_root / "intelligence" / "instrument_economic_assessment", repo_root=_repo_root,
    )
    if _result.valid:
        print(f"instrument_economic_assessment_validator: OK ({_result.record_count} result(s))")
        sys.exit(0)
    else:
        print("instrument_economic_assessment_validator: FAILED")
        for _r in _result.results:
            if not _r.valid:
                for _err in _r.errors:
                    print(f"  - [{_r.source}] {_err}")
        sys.exit(1)
