"""Read-only XASSET-0016 Level-1 numeric-sizing validator.

The numeric layer never treats a sealed hash or a stored Stage-4 label as
authority by itself.  It first runs the existing Level-1 profile,
relationship, and policy-adoption validators, then independently recomputes
Axis B/Axis C and both numeric triggers from those validated live sources.
"""
from __future__ import annotations

from decimal import Decimal, ROUND_HALF_EVEN
from pathlib import Path
import re
import yaml

from level1_sleeve_synthesis_validator import (
    SLEEVE_IDS,
    canonical_record_hash,
    compute_axis_b,
    compute_expected_sizing_readiness,
    compute_live_relationship_ledger,
    validate_policy_adoption_directory,
    validate_sleeve_profile_directory,
    validate_sleeve_relationship_directory,
    _comparative_superiority_scan,
    _prohibited_content_scan,
    _scan_contender_citation,
    _scan_key_names_recursive,
    _stage4_bounded_conclusion_scan,
    _stage4_numeric_leakage_scan,
)

SCHEMA_VERSION = "1.0"
READY = frozenset({"sizing_conditionally_ready", "sizing_ready"})
BASELINE = Decimal("16.67")
INCREMENT = Decimal("2.00")
PORTFOLIO_TOTAL = Decimal("100.00")
NUMERIC_DIR = "intelligence/level1_sleeve_synthesis/numeric_sizing"
PROFILE_DIR = "intelligence/level1_sleeve_synthesis/profiles"
POLICY_DIR = "intelligence/level1_sleeve_synthesis/policy_adoption"
REL_DIR = "intelligence/level1_sleeve_synthesis/relationships"
STATUS_ASSIGNED = "provisional_target_assigned"
STATUS_BLOCKED = "no_provisional_target_pending_axis_c"
TARGET_CLASS = "provisional_governance_guardrail"
GOVERNING_DECISIONS = ["XASSET-0016", "XASSET-0017"]
GOVERNING_DECISION = "XASSET-0016"
SEALED_AT = "2026-08-12T00:00:00Z"
SHARD_ID = "xasset-0016-level1-numeric-sizing-implementation"
BOUNDARY = "Provisional Level 1 sleeve sizing only; no Level 2 instrument selection or sizing, no adopted policy, and no allocation check is authorized by this record."
REVIEW = "Revisit upon the first governed sizing-challenge risk analysis or targeted backtest, a material sealed-population or relationship-accounting change, or a separately authorized study of the baseline or increment."
UNSIZED_DISCLOSURE = "This residual is capital not yet assigned to any sleeve pending resolution of a blocked sleeve status or additional evidence; it is not the cash_reserve sleeve, not an automatically deployable cash allocation, and is never redistributed without a future governance act."

RECORD_KEYS = frozenset({"schema_version","sleeve_id","policy_adoption_reference","numeric_target_status","provisional_target_pct","starting_baseline_pct","applied_adjustments","governing_rule_ids","target_classification","review_condition","uncertainty_disclosure","comparative_consistency_note","blocking_rationale","sizing_boundary_note","record_status","sealed_at","governing_decisions","drafting_session_or_shard_id","content_sha256","cohort_manifest_entry"})
REF_KEYS = frozenset({"record_path", "referenced_content_sha256"})
ADJ_KEYS = frozenset({"governing_rule_id", "direction", "magnitude_pct", "evidence_ref"})
MANIFEST_KEYS = frozenset({"schema_version","governing_decision","cohort","portfolio_reconciliation"})
ROW_KEYS = frozenset({"sleeve_id","record_path","content_sha256","schema_version","governing_decision","shard_id","sealed_at"})
REC_KEYS = frozenset({"sum_of_assigned_targets_pct","unsized_reserved_capital_pct","reconciliation_identity_holds","unsized_capital_disclosure"})

_NUMERIC_SPECIFIC_TEXT_PATTERNS = tuple(re.compile(p, re.IGNORECASE) for p in (
    # Level-2 amount/percentage in both ordinary and passive/reversed order.
    r"\b[A-Z]{2,5}(?:'s|s)?\b[^.]{0,60}\b(?<!not\s)(?<!never\s)(?<!cannot\s)(?:receives?|gets?|is\s+assigned|was\s+assigned|should\s+receive|should\s+get)\b[^.]{0,40}(?:\d+(?:\.\d+)?\s*%|more\s+capital)",
    r"(?:\d+(?:\.\d+)?\s*%|more\s+capital)[^.]{0,60}\b(?:is|was|should\s+be)\s+(?:assigned|allocated|given)\b[^.]{0,40}\b[A-Z]{2,5}(?:'s|s)?\b",
    # Withdrawn-R1/evidence-quantity reward under forward or reversed order.
    r"\b(?:more|additional|greater)\s+(?:citations?|evidence\s+bases?|documentation|evidence\s+routes?)\b[^.]{0,80}\b(?:deserves?|warrants?|justif(?:y|ies)|earns?|receives?|gets?)\b[^.]{0,30}\b(?:more|larger|higher|additional)\s+(?:capital|target|allocation)\b",
    r"\b(?:more|larger|higher|additional)\s+(?:capital|target|allocation)\b[^.]{0,80}\b(?:because|due\s+to|for)\b[^.]{0,30}\b(?:more|additional|greater)\s+(?:citations?|evidence\s+bases?|documentation|evidence\s+routes?)\b",
    # Explicit attempt to make the prohibited maturity fields numeric inputs.
    r"\b(?:stronger_evidence_maturity|favored_sleeve_id)\b[^.]{0,80}\b(?:increase|decrease|adjust|move|raise|lower|capital|target|allocation)\b",
))

# Numeric sizing legitimately cites its own R2/R3 rule IDs and Level 1/2
# boundary labels.  Those are governed proper nouns rather than amounts, so
# scrub only those exact structural forms before reusing Stage 4's otherwise
# strict numeric-leakage helper.  The fixed four-sleeve comparison-population
# label is likewise schema-required explanatory provenance, not a magnitude.
_NUMERIC_SIZING_STRUCTURAL_TERM_PATTERN = re.compile(
    r"\b(?:Level\s+[12]|R[23]|the\s+four\s+sleeves|level1_sleeve_synthesis)\b",
    re.IGNORECASE,
)
_ZERO_SIZING_INFLUENCE_PATTERN = re.compile(
    r"\bzero\s+(?:numeric\s+)?(?:sizing\s+influence|influence\s+on\s+sizing)\b",
    re.IGNORECASE,
)

_TICKER_TERM = r"[A-Z]{2,5}(?:'s|s)?"
_AMOUNT_TERM = (
    r"(?:more|most|greater|greatest|larger|largest|smaller|smallest|higher|"
    r"highest|lower|lowest|bigger|biggest|additional|extra|priority|first|top|"
    r"dominant|heavier|lighter)"
)
_CAPITAL_TERM = (
    r"(?:capital\s+(?:favorite|preferred|priority)\s+position|"
    r"(?:(?:sleeve|portfolio)\s+)?(?:capital|allocation|weight|weighting|"
    r"share|stake|exposure|slice|portion|position|room|priority)"
    r")"
)
_CHART_TERM = (
    r"(?:chart|setup|signal|pattern|technical\s+(?:structure|picture|setup|signal|pattern)|"
    r"price\s+(?:structure|setup|signal|pattern))"
)
_EVIDENCE_TERM = (
    r"(?:(?:more|broader|greater|additional|stronger)\s+(?:evidence|"
    r"evidentiary\s+support|documentation|support|bases?|citations?)|"
    r"(?:evidence|documentation)\s+(?:breadth|completeness|quantity|count|"
    r"maturity)|(?:more|better)[-\s]+documented\s+sleeve)"
)
_RESIDUAL_TERM = (
    r"(?:residual|remainder|unused\s+(?:capital|reserve|remainder)|remaining\s+"
    r"(?:capital|reserve|remainder)|reserved\s+capital|unsized\s+capital)"
)
_SEMANTIC_GAP = r"[^.;:!?—()]{0,55}"

