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
    # Round-2 addition (independent post-push review, pullrequestreview on
    # PR #303): the original list stopped at "ten", missing eleven through
    # ninety-nine -- a real numeric-leakage gap, not exploited by any real
    # sealed content but present as a validator-completeness weakness.
    "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen",
    "seventeen", "eighteen", "nineteen", "twenty", "thirty", "forty",
    "fifty", "sixty", "seventy", "eighty", "ninety",
)
_CARDINAL_WORD_PATTERN = re.compile(r"\b(" + "|".join(_CARDINAL_WORDS) + r")\b", re.IGNORECASE)
# Note: a compound tens-plus-ones form ("twenty-one", "twenty one") is
# already caught by the tens word alone -- \btwenty\b matches "twenty" in
# "twenty-one" since a hyphen is a non-word character, so no separate
# compound pattern is needed.


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
    # Round-2 additions (independent post-push review, pullrequestreview on
    # PR #303): three further ordinary comparative-superiority idioms not
    # covered by the adjective+noun alternation or the standalone-verb
    # patterns above -- same closed-list-broadening discipline, not a new
    # mechanism.
    re.compile(r"\bhas\s+the\s+edge\s+over\b", re.IGNORECASE),
    re.compile(r"\bwins?\s+out\s+over\b", re.IGNORECASE),
    re.compile(r"\bthe\s+top\s+choice\s+among\b", re.IGNORECASE),
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
        # (?!\.yaml) guards against "excluded/removed from holdings.yaml" --
        # this repository's own central filename, a legitimate structural
        # citation ordinary sealed content is likely to make, which the
        # plain \b boundary alone does not distinguish from the portfolio-
        # membership verdict this pattern targets (found and fixed for the
        # sibling "remove...from holdings" round-5 pattern below, then
        # applied here to the identical pre-existing shape).
        r"\bexclud(e|es|ed|ing)\b(?:[\s,;:]+[a-z][\w'-]*){0,4}[\s,;:]+\bfrom\s+holdings\b(?!\.yaml)",
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
        # Round-4 additions (independent post-push review, pullrequestreview
        # on PR #303): three further ordinary paraphrases the round-3 scan
        # did not catch -- "has a place... going forward" (a softer, no-
        # "portfolio-noun-object" variant of the already-caught "merits/
        # deserves a place in the portfolio" family), a colon-shorthand
        # keep/go verdict shape (the direct sibling of the already-caught
        # "sleeve: in"/"sleeve is out" shorthand), and an explicit "no case
        # for keeping" negative-inclusion finding. Same closed-list-
        # broadening discipline as rounds 2/3, not a new mechanism.
        r"\bhas\s+a\s+place\s+in\s+the\s+portfolio\b",
        r"\b(cash\s+reserve|equity|crypto|fund\s+broad\s+market|fund\s+gld\s+defensive|debt\s+reduction)\s*:\s*keep\b",
        # Anchored to a sentence-final "should go" (an informal removal
        # verdict), not "should go through"/"should go on to"/etc, which
        # are legitimate process-continuation phrasing -- a real false-
        # positive risk the plain \b boundary alone would not exclude.
        r"\bthe\s+(cash\s+reserve|equity|crypto|fund\s+broad\s+market|fund\s+gld\s+defensive|debt\s+reduction)\s+sleeve\s+should\s+go(?=[.,;:]|\s*$)",
        r"\bno\s+case\s+for\s+keeping\b(?:[\s,;:]+[a-z][\w'-]*){0,4}[\s,;:]+\bin\s+the\s+portfolio\b",
        # Round-5 additions (independent post-push delta review, round 1 of
        # PR #303's second correction round): five further ordinary
        # paraphrases the round-4 scan did not catch -- "belongs among
        # portfolio holdings" (a different noun-object variant of the
        # already-caught "belongs in the portfolio"), "should stay in the
        # investable set" (the sibling of the already-caught "should
        # remain in the portfolio"), "ought to remain a holding" (a
        # holding-noun variant of the already-caught "ought to
        # be/remain... the portfolio" family), an explicit "remove... from
        # holdings" object (the sibling of the already-caught "exclude...
        # from holdings"/"remove... from the investable set"), and a
        # "should no longer be held" disposal verdict.
        r"\bbelongs?\s+among\s+portfolio\s+holdings\b",
        r"\bshould\s+stay\s+in\s+the\s+investable\s+set\b",
        r"\bought\s+to\s+remain\s+a\s+holding\b",
        # (?!\.yaml) guard -- see the round-3 "exclude...from holdings"
        # pattern's own matching comment above; this session's own
        # adversarial probe found the identical false-positive risk here
        # before this pattern was ever shipped.
        r"\bremov(e|es|ed|ing)\b(?:[\s,;:]+[a-z][\w'-]*){0,4}[\s,;:]+\bfrom\s+holdings\b(?!\.yaml)",
        r"\bshould\s+no\s+longer\s+be\s+held\b",
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
    # Same evidence layer, two further domains that independently carry
    # their own abstention_reason on a per-record basis (XASSET-0012
    # SS4.2.1: a governed sub-field abstention must never silently
    # disappear behind a sealed parent record -- these two domains were
    # not previously scanned here at all).
    segment_abstained = [
        t for t, r in evidence.items()
        if isinstance(r.get("segment_evidence"), dict) and r["segment_evidence"].get("abstention_reason")
    ]
    if segment_abstained:
        findings.append(_AbstentionFinding(
            "valuation_evidence", "segment_evidence",
            "a disclosed minority of the equity sleeve's own sealed valuation-evidence records "
            "carry a segment-evidence abstention rather than a fully populated segment breakdown, "
            "per that layer's own disclosed gap",
        ))
    market_observed_abstained = [
        t for t, r in evidence.items()
        if isinstance(r.get("market_observed_evidence"), dict) and r["market_observed_evidence"].get("abstention_reason")
    ]
    if market_observed_abstained:
        findings.append(_AbstentionFinding(
            "valuation_evidence", "market_observed_evidence",
            "a disclosed minority of the equity sleeve's own sealed valuation-evidence records "
            "carry a market-observed-evidence abstention rather than a fully populated market-price "
            "input, per that layer's own disclosed gap",
        ))
    # Same evidence layer, three further domains its own schema (valuation_
    # evidence_validator.py's own _FINANCIAL_EVIDENCE_ALLOWED_KEYS/_PEER_
    # SET_EVIDENCE_ALLOWED_KEYS/_SCENARIO_EVIDENCE_ALLOWED_KEYS) permits an
    # identical abstention_reason on, not previously scanned here -- closing
    # the class this domain's own schema defines, not merely the specific
    # domains a live record happened to already exercise.
    financial_abstained = [
        t for t, r in evidence.items()
        if isinstance(r.get("financial_evidence"), dict) and r["financial_evidence"].get("abstention_reason")
    ]
    if financial_abstained:
        findings.append(_AbstentionFinding(
            "valuation_evidence", "financial_evidence",
            "a disclosed minority of the equity sleeve's own sealed valuation-evidence records "
            "carry a financial-evidence abstention rather than a fully populated financial-statement "
            "history, per that layer's own disclosed gap",
        ))
    peer_set_abstained = [
        t for t, r in evidence.items()
        if isinstance(r.get("peer_set_evidence"), dict) and r["peer_set_evidence"].get("abstention_reason")
    ]
    if peer_set_abstained:
        findings.append(_AbstentionFinding(
            "valuation_evidence", "peer_set_evidence",
            "a disclosed minority of the equity sleeve's own sealed valuation-evidence records "
            "carry a peer-set-evidence abstention rather than a populated comparability candidate "
            "set, per that layer's own disclosed gap",
        ))
    scenario_abstained = [
        t for t, r in evidence.items()
        if isinstance(r.get("scenario_evidence"), dict) and r["scenario_evidence"].get("abstention_reason")
    ]
    if scenario_abstained:
        findings.append(_AbstentionFinding(
            "valuation_evidence", "scenario_evidence",
            "a disclosed minority of the equity sleeve's own sealed valuation-evidence records "
            "carry a scenario-evidence abstention rather than a populated scenario-variable basis, "
            "per that layer's own disclosed gap",
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
    # Same layer, the fund-scoped sibling abstention-capable field
    # (instrument_economic_assessment_validator.py's own
    # _COST_TRACKING_ALLOWED_KEYS/abstention_reason pairing on
    # cost_and_tracking_quality_economic_significance), not previously
    # scanned.
    cost_abstained = [
        t for t, r in iea_scoped.items()
        if isinstance(r.get("cost_and_tracking_quality_economic_significance"), dict)
        and r["cost_and_tracking_quality_economic_significance"].get("significance_category") == "unable_to_determine"
    ]
    for t in cost_abstained:
        findings.append(_AbstentionFinding(
            "instrument_economic_assessment",
            f"{t}.cost_and_tracking_quality_economic_significance",
            "unable_to_determine",
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
    # Three further functional_doctrine-schema abstention-capable fields,
    # not previously scanned for GLD_DEFENSIVE_ROLE -- same class as the
    # cash_reserve/debt_reduction extension above.
    fr = fd.get("functional_role")
    if isinstance(fr, dict) and fr.get("role_category") == "unable_to_determine":
        findings.append(_AbstentionFinding("functional_doctrine", "functional_role", "unable_to_determine"))
    lc = fd.get("liquidity_character")
    if isinstance(lc, dict) and lc.get("liquidity_category") == "unable_to_determine":
        findings.append(_AbstentionFinding("functional_doctrine", "liquidity_character", "unable_to_determine"))
    cp = fd.get("capital_preservation_character")
    if isinstance(cp, dict) and cp.get("capital_preservation_category") == "unable_to_determine":
        findings.append(_AbstentionFinding("functional_doctrine", "capital_preservation_character", "unable_to_determine"))
    fs = fd.get("freshness_state")
    if isinstance(fs, dict) and fs.get("status") == "unable_to_determine_freshness":
        findings.append(_AbstentionFinding("functional_doctrine", "freshness_state.status", "unable_to_determine_freshness"))
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
    # Same layer, the crypto-scoped sibling abstention-capable field
    # (instrument_economic_assessment_validator.py's own
    # _INFLATION_SENSITIVITY_VALUES/abstention_reason pairing on
    # macro_behavioral_characterization.historical_inflation_sensitivity_
    # narrative), not previously scanned.
    inflation_abstained = [
        t for t, r in iea_scoped.items()
        if isinstance(r.get("macro_behavioral_characterization"), dict)
        and isinstance(r["macro_behavioral_characterization"].get("historical_inflation_sensitivity_narrative"), dict)
        and r["macro_behavioral_characterization"]["historical_inflation_sensitivity_narrative"].get("sensitivity_category") == "unable_to_determine"
    ]
    for t in inflation_abstained:
        findings.append(_AbstentionFinding(
            "instrument_economic_assessment",
            f"{t}.macro_behavioral_characterization.historical_inflation_sensitivity_narrative",
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
        # Three further functional_doctrine-schema abstention-capable
        # fields (functional_doctrine_validator.py's own
        # _LIQUIDITY_CHARACTER_ALLOWED_KEYS/_CAPITAL_PRESERVATION_ALLOWED_
        # KEYS/_FRESHNESS_STATUS_VALUES), not previously scanned for
        # CASH/RESERVE.
        lc = rec.get("liquidity_character")
        if isinstance(lc, dict) and lc.get("liquidity_category") == "unable_to_determine":
            findings.append(_AbstentionFinding("functional_doctrine", f"{t}.liquidity_character", "unable_to_determine"))
        cp = rec.get("capital_preservation_character")
        if isinstance(cp, dict) and cp.get("capital_preservation_category") == "unable_to_determine":
            findings.append(_AbstentionFinding("functional_doctrine", f"{t}.capital_preservation_character", "unable_to_determine"))
        fs = rec.get("freshness_state")
        if isinstance(fs, dict) and fs.get("status") == "unable_to_determine_freshness":
            findings.append(_AbstentionFinding("functional_doctrine", f"{t}.freshness_state.status", "unable_to_determine_freshness"))
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
    fs = fd.get("freshness_state")
    if isinstance(fs, dict) and fs.get("status") == "unable_to_determine_freshness":
        findings.append(_AbstentionFinding("functional_doctrine", "freshness_state.status", "unable_to_determine_freshness"))
    # Three further functional_doctrine-schema abstention-capable fields,
    # not previously scanned for DEBT_REDUCTION -- same class as the
    # cash_reserve/fund_gld_defensive extension above.
    fr = fd.get("functional_role")
    if isinstance(fr, dict) and fr.get("role_category") == "unable_to_determine":
        findings.append(_AbstentionFinding("functional_doctrine", "functional_role", "unable_to_determine"))
    lc = fd.get("liquidity_character")
    if isinstance(lc, dict) and lc.get("liquidity_category") == "unable_to_determine":
        findings.append(_AbstentionFinding("functional_doctrine", "liquidity_character", "unable_to_determine"))
    cp = fd.get("capital_preservation_character")
    if isinstance(cp, dict) and cp.get("capital_preservation_category") == "unable_to_determine":
        findings.append(_AbstentionFinding("functional_doctrine", "capital_preservation_character", "unable_to_determine"))
    # debt_reduction carries no separate economic_assessment/<subject>.yaml
    # record at all (unlike fund_gld_defensive/cash_reserve) -- its entire
    # economic-assessment-equivalent layer is the functional_doctrine
    # record's own economic_assessment_readiness sub-object, and that
    # sub-object is forced-abstained on both required sub-fields, per
    # XASSET-0012 SS4.2's own named forced_abstention example. Its own
    # freshness_state sub-field is independently abstained too (SS4.2.1: a
    # sub-field abstention inside an otherwise-sealed source record must
    # never disappear behind this sleeve's own forced_abstention coverage
    # value) -- scanned here so it is never silently missed.
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


# =============================================================================
# STAGE 4 -- policy_adoption (XASSET-0014 Stage 4a policy-adoption
# methodology, XASSET-0015 Stage 4b content authorization). This section is
# a "clearly separated Stage 4 section of the existing
# level1_sleeve_synthesis_validator.py module" -- the implementing session's
# own choice, justified per XASSET-0014 SS G.O/SS21's own preamble deferral
# (mirroring XASSET-0006 SS A point 3's and XASSET-0013 SS K's identical
# deferral): the two record types already sharing this module (sleeve_
# profile, sleeve_relationship) and policy_adoption records are tightly
# coupled -- every policy_adoption record structurally references exactly
# one sleeve_profile record and every sleeve_relationship record naming its
# own sleeve, and reuses this module's own SLEEVE_IDS, AUTHORIZED_
# RELATIONSHIP_PAIRS, canonical_record_hash(), _read_yaml(), _reject_
# unknown_keys(), _prohibited_content_scan(), _numeric_leakage_scan(),
# _comparative_superiority_scan(), _scan_key_names_recursive(), _scan_
# contender_citation(), and _live_profile() helpers wholesale. Splitting
# this into a fourth sibling module would either duplicate all of that
# shared logic or force a cross-file import between two otherwise-sibling
# modules over the same six-sleeve/seven-relationship population -- the
# identical reasoning XASSET-0012's own module docstring already gives for
# combining sleeve_profile and sleeve_relationship in one file, extended
# here to the third, still more tightly coupled record type.
#
# Zero import relationship with allocate.py or margin_state.py in either
# direction -- unchanged from the rest of this module.
# =============================================================================

_POLICY_ADOPTION_DIR = "intelligence/level1_sleeve_synthesis/policy_adoption"

# XASSET-0014 SS3, closed three-value Axis A vocabulary.
FUNCTION_CONFIRMED_DISTINCT = "function_confirmed_distinct"
FUNCTION_STATUS_UNRESOLVED = "function_status_unresolved"
AXIS_A_UNABLE_TO_DETERMINE = "unable_to_determine"

_PORTFOLIO_FUNCTION_STATUS_VALUES = frozenset({
    FUNCTION_CONFIRMED_DISTINCT, FUNCTION_STATUS_UNRESOLVED, AXIS_A_UNABLE_TO_DETERMINE,
})

# XASSET-0014 SS4, closed two-value Axis B vocabulary -- no abstention value
# by design (SS4's own "a pure function of an already-fully-determined
# input needs none" reasoning).
ELIGIBLE_FOR_TARGET_CONSIDERATION = "eligible_for_target_consideration"
NOT_YET_ELIGIBLE = "not_yet_eligible"

_CAPITAL_ELIGIBILITY_VALUES = frozenset({ELIGIBLE_FOR_TARGET_CONSIDERATION, NOT_YET_ELIGIBLE})

# XASSET-0014 SS5, closed three-value Axis C vocabulary.
SIZING_READY = "sizing_ready"
SIZING_CONDITIONALLY_READY = "sizing_conditionally_ready"
SIZING_BLOCKED = "sizing_blocked"

_SIZING_READINESS_VALUES = frozenset({SIZING_READY, SIZING_CONDITIONALLY_READY, SIZING_BLOCKED})

# XASSET-0014 SS5.1, closed three-value relationship-coverage-ledger vocabulary.
SEALED_DETERMINED = "sealed_determined"
SEALED_UNRESOLVED = "sealed_unresolved"
DEFERRED_DISCLOSED = "deferred_disclosed"

_COVERAGE_STATE_VALUES = frozenset({SEALED_DETERMINED, SEALED_UNRESOLVED, DEFERRED_DISCLOSED})

# XASSET-0013 SS E's own closed, three-class deferred-pair vocabulary.
_DEFERRAL_CLASS_VALUES = frozenset({"class_1", "class_2", "class_3"})

# XASSET-0014 SS14/SS21's own closed blocking_evidence reason-type vocabulary
# -- "one entry per contributing reason (a failed axis, a specific unable_
# to_determine relationship, a specific secondary condition, a specific
# deferred pair)", mapped to five closed, machine-checkable tokens.
_BLOCKING_REASON_TYPES = frozenset({
    "axis_a_unresolved", "axis_b_not_eligible", "sealed_unresolved_relationship",
    "deferred_relationship_pair", "secondary_condition_present",
})

# XASSET-0014 SS3.2 Basis 3 -- XASSET-0012 SS2's own fixed sleeve-to-asset_
# class mapping table, reproduced here as a governance-document fact (never
# live-recomputed from any sealed Intelligence record -- only its own live
# targets.yaml existence is checked, per SS3.2's own "structurally
# independent of evidence maturity" design). A sleeve mapped to () has no
# targets.yaml row at all (debt_reduction) -- Basis 3 is unavailable for it,
# by construction, not by any live-derived fact.
_BASIS3_ASSET_CLASSES: dict[str, tuple[str, ...]] = {
    EQUITY: ("equity",),
    FUND_BROAD_MARKET: ("fund",),
    FUND_GLD_DEFENSIVE: ("fund",),
    CRYPTO: ("crypto",),
    CASH_RESERVE: ("cash", "reserve"),
    DEBT_REDUCTION: (),
}

# Basis 3 is additionally scoped to specific tickers for the two sleeves
# that share the "fund" asset_class (fund_broad_market: SPY/VEA/VWO;
# fund_gld_defensive: GLD) -- mirrors this module's own _LAYER_REGISTRY
# sleeve_subjects scoping for etf_classification (SS4.1.1), reused here for
# structural-basis scoping rather than invented fresh.
_BASIS3_TICKER_SCOPE: dict[str, tuple[str, ...] | None] = {
    EQUITY: None,
    FUND_BROAD_MARKET: ("SPY", "VEA", "VWO"),
    FUND_GLD_DEFENSIVE: ("GLD",),
    CRYPTO: None,
    CASH_RESERVE: None,
    DEBT_REDUCTION: None,
}

# XASSET-0013 SS E's own exact, closed eight-pair deferred-relationship set,
# by deferral class -- together with AUTHORIZED_RELATIONSHIP_PAIRS (the
# sealed seven), this is the complete, closed C(6,2) = 15-pair population
# with zero gap and zero overlap, independently asserted below.
DEFERRED_PAIRS: dict[tuple[str, str], str] = {
    (FUND_BROAD_MARKET, FUND_GLD_DEFENSIVE): "class_1",
    (CRYPTO, FUND_BROAD_MARKET): "class_1",
    (CASH_RESERVE, FUND_BROAD_MARKET): "class_1",
    (DEBT_REDUCTION, FUND_BROAD_MARKET): "class_1",
    (CASH_RESERVE, FUND_GLD_DEFENSIVE): "class_2",
    (DEBT_REDUCTION, FUND_GLD_DEFENSIVE): "class_2",
    (CASH_RESERVE, CRYPTO): "class_3",
    (CRYPTO, DEBT_REDUCTION): "class_3",
}
for _a, _b in DEFERRED_PAIRS:
    assert _a < _b, f"DEFERRED_PAIRS entry not alphabetical: {_a!r}, {_b!r}"
del _a, _b

_ALL_FIFTEEN_PAIRS = {
    (a, b)
    for a in sorted(SLEEVE_IDS)
    for b in sorted(SLEEVE_IDS)
    if a < b
}
assert len(_ALL_FIFTEEN_PAIRS) == 15, "C(6,2) must equal 15"
assert set(AUTHORIZED_RELATIONSHIP_PAIRS) & set(DEFERRED_PAIRS) == set(), (
    "sealed and deferred pairs must not overlap"
)
assert set(AUTHORIZED_RELATIONSHIP_PAIRS) | set(DEFERRED_PAIRS) == _ALL_FIFTEEN_PAIRS, (
    "sealed (7) + deferred (8) must account for the full closed 15-pair population with zero gap"
)


def _all_pairs_touching(sleeve_id: str) -> list[tuple[str, str]]:
    """The sleeve's own five possible pairs (sealed + deferred), sorted."""
    return sorted(p for p in _ALL_FIFTEEN_PAIRS if sleeve_id in p)


def _other_sleeve_in_pair(pair: tuple[str, str], sleeve_id: str) -> str:
    a, b = pair
    return b if a == sleeve_id else a


# -- Basis 1 (relationship-record finding) -----------------------------------

def compute_basis1_findings(
    sleeve_id: str, repo_root: Path | None, *,
    relationship_data: dict[tuple[str, str], dict] | None = None,
) -> list[tuple[tuple[str, str], str]]:
    """XASSET-0014 SS3.2 Basis 1 -- every sealed sleeve_relationship record
    naming sleeve_id whose own primary_disposition is role_preserving or
    coexistence_supported (never stronger_evidence_maturity, by
    construction -- SS6). Reads primary_disposition only, NEVER favored_
    sleeve_id -- trivially immune to a favored_sleeve_id-masking transform,
    the structural guarantee behind the SS6/SS21 item 5 counterfactual-
    masking non-influence proof.

    relationship_data, when supplied, overrides live disk reads with an
    in-memory dict[pair] -> parsed record data -- used only by the
    counterfactual-masking / presence-independent regression-guard test
    harness (SS21 items 5/24), never by ordinary validation, which always
    reads live from repo_root."""
    findings: list[tuple[tuple[str, str], str]] = []
    for pair in AUTHORIZED_RELATIONSHIP_PAIRS:
        if sleeve_id not in pair:
            continue
        if relationship_data is not None:
            data = relationship_data.get(pair)
        elif repo_root is not None:
            a, b = pair
            data, err = _read_yaml(repo_root / _RELATIONSHIPS_DIR / f"{a}_{b}.yaml")
            if err or not isinstance(data, dict):
                data = None
        else:
            data = None
        if not isinstance(data, dict):
            continue
        disposition = data.get("primary_disposition")
        if disposition in (ROLE_PRESERVING, COEXISTENCE_SUPPORTED):
            findings.append((pair, disposition))
    return findings


# -- Basis 3 (structural sleeve-definition basis) -----------------------------

def compute_basis3_available(sleeve_id: str, repo_root: Path | None) -> bool:
    """XASSET-0014 SS3.2 Basis 3 -- a purely structural, categorical,
    mechanically-checkable existence check against the live targets.yaml
    destination list, scoped to this sleeve's own fixed asset_class/ticker
    mapping (never an individual destination row's own target_pct, weight,
    or rank). Reads NO sleeve_relationship record of any kind -- trivially
    immune to a favored_sleeve_id-masking transform by construction, since
    the function signature does not even accept relationship data."""
    classes = _BASIS3_ASSET_CLASSES.get(sleeve_id, ())
    if not classes or repo_root is None:
        return False
    data, err = _read_yaml(repo_root / "targets.yaml")
    if err or not isinstance(data, dict):
        return False
    destinations = data.get("destination")
    if not isinstance(destinations, list):
        return False
    scope = _BASIS3_TICKER_SCOPE.get(sleeve_id)
    for row in destinations:
        if not isinstance(row, dict):
            continue
        if row.get("asset_class") not in classes:
            continue
        if scope is not None and row.get("ticker") not in scope:
            continue
        return True
    return False


# -- Axis B (mechanical, zero drafting discretion) ----------------------------

def compute_axis_b(evidence_coverage_profile: object) -> str | None:
    """XASSET-0014 SS4 -- a pure, total function of evidence_coverage_
    profile. Returns None only if the input itself is not one of the four
    closed evidence_coverage_profile values (a hard schema failure
    upstream, never silently mapped to a default)."""
    if evidence_coverage_profile in (FULLY_COMPUTED, SUBSTANTIALLY_COMPUTED_WITH_DISCLOSED_GAPS):
        return ELIGIBLE_FOR_TARGET_CONSIDERATION
    if evidence_coverage_profile in (MATERIALLY_INCOMPLETE, FORCED_ABSTENTION):
        return NOT_YET_ELIGIBLE
    return None


# -- Relationship-coverage ledger (Axis C input, SS5.1) -----------------------

@dataclass(frozen=True)
class _LedgerEntry:
    other_sleeve_id: str
    pair: tuple[str, str]
    coverage_state: str
    deferral_class: str | None
    primary_disposition: str | None
    has_secondary_conditions: bool


def compute_live_relationship_ledger(
    sleeve_id: str, repo_root: Path | None, *,
    relationship_data: dict[tuple[str, str], dict] | None = None,
) -> list[_LedgerEntry]:
    """XASSET-0014 SS5.1 -- the sleeve's own exactly-five-pair coverage
    ledger, mechanically cross-referenced against the closed sealed-seven /
    deferred-eight population (never a sixth coverage state, never a pair
    outside that closed 15-pair set -- DEFERRED_PAIRS/AUTHORIZED_
    RELATIONSHIP_PAIRS's own module-load-time assertions already guarantee
    there is no such pair to encounter)."""
    entries: list[_LedgerEntry] = []
    for pair in _all_pairs_touching(sleeve_id):
        other = _other_sleeve_in_pair(pair, sleeve_id)
        if pair in DEFERRED_PAIRS:
            entries.append(_LedgerEntry(
                other_sleeve_id=other, pair=pair, coverage_state=DEFERRED_DISCLOSED,
                deferral_class=DEFERRED_PAIRS[pair], primary_disposition=None,
                has_secondary_conditions=False,
            ))
            continue
        # pair in AUTHORIZED_RELATIONSHIP_PAIRS (the module-load-time
        # assertions above guarantee no third possibility exists).
        if relationship_data is not None:
            data = relationship_data.get(pair)
        elif repo_root is not None:
            a, b = pair
            data, err = _read_yaml(repo_root / _RELATIONSHIPS_DIR / f"{a}_{b}.yaml")
            if err or not isinstance(data, dict):
                data = None
        else:
            data = None
        if not isinstance(data, dict):
            entries.append(_LedgerEntry(
                other_sleeve_id=other, pair=pair, coverage_state=SEALED_DETERMINED,
                deferral_class=None, primary_disposition=None, has_secondary_conditions=False,
            ))
            continue
        disposition = data.get("primary_disposition")
        secondary = data.get("secondary_conditions")
        has_secondary = isinstance(secondary, list) and len(secondary) > 0
        state = SEALED_UNRESOLVED if disposition == RELATIONSHIP_ABSTENTION else SEALED_DETERMINED
        entries.append(_LedgerEntry(
            other_sleeve_id=other, pair=pair, coverage_state=state,
            deferral_class=None, primary_disposition=disposition,
            has_secondary_conditions=has_secondary,
        ))
    return entries


def compute_expected_sizing_readiness(
    axis_a: str | None, axis_b: str | None, ledger: list[_LedgerEntry],
) -> str:
    """XASSET-0014 SS5's own three-way mechanical rule, exactly as
    corrected by SS5.1, including the closed-vocabulary partition this
    module treats as internally coherent (SS22 Case A: a sleeve with zero
    deferred_disclosed pairs but at least one sealed_determined pair
    carrying a disclosed secondary_conditions entry lands on sizing_
    conditionally_ready, never sizing_ready -- a secondary condition on an
    otherwise-fully-sealed ledger is itself one of sizing_conditionally_
    ready's own three named triggering conditions, per SS5 point 2, so
    sizing_ready's own point-1 conjunction is read as requiring, in
    addition to its own explicitly stated four conditions, that no
    sizing_conditionally_ready trigger condition is independently present
    -- the only reading that makes the three-value vocabulary a coherent
    partition rather than an overlapping ambiguity)."""
    if axis_a != FUNCTION_CONFIRMED_DISTINCT or axis_b != ELIGIBLE_FOR_TARGET_CONSIDERATION:
        return SIZING_BLOCKED
    if any(e.coverage_state == SEALED_UNRESOLVED for e in ledger):
        return SIZING_BLOCKED
    if any(e.coverage_state == DEFERRED_DISCLOSED for e in ledger):
        return SIZING_CONDITIONALLY_READY
    if any(e.coverage_state == SEALED_DETERMINED and e.has_secondary_conditions for e in ledger):
        return SIZING_CONDITIONALLY_READY
    return SIZING_READY


# -- Stage 4's own materially separate scans ----------------------------------
#
# XASSET-0014 SS21 item 13 -- "Stage 4's own bounded-conclusion scan,
# materially different from Stage 1-3's SS8.1 blanket eligibility-language
# ban": Stage 4's schema is explicitly designed to represent a bounded,
# closed-vocabulary role/eligibility/readiness judgment (unlike Stage 1-3,
# which decides no eligibility at all), so _eligibility_language_scan()
# above is deliberately NOT reused against Stage 4 free text -- doing so
# would make this schema's own boundary-disclosure prose ("this sleeve
# remains eligible for target consideration") unusable in its own required
# rationale fields. What remains barred, even in Stage 4 free text: (a) any
# numeric magnitude (SS21 item 7, reused via _numeric_leakage_scan); (b)
# trade/execution-directive language or a claim that a Stage 4 finding
# alone triggers deployment/an allocation check/Level 2 selection; (c) free
# text asserting a conclusion stronger than the record's own populated
# closed-vocabulary fields support (a fabricated fourth Axis A value, a
# permanent/irrevocable framing contradicting SS7's "never a permanent
# lock" rule); (d) individual-instrument eligibility or target-weight
# leakage (the Level 1/Level 2 boundary, SS12/SS21 item 9).

# MINOR-4 correction (independent exact-head review pullrequestreview-
# 4911497398): the original list caught only the forward word order
# ("X triggers an allocation check") and only the qualified adjective
# forms ("fully redundant", "fully subsumed by", "permanently"), missing
# passive/reversed word order ("an allocation check is triggered by X")
# and the bare, unqualified adjective forms ("this determination is
# permanent", "this sleeve is redundant"). Both gaps are closed below
# without weakening or removing any existing pattern -- purely additive.
# The bare "\bis\s+permanent\b"/"\bis\s+redundant\b" additions are
# deliberately narrower than a bare "\bpermanent\b"/"\bredundant\b" scan
# would be: this module's own real sealed corpus and test suite both rely
# on legitimate, boundary-preserving disclosure language that contains
# the bare word without asserting it ("never a permanent lock -- a future
# re-population would recompute this from scratch", SS7's own explicit
# rule) -- a bare-word scan would flag that disclosure itself as an
# overclaim, which is exactly backwards. Requiring the assertive verb
# ("is permanent"/"is redundant") immediately adjacent keeps the existing
# TestBoundedConclusionScan.test_never_a_permanent_lock_disclosure_
# language_passes false-positive guard clean while still catching the
# review's own literal bypass example.
_STAGE4_OVERCLAIM_PATTERNS = [
    re.compile(p, re.IGNORECASE)
    for p in [
        r"\bpermanently\b",
        r"\birrevocable\b",
        r"\birrevocably\b",
        r"\blocked\s+in\b",
        r"\bfixed\s+forever\b",
        r"\bcan\s*not\s+(be\s+)?(revisited|reopened|reconsidered|changed)\b",
        r"\bcannot\s+(be\s+)?(revisited|reopened|reconsidered|changed)\b",
        r"\bfully\s+(redundant|subsumed\s+by|replaced\s+by)\b",
        r"\bis\s+redundant\s+with\b",
        r"\btriggers?\s+(an?\s+)?(allocation\s+check|deployment|level\s*2\s+(instrument\s+)?selection)\b",
        r"\bautomatically\s+(deploys?|allocates?|triggers?)\b",
        r"\bthis\s+(finding|record)\s+alone\s+(triggers?|authorizes?|deploys?)\b",
        # -- MINOR-4 additions ------------------------------------------
        r"\b(allocation\s+check|deployment|level\s*2\s+(instrument\s+)?selection)\s+(is|was|gets?|remains?)\s+triggered\s+by\b",
        r"\btriggered\s+by\s+(this\s+)?(sleeve|finding|record)('s)?\s+own\s+finding\s+alone\b",
        r"\bis\s+permanent\b",
        r"\bis\s+redundant\b",
        r"\bsubsumed\s+by\b",
        # -- NEW-MINOR-B additions (independent exact-head delta review
        # pullrequestreview-4912431420): four further real bypasses of
        # the MINOR-4 fix immediately above, each its own distinct verb-
        # form/construction gap, none a redesign of the scan's own
        # bounded phrase-based mechanism.
        #
        # (1) "The sleeve remains redundant."/"The sleeve has been
        # subsumed." -- MINOR-4's own bare-adjective additions
        # ("is permanent"/"is redundant") and the original "subsumed by"
        # pattern both required a specific single verb form ("is", or a
        # trailing "by" clause). Broadened to the SAME closed verb
        # alternation already used two patterns above for the passive
        # allocation-trigger ban ((?:is|was|gets?|remains?)), applied
        # uniformly to permanent/redundant/subsumed together, and made
        # "subsumed" catchable without a trailing "by" clause at all.
        # Additive, not a replacement of the bare MINOR-4 patterns above
        # (which stay, for a stable diff and because narrower patterns
        # matching a subset of this one are harmless).
        r"\b(?:is|was|has\s+been|have\s+been|gets?|remains?)\s+(?:permanent|redundant|subsumed)\b",
        # (2) "An allocation check would be triggered solely by this
        # result." -- MINOR-4's own reversed-order pattern required
        # exactly one of (is|was|gets?|remains?) as the passive verb and
        # "triggered by" with nothing intervening. Neither "would be"/
        # "could be"/"can be" (a materially different, equally passive
        # verb form) nor an adverb between "triggered" and "by" ("solely
        # by", "exclusively by", "entirely by") was covered. Both gaps
        # closed together in one broadened pattern -- not a second,
        # duplicated pattern -- since they are independent axes of the
        # same construction and commonly co-occur in real prose.
        r"\b(allocation\s+check|deployment|level\s*2\s+(instrument\s+)?selection)\s+"
        r"(?:is|was|gets?|remains?|would\s+be|could\s+be|can\s+be)\s+triggered\s+"
        r"(?:solely\s+|exclusively\s+|entirely\s+)?by\b",
        # (3) "This result by itself is enough to trigger allocation
        # checking." -- an entirely different construction from every
        # existing "triggers"/"is triggered by" pattern above (no verb
        # "trigger" governs a noun directly; "is enough to trigger" is
        # itself the overclaim, regardless of what follows), so no
        # broadening of an existing pattern could reach it. Bounded to
        # this closed phrase, matching this scan's own established
        # phrase-list design (e.g. the pre-existing bare "automatically
        # (deploys?|allocates?|triggers?)" pattern, which likewise does
        # not require a specific following noun).
        r"\bis\s+enough\s+to\s+trigger\b",
        r"\bsufficient\s+(?:on\s+its\s+own|by\s+itself|alone)\s+to\s+trigger\b",
    ]
]

# MINOR-3 correction (independent exact-head review pullrequestreview-
# 4911497398): three real, independently reproduced gaps, all fixed
# without redesigning the scan's own bounded, phrase-based mechanism.
#
# (1) The ticker word-boundary construction \b{ticker}\b'?s? was broken:
# \b{ticker}\b requires a word boundary IMMEDIATELY after the ticker's own
# letters, so it never matches inside a no-apostrophe plural like "SPYs"
# (no boundary exists between "Y" and the following "s" -- both are word
# characters). Fixed by moving the optional possessive/plural suffix
# INSIDE the boundary group -- \b{ticker}(?:'s|s)?\b -- so "SPY", "SPY's",
# and "SPYs" are all recognized as the same ticker mention.
#
# (2) The trigger-word list was noun-only (weight/target percentage/own
# size/own allocation), missing verb forms ("SPY is weighted at...",
# "SPY should be allocated more capital") and bare comparative-capital
# phrasing ("BTC warrants more capital"). Broadened to a trigger
# alternation covering weight/weighted/weighting, target percentage/
# weight, own size/allocation, allocate/allocated/allocating/allocation,
# size/sized/sizing, and "more/less/greater/smaller/larger/higher/lower/
# fewer capital" -- still a closed, bounded phrase list, not a redesign.
#
# (3) The ticker population (_STAGE4_LEVEL2_TICKERS, the seven fund/
# crypto instruments) under-covered relative to this module's own
# docstring claim ("no individual equity ticker, fund, or coin symbol")
# and, more importantly, XASSET-0014 SS F's own controlling text: "no
# individual equity, fund, or coin's own weight, target, or size may be
# named by any Stage 4 record" -- equities are explicitly, textually in
# scope, not only the seven fund/crypto instruments. Mechanically
# extended via _stage4_level2_ticker_universe() below, which unions the
# static seven with the live canonical equity roster read directly from
# targets.yaml's own destination: list (mirroring compute_basis3_
# available()'s own established direct-targets.yaml-read convention in
# this same file, rather than hand-maintaining a second, duplicated
# ticker list or adding this module's first cross-validator import for
# one field lookup). A comparative cross-ticker pattern is added
# separately below to catch ticker-vs-ticker sizing claims that use no
# fixed trigger noun at all ("SPY should be sized larger than VEA," "BTC
# warrants more capital than ETH").
_STAGE4_LEVEL2_TICKERS = ("SPY", "VEA", "VWO", "GLD", "BTC", "ETH", "SOL")

_STAGE4_LEVEL2_TRIGGER_ALTERNATION = (
    r"weight(?:ed|ing)?|"
    r"target\s+(?:percentage|weight)|"
    r"own\s+(?:size|allocation)|"
    r"alloca(?:te|ted|ting|tion)|"
    r"siz(?:e|ed|ing)|"
    r"(?:more|less|greater|smaller|larger|higher|lower|fewer)\s+capital"
)
_STAGE4_LEVEL2_COMPARATIVE_WORD = r"(?:more|less|greater|smaller|larger|higher|lower|fewer)"
_STAGE4_LEVEL2_COMPARATIVE_NOUN = r"(?:capital|weight|allocation|size|shares?)"


def _stage4_level2_ticker_universe(repo_root: Path | None) -> tuple[str, ...]:
    """The seven fund/crypto Level 2 instruments unioned with the live
    canonical equity roster (targets.yaml's own destination: list, rows
    with asset_class == 'equity') -- see the MINOR-3 correction comment
    above for why. Falls back to the static seven alone when repo_root is
    unavailable (an isolated synthetic-data test with no real
    targets.yaml to read) -- a narrower, never a wider, fallback, so no
    existing caller silently gains equity-ticker coverage it did not ask
    for."""
    tickers = set(_STAGE4_LEVEL2_TICKERS)
    if repo_root is not None:
        data, errs = _read_yaml(repo_root / "targets.yaml")
        if not errs and isinstance(data, dict):
            destinations = data.get("destination")
            if isinstance(destinations, list):
                for row in destinations:
                    if (
                        isinstance(row, dict)
                        and row.get("asset_class") == "equity"
                        and isinstance(row.get("ticker"), str)
                    ):
                        tickers.add(row["ticker"])
    return tuple(sorted(tickers))


def _stage4_level2_weight_patterns(repo_root: Path | None) -> list["re.Pattern[str]"]:
    tickers = _stage4_level2_ticker_universe(repo_root)
    patterns = [
        re.compile(
            # \b{ticker}(?:'s|s)?\b -- the boundary now wraps the whole
            # optional possessive/plural suffix (see correction comment
            # above), matching "SPY", "SPY's own weight", and "SPYs
            # weight" alike.
            rf"\b{re.escape(ticker)}(?:'s|s)?\b(?:[\s,;:]+[a-z][\w'-]*){{0,4}}[\s,;:]+\b(?:{_STAGE4_LEVEL2_TRIGGER_ALTERNATION})\b",
            re.IGNORECASE,
        )
        for ticker in tickers
    ]
    if tickers:
        ticker_alt = "|".join(re.escape(t) for t in tickers)
        patterns.append(re.compile(
            rf"\b(?:{ticker_alt})(?:'s|s)?\b[^.]{{0,60}}\b{_STAGE4_LEVEL2_COMPARATIVE_WORD}\b"
            rf"[^.]{{0,40}}\b{_STAGE4_LEVEL2_COMPARATIVE_NOUN}\b[^.]{{0,40}}\bthan\b[^.]{{0,30}}"
            rf"\b(?:{ticker_alt})(?:'s|s)?\b",
            re.IGNORECASE,
        ))
        # NEW-MINOR-B addition (independent exact-head delta review
        # pullrequestreview-4912431420): the pattern immediately above
        # only recognizes TICKER-FIRST ordering ({ticker} ... comparative
        # ... noun ... than ... {ticker}). Two real bypasses use the
        # inverted, passive construction instead -- the comparative
        # phrase precedes the first ticker mention entirely ("More
        # capital should be allocated to SPY than VEA", "A larger weight
        # is assigned to BTC than ETH") -- neither ticker ever appears
        # before the comparative word, so the ticker-first pattern above
        # never even reaches its own anchor. A materially different word
        # order, not a broadening of the existing pattern: comparative
        # word, then comparative noun, then a preposition ("to"/"for")
        # introducing the first ticker, then "than", then the second
        # ticker.
        patterns.append(re.compile(
            rf"\b{_STAGE4_LEVEL2_COMPARATIVE_WORD}\b[^.]{{0,40}}\b{_STAGE4_LEVEL2_COMPARATIVE_NOUN}\b"
            rf"[^.]{{0,40}}\b(?:to|for)\b[^.]{{0,30}}\b(?:{ticker_alt})(?:'s|s)?\b[^.]{{0,30}}\bthan\b"
            rf"[^.]{{0,30}}\b(?:{ticker_alt})(?:'s|s)?\b",
            re.IGNORECASE,
        ))
    return patterns


# MINOR-5 correction (independent exact-head review pullrequestreview-
# 4911497398): compiled without re.IGNORECASE, unlike every sibling
# pattern list in this module -- "this mentions qqq only" (lowercase, no
# uppercase occurrence anywhere) passed the scan undetected. Added for
# consistency with _CONTENDER_CITATION_PATTERNS/_POLICY_LEAK_PATTERNS/
# every other pattern list here.
_STAGE4_QQQ_PATTERN = re.compile(r"\bQQQ\b", re.IGNORECASE)

# XASSET-0014 SS21 item 21 -- a Basis 3 citation referencing evidence-
# maturity or per-instrument-weight fields is a hard rejection, never a
# drafting judgment call; distinct from (and in addition to) the general
# policy-leak scan's own bare "target_pct"/"targets.yaml" patterns.
# Deliberately scoped to function_rationale ONLY (the one field where a
# Basis 1/2/3 citation is actually made) -- NOT part of the general
# _stage4_bounded_conclusion_scan()/_scan_stage4_free_text() wrapper,
# since evidence_coverage_profile is also the exact, legitimately-required
# vocabulary blocking_evidence[] must use to disclose an Axis B failure
# (SS14's own field-design comment) -- applying this ban universally would
# make that mandatory disclosure impossible to write.
_STAGE4_BASIS3_FORBIDDEN_FIELD_PATTERNS = [
    re.compile(p, re.IGNORECASE)
    for p in (r"\bevidence_coverage_profile\b", r"\bfavored_sleeve_id\b")
]


def _scan_basis3_forbidden_fields(text: str) -> list[str]:
    findings: list[str] = []
    for pat in _STAGE4_BASIS3_FORBIDDEN_FIELD_PATTERNS:
        if pat.search(text):
            findings.append(f"stage4-basis3-forbidden-field:{pat.pattern}")
    return findings

# "Basis 1"/"Basis 2"/"Basis 3" are XASSET-0014 SS3.2's own defined,
# governance-vocabulary proper-noun labels for the three lawful Axis A
# evidentiary bases -- SS14's own field-design comment REQUIRES
# function_rationale to cite them by this exact name ("Basis 2", "Basis
# 3"). Treated as legitimate defined-term references, exactly the same
# whitelisting precedent this module's own _STAGE_LEGITIMATE_USE_PATTERNS
# already establishes for "Stage 4"/"Stage N" -- without this scrub, the
# schema's own required citation field would be unusable for its designed
# purpose, since the bare-digit scan has no exception of any kind
# otherwise. Scoped narrowly to "Basis 1/2/3" only -- never a general
# digit exemption, and never applied to _numeric_leakage_scan() itself
# (which remains fully strict for Stage 1-3 and for every other Stage 4
# field/context).
_BASIS_LEGITIMATE_USE_PATTERN = re.compile(r"\bbasis\s+[123]\b", re.IGNORECASE)

# Governance decision-ID citations (e.g. "XASSET-0013") are likewise
# legitimate, required, digit-bearing proper-noun references -- the
# relationship-coverage ledger's own deferred-pair provenance is, by
# design, attributed to XASSET-0013 (SS5.1/SS14), and this schema's own
# governing_decisions field structurally requires citing XASSET-0014/
# XASSET-0015. Scrubbed the same way as "Basis N" -- a named citation, not
# a numeric magnitude, weight, score, or size claim.
_DECISION_ID_LEGITIMATE_USE_PATTERN = re.compile(r"\b[A-Z]{2,}-\d{4}\b")


def _stage4_numeric_leakage_scan(text: str) -> list[str]:
    scrubbed = _BASIS_LEGITIMATE_USE_PATTERN.sub("", text)
    scrubbed = _DECISION_ID_LEGITIMATE_USE_PATTERN.sub("", scrubbed)
    return _numeric_leakage_scan(scrubbed)

# CASH/RESERVE-distinction-language scan (SS9/SS21 item 12) -- reuses
# economic_assessment_validator.py's own established mechanism DESIGN
# (same pattern shapes), not its literal code, since that module's own
# _DISTINCTION_PATTERNS is private to its file; ported here rather than
# imported, matching this module's own existing local-helper convention.
#
# Split into two groups (NEW-MINOR-A correction, independent exact-head
# delta review pullrequestreview-4912431420): the four "differ/distinct/
# different (treatment|purpose|role|function)" patterns immediately
# below are the ONLY patterns in this scan an independently-reproduced
# false-positive class was found against (five natural, compliant
# non-settlement/hedged sentences, all sharing "CASH ... RESERVE ...
# differ/distinct" proximity with no assertion ever actually made -- see
# _STAGE4_CASH_RESERVE_NONSETTLEMENT_LEADIN below) -- these four alone
# are run through the negation/hedge guard. Every other pattern in this
# scan (the idiom-class patterns, the MAJOR-2 non-fungibility patterns,
# and the NEW-MINOR-B additions below) is NOT hedge-guarded: no false
# positive was reproduced against any of them, and applying an unproven
# guard to patterns that were never shown to need one would only widen
# the surface for a future bypass with no offsetting benefit.
_STAGE4_CASH_RESERVE_DIFFER_DISTINCT_PATTERNS = [
    re.compile(p, re.IGNORECASE)
    for p in (
        r"\bCASH\b[^.]{0,120}\b(differ|distinct|different\s+(treatment|purpose|role|function)s?)\b[^.]{0,80}\bRESERVE\b",
        r"\bRESERVE\b[^.]{0,120}\b(differ|distinct|different\s+(treatment|purpose|role|function)s?)\b[^.]{0,80}\bCASH\b",
        r"\bCASH\b[^.]{0,30}\bRESERVE\b[^.]{0,60}\b(differ|distinct|different\s+(treatment|purpose|role|function)s?)\b",
        r"\bRESERVE\b[^.]{0,30}\bCASH\b[^.]{0,60}\b(differ|distinct|different\s+(treatment|purpose|role|function)s?)\b",
    )
]

# NEW-MINOR-A correction (independent exact-head delta review
# pullrequestreview-4912431420): the four "differ/distinct" patterns
# above have no way to distinguish a genuine assertion of distinctness
# ("CASH and RESERVE differ in purpose") from an explicit, hedged
# NON-settlement of the identical question ("It has not been established
# that CASH and RESERVE differ in purpose.") -- five natural, compliant
# sentences independently reproduced as false positives, all sharing one
# shape: a small, closed set of assertion-negating lead-in phrases
# ("whether", "does not assert that", "has not been established that",
# "no evidence ... that", "no basis to conclude") sits IMMEDIATELY before
# the leading CASH/RESERVE mention.
#
# Deliberately NOT a general "does a negation word appear somewhere
# nearby" guard: this module's own sibling economic_assessment_
# validator.py spent seven separate bounded-correction rounds
# discovering that a blacklist-style "is there a negation/deferral word
# somewhere nearby" check for a materially similar scan is unprovably
# incomplete, and worse, becomes its own loophole -- a bare "not"
# appearing anywhere in an earlier, unrelated clause ("It is not the
# case that CASH and RESERVE are the same -- they are distinct.") would
# wrongly suppress a genuine, later assertion. The guard here is instead
# a small, CLOSED whitelist of specific, multi-word, assertion-negating
# idioms, each required to sit IMMEDIATELY adjacent (allowing only an
# optional "that ") to the leading entity mention the differ/distinct
# match itself starts at -- not "a negation word appears somewhere in
# the sentence." "not the case that" is deliberately absent from this
# whitelist, so the loophole sentence above remains caught (verified in
# the test suite, both for that literal sentence and for a same-shape
# "is not the case that ... are identical; in fact, they are distinct"
# variant). This is a narrow, purpose-built mechanism for this one
# scan's own demonstrated vulnerability class, not a port of economic_
# assessment_validator.py's own much larger general clause-whitelist
# architecture -- reusing that architecture's full machinery here is out
# of scope for this bounded correction (see the module comment above
# this scan's own pattern list for the existing "reuses DESIGN, not
# literal code" convention this follows).
_STAGE4_CASH_RESERVE_NONSETTLEMENT_LEADIN = re.compile(
    r"\b(?:"
    r"whether"
    r"|(?:does|do|did|is|are|has|have)\s+not\s+(?:been\s+)?"
    r"(?:assert|claim|conclude|establish|state|find|show|determine)\w*(?:\s+that)?"
    r"|no\s+(?:evidence|basis)(?:\s+\w+){0,4}?\s+(?:that|to\s+conclude|to\s+assert)"
    r")\b\s*(?=(?:CASH|RESERVE)\b)",
    re.IGNORECASE,
)


def _cash_reserve_differ_distinct_findings(text: str) -> list[str]:
    """Applies _STAGE4_CASH_RESERVE_NONSETTLEMENT_LEADIN as a per-match
    veto against _STAGE4_CASH_RESERVE_DIFFER_DISTINCT_PATTERNS only: a
    match is suppressed only when a whitelisted non-settlement lead-in
    phrase ends EXACTLY where that match's own leading CASH/RESERVE
    mention begins. Both the lead-in pattern's own lookahead and every
    differ/distinct pattern's own leading \\bCASH\\b/\\bRESERVE\\b anchor
    are zero-width at that boundary, so hedge_match.end() ==
    distinction_match.start() precisely when the hedge phrase is truly
    adjacent to the claim it is hedging -- never merely somewhere earlier
    in the same sentence."""
    hedge_ends = {m.end() for m in _STAGE4_CASH_RESERVE_NONSETTLEMENT_LEADIN.finditer(text)}
    findings: list[str] = []
    for pat in _STAGE4_CASH_RESERVE_DIFFER_DISTINCT_PATTERNS:
        for m in pat.finditer(text):
            if m.start() in hedge_ends:
                continue
            findings.append(f"stage4-cash-reserve-distinction:{pat.pattern}")
    return findings


_STAGE4_CASH_RESERVE_OTHER_DISTINCTION_PATTERNS = [
    re.compile(p, re.IGNORECASE)
    for p in (
        r"\bRESERVE\s+(functions|serves|acts)\s+as\b",
        r"\bCASH\s+is\s+used\s+for\b",
        r"\bRESERVE\s+is\s+(used|intended|held|meant)\s+for\b",
        r"\b(CASH|RESERVE)\s+individually\s+warrants?\b",
        r"\b(CASH|RESERVE)\s+(alone|specifically)\s+(is|represents|serves)\b",
        r"\bthe\s+(reserve|cash)\s+(percentage|pct|weight|target)\s+(suggests|implies|indicates)\b",
        # -- MAJOR-2 additions (independent exact-head review
        # pullrequestreview-4911497398): the original ten patterns all
        # required one of differ/distinct/different (treatment|purpose|
        # role|function) as the connecting verb/adjective -- a plain-
        # English non-fungibility assertion ("CASH and RESERVE are not
        # interchangeable," "CASH accomplishes something RESERVE does
        # not," "RESERVE cannot do what CASH does") states the identical
        # forbidden claim (XASSET-0008 SS N / XASSET-0009's own boundary)
        # without using any of those stem words, and evaded every
        # existing pattern. Added as their own idiom class, both entity
        # orders, alongside a false-positive guard requirement that
        # ordinary non-settlement/abstention language (e.g. this record's
        # own required cash_reserve_consolidation_note) stays clean --
        # verified against the real sealed cash_reserve.yaml note and the
        # adversarial matrix in test_level1_sleeve_synthesis_validator.py.
        #
        # NEW-MINOR-B correction (pullrequestreview-4912431420) broadened
        # the "accomplish(es)/does/performs something" tail noun below
        # from "something" alone to also include "a role"/"a function"/
        # "the role"/"the function" -- "RESERVE performs a role CASH
        # cannot perform" states the identical forbidden claim with a
        # concrete noun in place of "something," and evaded the original,
        # narrower alternative. "something" remains the first alternative
        # (no existing MAJOR-2 match is lost).
        r"\bCASH\b[^.]{0,60}\b(accomplish|accomplishes|does|performs)\s+(?:something|a\s+role|a\s+function|the\s+role|the\s+function)\b[^.]{0,60}\bRESERVE\b[^.]{0,30}\b(does\s+not|cannot|can\s*not)\b",
        r"\bRESERVE\b[^.]{0,60}\b(accomplish|accomplishes|does|performs)\s+(?:something|a\s+role|a\s+function|the\s+role|the\s+function)\b[^.]{0,60}\bCASH\b[^.]{0,30}\b(does\s+not|cannot|can\s*not)\b",
        r"\bCASH\b[^.]{0,30}\b(cannot|can\s*not)\s+do\s+what\b[^.]{0,30}\bRESERVE\b[^.]{0,20}\bdoes\b",
        r"\bRESERVE\b[^.]{0,30}\b(cannot|can\s*not)\s+do\s+what\b[^.]{0,30}\bCASH\b[^.]{0,20}\bdoes\b",
        r"\bCASH\b[^.]{0,120}\b(not\s+interchangeable|non-fungible|not\s+fungible)\b[^.]{0,80}\bRESERVE\b",
        r"\bRESERVE\b[^.]{0,120}\b(not\s+interchangeable|non-fungible|not\s+fungible)\b[^.]{0,80}\bCASH\b",
        r"\bCASH\b[^.]{0,120}\bRESERVE\b[^.]{0,60}\b(not\s+interchangeable|non-fungible|not\s+fungible)\b",
        r"\bRESERVE\b[^.]{0,120}\bCASH\b[^.]{0,60}\b(not\s+interchangeable|non-fungible|not\s+fungible)\b",
        # -- NEW-MINOR-B additions (pullrequestreview-4912431420): three
        # further real bypasses, each its own distinct construction the
        # existing idiom patterns above do not reach.
        #
        # "CASH cannot serve the function that RESERVE serves." -- a
        # shared-function-denial idiom distinct from the "do what"
        # construction two patterns above (no "do"/"does" verb at all).
        r"\bCASH\b[^.]{0,30}\bcannot\s+(?:serve|perform|fulfill)\s+the\s+(?:function|role)\s+(?:that|which)\b[^.]{0,30}\bRESERVE\b[^.]{0,20}\b(?:serves|performs|fulfills)\b",
        r"\bRESERVE\b[^.]{0,30}\bcannot\s+(?:serve|perform|fulfill)\s+the\s+(?:function|role)\s+(?:that|which)\b[^.]{0,30}\bCASH\b[^.]{0,20}\b(?:serves|performs|fulfills)\b",
        # "What CASH accomplishes, RESERVE does not." -- a fronted/
        # topicalized clause stating the same MAJOR-2 "accomplishes
        # something ... does not" claim with the object clause moved to
        # the front of the sentence, which the tight-proximity MAJOR-2
        # pattern (anchored on CASH/RESERVE appearing in that fixed
        # order) cannot reach.
        r"\bWhat\s+CASH\s+(?:accomplish|accomplishes|does|performs)\b[^,]{0,30},?\s*\bRESERVE\s+(?:does\s+not|cannot|can\s*not)\b",
        r"\bWhat\s+RESERVE\s+(?:accomplish|accomplishes|does|performs)\b[^,]{0,30},?\s*\bCASH\s+(?:does\s+not|cannot|can\s*not)\b",
        # "Non-fungible: CASH and RESERVE." -- phrase-before-entities
        # ordering; the existing non-fungibility patterns above only
        # recognize entities-then-phrase.
        r"\b(?:not\s+interchangeable|non-fungible|not\s+fungible)\b\s*[:.\-]{0,2}\s*\bCASH\b[^.]{0,30}\bRESERVE\b",
        r"\b(?:not\s+interchangeable|non-fungible|not\s+fungible)\b\s*[:.\-]{0,2}\s*\bRESERVE\b[^.]{0,30}\bCASH\b",
    )
]


def _stage4_bounded_conclusion_scan(text: str, repo_root: Path | None = None) -> list[str]:
    findings: list[str] = []
    for pat in _STAGE4_OVERCLAIM_PATTERNS:
        if pat.search(text):
            findings.append(f"stage4-overclaim:{pat.pattern}")
    for pat in _stage4_level2_weight_patterns(repo_root):
        if pat.search(text):
            findings.append(f"stage4-level2-weight-leakage:{pat.pattern}")
    if _STAGE4_QQQ_PATTERN.search(text):
        findings.append("stage4-qqq-boundary")
    findings.extend(_cash_reserve_differ_distinct_findings(text))
    for pat in _STAGE4_CASH_RESERVE_OTHER_DISTINCTION_PATTERNS:
        if pat.search(text):
            findings.append(f"stage4-cash-reserve-distinction:{pat.pattern}")
    return findings


def _scan_stage4_free_text(value: object, field_name: str, errors: list[str], *, repo_root: Path | None = None) -> None:
    """Reuses _prohibited_content_scan() (policy-leak, chart-domain,
    directive-word, bare-gate-word -- all already Stage-4-appropriate
    mechanisms, none redesigned) plus _numeric_leakage_scan() and _
    comparative_superiority_scan() wholesale, and adds this section's own
    materially separate bounded-conclusion / Level-2-weight / QQQ / CASH-
    RESERVE-distinction scans -- deliberately does NOT call _eligibility_
    language_scan() (Stage 1-3's blanket ban, inapplicable to Stage 4 by
    design -- see the module comment above item 13)."""
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
        for finding in _prohibited_content_scan(text):
            errors.append(f"{field_name} contains prohibited content ({finding})")
        for finding in _stage4_numeric_leakage_scan(text):
            errors.append(f"{field_name} contains prohibited content ({finding})")
        for finding in _comparative_superiority_scan(text):
            errors.append(f"{field_name} contains prohibited content ({finding})")
        for finding in _stage4_bounded_conclusion_scan(text, repo_root=repo_root):
            errors.append(f"{field_name} contains prohibited content ({finding})")
        for finding in _scan_contender_citation(text):
            errors.append(f"{field_name} contains prohibited content ({finding})")


# -- Schema shapes -------------------------------------------------------------

_POLICY_ADOPTION_TOP_KEYS = frozenset({
    "schema_version", "sleeve_id", "profile_reference", "relationship_references",
    "portfolio_function_status", "function_rationale", "abstention_index",
    "capital_eligibility_status", "sizing_readiness_status", "blocking_evidence",
    "unresolved_relationships", "relationship_coverage_ledger", "overlap_coordination_notes",
    "cash_reserve_consolidation_note", "record_status",
    *_SEAL_FIELDS,
})

_PROFILE_REF_KEYS = frozenset({"record_path", "referenced_content_sha256"})
_REL_REF_KEYS = frozenset({"sleeve_pair", "record_path", "referenced_content_sha256"})
_LEDGER_ENTRY_KEYS = frozenset({"other_sleeve_id", "coverage_state", "reference"})
_LEDGER_REF_SEALED_KEYS = frozenset({"record_path", "referenced_content_sha256"})
_LEDGER_REF_DEFERRED_KEYS = frozenset({"deferral_class", "governing_decision"})
_BLOCKING_EVIDENCE_KEYS = frozenset({"reason_type", "other_sleeve_id", "detail", "reference"})
_UNRESOLVED_REL_KEYS = frozenset({"other_sleeve_id", "record_path", "referenced_content_sha256"})
_OVERLAP_NOTE_KEYS = frozenset({"other_sleeve_id", "dimension_ids", "note"})


def _validate_hash_ref(
    ref: dict, label: str, errors: list[str], *, repo_root: Path | None, record_dir: str,
) -> None:
    """Verifies exactly the record_path/referenced_content_sha256 pair --
    deliberately does NOT reject-unknown-keys on the full ref dict, since
    callers routinely pass a superset dict (e.g. a relationship_references[]
    entry also carrying its own sleeve_pair key, or an unresolved_
    relationships[] entry also carrying its own other_sleeve_id key) --
    each caller performs its own full-shape _reject_unknown_keys check
    separately, against its own correct key set."""
    path_val = ref.get("record_path")
    hash_val = ref.get("referenced_content_sha256")
    if not _non_empty_str(path_val):
        errors.append(f"{label}.record_path must be a non-empty string")
        return
    if not _non_empty_str(hash_val):
        errors.append(f"{label}.referenced_content_sha256 must be a non-empty string")
        return
    if repo_root is None:
        return
    full = repo_root / path_val
    if not full.is_file():
        errors.append(f"{label} references missing file {full}")
        return
    data, errs = _read_yaml(full)
    if errs or not isinstance(data, dict):
        errors.append(f"{label} could not verify {full} -- unparseable")
        return
    live_hash = canonical_record_hash(data)
    if hash_val != live_hash:
        errors.append(
            f"{label}.referenced_content_sha256 is stale -- recorded {hash_val!r}, "
            f"live-recomputed {live_hash!r} against the current sealed {full}"
        )


def validate_policy_adoption_data(
    data: object, expected_sleeve_id: str | None = None, *, repo_root: Path | None = None,
) -> list[str]:
    """Mirrors validate_sleeve_profile_data()'s/validate_sleeve_relationship_
    data()'s own established convention exactly: a bare list[str] of errors
    (empty == valid), never a ValidationResult -- that wrapping happens only
    at the *_file() layer, matching every sibling record type in this
    module."""
    errors: list[str] = []
    if not isinstance(data, dict):
        return ["record must be a mapping"]

    _reject_unknown_keys(data, "<record>", _POLICY_ADOPTION_TOP_KEYS, errors)
    missing = _POLICY_ADOPTION_TOP_KEYS - data.keys()
    if missing:
        errors.append(f"record missing key(s): {sorted(missing)}")
        return errors

    if data.get("schema_version") != SCHEMA_VERSION:
        errors.append(f"schema_version must be {SCHEMA_VERSION!r}")

    sleeve_id = data.get("sleeve_id")
    if sleeve_id not in SLEEVE_IDS:
        errors.append(f"sleeve_id must be one of {sorted(SLEEVE_IDS)}, got {sleeve_id!r}")
        return errors
    if expected_sleeve_id is not None and sleeve_id != expected_sleeve_id:
        errors.append(f"sleeve_id {sleeve_id!r} does not match filename stem {expected_sleeve_id!r}")

    # -- profile_reference ----------------------------------------------
    profile_ref = data.get("profile_reference")
    if not isinstance(profile_ref, dict):
        errors.append("profile_reference must be a mapping")
    else:
        _reject_unknown_keys(profile_ref, "profile_reference", _PROFILE_REF_KEYS, errors)
        _validate_hash_ref(profile_ref, "profile_reference", errors, repo_root=repo_root, record_dir=_PROFILES_DIR)
        expected_path = f"{_PROFILES_DIR}/{sleeve_id}.yaml"
        if profile_ref.get("record_path") not in (None, expected_path):
            errors.append(f"profile_reference.record_path must be {expected_path!r}")

    # -- relationship_references[] ---------------------------------------
    rel_refs = data.get("relationship_references")
    declared_pairs: set[tuple[str, str]] = set()
    if not isinstance(rel_refs, list):
        errors.append("relationship_references must be a list")
    else:
        for i, entry in enumerate(rel_refs):
            label = f"relationship_references[{i}]"
            if not isinstance(entry, dict):
                errors.append(f"{label} must be a mapping")
                continue
            _reject_unknown_keys(entry, label, _REL_REF_KEYS, errors)
            missing_e = _REL_REF_KEYS - entry.keys()
            if missing_e:
                errors.append(f"{label} missing key(s): {sorted(missing_e)}")
                continue
            sp = entry.get("sleeve_pair")
            if not isinstance(sp, dict) or set(sp.keys()) != {"sleeve_a", "sleeve_b"}:
                errors.append(f"{label}.sleeve_pair must be a mapping with exactly sleeve_a/sleeve_b")
                continue
            pair = (sp.get("sleeve_a"), sp.get("sleeve_b"))
            if pair not in AUTHORIZED_RELATIONSHIP_PAIRS:
                errors.append(f"{label}.sleeve_pair {pair!r} is not one of the seven authorized sealed pairs")
                continue
            if sleeve_id not in pair:
                errors.append(f"{label}.sleeve_pair {pair!r} does not name this record's own sleeve_id {sleeve_id!r}")
            declared_pairs.add(pair)
            _validate_hash_ref(entry, label, errors, repo_root=repo_root, record_dir=_RELATIONSHIPS_DIR)
        expected_pairs = {p for p in AUTHORIZED_RELATIONSHIP_PAIRS if sleeve_id in p}
        if declared_pairs != expected_pairs:
            errors.append(
                f"relationship_references must cite exactly the sealed pairs naming this sleeve "
                f"{sorted(expected_pairs)}, got {sorted(declared_pairs)}"
            )

    # -- Axis A ------------------------------------------------------------
    axis_a = data.get("portfolio_function_status")
    if axis_a not in _PORTFOLIO_FUNCTION_STATUS_VALUES:
        errors.append(f"portfolio_function_status must be one of {sorted(_PORTFOLIO_FUNCTION_STATUS_VALUES)}")

    function_rationale = data.get("function_rationale")
    if not _non_empty_str(function_rationale):
        errors.append("function_rationale must be a non-empty string")
    else:
        _scan_stage4_free_text(function_rationale, "function_rationale", errors, repo_root=repo_root)
        for finding in _scan_basis3_forbidden_fields(function_rationale):
            errors.append(f"function_rationale contains prohibited content ({finding})")
        # SS21 item 22 -- structurally required to be substantial, never a
        # generic/templated placeholder; the validator cannot semantically
        # verify CLAUDE.md prose content (SS21 item 22's own disclosed
        # limit), so only a minimum-substance floor is mechanically
        # enforced here.
        if len(function_rationale.strip()) < 80:
            errors.append("function_rationale is too short to be a substantial, non-templated citation")

    if repo_root is not None and isinstance(sleeve_id, str) and sleeve_id in SLEEVE_IDS:
        basis1 = compute_basis1_findings(sleeve_id, repo_root)
        basis3 = compute_basis3_available(sleeve_id, repo_root)
        if axis_a == FUNCTION_CONFIRMED_DISTINCT and not (basis1 or basis3):
            errors.append(
                "portfolio_function_status == function_confirmed_distinct requires at least one "
                "live-verifiable lawful basis (Basis 1 or Basis 3) -- neither is available for this "
                "sleeve; a citation resting on Basis 2 alone cannot be independently confirmed by this "
                "validator and is not sufficient on its own to satisfy this mechanical gate"
            )
        if sleeve_id == DEBT_REDUCTION and basis3:
            errors.append("Basis 3 must never resolve available for debt_reduction (no targets.yaml row exists)")

    # -- abstention_index[] --------------------------------------------
    abstention_index = data.get("abstention_index")
    if not isinstance(abstention_index, list):
        errors.append("abstention_index must be a list")
    else:
        for i, entry in enumerate(abstention_index):
            label = f"abstention_index[{i}]"
            if not isinstance(entry, dict) or set(entry.keys()) != {"axis", "value", "reason"}:
                errors.append(f"{label} must be a mapping with exactly axis/value/reason")
                continue
            if entry.get("axis") != "portfolio_function_status":
                errors.append(f"{label}.axis must be 'portfolio_function_status' -- the only axis with an abstention path")
            if entry.get("value") != AXIS_A_UNABLE_TO_DETERMINE:
                errors.append(f"{label}.value must be {AXIS_A_UNABLE_TO_DETERMINE!r}")
            if not _non_empty_str(entry.get("reason")):
                errors.append(f"{label}.reason must be a non-empty string")
            else:
                _scan_stage4_free_text(entry.get("reason"), label + ".reason", errors, repo_root=repo_root)
        if axis_a == AXIS_A_UNABLE_TO_DETERMINE and not abstention_index:
            errors.append("abstention_index must be non-empty when portfolio_function_status == unable_to_determine")
        if axis_a != AXIS_A_UNABLE_TO_DETERMINE and abstention_index:
            errors.append("abstention_index must be empty when portfolio_function_status != unable_to_determine")

    # -- Axis B (mechanical re-derivation, zero drafting discretion) ----
    axis_b = data.get("capital_eligibility_status")
    if axis_b not in _CAPITAL_ELIGIBILITY_VALUES:
        errors.append(f"capital_eligibility_status must be one of {sorted(_CAPITAL_ELIGIBILITY_VALUES)}")
    live_profile = _live_profile(repo_root, sleeve_id) if isinstance(sleeve_id, str) else None
    live_axis_b = None
    if live_profile is not None:
        live_axis_b = compute_axis_b(live_profile.get("evidence_coverage_profile"))
        if live_axis_b is None:
            errors.append("live sleeve_profile.evidence_coverage_profile is not one of the four closed values")
        elif axis_b in _CAPITAL_ELIGIBILITY_VALUES and axis_b != live_axis_b:
            errors.append(
                f"capital_eligibility_status {axis_b!r} does not match the live-derived value "
                f"{live_axis_b!r} mechanically re-derived from this sleeve's own sealed "
                f"evidence_coverage_profile -- Axis B carries zero drafting-session discretion"
            )

    # -- relationship_coverage_ledger[] ----------------------------------
    ledger = data.get("relationship_coverage_ledger")
    live_ledger: list[_LedgerEntry] = []
    if isinstance(sleeve_id, str) and sleeve_id in SLEEVE_IDS:
        live_ledger = compute_live_relationship_ledger(sleeve_id, repo_root)
    live_by_other = {e.other_sleeve_id: e for e in live_ledger}
    if not isinstance(ledger, list):
        errors.append("relationship_coverage_ledger must be a list")
    else:
        seen_others: set[str] = set()
        for i, entry in enumerate(ledger):
            label = f"relationship_coverage_ledger[{i}]"
            if not isinstance(entry, dict):
                errors.append(f"{label} must be a mapping")
                continue
            _reject_unknown_keys(entry, label, _LEDGER_ENTRY_KEYS, errors)
            missing_e = _LEDGER_ENTRY_KEYS - entry.keys()
            if missing_e:
                errors.append(f"{label} missing key(s): {sorted(missing_e)}")
                continue
            other = entry.get("other_sleeve_id")
            if other in seen_others:
                errors.append(f"{label} duplicates other_sleeve_id {other!r}")
            seen_others.add(other)
            if other == sleeve_id or other not in SLEEVE_IDS:
                errors.append(f"{label}.other_sleeve_id {other!r} is invalid for sleeve_id {sleeve_id!r}")
                continue
            coverage_state = entry.get("coverage_state")
            if coverage_state not in _COVERAGE_STATE_VALUES:
                errors.append(f"{label}.coverage_state must be one of {sorted(_COVERAGE_STATE_VALUES)}")
                continue
            reference = entry.get("reference")
            if not isinstance(reference, dict):
                errors.append(f"{label}.reference must be a mapping")
                continue
            live = live_by_other.get(other)
            if coverage_state in (SEALED_DETERMINED, SEALED_UNRESOLVED):
                _reject_unknown_keys(reference, f"{label}.reference", _LEDGER_REF_SEALED_KEYS, errors)
                missing_r = _LEDGER_REF_SEALED_KEYS - reference.keys()
                if missing_r:
                    errors.append(f"{label}.reference missing key(s): {sorted(missing_r)}")
                else:
                    _validate_hash_ref(reference, f"{label}.reference", errors, repo_root=repo_root, record_dir=_RELATIONSHIPS_DIR)
            elif coverage_state == DEFERRED_DISCLOSED:
                _reject_unknown_keys(reference, f"{label}.reference", _LEDGER_REF_DEFERRED_KEYS, errors)
                missing_r = _LEDGER_REF_DEFERRED_KEYS - reference.keys()
                if missing_r:
                    errors.append(f"{label}.reference missing key(s): {sorted(missing_r)}")
                else:
                    if reference.get("governing_decision") != "XASSET-0013":
                        errors.append(f"{label}.reference.governing_decision must be 'XASSET-0013'")
                    declared_class = reference.get("deferral_class")
                    if declared_class not in _DEFERRAL_CLASS_VALUES:
                        errors.append(f"{label}.reference.deferral_class must be one of {sorted(_DEFERRAL_CLASS_VALUES)}")
                    if live is not None and live.deferral_class is not None and declared_class != live.deferral_class:
                        errors.append(
                            f"{label}.reference.deferral_class {declared_class!r} does not match the "
                            f"live, closed XASSET-0013 SS E deferral class {live.deferral_class!r}"
                        )
            if live is not None and coverage_state != live.coverage_state:
                errors.append(
                    f"{label}.coverage_state {coverage_state!r} does not match the live, mechanically "
                    f"cross-referenced coverage state {live.coverage_state!r} for the "
                    f"{sleeve_id}-{other} pair"
                )
        expected_others = {_other_sleeve_in_pair(p, sleeve_id) for p in _all_pairs_touching(sleeve_id)} if isinstance(sleeve_id, str) and sleeve_id in SLEEVE_IDS else set()
        if expected_others and seen_others != expected_others:
            missing_others = expected_others - seen_others
            extra_others = seen_others - expected_others
            if missing_others:
                errors.append(f"relationship_coverage_ledger missing entry(ies) for {sorted(missing_others)}")
            if extra_others:
                errors.append(f"relationship_coverage_ledger has non-authorized entry(ies) for {sorted(extra_others)}")
        elif expected_others and len(ledger if isinstance(ledger, list) else []) != 5:
            errors.append("relationship_coverage_ledger must have exactly five entries -- one per possible pair")

    # -- Axis C mechanical consistency -----------------------------------
    sizing = data.get("sizing_readiness_status")
    if sizing not in _SIZING_READINESS_VALUES:
        errors.append(f"sizing_readiness_status must be one of {sorted(_SIZING_READINESS_VALUES)}")
    elif live_ledger and axis_a in _PORTFOLIO_FUNCTION_STATUS_VALUES and live_axis_b is not None:
        expected_sizing = compute_expected_sizing_readiness(axis_a, live_axis_b, live_ledger)
        if sizing != expected_sizing:
            errors.append(
                f"sizing_readiness_status {sizing!r} does not match the live, mechanically derived "
                f"value {expected_sizing!r} (from portfolio_function_status={axis_a!r}, the live-"
                f"derived capital_eligibility_status={live_axis_b!r}, and the live relationship-"
                f"coverage ledger)"
            )

    # -- blocking_evidence[] ----------------------------------------------
    blocking = data.get("blocking_evidence")
    if not isinstance(blocking, list):
        errors.append("blocking_evidence must be a list")
    else:
        if sizing in (SIZING_BLOCKED, SIZING_CONDITIONALLY_READY) and not blocking:
            errors.append("blocking_evidence must be non-empty when sizing_readiness_status != sizing_ready")
        if sizing == SIZING_READY and blocking:
            errors.append("blocking_evidence must be empty when sizing_readiness_status == sizing_ready")
        for i, entry in enumerate(blocking):
            label = f"blocking_evidence[{i}]"
            if not isinstance(entry, dict):
                errors.append(f"{label} must be a mapping")
                continue
            _reject_unknown_keys(entry, label, _BLOCKING_EVIDENCE_KEYS, errors)
            missing_e = _BLOCKING_EVIDENCE_KEYS - entry.keys()
            if missing_e:
                errors.append(f"{label} missing key(s): {sorted(missing_e)}")
                continue
            if entry.get("reason_type") not in _BLOCKING_REASON_TYPES:
                errors.append(f"{label}.reason_type must be one of {sorted(_BLOCKING_REASON_TYPES)}")
            if not _non_empty_str(entry.get("detail")):
                errors.append(f"{label}.detail must be a non-empty string")
            else:
                _scan_stage4_free_text(entry.get("detail"), label + ".detail", errors, repo_root=repo_root)
            ref = entry.get("reference")
            if ref is not None:
                if not isinstance(ref, dict):
                    errors.append(f"{label}.reference must be a mapping or null")
                else:
                    # MAJOR-1 correction (independent exact-head review
                    # pullrequestreview-4911497398): _validate_hash_ref()
                    # deliberately performs no shape closure of its own (see
                    # its own docstring) -- every OTHER caller in this
                    # function closes its own reference shape before or via
                    # _validate_hash_ref (profile_reference,
                    # relationship_references[i], both
                    # relationship_coverage_ledger[i].reference branches,
                    # unresolved_relationships[i]); this call site was the
                    # one place that check was missing, letting an
                    # arbitrary extra key inside blocking_evidence[i].
                    # reference validate cleanly -- the exact defect class
                    # this PR's own commit message already disclosed fixing
                    # once for profile_reference, not generalized to every
                    # call site. blocking_evidence[i].reference shares the
                    # identical record_path/referenced_content_sha256 shape
                    # as relationship_coverage_ledger[i]'s own sealed-state
                    # reference (confirmed against every real sealed
                    # record), so the fix reuses _LEDGER_REF_SEALED_KEYS
                    # rather than inventing a new, duplicate key set.
                    _reject_unknown_keys(ref, f"{label}.reference", _LEDGER_REF_SEALED_KEYS, errors)
                    missing_ref = _LEDGER_REF_SEALED_KEYS - ref.keys()
                    if missing_ref:
                        errors.append(f"{label}.reference missing key(s): {sorted(missing_ref)}")
                    else:
                        _validate_hash_ref(ref, f"{label}.reference", errors, repo_root=repo_root, record_dir=_RELATIONSHIPS_DIR)

    # -- unresolved_relationships[] ----------------------------------------
    unresolved = data.get("unresolved_relationships")
    live_unresolved = {e.other_sleeve_id for e in live_ledger if e.coverage_state == SEALED_UNRESOLVED}
    if not isinstance(unresolved, list):
        errors.append("unresolved_relationships must be a list")
    else:
        declared_unresolved: set[str] = set()
        for i, entry in enumerate(unresolved):
            label = f"unresolved_relationships[{i}]"
            if not isinstance(entry, dict):
                errors.append(f"{label} must be a mapping")
                continue
            _reject_unknown_keys(entry, label, _UNRESOLVED_REL_KEYS, errors)
            missing_e = _UNRESOLVED_REL_KEYS - entry.keys()
            if missing_e:
                errors.append(f"{label} missing key(s): {sorted(missing_e)}")
                continue
            declared_unresolved.add(entry.get("other_sleeve_id"))
            _validate_hash_ref(entry, label, errors, repo_root=repo_root, record_dir=_RELATIONSHIPS_DIR)
        if live_ledger and declared_unresolved != live_unresolved:
            errors.append(
                f"unresolved_relationships must name exactly the live sealed_unresolved pairs "
                f"{sorted(live_unresolved)}, got {sorted(declared_unresolved)}"
            )

    # -- overlap_coordination_notes[] --------------------------------------
    overlap_notes = data.get("overlap_coordination_notes")
    if not isinstance(overlap_notes, list):
        errors.append("overlap_coordination_notes must be a list")
    else:
        for i, entry in enumerate(overlap_notes):
            label = f"overlap_coordination_notes[{i}]"
            if not isinstance(entry, dict):
                errors.append(f"{label} must be a mapping")
                continue
            _reject_unknown_keys(entry, label, _OVERLAP_NOTE_KEYS, errors)
            missing_e = _OVERLAP_NOTE_KEYS - entry.keys()
            if missing_e:
                errors.append(f"{label} missing key(s): {sorted(missing_e)}")
                continue
            other = entry.get("other_sleeve_id")
            if other not in SLEEVE_IDS or other == sleeve_id:
                errors.append(f"{label}.other_sleeve_id {other!r} is invalid")
            dim_ids = entry.get("dimension_ids")
            if not isinstance(dim_ids, list) or not dim_ids:
                errors.append(f"{label}.dimension_ids must be a non-empty list")
            else:
                for dim_id in dim_ids:
                    if not _non_empty_str(dim_id):
                        errors.append(f"{label}.dimension_ids has a non-string/empty entry")
                        continue
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
                            f"{label} cites dimension_id {dim_id!r} whose own live computation_status "
                            f"is not {_COMPUTED_FROM_EXISTING_MECHANISM!r}"
                        )
            if not _non_empty_str(entry.get("note")):
                errors.append(f"{label}.note must be a non-empty string")
            else:
                _scan_stage4_free_text(entry.get("note"), label + ".note", errors, repo_root=repo_root)

    # -- cash_reserve_consolidation_note ------------------------------------
    note = data.get("cash_reserve_consolidation_note")
    if sleeve_id == CASH_RESERVE:
        if not _non_empty_str(note):
            errors.append("cash_reserve_consolidation_note must be a non-empty string on the cash_reserve record")
        else:
            _scan_stage4_free_text(note, "cash_reserve_consolidation_note", errors, repo_root=repo_root)
            if len(note.strip()) < 80:
                errors.append("cash_reserve_consolidation_note is too short to be a substantial non-settlement statement")
    else:
        if note is not None:
            errors.append("cash_reserve_consolidation_note must be null on every record except cash_reserve")

    # -- record_status / seal -----------------------------------------------
    if data.get("record_status") not in _LIFECYCLE_VALUES:
        errors.append(f"record_status must be one of {sorted(_LIFECYCLE_VALUES)}")

    governing = data.get("governing_decisions")
    if not isinstance(governing, list) or set(governing) != {"XASSET-0014", "XASSET-0015"}:
        errors.append("governing_decisions must be exactly ['XASSET-0014', 'XASSET-0015']")

    if not _non_empty_str(data.get("sealed_at")):
        errors.append("sealed_at must be a non-empty string")
    if not _non_empty_str(data.get("drafting_session_or_shard_id")):
        errors.append("drafting_session_or_shard_id must be a non-empty string")
    expected_manifest_entry = f"{_POLICY_ADOPTION_DIR}/COHORT_MANIFEST.yaml#{sleeve_id}"
    if data.get("cohort_manifest_entry") != expected_manifest_entry:
        errors.append(f"cohort_manifest_entry must be {expected_manifest_entry!r}")

    if data.get("record_status") == "sealed":
        expected_hash = canonical_record_hash(data)
        if data.get("content_sha256") != expected_hash:
            errors.append(
                f"content_sha256 does not match the live-recomputed canonical hash "
                f"({data.get('content_sha256')!r} vs {expected_hash!r})"
            )

    # -- structural key-name / Level-2-leakage / contender-boundary scans --
    _scan_key_names_recursive(data, "<record>", errors, allow_keys=frozenset({"reference"}))
    _scan_all_strings_for_contender_citation(data, "<record>", errors)

    return errors


def validate_policy_adoption_file(path: Path, *, repo_root: Path | None = None) -> "ValidationResult":
    data, read_errors = _read_yaml(path)
    if read_errors:
        return ValidationResult(valid=False, errors=read_errors, source=str(path))
    errors = validate_policy_adoption_data(data, path.stem, repo_root=repo_root)
    return ValidationResult(valid=not errors, errors=errors, source=str(path))


# -- Manifest / directory validation ------------------------------------------

_POLICY_ADOPTION_MANIFEST_ROW_KEYS = frozenset({
    "sleeve_id", "shard_id", "sealed_at", "content_sha256", "schema_version",
    "governing_decision", "record_path",
})


def validate_policy_adoption_cohort_manifest(manifest_path: Path, records_dir: Path) -> "ValidationResult":
    errors: list[str] = []
    data, read_errors = _read_yaml(manifest_path)
    if read_errors:
        return ValidationResult(valid=False, errors=read_errors, source=str(manifest_path))
    if not isinstance(data, dict):
        return ValidationResult(valid=False, errors=["manifest must be a mapping"], source=str(manifest_path))

    _reject_unknown_keys(data, "<manifest>", _MANIFEST_TOP_KEYS, errors)
    if data.get("schema_version") != SCHEMA_VERSION:
        errors.append(f"manifest schema_version must be {SCHEMA_VERSION!r}")
    if data.get("governing_decision") != "XASSET-0015":
        errors.append("manifest governing_decision must be 'XASSET-0015'")

    cohort = data.get("cohort")
    if not isinstance(cohort, list):
        errors.append("manifest cohort must be a list")
        return ValidationResult(valid=not errors, errors=errors, source=str(manifest_path))

    seen: set[str] = set()
    for i, row in enumerate(cohort):
        if not isinstance(row, dict):
            errors.append(f"cohort[{i}] must be a mapping")
            continue
        _reject_unknown_keys(row, f"cohort[{i}]", _POLICY_ADOPTION_MANIFEST_ROW_KEYS, errors)
        missing = _POLICY_ADOPTION_MANIFEST_ROW_KEYS - row.keys()
        if missing:
            errors.append(f"cohort[{i}] missing key(s): {sorted(missing)}")
            continue
        sleeve_id = row["sleeve_id"]
        if sleeve_id in seen:
            errors.append(f"cohort has duplicate sleeve_id: {sleeve_id!r}")
        seen.add(sleeve_id)

        expected_record_path = f"{_POLICY_ADOPTION_DIR}/{sleeve_id}.yaml"
        if row["record_path"] != expected_record_path:
            errors.append(f"cohort[{i}] ({sleeve_id!r}) record_path must be {expected_record_path!r}")

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


def validate_policy_adoption_directory(records_dir: Path, *, repo_root: Path | None = None) -> "DirectoryValidationResult":
    results: list[ValidationResult] = []
    if not records_dir.is_dir():
        return DirectoryValidationResult(valid=True, results=[])

    for path in sorted(records_dir.glob("*.yaml")):
        if path.name == "COHORT_MANIFEST.yaml":
            continue
        results.append(validate_policy_adoption_file(path, repo_root=repo_root))

    manifest_path = records_dir / "COHORT_MANIFEST.yaml"
    if manifest_path.is_file():
        results.append(validate_policy_adoption_cohort_manifest(manifest_path, records_dir))
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


if __name__ == "__main__":
    import sys

    _repo_root = Path(__file__).resolve().parent
    _profile_result = validate_sleeve_profile_directory(
        _repo_root / _PROFILES_DIR, repo_root=_repo_root,
    )
    _relationship_result = validate_sleeve_relationship_directory(
        _repo_root / _RELATIONSHIPS_DIR, repo_root=_repo_root,
    )
    _policy_adoption_result = validate_policy_adoption_directory(
        _repo_root / _POLICY_ADOPTION_DIR, repo_root=_repo_root,
    )
    _all_valid = _profile_result.valid and _relationship_result.valid and _policy_adoption_result.valid
    if _all_valid:
        print(
            f"level1_sleeve_synthesis_validator: OK "
            f"({_profile_result.record_count} profile result(s), "
            f"{_relationship_result.record_count} relationship result(s), "
            f"{_policy_adoption_result.record_count} policy_adoption result(s))"
        )
        sys.exit(0)
    else:
        print("level1_sleeve_synthesis_validator: FAILED")
        for _r in (*_profile_result.results, *_relationship_result.results, *_policy_adoption_result.results):
            if not _r.valid:
                for _err in _r.errors:
                    print(f"  - [{_r.source}] {_err}")
        sys.exit(1)
