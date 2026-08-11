"""contender_evaluation_validator.py -- closed-schema validator for
intelligence/contender_evaluation/<TICKER>.yaml, authorized by
governance/decisions/CONTENDER-0003-vrt-wmt-contender-competition-pilot-authorization.md.

Freshly authored (CONTENDER-0003 SS D/SS F) -- a new, separate,
non-canonical directory and validator, because classification_validator.py,
valuation_archetype_validator.py, and valuation_evidence_validator.py all
hard-enforce the live 27-name canonical population via
relationship_validator.load_canonical_universe() and must not be weakened
or expanded to admit VRT/WMT (CONTENDER-0003 SS D). Zero import coupling
with allocate.py/margin_state.py in either direction.

Two read-only cross-schema helpers ARE imported, matching this
repository's own established "reuse doctrine by reference, never
redesign" convention (CONTENDER-0003 SS B/SS C):
  - valuation_archetype_validator.canonical_record_hash() -- to
    independently, live-recompute the structural-reference hash pin into
    GEV.yaml/COST.yaml (CONTENDER-0003 SS B: "a hash mismatch is a hard
    validator failure, never trusted from a stored value").
  - valuation_result_validator.governed_role_for() -- to reuse the
    already-transcribed, already-tested VALUATION-0002 SS2 per-family
    governed-role table verbatim, rather than re-transcribing the same
    49-cell matrix a second time and risking a fresh transcription error
    (CONTENDER-0003 SS C.5: "a mechanical lookup only... never a new
    judgment").

Neither import creates any coupling back toward allocate.py/margin_state.py
(independently AST-verified by this module's own test suite), and neither
sibling module is modified by this filing.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from hashlib import sha256
from pathlib import Path

import yaml

SCHEMA_VERSION = "1.0"

# ---------------------------------------------------------------------------
# CONTENDER-0003 SS A / SS D -- hard-coded, closed two-name population and
# its exact comparator mapping. No targets.yaml row exists for either
# ticker to derive a live population from (unlike relationship_validator's
# load_canonical_universe()) -- this is a fixed constant, matching
# etf_classification_validator.py's/crypto_classification_validator.py's
# own hard-coded fixed-population design, not a live-derived roster.
# ---------------------------------------------------------------------------

AUTHORIZED_COMPARATOR_MAP: dict[str, str] = {
    "VRT": "GEV",
    "WMT": "COST",
}
AUTHORIZED_POPULATION = frozenset(AUTHORIZED_COMPARATOR_MAP.keys())

_GOVERNING_DECISION = "CONTENDER-0003"

_ARCHETYPE_LETTERS = frozenset({"A", "B", "C", "D", "E", "F", "G"})
_ARCHETYPE_ABSTENTION = "unable_to_determine_archetype"
_PRIMARY_ARCHETYPE_VALUES = _ARCHETYPE_LETTERS | {_ARCHETYPE_ABSTENTION}
_SECONDARY_ARCHETYPE_VALUES = _ARCHETYPE_LETTERS

_PRIMARY_SOURCE_COVERAGE_VALUES = frozenset({"comprehensive", "partial", "limited", "blocked"})

_SOURCE_TYPE_VALUES = frozenset({"primary", "secondary"})
_ACCESS_STATUS_VALUES = frozenset({
    "directly_inspected", "consulted_via_search_aggregation", "attempted_not_directly_inspected",
})

_FAMILY_IDS = (
    "family_1_asset_based_sotp",
    "family_2_fcff_dcf",
    "family_3_fcfe_dcf",
    "family_4_earnings_fcf_yield",
    "family_5_relative_valuation",
    "family_6_roic_reinvestment",
    "family_7_scenario_probability_weighted",
)

_EVIDENCE_PARITY_FINDING_VALUES = frozenset({
    "comparable_evidence_depth",
    "contender_evidence_gap",
    "comparator_evidence_richer",
    "insufficient_evidence_for_parity_determination",
})
_EVIDENCE_PARITY_ABSTENTION = "insufficient_evidence_for_parity_determination"

_LIFECYCLE_VALUES = frozenset({"sealed"})

_VALUATION_ARCHETYPE_DIR = "intelligence/valuation_archetype"


# ---------------------------------------------------------------------------
# Schema shape -- closed at every nesting level, extra-key rejection
# everywhere (CONTENDER-0003 SS F: "learning directly from
# contender_registry_validator.py's own disclosed MAJOR finding").
# ---------------------------------------------------------------------------

_TOP_LEVEL_REQUIRED = frozenset({
    "schema_version", "contender_symbol", "canonical_comparator_symbol",
    "provenance", "comparator_structural_reference", "archetype_assessment",
    "evidence_quality_assessment", "methodology_applicability_reference",
    "evidence_parity_finding", "abstention_index",
    "lifecycle_status", "sealed_at", "governing_decisions",
    "drafting_session_or_shard_id", "cohort_manifest_entry", "content_sha256",
})
_TOP_LEVEL_ALL = _TOP_LEVEL_REQUIRED

_SEAL_FIELDS = (
    "sealed_at", "governing_decisions", "drafting_session_or_shard_id",
    "content_sha256", "cohort_manifest_entry",
)

_PROVENANCE_ALLOWED_KEYS = frozenset({"sources"})
_SOURCE_REQUIRED_KEYS = frozenset({"source_identifier", "source_type", "as_of_date", "access_status"})
_SOURCE_ALLOWED_KEYS = frozenset({*_SOURCE_REQUIRED_KEYS, "limitation"})

_STRUCTURAL_REFERENCE_KEYS = frozenset({"source_schema", "source_file", "referenced_content_sha256"})
_EXPECTED_STRUCTURAL_SOURCE_SCHEMA = "valuation_archetype"

_ARCHETYPE_ASSESSMENT_KEYS = frozenset({"primary_archetype", "secondary_archetype", "rationale"})

_EVIDENCE_QUALITY_KEYS = frozenset({"primary_source_coverage", "uncertainty_statement"})

_METHODOLOGY_REF_KEYS = frozenset({"archetype", *_FAMILY_IDS})

_EVIDENCE_PARITY_KEYS = frozenset({"finding", "rationale"})

_ABSTENTION_ENTRY_KEYS = frozenset({"field", "value", "reason"})


# ---------------------------------------------------------------------------
# Canonical hashing -- excludes only the seal fields, mirrors every prior
# sealed-cohort validator's identical convention.
# ---------------------------------------------------------------------------

def canonical_record_hash(data: dict) -> str:
    hashable = {k: v for k, v in data.items() if k not in _SEAL_FIELDS}
    canonical = json.dumps(hashable, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return sha256(canonical.encode("utf-8")).hexdigest()


# ---------------------------------------------------------------------------
# Independent free-text scans -- four materially separate mechanisms:
#   1. general prohibited-content scan (policy/chart/directive leakage,
#      reused from valuation_archetype_validator.py's own pattern set)
#   2. numeric-leakage scan (bare digit -- "no carve-out of any kind",
#      CONTENDER-0003 SS E.8 -- plus a written-out magnitude-comparison
#      scan, the specific gap CONTENDER-0003 SS F names as a lesson from
#      instrument_economic_assessment_validator.py's own disclosed
#      MINOR-1 finding on SPY.yaml)
#   3. a dedicated forbidden-promotion-language scan (SS F, 4th bullet)
#   4. a MATERIALLY SEPARATE comparative-investment-superiority scan
#      (SS F, 5th bullet) -- its own distinct pattern list, deliberately
#      not reusing scan 3's patterns, since an add/promote/replace/
#      supersede/displace/score/rank assertion is a structurally
#      different claim from an implied investment-preference claim that
#      never names an action or a score.
# ---------------------------------------------------------------------------

_POLICY_LEAK_PATTERNS = [
    re.compile(p, re.IGNORECASE)
    for p in [
        r"\bconviction\b",
        r"portfolio_role_ref",
        r"target_pct",
        r"targets\.yaml",
        r"holdings\.yaml",
        r"gates\.yaml",
        r"\bnext_gate\b",
        r"\ballow_add\b",
        r"issuer_lookthrough\.yaml",
        r"%\s*of\s+(the\s+)?book",
        r"%\s*of\s+portfolio",
        r"target\s+weight",
        r"destination\s+weight",
        r"primary_disposition",
        r"case_for_review",
        r"maintain_current_weight",
        r"divergence_requires_review",
        r"baseline_assumption_stale",
        r"structural_measurement_gap",
        r"relationship_measurement_required",
    ]
]

_GATE_LEGITIMATE_USE_PATTERNS = [
    re.compile(p, re.IGNORECASE)
    for p in [
        r"technological gate",
        r"gate-all-around",
        r"customer-qualification gate",
        r"qualification gate",
        r"stop-before-drafting gate",
        r"source-readiness gate",
        r"\bci gate\b",
    ]
]


def _gate_word_leak(text: str) -> bool:
    scrubbed = text
    for pat in _GATE_LEGITIMATE_USE_PATTERNS:
        scrubbed = pat.sub("", scrubbed)
    return bool(re.search(r"\bgates?\b", scrubbed, re.IGNORECASE))


_CHART_DOMAIN_PATTERNS = [
    re.compile(p, re.IGNORECASE)
    for p in [
        r"support\s+level", r"resistance\s+level", r"breakout", r"trend\s*line",
        r"moving\s+average", r"\brsi\b", r"\bmacd\b", r"candlestick",
        r"chart\s+pattern", r"technical\s+analysis", r"oversold", r"overbought",
        r"fibonacci", r"volume\s+profile", r"price\s+target",
    ]
]

_DIRECTIVE_WORDS = ("buy", "sell", "add", "hold", "trim", "exit", "wait", "stage")
_DIRECTIVE_PATTERNS = [re.compile(rf"\b{w}\b", re.IGNORECASE) for w in _DIRECTIVE_WORDS]

# "stage" is also legitimate taxonomy vocabulary as a hyphenated compound
# (archetype E is literally "Early-stage / binary-outcome") -- whitelisted
# the same way valuation_archetype_validator.py already does.
_STAGE_LEGITIMATE_USE_PATTERN = re.compile(r"[a-z]+-stage", re.IGNORECASE)


def _prohibited_content_scan(text: str, *, skip_directive: bool = False) -> list[str]:
    findings: list[str] = []
    for pat in _POLICY_LEAK_PATTERNS:
        if pat.search(text):
            findings.append(f"policy-leak:{pat.pattern}")
    for pat in _CHART_DOMAIN_PATTERNS:
        if pat.search(text):
            findings.append(f"chart-domain:{pat.pattern}")
    if not skip_directive:
        stage_scrubbed = _STAGE_LEGITIMATE_USE_PATTERN.sub("", text)
        for pat in _DIRECTIVE_PATTERNS:
            haystack = stage_scrubbed if pat.pattern == r"\bstage\b" else text
            if pat.search(haystack):
                findings.append(f"directive-word:{pat.pattern}")
    if _gate_word_leak(text):
        findings.append("bare-gate-word")
    return findings


# -- numeric leakage: bare digit, no carve-out of any kind (SS E.8) -------

_BARE_DIGIT_PATTERN = re.compile(r"\d")

# Written-out magnitude-comparison words -- the specific gap
# instrument_economic_assessment_validator.py's own disclosed MINOR-1
# finding named ("three times lower", caught by no digit+%-shaped
# pattern at all). Independent of the bare-digit scan: a magnitude claim
# using only words ("grew twice as fast", "revenue doubled") carries no
# digit character whatsoever.
_MAGNITUDE_WORD_PATTERN = re.compile(
    r"\b(times|twice|doubled?|tripled?|quadrupled?|"
    r"threefold|twofold|fourfold|fivefold|\w+-fold|"
    r"halved)\b",
    re.IGNORECASE,
)

# Spelled-out cardinal numbers -- a bounded reviewer-corrected finding
# (a real, shipped "three reported operating segments" violation): the
# magnitude-comparison scan above catches "three times" but not an
# ordinary spelled-out count used as a factual claim. Bounded, closed
# vocabulary (not a general NLP number parser), matching every other
# scan in this module's own design discipline.
_CARDINAL_WORDS = (
    "zero", "one", "two", "three", "four", "five", "six", "seven", "eight",
    "nine", "ten", "dozen", "hundred", "thousand", "million", "billion",
)
_CARDINAL_WORD_PATTERN = re.compile(r"\b(" + "|".join(_CARDINAL_WORDS) + r")\b", re.IGNORECASE)


def _numeric_leakage_scan(text: str) -> list[str]:
    findings: list[str] = []
    if _BARE_DIGIT_PATTERN.search(text):
        findings.append("numeric-leakage:bare-digit")
    if _MAGNITUDE_WORD_PATTERN.search(text):
        findings.append("numeric-leakage:written-out-magnitude-word")
    if _CARDINAL_WORD_PATTERN.search(text):
        findings.append("numeric-leakage:spelled-out-cardinal-number")
    return findings


# -- forbidden-promotion-language scan (SS F, 4th bullet) ------------------
# Broadened per an independent exact-head review's finding that the
# original list caught only literal promote/replace/supersede/displace --
# missing the comparator-directed half of SS G's dual-sided prohibition
# ("remove, demote, or reclassify GEV or COST") and several common
# paraphrases of "add"/"take X's place"/"deserves inclusion". Still a
# bounded, closed pattern set, not a generic classifier.

_PROMOTION_ACTION_PATTERNS = [
    re.compile(p, re.IGNORECASE)
    for p in [
        r"\bpromot(e|es|ed|ing|ion)\b",
        r"\breplac(e|es|ed|ing|ement)\b",
        r"\bsupersed(e|es|ed|ing)\b",
        r"\bdisplac(e|es|ed|ing)\b",
        r"\bremov(e|es|ed|ing|al)\b",
        r"\bdemot(e|es|ed|ing|ion)\b",
        r"\bswap(s|ped|ping)?\b",
        r"\btak(e|es|ing)\b(?:\s+[\w'-]+){0,4}\s+place\b",
        r"\bdeserves?\s+a\s+spot\b",
        r"\bmerits?\s+inclusion\b",
        r"\badd(?:ing|ed|s)?\b(?:\s+[\w'-]+){0,3}\s+to\s+the\s+(?:canonical|portfolio|targets|holdings)\b",
        r"\bfit\s+for\s+the\s+canonical\b",
        r"\bcanonical\s+27\b",
        r"\bcanonical\s+(cohort|equity\s+cohort|roster)\b",
        r"\bshould\s+be\s+added\b",
        # Round-2 additions: an independent delta review found the
        # inclusion/reconsideration/precedence half of the promotion class
        # unguarded ("inclusion should be reconsidered in favor of").
        # The exclude pattern is deliberately SCOPED to require a
        # co-occurring "in favor of" within a bounded gap rather than a
        # bare "exclude" match -- an unscoped bare pattern was found, by
        # direct testing against this record set's own real text, to
        # false-positive on VRT.yaml's legitimate "...explicitly excluded
        # from this assessment's own reasoning" (excluded FROM THE
        # ANALYSIS, not a comparator-inclusion judgment). Scoping to the
        # co-occurring "in favor of" phrase preserves that legitimate use
        # while still catching the actual prohibited construction.
        r"\bexclud(e|es|ed|ing)\b(?:[\s,;:]+[a-z][\w'-]*){0,4}[\s,;:]+\bin\s+favor\s+of\b",
        r"\binclusion\b(?:[\s,;:]+[a-z][\w'-]*){0,4}[\s,;:]+\b(?:in\s+favor\s+of|favors?|is\s+preferred\s+over|preferred\s+over)\b",
        r"\breconsider(?:ed|ing|s)?\b(?:[\s,;:]+[a-z][\w'-]*){0,4}[\s,;:]+\b(?:inclusion|in\s+favor\s+of)\b",
        r"\bshould\s+(?:be|remain)\s+included\b(?:[\s,;:]+[a-z][\w'-]*){0,3}[\s,;:]+\b(?:instead\s+of|over)\b",
        r"\bshould\s+take\s+precedence\s+over\b",
        r"\btakes?\s+precedence\s+over\b",
        r"\bprefer(?:red|s)?\b(?:[\s,;:]+[a-z][\w'-]*){0,4}[\s,;:]+\b(?:over|to)\b",
        # reversed subject/object ("in favor of X, Y's inclusion should be
        # reconsidered")
        r"\bin\s+favor\s+of\b(?:[\s,;:]+[a-z][\w'-]*){0,6}[\s,;:]+\b(?:inclusion|reconsider(?:ed|ing|s)?|exclud(?:e|es|ed|ing))\b",
    ]
]

_SCORE_RANK_KEY_SUBSTRINGS = (
    "score", "rank", "priority_index", "composite", "ranking",
)


def _promotion_language_scan(text: str) -> list[str]:
    findings: list[str] = []
    for pat in _PROMOTION_ACTION_PATTERNS:
        if pat.search(text):
            findings.append(f"promotion-language:{pat.pattern}")
    return findings


# -- comparative-investment-superiority scan (SS F, 5th bullet) --
# a MATERIALLY SEPARATE mechanism from the promotion-language scan above:
# it catches an implied investment-preference or expected-relative-
# performance judgment that never names an action (add/promote/replace)
# or a score/rank. Deliberately a bounded, closed term/phrase list, not a
# generic sentiment classifier (SS F's own explicit instruction).
#
# Broadened per an independent exact-head review's finding that the
# original adjective/noun list and strict-adjacency regex protected
# seven specific phrases rather than the vulnerability class: added
# comparative/superlative modifiers (more/less attractive|compelling|
# appealing, higher/lower-quality, top/best/worst/smarter), a bounded
# 0-3-word intervening-modifier gap (so "the weaker long-term holding"
# still matches despite "long-term" sitting between the adjective and
# the noun), and standalone idioms (top pick, best choice, beat/edge out).
# ---------------------------------------------------------------------------

_COMPARATIVE_SUPERIORITY_NOUNS = (
    "investment", "compounder", "business", "company", "opportunity",
    "choice", "pick", "holding", "allocation", "quality", "thesis", "case",
    "option", "options", "one",
)
_COMPARATIVE_SUPERIORITY_ADJECTIVES = (
    "stronger", "weaker", "superior", "inferior", "better", "worse",
    "preferable", "preferred", "best", "worst", "smarter",
    "more attractive", "less attractive", "more compelling", "less compelling",
    "more appealing", "less appealing", "higher-quality", "lower-quality",
    "top-tier", "top-rated",
    # Round-2 additions: these require a TRAILING NOUN via the same
    # adj-noun template below, so a bare fragment with no noun ("evidence
    # maturity is relatively weaker") stays unmatched and allowed, while a
    # noun-attached form ("relatively weaker holding") is caught -- the
    # explicit allowed/prohibited distinction an independent delta review
    # required (comparative EVIDENCE quality/maturity = allowed;
    # comparative INVESTMENT/PORTFOLIO quality or inclusion judgment =
    # reject).
    "relatively stronger", "relatively weaker", "relatively superior",
    "relatively inferior",
)


def _phrase_to_regex_alternative(phrase: str) -> str:
    return re.escape(phrase).replace(r"\ ", r"\s+")


_COMPARATIVE_SUPERIORITY_ADJ_ALTERNATION = "|".join(
    _phrase_to_regex_alternative(a) for a in _COMPARATIVE_SUPERIORITY_ADJECTIVES
)
_COMPARATIVE_SUPERIORITY_NOUN_ALTERNATION = "|".join(_COMPARATIVE_SUPERIORITY_NOUNS)

_COMPARATIVE_SUPERIORITY_PATTERNS = [
    # comparative/superlative modifier ... (bounded 0-3-word intervening
    # gap, tolerant of light punctuation -- e.g. "the weaker long-term
    # holding" and "the weaker, long-term holding, on balance" both
    # match) ... noun
    re.compile(
        rf"\b(?:{_COMPARATIVE_SUPERIORITY_ADJ_ALTERNATION})\b"
        rf"(?:[\s,;:]+[a-z][\w'-]*){{0,3}}[\s,;:]+\b(?:{_COMPARATIVE_SUPERIORITY_NOUN_ALTERNATION})\b",
        re.IGNORECASE,
    ),
    re.compile(r"\b(superior|inferior|preferable)\s+to\b", re.IGNORECASE),
    re.compile(r"\bbetter\s+positioned\b", re.IGNORECASE),
    re.compile(r"\boutperform(s|ed|ing)?\b", re.IGNORECASE),
    re.compile(r"\bunderperform(s|ed|ing)?\b", re.IGNORECASE),
    re.compile(r"\bshould\s+(outperform|underperform|beat)\b", re.IGNORECASE),
    re.compile(r"\bbeat(s|ing)?\b", re.IGNORECASE),
    re.compile(r"\bedge(s|d)?\s+out\b", re.IGNORECASE),
    re.compile(r"\btop\s+pick\b", re.IGNORECASE),
    re.compile(r"\bbest\s+choice\b", re.IGNORECASE),
    # Round-2 addition: catches "looks/appears/seems weaker on a relative
    # basis"/"appears stronger relative to" -- a verb + comparative
    # adjective + an explicit relative-comparison suffix marker, distinct
    # from the adj-noun pattern above (this construction has no trailing
    # noun at all). A bounded 0-2-word gap between the verb and the
    # adjective, and a bounded 0-4-word gap between the adjective and the
    # relative-suffix marker, keep this tolerant of short intervening
    # modifiers without becoming unbounded.
    re.compile(
        rf"\b(?:looks?|appears?|seems?)\b(?:[\s,;:]+[a-z][\w'-]*){{0,2}}[\s,;:]+"
        rf"\b(?:{_COMPARATIVE_SUPERIORITY_ADJ_ALTERNATION})\b"
        rf"(?:[\s,;:]+[a-z][\w'-]*){{0,4}}[\s,;:]+"
        rf"\b(?:relative\s+to|on\s+a\s+relative\s+basis|than)\b",
        re.IGNORECASE,
    ),
]


def _comparative_superiority_scan(text: str) -> list[str]:
    findings: list[str] = []
    for pat in _COMPARATIVE_SUPERIORITY_PATTERNS:
        if pat.search(text):
            findings.append(f"comparative-superiority:{pat.pattern}")
    return findings


def _scan_free_text(
    value: object, field_name: str, errors: list[str], *,
    include_numeric: bool = True, include_comparative_superiority: bool = False,
    is_citation_field: bool = False,
) -> None:
    """is_citation_field=True applies the citation-field exemption pattern
    already established elsewhere in this repository (e.g.
    functional_doctrine_validator.py's _CITATION_FIELD_NAMES): the
    directive-word scan is skipped (a legitimate path/citation string
    should never be penalized for incidentally containing a bare
    "add"/"hold"-shaped word), and the numeric-leakage scan is skipped
    for source_identifier specifically, since a real repository path
    legitimately and unavoidably contains digits (e.g. a decision ID
    like "PI-0019"). Every other scan -- policy-leak, chart-domain,
    promotion-language, comparative-superiority -- still applies in
    full, with no exemption, matching an independent exact-head review's
    explicit finding that these fields must not be left wholly unguarded."""
    if value is None:
        return
    texts: list[str]
    if isinstance(value, str):
        texts = [value]
    elif isinstance(value, list):
        texts = [v for v in value if isinstance(v, str)]
    else:
        return
    for text in texts:
        for finding in _prohibited_content_scan(text, skip_directive=is_citation_field):
            errors.append(f"{field_name} contains prohibited content ({finding})")
        for finding in _promotion_language_scan(text):
            errors.append(f"{field_name} contains prohibited content ({finding})")
        if include_numeric:
            for finding in _numeric_leakage_scan(text):
                errors.append(f"{field_name} contains prohibited content ({finding})")
        if include_comparative_superiority:
            for finding in _comparative_superiority_scan(text):
                errors.append(f"{field_name} contains prohibited content ({finding})")


# ---------------------------------------------------------------------------
# Small shared helpers
# ---------------------------------------------------------------------------

def _reject_unknown_keys(value: dict, field_name: str, allowed: frozenset[str], errors: list[str]) -> None:
    extra = set(value.keys()) - allowed
    if extra:
        errors.append(f"{field_name} has unrecognized key(s): {sorted(extra)}")


def _non_empty_str(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _scan_key_names_recursive(value: object, path: str, errors: list[str]) -> None:
    """Defense-in-depth: an explicit, named scan for score/rank/composite-
    shaped key names anywhere in the document tree, distinct from (and in
    addition to) closed-schema extra-key rejection at every level (SS F,
    4th bullet's own explicit "any composite-score- or ranking-shaped key
    name" requirement)."""
    if isinstance(value, dict):
        for k, v in value.items():
            lowered = str(k).lower()
            for substring in _SCORE_RANK_KEY_SUBSTRINGS:
                if substring in lowered:
                    errors.append(f"{path}.{k} is a forbidden score/rank/composite-shaped key name")
            _scan_key_names_recursive(v, f"{path}.{k}", errors)
    elif isinstance(value, list):
        for i, item in enumerate(value):
            _scan_key_names_recursive(item, f"{path}[{i}]", errors)


# ---------------------------------------------------------------------------
# Sub-object validators
# ---------------------------------------------------------------------------

def _validate_provenance(value: object, errors: list[str]) -> None:
    if not isinstance(value, dict):
        errors.append("provenance must be a mapping")
        return
    missing = _PROVENANCE_ALLOWED_KEYS - value.keys()
    if missing:
        errors.append(f"provenance missing key(s): {sorted(missing)}")
        return
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
        missing_src = _SOURCE_REQUIRED_KEYS - src.keys()
        if missing_src:
            errors.append(f"{label} missing key(s): {sorted(missing_src)}")
        _reject_unknown_keys(src, label, _SOURCE_ALLOWED_KEYS, errors)
        if not _non_empty_str(src.get("source_identifier")):
            errors.append(f"{label}.source_identifier must be a non-empty string")
        else:
            # Citation/path field -- policy-leak/chart-domain/promotion-
            # language/comparative-superiority scans apply in full;
            # directive-word and numeric-leakage are exempted, since a
            # real repository path legitimately and unavoidably contains
            # digits (e.g. a decision ID like "PI-0019") and incidental
            # directive-shaped substrings (SS F, an independent review's
            # own MAJOR-2 finding).
            _scan_free_text(
                src["source_identifier"], f"{label}.source_identifier", errors,
                include_numeric=False, include_comparative_superiority=True,
                is_citation_field=True,
            )
        if src.get("source_type") not in _SOURCE_TYPE_VALUES:
            errors.append(f"{label}.source_type invalid: {src.get('source_type')!r}")
        if not _non_empty_str(src.get("as_of_date")):
            errors.append(f"{label}.as_of_date must be a non-empty string")
        if src.get("access_status") not in _ACCESS_STATUS_VALUES:
            errors.append(f"{label}.access_status invalid: {src.get('access_status')!r}")
        if "limitation" in src:
            if not _non_empty_str(src.get("limitation")):
                errors.append(f"{label}.limitation must be a non-empty string when present")
            else:
                # A genuinely narrative field (a short prose note, not a
                # path) -- numeric leakage applies with no carve-out,
                # matching every other rationale-shaped field; only the
                # directive-word scan is exempted, per the same citation-
                # field precedent applied to source_identifier above.
                _scan_free_text(
                    src["limitation"], f"{label}.limitation", errors,
                    include_numeric=True, include_comparative_superiority=True,
                    is_citation_field=True,
                )


def _validate_comparator_structural_reference(
    value: object, contender_symbol: str | None, errors: list[str], *, repo_root: Path | None,
) -> None:
    if not isinstance(value, dict):
        errors.append("comparator_structural_reference must be a mapping")
        return
    missing = _STRUCTURAL_REFERENCE_KEYS - value.keys()
    if missing:
        errors.append(f"comparator_structural_reference missing key(s): {sorted(missing)}")
    _reject_unknown_keys(value, "comparator_structural_reference", _STRUCTURAL_REFERENCE_KEYS, errors)

    if value.get("source_schema") != _EXPECTED_STRUCTURAL_SOURCE_SCHEMA:
        errors.append(
            f"comparator_structural_reference.source_schema must be "
            f"{_EXPECTED_STRUCTURAL_SOURCE_SCHEMA!r}, got {value.get('source_schema')!r}"
        )

    expected_comparator = AUTHORIZED_COMPARATOR_MAP.get(contender_symbol) if contender_symbol else None
    expected_file = (
        f"{_VALUATION_ARCHETYPE_DIR}/{expected_comparator}.yaml" if expected_comparator else None
    )
    source_file = value.get("source_file")
    if expected_file is not None and source_file != expected_file:
        errors.append(
            f"comparator_structural_reference.source_file must be {expected_file!r} "
            f"(the authorized comparator for {contender_symbol!r} is {expected_comparator!r}), "
            f"got {source_file!r}"
        )
    elif expected_file is None and not _non_empty_str(source_file):
        errors.append("comparator_structural_reference.source_file must be a non-empty string")

    recorded_hash = value.get("referenced_content_sha256")
    if not _non_empty_str(recorded_hash):
        errors.append("comparator_structural_reference.referenced_content_sha256 must be a non-empty string")
        return
    if repo_root is None or expected_comparator is None:
        return

    comparator_path = repo_root / _VALUATION_ARCHETYPE_DIR / f"{expected_comparator}.yaml"
    if not comparator_path.is_file():
        errors.append(
            f"comparator_structural_reference could not be verified -- "
            f"{comparator_path} does not exist"
        )
        return
    try:
        comparator_data = yaml.safe_load(comparator_path.read_text(encoding="utf-8"))
    except (yaml.YAMLError, OSError) as exc:
        errors.append(f"comparator_structural_reference could not be verified -- {exc}")
        return
    if not isinstance(comparator_data, dict):
        errors.append("comparator_structural_reference could not be verified -- comparator record did not parse to a mapping")
        return

    # Local import avoids a module-level dependency on valuation_archetype_
    # validator.py existing at import time for callers that only need the
    # schema shape (mirrors economic_assessment_validator.py's own pattern
    # for cross-schema structural-reference verification).
    from valuation_archetype_validator import canonical_record_hash as _archetype_hash

    live_hash = _archetype_hash(comparator_data)
    if recorded_hash != live_hash:
        errors.append(
            f"comparator_structural_reference.referenced_content_sha256 is stale -- "
            f"recorded {recorded_hash!r}, live-recomputed {live_hash!r} against the current "
            f"sealed {expected_comparator}.yaml (CONTENDER-0003 SS B: never trusted from a "
            f"stored value)"
        )


def _validate_archetype_assessment(data: dict, errors: list[str]) -> None:
    value = data.get("archetype_assessment")
    if not isinstance(value, dict):
        errors.append("archetype_assessment must be a mapping")
        return
    missing = _ARCHETYPE_ASSESSMENT_KEYS - value.keys()
    if missing:
        errors.append(f"archetype_assessment missing key(s): {sorted(missing)}")
        return
    _reject_unknown_keys(value, "archetype_assessment", _ARCHETYPE_ASSESSMENT_KEYS, errors)

    primary = value.get("primary_archetype")
    if primary not in _PRIMARY_ARCHETYPE_VALUES:
        errors.append(f"archetype_assessment.primary_archetype invalid: {primary!r}")

    secondary = value.get("secondary_archetype")
    if secondary is not None:
        if secondary not in _SECONDARY_ARCHETYPE_VALUES:
            errors.append(f"archetype_assessment.secondary_archetype invalid: {secondary!r}")
        elif secondary == primary:
            errors.append("archetype_assessment.secondary_archetype must not equal primary_archetype")
        if primary == _ARCHETYPE_ABSTENTION:
            errors.append(
                "archetype_assessment.secondary_archetype must be null when "
                "primary_archetype is the abstention value"
            )

    if not _non_empty_str(value.get("rationale")):
        errors.append("archetype_assessment.rationale must be a non-empty string")
    else:
        _scan_free_text(
            value["rationale"], "archetype_assessment.rationale", errors,
            include_comparative_superiority=True,
        )


def _validate_evidence_quality_assessment(data: dict, errors: list[str]) -> None:
    value = data.get("evidence_quality_assessment")
    if not isinstance(value, dict):
        errors.append("evidence_quality_assessment must be a mapping")
        return
    missing = _EVIDENCE_QUALITY_KEYS - value.keys()
    if missing:
        errors.append(f"evidence_quality_assessment missing key(s): {sorted(missing)}")
        return
    _reject_unknown_keys(value, "evidence_quality_assessment", _EVIDENCE_QUALITY_KEYS, errors)
    cov = value.get("primary_source_coverage")
    if cov not in _PRIMARY_SOURCE_COVERAGE_VALUES:
        errors.append(f"evidence_quality_assessment.primary_source_coverage invalid: {cov!r}")
    if not _non_empty_str(value.get("uncertainty_statement")):
        errors.append("evidence_quality_assessment.uncertainty_statement must be a non-empty string")
    else:
        _scan_free_text(
            value["uncertainty_statement"], "evidence_quality_assessment.uncertainty_statement", errors,
        )


def _validate_methodology_applicability_reference(data: dict, errors: list[str]) -> None:
    """SS C.5 / SS E.5 -- a read-only mechanical lookup against VALUATION-
    0002 SS2's own already-transcribed table (reused via
    valuation_result_validator.governed_role_for(), never re-transcribed
    here). Required (populated, matching the live table) whenever
    primary_archetype is determined; must be null when primary_archetype
    is the abstention value -- a genuine structural dependency (the
    lookup key does not exist), not a forced cascade of an unrelated
    axis (SS C.3's non-cascading rule governs unrelated fields, not this
    one)."""
    archetype_assessment = data.get("archetype_assessment")
    primary = archetype_assessment.get("primary_archetype") if isinstance(archetype_assessment, dict) else None

    value = data.get("methodology_applicability_reference")

    if primary == _ARCHETYPE_ABSTENTION:
        if value is not None:
            errors.append(
                "methodology_applicability_reference must be null when "
                "archetype_assessment.primary_archetype is the abstention value"
            )
        return

    if not isinstance(value, dict):
        errors.append("methodology_applicability_reference must be a mapping (or null on archetype abstention)")
        return
    missing = _METHODOLOGY_REF_KEYS - value.keys()
    if missing:
        errors.append(f"methodology_applicability_reference missing key(s): {sorted(missing)}")
        return
    _reject_unknown_keys(value, "methodology_applicability_reference", _METHODOLOGY_REF_KEYS, errors)

    if value.get("archetype") != primary:
        errors.append(
            f"methodology_applicability_reference.archetype must equal "
            f"archetype_assessment.primary_archetype ({primary!r}), got {value.get('archetype')!r}"
        )
        return

    if primary not in _ARCHETYPE_LETTERS:
        return  # already flagged by _validate_archetype_assessment

    # Local import -- see comment in _validate_comparator_structural_reference.
    from valuation_result_validator import governed_role_for

    for family_id in _FAMILY_IDS:
        expected_role = governed_role_for(family_id, primary)
        actual_role = value.get(family_id)
        if actual_role != expected_role:
            errors.append(
                f"methodology_applicability_reference.{family_id} must be "
                f"{expected_role!r} (VALUATION-0002 SS2's own governed-role table for "
                f"archetype {primary!r}), got {actual_role!r}"
            )


def _validate_evidence_parity_finding(data: dict, errors: list[str]) -> None:
    value = data.get("evidence_parity_finding")
    if not isinstance(value, dict):
        errors.append("evidence_parity_finding must be a mapping")
        return
    missing = _EVIDENCE_PARITY_KEYS - value.keys()
    if missing:
        errors.append(f"evidence_parity_finding missing key(s): {sorted(missing)}")
        return
    _reject_unknown_keys(value, "evidence_parity_finding", _EVIDENCE_PARITY_KEYS, errors)

    finding = value.get("finding")
    if finding not in _EVIDENCE_PARITY_FINDING_VALUES:
        errors.append(f"evidence_parity_finding.finding invalid: {finding!r}")

    if not _non_empty_str(value.get("rationale")):
        errors.append("evidence_parity_finding.rationale must be a non-empty string")
    else:
        _scan_free_text(
            value["rationale"], "evidence_parity_finding.rationale", errors,
            include_comparative_superiority=True,
        )


def _find_abstention_fields(data: dict) -> list[tuple[str, str, str]]:
    """(field_path, field_name, value) triples where a field is set to its
    own closed-vocabulary abstention value -- archetype_assessment.
    primary_archetype == 'unable_to_determine_archetype', or
    evidence_parity_finding.finding == 'insufficient_evidence_for_parity_
    determination'. Each is an independent, non-cascading abstention (SS
    C.3): the two fields are not forced to abstain together."""
    pairs: list[tuple[str, str, str]] = []

    archetype_assessment = data.get("archetype_assessment")
    if isinstance(archetype_assessment, dict) and archetype_assessment.get("primary_archetype") == _ARCHETYPE_ABSTENTION:
        pairs.append(("archetype_assessment", "primary_archetype", _ARCHETYPE_ABSTENTION))

    evidence_parity = data.get("evidence_parity_finding")
    if isinstance(evidence_parity, dict) and evidence_parity.get("finding") == _EVIDENCE_PARITY_ABSTENTION:
        pairs.append(("evidence_parity_finding", "finding", _EVIDENCE_PARITY_ABSTENTION))

    return pairs


def _validate_abstention_index(data: dict, errors: list[str]) -> None:
    value = data.get("abstention_index")
    if not isinstance(value, list):
        errors.append("abstention_index must be a list")
        return
    for i, entry in enumerate(value):
        label = f"abstention_index[{i}]"
        if not isinstance(entry, dict):
            errors.append(f"{label} must be a mapping")
            continue
        missing = _ABSTENTION_ENTRY_KEYS - entry.keys()
        if missing:
            errors.append(f"{label} missing key(s): {sorted(missing)}")
            continue
        _reject_unknown_keys(entry, label, _ABSTENTION_ENTRY_KEYS, errors)
        for k in ("field", "value", "reason"):
            if not _non_empty_str(entry.get(k)):
                errors.append(f"{label}.{k} must be a non-empty string")
        if _non_empty_str(entry.get("reason")):
            _scan_free_text(entry["reason"], f"{label}.reason", errors)

    # Bidirectional reconciliation -- every genuine abstention actually
    # present must appear in the index, and the index must contain no
    # entry for a field that is not genuinely abstained (SS F: "the
    # index is a mechanical rollup", matching etf_classification_
    # validator.py's own disclosed v1.1 lesson on self-declared-flag-
    # without-independent-reconciliation).
    actual = _find_abstention_fields(data)
    actual_fields = {field_name for _, field_name, _ in actual}
    indexed_fields = {entry.get("field") for entry in value if isinstance(entry, dict)}
    for _, field_name, abstained_value in actual:
        if field_name not in indexed_fields:
            errors.append(
                f"abstention_index is missing an entry for field {field_name!r} "
                f"(value {abstained_value!r})"
            )
    for entry in value:
        if not isinstance(entry, dict):
            continue
        entry_field = entry.get("field")
        if entry_field is not None and entry_field not in actual_fields:
            errors.append(
                f"abstention_index has an entry for field {entry_field!r} that is not "
                f"genuinely abstained in the record"
            )


# ---------------------------------------------------------------------------
# Top-level record validation
# ---------------------------------------------------------------------------

@dataclass
class ValidationResult:
    valid: bool
    errors: list[str] = field(default_factory=list)
    source: str | None = None


@dataclass
class DirectoryValidationResult:
    valid: bool
    results: list[ValidationResult] = field(default_factory=list)

    @property
    def record_count(self) -> int:
        return len(self.results)


def validate_contender_evaluation_data(
    data: object, expected_ticker: str | None = None, *, repo_root: Path | None = None,
) -> list[str]:
    errors: list[str] = []
    if not isinstance(data, dict):
        return ["record must be a mapping"]

    missing = _TOP_LEVEL_REQUIRED - data.keys()
    if missing:
        errors.append(f"missing top-level key(s): {sorted(missing)}")
    _reject_unknown_keys(data, "<record>", _TOP_LEVEL_ALL, errors)
    _scan_key_names_recursive(data, "<record>", errors)

    if data.get("schema_version") != SCHEMA_VERSION:
        errors.append(f"schema_version must be {SCHEMA_VERSION!r}, got {data.get('schema_version')!r}")

    contender_symbol = data.get("contender_symbol")
    if not _non_empty_str(contender_symbol):
        errors.append("contender_symbol must be a non-empty string")
        contender_symbol = None
    elif contender_symbol not in AUTHORIZED_POPULATION:
        errors.append(
            f"contender_symbol {contender_symbol!r} is not in the CONTENDER-0003-authorized "
            f"population {sorted(AUTHORIZED_POPULATION)}"
        )
        contender_symbol = None
    elif expected_ticker is not None and contender_symbol != expected_ticker:
        errors.append(f"contender_symbol {contender_symbol!r} does not match filename-derived {expected_ticker!r}")

    canonical_comparator_symbol = data.get("canonical_comparator_symbol")
    expected_comparator = AUTHORIZED_COMPARATOR_MAP.get(contender_symbol) if contender_symbol else None
    if not _non_empty_str(canonical_comparator_symbol):
        errors.append("canonical_comparator_symbol must be a non-empty string")
    elif expected_comparator is not None and canonical_comparator_symbol != expected_comparator:
        errors.append(
            f"canonical_comparator_symbol must be {expected_comparator!r} for contender "
            f"{contender_symbol!r} (CONTENDER-0003 SS A's fixed comparator map), got "
            f"{canonical_comparator_symbol!r}"
        )

    _validate_provenance(data.get("provenance"), errors)
    _validate_comparator_structural_reference(
        data.get("comparator_structural_reference"), contender_symbol, errors, repo_root=repo_root,
    )
    _validate_archetype_assessment(data, errors)
    _validate_evidence_quality_assessment(data, errors)
    _validate_methodology_applicability_reference(data, errors)
    _validate_evidence_parity_finding(data, errors)
    _validate_abstention_index(data, errors)

    if data.get("lifecycle_status") not in _LIFECYCLE_VALUES:
        errors.append(f"lifecycle_status invalid: {data.get('lifecycle_status')!r}")
    if not _non_empty_str(data.get("sealed_at")):
        errors.append("sealed_at must be a non-empty string")

    governing_decisions = data.get("governing_decisions")
    if governing_decisions != [_GOVERNING_DECISION]:
        errors.append(
            f"governing_decisions must be [{_GOVERNING_DECISION!r}], got {governing_decisions!r}"
        )
    if not _non_empty_str(data.get("drafting_session_or_shard_id")):
        errors.append("drafting_session_or_shard_id must be a non-empty string")
    if not _non_empty_str(data.get("cohort_manifest_entry")):
        errors.append("cohort_manifest_entry must be a non-empty string")

    recorded_hash = data.get("content_sha256")
    if not _non_empty_str(recorded_hash):
        errors.append("content_sha256 must be a non-empty string")
    elif not errors:
        expected_hash = canonical_record_hash(data)
        if recorded_hash != expected_hash:
            errors.append(
                f"content_sha256 does not reproduce -- recorded {recorded_hash!r}, "
                f"recomputed {expected_hash!r}"
            )

    return errors


def _read_yaml(path: Path) -> tuple[object, list[str]]:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        return None, [f"could not read file: {exc}"]
    try:
        return yaml.safe_load(text), []
    except yaml.YAMLError as exc:
        return None, [f"YAML parse error: {exc}"]


def validate_contender_evaluation_file(path: Path, *, repo_root: Path | None = None) -> ValidationResult:
    expected_ticker = path.stem
    data, errors = _read_yaml(path)
    if errors:
        return ValidationResult(valid=False, errors=errors, source=str(path))
    errors = validate_contender_evaluation_data(data, expected_ticker=expected_ticker, repo_root=repo_root)
    return ValidationResult(valid=not errors, errors=errors, source=str(path))


# ---------------------------------------------------------------------------
# Cohort manifest validation
# ---------------------------------------------------------------------------

_MANIFEST_ROW_KEYS = frozenset({
    "contender_symbol", "canonical_comparator_symbol", "shard_id", "sealed_at",
    "content_sha256", "schema_version", "governing_decision", "record_path",
})
_MANIFEST_TOP_KEYS = frozenset({"schema_version", "governing_decision", "cohort"})


def validate_cohort_manifest(manifest_path: Path, records_dir: Path) -> ValidationResult:
    errors: list[str] = []
    data, read_errors = _read_yaml(manifest_path)
    if read_errors:
        return ValidationResult(valid=False, errors=read_errors, source=str(manifest_path))
    if not isinstance(data, dict):
        return ValidationResult(valid=False, errors=["manifest must be a mapping"], source=str(manifest_path))

    _reject_unknown_keys(data, "<manifest>", _MANIFEST_TOP_KEYS, errors)
    if data.get("schema_version") != SCHEMA_VERSION:
        errors.append(f"manifest schema_version must be {SCHEMA_VERSION!r}")
    if data.get("governing_decision") != _GOVERNING_DECISION:
        errors.append(f"manifest governing_decision must be {_GOVERNING_DECISION!r}")

    cohort = data.get("cohort")
    if not isinstance(cohort, list):
        errors.append("manifest cohort must be a list")
        return ValidationResult(valid=not errors, errors=errors, source=str(manifest_path))

    seen_tickers: set[str] = set()
    for i, row in enumerate(cohort):
        if not isinstance(row, dict):
            errors.append(f"cohort[{i}] must be a mapping")
            continue
        _reject_unknown_keys(row, f"cohort[{i}]", _MANIFEST_ROW_KEYS, errors)
        missing = _MANIFEST_ROW_KEYS - row.keys()
        if missing:
            errors.append(f"cohort[{i}] missing key(s): {sorted(missing)}")
            continue
        ticker = row["contender_symbol"]
        if ticker in seen_tickers:
            errors.append(f"cohort has duplicate contender_symbol: {ticker!r}")
        seen_tickers.add(ticker)

        expected_comparator = AUTHORIZED_COMPARATOR_MAP.get(ticker)
        if expected_comparator is not None and row["canonical_comparator_symbol"] != expected_comparator:
            errors.append(
                f"cohort[{i}] ({ticker!r}) canonical_comparator_symbol must be "
                f"{expected_comparator!r}, got {row['canonical_comparator_symbol']!r}"
            )

        expected_record_path = f"intelligence/contender_evaluation/{ticker}.yaml"
        if row["record_path"] != expected_record_path:
            errors.append(
                f"cohort[{i}] ({ticker!r}) record_path must be {expected_record_path!r}, "
                f"got {row['record_path']!r}"
            )

        record_path = records_dir / f"{ticker}.yaml"
        if not record_path.is_file():
            errors.append(f"cohort[{i}] ({ticker!r}) references missing record file {record_path}")
            continue
        record_data, record_read_errors = _read_yaml(record_path)
        if record_read_errors or not isinstance(record_data, dict):
            errors.append(f"cohort[{i}] ({ticker!r}) record file could not be parsed")
            continue
        expected_hash = canonical_record_hash(record_data)
        if row["content_sha256"] != expected_hash:
            errors.append(
                f"cohort[{i}] ({ticker!r}) content_sha256 mismatch -- manifest "
                f"{row['content_sha256']!r}, recomputed {expected_hash!r}"
            )
        if record_data.get("content_sha256") != row["content_sha256"]:
            errors.append(
                f"cohort[{i}] ({ticker!r}) manifest content_sha256 does not match the "
                f"record's own recorded content_sha256"
            )

    # exact population -- {VRT, WMT}, zero missing, zero extra, zero silent
    # contraction or expansion (CONTENDER-0003 SS F)
    missing_from_manifest = AUTHORIZED_POPULATION - seen_tickers
    extra_in_manifest = seen_tickers - AUTHORIZED_POPULATION
    if missing_from_manifest:
        errors.append(f"manifest missing authorized ticker(s): {sorted(missing_from_manifest)}")
    if extra_in_manifest:
        errors.append(f"manifest has non-authorized ticker(s): {sorted(extra_in_manifest)}")

    # orphan sealed records -- every *.yaml in records_dir must appear in
    # the manifest
    if records_dir.is_dir():
        on_disk = {p.stem for p in records_dir.glob("*.yaml") if p.name != "COHORT_MANIFEST.yaml"}
        orphans = on_disk - seen_tickers
        if orphans:
            errors.append(f"sealed record(s) on disk with no manifest entry: {sorted(orphans)}")

    return ValidationResult(valid=not errors, errors=errors, source=str(manifest_path))


def validate_contender_evaluation_directory(
    records_dir: Path, *, repo_root: Path | None = None,
) -> DirectoryValidationResult:
    results: list[ValidationResult] = []
    if not records_dir.is_dir():
        return DirectoryValidationResult(valid=True, results=[])

    for path in sorted(records_dir.glob("*.yaml")):
        if path.name == "COHORT_MANIFEST.yaml":
            continue
        results.append(validate_contender_evaluation_file(path, repo_root=repo_root))

    manifest_path = records_dir / "COHORT_MANIFEST.yaml"
    if manifest_path.is_file():
        results.append(validate_cohort_manifest(manifest_path, records_dir))
    else:
        results.append(ValidationResult(valid=False, errors=["COHORT_MANIFEST.yaml is missing"], source=str(manifest_path)))

    # exact population check independent of the manifest's own accounting
    on_disk_tickers = {p.stem for p in records_dir.glob("*.yaml") if p.name != "COHORT_MANIFEST.yaml"}
    missing = AUTHORIZED_POPULATION - on_disk_tickers
    extra = on_disk_tickers - AUTHORIZED_POPULATION
    pop_errors = []
    if missing:
        pop_errors.append(f"missing sealed record(s) for authorized ticker(s): {sorted(missing)}")
    if extra:
        pop_errors.append(f"sealed record(s) for non-authorized ticker(s): {sorted(extra)}")
    if pop_errors:
        results.append(ValidationResult(valid=False, errors=pop_errors, source="<population>"))

    return DirectoryValidationResult(valid=all(r.valid for r in results), results=results)


if __name__ == "__main__":
    import sys

    _repo_root = Path(__file__).resolve().parent
    _result = validate_contender_evaluation_directory(
        _repo_root / "intelligence" / "contender_evaluation", repo_root=_repo_root,
    )
    if _result.valid:
        print(f"contender_evaluation_validator: OK ({_result.record_count} result(s))")
        sys.exit(0)
    else:
        print("contender_evaluation_validator: FAILED")
        for _r in _result.results:
            if not _r.valid:
                for _err in _r.errors:
                    print(f"  - [{_r.source}] {_err}")
        sys.exit(1)
