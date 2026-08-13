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
    r"\b[A-Z]{2,5}(?:'s|s)?\b[^.]{0,60}\b(?:receives?|gets?|is\s+assigned|was\s+assigned|should\s+receive|should\s+get)\b[^.]{0,40}(?:\d+(?:\.\d+)?\s*%|more\s+capital)",
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
    r"(?:chart|technical\s+(?:structure|picture|setup|signal|pattern)|"
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


def _rule_state_contrast_described(note, clauses, rule, self_state, other_state):
    """Verify that prose describes the live trigger-state contrast.

    A bare rule citation (``R2 exists/applies``) is never evidence.  When one
    peer is no-fire and the other fires, the note must establish both sides;
    the sealed grouped form ``R2 fires for those sleeves`` is accepted only
    when the same note also establishes the current sleeve's R2 no-fire state.
    When both fire in opposite directions, both directions must be present.
    """
    joined = " ".join(clauses)
    if self_state == other_state:
        if self_state is None:
            return _rule_no_fire_described(joined, rule)
        return _rule_direction_described(joined, rule, self_state)
    if self_state is not None and other_state is not None:
        return (
            _rule_direction_described(joined, rule, self_state)
            and _rule_direction_described(joined, rule, other_state)
        )
    if self_state is None:
        other_fires = (
            _rule_direction_described(joined, rule, other_state)
            or bool(
                re.search(
                    rf"\b{rule}\b[^.;]{{0,35}}\bfires?\s+for\s+(?:that|the|those|other)\s+sleeves?\b",
                    joined,
                    re.IGNORECASE,
                )
            )
        )
        return _rule_no_fire_described(note, rule) and other_fires
    return (
        _rule_direction_described(joined, rule, self_state)
        and _rule_no_fire_described(joined, rule)
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