# Every pattern names the actual prohibited predicate.  Negation is checked
# only at that predicate's own boundary by _semantic_match_is_negated(),
# following the repository's hardened per-claim design: a bare "not"
# elsewhere in a wide natural-language match never shields the assertion.
_NUMERIC_SIZING_SEMANTIC_PATTERNS = tuple(re.compile(p, re.IGNORECASE) for p in (
    # Instrument-first active/passive allocations and relative amounts.
    rf"\b(?:no\s+)?{_TICKER_TERM}\b{_SEMANTIC_GAP}\b(?P<predicate>assigned|allocated|given|awarded|weighted|sized|receives?|gets?|takes?|deserves?|earns?|warrants?|carries?|holds?)\b[^.;:!?—()]{{0,35}}\b(?:the\s+|a\s+|our\s+)?(?:{_AMOUNT_TERM}\s+)?{_CAPITAL_TERM}\b",
    # Amount/allocation first, then destination instrument.
    rf"\b(?:no\s+)?(?:the\s+|a\s+|our\s+)?{_AMOUNT_TERM}\s+{_CAPITAL_TERM}\b{_SEMANTIC_GAP}\b(?P<predicate>belongs?|goes?|flows?|settles?|moves?|allocated|assigned|given|awarded|directed)\b[^.;:!?—()]{{0,30}}\b(?:to\s+|into\s+)?{_TICKER_TERM}\b",
    # Preference, conviction, ranking, and priority assertions.
    rf"\b(?:no\s+)?{_TICKER_TERM}\b{_SEMANTIC_GAP}\b(?P<predicate>favou?red|favorites?|preferred|ranked|ranks?|placed|prioritized)\b[^.;:!?—()]{{0,40}}\b(?:fund|instrument|ticker|coin|holding|sleeve|first|top|highest\s+conviction|for\s+(?:sizing|capital))\b",
    rf"\b(?:no\s+)?(?:instrument|ticker|fund|coin|holding|sleeve)\b{_SEMANTIC_GAP}\b(?P<predicate>favou?red|preferred|ranked|prioritized)\b",
    rf"\b(?:capital|allocation|weight|weighting|share|stake|exposure|sizing\s+preference)\b{_SEMANTIC_GAP}\b(?P<predicate>favors?|favours?|prefers?|prioritizes?)\b[^.;:!?—()]{{0,35}}\b{_TICKER_TERM}\b",
    rf"\b(?:our\s+|the\s+)?(?:capital\s+preference|preferred\s+allocation|favou?red\s+allocation|favorite\s+allocation)\b{_SEMANTIC_GAP}\b(?P<predicate>is|becomes?|remains?)\b\s+(?:not\s+)?(?:the\s+)?{_TICKER_TERM}(?:-heavy)?\b",
    rf"\b(?:no\s+)?(?:the\s+)?(?:ranking|rank|capital[-\s]+priority|sizing\s+preference|composite\s+score)\b{_SEMANTIC_GAP}\b(?P<predicate>places?|puts?|assigns?|gives?|is|follows?|made|drawn|established|reached|asserted)\b[^.;:!?—()]{{0,35}}\b(?:{_TICKER_TERM}|first|top|highest|lowest|price\s+(?:setup|structure))\b",
    # Chart/technical causality, forward and reversed/passive.
    rf"\b(?P<predicate>use|follow|read|consult|apply)(?:s|d|ing)?\b[^.;:!?—()]{{0,35}}\b{_CHART_TERM}\b[^.;:!?—()]{{0,30}}\b(?:to|for)\s+(?:size|sizing|weight|weighting|allocate|allocation)\b[^.;:!?—()]{{0,20}}\b{_TICKER_TERM}\b",
    rf"\b{_CHART_TERM}\b{_SEMANTIC_GAP}\b(?P<predicate>used|followed|read|consulted|applied)\b[^.;:!?—()]{{0,30}}\b(?:to|for)\s+(?:size|sizing|weight|weighting|allocate|allocation)\b[^.;:!?—()]{{0,20}}\b{_TICKER_TERM}\b",
    rf"\b{_CHART_TERM}\b{_SEMANTIC_GAP}\b(?P<predicate>supports?|warrants?|argues?|calls?|drives?|determines?|dictates?|makes?|sets?|guides?|favors?)\b[^.;:!?—()]{{0,45}}\b(?:{_AMOUNT_TERM}|increas\w*|decreas\w*|siz\w*|allocat\w*|weight\w*|capital|crypto|{_TICKER_TERM})\b",
    rf"\b(?:{_AMOUNT_TERM}\s+)?(?:{_TICKER_TERM}\s+)?(?:allocation|weight|share|stake|exposure|position|sizing\s+preference)\b{_SEMANTIC_GAP}\b(?P<predicate>supported|warranted|driven|determined|guided|favou?red|based|follows?|tracks?|reflects?|uses?|grows?|increases?|decreases?)\b[^.;:!?—()]{{0,30}}\b(?:(?:because\s+of|by|on|from)\s+)?{_CHART_TERM}\b",
    # Withdrawn R1 evidence-quantity/completeness reward.
    rf"\b{_EVIDENCE_TERM}\b{_SEMANTIC_GAP}\b(?P<predicate>warrants?|earns?|supports?|justif(?:y|ies)|deserves?|receives?|gets?|determines?|drives?|gives?|confers?|awards?)\b[^.;:!?—()]{{0,40}}\b(?:the\s+|a\s+)?(?:(?:{_AMOUNT_TERM}\s+)?{_CAPITAL_TERM}|{_TICKER_TERM}\s+(?:{_AMOUNT_TERM}\s+)?{_CAPITAL_TERM})\b",
    rf"\b(?:{_AMOUNT_TERM}\s+){_CAPITAL_TERM}\b{_SEMANTIC_GAP}\b(?P<predicate>follows?|tracks?|reflects?|results?|comes?)\b[^.;:!?—()]{{0,30}}\b{_EVIDENCE_TERM}\b",
    # Residual/remainder settlement and its reversed cash-destination form.
    rf"\b{_RESIDUAL_TERM}\b\s+(?P<predicate>is|equals?|represents?|becomes?|remains?)\s+(?:not\s+)?(?:a\s+|the\s+)?(?:deployable\s+)?cash(?:\s+(?:target|allocation|sleeve))?\b",
    rf"\b{_RESIDUAL_TERM}\b{_SEMANTIC_GAP}\b(?P<predicate>settles?|flows?|goes?|moves?|converts?|deploys?|allocated|assigned|directed)\b[^.;:!?—()]{{0,30}}\b(?:to|into|as)\s+(?:the\s+)?(?:deployable\s+)?cash(?:_reserve|\s+(?:target|allocation|sleeve))?\b",
    rf"\bcash(?:_reserve|\s+(?:target|allocation|sleeve))?\b{_SEMANTIC_GAP}\b(?P<predicate>receives?|gets?|absorbs?|takes?|is|equals?|represents?)\b[^.;:!?—()]{{0,30}}\b(?:the\s+)?{_RESIDUAL_TERM}\b",
    rf"\b(?P<predicate>treat|classify|count|book|deploy|allocate|assign|move|convert)(?:s|ed|ing)?\b[^.;:!?—()]{{0,35}}\b(?:the\s+)?{_RESIDUAL_TERM}\b[^.;:!?—()]{{0,20}}\b(?:to|into|as)\s+(?:deployable\s+)?cash\b",
))

