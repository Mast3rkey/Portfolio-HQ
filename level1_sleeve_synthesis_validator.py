"""
level1_sleeve_synthesis_validator.py -- read-only schema validator for the
WS-0014 Level 1 cross-asset sleeve-allocation synthesis (Stage 3 content),
authorized by governance/decisions/XASSET-0013-ws0014-level1-synthesis-
content-authorization.md under the methodology
governance/decisions/XASSET-0012-ws0014-level1-cross-asset-synthesis-
methodology.md already designs in full (supporting artifact
governance/audits/WS0014_LEVEL1_CROSS_ASSET_SYNTHESIS_METHODOLOGY_
DESIGN_20260811.md).

ONE MODULE COVERS BOTH RECORD TYPES (sleeve_profile and sleeve_relationship),
the implementing session's own choice, justified per XASSET-0012 SS9's
explicit deferral (mirroring XASSET-0006 SS A point 3): the two schemas are
tightly coupled -- every sleeve_relationship record structurally references
two sleeve_profile records by content hash, and both record types share the
same closed six-sleeve vocabulary, the same forbidden-language scan suite,
and the same manifest bidirectional-reconciliation pattern. Splitting them
into two files would either duplicate that shared logic or force a
cross-file import between two otherwise-sibling modules -- unlike the
functional-doctrine/overlap-model split (XASSET-0006 vs XASSET-0007), which
was justified specifically because those two schemas are genuinely
independent, with no record of one type ever citing a record of the other.

Scope, exactly what XASSET-0012/XASSET-0013 authorize this module to
validate:

- Source-of-truth convention: intelligence/level1_sleeve_synthesis/
  profiles/<SLEEVE_ID>.yaml (exactly six) and intelligence/
  level1_sleeve_synthesis/relationships/<SLEEVE_A>_<SLEEVE_B>.yaml (exactly
  seven, of the fifteen possible C(6,2) pairs XASSET-0013 SS C authorizes),
  single-file records (no paired Markdown, matching every prior
  classification-shaped framework's convention), one COHORT_MANIFEST.yaml
  per subdirectory.
- Six closed sleeve_id values (XASSET-0012 SS2): equity, fund_broad_market
  (SPY/VEA/VWO), fund_gld_defensive (GLD), crypto (BTC/ETH/SOL), cash_reserve
  (CASH+RESERVE, one combined family per XASSET-0008), debt_reduction (a
  margin-policy lever, no targets.yaml row).
- Sleeve-relationship filenames restricted to deterministic-alphabetical
  <A>_<B> ordering (sleeve_a < sleeve_b lexicographically), mirroring
  relationship_validator.py's own enforcement exactly (REL-0001's pairwise
  convention, reused by reference per XASSET-0012 SS3/SS5).
- Sleeve profile (XASSET-0012 SS4): evidence_layer_references[] (layer-
  scoped by default, SS4.1; a sleeve_subject_scope sub-object required,
  without exception, on every reference into a layer whose own
  COHORT_MANIFEST.yaml is shared across more than one sleeve's authorized
  population -- SS4.1.1, computed generically from this module's own
  _LAYER_REGISTRY rather than hard-coded to a single named layer, since
  live inspection this session found FOUR layers genuinely shared across
  sleeve boundaries -- etf_classification, functional_doctrine,
  economic_assessment, and instrument_economic_assessment -- not only the
  one XASSET-0012's own preflight text names; this is a disclosed,
  implementation-time application of SS4.1.1's own general rule to every
  layer it actually applies to, never a redesign of the rule itself),
  economic_role_summary, evidence_coverage_profile (mechanically derived,
  never self-declared -- SS4.2), functional_role_note, abstention_index[]
  (sub-field-level abstention roll-up -- SS4.2.1), record_status, and the
  five standard seal fields.
- Sleeve relationship (XASSET-0012 SS5): sleeve_pair, profile_references[]
  (exactly two hash pins), primary_disposition (closed four-value
  vocabulary -- SS5.1), favored_sleeve_id (required iff primary_disposition
  == stronger_evidence_maturity, forced null otherwise), secondary_
  conditions[] (closed zero-to-three-member set, live-derived from the two
  cited profiles' own current state, never self-declared -- SS5.2),
  overlap_dimension_references[] (required iff overlap_or_duplication_
  disclosed is set; every cited dimension_id's own live computation_status
  must equal computed_from_existing_mechanism -- SS5.3), rationale,
  abstention_index[], record_status, and the five standard seal fields.
- Exactly six sleeve_profile records and exactly the seven XASSET-0013 SS C
  sleeve_relationship records authorized -- no eighth relationship, no
  seventh profile, no missing record.
- Zero numeric fields anywhere, no carve-out of any kind (XASSET-0012 SS6,
  stricter than the ETF framework's own expense_ratio_pct exception).
  IMPLEMENTATION NOTE, disclosed: XASSET-0012 SS4.1 names "population count"
  and "aggregate status tally" as concepts an evidence_layer_reference
  summarizes, while SS6 simultaneously requires zero numeric fields with no
  carve-out and explicitly cites a bare "evidence completeness: 80%" figure
  as the exact prohibited example. This module resolves that tension by
  never storing a population count or a status tally as a literal number
  anywhere in either schema -- instead, every evidence_layer_reference
  carries only hash pins (a manifest-level hash, plus a sleeve_subject_scope
  sub-object of per-subject hash pins where required) and short descriptive
  strings; "population count" and "aggregate status tally" are concepts
  this validator itself independently, live-derives by directly reading the
  cited layer's own real files at validation time (SS4.2's own "never
  self-declared" instruction, applied to its logical conclusion -- a stored
  count would itself be a self-declared numeric field, the very thing SS6
  forbids). This is the smallest change consistent with both sections' own
  text, not a narrowing of either.
- No composite priority/opportunity-cost score or rank anywhere, at any
  level, in any single record or across the full corpus (SS6) -- a
  dedicated forbidden-pattern scan for any bare score/rank/composite/
  priority-index-shaped key name not already part of this schema's own
  named fields.
- No cross-schema field-name leakage -- no equity-, ETF-, crypto-,
  functional-doctrine-, economic-assessment-, or instrument-economic-
  assessment-shaped field name anywhere in a Level 1 record (XASSET-0012
  SS9 item 8) -- a dedicated forbidden-key scan applied at every nesting
  level.
- Level 1 / Level 2 boundary (XASSET-0012 SS7/SS9 item 9) -- zero target_pct/
  max_position_size/tier/gate/cluster/holding-shaped key name or value
  anywhere; no individual equity ticker, fund, or coin symbol may be named
  as bearing its own weight, target, or size (structural-reference hash
  pins and sleeve_subject_scope subject identity lists are explicitly
  exempted from this specific check, since naming which sealed records a
  sleeve profile is entitled to draw evidence from is not a weight or size
  claim -- XASSET-0012 SS4.1.1's own text: "an identity list only... never
  a per-ticker judgment, weight, or conclusion").
- Portfolio-selection / eligibility-language boundary (XASSET-0012 SS7/SS8.1
  /SS9 item 17) -- a materially separate mechanism from the comparative-
  investment-superiority scan (item 12), the directive/trading-language
  scan (item 10), and the structural target/weight-leakage scan (item 9);
  hardened at implementation time per XASSET-0013 SS H's own mandatory
  adversarial probe requirement -- see the module-level "ELIGIBILITY
  PARAPHRASE PROBE" section below for the disclosed result.
- Contender/QQQ boundary (XASSET-0012 SS7/SS9 item 13) -- zero citation of
  intelligence/contender_evaluation/ or intelligence/contenders/ anywhere;
  no fund population beyond the exact four sealed etf_classification
  instruments (SPY/VEA/VWO/GLD), no QQQ.
- Overlap citation rule (XASSET-0012 SS5.3/SS9 item 5) -- overlap_
  dimension_references may cite only overlap_model dimensions whose own
  live computation_status equals computed_from_existing_mechanism; citing
  one of the four interface-only/requires-future-authorization dimensions
  is a hard failure, independent of the record's own secondary_conditions
  claim.
- Live, independent recomputation of every structural reference hash (this
  module's own evidence-layer manifest/record hashes; sleeve_profile
  hashes cited by a sleeve_relationship's profile_references; overlap_
  model dimension hashes cited by overlap_dimension_references) -- never
  trusted from a stored value (XASSET-0012 SS9 item 3).
- evidence_coverage_profile and secondary_conditions are both re-derived
  live from the cited layers'/profiles' own current state at validation
  time, never accepted as self-declared (XASSET-0012 SS9 items 4/6).
- Non-cascading abstention discipline -- an abstention on one field never
  forces or implies a value on another (XASSET-0012 SS9 item 16).
- Manifest bidirectional reconciliation (hash, duplicate, missing, extra,
  orphan) for both subdirectories' own COHORT_MANIFEST.yaml (SS9 item 15).
- Protected-path/byte-identity proof that every one of the twelve input
  layers this module reads from remains untouched (SS9 item 14).
- Closed schema at every nesting level, extra-key rejection everywhere
  (SS9 item 1).

This module is a validator, not a data producer. It never opens a file in
write/append/update mode, never creates a directory, and has zero import
relationship with allocate.py or margin_state.py in either direction.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from hashlib import sha256
from pathlib import Path

import yaml

SCHEMA_VERSION = "1.0"

_GOVERNING_DECISION = "XASSET-0013"

# ---------------------------------------------------------------------------
# XASSET-0012 SS2 -- the closed six-sleeve taxonomy.
# ---------------------------------------------------------------------------

EQUITY = "equity"
FUND_BROAD_MARKET = "fund_broad_market"
FUND_GLD_DEFENSIVE = "fund_gld_defensive"
CRYPTO = "crypto"
CASH_RESERVE = "cash_reserve"
DEBT_REDUCTION = "debt_reduction"

SLEEVE_IDS = frozenset({
    EQUITY, FUND_BROAD_MARKET, FUND_GLD_DEFENSIVE, CRYPTO, CASH_RESERVE, DEBT_REDUCTION,
})

# ---------------------------------------------------------------------------
# XASSET-0013 SS C -- the exact, closed seven-pair sleeve_relationship
# population, filed in REL-0001's own deterministic-alphabetical order.
# ---------------------------------------------------------------------------

AUTHORIZED_RELATIONSHIP_PAIRS: tuple[tuple[str, str], ...] = (
    (CASH_RESERVE, DEBT_REDUCTION),
    (CASH_RESERVE, EQUITY),
    (CRYPTO, EQUITY),
    (CRYPTO, FUND_GLD_DEFENSIVE),
    (DEBT_REDUCTION, EQUITY),
    (EQUITY, FUND_BROAD_MARKET),
    (EQUITY, FUND_GLD_DEFENSIVE),
)
for _a, _b in AUTHORIZED_RELATIONSHIP_PAIRS:
    assert _a < _b, f"AUTHORIZED_RELATIONSHIP_PAIRS entry not alphabetical: {_a!r}, {_b!r}"
del _a, _b

# ---------------------------------------------------------------------------
# XASSET-0012 SS1/SS2/SS4.1.1 -- the layer registry. For each governed
# Intelligence layer this synthesis draws from: which module owns its
# canonical_record_hash(), its directory, and which sleeve(s) draw which
# subject(s) from it. A layer whose own dict below carries more than one
# sleeve_id key is, by construction, "shared across more than one sleeve's
# authorized population" (XASSET-0012 SS4.1.1) -- sleeve_subject_scope is
# then REQUIRED on every evidence_layer_reference entry citing it; a layer
# with exactly one sleeve_id key is single-sleeve -- sleeve_subject_scope
# is FORBIDDEN there. A subject value of None means the sleeve consumes
# that layer's own full, unscoped population (equity's four layers;
# crypto's own crypto_classification layer).
# ---------------------------------------------------------------------------

_LAYER_REGISTRY: dict[str, dict] = {
    "classification": {
        "module": "classification_validator",
        "directory": "intelligence/classification",
        "sleeve_subjects": {EQUITY: None},
    },
    "valuation_archetype": {
        "module": "valuation_archetype_validator",
        "directory": "intelligence/valuation_archetype",
        "sleeve_subjects": {EQUITY: None},
    },
    "valuation_evidence": {
        "module": "valuation_evidence_validator",
        "directory": "intelligence/valuation_evidence",
        "sleeve_subjects": {EQUITY: None},
    },
    "valuation_results": {
        "module": "valuation_result_validator",
        "directory": "intelligence/valuation_results",
        "sleeve_subjects": {EQUITY: None},
    },
    "etf_classification": {
        "module": "etf_classification_validator",
        "directory": "intelligence/etf_classification",
        "sleeve_subjects": {
            FUND_BROAD_MARKET: ("SPY", "VEA", "VWO"),
            FUND_GLD_DEFENSIVE: ("GLD",),
        },
    },
    "crypto_classification": {
        "module": "crypto_classification_validator",
        "directory": "intelligence/crypto_classification",
        "sleeve_subjects": {CRYPTO: None},
    },
    "functional_doctrine": {
        "module": "functional_doctrine_validator",
        "directory": "intelligence/functional_doctrine",
        "sleeve_subjects": {
            CASH_RESERVE: ("CASH", "RESERVE"),
            FUND_GLD_DEFENSIVE: ("GLD_DEFENSIVE_ROLE",),
            DEBT_REDUCTION: ("DEBT_REDUCTION",),
        },
    },
    "economic_assessment": {
        "module": "economic_assessment_validator",
        "directory": "intelligence/economic_assessment",
        "sleeve_subjects": {
            FUND_GLD_DEFENSIVE: ("GLD",),
            CASH_RESERVE: ("CASH_LIKE_CAPITAL",),
        },
    },
    "instrument_economic_assessment": {
        "module": "instrument_economic_assessment_validator",
        "directory": "intelligence/instrument_economic_assessment",
        "sleeve_subjects": {
            FUND_BROAD_MARKET: ("SPY", "VEA", "VWO"),
            CRYPTO: ("BTC", "ETH", "SOL"),
        },
    },
}

# Which layers a sleeve's own profile is authorized to cite, in a fixed,
# deterministic order (XASSET-0012 SS2's own per-sleeve governed-layer
# table -- "primary governed layers (structural)" first, then "secondary
# governed layers (functional/economic)").
_SLEEVE_LAYERS: dict[str, tuple[str, ...]] = {
    EQUITY: ("classification", "valuation_archetype", "valuation_evidence", "valuation_results"),
    FUND_BROAD_MARKET: ("etf_classification", "instrument_economic_assessment"),
    FUND_GLD_DEFENSIVE: ("etf_classification", "functional_doctrine", "economic_assessment"),
    CRYPTO: ("crypto_classification", "instrument_economic_assessment"),
    CASH_RESERVE: ("functional_doctrine", "economic_assessment"),
    DEBT_REDUCTION: ("functional_doctrine",),
}


def _layer_is_shared(layer_name: str) -> bool:
    return len(_LAYER_REGISTRY[layer_name]["sleeve_subjects"]) > 1


def _expected_subjects(layer_name: str, sleeve_id: str) -> tuple[str, ...] | None:
    """None means the sleeve draws the layer's full, unscoped population."""
    return _LAYER_REGISTRY[layer_name]["sleeve_subjects"].get(sleeve_id)


