"""
economic_assessment_validator.py -- read-only schema validator for the
first (and only, per XASSET-0009's own bounded authorization) WS-0014
economic-assessment content batch, authored against the closed
GLD/CASH_LIKE_CAPITAL economic-assessment methodology
`governance/decisions/XASSET-0008-gld-cash-reserve-economic-assessment-
methodology.md`'s supporting artifact
(`governance/audits/WS0014_GLD_CASH_RESERVE_ECONOMIC_ASSESSMENT_
METHODOLOGY_DESIGN_20260809.md`, SS4/SS5/SS9/SS11) designed, for the one
implementation PR authorized by `governance/decisions/XASSET-0009-ws0014-
gld-cash-like-economic-assessment-content-authorization.md`.

Scope, exactly what is validated:

- Source-of-truth convention: `intelligence/economic_assessment/
  <ANALYTICAL_SUBJECT>.yaml`, one file per analytical subject, single-file
  (no paired Markdown), filesystem is the index, plus
  `COHORT_MANIFEST.yaml` -- mirrors every prior classification framework's
  own convention exactly.
- Exactly two `analytical_subject` values: `GLD`, `CASH_LIKE_CAPITAL` --
  no `CASH` or `RESERVE` as a standalone value, no `DEBT_REDUCTION`
  (XASSET-0008 SSB, SS11 point 1).
- One shared substantive axis (`deployability_and_optionality`, computed
  once per analytical subject) plus one GLD-only compound axis
  (`instrument_specific_economic_characterization`, `not_applicable: true`
  literal marker on `CASH_LIKE_CAPITAL`) plus `evidence_quality` on both --
  no third substantive axis, no numeric field of any kind anywhere, with
  **no** carve-out of any kind (XASSET-0008 SSG -- stricter than the ETF
  framework's own scoped `expense_ratio_pct` exception; stricter than the
  functional-doctrine schema's own numeric-key-only scan, since this
  schema additionally rejects every bare numeric-percent-shaped token in
  free text, no carve-out).
- `structural_reference_etf_classification` / `structural_reference_
  functional_doctrine` -- required, both present, `GLD` only; forbidden
  (rejected as unknown keys) on `CASH_LIKE_CAPITAL`. Both independently,
  live-recompute their pinned record's hash on every validator run via a
  **read-only** call to the existing `canonical_record_hash()` functions
  in `etf_classification_validator` and `functional_doctrine_validator`
  respectively -- a stale reference is mechanically detected and rejected
  (XASSET-0008 SSH, supporting artifact SS5).
- `legacy_structural_references` -- a list of **exactly two** entries
  (`source_capital_use_type: "CASH"`, `source_capital_use_type:
  "RESERVE"`), each independently, live-recomputing its own hash via
  `functional_doctrine_validator.canonical_record_hash()`, `CASH_LIKE_
  CAPITAL` only; forbidden on `GLD`. Neither pinned record's own field
  values may be copied, restated, or treated as a `CASH_LIKE_CAPITAL`-
  level finding (supporting artifact SS5, SS7).
- A dedicated, materially independent free-text scan rejecting any claim,
  however hedged, that `CASH` and `RESERVE` individually warrant
  different treatment or that their different `target_pct` values are
  meaningful as evidence (XASSET-0008 SSD.4, supporting artifact SS11
  point 15) -- a genuinely separate mechanism from the `legacy_
  structural_references` hash-reconciliation check (point 8), learning
  directly from `TIER-0004`'s own dangling-reference correction history.
- Abstention: `unable_to_determine` with a required, non-empty
  `abstention_reason` on every substantive axis/sub-field; `not_
  applicable` reserved for `instrument_specific_economic_
  characterization` on `CASH_LIKE_CAPITAL` specifically (a structurally
  absent concept, not an evidence gap). Abstention does not cascade
  between axes or sub-fields (XASSET-0008 SSJ, supporting artifact SS4.2/
  SS4.3).
- GLD / overlap-model non-duplication: every `GLD` record's
  `historical_equity_drawdown_behavior` sub-field must carry a non-empty
  `single_asset_disclosure` and must never assert a whole-portfolio
  diversification-benefit or correlation-to-the-current-portfolio claim
  anywhere in its own free text -- that remains `defensive_offset_
  interface`'s own, separate, still-forced-abstention job (XASSET-0008
  SSE, supporting artifact SS6).
- No predictive-language leakage inside `historical_inflation_
  sensitivity`'s and `historical_equity_drawdown_behavior`'s own free-text
  fields specifically (supporting artifact SS11 point 11) -- both sub-
  fields are historically-grounded, backward-looking characterizations
  only, never a forecast.
- Closed schema at every level (envelope, both structural-reference
  shapes, `instrument_specific_economic_characterization` and its three
  sub-fields, `deployability_and_optionality`, `evidence_quality`,
  `cross_asset_handoff`, provenance source, manifest row) -- an explicit
  permitted-key set per level, rejecting any unknown key, learning
  directly from `contender_registry_validator.py`'s own independent-
  review-found MAJOR gap and `etf_classification_validator.py`'s own
  disclosed MINOR-1 finding (supporting artifact SS11 points 2/SS11.1).
- No equity-shaped, ETF-shaped, crypto-shaped, functional-doctrine-
  shaped, or overlap-model-shaped field-name leakage anywhere in the
  document tree (supporting artifact SS11 point 5).
- Deterministic hashing (`canonical_record_hash`) excludes only the five
  seal fields (`sealed_at`, `governing_decision`, `drafting_session_or_
  shard_id`, `content_sha256`, `cohort_manifest_entry`) -- `content_
  sha256` is independently recomputable and must match on every sealed
  record and every manifest row, bidirectionally.

This module is a validator, not a data producer. It never opens a file in
write/append/update mode, never creates a directory, and has zero import
relationship with `allocate.py` or `margin_state.py` in either direction.
It imports `etf_classification_validator` and `functional_doctrine_
validator` for exactly one read-only public function each
(`canonical_record_hash`) to implement the structural-reference hash
pins -- no other cross-module coupling.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from hashlib import sha256
from pathlib import Path

import yaml

import etf_classification_validator as _etf
import functional_doctrine_validator as _fd

AUTHORIZED_POPULATION = frozenset({"GLD", "CASH_LIKE_CAPITAL"})
_GLD_SUBJECT = "GLD"
_CASH_LIKE_SUBJECT = "CASH_LIKE_CAPITAL"

_UNABLE_TO_DETERMINE_VALUE = "unable_to_determine"

# ── deployability_and_optionality (SS4.2) -- both subjects, computed once ──

_DEPLOYABILITY_CATEGORY_VALUES = frozenset({
    "high_optionality_low_friction", "moderate_optionality",
    "low_optionality_or_structurally_constrained", _UNABLE_TO_DETERMINE_VALUE,
})
_DEPLOYABILITY_ALLOWED_KEYS = frozenset({"deployability_category", "rationale", "abstention_reason"})

# ── instrument_specific_economic_characterization (SS4.3) -- GLD only ──────

_COST_TRACKING_CATEGORY_VALUES = frozenset({
    "in_line_with_category", "elevated_vs_category", "favorable_vs_category",
    _UNABLE_TO_DETERMINE_VALUE,
})
_INFLATION_SENSITIVITY_CATEGORY_VALUES = frozenset({
    "historically_positively_associated", "historically_mixed_or_inconsistent",
    "historically_weakly_associated", _UNABLE_TO_DETERMINE_VALUE,
})
_DRAWDOWN_BEHAVIOR_CATEGORY_VALUES = frozenset({
    "historically_uncorrelated_or_negatively_correlated", "historically_mixed",
    "historically_positively_correlated", _UNABLE_TO_DETERMINE_VALUE,
})

_COST_TRACKING_ALLOWED_KEYS = frozenset({"significance_category", "rationale", "abstention_reason"})
_INFLATION_SENSITIVITY_ALLOWED_KEYS = frozenset({"sensitivity_category", "rationale", "abstention_reason"})
_DRAWDOWN_BEHAVIOR_ALLOWED_KEYS = frozenset({
    "behavior_category", "rationale", "abstention_reason", "single_asset_disclosure",
})
_INSTRUMENT_SPECIFIC_SUB_FIELDS = frozenset({
    "cost_and_tracking_economic_significance", "historical_inflation_sensitivity",
    "historical_equity_drawdown_behavior",
})
_INSTRUMENT_SPECIFIC_POPULATED_ALLOWED_KEYS = _INSTRUMENT_SPECIFIC_SUB_FIELDS
_INSTRUMENT_SPECIFIC_NOT_APPLICABLE_ALLOWED_KEYS = frozenset({"not_applicable"})

# ── structural references (SS5) ─────────────────────────────────────────

_STRUCTURAL_REFERENCE_ETF_ALLOWED_KEYS = frozenset({
    "source_instrument_id", "source_schema", "source_file", "referenced_content_sha256",
})
_STRUCTURAL_REFERENCE_FD_ALLOWED_KEYS = frozenset({
    "source_capital_use_type", "source_schema", "source_file", "referenced_content_sha256",
})
_EXPECTED_ETF_SOURCE_INSTRUMENT_ID = "GLD"
_EXPECTED_ETF_SOURCE_SCHEMA = "etf_classification"
_EXPECTED_ETF_SOURCE_FILE = "intelligence/etf_classification/GLD.yaml"
_EXPECTED_FD_SOURCE_CAPITAL_USE_TYPE = "GLD_DEFENSIVE_ROLE"
_EXPECTED_FD_SOURCE_SCHEMA = "functional_doctrine"
_EXPECTED_FD_SOURCE_FILE = "intelligence/functional_doctrine/GLD_DEFENSIVE_ROLE.yaml"

_LEGACY_REFERENCE_ALLOWED_KEYS = _STRUCTURAL_REFERENCE_FD_ALLOWED_KEYS
_LEGACY_REFERENCE_EXPECTED_TYPES = frozenset({"CASH", "RESERVE"})
_LEGACY_REFERENCE_SOURCE_FILES = {
    "CASH": "intelligence/functional_doctrine/CASH.yaml",
    "RESERVE": "intelligence/functional_doctrine/RESERVE.yaml",
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

# ── cross_asset_handoff (SS9) -- exactly four fields, no fifth ─────────────

_CROSS_ASSET_HANDOFF_ALLOWED_KEYS = frozenset({
    "deployability_summary", "instrument_specific_summary",
    "evidence_quality_summary", "uncertainty_summary",
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
    "schema_version", "analytical_subject", "provenance",
    "uncertainty_summary", "evidence_quality_status", "record_status",
    "later_governance_action", "cross_asset_handoff", "abstention_index",
})
_POPULATION_CONDITIONAL_KEYS = frozenset({
    "structural_reference_etf_classification", "structural_reference_functional_doctrine",
    "legacy_structural_references",
})
_SHARED_AXIS_KEYS = frozenset({
    "deployability_and_optionality", "instrument_specific_economic_characterization", "evidence_quality",
})
_ALL_TOP_LEVEL_KEYS = frozenset({
    *_ENVELOPE_ONLY_KEYS, *_POPULATION_CONDITIONAL_KEYS, *_SHARED_AXIS_KEYS, *_SEAL_REQUIRED_KEYS,
})
# structural_reference_etf_classification / structural_reference_
# functional_doctrine / legacy_structural_references are all conditionally
# present -- excluded from the hashable set exactly like every other
# envelope field is included; each participates in hashing when present,
# absent otherwise (data.get(k) naturally returns None when absent).

# ── forbidden leakage: cross-schema field names ─────────────────────────

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
    "functional_role", "hard_constraint_status", "economic_assessment_readiness",
    "liquidity_character", "capital_preservation_character", "freshness_state", "capital_use_type",
})
_OVERLAP_MODEL_FIELD_LEAKAGE = frozenset({
    "dimension_id", "dimension_type", "source_mechanism", "computation_status",
    "evidence_or_source_refs", "output_shape", "uncertainty_or_gap_disclosure",
})
_CROSS_SCHEMA_LEAKAGE_GROUPS = (
    (_EQUITY_FIELD_LEAKAGE, "an equity-classification-shaped field"),
    (_ETF_FIELD_LEAKAGE, "an ETF-classification-shaped axis field"),
    (_CRYPTO_FIELD_LEAKAGE, "a crypto-classification-shaped axis field"),
    (_FUNCTIONAL_DOCTRINE_FIELD_LEAKAGE, "a functional-doctrine-shaped field"),
    (_OVERLAP_MODEL_FIELD_LEAKAGE, "an overlap-model-shaped field"),
)
_ALL_CROSS_SCHEMA_LEAKAGE_KEYS = frozenset().union(*(g for g, _ in _CROSS_SCHEMA_LEAKAGE_GROUPS))

# ── forbidden leakage: numeric fields (SS11 point 6) -- no carve-out ───────

_NUMERIC_LEAKAGE_KEYS = frozenset({
    "expected_return", "hurdle_rate", "price_target", "fair_value",
    "correlation_coefficient", "beta", "target_pct", "target_weight",
    "opportunity_cost_score", "ranking_score", "allocation_pct", "leverage_amount",
})
_FORBIDDEN_KEY_NAMES = frozenset({*_ALL_CROSS_SCHEMA_LEAKAGE_KEYS, *_NUMERIC_LEAKAGE_KEYS})

# Bare numeric-percent-shaped token -- rejected everywhere in free text,
# with NO carve-out of any kind (SS11 point 6's own explicit instruction,
# stricter than every prior framework's own scoped exception).
_NUMERIC_PERCENT_PATTERN = re.compile(r"\d+(?:\.\d+)?\s*%")

_FORBIDDEN_TEXT_PATTERNS = [
    re.compile(p, re.IGNORECASE) for p in (
        r"\bshould\s+be\s+(increased|decreased|raised|lowered|set)\s+to\b",
        r"\brecommend(?:ed|s|ing)?\s+(a\s+)?(target|weight|allocation|position\s+size)\s+of\b",
        r"\bnew\s+target\s+(pct|percent|percentage|range)\b",
        r"\bbuy\s+recommendation\b",
        r"\bsell\s+recommendation\b",
        r"\btrim\s+recommendation\b",
    )
]

# Word-boundary matched so "hold" never flags the noun "holdings", "exit"
# never flags "exiting", "add" never flags "address", and so on
# (recommendation_validator.py's own established design, reused
# unmodified -- this schema has no debt/cash-specific verb list, since it
# is a valuation/economic-characterization schema, not an operational
# capital-use schema like functional-doctrine's).
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

# ── predictive-language leakage (SS11 point 11) -- scoped to exactly two
#    GLD sub-fields' own free text, not the whole document ────────────────

_PREDICTIVE_TERMS = ("forecast", "predict", "expected to", "will likely", "projected")


def _predictive_pattern(term: str) -> re.Pattern:
    if " " in term:
        return re.compile(re.escape(term), re.IGNORECASE)
    return re.compile(rf"\b{re.escape(term)}\w*", re.IGNORECASE)


_PREDICTIVE_PATTERNS = [(t, _predictive_pattern(t)) for t in _PREDICTIVE_TERMS]
_PREDICTIVE_SCOPED_SUB_FIELDS = frozenset({
    "historical_inflation_sensitivity", "historical_equity_drawdown_behavior",
})

# ── CASH-vs-RESERVE distinction leakage (SS11 point 15) -- a materially
#    independent mechanism from the legacy_structural_references hash
#    check (point 8); never a byproduct of it ─────────────────────────────

_DISTINCTION_PATTERNS = [
    re.compile(p, re.IGNORECASE) for p in (
        r"\bCASH\b[^.]{0,120}\b(differ|distinct|different\s+(treatment|purpose|role|function))\b[^.]{0,80}\bRESERVE\b",
        r"\bRESERVE\b[^.]{0,120}\b(differ|distinct|different\s+(treatment|purpose|role|function))\b[^.]{0,80}\bCASH\b",
        r"\bCASH\b[^.]{0,30}\bRESERVE\b[^.]{0,60}\b(differ|distinct|different\s+(treatment|purpose|role|function))\b",
        r"\bRESERVE\b[^.]{0,30}\bCASH\b[^.]{0,60}\b(differ|distinct|different\s+(treatment|purpose|role|function))\b",
        r"\bRESERVE\s+(functions|serves|acts)\s+as\b",
        r"\bCASH\s+is\s+used\s+for\b",
        r"\bRESERVE\s+is\s+(used|intended|held|meant)\s+for\b",
        r"\b(CASH|RESERVE)\s+individually\s+warrants?\b",
        r"\b(CASH|RESERVE)\s+(alone|specifically)\s+(is|represents|serves)\b",
        r"\bthe\s+(reserve|cash)\s+(percentage|pct|weight|target)\s+(suggests|implies|indicates)\b",
    )
]

# ── overlap-model (defensive_offset_interface) non-duplication (SS11
#    point 12) -- rejects a whole-portfolio diversification/correlation
#    claim anywhere in historical_equity_drawdown_behavior's own free
#    text; a separate mechanism from the required single_asset_disclosure
#    presence check. Bounded correction: broadened beyond the original
#    fixed-phrase set to catch equivalent verb forms ("diversifies",
#    "offsets", "hedge") that a hand-crafted record could otherwise use
#    to smuggle the same class of assertion past a narrower list ────────

_PORTFOLIO_DIVERSIFICATION_PATTERNS = [
    re.compile(p, re.IGNORECASE) for p in (
        r"diversification\s+benefit\s+to\s+(the\s+)?(current\s+)?portfolio",
        r"correlat(?:ed|ion)\s+with\s+(the\s+)?(current\s+)?portfolio",
        r"portfolio[-\s]level\s+diversification",
        r"reduces?\s+(the\s+)?portfolio(?:'s)?\s+risk",
        r"hedges?\s+(the\s+)?(current\s+)?portfolio",
        r"portfolio-hq's\s+own\s+(current\s+)?holdings",
        # Broader verb-form coverage, each pairing the concept word with
        # "portfolio" inside a bounded, same-sentence-scale window (a
        # deliberately loose "concept near portfolio" match, not a fixed
        # multi-word phrase) -- catches "diversifies the whole portfolio",
        # "reduces total portfolio drawdown", "offsets equity risk at the
        # portfolio level", "provides a portfolio hedge", and equivalent
        # phrasing the original fixed-phrase list above would miss.
        r"diversif\w*[^.]{0,60}\bportfolio\b",
        r"\bportfolio\b[^.]{0,60}diversif\w*",
        r"\bportfolio\b[^.]{0,60}correlat(?:ed|ion)\w*",
        r"reduc\w*[^.]{0,60}\bportfolio\b[^.]{0,30}\b(risk|drawdown|volatility)\b",
        # Reversed word order of the pattern immediately above -- "the
        # portfolio's risk is reduced by GLD" states the identical claim
        # with "portfolio...risk" preceding "reduc(ed)", which the
        # forward-order pattern alone does not match.
        r"\bportfolio(?:'s)?\b[^.]{0,30}\b(risk|drawdown|volatility)\b[^.]{0,60}reduc\w*",
        r"\bportfolio\b[^.]{0,20}\bhedge\w*\b",
        # Leading `\b` -- without it, this pattern matched "offset" as a
        # substring of an unrelated identifier like the schema's own
        # "defensive_offset_interface" dimension name (a real,
        # legitimate cross-reference that appears in accepted disclaimer
        # language): Python's `\b` is defined by a \w/non-\w transition,
        # and since the underscore before "offset" in that identifier is
        # itself a \w character, there is no such transition there for
        # an unanchored "offsets?" to require -- it matched regardless.
        # An explicit leading `\b` closes that gap; `[a-z]*` (not `\w*`)
        # also keeps any trailing continuation to letters only, so a
        # genuine word-initial "offset_interface" (no separating
        # boundary at all before "offset") still cannot match either.
        r"\boffsets?[a-z]*[^.]{0,60}\bportfolio\b",
    )
]

_REQUIRED_DISCLOSURE_MARKERS = ("single-asset", "single asset")

# Bounded correction (SS11 point 12 defense-in-depth gap, disclosed in
# the retained audit): the original design fully exempted single_asset_
# disclosure from this scan, since its own required job is to name and
# disclaim the portfolio-level boundary using this same vocabulary. That
# exemption was too broad -- a hand-crafted record could bury a real,
# unnegated portfolio-level claim inside single_asset_disclosure and pass
# clean. The corrected mechanism is negation-aware and sentence-scoped,
# not a fixed-character-window heuristic (which would misfire against the
# real sealed record's own disclaimer -- its own negation cue sits well
# beyond a small fixed window from the claim it disclaims): a
# _PORTFOLIO_DIVERSIFICATION_PATTERNS match inside single_asset_
# disclosure is allowed only when a genuine disclaiming-negation phrase
# (a negation word immediately paired with a disclaiming verb -- "does
# not compute", "never establishes", etc., not a bare "not" anywhere in
# the field) appears earlier in the *same sentence*. This is a materially
# different mechanism from rationale's own unconditional block (below),
# never a byproduct of it -- rationale is never expected to discuss
# portfolio-level boundaries at all, disclaiming or otherwise, so it
# keeps the original full-block behavior unchanged.
_DISCLAIMING_NEGATION_PATTERN = re.compile(
    r"\b(?:does|do|did|is|are|will|can)\s+not\s+"
    r"(?:compute|constitute|imply|substitute|establish|determine|represent|assert|claim|find|show|demonstrate|indicate|prove)\w*"
    r"|\bnever\s+"
    r"(?:compute|constitute|impl\w*|substitute|establish\w*|determine\w*|represent\w*|assert\w*|claim\w*|find\w*|show\w*|demonstrate\w*|indicate\w*|prove\w*)"
    r"|\bnone\b[^.;:]{0,20}?\b"
    r"(?:establish\w*|constitute\w*|impl\w*|substitute\w*|determine\w*|represent\w*|assert\w*|claim\w*|find\w*|show\w*|demonstrate\w*|indicate\w*|prove\w*)",
    re.IGNORECASE,
)

# Fourth bounded correction, MINOR half (a legitimate quantifier-negation
# false rejection, disclosed in the retained audit SS12): the negation
# pattern above only recognized "(does/is/...) not VERB" and "never VERB"
# forms -- it did not recognize a bare quantifier negation ("No X
# conclusion is established.", "None of this establishes X..."), an
# ordinary, entirely safe way to phrase the exact same disclaimer. The
# "None ... VERB" form is folded into _DISCLAIMING_NEGATION_PATTERN above
# (it behaves like ordinary negation -- the claim is the object of the
# negated verb, governed by the same per-match veto check below). The
# "No [claim] conclusion/finding/determination/benefit is
# established/drawn/made/..." form is structurally different -- the claim
# sits *between* "No" and the meta-noun ("conclusion", etc.), which is
# itself the subject of "is established", not the claim directly -- so it
# is matched as its own whole-span pattern, and a claim match falling
# entirely within that span is accepted outright, bypassing the veto
# check below (which would otherwise misfire on "conclusion is
# established" immediately following the claim).
_QUANTIFIER_NEGATION_CLAIM_PATTERN = re.compile(
    r"\bno\b[^.;:]{0,80}?\b(?:conclusion|finding|determination|benefit)\b[^.;:]{0,30}?"
    r"\b(?:is|are|was|were)\s+(?:established|drawn|made|supported|reached|claimed|found|identified)\w*",
    re.IGNORECASE,
)

# Second bounded correction (same-sentence, cross-clause negation
# laundering, disclosed in the retained audit SS10): a genuine negation in
# one clause of a sentence was being treated as disclaiming a later,
# independent claim in a *different* clause of the same sentence, joined
# by a comma+conjunction, a semicolon, or a contrastive conjunction (e.g.
# "This does not establish X, and GLD diversifies the whole portfolio.").
# Sentence-scoping alone is too coarse for negation; a disclaiming cue
# must be evaluated per *clause*, not per sentence.
#
# `remains separately governed` (and equivalent phrasing) is accepted as a
# second, independent disclaiming cue alongside the negation-verb pattern
# above -- both are genuine ways to defer a portfolio-level claim to
# defensive_offset_interface without literally saying "does not X".
_DECLARATIVE_DEFERRAL_PATTERN = re.compile(
    r"remains?\s+(?:separately\s+)?"
    r"(?:governed|unmeasured|unresolved|ungoverned|undetermined|unaddressed)\b",
    re.IGNORECASE,
)

# Sixth bounded correction (negation-laundering vulnerability CLASS,
# disclosed in the retained audit SS14): rounds two through five each
# patched one more concrete bypass construction by enumerating more
# clause-boundary punctuation, conjunction words, and finite-verb
# interruptors -- a BLACKLIST architecture ("does anything resembling a
# boundary appear nearby") that an independent review demonstrated
# incomplete at every round (most recently, a bare comma-delimited
# appositive truncating the fourth round's own lookahead window before
# it ever reached the finite predicate that would have exposed the
# bypass). A blacklist of "things that end a clause" can never be proven
# exhaustive against natural-language variation -- each fix closed one
# more specific construction, not the class.
#
# The mechanism below is a WHITELIST instead, evaluated per claim match
# rather than per pre-split "clause" (clause-splitting was itself part
# of the discarded blacklist architecture): a claim match is governed
# only when the text separating it from its governing negation or
# deferral is *purely connective tissue* -- a small closed set of
# function words plus the scan's own two closed vocabularies below (the
# disclaiming-verb-word list, the diversification-concept-noun list).
# Any token outside that closed whitelist disqualifies the span
# immediately, with no enumeration of what that token might be required,
# because ordinary English has no way to state a genuinely different
# subject, predicate, or unrelated claim using only connective tissue --
# a real new clause's own subject or verb is, definitionally, not a
# preposition/article/conjunction/one of these two closed vocabularies.
# This closes the whole demonstrated vulnerability class (every round
# two through five bypass, plus an adversarial matrix of unseen variants
# spanning coordination, punctuation, subject/object order, voice,
# parentheticals, negation position, quantifiers, and clause order --
# retained audit SS14) rather than one more punctuation form.
_DISCLAIMING_VERB_WORDS = (
    r"compute|constitute|imply|substitute|establish|determine|represent|"
    r"assert|claim|find|show|demonstrate|indicate|prove"
)
_DIVERSIFICATION_CONCEPT_NOUNS = (
    r"diversification(?:-benefit)?|correlation|hedge(?:\s+effectiveness)?|"
    r"risk(?:\s+reduction)?|drawdown|volatility"
)
_HARD_BOUNDARY_STOP_PATTERN = re.compile(
    r";|:|--|—"
    r"|\b(?:but|so|nor|yet|however|though|although|while)\b",
    re.IGNORECASE,
)
_SENTENCE_SPLIT_PATTERN = re.compile(r"(?<=[.!?])\s+")


def _split_sentences(text: str) -> list[str]:
    return [s for s in _SENTENCE_SPLIT_PATTERN.split(text) if s]


# The whitelist itself: pure function words plus the fixed noun-phrase
# scaffolding the real sealed disclosure and every accepted allowed-
# language construction actually use to connect a negation/deferral to
# its governed claim (e.g. "for a whole-portfolio diversification-
# benefit or correlation finding specific to Portfolio-HQ's own current
# holdings"). Kept as small as the real record and the governed allowed-
# language matrix actually require, never widened speculatively -- a
# wider whitelist is a wider bypass surface. Note the tokenizer below
# deliberately excludes the hyphen from its word-character class, so a
# hyphenated compound like "whole-portfolio" splits into two separate
# tokens ("whole", "portfolio"), each independently whitelisted, rather
# than needing every hyphenated form spelled out as its own entry.
_CONNECTIVE_WORD_WHITELIST = frozenset({
    "and", "or", "for", "a", "an", "the", "to", "of", "specific",
    "finding", "whole", "benefit", "level", "own", "current", "holdings",
    "hq", "hq's", "effect", "effects", "portfolio",
    # "with" is a literal anchor word inside one of the thirteen fixed
    # _PORTFOLIO_DIVERSIFICATION_PATTERNS phrases itself
    # (correlat(?:ed|ion)\s+with\s+...portfolio) -- any match of that
    # pattern necessarily contains "with" as part of its own matched
    # text, so it must be whitelisted for the internal-purity check to
    # ever accept that pattern's own legitimate matches at all.
    "with",
    # "either" is an inert intensifying adverb/correlative ("...does not
    # establish X either") -- it never itself introduces a new subject or
    # predicate, and combining it with any of the words above cannot
    # construct a coherent independent clause without also including a
    # verb or subject noun, neither of which this whitelist contains.
    "either",
})
_CONNECTIVE_VERB_NOUN_PATTERN = re.compile(
    rf"^(?:{_DISCLAIMING_VERB_WORDS})\w*$|^(?:{_DIVERSIFICATION_CONCEPT_NOUNS})$",
    re.IGNORECASE,
)
_TOKEN_PATTERN = re.compile(r"[A-Za-z][\w']*")
_MAX_CONNECTIVE_SPAN_CHARS = 160


def _is_purely_connective(span: str) -> bool:
    """True only when every word token in `span` is either a member of
    the small closed function-word whitelist or itself one more item
    from the scan's own two closed vocabularies (a disclaiming-verb-word
    or a diversification-concept-noun) -- i.e. the span could only ever
    be inert connective tissue joining a governing cue to the claim it
    governs, never an intervening subject, predicate, or unrelated
    claim. A single disqualifying token anywhere in the span fails the
    whole check."""
    for tok in _TOKEN_PATTERN.findall(span):
        low = tok.lower()
        if low in _CONNECTIVE_WORD_WHITELIST:
            continue
        if _CONNECTIVE_VERB_NOUN_PATTERN.match(low):
            continue
        return False
    return True


def _match_content_is_explained(match_text: str) -> bool:
    """Own-suite regression testing, before push, found that a match's
    impure filler is not always dangerous: "does not establish portfolio
    diversification; it also does not establish portfolio correlation"
    produces one claim match whose own text spans a semicolon and a
    second, independent "it also does not establish" -- genuinely impure
    by `_is_purely_connective`, yet perfectly safe, because the filler IS
    itself a second, complete disclaiming negation, not a bare assertion.
    A match is therefore accepted for further governance consideration
    when it is either purely connective, OR its own text contains a
    genuine `_DISCLAIMING_NEGATION_PATTERN` or `_DECLARATIVE_DEFERRAL_PATTERN`
    sub-match -- evidence the "impurity" is itself another governing
    disclaimer. This does not weaken the check: a match whose filler
    contains no such sub-match (the actual bypass class -- "and GLD
    diversifies the whole portfolio" contains no negation or deferral
    anywhere) is still rejected outright, and a match accepted here still
    must separately pass `_claim_is_governed` against its own genuinely
    external context -- confirmed by adversarial testing that embedding a
    decoy negation/deferral inside an otherwise-impure match's filler,
    while a real unguarded claim survives elsewhere in the same match or
    sentence, does not itself satisfy that downstream check."""
    if _is_purely_connective(match_text):
        return True
    return bool(
        _DISCLAIMING_NEGATION_PATTERN.search(match_text)
        or _DECLARATIVE_DEFERRAL_PATTERN.search(match_text)
    )


def _bounded_trailing_window(sentence: str, start: int, other_claim_starts: list[int]) -> str:
    """The span from `start` up to whichever comes first: an unambiguous
    hard clause boundary (`_HARD_BOUNDARY_STOP_PATTERN`), the bounded
    character cap, or the start of another recognized claim match in the
    same sentence (multiple _PORTFOLIO_DIVERSIFICATION_PATTERNS entries
    can match overlapping/adjacent spans of one real sentence -- stopping
    here prevents one match's own trailing-connective check from
    spilling into text that belongs to a different match)."""
    stop = _HARD_BOUNDARY_STOP_PATTERN.search(sentence, start)
    candidates = [start + _MAX_CONNECTIVE_SPAN_CHARS]
    if stop:
        candidates.append(stop.start())
    for pos in other_claim_starts:
        if pos > start:
            candidates.append(pos)
    return sentence[start:min(candidates)]


def _claim_is_governed(
    sentence: str, match_start: int, match_end: int, other_claim_starts: list[int]
) -> bool:
    """A claim match is governed only when the governing cue applies to
    THAT specific claim, not merely occurs elsewhere in the sentence:
    either (a) a disclaiming negation precedes it with nothing but
    connective tissue between negation and claim, AND nothing but
    connective tissue follows the claim out to a bounded stopping point
    (both directions required -- a preceding negation earlier in the
    sentence must never "shield" an unrelated positive assertion that
    continues past the claim with its own new predicate, which is
    exactly the class of bypass every prior round's own blacklist
    eventually let through); or (b) a declarative-deferral phrase
    follows the claim with nothing but connective tissue between claim
    and deferral."""
    for neg in _DISCLAIMING_NEGATION_PATTERN.finditer(sentence[:match_start]):
        if not _is_purely_connective(sentence[neg.end():match_start]):
            continue
        trailing = _bounded_trailing_window(sentence, match_end, other_claim_starts)
        if _is_purely_connective(trailing):
            return True
    for defr in _DECLARATIVE_DEFERRAL_PATTERN.finditer(sentence[match_end:]):
        if _is_purely_connective(sentence[match_end:match_end + defr.start()]):
            return True
    return False


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
    """SHA-256 of the record's full content (envelope + all axis-
    equivalent fields + structural references + evidence_quality),
    canonical sorted-key JSON, UTF-8 -- excludes every seal field,
    avoiding circular self-hashing. Population-conditional fields
    naturally participate only when present (`data.get(...)` returns
    `None` for an absent key, same as any other absent key)."""
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
            f"closed; only {sorted(allowed)} are permitted (XASSET-0008 supporting artifact SS4/SS5)"
        )


def _scan_forbidden_keys(value: object, path: str, errors: list[str]) -> None:
    """Structural scan: a forbidden key name anywhere in the document
    tree, not just at the top level (SS11 point 5/6)."""
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
                    f"economic-assessment record (XASSET-0008 supporting artifact SS11 points 5/6)"
                )
            _scan_forbidden_keys(v, f"{path}.{key_str}", errors)
    elif isinstance(value, list):
        for i, item in enumerate(value):
            _scan_forbidden_keys(item, f"{path}[{i}]", errors)


def _scan_free_text_strings(value: object, path: str, errors: list[str], *, in_citation: bool = False) -> None:
    """Recursively scan every free-text string value for forbidden
    recommendation-shaped phrases, directive/trading language, chart-
    derived terminology, and any bare numeric-percent-shaped token (no
    carve-out of any kind, SS11 point 6) -- an independent mechanism
    from whatever accepted this string into the document, not a self-
    declared flag. `provenance.sources[].source_identifier`/`.limitation`
    are pure citation strings (never judgment prose) and are exempted
    from the directive-word check only."""
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
                        f"framing (XASSET-0008 SSF, SSL)"
                    )
        for term, pattern in _CHART_PATTERNS:
            if pattern.search(value):
                errors.append(
                    f"{path}: contains chart-derived terminology {term!r} -- no chart evidence "
                    f"of any kind is permitted (XASSET-0008 supporting artifact SS11 point 9)"
                )
        if _NUMERIC_PERCENT_PATTERN.search(value):
            errors.append(
                f"{path}: contains a bare numeric-percent-shaped token -- no numeric field or "
                f"figure of any kind is permitted anywhere in this schema, with no carve-out "
                f"(XASSET-0008 SSG, supporting artifact SS11 point 6)"
            )


def _scan_distinction_leakage(value: object, path: str, errors: list[str]) -> None:
    """SS11 point 15: a dedicated, materially independent free-text scan
    (no shared logic with the legacy_structural_references hash check)
    rejecting any claim that CASH and RESERVE individually warrant
    different treatment. Runs across the whole CASH_LIKE_CAPITAL record,
    not scoped to a single field, since such a claim could appear
    anywhere."""
    if isinstance(value, dict):
        for k, v in value.items():
            _scan_distinction_leakage(v, f"{path}.{k}", errors)
    elif isinstance(value, list):
        for i, item in enumerate(value):
            _scan_distinction_leakage(item, f"{path}[{i}]", errors)
    elif isinstance(value, str):
        for pattern in _DISTINCTION_PATTERNS:
            if pattern.search(value):
                errors.append(
                    f"{path}: contains a claim that CASH and RESERVE individually warrant "
                    f"different treatment, or an equivalent distinct-purpose assertion -- "
                    f"forbidden under any framing (XASSET-0008 SSD.4, supporting artifact SS11 "
                    f"point 15) matching pattern {pattern.pattern!r}"
                )


def _scan_overlap_model_non_duplication(drawdown: dict, errors: list[str]) -> None:
    """SS11 point 12: a dedicated scan confirming a GLD record's
    historical_equity_drawdown_behavior sub-field is never represented as
    a computed portfolio-level correlation or diversification-benefit
    finding -- independent of, and in addition to, the required single_
    asset_disclosure presence check (SSE, supporting artifact SS6).

    `rationale` is scanned unconditionally (any match is rejected, no
    negation carve-out) -- rationale is never expected to discuss
    portfolio-level boundaries at all, disclaiming or otherwise; a
    positive assertion has nowhere else to hide there, since every other
    field on this sub-object is a closed enum, an abstention reason, or
    the disclosure field itself.

    `single_asset_disclosure` is scanned too (bounded correction -- an
    independent review found the original full exemption too broad,
    §11.1's own "self-declared flag is not a substitute for an
    independent scan" lesson applied a second time here).

    Sixth bounded correction (structural redesign closing the whole
    negation-laundering vulnerability CLASS, disclosed in the retained
    audit §14): rounds two through five each patched one more concrete
    bypass construction with an ever-growing BLACKLIST of enumerated
    clause-boundary punctuation, conjunction words, and finite-verb
    interruptors -- and each blacklist was, in turn, demonstrated
    incomplete by the next adversarial construction. This scan now
    checks each claim match directly against a WHITELIST
    (`_claim_is_governed`, `_is_purely_connective`): a match is governed
    only when the specific text separating it from its governing
    negation or deferral is *purely connective tissue* -- a small closed
    set of function words plus the scan's own two closed vocabularies
    (disclaiming-verb-words, diversification-concept-nouns) -- checked in
    BOTH directions for a preceding negation (nothing but connective
    tissue before the claim AND nothing but connective tissue after it,
    out to a bounded stop), so a genuine negation earlier in the sentence
    can never "shield" an unrelated positive assertion that continues
    past the claim with its own new predicate -- the exact class of
    bypass every prior round's own blacklist eventually let through. No
    pre-splitting into "clauses" occurs at all; governance is evaluated
    directly per claim match, per sentence.

    A legitimate quantifier-negation construction ("No portfolio
    correlation conclusion is established.") is recognized as its own
    whole-span pattern (`_QUANTIFIER_NEGATION_CLAIM_PATTERN`) -- a claim
    match falling entirely within that span is accepted outright.

    Sixth bounded correction, second half (own-suite regression found
    before push, disclosed in the retained audit §14): the claim patterns'
    own bounded same-sentence gap (`[^.]{0,60}` between two anchor
    concepts, e.g. "portfolio" ... "diversif...") can, when a match's two
    anchors sit far enough apart, greedily absorb an entire intervening
    unrelated clause -- including its own foreign subject -- into the
    match text itself (e.g. "does not establish portfolio
    diversification, and GLD diversifies the whole portfolio" matches as
    ONE span, "portfolio diversification, and GLD diversifies", with the
    dangerous ", and GLD diversifies" content living *inside* the match,
    invisible to the before/after whitelist check, which only inspects
    text outside a match). Every match is therefore additionally checked
    for internal purity (`_is_purely_connective(m.group())`) before
    governance is even considered: a well-formed claim phrase is always
    composed entirely of whitelisted connective words and the scan's own
    two closed vocabularies (confirmed against the real sealed record and
    every governed allowed-language construction); a match containing any
    other token has necessarily absorbed foreign clause content and is
    rejected outright, without regard to whatever negation or deferral
    might otherwise appear to govern it."""
    rationale = drawdown.get("rationale")
    if isinstance(rationale, str):
        for pattern in _PORTFOLIO_DIVERSIFICATION_PATTERNS:
            if pattern.search(rationale):
                errors.append(
                    f"historical_equity_drawdown_behavior.rationale: asserts a whole-"
                    f"portfolio diversification-benefit or correlation-to-the-current-"
                    f"portfolio claim -- that remains defensive_offset_interface's own, "
                    f"separate, still-forced-abstention job (XASSET-0008 SSE, supporting "
                    f"artifact SS6) matching pattern {pattern.pattern!r}"
                )

    disclosure = drawdown.get("single_asset_disclosure")
    if isinstance(disclosure, str):
        for sentence in _split_sentences(disclosure):
            quantifier_spans = [
                qm.span() for qm in _QUANTIFIER_NEGATION_CLAIM_PATTERN.finditer(sentence)
            ]
            all_matches: list[tuple[re.Pattern, re.Match]] = []
            for pattern in _PORTFOLIO_DIVERSIFICATION_PATTERNS:
                for m in pattern.finditer(sentence):
                    all_matches.append((pattern, m))
            all_starts = sorted(m.start() for _, m in all_matches)
            for pattern, m in all_matches:
                if any(qs <= m.start() and m.end() <= qe for qs, qe in quantifier_spans):
                    continue  # governed by a quantifier-negation construction
                if not _match_content_is_explained(m.group()):
                    # The claim pattern's own bounded same-sentence gap
                    # ([^.]{0,60} between anchor concepts) swallowed a
                    # foreign token -- an unrelated subject/predicate that
                    # does not belong to either closed vocabulary -- into
                    # the match text itself, which the before/after
                    # governance check below never inspects (it only
                    # checks text outside the match). A well-formed claim
                    # match is always either purely connective, or its own
                    # impurity is itself explained by a second genuine
                    # negation/deferral sub-match (`_match_content_is_
                    # explained`); a match that is neither is definitionally
                    # not one coherent, safely-governable claim phrase, and
                    # is rejected outright rather than evaluated for
                    # governance -- exactly the mechanism a construction
                    # like "does not establish portfolio diversification,
                    # and GLD diversifies the whole portfolio" needs, where
                    # the greedy gap otherwise absorbs ", and GLD
                    # diversifies" into one single match spanning both
                    # claims with no negation or deferral of its own.
                    errors.append(
                        f"historical_equity_drawdown_behavior.single_asset_disclosure: "
                        f"asserts a whole-portfolio diversification-benefit or correlation-"
                        f"to-the-current-portfolio claim whose own matched text spans "
                        f"foreign, non-connective content -- not governed, for that specific "
                        f"claim, by a disclaiming negation or declarative deferral -- that "
                        f"remains defensive_offset_interface's own, separate, "
                        f"still-forced-abstention job (XASSET-0008 SSE, supporting artifact "
                        f"SS6) matching pattern {pattern.pattern!r} in sentence {sentence!r}"
                    )
                    continue
                other_claim_starts = [s for s in all_starts if s > m.start()]
                if _claim_is_governed(sentence, m.start(), m.end(), other_claim_starts):
                    continue
                errors.append(
                    f"historical_equity_drawdown_behavior.single_asset_disclosure: "
                    f"asserts a whole-portfolio diversification-benefit or correlation-"
                    f"to-the-current-portfolio claim not governed, for that specific claim, "
                    f"by a disclaiming negation or declarative deferral -- that remains "
                    f"defensive_offset_interface's own, separate, still-forced-abstention "
                    f"job (XASSET-0008 SSE, supporting artifact SS6) matching pattern "
                    f"{pattern.pattern!r} in sentence {sentence!r}"
                )


def _scan_predictive_language(value: dict, sub_field_name: str, errors: list[str]) -> None:
    """SS11 point 11: forward-looking-term scan, scoped to exactly
    historical_inflation_sensitivity's and historical_equity_drawdown_
    behavior's own free text -- both are historically-grounded,
    backward-looking characterizations only, never a forecast."""
    for field_name, field_value in value.items():
        if isinstance(field_value, str):
            for term, pattern in _PREDICTIVE_PATTERNS:
                if pattern.search(field_value):
                    errors.append(
                        f"{sub_field_name}.{field_name}: contains forward-looking term {term!r} "
                        f"-- {sub_field_name} is a historically-grounded characterization only, "
                        f"never a forecast (XASSET-0008 supporting artifact SS11 point 11)"
                    )


# ── deployability_and_optionality (SS4.2) ───────────────────────────────

def _validate_deployability(value: object, errors: list[str]) -> None:
    if not _require_keys(value, "deployability_and_optionality", frozenset({"deployability_category", "rationale"}), errors):
        return
    value = value  # type: dict
    _reject_unknown_keys(value, "deployability_and_optionality", _DEPLOYABILITY_ALLOWED_KEYS, errors)

    category = value.get("deployability_category")
    if category not in _DEPLOYABILITY_CATEGORY_VALUES:
        errors.append(
            f"deployability_and_optionality.deployability_category must be one of "
            f"{sorted(_DEPLOYABILITY_CATEGORY_VALUES)} (XASSET-0008 supporting artifact SS4.2) -- got {category!r}"
        )

    if not _non_empty_str(value.get("rationale")):
        errors.append("deployability_and_optionality.rationale must be a non-empty string")

    abstention_reason = value.get("abstention_reason")
    if category == _UNABLE_TO_DETERMINE_VALUE:
        if not _non_empty_str(abstention_reason):
            errors.append("deployability_and_optionality.abstention_reason is required and non-empty when deployability_category is 'unable_to_determine'")
    elif abstention_reason is not None:
        errors.append("deployability_and_optionality.abstention_reason must be absent unless deployability_category is 'unable_to_determine'")


# ── instrument_specific_economic_characterization (SS4.3) ──────────────

def _validate_cost_tracking(value: object, errors: list[str]) -> None:
    if not _require_keys(value, "instrument_specific_economic_characterization.cost_and_tracking_economic_significance", frozenset({"significance_category", "rationale"}), errors):
        return
    value = value  # type: dict
    _reject_unknown_keys(value, "instrument_specific_economic_characterization.cost_and_tracking_economic_significance", _COST_TRACKING_ALLOWED_KEYS, errors)

    category = value.get("significance_category")
    if category not in _COST_TRACKING_CATEGORY_VALUES:
        errors.append(
            f"cost_and_tracking_economic_significance.significance_category must be one of "
            f"{sorted(_COST_TRACKING_CATEGORY_VALUES)} -- got {category!r}"
        )
    if not _non_empty_str(value.get("rationale")):
        errors.append("cost_and_tracking_economic_significance.rationale must be a non-empty string")

    abstention_reason = value.get("abstention_reason")
    if category == _UNABLE_TO_DETERMINE_VALUE:
        if not _non_empty_str(abstention_reason):
            errors.append("cost_and_tracking_economic_significance.abstention_reason is required when significance_category is 'unable_to_determine'")
    elif abstention_reason is not None:
        errors.append("cost_and_tracking_economic_significance.abstention_reason must be absent unless significance_category is 'unable_to_determine'")


def _validate_inflation_sensitivity(value: object, errors: list[str]) -> None:
    if not _require_keys(value, "instrument_specific_economic_characterization.historical_inflation_sensitivity", frozenset({"sensitivity_category", "rationale"}), errors):
        return
    value = value  # type: dict
    _reject_unknown_keys(value, "instrument_specific_economic_characterization.historical_inflation_sensitivity", _INFLATION_SENSITIVITY_ALLOWED_KEYS, errors)

    category = value.get("sensitivity_category")
    if category not in _INFLATION_SENSITIVITY_CATEGORY_VALUES:
        errors.append(
            f"historical_inflation_sensitivity.sensitivity_category must be one of "
            f"{sorted(_INFLATION_SENSITIVITY_CATEGORY_VALUES)} -- got {category!r}"
        )
    if not _non_empty_str(value.get("rationale")):
        errors.append("historical_inflation_sensitivity.rationale must be a non-empty string")

    abstention_reason = value.get("abstention_reason")
    if category == _UNABLE_TO_DETERMINE_VALUE:
        if not _non_empty_str(abstention_reason):
            errors.append("historical_inflation_sensitivity.abstention_reason is required when sensitivity_category is 'unable_to_determine'")
    elif abstention_reason is not None:
        errors.append("historical_inflation_sensitivity.abstention_reason must be absent unless sensitivity_category is 'unable_to_determine'")

    _scan_predictive_language(value, "historical_inflation_sensitivity", errors)


def _validate_drawdown_behavior(value: object, errors: list[str]) -> None:
    if not _require_keys(value, "instrument_specific_economic_characterization.historical_equity_drawdown_behavior", frozenset({"behavior_category", "rationale", "single_asset_disclosure"}), errors):
        return
    value = value  # type: dict
    _reject_unknown_keys(value, "instrument_specific_economic_characterization.historical_equity_drawdown_behavior", _DRAWDOWN_BEHAVIOR_ALLOWED_KEYS, errors)

    category = value.get("behavior_category")
    if category not in _DRAWDOWN_BEHAVIOR_CATEGORY_VALUES:
        errors.append(
            f"historical_equity_drawdown_behavior.behavior_category must be one of "
            f"{sorted(_DRAWDOWN_BEHAVIOR_CATEGORY_VALUES)} -- got {category!r}"
        )
    if not _non_empty_str(value.get("rationale")):
        errors.append("historical_equity_drawdown_behavior.rationale must be a non-empty string")

    disclosure = value.get("single_asset_disclosure")
    if not _non_empty_str(disclosure):
        errors.append(
            "historical_equity_drawdown_behavior.single_asset_disclosure is required and must be "
            "a non-empty string on every GLD record, stating the finding is single-asset and "
            "historical only, not a computed whole-portfolio diversification-benefit finding "
            "(XASSET-0008 SSE, supporting artifact SS6)"
        )
    elif not any(marker in disclosure.lower() for marker in _REQUIRED_DISCLOSURE_MARKERS):
        errors.append(
            "historical_equity_drawdown_behavior.single_asset_disclosure must explicitly state "
            "the finding is single-asset (XASSET-0008 supporting artifact SS6's mandatory "
            "disclosure requirement)"
        )

    abstention_reason = value.get("abstention_reason")
    if category == _UNABLE_TO_DETERMINE_VALUE:
        if not _non_empty_str(abstention_reason):
            errors.append("historical_equity_drawdown_behavior.abstention_reason is required when behavior_category is 'unable_to_determine'")
    elif abstention_reason is not None:
        errors.append("historical_equity_drawdown_behavior.abstention_reason must be absent unless behavior_category is 'unable_to_determine'")

    _scan_predictive_language(value, "historical_equity_drawdown_behavior", errors)
    _scan_overlap_model_non_duplication(value, errors)


def _validate_instrument_specific(value: object, analytical_subject: object, errors: list[str]) -> None:
    if not isinstance(value, dict):
        errors.append("instrument_specific_economic_characterization must be a mapping")
        return

    if analytical_subject == _CASH_LIKE_SUBJECT:
        _reject_unknown_keys(value, "instrument_specific_economic_characterization", _INSTRUMENT_SPECIFIC_NOT_APPLICABLE_ALLOWED_KEYS, errors)
        if value.get("not_applicable") is not True:
            errors.append(
                "instrument_specific_economic_characterization must be exactly {'not_applicable': "
                "true} on CASH_LIKE_CAPITAL -- a non-instrument analytical family has no compound "
                "instrument-specific axis (XASSET-0008 supporting artifact SS4.3)"
            )
        return

    if analytical_subject == _GLD_SUBJECT:
        if "not_applicable" in value:
            errors.append(
                "instrument_specific_economic_characterization must be a populated compound "
                "object on GLD -- 'not_applicable' is forbidden (XASSET-0008 supporting artifact SS4.3)"
            )
            return
        missing = _INSTRUMENT_SPECIFIC_SUB_FIELDS - value.keys()
        if missing:
            errors.append(f"instrument_specific_economic_characterization missing required sub-field(s): {sorted(missing)}")
        _reject_unknown_keys(value, "instrument_specific_economic_characterization", _INSTRUMENT_SPECIFIC_POPULATED_ALLOWED_KEYS, errors)
        if "cost_and_tracking_economic_significance" in value:
            _validate_cost_tracking(value["cost_and_tracking_economic_significance"], errors)
        if "historical_inflation_sensitivity" in value:
            _validate_inflation_sensitivity(value["historical_inflation_sensitivity"], errors)
        if "historical_equity_drawdown_behavior" in value:
            _validate_drawdown_behavior(value["historical_equity_drawdown_behavior"], errors)


# ── evidence_quality (unchanged shape) ──────────────────────────────────

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


# ── provenance (unchanged shape) ────────────────────────────────────────

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


# ── structural references (SS5) ─────────────────────────────────────────

def _validate_structural_reference_etf(value: object, *, repo_root: Path | None, errors: list[str]) -> None:
    if not _require_keys(value, "structural_reference_etf_classification", _STRUCTURAL_REFERENCE_ETF_ALLOWED_KEYS, errors):
        return
    value = value  # type: dict
    _reject_unknown_keys(value, "structural_reference_etf_classification", _STRUCTURAL_REFERENCE_ETF_ALLOWED_KEYS, errors)

    if value.get("source_instrument_id") != _EXPECTED_ETF_SOURCE_INSTRUMENT_ID:
        errors.append(f"structural_reference_etf_classification.source_instrument_id must be exactly {_EXPECTED_ETF_SOURCE_INSTRUMENT_ID!r} -- got {value.get('source_instrument_id')!r}")
    if value.get("source_schema") != _EXPECTED_ETF_SOURCE_SCHEMA:
        errors.append(f"structural_reference_etf_classification.source_schema must be exactly {_EXPECTED_ETF_SOURCE_SCHEMA!r} -- got {value.get('source_schema')!r}")
    if value.get("source_file") != _EXPECTED_ETF_SOURCE_FILE:
        errors.append(f"structural_reference_etf_classification.source_file must be exactly {_EXPECTED_ETF_SOURCE_FILE!r} -- got {value.get('source_file')!r}")

    recorded_hash = value.get("referenced_content_sha256")
    if not _non_empty_str(recorded_hash):
        errors.append("structural_reference_etf_classification.referenced_content_sha256 must be a non-empty string")
        return
    if repo_root is None:
        return

    gld_path = repo_root / "intelligence" / "etf_classification" / "GLD.yaml"
    if not gld_path.is_file():
        errors.append("structural_reference_etf_classification could not be verified -- intelligence/etf_classification/GLD.yaml does not exist")
        return
    try:
        gld_data = yaml.safe_load(gld_path.read_text())
    except yaml.YAMLError as exc:
        errors.append(f"structural_reference_etf_classification could not be verified -- GLD.yaml is invalid YAML: {exc}")
        return
    if not isinstance(gld_data, dict):
        errors.append("structural_reference_etf_classification could not be verified -- GLD.yaml did not parse to a mapping")
        return

    live_hash = _etf.canonical_record_hash(gld_data)
    if recorded_hash != live_hash:
        errors.append(
            f"structural_reference_etf_classification.referenced_content_sha256 is stale -- "
            f"recorded {recorded_hash!r}, live-recomputed {live_hash!r} against the current "
            f"sealed GLD.yaml (XASSET-0008 supporting artifact SS5)"
        )


def _validate_structural_reference_fd(
    value: object, *, expected_capital_use_type: str, expected_source_file: str,
    field_name: str, repo_root: Path | None, errors: list[str],
) -> None:
    allowed = _STRUCTURAL_REFERENCE_FD_ALLOWED_KEYS if field_name.startswith("structural_reference") else _LEGACY_REFERENCE_ALLOWED_KEYS
    if not _require_keys(value, field_name, allowed, errors):
        return
    value = value  # type: dict
    _reject_unknown_keys(value, field_name, allowed, errors)

    if value.get("source_capital_use_type") != expected_capital_use_type:
        errors.append(f"{field_name}.source_capital_use_type must be exactly {expected_capital_use_type!r} -- got {value.get('source_capital_use_type')!r}")
    if value.get("source_schema") != _EXPECTED_FD_SOURCE_SCHEMA:
        errors.append(f"{field_name}.source_schema must be exactly {_EXPECTED_FD_SOURCE_SCHEMA!r} -- got {value.get('source_schema')!r}")
    if value.get("source_file") != expected_source_file:
        errors.append(f"{field_name}.source_file must be exactly {expected_source_file!r} -- got {value.get('source_file')!r}")

    recorded_hash = value.get("referenced_content_sha256")
    if not _non_empty_str(recorded_hash):
        errors.append(f"{field_name}.referenced_content_sha256 must be a non-empty string")
        return
    if repo_root is None:
        return

    target_path = repo_root / expected_source_file
    if not target_path.is_file():
        errors.append(f"{field_name} could not be verified -- {expected_source_file} does not exist")
        return
    try:
        target_data = yaml.safe_load(target_path.read_text())
    except yaml.YAMLError as exc:
        errors.append(f"{field_name} could not be verified -- {expected_source_file} is invalid YAML: {exc}")
        return
    if not isinstance(target_data, dict):
        errors.append(f"{field_name} could not be verified -- {expected_source_file} did not parse to a mapping")
        return

    live_hash = _fd.canonical_record_hash(target_data)
    if recorded_hash != live_hash:
        errors.append(
            f"{field_name}.referenced_content_sha256 is stale -- recorded {recorded_hash!r}, "
            f"live-recomputed {live_hash!r} against the current sealed {expected_source_file} "
            f"(XASSET-0008 supporting artifact SS5)"
        )


def _validate_legacy_structural_references(value: object, *, repo_root: Path | None, errors: list[str]) -> None:
    if not isinstance(value, list):
        errors.append("legacy_structural_references must be a list")
        return
    if len(value) != 2:
        errors.append(
            f"legacy_structural_references must contain exactly two entries (one CASH, one "
            f"RESERVE) -- got {len(value)} (XASSET-0008 supporting artifact SS5)"
        )

    seen_types: list[str] = []
    for i, entry in enumerate(value):
        label = f"legacy_structural_references[{i}]"
        if not isinstance(entry, dict):
            errors.append(f"{label} must be a mapping")
            continue
        cut = entry.get("source_capital_use_type")
        if cut not in _LEGACY_REFERENCE_EXPECTED_TYPES:
            errors.append(f"{label}.source_capital_use_type must be one of {sorted(_LEGACY_REFERENCE_EXPECTED_TYPES)} -- got {cut!r}")
            continue
        seen_types.append(cut)
        _validate_structural_reference_fd(
            entry,
            expected_capital_use_type=cut,
            expected_source_file=_LEGACY_REFERENCE_SOURCE_FILES[cut],
            field_name=label,
            repo_root=repo_root,
            errors=errors,
        )

    if len(seen_types) != len(set(seen_types)):
        errors.append("legacy_structural_references contains a duplicate source_capital_use_type entry")
    missing_types = _LEGACY_REFERENCE_EXPECTED_TYPES - set(seen_types)
    if missing_types:
        errors.append(f"legacy_structural_references is missing entry/entries for: {sorted(missing_types)}")


# ── abstention_index ─────────────────────────────────────────────────────

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
    every axis/sub-field in this schema unambiguously treats as a genuine
    abstention. Deliberately does NOT treat instrument_specific_economic_
    characterization's own 'not_applicable' marker as an abstention on
    CASH_LIKE_CAPITAL -- that is a structural fact, not an evidence gap."""
    pairs: list[tuple[str, str]] = []

    deploy = data.get("deployability_and_optionality")
    if isinstance(deploy, dict) and deploy.get("deployability_category") == _UNABLE_TO_DETERMINE_VALUE:
        pairs.append(("deployability_and_optionality", "deployability_category"))

    isec = data.get("instrument_specific_economic_characterization")
    if isinstance(isec, dict) and isec.get("not_applicable") is not True:
        sub_field_map = {
            "cost_and_tracking_economic_significance": "significance_category",
            "historical_inflation_sensitivity": "sensitivity_category",
            "historical_equity_drawdown_behavior": "behavior_category",
        }
        for sub_field, category_key in sub_field_map.items():
            sub = isec.get(sub_field)
            if isinstance(sub, dict) and sub.get(category_key) == _UNABLE_TO_DETERMINE_VALUE:
                pairs.append((f"instrument_specific_economic_characterization.{sub_field}", category_key))

    return pairs


def _check_abstention_index_completeness(data: dict, errors: list[str]) -> None:
    """SS9: abstention_index is a mechanical rollup a future cross-asset
    synthesis unit can scan without re-reading every axis -- that
    guarantee requires every genuine abstention to actually appear in it,
    not merely a self-declared list left unreconciled against the axes
    it claims to summarize (the same defect class etf_classification_
    validator.py's own disclosed v1.1 finding names)."""
    actual = _find_abstention_fields(data)
    if not actual:
        return
    index = data.get("abstention_index")
    if not isinstance(index, list):
        return  # already flagged by _validate_abstention_index
    indexed = {(entry.get("axis"), entry.get("field")) for entry in index if isinstance(entry, dict)}
    for axis, field_name in actual:
        if (axis, field_name) not in indexed:
            errors.append(
                f"abstention_index is missing an entry for {axis}.{field_name} -- every genuine "
                f"unable_to_determine abstention must be represented in abstention_index "
                f"(XASSET-0008 supporting artifact SS9), not merely self-declared and left unreconciled"
            )


# ── envelope projection consistency + population-conditional shape ─────

def _validate_envelope_projection_consistency(data: dict, errors: list[str]) -> None:
    """SS9: every cross_asset_handoff field that summarizes an axis is a
    read-only copy, never independently computed -- checked for exact
    consistency against its source. structural_risk_flags does not exist
    in this schema (unlike the ETF/functional-doctrine schemas) -- this
    schema has no hard_constraint_status axis to project."""
    eq = data.get("evidence_quality") or {}
    if isinstance(eq, dict):
        if data.get("uncertainty_summary") != eq.get("thesis_uncertainty_statement"):
            errors.append(
                "uncertainty_summary must exactly equal evidence_quality.thesis_uncertainty_"
                "statement (SS9 read-only-projection rule)"
            )
        if data.get("evidence_quality_status") != eq.get("primary_source_coverage"):
            errors.append(
                "evidence_quality_status must exactly equal evidence_quality."
                "primary_source_coverage (SS9 read-only-projection rule)"
            )

    deploy = data.get("deployability_and_optionality") or {}
    isec = data.get("instrument_specific_economic_characterization")
    handoff = data.get("cross_asset_handoff")
    if not isinstance(handoff, dict):
        errors.append("cross_asset_handoff must be a mapping")
    else:
        _reject_unknown_keys(handoff, "cross_asset_handoff", _CROSS_ASSET_HANDOFF_ALLOWED_KEYS, errors)
        missing = _CROSS_ASSET_HANDOFF_ALLOWED_KEYS - handoff.keys()
        if missing:
            errors.append(f"cross_asset_handoff missing required key(s): {sorted(missing)}")

        if isinstance(deploy, dict) and handoff.get("deployability_summary") != deploy.get("deployability_category"):
            errors.append("cross_asset_handoff.deployability_summary must exactly equal deployability_and_optionality.deployability_category (SS9)")
        if isinstance(eq, dict) and handoff.get("evidence_quality_summary") != eq.get("primary_source_coverage"):
            errors.append("cross_asset_handoff.evidence_quality_summary must exactly equal evidence_quality.primary_source_coverage (SS9)")
        if handoff.get("uncertainty_summary") != data.get("uncertainty_summary"):
            errors.append("cross_asset_handoff.uncertainty_summary must exactly equal the envelope's own uncertainty_summary (SS9)")
        if isec is not None and handoff.get("instrument_specific_summary") != isec:
            errors.append(
                "cross_asset_handoff.instrument_specific_summary must exactly equal "
                "instrument_specific_economic_characterization, copied verbatim (SS9)"
            )

    analytical_subject = data.get("analytical_subject")
    has_etf_ref = "structural_reference_etf_classification" in data
    has_fd_ref = "structural_reference_functional_doctrine" in data
    has_legacy_refs = "legacy_structural_references" in data

    if _non_empty_str(analytical_subject) and analytical_subject == _GLD_SUBJECT:
        if not has_etf_ref:
            errors.append("structural_reference_etf_classification is required when analytical_subject is 'GLD' (XASSET-0008 SSH)")
        if not has_fd_ref:
            errors.append("structural_reference_functional_doctrine is required when analytical_subject is 'GLD' (XASSET-0008 SSH)")
        if has_legacy_refs:
            errors.append("legacy_structural_references is forbidden (rejected as an unknown key) on analytical_subject 'GLD' (XASSET-0008 supporting artifact SS5)")
    elif _non_empty_str(analytical_subject) and analytical_subject == _CASH_LIKE_SUBJECT:
        if not has_legacy_refs:
            errors.append("legacy_structural_references is required when analytical_subject is 'CASH_LIKE_CAPITAL' (XASSET-0008 supporting artifact SS5)")
        if has_etf_ref:
            errors.append("structural_reference_etf_classification is forbidden (rejected as an unknown key) on analytical_subject 'CASH_LIKE_CAPITAL' (XASSET-0008 SSH)")
        if has_fd_ref:
            errors.append("structural_reference_functional_doctrine is forbidden (rejected as an unknown key) on analytical_subject 'CASH_LIKE_CAPITAL' (XASSET-0008 SSH)")


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
            f"record contains unexpected top-level field(s) {sorted(stray)} -- exactly the two "
            f"shared axes plus population-conditional structural references plus envelope/seal "
            f"fields are permitted, no third substantive judgment axis (XASSET-0008 supporting "
            f"artifact SS4.1)"
        )


# ── public API: in-memory record validation ─────────────────────────────

def validate_economic_assessment_data(
    data: object,
    *,
    source: str | None = None,
    authorized_population: frozenset[str] = AUTHORIZED_POPULATION,
    repo_root: Path | None = None,
) -> ValidationResult:
    """Validate an already-parsed economic-assessment mapping. Never
    touches the filesystem except for the live GLD.yaml/GLD_DEFENSIVE_
    ROLE.yaml/CASH.yaml/RESERVE.yaml structural-reference-hash recomputes
    when `repo_root` is supplied."""
    errors: list[str] = []

    if not isinstance(data, dict):
        errors.append(f"root document must be a mapping, got {type(data).__name__}")
        return ValidationResult(valid=False, errors=errors, source=source)

    analytical_subject = data.get("analytical_subject")
    if not _non_empty_str(analytical_subject):
        errors.append("analytical_subject must be a non-empty string")
    elif authorized_population and analytical_subject not in authorized_population:
        errors.append(
            f"analytical_subject {analytical_subject!r} is not in the authorized two-subject "
            f"population {sorted(authorized_population)} (XASSET-0009 SSA.1) -- no CASH or "
            f"RESERVE as a standalone value, no DEBT_REDUCTION, no third value is authorized "
            f"without its own separate schema-amendment decision"
        )

    if not _non_empty_str(data.get("schema_version")):
        errors.append("schema_version must be a non-empty string")

    if "deployability_and_optionality" not in data:
        errors.append("record missing required field: deployability_and_optionality")
    else:
        _validate_deployability(data["deployability_and_optionality"], errors)

    if "instrument_specific_economic_characterization" not in data:
        errors.append("record missing required field: instrument_specific_economic_characterization")
    else:
        _validate_instrument_specific(data["instrument_specific_economic_characterization"], analytical_subject, errors)

    if "evidence_quality" not in data:
        errors.append("record missing required field: evidence_quality")
    else:
        _validate_evidence_quality(data["evidence_quality"], errors)

    if "provenance" not in data:
        errors.append("record missing required field: provenance")
    else:
        _validate_provenance(data["provenance"], errors)

    if "structural_reference_etf_classification" in data:
        _validate_structural_reference_etf(data["structural_reference_etf_classification"], repo_root=repo_root, errors=errors)
    if "structural_reference_functional_doctrine" in data:
        _validate_structural_reference_fd(
            data["structural_reference_functional_doctrine"],
            expected_capital_use_type=_EXPECTED_FD_SOURCE_CAPITAL_USE_TYPE,
            expected_source_file=_EXPECTED_FD_SOURCE_FILE,
            field_name="structural_reference_functional_doctrine",
            repo_root=repo_root,
            errors=errors,
        )
    if "legacy_structural_references" in data:
        _validate_legacy_structural_references(data["legacy_structural_references"], repo_root=repo_root, errors=errors)

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

    label = str(analytical_subject) if _non_empty_str(analytical_subject) else "<record>"
    _scan_forbidden_keys(data, label, errors)
    _scan_free_text_strings(data, label, errors)
    if analytical_subject == _CASH_LIKE_SUBJECT:
        _scan_distinction_leakage(data, label, errors)

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


def validate_economic_assessment_file(
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

    result = validate_economic_assessment_data(
        data, source=source, authorized_population=authorized_population, repo_root=repo_root,
    )

    if isinstance(data, dict) and _non_empty_str(data.get("analytical_subject")):
        expected_stem = data["analytical_subject"]
        if path.stem != expected_stem:
            result.errors.append(
                f"filename stem {path.stem!r} does not match the record's own analytical_subject {expected_stem!r}"
            )
            result.valid = False

    return result


_MANIFEST_FILENAME = "COHORT_MANIFEST.yaml"
_MANIFEST_REQUIRED_ROW_KEYS = frozenset({
    "analytical_subject", "sealed_at", "content_sha256", "schema_version", "governing_decision", "record_path",
})
_MANIFEST_ROW_ALLOWED_KEYS = _MANIFEST_REQUIRED_ROW_KEYS
_MANIFEST_TOP_LEVEL_ALLOWED_KEYS = frozenset({"schema_version", "governing_decision", "cohort"})


def validate_cohort_manifest(
    manifest_data: object,
    records_by_analytical_subject: dict[str, dict],
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

        analytical_subject = row["analytical_subject"]
        if analytical_subject in seen:
            errors.append(f"cohort manifest lists {analytical_subject!r} more than once")
        seen.add(analytical_subject)

        record = records_by_analytical_subject.get(analytical_subject)
        if record is None:
            errors.append(f"cohort[{i}] analytical_subject {analytical_subject!r} has no corresponding sealed record file")
            continue

        expected_hash = canonical_record_hash(record)
        if row["content_sha256"] != expected_hash:
            errors.append(f"cohort[{i}] ({analytical_subject!r}) content_sha256 mismatch -- manifest {row['content_sha256']!r}, recomputed {expected_hash!r}")
        if record.get("content_sha256") != row["content_sha256"]:
            errors.append(f"cohort[{i}] ({analytical_subject!r}) manifest content_sha256 does not match the record's own recorded content_sha256")

    if authorized_population:
        missing_from_manifest = authorized_population - seen
        if missing_from_manifest:
            errors.append(f"cohort manifest is missing authorized analytical_subject(s): {sorted(missing_from_manifest)}")
        extra = seen - authorized_population
        if extra:
            errors.append(f"cohort manifest lists analytical_subject(s) outside the authorized population: {sorted(extra)}")

    orphans = set(records_by_analytical_subject) - seen
    if orphans:
        errors.append(f"sealed record(s) exist with no corresponding cohort manifest entry: {sorted(orphans)}")

    return ValidationResult(valid=not errors, errors=errors, source=_MANIFEST_FILENAME)


def validate_economic_assessment_directory(
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
        validate_economic_assessment_file(p, authorized_population=authorized_population, repo_root=repo_root)
        for p in yaml_paths
    ]

    records_by_analytical_subject: dict[str, dict] = {}
    for p in yaml_paths:
        data, read_errors = _read_yaml(p)
        if not read_errors and isinstance(data, dict) and _non_empty_str(data.get("analytical_subject")):
            records_by_analytical_subject[data["analytical_subject"]] = data

    manifest_path = directory / _MANIFEST_FILENAME
    if manifest_path.is_file():
        manifest_data, read_errors = _read_yaml(manifest_path)
        if read_errors:
            results.append(ValidationResult(valid=False, errors=read_errors, source=str(manifest_path)))
        else:
            results.append(
                validate_cohort_manifest(manifest_data, records_by_analytical_subject, authorized_population=authorized_population)
            )
    elif records_by_analytical_subject:
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
    _result = validate_economic_assessment_directory(
        _repo_root / "intelligence" / "economic_assessment", repo_root=_repo_root,
    )
    if _result.valid:
        print(f"economic_assessment_validator: OK ({_result.record_count} result(s))")
        sys.exit(0)
    else:
        print("economic_assessment_validator: FAILED")
        for _r in _result.results:
            if not _r.valid:
                for _err in _r.errors:
                    print(f"  - [{_r.source}] {_err}")
        sys.exit(1)