_LOCAL_PREDICATE_NEGATION = re.compile(
    r"(?:\b(?:does|do|did|is|are|was|were|has|have|had|should|must|would|"
    r"will|can|could|may|might)\s+not\s+(?:be\s+)?|\bcannot\s+(?:be\s+)?|"
    r"\bcan't\s+(?:be\s+)?|\bnever\s+(?:be\s+)?)$",
    re.IGNORECASE,
)
_COPULA_PREDICATES = frozenset({"is", "are", "was", "were", "equals", "equal", "represents", "represent", "becomes", "become", "remains", "remain"})

# Round-4 semantic normalization.  The regex families above remain as a
# conservative compatibility layer for the already-governed corpus.  This
# layer closes the more general composition problem exposed by independent
# review: prohibited meaning may be distributed across nominal, passive, or
# reversed word order even when no single surface-form regex spans it.  It
# therefore normalizes bounded clauses into closed subject/action/object role
# families and applies negation to each candidate predicate, never to the
# sentence as a whole.
_SEMANTIC_TOKEN_PATTERN = re.compile(r"[A-Za-z][A-Za-z0-9_]*(?:'[A-Za-z]+)?")
_SEMANTIC_HARD_BOUNDARY = re.compile(r"\s*(?:;|:|—|\(|\))\s*")
_SEMANTIC_SOFT_BOUNDARY = re.compile(
    r"\b(?:but|however|although|while|whereas|yet)\b", re.IGNORECASE
)
_SEMANTIC_CONTRACTIONS = {
    "can't": "can not",
    "cannot": "can not",
    "couldn't": "could not",
    "didn't": "did not",
    "doesn't": "does not",
    "don't": "do not",
    "hadn't": "had not",
    "hasn't": "has not",
    "haven't": "have not",
    "isn't": "is not",
    "mustn't": "must not",
    "shouldn't": "should not",
    "wasn't": "was not",
    "weren't": "were not",
    "won't": "will not",
    "wouldn't": "would not",
}
_KNOWN_LEVEL2_INSTRUMENTS = frozenset({"spy", "vea", "vwo", "btc", "eth", "sol"})
_GENERIC_INSTRUMENT_TERMS = frozenset({"instrument", "ticker", "fund", "coin", "holding"})
_CAPITAL_ROLE_TERMS = frozenset({
    "capital", "allocation", "weight", "share", "stake", "exposure", "slice",
    "portion", "position", "room", "size", "sizing", "sleeve",
})
_RELATIVE_TERMS = frozenset({
    "more", "most", "greater", "greatest", "larger", "largest", "smaller",
    "smallest", "higher", "highest", "lower", "lowest", "bigger", "biggest",
    "additional", "extra", "dominant", "heavier", "lighter", "first", "top",
})
_PREFERENCE_TERMS = frozenset({"prefer", "preference", "favor", "favorite", "priority", "rank", "best"})
_ALLOCATION_PREDICATES = frozenset({
    "allocate", "assign", "give", "receive", "get", "deserve",
    "earn", "warrant", "carry", "hold", "take", "award", "direct", "belong",
    "go", "flow", "settle", "move", "point", "prioritize", "accrue",
})
_CAUSAL_PREDICATES = frozenset({
    "support", "warrant", "argue", "call", "drive", "determine", "dictate",
    "make", "set", "guide", "favor", "prefer", "justify", "earn", "deserve",
    "give", "confer", "award", "follow", "track", "reflect", "use", "base",
    "grow", "influence", "allocate", "assign",
    "receive", "get", "point",
})
_RESIDUAL_PREDICATES = frozenset({
    "be", "equal", "represent", "become", "flow", "settle", "go", "assign",
    "allocate", "deploy", "convert", "move", "direct", "absorb", "receive", "get",
    "take", "book", "classify", "count", "treat",
})
_AUXILIARIES = frozenset({
    "do", "be", "have", "should", "must", "would", "will", "can", "could",
    "may", "might",
})


def _canonical_semantic_token(raw: str) -> str:
    token = raw.lower().replace("’", "'")
    if token.endswith("'s"):
        token = token[:-2]
    families = (
        (r"allocations?", "allocation"),
        (r"allocat(?:e|es|ed|ing)", "allocate"),
        (r"assign\w*", "assign"),
        (r"giv(?:e|es|en|ing)", "give"),
        (r"receiv\w*", "receive"),
        (r"(?:get|gets|got|getting)", "get"),
        (r"(?:weight|weights|weighting)", "weight"),
        (r"weighted", "weight"),
        (r"sizing", "sizing"),
        (r"(?:size|sizes|sized)", "size"),
        (r"deserv\w*", "deserve"),
        (r"earn\w*", "earn"),
        (r"warrant\w*", "warrant"),
        (r"carr(?:y|ies|ied|ying)", "carry"),
        (r"hold\w*", "hold"),
        (r"tak(?:e|es|en|ing)", "take"),
        (r"award\w*", "award"),
        (r"direct\w*", "direct"),
        (r"belong\w*", "belong"),
        (r"(?:go|goes|went|going)", "go"),
        (r"flow\w*", "flow"),
        (r"settl\w*", "settle"),
        (r"mov\w*", "move"),
        (r"point\w*", "point"),
        (r"favorites?", "favorite"),
        (r"favou?r(?:s|ed|ing)?", "favor"),
        (r"preferences?", "preference"),
        (r"prefer(?:s|red|ring)?", "prefer"),
        (r"priorit\w*", "prioritize"),
        (r"rank\w*", "rank"),
        (r"accru\w*", "accrue"),
        (r"support\w*", "support"),
        (r"argu\w*", "argue"),
        (r"call\w*", "call"),
        (r"driv\w*", "drive"),
        (r"determin\w*", "determine"),
        (r"dictat\w*", "dictate"),
        (r"(?:make|makes|making|made)", "make"),
        (r"(?:set|sets|setting)", "set"),
        (r"guid\w*", "guide"),
        (r"justif\w*", "justify"),
        (r"confer\w*", "confer"),
        (r"follow\w*", "follow"),
        (r"track\w*", "track"),
        (r"reflect\w*", "reflect"),
        (r"us(?:e|es|ed|ing)", "use"),
        (r"bas(?:e|es|ed|ing)", "base"),
        (r"grow\w*", "grow"),
        (r"increas\w*", "increase"),
        (r"decreas\w*", "decrease"),
        (r"chang\w*", "change"),
        (r"influenc\w*", "influence"),
        (r"equal\w*", "equal"),
        (r"represent\w*", "represent"),
        (r"becom\w*", "become"),
        (r"deploy\w*", "deploy"),
        (r"convert\w*", "convert"),
        (r"absorb\w*", "absorb"),
        (r"book\w*", "book"),
        (r"classif\w*", "classify"),
        (r"count\w*", "count"),
        (r"treat\w*", "treat"),
        (r"(?:is|are|was|were|be|been|being)", "be"),
        (r"(?:has|have|had)", "have"),
        (r"(?:does|do|did)", "do"),
    )
    for pattern, replacement in families:
        if re.fullmatch(pattern, token):
            return replacement
    return token