# ---------------------------------------------------------------------------
# XASSET-0012 SS5.1/SS5.2 -- closed relationship vocabularies.
# ---------------------------------------------------------------------------

STRONGER_EVIDENCE_MATURITY = "stronger_evidence_maturity"
ROLE_PRESERVING = "role_preserving"
COEXISTENCE_SUPPORTED = "coexistence_supported"
RELATIONSHIP_ABSTENTION = "unable_to_determine"

_PRIMARY_DISPOSITION_VALUES = frozenset({
    STRONGER_EVIDENCE_MATURITY, ROLE_PRESERVING, COEXISTENCE_SUPPORTED, RELATIONSHIP_ABSTENTION,
})

OVERLAP_OR_DUPLICATION_DISCLOSED = "overlap_or_duplication_disclosed"
EVIDENCE_PARTIAL_PRESENT = "evidence_partial_present"
FORCED_ABSTENTION_PRESENT = "forced_abstention_present"

_SECONDARY_CONDITION_VALUES = frozenset({
    OVERLAP_OR_DUPLICATION_DISCLOSED, EVIDENCE_PARTIAL_PRESENT, FORCED_ABSTENTION_PRESENT,
})

# XASSET-0012 SS4.2 -- closed evidence_coverage_profile vocabulary.
FULLY_COMPUTED = "fully_computed"
SUBSTANTIALLY_COMPUTED_WITH_DISCLOSED_GAPS = "substantially_computed_with_disclosed_gaps"
MATERIALLY_INCOMPLETE = "materially_incomplete"
FORCED_ABSTENTION = "forced_abstention"

_EVIDENCE_COVERAGE_VALUES = frozenset({
    FULLY_COMPUTED, SUBSTANTIALLY_COMPUTED_WITH_DISCLOSED_GAPS, MATERIALLY_INCOMPLETE, FORCED_ABSTENTION,
})

_LIFECYCLE_VALUES = frozenset({"draft", "sealed"})

_COMPUTED_FROM_EXISTING_MECHANISM = "computed_from_existing_mechanism"

_OVERLAP_MODEL_DIR = "intelligence/overlap_model"
_PROFILES_DIR = "intelligence/level1_sleeve_synthesis/profiles"
_RELATIONSHIPS_DIR = "intelligence/level1_sleeve_synthesis/relationships"


# ---------------------------------------------------------------------------
# Small shared helpers (deliberately local to this module, matching this
# repository's own established per-file-helper convention).
# ---------------------------------------------------------------------------