def _semantic_units(text: str) -> list[str]:
    normalized = text.replace("’", "'")
    for contraction, expanded in _SEMANTIC_CONTRACTIONS.items():
        normalized = re.sub(rf"\b{re.escape(contraction)}\b", expanded, normalized, flags=re.IGNORECASE)
    units: list[str] = []
    for sentence in re.split(r"(?<=[.!?])\s+", normalized):
        for hard_clause in _SEMANTIC_HARD_BOUNDARY.split(sentence):
            hard_clause = hard_clause.strip(" \t\r\n,.-")
            if not hard_clause:
                continue
            units.append(hard_clause)
            units.extend(
                part.strip(" \t\r\n,.-")
                for part in _SEMANTIC_SOFT_BOUNDARY.split(hard_clause)
                if part.strip(" \t\r\n,.-") and part.strip(" \t\r\n,.-") != hard_clause
            )
    return list(dict.fromkeys(units))


def _semantic_tokens(unit: str) -> tuple[list[str], list[str]]:
    raw = _SEMANTIC_TOKEN_PATTERN.findall(unit)
    return raw, [_canonical_semantic_token(token) for token in raw]


def _instrument_positions(raw: list[str], tokens: list[str]) -> list[int]:
    positions = []
    for index, (surface, token) in enumerate(zip(raw, tokens)):
        bare = surface.replace("’", "'")
        if bare.lower().endswith("'s"):
            bare = bare[:-2]
        if (
            token in _KNOWN_LEVEL2_INSTRUMENTS
            or token in _GENERIC_INSTRUMENT_TERMS
            or (bare.isupper() and 2 <= len(bare) <= 5 and bare not in {"CASH", "LEVEL"})
        ):
            positions.append(index)
    return positions


def _nearest(position: int, candidates: list[int]) -> int | None:
    return min(candidates, key=lambda candidate: abs(candidate - position)) if candidates else None


def _predicate_is_locally_negated(tokens: list[str], predicate: int, subject: int | None = None) -> bool:
    """Bounded compositional negation for normalized propositions.

    Only immediately governed auxiliary/coplanar negation, ``without VERB``,
    an adjacent ``no SUBJECT`` quantifier, or an explicit zero/no outcome can
    suppress a candidate.  ``not only`` and ``not fail to VERB`` therefore do
    not create a waiver, and an unrelated earlier ``not`` is invisible here.
    """
    if subject is not None and subject > 0 and tokens[subject - 1] == "no":
        return True
    if predicate > 0 and tokens[predicate - 1] in {"not", "never", "without"}:
        return not (tokens[predicate - 1] == "not" and predicate < len(tokens) and tokens[predicate] == "only")
    if predicate > 1 and tokens[predicate - 2] in _AUXILIARIES and tokens[predicate - 1] == "not":
        return True
    if (
        predicate > 2
        and tokens[predicate - 3] in _AUXILIARIES
        and tokens[predicate - 2] == "not"
        and tokens[predicate - 1] == "be"
    ):
        return True
    if tokens[predicate] == "be" and predicate + 1 < len(tokens) and tokens[predicate + 1] == "not":
        return True
    if predicate + 1 < len(tokens) and tokens[predicate + 1] in {"no", "zero"}:
        return True
    if tokens[predicate] == "influence" and any(
        token in {"no", "zero"} for token in tokens[max(0, predicate - 3):predicate]
    ):
        return True
    return False


def _evidence_quantity_positions(tokens: list[str]) -> list[int]:
    quantity = {"more", "broader", "greater", "additional", "stronger", "wider", "better"}
    evidence = {"evidence", "documentation", "support", "basis", "bases", "citation", "citations"}
    measures = {"breadth", "completeness", "quantity", "count", "maturity", "volume"}
    positions = []
    for index, token in enumerate(tokens):
        if token in evidence:
            if (index > 0 and tokens[index - 1] in quantity) or (index + 1 < len(tokens) and tokens[index + 1] in measures):
                positions.append(index)
        if token in {"documented", "document"} and index > 0 and tokens[index - 1] in {"more", "better"}:
            positions.append(index)
    return positions


def _chart_positions(tokens: list[str]) -> list[int]:
    positions = [
        index for index, token in enumerate(tokens)
        if token in {"chart", "technical", "setup", "signal", "pattern"}
    ]
    positions.extend(
        index for index in range(len(tokens) - 1)
        if tokens[index] == "price" and tokens[index + 1] in {"structure", "setup", "signal", "pattern"}
    )
    return sorted(set(positions))


def _residual_positions(tokens: list[str]) -> list[int]:
    positions = []
    residual_heads = {"residual", "remainder"}
    modifiers = {"unused", "remaining", "reserved", "unsized", "leftover"}
    objects = {"capital", "reserve", "remainder", "amount", "fund", "funds"}
    for index, token in enumerate(tokens):
        if token in residual_heads:
            positions.append(index)
        elif token in modifiers and index + 1 < len(tokens) and tokens[index + 1] in objects:
            positions.append(index)
    return positions


def _affirmative_candidate(
    tokens: list[str], candidates: list[int], subjects: list[int]
) -> bool:
    for predicate in candidates:
        if not _predicate_is_locally_negated(tokens, predicate, _nearest(predicate, subjects)):
            return True
    return False


def _normalized_semantic_findings(text: str) -> list[str]:
    findings: set[str] = set()
    for unit in _semantic_units(text):
        raw, tokens = _semantic_tokens(unit)
        instruments = _instrument_positions(raw, tokens)
        capital = [i for i, token in enumerate(tokens) if token in _CAPITAL_ROLE_TERMS]
        relative = [i for i, token in enumerate(tokens) if token in _RELATIVE_TERMS]
        preference = [i for i, token in enumerate(tokens) if token in _PREFERENCE_TERMS]
        actions = [i for i, token in enumerate(tokens) if token in _ALLOCATION_PREDICATES]

        if instruments:
            allocation_candidates = list(actions)
            if capital and relative and not actions:
                allocation_candidates.extend(relative)
            if capital and preference:
                allocation_candidates.extend(
                    i for i, token in enumerate(tokens) if token in {"be", "belong", "point"}
                )
            if preference:
                allocation_candidates.extend(
                    copula
                    for copula, token in enumerate(tokens)
                    if token == "be"
                    and any(
                        min(subject, nominal) < copula < max(subject, nominal)
                        and abs(subject - nominal) <= 4
                        for subject in instruments
                        for nominal in preference
                    )
                )
            # A preference/rank verb applied directly to an instrument is
            # prohibited even without an explicit capital noun.  Nominal
            # mentions still require a copular/destination predicate.
            allocation_candidates.extend(
                i for i in preference
                if tokens[i] in {"prefer", "favor", "rank"}
                and (any(subject <= i for subject in instruments) or bool(capital))
            )
            if (
                (capital or preference)
                and _affirmative_candidate(tokens, sorted(set(allocation_candidates)), instruments)
            ):
                findings.add("instrument-allocation-or-ranking")

        charts = _chart_positions(tokens)
        chart_candidates = [i for i, token in enumerate(tokens) if token in _CAUSAL_PREDICATES]
        if charts and (capital or instruments) and _affirmative_candidate(tokens, chart_candidates, charts):
            findings.add("chart-driven-sizing")

        evidence = _evidence_quantity_positions(tokens)
        evidence_candidates = [i for i, token in enumerate(tokens) if token in _CAUSAL_PREDICATES]
        if evidence and (capital or instruments) and _affirmative_candidate(tokens, evidence_candidates, evidence):
            # Explicit zero influence is a disclosure, not a causal claim.
            zero_influence = any(
                tokens[i] == "influence" and "zero" in tokens[max(0, i - 3):i]
                for i in evidence_candidates
            )
            if not zero_influence:
                findings.add("evidence-quantity-sizing")

        residual = _residual_positions(tokens)
        cash = [i for i, token in enumerate(tokens) if token in {"cash", "cash_reserve"}]
        residual_candidates = []
        if residual and cash:
            for index, token in enumerate(tokens):
                if token not in _RESIDUAL_PREDICATES:
                    continue
                if token == "be":
                    # Copular equivalence must connect the two roles; do not
                    # reject lawful "residual and cash are distinct" prose.
                    if not any(
                        min(r, c) < index < max(r, c) for r in residual for c in cash
                    ):
                        continue
                    if any(term in tokens for term in {"distinct", "different", "separate"}):
                        continue
                residual_candidates.append(index)
            if _affirmative_candidate(tokens, residual_candidates, residual + cash):
                findings.add("residual-cash-conflation")
    return sorted(findings)


def _semantic_match_is_negated(match: re.Match) -> bool:
    """True only when negation grammatically binds this match's predicate.

    This deliberately mirrors the hardened repository precedent of checking
    each recognized claim, not granting a sentence/match-wide "not" waiver.
    Subject quantifier negation is accepted only when the matched proposition
    itself starts with ``no``; auxiliary negation must end immediately at the
    predicate; copular equivalence also recognizes ``is not ...`` immediately
    after the copula.
    """
    predicate_start, predicate_end = match.span("predicate")
    before = match.string[match.start():predicate_start]
    if re.match(r"^\s*no\b", before, re.IGNORECASE):
        return True
    if _LOCAL_PREDICATE_NEGATION.search(before):
        return True
    predicate = match.group("predicate").lower()
    after = match.string[predicate_end:match.end()]
    return predicate in _COPULA_PREDICATES and bool(re.match(r"\s+not\b", after, re.IGNORECASE))


def _scrub_locally_negated_semantic_claims(text: str) -> str:
    """Blank only fully recognized claims whose own predicate is negated.

    The reused Stage-4 bounded scan predates numeric sizing's governed need
    to permit explicit non-influence/non-settlement statements.  Scrubbing
    these exact, predicate-local spans before that reused semantic scan keeps
    the older helper from false-rejecting a lawful denial, while the original
    text still goes through strict numeric leakage and every affirmative
    numeric-sizing semantic pattern below.
    """
    chars = list(text)
    for pattern in _NUMERIC_SIZING_SEMANTIC_PATTERNS:
        for match in pattern.finditer(text):
            if _semantic_match_is_negated(match):
                chars[match.start():match.end()] = " " * (match.end() - match.start())
    return "".join(chars)


class SourceValidationError(ValueError):
    """Authoritative Stage-4 source corpus is invalid or incomplete."""


def _load(path: Path):
    with path.open(encoding="utf-8") as f:
        return yaml.safe_load(f)


def _two(value) -> Decimal:
    if isinstance(value, (float, int)) or not re.fullmatch(r"\d+\.\d{2}", str(value)):
        raise ValueError(f"expected YAML string with two-decimal precision, got {value!r}")
    return Decimal(str(value))


def _closed(obj, keys, where, errors):
    if not isinstance(obj, dict):
        errors.append(f"{where} must be a mapping")
        return False
    missing, extra = set(keys) - set(obj), set(obj) - set(keys)
    if missing:
        errors.append(f"{where} missing keys: {sorted(missing)}")
    if extra:
        errors.append(f"{where} extra keys: {sorted(extra)}")
    return not missing


def _source_errors(repo_root: Path) -> list[str]:
    checks = (
        ("profile", validate_sleeve_profile_directory(repo_root / PROFILE_DIR, repo_root=repo_root)),
        ("relationship", validate_sleeve_relationship_directory(repo_root / REL_DIR, repo_root=repo_root)),
        ("policy_adoption", validate_policy_adoption_directory(repo_root / POLICY_DIR, repo_root=repo_root)),
    )
    errors = []
    for kind, result in checks:
        for item in result.results:
            errors.extend(f"{kind} source [{item.source}]: {error}" for error in item.errors)
    return errors


def _validated_sources(repo_root: Path):
    errors = _source_errors(repo_root)
    if errors:
        raise SourceValidationError("\n".join(errors))
    policies = {}
    independently_derived_sizing = {}
    for sid in SLEEVE_IDS:
        policy_path = repo_root / POLICY_DIR / f"{sid}.yaml"
        policy = _load(policy_path)
        profile = _load(repo_root / PROFILE_DIR / f"{sid}.yaml")
        axis_b = compute_axis_b(profile.get("evidence_coverage_profile"))
        ledger = compute_live_relationship_ledger(sid, repo_root)
        sizing = compute_expected_sizing_readiness(
            policy.get("portfolio_function_status"), axis_b, ledger
        )
        # This is deliberately not the stored policy Axis-C field.  The
        # authoritative policy validator above separately rejects any stale
        # stored Axis A/B/C combination.
        independently_derived_sizing[sid] = sizing
        policies[sid] = (policy_path, policy)
    return policies, independently_derived_sizing


def derive(repo_root: Path):
    policies, sizing = _validated_sources(repo_root)
    eligible = sorted(s for s, status in sizing.items() if status in READY)
    # R2's governed field is the policy record's own coverage ledger.  It is
    # safe to read only after the authoritative Stage-4 validator above has
    # proved it byte-for-byte consistent with the live relationship corpus.
    deferred = {
        s: sum(entry["coverage_state"] == "deferred_disclosed" for entry in policies[s][1]["relationship_coverage_ledger"])
        for s in eligible
    }
    breadth = {s: set() for s in eligible}
    rel_refs = {s: [] for s in eligible}
    for path in sorted((repo_root / REL_DIR).glob("*.yaml")):
        if path.name == "COHORT_MANIFEST.yaml":
            continue
        data = _load(path)
        pair = data["sleeve_pair"]
        for sid in (pair["sleeve_a"], pair["sleeve_b"]):
            if sid in breadth:
                breadth[sid].update(data["secondary_conditions"])
                rel_refs[sid].append({
                    "record_path": str(path.relative_to(repo_root)),
                    "referenced_content_sha256": canonical_record_hash(data),
                })
    states = {s: {} for s in eligible}
    for rule, values in (("R2", deferred), ("R3", {s: len(v) for s, v in breadth.items()})):
        lo, hi = min(values.values()), max(values.values())
        for sid, value in values.items():
            states[sid][rule] = (
                "up" if value == lo and list(values.values()).count(lo) == 1
                else "down" if value == hi and list(values.values()).count(hi) == 1
                else None
            )
    output = {}
    for sid in eligible:
        adjustments = []
        for rule in ("R2", "R3"):
            direction = states[sid][rule]
            if direction:
                refs = ([{
                    "record_path": str(policies[sid][0].relative_to(repo_root)),
                    "referenced_content_sha256": canonical_record_hash(policies[sid][1]),
                }] if rule == "R2" else rel_refs[sid])
                adjustments.append({
                    "governing_rule_id": rule,
                    "direction": direction,
                    "magnitude_pct": "2.00",
                    "evidence_ref": refs,
                })
        net = sum(INCREMENT if a["direction"] == "up" else -INCREMENT for a in adjustments)
        output[sid] = {
            "baseline": "16.67",
            "inputs": {
                "R2_deferred_count": deferred[sid],
                "R3_secondary_condition_breadth": len(breadth[sid]),
            },
            "adjustments": adjustments,
            "rules": [a["governing_rule_id"] for a in adjustments],
            "target": str((BASELINE + net).quantize(Decimal("0.01"), rounding=ROUND_HALF_EVEN)),
            "state": states[sid],
        }
    return policies, eligible, output