def _non_empty_str(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _reject_unknown_keys(value: dict, field_name: str, allowed: frozenset[str] | set[str], errors: list[str]) -> None:
    extra = set(value.keys()) - set(allowed)
    if extra:
        errors.append(f"{field_name} has unrecognized key(s): {sorted(extra)}")


def _read_yaml(path: Path) -> tuple[object, list[str]]:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        return None, [f"could not read file: {exc}"]
    try:
        return yaml.safe_load(text), []
    except yaml.YAMLError as exc:
        return None, [f"YAML parse error: {exc}"]


def _hash_manifest_data(data: dict) -> str:
    """Live hash of an entire source layer's own COHORT_MANIFEST.yaml
    content -- the same canonical-JSON + sha256 technique every sibling
    validator's own canonical_record_hash() already uses for a sealed
    record, applied here to a manifest instead (which carries no seal
    fields of its own to exclude)."""
    canonical = json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return sha256(canonical.encode("utf-8")).hexdigest()


_SEAL_FIELDS = (
    "sealed_at", "governing_decisions", "drafting_session_or_shard_id",
    "content_sha256", "cohort_manifest_entry",
)


def canonical_record_hash(data: dict) -> str:
    """Excludes only the five seal fields, mirroring every prior sealed-
    cohort validator's identical convention. Shared by both record types
    in this module -- profile and relationship records use the same seal-
    field set."""
    hashable = {k: v for k, v in data.items() if k not in _SEAL_FIELDS}
    canonical = json.dumps(hashable, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return sha256(canonical.encode("utf-8")).hexdigest()


def _get_layer_hash_fn(layer_name: str):
    """Local, per-call import of the cited layer's own canonical_record_
    hash() function -- avoids a module-level dependency on all nine sibling
    modules for callers that only need this module's own schema shape,
    matching contender_evaluation_validator.py's/economic_assessment_
    validator.py's established local-import convention for cross-schema
    structural-reference verification."""
    module_name = _LAYER_REGISTRY[layer_name]["module"]
    import importlib
    mod = importlib.import_module(module_name)
    return mod.canonical_record_hash


# ---------------------------------------------------------------------------
# Free-text scans -- six materially separate mechanisms, matching this
# repository's own established convention that each forbidden-content
# category gets its own distinct check rather than one merged pattern list
# (contender_evaluation_validator.py SS F is the direct precedent this
# reuses, adapted for Level 1's own vocabulary):
#   1. policy-leak scan (target/tier/gate/conviction-shaped leakage)
#   2. chart-domain scan
#   3. directive/trading-language scan
#   4. numeric-leakage scan (bare digit, no carve-out -- SS6)
#   5. comparative-investment-superiority scan (SS8)
#   6. eligibility/portfolio-membership scan (SS8.1) -- see the dedicated
#      "ELIGIBILITY PARAPHRASE PROBE" section below for the adversarial
#      hardening this scan received per XASSET-0013 SS H's mandatory probe.
# Plus a structural (not free-text) forbidden-key-name scan for score/
# rank/composite/priority-index-shaped keys, target_pct/max_position_size/
# tier/gate/cluster/holding-shaped keys, and every cross-schema field name
# named in the module docstring above.
# ---------------------------------------------------------------------------

_POLICY_LEAK_PATTERNS = [
    re.compile(p, re.IGNORECASE)
    for p in [
        r"\bconviction\b",
        r"portfolio_role_ref",
        r"target_pct",
        r"max_position_size",
        r"targets\.yaml",
        r"holdings\.yaml",
        r"gates\.yaml",
        r"\bnext_gate\b",
        r"\ballow_add\b",
        r"issuer_lookthrough\.yaml",
        r"%\s*of\s+(the\s+)?book",
        r"%\s*of\s+portfolio",
        r"percent\s+of\s+(the\s+)?book",
        r"percent\s+of\s+portfolio",
        r"target\s+weight",
        r"destination\s+weight",
        r"primary_archetype",
        r"capital_priority",
        r"risk_concentration",
        r"economic_system_ref",
        r"case_for_review",
        r"maintain_current_weight",
        r"divergence_requires_review",
        r"baseline_assumption_stale",
        r"structural_measurement_gap",
        r"relationship_measurement_required",
        r"capital_use_type",
        r"hard_constraint_status",
        # A sizing-recommendation shape -- naming an actual target/size
        # figure change is Level 2/allocator territory (XASSET-0012 SS7),
        # distinct from the bare, legitimately-used word "target" alone
        # (this schema's own boundary-disclosure prose routinely states
        # "no claim about... target" without recommending any change).
        r"\btarget\b(?:[\s,;:]+[a-z][\w'-]*){0,3}[\s,;:]+\b(?:should|ought)\s+(?:be\s+)?(?:increase|decrease|raise|lower|change|adjust)",
        r"\b(?:increase|decrease|raise|lower|adjust)\b(?:[\s,;:]+[a-z][\w'-]*){0,3}[\s,;:]+\bthe\s+target\b",
        r"\bsize\b(?:[\s,;:]+[a-z][\w'-]*){0,3}[\s,;:]+\bshould\s+(?:be\s+)?(?:increase|decrease|raise|lower)",
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

# "stage" is also legitimate vocabulary as a hyphenated compound (e.g.
# "early-stage") and as this repository's own four-stage design-sequence
# noun ("Stage 1... Stage 2..."); whitelisted the same way
# valuation_archetype_validator.py/contender_evaluation_validator.py
# already do for "stage", extended here to also cover the bare noun form
# this module's own governing decisions use routinely ("this Stage 3
# implementation").
_STAGE_LEGITIMATE_USE_PATTERNS = [
    re.compile(r"[a-z]+-stage", re.IGNORECASE),
    re.compile(r"\bstage\s+\d\b", re.IGNORECASE),
]


def _prohibited_content_scan(text: str, *, skip_directive: bool = False) -> list[str]:
    findings: list[str] = []
    for pat in _POLICY_LEAK_PATTERNS:
        if pat.search(text):
            findings.append(f"policy-leak:{pat.pattern}")
    for pat in _CHART_DOMAIN_PATTERNS:
        if pat.search(text):
            findings.append(f"chart-domain:{pat.pattern}")
    if not skip_directive:
        stage_scrubbed = text
        for pat in _STAGE_LEGITIMATE_USE_PATTERNS:
            stage_scrubbed = pat.sub("", stage_scrubbed)
        for pat in _DIRECTIVE_PATTERNS:
            haystack = stage_scrubbed if pat.pattern == r"\bstage\b" else text
            if pat.search(haystack):
                findings.append(f"directive-word:{pat.pattern}")
    if _gate_word_leak(text):
        findings.append("bare-gate-word")
    return findings


# -- numeric leakage: bare digit, magnitude word, spelled-out cardinal,
#    no carve-out of any kind (XASSET-0012 SS6) -----------------------------

_BARE_DIGIT_PATTERN = re.compile(r"\d")

_MAGNITUDE_WORD_PATTERN = re.compile(
    r"\b(times|twice|doubled?|tripled?|quadrupled?|"
    r"threefold|twofold|fourfold|fivefold|\w+-fold|"
    r"halved)\b",
    re.IGNORECASE,
)

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


# -- comparative-investment-superiority scan (XASSET-0012 SS8) -- reused,
#    not redesigned, from contender_evaluation_validator.py's own SS F
#    fifth-bullet mechanism (that module's own class, already broadened
#    twice across two independent reviews) -----------------------------

_COMPARATIVE_SUPERIORITY_NOUNS = (
    "investment", "compounder", "business", "company", "opportunity",
    "choice", "pick", "holding", "allocation", "quality", "thesis", "case",
    "option", "options", "one", "sleeve",
)
_COMPARATIVE_SUPERIORITY_ADJECTIVES = (
    "stronger", "weaker", "superior", "inferior", "better", "worse",
    "preferable", "preferred", "best", "worst", "smarter",
    "more attractive", "less attractive", "more compelling", "less compelling",
    "more appealing", "less appealing", "higher-quality", "lower-quality",
    "top-tier", "top-rated",
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


# ---------------------------------------------------------------------------
# ELIGIBILITY PARAPHRASE PROBE (XASSET-0012 SS8.1, hardened per XASSET-0013
# SS H's mandatory pre-push adversarial probe requirement).
#
# XASSET-0012's own final delta review (pullrequestreview-4906063644)
# carried one non-blocking NOTE, explicitly deferred rather than resolved:
# natural-language eligibility/inclusion paraphrases that avoid SS8.1's
# original literal phrase list while still asserting a portfolio-membership
# conclusion ("crypto is eligible for portfolio inclusion", "exclude gold
# from portfolio"). XASSET-0013 SS H requires this implementing session to
# write adversarial test cases against that exact vulnerability class before
# push and disclose the result.
#
# RESULT, DISCLOSED: building the adversarial matrix (see
# test_level1_sleeve_synthesis_validator.py's own dedicated eligibility-
# paraphrase test class) against SS8.1's ORIGINAL literal phrase list found
# a genuine gap -- ordinary paraphrases using "eligible"/"deserves"/
# "belongs"/"merits"/"warrants"/"ought to"/"should remain"/"remove... from
# the investable set" outside the small set of exact strings SS8.1's own
# text enumerates were NOT caught. Per XASSET-0013 SS H's own explicit
# instruction ("a probe requirement, not a redesign authorization"), and
# per this repository's own established "apply the smallest bounded
# correction consistent with the existing scan's own authority" discipline
# (the identical class of finding CONTENDER-0003's own two prior review
# rounds already resolved for its sibling promotion-language/comparative-
# superiority scans, by broadening the SAME closed pattern list rather than
# inventing a new mechanism), this scan below is broadened -- not redesigned
# -- to catch the paraphrase class while preserving every one of SS8.1's own
# mandatory false-positive guards. The underlying SS8.1 boundary itself
# (comparative evidence findings only, no sleeve eligibility/inclusion
# disposition) is unchanged.
# ---------------------------------------------------------------------------

_ELIGIBILITY_PATTERNS = [
    re.compile(p, re.IGNORECASE)
    for p in [
        # SS8.1's own original, literal phrase list.
        r"\binclud(e|es|ed|ing)\b(?:[\s,;:]+[a-z][\w'-]*){0,4}[\s,;:]+\bin\s+the\s+portfolio\b",
        r"\bshould\s+be\s+included\s+in\s+the\s+portfolio\b",
        r"\bwarrants?\s+inclusion\b",
        r"\bmerits?\s+inclusion\b",
        r"\bdeserves?\s+inclusion\b",
        r"\bexclud(e|es|ed|ing)\b(?:[\s,;:]+[a-z][\w'-]*){0,4}[\s,;:]+\bfrom\s+the\s+portfolio\b",
        r"\bshould\s+be\s+excluded\s+from\s+the\s+portfolio\b",
        r"\bremov(e|es|ed|ing)\b(?:[\s,;:]+[a-z][\w'-]*){0,4}[\s,;:]+\bfrom\s+the\s+portfolio\b",
        r"\beligible\s+for\s+the\s+portfolio\b",
        r"\bportfolio-eligible\b",
        r"\bineligible\s+for\s+the\s+portfolio\b",
        r"\bshould\s+be\s+in\s+the\s+portfolio\b",
        r"\bshould\s+not\s+be\s+in\s+the\s+portfolio\b",
        r"\bshould\s+remain\s+in\s+the\s+portfolio\b",
        r"\bshould\s+not\s+remain\s+in\s+the\s+portfolio\b",
        r"\bportfolio\s+membership\s+is\s+(confirmed|warranted)\b",
        r"\bfinal\s+selection\b",
        r"\bselected\s+for\s+the\s+portfolio\b",
        r"\bnot\s+selected\s+for\s+the\s+portfolio\b",
        r"\bsleeve\s*:\s*in\b",
        r"\bthis\s+sleeve\s+is\s+out\b",
        # Hardened, round-2 additions -- ordinary paraphrases the review's
        # own carried-forward NOTE named as sitting just outside the
        # original list, plus the same-shaped constructions the equivalent
        # promotion-language scan in contender_evaluation_validator.py was
        # already broadened to catch for an analogous vulnerability class.
        r"\beligible\s+for\s+portfolio\s+inclusion\b",
        r"\bexclud(e|es|ed|ing)\s+(gold|crypto|equity|equities|cash|debt\s+reduction)\s+from\s+(the\s+)?portfolio\b",
        r"\bbelongs?\s+(in|within)\s+the\s+portfolio\b",
        r"\bdoes\s+not\s+belong\s+(in|within)\s+the\s+portfolio\b",
        r"\bought\s+to\s+(be|remain)\s+(in|part\s+of)\s+the\s+portfolio\b",
        r"\bshould\s+be\s+part\s+of\s+the\s+portfolio\b",
        r"\bshould\s+not\s+be\s+part\s+of\s+the\s+portfolio\b",
        r"\bmerits?\s+(a\s+)?place\s+in\s+the\s+portfolio\b",
        r"\bdeserves?\s+(a\s+)?place\s+in\s+the\s+portfolio\b",
        r"\bportfolio-worthy\b",
        r"\bwarrants?\s+(a\s+)?place\s+in\s+the\s+portfolio\b",
        r"\binclusion\s+is\s+warranted\b",
        r"\bmembership\s+is\s+justified\b",
        r"\bremove\s+this\s+sleeve\s+from\s+the\s+investable\s+set\b",
        r"\bshould\s+be\s+removed\s+from\s+the\s+investable\s+set\b",
        r"\bnot\s+part\s+of\s+the\s+investable\s+(set|universe)\b",
        # Round-3 additions (XASSET-0013 SS H's mandatory pre-push
        # adversarial probe, performed by this implementing session):
        # empirically testing the task's own required phrase matrix against
        # the round-2 scan found seven genuine, ordinary-paraphrase gaps
        # ("should remain part of the portfolio", "excluded from holdings",
        # a bare "ought to be included/excluded", and four word-order/
        # subject-object-reversal variants of already-caught phrases) --
        # closed the same way round 2 closed CONTENDER-0003's own carried-
        # forward NOTE: broadening this existing, closed pattern list, never
        # inventing a new mechanism.
        r"\bshould\s+remain\s+part\s+of\s+the\s+portfolio\b",
        r"\bdeserves?\s+to\s+remain\s+(in|part\s+of)\s+the\s+portfolio\b",
        r"\bexclud(e|es|ed|ing)\b(?:[\s,;:]+[a-z][\w'-]*){0,4}[\s,;:]+\bfrom\s+holdings\b",
        r"\bought\s+to\s+be\s+(included|excluded)\b",
        r"\bwarranted\s+that\b(?:[\s,;:]+[a-z][\w'-]*){0,6}[\s,;:]+\binclusion\b",
        r"\binclusion\b(?:[\s,;:]+[a-z][\w'-]*){0,6}[\s,;:]+\bis\s+eligible\b",
        r"\b(the\s+)?portfolio\s+should\s+(not\s+)?include\s+this\s+sleeve\b",
        r"\bshould\s+not\s+include\s+this\s+sleeve\b",
        # "deserves capital" -- a capital-priority-allocation claim, the
        # same conceptual family as the already-present "deserves
        # inclusion"/"deserves a place in the portfolio" patterns, adding
        # only the direct-object-omitted variant this session's own
        # adversarial probe found unguarded.
        r"\bdeserves?\s+(more\s+)?capital\b",
        r"\bwarrants?\s+(more\s+)?capital\b",
    ]
]

# Mandatory false-positive guards (SS8.1) -- these must NEVER match the
# scan above. Not implemented as an allow-list scrub (unlike the gate-word
# scan's own approach): each ELIGIBILITY pattern is itself already anchored
# tightly enough (requiring "the portfolio"/"portfolio inclusion"/"the
# investable set" as an explicit object) that legitimate evidence/process
# uses of "included"/"excluded" (e.g. "included in the evidence inventory",
# "excluded from this calculation because evidence is unavailable", "the
# manifest includes four instruments", "excluded from the first synthesis's
# governed evidence base") never satisfy any pattern's own required phrase
# -- proven by dedicated adversarial tests, not asserted here.


def _eligibility_language_scan(text: str) -> list[str]:
    findings: list[str] = []
    for pat in _ELIGIBILITY_PATTERNS:
        if pat.search(text):
            findings.append(f"eligibility-language:{pat.pattern}")
    return findings


def _scan_free_text(
    value: object, field_name: str, errors: list[str], *,
    include_numeric: bool = True, is_citation_field: bool = False,
) -> None:
    """is_citation_field=True applies the citation-field exemption pattern
    already established elsewhere in this repository (functional_doctrine_
    validator.py's/contender_evaluation_validator.py's own _CITATION_FIELD_
    NAMES): the directive-word scan is skipped, and the numeric-leakage
    scan is skipped, since a legitimate path/hash/date string should never
    be penalized for incidentally containing digits or a bare directive-
    shaped word. Every other scan -- policy-leak, chart-domain,
    comparative-superiority, eligibility-language -- still applies in full,
    with no exemption."""
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
        if include_numeric and not is_citation_field:
            for finding in _numeric_leakage_scan(text):
                errors.append(f"{field_name} contains prohibited content ({finding})")
        for finding in _comparative_superiority_scan(text):
            errors.append(f"{field_name} contains prohibited content ({finding})")
        for finding in _eligibility_language_scan(text):
            errors.append(f"{field_name} contains prohibited content ({finding})")


# ---------------------------------------------------------------------------
# Structural forbidden-key-name scan -- score/rank/composite leakage plus
# every cross-schema field name named in the module docstring, plus the
# Level 1/Level 2 target/weight/tier/gate/cluster/holding-shaped leakage
# scan (XASSET-0012 SS7/SS9 item 9).
# ---------------------------------------------------------------------------

_SCORE_RANK_KEY_SUBSTRINGS = ("score", "rank", "priority_index", "composite", "ranking")

_CROSS_SCHEMA_FORBIDDEN_KEYS = frozenset({
    # equity (classification/valuation_archetype/valuation_evidence/valuation_results)
    "economic_role", "capital_priority", "risk_concentration", "portfolio_role_ref",
    "conviction", "economic_system_ref", "primary_archetype", "secondary_archetype",
    "result_status", "methodology_families_applied",
    # etf_classification
    "structural_role", "constituent_exposure", "overlap_and_concentration",
    "cost_and_tracking_quality", "liquidity", "structure_and_methodology",
    # crypto_classification
    "network_fundamentals", "economic_model", "liquidity_and_market_structure",
    "custody_and_counterparty_risk", "correlation_and_volatility",
    "regulatory_and_structural_uncertainty",
    # functional_doctrine / economic_assessment
    "capital_use_type", "functional_role", "hard_constraint_status",
    "economic_assessment_readiness", "liquidity_character", "capital_preservation_character",
    "deployability_and_optionality", "instrument_specific_economic_characterization",
    # instrument_economic_assessment
    "macro_behavioral_characterization",
    # Level 2 / allocator-policy-shaped keys never permitted on a Level 1 record
    "target_pct", "max_position_size", "tier", "gate", "cluster", "destination_weight",
})

_LEVEL2_LEAKAGE_KEY_SUBSTRINGS = ("target_pct", "max_position_size")


def _scan_key_names_recursive(value: object, path: str, errors: list[str], *, allow_keys: frozenset[str] = frozenset()) -> None:
    """Defense-in-depth: an explicit, named scan for score/rank/composite-
    shaped key names, cross-schema field-name leakage, and Level 2 sizing-
    shaped key names anywhere in the document tree, distinct from (and in
    addition to) closed-schema extra-key rejection at every level.
    allow_keys exempts a bounded set of keys this schema's own design
    deliberately permits despite overlapping a forbidden substring (none
    at present -- kept for parity with sibling modules' own established
    shape)."""
    if isinstance(value, dict):
        for k, v in value.items():
            if k in allow_keys:
                _scan_key_names_recursive(v, f"{path}.{k}", errors, allow_keys=allow_keys)
                continue
            lowered = str(k).lower()
            for substring in _SCORE_RANK_KEY_SUBSTRINGS:
                if substring in lowered:
                    errors.append(f"{path}.{k} is a forbidden score/rank/composite-shaped key name")
            if k in _CROSS_SCHEMA_FORBIDDEN_KEYS:
                errors.append(f"{path}.{k} is a forbidden cross-schema/Level-2-leakage key name")
            _scan_key_names_recursive(v, f"{path}.{k}", errors, allow_keys=allow_keys)
    elif isinstance(value, list):
        for i, item in enumerate(value):
            _scan_key_names_recursive(item, f"{path}[{i}]", errors, allow_keys=allow_keys)


_CONTENDER_CITATION_PATTERNS = [
    re.compile(p, re.IGNORECASE)
    for p in [
        r"contender_evaluation", r"intelligence/contenders", r"\bVRT\b", r"\bWMT\b",
    ]
]


def _scan_contender_citation(text: str) -> list[str]:
    findings: list[str] = []
    for pat in _CONTENDER_CITATION_PATTERNS:
        if pat.search(text):
            findings.append(f"contender-boundary:{pat.pattern}")
    return findings


def _scan_all_strings_for_contender_citation(value: object, path: str, errors: list[str]) -> None:
    if isinstance(value, str):
        for finding in _scan_contender_citation(value):
            errors.append(f"{path} contains prohibited content ({finding})")
    elif isinstance(value, dict):
        for k, v in value.items():
            _scan_all_strings_for_contender_citation(v, f"{path}.{k}", errors)
    elif isinstance(value, list):
        for i, item in enumerate(value):
            _scan_all_strings_for_contender_citation(item, f"{path}[{i}]", errors)


# ---------------------------------------------------------------------------
# Live evidence-coverage derivation -- SIX per-sleeve functions, one per
# sleeve_id, each independently reading the real sealed source files this
# session inventoried (module docstring) and returning the mechanically
# correct evidence_coverage_profile value plus the exact set of sub-field-
# level abstentions live in that sleeve's own scoped population today
# (XASSET-0012 SS4.2/SS4.2.1: "mechanically derived... never self-
# declared"). A profile record's own declared evidence_coverage_profile and
# abstention_index[] are cross-checked against this live computation at
# validation time -- a record claiming a value this computation does not
# independently reproduce is a hard failure.
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class _AbstentionFinding:
    source_layer: str
    field_path: str
    value: str


def _load_dir_records(repo_root: Path, directory: str, id_key: str | None = None) -> dict[str, dict]:
    """Loads every *.yaml record (excluding COHORT_MANIFEST.yaml) in a
    directory, keyed by filename stem."""
    d = repo_root / directory
    out: dict[str, dict] = {}
    if not d.is_dir():
        return out
    for p in sorted(d.glob("*.yaml")):
        if p.name == "COHORT_MANIFEST.yaml":
            continue
        data, errs = _read_yaml(p)
        if not errs and isinstance(data, dict):
            out[p.stem] = data
    return out


def _compute_equity_coverage(repo_root: Path) -> tuple[str, list[_AbstentionFinding]]:
    findings: list[_AbstentionFinding] = []
    results = _load_dir_records(repo_root, "intelligence/valuation_results")
    partial = [t for t, r in results.items() if r.get("result_status") == "partial"]
    if partial:
        findings.append(_AbstentionFinding(
            "valuation_results", "result_status",
            "a disclosed minority of the equity sleeve's own sealed valuation-result records "
            "remain partial rather than completed, per VALUATION-0006/VALUATION-0007's own "
            "sealed corpus",
        ))
    evidence = _load_dir_records(repo_root, "intelligence/valuation_evidence")
    dre_abstained = [
        t for t, r in evidence.items()
        if isinstance(r.get("discount_rate_evidence"), dict) and r["discount_rate_evidence"].get("abstention_reason")
    ]
    if dre_abstained and len(dre_abstained) == len(evidence):
        findings.append(_AbstentionFinding(
            "valuation_evidence", "discount_rate_evidence",
            "discount-rate evidence is abstained across the equity sleeve's entire sealed "
            "valuation-evidence corpus, per VALUATION-0004/VALUATION-0005's own disclosed gap",
        ))
    archetype_abstained = [
        t for t, r in _load_dir_records(repo_root, "intelligence/valuation_archetype").items()
        if r.get("primary_archetype") == "unable_to_determine_archetype"
    ]
    for t in archetype_abstained:
        findings.append(_AbstentionFinding("valuation_archetype", "primary_archetype", "unable_to_determine_archetype"))
    classification = _load_dir_records(repo_root, "intelligence/classification")
    no_assessment = [t for t, r in classification.items() if isinstance(r.get("capital_priority"), dict) and r["capital_priority"].get("status") == "no_assessment"]
    if no_assessment:
        findings.append(_AbstentionFinding(
            "classification", "capital_priority.status",
            "a disclosed minority of the equity sleeve's own sealed classification records "
            "carry a capital-priority abstention rather than a determined status",
        ))
    return SUBSTANTIALLY_COMPUTED_WITH_DISCLOSED_GAPS, findings


def _compute_fund_broad_market_coverage(repo_root: Path) -> tuple[str, list[_AbstentionFinding]]:
    findings: list[_AbstentionFinding] = []
    etf = _load_dir_records(repo_root, "intelligence/etf_classification")
    scoped = {k: v for k, v in etf.items() if k in ("SPY", "VEA", "VWO")}
    if any(r.get("evidence_quality_status") == "partial" for r in scoped.values()):
        findings.append(_AbstentionFinding(
            "etf_classification", "evidence_quality_status",
            "every fund in the broad-market sleeve's own sealed ETF-classification cohort "
            "carries a disclosed partial evidence-quality status",
        ))
    iea = _load_dir_records(repo_root, "intelligence/instrument_economic_assessment")
    iea_scoped = {k: v for k, v in iea.items() if k in ("SPY", "VEA", "VWO")}
    if any(r.get("evidence_quality_status") == "partial" for r in iea_scoped.values()):
        findings.append(_AbstentionFinding(
            "instrument_economic_assessment", "evidence_quality_status",
            "every fund in the broad-market sleeve's own sealed instrument-economic-assessment "
            "cohort carries a disclosed partial evidence-quality status",
        ))
    return SUBSTANTIALLY_COMPUTED_WITH_DISCLOSED_GAPS, findings


def _compute_fund_gld_defensive_coverage(repo_root: Path) -> tuple[str, list[_AbstentionFinding]]:
    findings: list[_AbstentionFinding] = []
    etf = _load_dir_records(repo_root, "intelligence/etf_classification").get("GLD", {})
    if etf.get("evidence_quality_status") == "partial":
        findings.append(_AbstentionFinding(
            "etf_classification", "evidence_quality_status",
            "GLD's own sealed ETF-classification record carries a disclosed partial "
            "evidence-quality status",
        ))
    fd = _load_dir_records(repo_root, "intelligence/functional_doctrine").get("GLD_DEFENSIVE_ROLE", {})
    ear = fd.get("economic_assessment_readiness")
    if isinstance(ear, dict) and ear.get("status") == "assessment_required":
        findings.append(_AbstentionFinding(
            "functional_doctrine", "economic_assessment_readiness",
            "GLD_DEFENSIVE_ROLE's own sealed functional-doctrine record carries a forced "
            "assessment-required abstention on its economic-assessment readiness",
        ))
    ea = _load_dir_records(repo_root, "intelligence/economic_assessment").get("GLD", {})
    if ea.get("evidence_quality_status") == "partial":
        findings.append(_AbstentionFinding(
            "economic_assessment", "evidence_quality_status",
            "GLD's own sealed economic-assessment record carries a disclosed partial "
            "evidence-quality status",
        ))
    return SUBSTANTIALLY_COMPUTED_WITH_DISCLOSED_GAPS, findings


def _compute_crypto_coverage(repo_root: Path) -> tuple[str, list[_AbstentionFinding]]:
    findings: list[_AbstentionFinding] = []
    crypto = _load_dir_records(repo_root, "intelligence/crypto_classification")
    ccs = [
        t for t, r in crypto.items()
        if isinstance(r.get("correlation_and_volatility"), dict)
        and r["correlation_and_volatility"].get("cross_coin_correlation_status") == "not_yet_measured"
    ]
    if ccs and len(ccs) == len(crypto):
        findings.append(_AbstentionFinding(
            "crypto_classification", "correlation_and_volatility.cross_coin_correlation_status",
            "cross-coin correlation is forced not-yet-measured across the crypto sleeve's "
            "entire sealed classification corpus",
        ))
    iea = _load_dir_records(repo_root, "intelligence/instrument_economic_assessment")
    iea_scoped = {k: v for k, v in iea.items() if k in ("BTC", "ETH", "SOL")}
    drawdown_abstained = [
        t for t, r in iea_scoped.items()
        if isinstance(r.get("macro_behavioral_characterization"), dict)
        and isinstance(r["macro_behavioral_characterization"].get("historical_equity_market_drawdown_behavior"), dict)
        and r["macro_behavioral_characterization"]["historical_equity_market_drawdown_behavior"].get("behavior_category") == "unable_to_determine"
    ]
    for t in drawdown_abstained:
        findings.append(_AbstentionFinding(
            "instrument_economic_assessment",
            f"{t}.macro_behavioral_characterization.historical_equity_market_drawdown_behavior",
            "unable_to_determine",
        ))
    return SUBSTANTIALLY_COMPUTED_WITH_DISCLOSED_GAPS, findings


def _compute_cash_reserve_coverage(repo_root: Path) -> tuple[str, list[_AbstentionFinding]]:
    findings: list[_AbstentionFinding] = []
    fd = _load_dir_records(repo_root, "intelligence/functional_doctrine")
    for t in ("CASH", "RESERVE"):
        rec = fd.get(t, {})
        fr = rec.get("functional_role")
        if isinstance(fr, dict) and fr.get("role_category") == "unable_to_determine":
            findings.append(_AbstentionFinding("functional_doctrine", f"{t}.functional_role", "unable_to_determine"))
        ear = rec.get("economic_assessment_readiness")
        if isinstance(ear, dict) and ear.get("status") == "assessment_required":
            findings.append(_AbstentionFinding("functional_doctrine", f"{t}.economic_assessment_readiness", "assessment_required"))
    ea = _load_dir_records(repo_root, "intelligence/economic_assessment").get("CASH_LIKE_CAPITAL", {})
    if ea.get("evidence_quality_status") == "partial":
        findings.append(_AbstentionFinding(
            "economic_assessment", "evidence_quality_status",
            "CASH_LIKE_CAPITAL's own sealed economic-assessment record carries a disclosed "
            "partial evidence-quality status",
        ))
    return SUBSTANTIALLY_COMPUTED_WITH_DISCLOSED_GAPS, findings


def _compute_debt_reduction_coverage(repo_root: Path) -> tuple[str, list[_AbstentionFinding]]:
    fd = _load_dir_records(repo_root, "intelligence/functional_doctrine").get("DEBT_REDUCTION", {})
    ear = fd.get("economic_assessment_readiness")
    findings: list[_AbstentionFinding] = []
    if isinstance(ear, dict):
        for sub in ("avoided_borrowing_cost_readiness", "survivability_and_buffer_benefit_readiness"):
            if isinstance(ear.get(sub), dict) and ear[sub].get("status") == "assessment_required":
                findings.append(_AbstentionFinding("functional_doctrine", f"economic_assessment_readiness.{sub}", "assessment_required"))
    # debt_reduction carries no separate economic_assessment/<subject>.yaml
    # record at all (unlike fund_gld_defensive/cash_reserve) -- its entire
    # economic-assessment-equivalent layer is the functional_doctrine
    # record's own economic_assessment_readiness sub-object, and that
    # sub-object is forced-abstained on both required sub-fields, per
    # XASSET-0012 SS4.2's own named forced_abstention example.
    return FORCED_ABSTENTION, findings


_COVERAGE_FUNCTIONS = {
    EQUITY: _compute_equity_coverage,
    FUND_BROAD_MARKET: _compute_fund_broad_market_coverage,
    FUND_GLD_DEFENSIVE: _compute_fund_gld_defensive_coverage,
    CRYPTO: _compute_crypto_coverage,
    CASH_RESERVE: _compute_cash_reserve_coverage,
    DEBT_REDUCTION: _compute_debt_reduction_coverage,
}


def compute_live_evidence_coverage(sleeve_id: str, repo_root: Path) -> tuple[str, list[_AbstentionFinding]]:
    """Public, live, mechanically-derived evidence_coverage_profile plus
    abstention findings for a given sleeve, independent of any record's own
    declared content. Used both by this module's own validator and
    available for a future implementation to call directly."""
    fn = _COVERAGE_FUNCTIONS[sleeve_id]
    return fn(repo_root)


# ---------------------------------------------------------------------------
# Sleeve profile schema (XASSET-0012 SS4).
# ---------------------------------------------------------------------------

_PROFILE_TOP_LEVEL_REQUIRED = frozenset({
    "schema_version", "sleeve_id", "evidence_layer_references", "economic_role_summary",
    "evidence_coverage_profile", "functional_role_note", "abstention_index",
    "record_status", "sealed_at", "governing_decisions", "drafting_session_or_shard_id",
    "content_sha256", "cohort_manifest_entry",
})

_EVIDENCE_LAYER_REF_BASE_KEYS = frozenset({"layer_name", "module", "directory", "manifest_content_sha256", "as_of_note"})
_EVIDENCE_LAYER_REF_SCOPED_KEYS = _EVIDENCE_LAYER_REF_BASE_KEYS | {"sleeve_subject_scope"}

_SLEEVE_SUBJECT_SCOPE_KEYS = frozenset({"referenced_subject_ids", "referenced_record_content_sha256"})

_PROFILE_ABSTENTION_ENTRY_KEYS = frozenset({"source_layer", "field_path", "value", "reason"})

# Sleeves for which functional_role_note is required (non-null); every
# other sleeve must carry functional_role_note: null (XASSET-0012 SS4:
# "populated only for sleeves with a functional_doctrine or economic_
# assessment layer").
_FUNCTIONAL_ROLE_NOTE_REQUIRED_SLEEVES = frozenset({FUND_GLD_DEFENSIVE, CASH_RESERVE, DEBT_REDUCTION})


def _validate_sleeve_subject_scope(
    value: object, layer_name: str, sleeve_id: str, errors: list[str], *, repo_root: Path | None,
) -> None:
    label = f"evidence_layer_references[{layer_name}].sleeve_subject_scope"
    if not isinstance(value, dict):
        errors.append(f"{label} must be a mapping")
        return
    missing = _SLEEVE_SUBJECT_SCOPE_KEYS - value.keys()
    if missing:
        errors.append(f"{label} missing key(s): {sorted(missing)}")
        return
    _reject_unknown_keys(value, label, _SLEEVE_SUBJECT_SCOPE_KEYS, errors)

    expected = _expected_subjects(layer_name, sleeve_id)
    if expected is None:
        errors.append(f"{label} present but {layer_name!r} is not registered as shared for sleeve {sleeve_id!r}")
        return

    subjects = value.get("referenced_subject_ids")
    if not isinstance(subjects, list) or not all(isinstance(s, str) for s in subjects):
        errors.append(f"{label}.referenced_subject_ids must be a list of strings")
        return
    if sorted(subjects) != sorted(expected):
        errors.append(
            f"{label}.referenced_subject_ids must be exactly {sorted(expected)} for sleeve "
            f"{sleeve_id!r} on layer {layer_name!r} (XASSET-0012 SS2's own fixed sleeve-to-"
            f"subject mapping), got {sorted(subjects)}"
        )

    hashes = value.get("referenced_record_content_sha256")
    if not isinstance(hashes, dict):
        errors.append(f"{label}.referenced_record_content_sha256 must be a mapping")
        return
    if set(hashes.keys()) != set(subjects):
        errors.append(
            f"{label}.referenced_record_content_sha256 keys must exactly match "
            f"referenced_subject_ids {sorted(subjects)}, got {sorted(hashes.keys())}"
        )
    for subject_id, recorded_hash in hashes.items():
        if not _non_empty_str(recorded_hash):
            errors.append(f"{label}.referenced_record_content_sha256[{subject_id!r}] must be a non-empty string")
            continue
        if repo_root is None:
            continue
        directory = _LAYER_REGISTRY[layer_name]["directory"]
        manifest_path = repo_root / directory / "COHORT_MANIFEST.yaml"
        manifest_data, manifest_errs = _read_yaml(manifest_path)
        if manifest_errs or not isinstance(manifest_data, dict):
            errors.append(f"{label} could not verify manifest membership -- {manifest_path} unreadable")
            continue
        cohort = manifest_data.get("cohort")
        on_manifest = set()
        if isinstance(cohort, list):
            for row in cohort:
                if isinstance(row, dict):
                    on_manifest.update(v for v in row.values() if isinstance(v, str))
        if subject_id not in on_manifest:
            errors.append(
                f"{label}.referenced_subject_ids includes {subject_id!r}, which does not appear "
                f"in {directory}/COHORT_MANIFEST.yaml's own sealed cohort -- unknown subject"
            )
        record_path = repo_root / directory / f"{subject_id}.yaml"
        if not record_path.is_file():
            errors.append(f"{label} references missing record file {record_path}")
            continue
        record_data, record_errs = _read_yaml(record_path)
        if record_errs or not isinstance(record_data, dict):
            errors.append(f"{label} could not verify {record_path} -- unparseable")
            continue
        try:
            hash_fn = _get_layer_hash_fn(layer_name)
        except ImportError as exc:
            errors.append(f"{label} could not import hashing module for {layer_name!r}: {exc}")
            continue
        live_hash = hash_fn(record_data)
        if recorded_hash != live_hash:
            errors.append(
                f"{label}.referenced_record_content_sha256[{subject_id!r}] is stale -- "
                f"recorded {recorded_hash!r}, live-recomputed {live_hash!r} against the "
                f"current sealed {record_path} (never trusted from a stored value)"
            )


def _validate_evidence_layer_references(
    data: dict, errors: list[str], *, repo_root: Path | None,
) -> None:
    sleeve_id = data.get("sleeve_id")
    value = data.get("evidence_layer_references")
    if not isinstance(value, list) or not value:
        errors.append("evidence_layer_references must be a non-empty list")
        return
    if sleeve_id not in _SLEEVE_LAYERS:
        return  # sleeve_id itself already flagged elsewhere

    expected_layers = _SLEEVE_LAYERS[sleeve_id]
    seen_layers: list[str] = []
    for i, entry in enumerate(value):
        label = f"evidence_layer_references[{i}]"
        if not isinstance(entry, dict):
            errors.append(f"{label} must be a mapping")
            continue
        layer_name = entry.get("layer_name")
        if layer_name not in _LAYER_REGISTRY:
            errors.append(f"{label}.layer_name {layer_name!r} is not a recognized governed layer")
            continue
        seen_layers.append(layer_name)
        if layer_name not in expected_layers:
            errors.append(
                f"{label}.layer_name {layer_name!r} is not an authorized governed layer for "
                f"sleeve {sleeve_id!r} (XASSET-0012 SS2's own per-sleeve layer table)"
            )

        shared = _layer_is_shared(layer_name)
        allowed_keys = _EVIDENCE_LAYER_REF_SCOPED_KEYS if shared else _EVIDENCE_LAYER_REF_BASE_KEYS
        required_keys = _EVIDENCE_LAYER_REF_BASE_KEYS | ({"sleeve_subject_scope"} if shared else set())
        missing = required_keys - entry.keys()
        if missing:
            errors.append(f"{label} missing key(s): {sorted(missing)}")
        _reject_unknown_keys(entry, f"{label} (layer_name={layer_name!r})", allowed_keys, errors)

        if not shared and "sleeve_subject_scope" in entry:
            errors.append(
                f"{label}.sleeve_subject_scope is present but layer {layer_name!r} is not "
                f"shared across more than one sleeve for this synthesis -- forbidden "
                f"(XASSET-0012 SS4.1.1)"
            )
        elif shared:
            _validate_sleeve_subject_scope(entry.get("sleeve_subject_scope"), layer_name, sleeve_id, errors, repo_root=repo_root)

        expected_directory = _LAYER_REGISTRY[layer_name]["directory"]
        if entry.get("directory") != expected_directory:
            errors.append(f"{label}.directory must be {expected_directory!r}, got {entry.get('directory')!r}")
        expected_module = f"{_LAYER_REGISTRY[layer_name]['module']}.py"
        if entry.get("module") != expected_module:
            errors.append(f"{label}.module must be {expected_module!r}, got {entry.get('module')!r}")

        recorded_hash = entry.get("manifest_content_sha256")
        if not _non_empty_str(recorded_hash):
            errors.append(f"{label}.manifest_content_sha256 must be a non-empty string")
        elif repo_root is not None:
            manifest_path = repo_root / expected_directory / "COHORT_MANIFEST.yaml"
            manifest_data, manifest_errs = _read_yaml(manifest_path)
            if manifest_errs or not isinstance(manifest_data, dict):
                errors.append(f"{label} could not verify manifest hash -- {manifest_path} unreadable")
            else:
                live_hash = _hash_manifest_data(manifest_data)
                if recorded_hash != live_hash:
                    errors.append(
                        f"{label}.manifest_content_sha256 is stale -- recorded {recorded_hash!r}, "
                        f"live-recomputed {live_hash!r} against the current sealed "
                        f"{manifest_path} (never trusted from a stored value)"
                    )

        if not _non_empty_str(entry.get("as_of_note")):
            errors.append(f"{label}.as_of_note must be a non-empty string")
        else:
            _scan_free_text(entry["as_of_note"], f"{label}.as_of_note", errors, include_numeric=False, is_citation_field=True)

    if sorted(seen_layers) != sorted(expected_layers):
        errors.append(
            f"evidence_layer_references must cite exactly {sorted(expected_layers)} for sleeve "
            f"{sleeve_id!r}, got {sorted(seen_layers)}"
        )


def _validate_profile_abstention_index(data: dict, errors: list[str], *, repo_root: Path | None) -> None:
    value = data.get("abstention_index")
    if not isinstance(value, list):
        errors.append("abstention_index must be a list")
        return
    for i, entry in enumerate(value):
        label = f"abstention_index[{i}]"
        if not isinstance(entry, dict):
            errors.append(f"{label} must be a mapping")
            continue
        missing = _PROFILE_ABSTENTION_ENTRY_KEYS - entry.keys()
        if missing:
            errors.append(f"{label} missing key(s): {sorted(missing)}")
            continue
        _reject_unknown_keys(entry, label, _PROFILE_ABSTENTION_ENTRY_KEYS, errors)
        for k in ("source_layer", "field_path", "value", "reason"):
            if not _non_empty_str(entry.get(k)):
                errors.append(f"{label}.{k} must be a non-empty string")
        if _non_empty_str(entry.get("reason")):
            _scan_free_text(entry["reason"], f"{label}.reason", errors)

    sleeve_id = data.get("sleeve_id")
    if repo_root is None or sleeve_id not in _COVERAGE_FUNCTIONS:
        return
    live_coverage, live_findings = compute_live_evidence_coverage(sleeve_id, repo_root)

    declared_coverage = data.get("evidence_coverage_profile")
    if declared_coverage != live_coverage:
        errors.append(
            f"evidence_coverage_profile does not reproduce -- declared {declared_coverage!r}, "
            f"live-recomputed {live_coverage!r} from the sleeve's own currently sealed source "
            f"layers (XASSET-0012 SS4.2: never self-declared)"
        )

    declared_pairs = {
        (e.get("source_layer"), e.get("field_path"))
        for e in value if isinstance(e, dict)
    }
    live_pairs = {(f.source_layer, f.field_path) for f in live_findings}
    missing_from_index = live_pairs - declared_pairs
    if missing_from_index:
        errors.append(
            f"abstention_index is missing live-detected sub-field abstention(s): "
            f"{sorted(missing_from_index)} (XASSET-0012 SS4.2.1: a sub-field abstention must "
            f"never silently disappear behind a sealed parent record)"
        )
    extra_in_index = declared_pairs - live_pairs
    if extra_in_index:
        errors.append(
            f"abstention_index has entry/entries for field(s) that are not genuinely abstained "
            f"in the sleeve's own current source layers: {sorted(extra_in_index)}"
        )


def validate_sleeve_profile_data(
    data: object, expected_sleeve_id: str | None = None, *, repo_root: Path | None = None,
) -> list[str]:
    errors: list[str] = []
    if not isinstance(data, dict):
        return ["record must be a mapping"]

    missing = _PROFILE_TOP_LEVEL_REQUIRED - data.keys()
    if missing:
        errors.append(f"missing top-level key(s): {sorted(missing)}")
    _reject_unknown_keys(data, "<profile>", _PROFILE_TOP_LEVEL_REQUIRED, errors)
    _scan_key_names_recursive(data, "<profile>", errors)
    _scan_all_strings_for_contender_citation(data, "<profile>", errors)

    if data.get("schema_version") != SCHEMA_VERSION:
        errors.append(f"schema_version must be {SCHEMA_VERSION!r}, got {data.get('schema_version')!r}")

    sleeve_id = data.get("sleeve_id")
    if sleeve_id not in SLEEVE_IDS:
        errors.append(f"sleeve_id invalid: {sleeve_id!r}")
    elif expected_sleeve_id is not None and sleeve_id != expected_sleeve_id:
        errors.append(f"sleeve_id {sleeve_id!r} does not match filename-derived {expected_sleeve_id!r}")

    _validate_evidence_layer_references(data, errors, repo_root=repo_root)

    if not _non_empty_str(data.get("economic_role_summary")):
        errors.append("economic_role_summary must be a non-empty string")
    else:
        _scan_free_text(data["economic_role_summary"], "economic_role_summary", errors)

    coverage = data.get("evidence_coverage_profile")
    if coverage not in _EVIDENCE_COVERAGE_VALUES:
        errors.append(f"evidence_coverage_profile invalid: {coverage!r}")

    functional_role_note = data.get("functional_role_note")
    if sleeve_id in _FUNCTIONAL_ROLE_NOTE_REQUIRED_SLEEVES:
        if not _non_empty_str(functional_role_note):
            errors.append(f"functional_role_note must be a non-empty string for sleeve_id {sleeve_id!r}")
        else:
            _scan_free_text(functional_role_note, "functional_role_note", errors)
    elif functional_role_note is not None:
        errors.append(f"functional_role_note must be null for sleeve_id {sleeve_id!r}")

    _validate_profile_abstention_index(data, errors, repo_root=repo_root)

    if data.get("record_status") not in _LIFECYCLE_VALUES:
        errors.append(f"record_status invalid: {data.get('record_status')!r}")
    if not _non_empty_str(data.get("sealed_at")):
        errors.append("sealed_at must be a non-empty string")

    governing_decisions = data.get("governing_decisions")
    if governing_decisions != [_GOVERNING_DECISION]:
        errors.append(f"governing_decisions must be [{_GOVERNING_DECISION!r}], got {governing_decisions!r}")
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
            errors.append(f"content_sha256 does not reproduce -- recorded {recorded_hash!r}, recomputed {expected_hash!r}")

    return errors


def validate_sleeve_profile_file(path: Path, *, repo_root: Path | None = None) -> "ValidationResult":
    expected_sleeve_id = path.stem
    data, errors = _read_yaml(path)
    if errors:
        return ValidationResult(valid=False, errors=errors, source=str(path))
    errors = validate_sleeve_profile_data(data, expected_sleeve_id=expected_sleeve_id, repo_root=repo_root)
    return ValidationResult(valid=not errors, errors=errors, source=str(path))


# ---------------------------------------------------------------------------
# Sleeve relationship schema (XASSET-0012 SS5).
# ---------------------------------------------------------------------------

_RELATIONSHIP_TOP_LEVEL_REQUIRED = frozenset({
    "schema_version", "sleeve_pair", "profile_references", "primary_disposition",
    "favored_sleeve_id", "secondary_conditions", "overlap_dimension_references",
    "rationale", "abstention_index", "record_status", "sealed_at", "governing_decisions",
    "drafting_session_or_shard_id", "content_sha256", "cohort_manifest_entry",
})

_SLEEVE_PAIR_KEYS = frozenset({"sleeve_a", "sleeve_b"})
_PROFILE_REFERENCE_KEYS = frozenset({"sleeve_id", "referenced_content_sha256"})
_OVERLAP_DIMENSION_REF_KEYS = frozenset({"dimension_id", "referenced_content_sha256"})
_RELATIONSHIP_ABSTENTION_ENTRY_KEYS = frozenset({"field", "value", "reason"})


def _validate_sleeve_pair(data: dict, errors: list[str], *, expected_filename_stem: str | None) -> tuple[str | None, str | None]:
    value = data.get("sleeve_pair")
    if not isinstance(value, dict):
        errors.append("sleeve_pair must be a mapping")
        return None, None
    missing = _SLEEVE_PAIR_KEYS - value.keys()
    if missing:
        errors.append(f"sleeve_pair missing key(s): {sorted(missing)}")
        return None, None
    _reject_unknown_keys(value, "sleeve_pair", _SLEEVE_PAIR_KEYS, errors)
    a, b = value.get("sleeve_a"), value.get("sleeve_b")
    if a not in SLEEVE_IDS:
        errors.append(f"sleeve_pair.sleeve_a invalid: {a!r}")
    if b not in SLEEVE_IDS:
        errors.append(f"sleeve_pair.sleeve_b invalid: {b!r}")
    if isinstance(a, str) and isinstance(b, str):
        if a >= b:
            errors.append(f"sleeve_pair must be alphabetically ordered (sleeve_a < sleeve_b), got sleeve_a={a!r}, sleeve_b={b!r}")
        if (a, b) not in AUTHORIZED_RELATIONSHIP_PAIRS:
            errors.append(
                f"sleeve_pair ({a!r}, {b!r}) is not one of the seven XASSET-0013 SS C "
                f"authorized sleeve_relationship pairs"
            )
        if expected_filename_stem is not None and f"{a}_{b}" != expected_filename_stem:
            errors.append(f"sleeve_pair ({a!r}, {b!r}) does not match filename-derived stem {expected_filename_stem!r}")
    return (a if isinstance(a, str) else None), (b if isinstance(b, str) else None)


def _validate_profile_references(
    data: dict, sleeve_a: str | None, sleeve_b: str | None, errors: list[str], *, repo_root: Path | None,
) -> None:
    value = data.get("profile_references")
    if not isinstance(value, list) or len(value) != 2:
        errors.append("profile_references must be a list of exactly two entries")
        return
    seen_sleeves: set[str] = set()
    for i, entry in enumerate(value):
        label = f"profile_references[{i}]"
        if not isinstance(entry, dict):
            errors.append(f"{label} must be a mapping")
            continue
        missing = _PROFILE_REFERENCE_KEYS - entry.keys()
        if missing:
            errors.append(f"{label} missing key(s): {sorted(missing)}")
            continue
        _reject_unknown_keys(entry, label, _PROFILE_REFERENCE_KEYS, errors)
        sid = entry.get("sleeve_id")
        if sid not in {sleeve_a, sleeve_b}:
            errors.append(f"{label}.sleeve_id {sid!r} must be one of the pair's own two sleeve_id values")
            continue
        seen_sleeves.add(sid)
        recorded_hash = entry.get("referenced_content_sha256")
        if not _non_empty_str(recorded_hash):
            errors.append(f"{label}.referenced_content_sha256 must be a non-empty string")
            continue
        if repo_root is None:
            continue
        profile_path = repo_root / _PROFILES_DIR / f"{sid}.yaml"
        if not profile_path.is_file():
            errors.append(f"{label} references missing profile file {profile_path}")
            continue
        profile_data, profile_errs = _read_yaml(profile_path)
        if profile_errs or not isinstance(profile_data, dict):
            errors.append(f"{label} could not verify {profile_path} -- unparseable")
            continue
        live_hash = canonical_record_hash(profile_data)
        if recorded_hash != live_hash:
            errors.append(
                f"{label}.referenced_content_sha256 is stale -- recorded {recorded_hash!r}, "
                f"live-recomputed {live_hash!r} against the current sealed {profile_path} "
                f"(never trusted from a stored value)"
            )
    if seen_sleeves != {sleeve_a, sleeve_b} and sleeve_a is not None and sleeve_b is not None:
        errors.append(f"profile_references must cite exactly {{{sleeve_a!r}, {sleeve_b!r}}}, got {sorted(seen_sleeves)}")


def _live_profile(repo_root: Path | None, sleeve_id: str | None) -> dict | None:
    if repo_root is None or sleeve_id is None:
        return None
    path = repo_root / _PROFILES_DIR / f"{sleeve_id}.yaml"
    if not path.is_file():
        return None
    data, errs = _read_yaml(path)
    if errs or not isinstance(data, dict):
        return None
    return data


def _live_secondary_conditions(
    sleeve_a: str | None, sleeve_b: str | None, repo_root: Path | None,
    overlap_dimension_references: list,
) -> set[str] | None:
    """Live, mechanically-derived secondary_conditions -- never trusted
    from a stored value (XASSET-0012 SS9 item 6, applied to SS5.2)."""
    if repo_root is None:
        return None
    profile_a = _live_profile(repo_root, sleeve_a)
    profile_b = _live_profile(repo_root, sleeve_b)
    if profile_a is None or profile_b is None:
        return None
    live: set[str] = set()
    if profile_a.get("evidence_coverage_profile") != FULLY_COMPUTED or profile_b.get("evidence_coverage_profile") != FULLY_COMPUTED:
        live.add(EVIDENCE_PARTIAL_PRESENT)
    for p in (profile_a, profile_b):
        if p.get("evidence_coverage_profile") == FORCED_ABSTENTION:
            live.add(FORCED_ABSTENTION_PRESENT)
        ai = p.get("abstention_index")
        if isinstance(ai, list) and len(ai) > 0:
            live.add(FORCED_ABSTENTION_PRESENT)
    if isinstance(overlap_dimension_references, list) and len(overlap_dimension_references) > 0:
        live.add(OVERLAP_OR_DUPLICATION_DISCLOSED)
    return live


def _validate_overlap_dimension_references(
    data: dict, secondary_conditions: object, errors: list[str], *, repo_root: Path | None,
) -> None:
    value = data.get("overlap_dimension_references")
    if not isinstance(value, list):
        errors.append("overlap_dimension_references must be a list")
        return
    declared_secondary = secondary_conditions if isinstance(secondary_conditions, list) else []
    disclosed = OVERLAP_OR_DUPLICATION_DISCLOSED in declared_secondary
    if disclosed and not value:
        errors.append(
            "overlap_dimension_references must be non-empty when secondary_conditions "
            "includes overlap_or_duplication_disclosed"
        )
    if not disclosed and value:
        errors.append(
            "overlap_dimension_references must be empty when secondary_conditions does not "
            "include overlap_or_duplication_disclosed"
        )
    for i, entry in enumerate(value):
        label = f"overlap_dimension_references[{i}]"
        if not isinstance(entry, dict):
            errors.append(f"{label} must be a mapping")
            continue
        missing = _OVERLAP_DIMENSION_REF_KEYS - entry.keys()
        if missing:
            errors.append(f"{label} missing key(s): {sorted(missing)}")
            continue
        _reject_unknown_keys(entry, label, _OVERLAP_DIMENSION_REF_KEYS, errors)
        dim_id = entry.get("dimension_id")
        if not _non_empty_str(dim_id):
            errors.append(f"{label}.dimension_id must be a non-empty string")
            continue
        recorded_hash = entry.get("referenced_content_sha256")
        if not _non_empty_str(recorded_hash):
            errors.append(f"{label}.referenced_content_sha256 must be a non-empty string")
        if repo_root is None:
            continue
        dim_path = repo_root / _OVERLAP_MODEL_DIR / f"{dim_id}.yaml"
        if not dim_path.is_file():
            errors.append(f"{label} references missing overlap-model dimension file {dim_path}")
            continue
        dim_data, dim_errs = _read_yaml(dim_path)
        if dim_errs or not isinstance(dim_data, dict):
            errors.append(f"{label} could not verify {dim_path} -- unparseable")
            continue
        if dim_data.get("computation_status") != _COMPUTED_FROM_EXISTING_MECHANISM:
            errors.append(
                f"{label} cites dimension_id {dim_id!r}, whose own live computation_status is "
                f"{dim_data.get('computation_status')!r}, not {_COMPUTED_FROM_EXISTING_MECHANISM!r} -- "
                f"XASSET-0012 SS5.3: only computed_from_existing_mechanism dimensions may back an "
                f"overlap finding, a hard failure independent of the record's own secondary_conditions claim"
            )
        try:
            from overlap_model_validator import canonical_record_hash as _overlap_hash
        except ImportError as exc:
            errors.append(f"{label} could not import overlap_model_validator: {exc}")
            continue
        if _non_empty_str(recorded_hash):
            live_hash = _overlap_hash(dim_data)
            if recorded_hash != live_hash:
                errors.append(
                    f"{label}.referenced_content_sha256 is stale -- recorded {recorded_hash!r}, "
                    f"live-recomputed {live_hash!r} against the current sealed {dim_path}"
                )


def _validate_relationship_abstention_index(data: dict, errors: list[str]) -> None:
    value = data.get("abstention_index")
    if not isinstance(value, list):
        errors.append("abstention_index must be a list")
        return
    for i, entry in enumerate(value):
        label = f"abstention_index[{i}]"
        if not isinstance(entry, dict):
            errors.append(f"{label} must be a mapping")
            continue
        missing = _RELATIONSHIP_ABSTENTION_ENTRY_KEYS - entry.keys()
        if missing:
            errors.append(f"{label} missing key(s): {sorted(missing)}")
            continue
        _reject_unknown_keys(entry, label, _RELATIONSHIP_ABSTENTION_ENTRY_KEYS, errors)
        for k in ("field", "value", "reason"):
            if not _non_empty_str(entry.get(k)):
                errors.append(f"{label}.{k} must be a non-empty string")
        if _non_empty_str(entry.get("reason")):
            _scan_free_text(entry["reason"], f"{label}.reason", errors)

    primary = data.get("primary_disposition")
    has_primary_entry = any(
        isinstance(e, dict) and e.get("field") == "primary_disposition" and e.get("value") == RELATIONSHIP_ABSTENTION
        for e in value
    )
    if primary == RELATIONSHIP_ABSTENTION and not has_primary_entry:
        errors.append(
            "abstention_index must contain an entry with field='primary_disposition', "
            "value='unable_to_determine' when primary_disposition is the abstention value "
            "(XASSET-0012 SS5.1)"
        )
    if primary != RELATIONSHIP_ABSTENTION and has_primary_entry:
        errors.append(
            "abstention_index carries a primary_disposition abstention entry, but "
            "primary_disposition is not the abstention value -- not genuinely abstained"
        )


def validate_sleeve_relationship_data(
    data: object, expected_filename_stem: str | None = None, *, repo_root: Path | None = None,
) -> list[str]:
    errors: list[str] = []
    if not isinstance(data, dict):
        return ["record must be a mapping"]

    missing = _RELATIONSHIP_TOP_LEVEL_REQUIRED - data.keys()
    if missing:
        errors.append(f"missing top-level key(s): {sorted(missing)}")
    _reject_unknown_keys(data, "<relationship>", _RELATIONSHIP_TOP_LEVEL_REQUIRED, errors)
    _scan_key_names_recursive(data, "<relationship>", errors)
    _scan_all_strings_for_contender_citation(data, "<relationship>", errors)

    if data.get("schema_version") != SCHEMA_VERSION:
        errors.append(f"schema_version must be {SCHEMA_VERSION!r}, got {data.get('schema_version')!r}")

    sleeve_a, sleeve_b = _validate_sleeve_pair(data, errors, expected_filename_stem=expected_filename_stem)
    _validate_profile_references(data, sleeve_a, sleeve_b, errors, repo_root=repo_root)

    primary = data.get("primary_disposition")
    if primary not in _PRIMARY_DISPOSITION_VALUES:
        errors.append(f"primary_disposition invalid: {primary!r}")

    favored = data.get("favored_sleeve_id")
    if primary == STRONGER_EVIDENCE_MATURITY:
        if favored not in {sleeve_a, sleeve_b} or favored is None:
            errors.append(f"favored_sleeve_id must equal sleeve_a or sleeve_b when primary_disposition is stronger_evidence_maturity, got {favored!r}")
    elif favored is not None:
        errors.append(f"favored_sleeve_id must be null when primary_disposition is not stronger_evidence_maturity, got {favored!r}")

    secondary = data.get("secondary_conditions")
    if not isinstance(secondary, list) or len(secondary) != len(set(secondary)) or not set(secondary) <= _SECONDARY_CONDITION_VALUES:
        errors.append(f"secondary_conditions invalid: {secondary!r}")
    else:
        live = _live_secondary_conditions(sleeve_a, sleeve_b, repo_root, data.get("overlap_dimension_references") or [])
        if live is not None and set(secondary) != live:
            errors.append(
                f"secondary_conditions does not reproduce -- declared {sorted(secondary)}, "
                f"live-recomputed {sorted(live)} from the two cited profiles' own current state "
                f"(XASSET-0012 SS5.2/SS9 item 6: never self-declared)"
            )

    _validate_overlap_dimension_references(data, secondary, errors, repo_root=repo_root)

    if not _non_empty_str(data.get("rationale")):
        errors.append("rationale must be a non-empty string")
    else:
        _scan_free_text(data["rationale"], "rationale", errors)

    _validate_relationship_abstention_index(data, errors)

    if data.get("record_status") not in _LIFECYCLE_VALUES:
        errors.append(f"record_status invalid: {data.get('record_status')!r}")
    if not _non_empty_str(data.get("sealed_at")):
        errors.append("sealed_at must be a non-empty string")

    governing_decisions = data.get("governing_decisions")
    if governing_decisions != [_GOVERNING_DECISION]:
        errors.append(f"governing_decisions must be [{_GOVERNING_DECISION!r}], got {governing_decisions!r}")
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
            errors.append(f"content_sha256 does not reproduce -- recorded {recorded_hash!r}, recomputed {expected_hash!r}")

    return errors


def validate_sleeve_relationship_file(path: Path, *, repo_root: Path | None = None) -> "ValidationResult":
    expected_stem = path.stem
    data, errors = _read_yaml(path)
    if errors:
        return ValidationResult(valid=False, errors=errors, source=str(path))
    errors = validate_sleeve_relationship_data(data, expected_filename_stem=expected_stem, repo_root=repo_root)
    return ValidationResult(valid=not errors, errors=errors, source=str(path))


# ---------------------------------------------------------------------------
# Result dataclasses.
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


# ---------------------------------------------------------------------------
# Cohort manifest validation -- one for profiles, one for relationships.
# ---------------------------------------------------------------------------

_PROFILE_MANIFEST_ROW_KEYS = frozenset({
    "sleeve_id", "shard_id", "sealed_at", "content_sha256", "schema_version",
    "governing_decision", "record_path",
})
_RELATIONSHIP_MANIFEST_ROW_KEYS = frozenset({
    "sleeve_a", "sleeve_b", "shard_id", "sealed_at", "content_sha256", "schema_version",
    "governing_decision", "record_path",
})
_MANIFEST_TOP_KEYS = frozenset({"schema_version", "governing_decision", "cohort"})


def validate_profile_cohort_manifest(manifest_path: Path, records_dir: Path) -> ValidationResult:
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

    seen: set[str] = set()
    for i, row in enumerate(cohort):
        if not isinstance(row, dict):
            errors.append(f"cohort[{i}] must be a mapping")
            continue
        _reject_unknown_keys(row, f"cohort[{i}]", _PROFILE_MANIFEST_ROW_KEYS, errors)
        missing = _PROFILE_MANIFEST_ROW_KEYS - row.keys()
        if missing:
            errors.append(f"cohort[{i}] missing key(s): {sorted(missing)}")
            continue
        sleeve_id = row["sleeve_id"]
        if sleeve_id in seen:
            errors.append(f"cohort has duplicate sleeve_id: {sleeve_id!r}")
        seen.add(sleeve_id)

        expected_record_path = f"{_PROFILES_DIR}/{sleeve_id}.yaml"
        if row["record_path"] != expected_record_path:
            errors.append(f"cohort[{i}] ({sleeve_id!r}) record_path must be {expected_record_path!r}, got {row['record_path']!r}")

        record_path = records_dir / f"{sleeve_id}.yaml"
        if not record_path.is_file():
            errors.append(f"cohort[{i}] ({sleeve_id!r}) references missing record file {record_path}")
            continue
        record_data, record_read_errors = _read_yaml(record_path)
        if record_read_errors or not isinstance(record_data, dict):
            errors.append(f"cohort[{i}] ({sleeve_id!r}) record file could not be parsed")
            continue
        expected_hash = canonical_record_hash(record_data)
        if row["content_sha256"] != expected_hash:
            errors.append(f"cohort[{i}] ({sleeve_id!r}) content_sha256 mismatch -- manifest {row['content_sha256']!r}, recomputed {expected_hash!r}")
        if record_data.get("content_sha256") != row["content_sha256"]:
            errors.append(f"cohort[{i}] ({sleeve_id!r}) manifest content_sha256 does not match the record's own recorded content_sha256")

    missing_from_manifest = SLEEVE_IDS - seen
    extra_in_manifest = seen - SLEEVE_IDS
    if missing_from_manifest:
        errors.append(f"manifest missing authorized sleeve_id(s): {sorted(missing_from_manifest)}")
    if extra_in_manifest:
        errors.append(f"manifest has non-authorized sleeve_id(s): {sorted(extra_in_manifest)}")

    if records_dir.is_dir():
        on_disk = {p.stem for p in records_dir.glob("*.yaml") if p.name != "COHORT_MANIFEST.yaml"}
        orphans = on_disk - seen
        if orphans:
            errors.append(f"sealed record(s) on disk with no manifest entry: {sorted(orphans)}")

    return ValidationResult(valid=not errors, errors=errors, source=str(manifest_path))


def validate_relationship_cohort_manifest(manifest_path: Path, records_dir: Path) -> ValidationResult:
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

    seen: set[tuple[str, str]] = set()
    for i, row in enumerate(cohort):
        if not isinstance(row, dict):
            errors.append(f"cohort[{i}] must be a mapping")
            continue
        _reject_unknown_keys(row, f"cohort[{i}]", _RELATIONSHIP_MANIFEST_ROW_KEYS, errors)
        missing = _RELATIONSHIP_MANIFEST_ROW_KEYS - row.keys()
        if missing:
            errors.append(f"cohort[{i}] missing key(s): {sorted(missing)}")
            continue
        pair = (row["sleeve_a"], row["sleeve_b"])
        if pair in seen:
            errors.append(f"cohort has duplicate pair: {pair!r}")
        seen.add(pair)
        stem = f"{pair[0]}_{pair[1]}"

        expected_record_path = f"{_RELATIONSHIPS_DIR}/{stem}.yaml"
        if row["record_path"] != expected_record_path:
            errors.append(f"cohort[{i}] ({pair!r}) record_path must be {expected_record_path!r}, got {row['record_path']!r}")

        record_path = records_dir / f"{stem}.yaml"
        if not record_path.is_file():
            errors.append(f"cohort[{i}] ({pair!r}) references missing record file {record_path}")
            continue
        record_data, record_read_errors = _read_yaml(record_path)
        if record_read_errors or not isinstance(record_data, dict):
            errors.append(f"cohort[{i}] ({pair!r}) record file could not be parsed")
            continue
        expected_hash = canonical_record_hash(record_data)
        if row["content_sha256"] != expected_hash:
            errors.append(f"cohort[{i}] ({pair!r}) content_sha256 mismatch -- manifest {row['content_sha256']!r}, recomputed {expected_hash!r}")
        if record_data.get("content_sha256") != row["content_sha256"]:
            errors.append(f"cohort[{i}] ({pair!r}) manifest content_sha256 does not match the record's own recorded content_sha256")

    missing_from_manifest = set(AUTHORIZED_RELATIONSHIP_PAIRS) - seen
    extra_in_manifest = seen - set(AUTHORIZED_RELATIONSHIP_PAIRS)
    if missing_from_manifest:
        errors.append(f"manifest missing authorized pair(s): {sorted(missing_from_manifest)}")
    if extra_in_manifest:
        errors.append(f"manifest has non-authorized pair(s): {sorted(extra_in_manifest)}")

    if records_dir.is_dir():
        on_disk = {p.stem for p in records_dir.glob("*.yaml") if p.name != "COHORT_MANIFEST.yaml"}
        expected_stems = {f"{a}_{b}" for a, b in AUTHORIZED_RELATIONSHIP_PAIRS}
        seen_stems = {f"{a}_{b}" for a, b in seen}
        orphans = on_disk - seen_stems
        if orphans:
            errors.append(f"sealed record(s) on disk with no manifest entry: {sorted(orphans)}")

    return ValidationResult(valid=not errors, errors=errors, source=str(manifest_path))


# ---------------------------------------------------------------------------
# Directory validation.
# ---------------------------------------------------------------------------

def validate_sleeve_profile_directory(records_dir: Path, *, repo_root: Path | None = None) -> DirectoryValidationResult:
    results: list[ValidationResult] = []
    if not records_dir.is_dir():
        return DirectoryValidationResult(valid=True, results=[])

    for path in sorted(records_dir.glob("*.yaml")):
        if path.name == "COHORT_MANIFEST.yaml":
            continue
        results.append(validate_sleeve_profile_file(path, repo_root=repo_root))

    manifest_path = records_dir / "COHORT_MANIFEST.yaml"
    if manifest_path.is_file():
        results.append(validate_profile_cohort_manifest(manifest_path, records_dir))
    else:
        results.append(ValidationResult(valid=False, errors=["COHORT_MANIFEST.yaml is missing"], source=str(manifest_path)))

    on_disk = {p.stem for p in records_dir.glob("*.yaml") if p.name != "COHORT_MANIFEST.yaml"}
    missing = SLEEVE_IDS - on_disk
    extra = on_disk - SLEEVE_IDS
    pop_errors = []
    if missing:
        pop_errors.append(f"missing sealed record(s) for authorized sleeve_id(s): {sorted(missing)}")
    if extra:
        pop_errors.append(f"sealed record(s) for non-authorized sleeve_id(s): {sorted(extra)}")
    if pop_errors:
        results.append(ValidationResult(valid=False, errors=pop_errors, source="<population>"))

    return DirectoryValidationResult(valid=all(r.valid for r in results), results=results)


def validate_sleeve_relationship_directory(records_dir: Path, *, repo_root: Path | None = None) -> DirectoryValidationResult:
    results: list[ValidationResult] = []
    if not records_dir.is_dir():
        return DirectoryValidationResult(valid=True, results=[])

    for path in sorted(records_dir.glob("*.yaml")):
        if path.name == "COHORT_MANIFEST.yaml":
            continue
        results.append(validate_sleeve_relationship_file(path, repo_root=repo_root))

    manifest_path = records_dir / "COHORT_MANIFEST.yaml"
    if manifest_path.is_file():
        results.append(validate_relationship_cohort_manifest(manifest_path, records_dir))
    else:
        results.append(ValidationResult(valid=False, errors=["COHORT_MANIFEST.yaml is missing"], source=str(manifest_path)))

    on_disk = {p.stem for p in records_dir.glob("*.yaml") if p.name != "COHORT_MANIFEST.yaml"}
    expected_stems = {f"{a}_{b}" for a, b in AUTHORIZED_RELATIONSHIP_PAIRS}
    missing = expected_stems - on_disk
    extra = on_disk - expected_stems
    pop_errors = []
    if missing:
        pop_errors.append(f"missing sealed record(s) for authorized pair(s): {sorted(missing)}")
    if extra:
        pop_errors.append(f"sealed record(s) for non-authorized pair(s): {sorted(extra)}")
    if pop_errors:
        results.append(ValidationResult(valid=False, errors=pop_errors, source="<population>"))

    return DirectoryValidationResult(valid=all(r.valid for r in results), results=results)


if __name__ == "__main__":
    import sys

    _repo_root = Path(__file__).resolve().parent
    _profile_result = validate_sleeve_profile_directory(
        _repo_root / _PROFILES_DIR, repo_root=_repo_root,
    )
    _relationship_result = validate_sleeve_relationship_directory(
        _repo_root / _RELATIONSHIPS_DIR, repo_root=_repo_root,
    )
    _all_valid = _profile_result.valid and _relationship_result.valid
    if _all_valid:
        print(
            f"level1_sleeve_synthesis_validator: OK "
            f"({_profile_result.record_count} profile result(s), "
            f"{_relationship_result.record_count} relationship result(s))"
        )
        sys.exit(0)
    else:
        print("level1_sleeve_synthesis_validator: FAILED")
        for _r in (*_profile_result.results, *_relationship_result.results):
            if not _r.valid:
                for _err in _r.errors:
                    print(f"  - [{_r.source}] {_err}")
        sys.exit(1)