def _scan_numeric_free_text(text, where, errors, repo_root):
    if not isinstance(text, str):
        return
    semantic_scrubbed = _scrub_locally_negated_semantic_claims(text)
    for finding in _prohibited_content_scan(text):
        errors.append(f"{where} contains prohibited content ({finding})")
    for finding in _comparative_superiority_scan(semantic_scrubbed):
        errors.append(f"{where} contains prohibited content ({finding})")
    for finding in _stage4_bounded_conclusion_scan(semantic_scrubbed, repo_root=repo_root):
        errors.append(f"{where} contains prohibited content ({finding})")
    for finding in _scan_contender_citation(text):
        errors.append(f"{where} contains prohibited content ({finding})")
    scrubbed = _NUMERIC_SIZING_STRUCTURAL_TERM_PATTERN.sub("", text)
    # "zero sizing influence" is a categorical non-influence disclosure,
    # not a governed amount.  Scrub only that closed phrase; every other
    # digit/spelled-cardinal remains subject to Stage-4 numeric leakage.
    scrubbed = _ZERO_SIZING_INFLUENCE_PATTERN.sub("", scrubbed)
    for finding in _stage4_numeric_leakage_scan(scrubbed):
        errors.append(f"{where} contains prohibited content ({finding})")
    for pattern in _NUMERIC_SPECIFIC_TEXT_PATTERNS:
        if pattern.search(text):
            errors.append(f"{where} contains prohibited numeric-sizing content ({pattern.pattern})")
    for pattern in _NUMERIC_SIZING_SEMANTIC_PATTERNS:
        for match in pattern.finditer(text):
            if _semantic_match_is_negated(match):
                continue
            errors.append(f"{where} contains prohibited numeric-sizing semantics ({pattern.pattern})")
    for finding in _normalized_semantic_findings(text):
        errors.append(f"{where} contains prohibited numeric-sizing semantics ({finding})")


def _rule_no_fire_described(text: str, rule: str) -> bool:
    return bool(
        re.search(
            rf"\b{rule}\b[^.;]{{0,55}}\b(?:does\s+not\s+fire|no[-\s]?fire|tie|none)\b",
            text,
            re.IGNORECASE,
        )
        or re.search(
            rf"\bR2\b\s+(?:and|/)\s*\bR3\b[^.;]{{0,20}}\bno[-\s]?fire\b",
            text,
            re.IGNORECASE,
        )
    )


def _rule_direction_described(text: str, rule: str, direction: str) -> bool:
    return bool(re.search(rf"\b{rule}\b[^.;]{{0,55}}\b{direction}\b", text, re.IGNORECASE))


def _rule_bound_directions(text: str, rule: str, sid: str, other: str) -> dict[str, set[str]]:
    """Extract only directions explicitly bound to this sleeve or its peer.

    The accepted disclosure syntax is intentionally small: ``up/down
    here/there``, ``up/down for <named sleeve>``, and their named-sleeve-first
    inversion.  Direction words that merely occur somewhere after a rule ID
    are not authority and are not returned.
    """
    bound = {"self": set(), "other": set()}
    self_names = rf"(?:here|self|{re.escape(sid)}|this\s+sleeve|current\s+sleeve)"
    other_names = rf"(?:there|{re.escape(other)}|that\s+sleeve|other\s+sleeve|their\s+tie)"
    for match in re.finditer(
        rf"\b{rule}\b(?:(?!\bR[23]\b)[^.;]){{0,100}}", text, re.IGNORECASE
    ):
        region = match.group(0)
        for direction_match in re.finditer(
            rf"\b(?P<direction>up|down)\b\s+(?:for\s+)?(?P<location>{self_names}|{other_names})\b",
            region,
            re.IGNORECASE,
        ):
            location = direction_match.group("location")
            key = "self" if re.fullmatch(self_names, location, re.IGNORECASE) else "other"
            bound[key].add(direction_match.group("direction").lower())
    # Named-sleeve-first syntax can place the name before the rule token and
    # therefore outside the rule-forward region above.
    for key, name_pattern in (("self", self_names), ("other", other_names)):
        for match in re.finditer(
            rf"\b{name_pattern}\b\s+(?:has|is|shows?)\s+\b{rule}\b"
            rf"(?:\s+fires?)?\s+(?P<direction>up|down)\b",
            text,
            re.IGNORECASE,
        ):
            bound[key].add(match.group("direction").lower())
    return bound


def _rule_bound_no_fire(text: str, rule: str, sid: str, other: str) -> set[str]:
    bound: set[str] = set()
    self_names = rf"(?:here|self|{re.escape(sid)}|this\s+sleeve|current\s+sleeve)"
    other_names = rf"(?:there|{re.escape(other)}|that\s+sleeve|other\s+sleeve|their\s+tie)"
    for match in re.finditer(
        rf"\b{rule}\b(?:(?!\bR[23]\b)[^.;]){{0,100}}", text, re.IGNORECASE
    ):
        region = match.group(0)
        for state_match in re.finditer(
            rf"\b(?:does\s+not\s+fire|no[-\s]?fire|none)\b(?:\s+for)?\s+(?P<location>{self_names}|{other_names})\b",
            region,
            re.IGNORECASE,
        ):
            location = state_match.group("location")
            bound.add("self" if re.fullmatch(self_names, location, re.IGNORECASE) else "other")
    return bound


def _rule_both_no_fire_described(text: str, rule: str) -> bool:
    return bool(
        re.search(
            rf"\bboth\b[^.;]{{0,55}}\b{rule}\b[^.;]{{0,35}}\b(?:no[-\s]?fire|does\s+not\s+fire|none)\b",
            text,
            re.IGNORECASE,
        )
        or re.search(
            rf"\b{rule}\b[^.;]{{0,45}}\b(?:no[-\s]?fire|does\s+not\s+fire|none)\b[^.;]{{0,20}}\bboth\b",
            text,
            re.IGNORECASE,
        )
    )


def _rule_state_contrast_described(note, clauses, rule, self_state, other_state, sid, other):
    """Verify that prose describes the live trigger-state contrast.

    A bare rule citation (``R2 exists/applies``) is never evidence.  When one
    peer is no-fire and the other fires, the note must establish both sides;
    the sealed grouped form ``R2 fires for those sleeves`` is accepted only
    when the same note also establishes the current sleeve's R2 no-fire state.
    When both fire, each direction must be explicitly bound to the correct
    sleeve; mere co-occurrence of both direction words is insufficient.
    """
    joined = " ".join(clauses)
    directions = _rule_bound_directions(joined, rule, sid, other)
    no_fire = _rule_bound_no_fire(joined, rule, sid, other)
    if self_state == other_state:
        if self_state is None:
            return _rule_both_no_fire_described(joined, rule) and not any(directions.values())
        return directions["self"] == {self_state} and directions["other"] == {other_state}
    if self_state is not None and other_state is not None:
        return (
            directions["self"] == {self_state}
            and directions["other"] == {other_state}
        )
    if self_state is None:
        grouped_other_fire = bool(
            re.search(
                rf"\b{rule}\b[^.;]{{0,35}}\bfires?\s+for\s+(?:that|the|those|other)\s+sleeves?\b",
                joined,
                re.IGNORECASE,
            )
        )
        if any(directions.values()):
            other_fires = (
                directions["other"] == {other_state}
                and not directions["self"]
                and "self" in no_fire
            )
        else:
            other_fires = grouped_other_fire
        return _rule_no_fire_described(note, rule) and other_fires
    return (
        directions["self"] == {self_state}
        and not directions["other"]
        and "other" in no_fire
    )


def _validate_comparative_consistency(sid, note, expected, errors):
    """Require every live comparison assertion to be mechanically auditable.

    Equal-output peers must be named in a no-material-difference clause.  A
    differing peer must be named in a difference clause that cites every R2/R3
    state difference responsible for the output.  This validates provenance;
    it does not infer or trust a stored target.
    """
    if not isinstance(note, str):
        return
    for sleeve, row in expected.items():
        deterministic_target = BASELINE + sum(
            INCREMENT if row["state"][rule] == "up"
            else -INCREMENT if row["state"][rule] == "down"
            else Decimal("0.00")
            for rule in ("R2", "R3")
        )
        if Decimal(row["target"]) != deterministic_target:
            errors.append(
                f"{sleeve}: comparative input target does not match deterministic live R2/R3 arithmetic"
            )
    clauses = [clause.strip() for clause in re.split(r"[.;]", note) if clause.strip()]
    for other in sorted(expected):
        if other == sid:
            continue
        other_pattern = re.compile(rf"\b{re.escape(other)}\b", re.IGNORECASE)
        matching = [clause for clause in clauses if other_pattern.search(clause)]
        if expected[sid]["target"] == expected[other]["target"]:
            equal_clauses = [
                clause for clause in matching
                if re.search(r"\bno\s+material\s+difference\b", clause, re.IGNORECASE)
            ]
            if not equal_clauses:
                errors.append(f"{sid}.comparative_consistency_note must state no material difference from equal-output sleeve {other}")
                continue
            differing_rules = [
                rule for rule in ("R2", "R3")
                if expected[sid]["state"][rule] != expected[other]["state"][rule]
            ]
            for rule in differing_rules:
                if not _rule_state_contrast_described(
                    note,
                    equal_clauses,
                    rule,
                    expected[sid]["state"][rule],
                    expected[other]["state"][rule],
                    sid,
                    other,
                ):
                    errors.append(f"{sid}.comparative_consistency_note must identify the live {rule} state difference from {other}")
            if not differing_rules:
                for rule in ("R2", "R3"):
                    if not _rule_state_contrast_described(
                        note,
                        equal_clauses,
                        rule,
                        expected[sid]["state"][rule],
                        expected[other]["state"][rule],
                        sid,
                        other,
                    ):
                        errors.append(f"{sid}.comparative_consistency_note must identify the shared live {rule} state with {other}")
        else:
            differing_rules = [
                rule for rule in ("R2", "R3")
                if expected[sid]["state"][rule] != expected[other]["state"][rule]
            ]
            if not differing_rules:
                errors.append(
                    f"{sid}.comparative_consistency_note cannot reconcile different targets "
                    f"with identical live R2/R3 states for {other}"
                )
                continue
            difference_clauses = [
                clause for clause in matching
                if re.search(r"\bdiffer(?:s|ed|ent|ence)?\b", clause, re.IGNORECASE)
            ]
            if not difference_clauses:
                errors.append(f"{sid}.comparative_consistency_note must identify its difference from {other}")
                continue
            for rule in differing_rules:
                if not _rule_state_contrast_described(
                    note,
                    difference_clauses,
                    rule,
                    expected[sid]["state"][rule],
                    expected[other]["state"][rule],
                    sid,
                    other,
                ):
                    errors.append(f"{sid}.comparative_consistency_note must identify the live {rule} state contrast from {other}")


def _validate_reconciliation(reconciliation, live_sum: Decimal, errors: list[str]):
    """Production reconciliation path, including defensive reachable and
    currently-unreachable arithmetic cases required by XASSET-0016."""
    if not _closed(reconciliation, REC_KEYS, "portfolio_reconciliation", errors):
        return
    residual = (PORTFOLIO_TOTAL - live_sum).quantize(Decimal("0.01"), rounding=ROUND_HALF_EVEN)
    try:
        stored_sum = _two(reconciliation["sum_of_assigned_targets_pct"])
        stored_residual = _two(reconciliation["unsized_reserved_capital_pct"])
        if stored_sum != live_sum or stored_sum > PORTFOLIO_TOTAL:
            errors.append("manifest assigned sum mismatch/overshoot")
        if stored_residual < 0 or stored_residual != residual:
            errors.append("manifest residual mismatch/negative")
        if stored_sum + stored_residual != PORTFOLIO_TOTAL or reconciliation["reconciliation_identity_holds"] is not True:
            errors.append("manifest reconciliation identity fails")
    except ValueError as exc:
        errors.append(f"manifest: {exc}")
    if reconciliation["unsized_capital_disclosure"] != UNSIZED_DISCLOSURE:
        errors.append("manifest unsized disclosure invalid")


def validate(repo_root: Path) -> list[str]:
    errors = []
    records_dir = repo_root / NUMERIC_DIR
    try:
        policies, eligible, expected = derive(repo_root)
    except (SourceValidationError, OSError, KeyError, TypeError, yaml.YAMLError) as exc:
        return [f"authoritative Stage-4 source validation failed: {exc}"]

    on_disk = {p.stem for p in records_dir.glob("*.yaml") if p.name != "COHORT_MANIFEST.yaml"}
    if on_disk != SLEEVE_IDS:
        errors.append(f"numeric_sizing population mismatch: {sorted(on_disk)}")
    records = {}
    for sid in sorted(on_disk):
        path = records_dir / f"{sid}.yaml"
        data = _load(path)
        records[sid] = data
        if not isinstance(data, dict):
            errors.append(f"{sid}: record must be a mapping")
            continue
        complete = _closed(data, RECORD_KEYS, sid, errors)
        _scan_key_names_recursive(data, sid, errors, allow_keys=frozenset({"provisional_target_pct","starting_baseline_pct","magnitude_pct","target_classification","numeric_target_status"}))
        if sid not in SLEEVE_IDS:
            errors.append(f"{sid}: unauthorized/orphan sleeve_id")
            continue
        if not complete:
            continue
        if data["schema_version"] != SCHEMA_VERSION or data["sleeve_id"] != sid:
            errors.append(f"{sid}: identity/schema mismatch")
        if data["governing_decisions"] != GOVERNING_DECISIONS:
            errors.append(f"{sid}: governing_decisions must be {GOVERNING_DECISIONS!r}")
        if data["sealed_at"] != SEALED_AT:
            errors.append(f"{sid}: sealed_at must be {SEALED_AT!r}")
        if data["drafting_session_or_shard_id"] != SHARD_ID:
            errors.append(f"{sid}: drafting_session_or_shard_id must be {SHARD_ID!r}")
        expected_entry = f"{NUMERIC_DIR}/COHORT_MANIFEST.yaml#{sid}"
        if data["cohort_manifest_entry"] != expected_entry:
            errors.append(f"{sid}: cohort_manifest_entry must be {expected_entry!r}")

        _closed(data["policy_adoption_reference"], REF_KEYS, f"{sid}.policy_adoption_reference", errors)
        policy_path, policy = policies[sid]
        pref = data["policy_adoption_reference"] if isinstance(data["policy_adoption_reference"], dict) else {}
        if pref.get("record_path") != str(policy_path.relative_to(repo_root)) or pref.get("referenced_content_sha256") != canonical_record_hash(policy):
            errors.append(f"{sid}: stale policy_adoption_reference")

        assigned = sid in eligible
        expected_status = STATUS_ASSIGNED if assigned else STATUS_BLOCKED
        if data["numeric_target_status"] != expected_status:
            errors.append(f"{sid}: numeric_target_status not independently live-derived")
        if assigned:
            exp = expected[sid]
            try:
                baseline = _two(data["starting_baseline_pct"])
                target = _two(data["provisional_target_pct"])
                if baseline != BASELINE:
                    errors.append(f"{sid}: wrong baseline")
                if target < Decimal("12.67") or target > Decimal("20.67"):
                    errors.append(f"{sid}: target outside governed generic range")
                if target != Decimal(exp["target"]):
                    errors.append(f"{sid}: target does not match live derivation")
            except ValueError as exc:
                errors.append(f"{sid}: {exc}")
            if data["applied_adjustments"] != exp["adjustments"]:
                errors.append(f"{sid}: adjustments do not match live R2/R3 derivation")
            if data["governing_rule_ids"] != exp["rules"]:
                errors.append(f"{sid}: governing_rule_ids mismatch")
            if (
                not isinstance(data["governing_rule_ids"], list)
                or any(rule not in {"R2", "R3"} for rule in data["governing_rule_ids"])
            ):
                errors.append(f"{sid}: governing_rule_ids contains retired/unknown rule")
            if not isinstance(data["applied_adjustments"], list):
                errors.append(f"{sid}: applied_adjustments must be a list")
            else:
                for i, adjustment in enumerate(data["applied_adjustments"]):
                    label = f"{sid}.applied_adjustments[{i}]"
                    if not _closed(adjustment, ADJ_KEYS, label, errors):
                        continue
                    if adjustment["governing_rule_id"] not in {"R2", "R3"}:
                        errors.append(f"{label}: retired/unknown rule")
                    if adjustment["direction"] not in {"up", "down"}:
                        errors.append(f"{label}: invalid direction")
                    try:
                        if _two(adjustment["magnitude_pct"]) != INCREMENT:
                            errors.append(f"{label}: wrong adjustment magnitude")
                    except ValueError as exc:
                        errors.append(f"{label}: {exc}")
                    refs = adjustment["evidence_ref"]
                    if not isinstance(refs, list) or not refs:
                        errors.append(f"{label}.evidence_ref must be a non-empty list")
                    else:
                        for j, ref in enumerate(refs):
                            _closed(ref, REF_KEYS, f"{label}.evidence_ref[{j}]", errors)
            if data["target_classification"] != TARGET_CLASS:
                errors.append(f"{sid}: target_classification must be {TARGET_CLASS!r}")
            if data["review_condition"] != REVIEW:
                errors.append(f"{sid}: review_condition must be the governed exact condition")
            for field in ("uncertainty_disclosure", "comparative_consistency_note"):
                if not isinstance(data[field], str) or not data[field].strip():
                    errors.append(f"{sid}: {field} must be non-empty")
                else:
                    _scan_numeric_free_text(data[field], f"{sid}.{field}", errors, repo_root)
            _validate_comparative_consistency(
                sid, data["comparative_consistency_note"], expected, errors
            )
            if data["blocking_rationale"] is not None:
                errors.append(f"{sid}: blocking_rationale must be null")
        else:
            nullable = ("provisional_target_pct","starting_baseline_pct","target_classification","review_condition","uncertainty_disclosure","comparative_consistency_note")
            for field in nullable:
                if data[field] is not None:
                    errors.append(f"{sid}: blocked field {field} must be null")
            if data["applied_adjustments"] != [] or data["governing_rule_ids"] != []:
                errors.append(f"{sid}: blocked adjustments/rules must be empty")
            if not isinstance(data["blocking_rationale"], str) or not data["blocking_rationale"].strip():
                errors.append(f"{sid}: blocking_rationale must be non-empty")
            else:
                _scan_numeric_free_text(data["blocking_rationale"], f"{sid}.blocking_rationale", errors, repo_root)
        if data["sizing_boundary_note"] != BOUNDARY:
            errors.append(f"{sid}: sizing_boundary_note must be the governed exact boundary")
        if data["record_status"] != "sealed":
            errors.append(f"{sid}: record_status must be 'sealed'")
        if canonical_record_hash(data) != data["content_sha256"]:
            errors.append(f"{sid}: content_sha256 mismatch")

    manifest_path = records_dir / "COHORT_MANIFEST.yaml"
    manifest = _load(manifest_path) if manifest_path.is_file() else {}
    if _closed(manifest, MANIFEST_KEYS, "manifest", errors):
        if manifest["schema_version"] != SCHEMA_VERSION:
            errors.append("manifest schema_version mismatch")
        if manifest["governing_decision"] != GOVERNING_DECISION:
            errors.append(f"manifest governing_decision must be {GOVERNING_DECISION!r}")
        cohort = manifest["cohort"]
        if not isinstance(cohort, list):
            errors.append("manifest cohort must be a list")
            cohort = []
        seen = []
        for i, row in enumerate(cohort):
            if not _closed(row, ROW_KEYS, f"manifest.cohort[{i}]", errors):
                continue
            sid = row["sleeve_id"]
            seen.append(sid)
            if row["schema_version"] != SCHEMA_VERSION or row["governing_decision"] != GOVERNING_DECISION or row["shard_id"] != SHARD_ID or row["sealed_at"] != SEALED_AT:
                errors.append(f"manifest row {sid}: governed constants mismatch")
            if sid in records and (row["record_path"] != f"{NUMERIC_DIR}/{sid}.yaml" or row["content_sha256"] != canonical_record_hash(records[sid])):
                errors.append(f"manifest row {sid}: path/hash mismatch")
        if set(seen) != SLEEVE_IDS or len(seen) != len(SLEEVE_IDS):
            errors.append("manifest population duplicate/missing/orphan")
        live_sum = sum(Decimal(expected[s]["target"]) for s in eligible)
        _validate_reconciliation(manifest["portfolio_reconciliation"], live_sum, errors)
    return errors


if __name__ == "__main__":
    root = Path(__file__).resolve().parent
    errs = validate(root)
    if errs:
        print("numeric_sizing_validator: FAILED")
        for error in errs:
            print("  -", error)
        raise SystemExit(1)
    print("numeric_sizing_validator: OK (6 record(s), authoritative Stage-4 and live R2/R3 rederived)")
