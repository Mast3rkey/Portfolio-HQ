"""
recommendation_validator.py -- read-only schema validator for the WS-0005
Milestone 8 policy-recommendation package
(`intelligence/recommendations/MILESTONE8_POLICY_RECOMMENDATION_PACKAGE.yaml`),
authorized by
`governance/decisions/TIER-0009-ws0005-milestone8-policy-recommendation-framework-authorization.md`.

Scope, exactly what is validated (TIER-0009 SSG-SSJ):

- Source-of-truth convention: one retained YAML artifact covering all 27
  sealed canonical equities, `recommendations:` a list of exactly 27 entries
  in deterministic alphabetical ticker order, no duplicates, no ticker
  outside the current canonical universe.
- Each ticker entry carries exactly the closed set of top-level keys TIER-0009
  SS I.1 requires (`ticker`, `milestone7_reference`, `policy_areas`,
  `uncertainty`) -- no missing key, no extra key.
- `policy_areas` carries exactly the eight named areas (TIER-0009 SS A/SS G):
  `role`, `tier_architecture`, `capital_priority`, `target_and_range`,
  `maximum_position_size`, `overlap_and_concentration`,
  `monitoring_and_thesis_break`, `add_hold_trim_exit_discipline` -- no
  missing area, no extra area.
- Each area-entry carries exactly `primary_status`, `secondary_conditions`,
  `rationale`, `supporting_evidence`, `later_governance_action` (TIER-0009
  SS I.1) -- no missing key, no extra key.
- `primary_status` (TIER-0009 SS H): exactly one of the closed seven-value
  vocabulary, restricted per area to the subset TIER-0009 SS G actually
  permits for that specific area (e.g. `target_and_range` and
  `maximum_position_size` may only ever be `valuation_required`).
- `secondary_conditions` (TIER-0009 SS H): a list of zero to two values
  drawn from the closed set `unresolved_evidence` / `structural_measurement_gap`,
  no duplicates. `overlap_and_concentration` may never carry
  `structural_measurement_gap` as a secondary flag -- for that area the
  identical gap is the *primary*-status-forcing condition (TIER-0009 SS H,
  the G.6 contrast example), never a secondary annotation.
- G.4/G.5 forced abstention (TIER-0009 SS G.4/SS G.5/SS I.3.c): every one of
  the 27 tickers must carry `primary_status: valuation_required` on both
  `target_and_range` and `maximum_position_size`, with no exception --
  mechanically verified, not left to per-ticker judgment.
- G.6 live-recomputed structural-gap assignment (TIER-0009 SS G.6/SS I.3.d):
  the set of tickers carrying `primary_status: relationship_measurement_required`
  on `overlap_and_concentration` is independently recomputed live from
  `targets.yaml` `caps.clusters`, `issuer_lookthrough.yaml`, and
  `intelligence/relationships/*.yaml` at validation time -- cross-checked
  against the artifact, not merely against the artifact's own cached claim
  (the same anti-drift discipline `REL-0007` applied when it found
  `TIER-0002`'s own cached count stale).
- Prohibited content (TIER-0009 SS D/SS G.4/SS G.5/SS G.8/SS J), scanned
  independently on every free-text field within each ticker entry (never on
  top-level metadata, which must be free to name the eight areas by title --
  matching `reconciliation_validator.py`'s own established scope precedent
  of scanning ticker-entry content, not artifact-level prose):
  - forbidden KEY NAMES anywhere in a ticker entry's structure (a *smuggled
    numeric field*, not a prose word) -- `proposed_target_pct`,
    `proposed_target`, `recommended_target_pct`, `target_range`, `score`,
    `conviction_score`, `rank`, `ranking`, `recommendation`, `buy_sell_hold`;
  - forbidden recommendation-shaped TEXT PATTERNS (a proposed number or an
    explicit buy/sell/trim recommendation phrase);
  - numeric-percent-shaped tokens, scoped to the two inherently-numeric
    areas (`target_and_range`, `maximum_position_size`) specifically --
    those two areas must never carry a ticker-specific percentage of any
    kind, since their `primary_status` is doctrinally fixed and their
    `rationale` is universal, not ticker-derived;
  - directive-language (TIER-0009 SS G.8(6)/SS J): the bare words `buy`,
    `sell`, `add`, `hold` (as a verb, word-boundary-matched so it never
    flags the noun "holdings"), `trim`, `exit`, `wait`, `stage` must never
    appear anywhere in any ticker entry's free-text content, in any area,
    under any framing -- this repository's own generated content is
    required to describe the *absence* of a directive without using the
    literal directive vocabulary (e.g. "no directional instruction ... is
    issued", never "no buy/sell action");
  - chart-derived terminology (TIER-0009 SS D/SS F/SS I.3.e): an
    independent free-text scan -- not merely reliance on the self-declared
    `chart_evidence_used` flag, the exact disclosed MINOR defense-in-depth
    gap `TIER-0007`/`TIER-0008` SS B.1 left open and this filing is
    required not to repeat -- for raw indicator names and chart-technical
    phrases (support/resistance, breakout, trend line, moving average, RSI,
    MACD, candlestick, chart pattern, technical analysis, oversold,
    overbought, Fibonacci, volume profile, price target, momentum).
- Top-level metadata: `governing_decision: TIER-0009`, a `source_main_sha`
  (exact comparison-source commit), `milestone_references` naming both
  TIER-0006 (Milestone 6 sealing) and TIER-0008 (Milestone 7 completion),
  `integrity_checks_performed`, `chart_evidence_used: false` (independently
  re-verified, not merely trusted), `equity_scope_disclosure` (TIER-0009
  SS E.2's exact required statement, present in substance), `cohort_size: 27`.
- Aggregate reconciliation (TIER-0009 SS I): the `aggregate` section's
  per-area primary/secondary ticker lists are independently recomputed from
  the raw `recommendations` entries and must match exactly -- no drift, no
  merged/portfolio-wide score.
- Determinism: `validate_recommendation_data` is a pure function of its
  input with no reliance on wall-clock time, randomness, or generation
  order; running it twice on the same data structure produces byte-for-byte
  identical `ValidationResult` content (see `test_recommendation_validator.py`).

This module never opens `intelligence/classification/*.yaml`,
`COHORT_MANIFEST.yaml`, or
`intelligence/reconciliation/MILESTONE7_BASELINE_RECONCILIATION.yaml` in
write mode, never creates a directory, and has zero import relationship
with `allocate.py`, `margin_state.py`, `targets.py`, or any brokerage code
in either direction (see `test_recommendation_validator.py`'s isolation
tests) -- nothing in this repository imports it, and it cannot influence
any allocator recommendation.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

import yaml

_ARTIFACT_FILENAME = "MILESTONE8_POLICY_RECOMMENDATION_PACKAGE.yaml"

_PRIMARY_STATUSES = frozenset(
    {
        "retain_current_baseline",
        "review_warranted",
        "valuation_required",
        "cross_asset_framework_required",
        "relationship_measurement_required",
        "defer_pending_governance",
        "no_policy_conclusion",
    }
)
_SECONDARY_CONDITIONS = frozenset({"unresolved_evidence", "structural_measurement_gap"})

_AREA_KEYS = (
    "role",
    "tier_architecture",
    "capital_priority",
    "target_and_range",
    "maximum_position_size",
    "overlap_and_concentration",
    "monitoring_and_thesis_break",
    "add_hold_trim_exit_discipline",
)

# TIER-0009 SS G: which primary_status values are reachable per area.
_AREA_ALLOWED_PRIMARY = {
    "role": frozenset({"retain_current_baseline", "review_warranted", "no_policy_conclusion"}),
    "tier_architecture": frozenset(
        {"retain_current_baseline", "review_warranted", "defer_pending_governance", "no_policy_conclusion"}
    ),
    "capital_priority": frozenset({"retain_current_baseline", "review_warranted", "no_policy_conclusion"}),
    "target_and_range": frozenset({"valuation_required"}),
    "maximum_position_size": frozenset({"valuation_required"}),
    "overlap_and_concentration": frozenset(
        {"retain_current_baseline", "review_warranted", "relationship_measurement_required", "no_policy_conclusion"}
    ),
    "monitoring_and_thesis_break": frozenset({"retain_current_baseline", "review_warranted", "no_policy_conclusion"}),
    "add_hold_trim_exit_discipline": frozenset(
        {"retain_current_baseline", "review_warranted", "no_policy_conclusion"}
    ),
}

# TIER-0009 SS H: for overlap_and_concentration, structural_measurement_gap is
# the *forcing* primary-status condition, never a secondary annotation.
_AREA_FORBIDDEN_SECONDARY = {
    "overlap_and_concentration": frozenset({"structural_measurement_gap"}),
}

_TICKER_ALLOWED_KEYS = frozenset({"ticker", "milestone7_reference", "policy_areas", "uncertainty"})
_TICKER_REQUIRED_KEYS = _TICKER_ALLOWED_KEYS

_AREA_ENTRY_ALLOWED_KEYS = frozenset(
    {"primary_status", "secondary_conditions", "rationale", "supporting_evidence", "later_governance_action"}
)
_AREA_ENTRY_REQUIRED_KEYS = _AREA_ENTRY_ALLOWED_KEYS

_MILESTONE7_REF_ALLOWED_KEYS = frozenset({"primary_disposition", "secondary_conditions"})
_M7_PRIMARY_DISPOSITIONS = frozenset(
    {"baseline_assumption_stale", "divergence_requires_review", "aligned", "no_policy_conclusion"}
)

_TOP_LEVEL_ALLOWED_KEYS = frozenset(
    {
        "schema_version",
        "governing_decision",
        "artifact_purpose",
        "source_main_sha",
        "milestone_references",
        "integrity_checks_performed",
        "chart_evidence_used",
        "equity_scope_disclosure",
        "generation_date",
        "cohort_size",
        "recommendations",
        "aggregate",
    }
)
_TOP_LEVEL_REQUIRED_KEYS = _TOP_LEVEL_ALLOWED_KEYS

_REQUIRED_MILESTONE_REF_KEYS = frozenset(
    {
        "milestone6_governing_decision",
        "milestone6_sealed_at_merge_commit",
        "milestone7_governing_decision",
        "milestone7_artifact",
        "milestone7_source_main_sha",
    }
)

_KNOWN_TIER0006_MERGE_COMMIT = "1107c5b70801ff5e7027efddf6a2aa916030dce2"

_EQUITY_SCOPE_REQUIRED_SUBSTRING = "27 canonical equity destinations only"

# TIER-0009 SS I.3.e / SS D / SS J: forbidden dict KEY names anywhere inside a
# ticker entry -- a structural smuggled numeric/score/rank field, never a
# prose word (bare "score"/"rank"/"ranking" remain legitimate English inside
# a sentence that *describes the prohibition itself*, e.g. "no ... ranking is
# performed" -- only the literal key name is banned, matching
# reconciliation_validator.py's own established design).
_FORBIDDEN_KEY_NAMES = frozenset(
    {
        "proposed_target_pct",
        "proposed_target",
        "recommended_target_pct",
        "target_range",
        "score",
        "conviction_score",
        "rank",
        "ranking",
        "recommendation",
        "buy_sell_hold",
    }
)

_FORBIDDEN_TEXT_PATTERNS = [
    re.compile(p, re.IGNORECASE)
    for p in [
        r"\bshould\s+be\s+(increased|decreased|raised|lowered|set)\s+to\b",
        r"\brecommend(?:ed|s|ing)?\s+(a\s+)?(target|weight|allocation|position\s+size)\s+of\b",
        r"\bnew\s+target\s+(pct|percent|percentage|range)\b",
        r"\bbuy\s+recommendation\b",
        r"\bsell\s+recommendation\b",
        r"\btrim\s+recommendation\b",
    ]
]

# TIER-0009 SS G.8(6)/SS J: directive words must never appear as an actual
# directive, in any area, under any framing. Word-boundary matched so "hold"
# never flags the noun "holdings", and "exit"/"add"/"wait"/"stage" never
# false-positive on unrelated substrings. Scoped to ticker-entry free text
# only (never top-level metadata, which must be free to name the eighth
# policy area, "add/hold/trim/exit-review discipline", by title).
_DIRECTIVE_WORDS = ("buy", "sell", "add", "hold", "trim", "exit", "wait", "stage")
_DIRECTIVE_PATTERNS = [re.compile(rf"\b{w}\b", re.IGNORECASE) for w in _DIRECTIVE_WORDS]

# TIER-0009 SS D/SS F/SS I.3.e: chart-derived terminology, independently
# scanned (not merely the self-declared chart_evidence_used flag) -- learning
# from reconciliation_validator.py's own disclosed MINOR gap
# (TIER-0007/TIER-0008 SS B.1) rather than repeating it.
_CHART_TERMS = (
    "support",
    "resistance",
    "breakout",
    "trend line",
    "trendline",
    "moving average",
    "rsi",
    "macd",
    "candlestick",
    "chart pattern",
    "technical analysis",
    "oversold",
    "overbought",
    "fibonacci",
    "volume profile",
    "price target",
    "momentum",
)


def _chart_pattern(term: str) -> re.Pattern:
    if " " in term:
        return re.compile(re.escape(term), re.IGNORECASE)
    return re.compile(rf"\b{re.escape(term)}\b", re.IGNORECASE)


_CHART_PATTERNS = [(t, _chart_pattern(t)) for t in _CHART_TERMS]

# TIER-0009 SS G.4/SS G.5: these two areas must never carry a ticker-specific
# percentage of any kind -- the scan is scoped to them specifically, matching
# how the rest of the artifact (uncertainty, other areas' rationale) may
# legitimately cite already-disclosed financial percentages inherited
# faithfully from Milestone 7 (e.g. revenue-mix, growth-rate, customer-
# concentration facts), exactly as Milestone 7's own accepted content does.
_PERCENT_RESTRICTED_AREAS = frozenset({"target_and_range", "maximum_position_size"})
_PERCENT_TOKEN_RE = re.compile(r"\d+(\.\d+)?\s*%")


@dataclass
class ValidationResult:
    valid: bool
    errors: list[str] = field(default_factory=list)
    source: str = ""


def _non_empty_str(value: object) -> bool:
    return isinstance(value, str) and value.strip() != ""


def _reject_unknown_keys(
    value: object, allowed: frozenset[str], required: frozenset[str], label: str, errors: list[str]
) -> None:
    if not isinstance(value, dict):
        errors.append(f"{label} must be a mapping")
        return
    unknown = set(value.keys()) - allowed
    if unknown:
        errors.append(f"{label} contains unexpected key(s) {sorted(unknown)} -- schema is closed, only {sorted(allowed)} are permitted")
    missing = required - set(value.keys())
    if missing:
        errors.append(f"{label} is missing required key(s) {sorted(missing)}")


def _scan_forbidden_keys(value: object, path: str, errors: list[str]) -> None:
    if isinstance(value, dict):
        for k, v in value.items():
            key_str = str(k)
            if key_str in _FORBIDDEN_KEY_NAMES:
                errors.append(f"{path}.{key_str}: forbidden key name -- Milestone 8 may not introduce a numeric target/range/score/ranking field")
            _scan_forbidden_keys(v, f"{path}.{key_str}", errors)
    elif isinstance(value, list):
        for i, item in enumerate(value):
            _scan_forbidden_keys(item, f"{path}[{i}]", errors)


def _scan_free_text_strings(value: object, path: str, errors: list[str], *, scan_percent: bool) -> None:
    """Recursively scan free-text string values for forbidden recommendation-
    shaped phrases, directive language, and chart-derived terminology.
    `scan_percent` gates the numeric-percent-token check, applied only within
    the two doctrinally-fixed areas (TIER-0009 SS G.4/SS G.5)."""
    if isinstance(value, dict):
        for k, v in value.items():
            _scan_free_text_strings(v, f"{path}.{k}", errors, scan_percent=scan_percent)
    elif isinstance(value, list):
        for i, item in enumerate(value):
            _scan_free_text_strings(item, f"{path}[{i}]", errors, scan_percent=scan_percent)
    elif isinstance(value, str):
        for pattern in _FORBIDDEN_TEXT_PATTERNS:
            if pattern.search(value):
                errors.append(f"{path}: contains forbidden recommendation-shaped phrase matching {pattern.pattern!r}")
        for pattern in _DIRECTIVE_PATTERNS:
            if pattern.search(value):
                errors.append(f"{path}: contains directive word {pattern.pattern!r} -- TIER-0009 SS G.8(6)/SS J prohibits directive language in any area, under any framing")
        for term, pattern in _CHART_PATTERNS:
            if pattern.search(value):
                errors.append(f"{path}: contains chart-derived terminology {term!r} -- TIER-0009 SS D/SS F prohibits chart evidence of any kind")
        if scan_percent and _PERCENT_TOKEN_RE.search(value):
            errors.append(f"{path}: contains a numeric-percent-shaped token -- TIER-0009 SS G.4/SS G.5 forbid any ticker-specific percentage in this area")


def validate_area_entry(entry: object, *, ticker: str, area: str, errors: list[str]) -> None:
    label = f"{ticker}.policy_areas.{area}"
    if not isinstance(entry, dict):
        errors.append(f"{label} must be a mapping")
        return

    _reject_unknown_keys(entry, _AREA_ENTRY_ALLOWED_KEYS, _AREA_ENTRY_REQUIRED_KEYS, label, errors)

    primary = entry.get("primary_status")
    if primary not in _PRIMARY_STATUSES:
        errors.append(f"{label}.primary_status {primary!r} is not one of {sorted(_PRIMARY_STATUSES)}")
    else:
        allowed_for_area = _AREA_ALLOWED_PRIMARY[area]
        if primary not in allowed_for_area:
            errors.append(f"{label}.primary_status {primary!r} is not reachable for area {area!r} -- TIER-0009 SS G restricts this area to {sorted(allowed_for_area)}")

    secondary = entry.get("secondary_conditions")
    if not isinstance(secondary, list):
        errors.append(f"{label}.secondary_conditions must be a list")
    else:
        if len(secondary) > 2:
            errors.append(f"{label}.secondary_conditions has {len(secondary)} values -- maximum is two")
        if len(secondary) != len(set(secondary)):
            errors.append(f"{label}.secondary_conditions contains duplicate value(s)")
        unknown_secondary = set(secondary) - _SECONDARY_CONDITIONS
        if unknown_secondary:
            errors.append(f"{label}.secondary_conditions contains unknown value(s) {sorted(unknown_secondary)} -- only {sorted(_SECONDARY_CONDITIONS)} are permitted")
        forbidden_for_area = _AREA_FORBIDDEN_SECONDARY.get(area, frozenset())
        overlap_forbidden = set(secondary) & forbidden_for_area
        if overlap_forbidden:
            errors.append(f"{label}.secondary_conditions contains {sorted(overlap_forbidden)} -- forbidden as a secondary flag for area {area!r} (TIER-0009 SS H: this gap forces the primary status directly for this area, it is never a secondary annotation)")

    if not _non_empty_str(entry.get("rationale")):
        errors.append(f"{label}.rationale must be a non-empty string")

    supporting = entry.get("supporting_evidence")
    if not isinstance(supporting, list) or not supporting or not all(_non_empty_str(s) for s in supporting):
        errors.append(f"{label}.supporting_evidence must be a non-empty list of non-empty citation strings")

    later = entry.get("later_governance_action")
    if not _non_empty_str(later):
        errors.append(f"{label}.later_governance_action must be a non-empty string")
    elif primary in _PRIMARY_STATUSES and primary != "retain_current_baseline":
        if later.strip().lower().startswith("none"):
            errors.append(f"{label}.later_governance_action must name a real future action when primary_status is not retain_current_baseline (got {later!r})")


def validate_ticker_entry(entry: object, *, index: int) -> ValidationResult:
    errors: list[str] = []
    label = f"recommendations[{index}]"

    if not isinstance(entry, dict):
        return ValidationResult(valid=False, errors=[f"{label} must be a mapping"], source=label)

    _reject_unknown_keys(entry, _TICKER_ALLOWED_KEYS, _TICKER_REQUIRED_KEYS, label, errors)

    ticker = entry.get("ticker")
    if not _non_empty_str(ticker):
        errors.append(f"{label}.ticker must be a non-empty string")
        ticker = f"<entry {index}>"

    m7ref = entry.get("milestone7_reference")
    if not isinstance(m7ref, dict):
        errors.append(f"{ticker}.milestone7_reference must be a mapping")
    else:
        unknown = set(m7ref.keys()) - _MILESTONE7_REF_ALLOWED_KEYS
        if unknown:
            errors.append(f"{ticker}.milestone7_reference contains unexpected key(s) {sorted(unknown)}")
        missing = _MILESTONE7_REF_ALLOWED_KEYS - set(m7ref.keys())
        if missing:
            errors.append(f"{ticker}.milestone7_reference is missing required key(s) {sorted(missing)}")
        disp = m7ref.get("primary_disposition")
        if disp not in _M7_PRIMARY_DISPOSITIONS:
            errors.append(f"{ticker}.milestone7_reference.primary_disposition {disp!r} is not one of {sorted(_M7_PRIMARY_DISPOSITIONS)}")
        m7sec = m7ref.get("secondary_conditions")
        if not isinstance(m7sec, list) or not all(s in _SECONDARY_CONDITIONS for s in (m7sec or [])):
            errors.append(f"{ticker}.milestone7_reference.secondary_conditions must be a list drawn from {sorted(_SECONDARY_CONDITIONS)}")

    if not _non_empty_str(entry.get("uncertainty")):
        errors.append(f"{ticker}.uncertainty must be a non-empty string")

    areas = entry.get("policy_areas")
    if not isinstance(areas, dict):
        errors.append(f"{ticker}.policy_areas must be a mapping")
        areas = {}
    else:
        unknown_areas = set(areas.keys()) - set(_AREA_KEYS)
        if unknown_areas:
            errors.append(f"{ticker}.policy_areas contains unexpected area(s) {sorted(unknown_areas)} -- only {list(_AREA_KEYS)} are permitted")
        missing_areas = set(_AREA_KEYS) - set(areas.keys())
        if missing_areas:
            errors.append(f"{ticker}.policy_areas is missing required area(s) {sorted(missing_areas)}")

    for area in _AREA_KEYS:
        if area in areas:
            validate_area_entry(areas[area], ticker=str(ticker), area=area, errors=errors)

    # Prohibited-content scan: scoped to this ticker entry's own free text,
    # never top-level artifact metadata (TIER-0009 SS I -- the latter must be
    # free to name the eight areas by title, e.g. in artifact_purpose).
    _scan_forbidden_keys(entry, ticker, errors)
    for area in _AREA_KEYS:
        if area in areas and isinstance(areas[area], dict):
            for field_name, field_value in areas[area].items():
                _scan_free_text_strings(
                    field_value,
                    f"{ticker}.policy_areas.{area}.{field_name}",
                    errors,
                    scan_percent=area in _PERCENT_RESTRICTED_AREAS,
                )
    if _non_empty_str(entry.get("uncertainty")):
        _scan_free_text_strings(entry["uncertainty"], f"{ticker}.uncertainty", errors, scan_percent=False)

    return ValidationResult(valid=not errors, errors=errors, source=str(ticker))


def _recompute_unmeasured_tickers(repo_root: Path, canonical_universe: frozenset[str]) -> frozenset[str]:
    """Live recomputation of the structural-measurement-gap set (TIER-0009
    SS G.6/SS I.3.d) from the three governed coverage mechanisms -- cluster-cap
    membership, issuer-look-through membership, and relationship-record
    coverage -- reproducing REL-0007's own independently-derived 11-name
    finding. Never trusts the artifact's own cached claim."""
    measured: set[str] = set()

    targets_path = repo_root / "targets.yaml"
    if targets_path.is_file():
        try:
            targets_data = yaml.safe_load(targets_path.read_text())
        except yaml.YAMLError:
            targets_data = None
        if isinstance(targets_data, dict):
            clusters = ((targets_data.get("caps") or {}).get("clusters")) or []
            for cluster in clusters:
                if isinstance(cluster, dict):
                    measured.update(cluster.get("tickers") or [])

    issuer_path = repo_root / "issuer_lookthrough.yaml"
    if issuer_path.is_file():
        try:
            issuer_data = yaml.safe_load(issuer_path.read_text())
        except yaml.YAMLError:
            issuer_data = None
        if isinstance(issuer_data, dict):
            for issuer_entry in issuer_data.get("issuers") or []:
                if isinstance(issuer_entry, dict) and _non_empty_str(issuer_entry.get("ticker")):
                    measured.add(issuer_entry["ticker"])

    rel_dir = repo_root / "intelligence" / "relationships"
    if rel_dir.is_dir():
        for rel_file in rel_dir.glob("*.yaml"):
            try:
                rel_data = yaml.safe_load(rel_file.read_text())
            except yaml.YAMLError:
                continue
            if isinstance(rel_data, dict):
                measured.update(rel_data.get("tickers") or [])

    return frozenset(t for t in canonical_universe if t not in measured)


def _check_forced_and_live_recompute(
    rows: list[dict], *, canonical_universe: frozenset[str], repo_root: Path | None, errors: list[str]
) -> None:
    for entry in rows:
        if not isinstance(entry, dict):
            continue
        ticker = entry.get("ticker")
        areas = entry.get("policy_areas")
        if not isinstance(areas, dict) or not _non_empty_str(ticker):
            continue
        for area in ("target_and_range", "maximum_position_size"):
            area_entry = areas.get(area)
            if isinstance(area_entry, dict) and area_entry.get("primary_status") != "valuation_required":
                errors.append(
                    f"{ticker}.policy_areas.{area}.primary_status must be exactly 'valuation_required' for every one of the 27 tickers, with no exception (TIER-0009 SS G.4/SS G.5/SS I.3.c)"
                )

    if repo_root is None:
        return

    # The live recompute is independent of population/order checks -- it
    # only needs the set of tickers actually present in this artifact, not
    # an externally supplied full canonical universe (which may be absent in
    # a synthetic single-ticker fixture under test).
    present_tickers = frozenset(
        entry["ticker"]
        for entry in rows
        if isinstance(entry, dict) and _non_empty_str(entry.get("ticker"))
    )
    recompute_universe = canonical_universe | present_tickers if canonical_universe else present_tickers
    if not recompute_universe:
        return

    live_unmeasured = _recompute_unmeasured_tickers(repo_root, recompute_universe)
    for entry in rows:
        if not isinstance(entry, dict):
            continue
        ticker = entry.get("ticker")
        areas = entry.get("policy_areas")
        if not isinstance(areas, dict) or not _non_empty_str(ticker) or ticker not in recompute_universe:
            continue
        overlap_entry = areas.get("overlap_and_concentration")
        if not isinstance(overlap_entry, dict):
            continue
        status = overlap_entry.get("primary_status")
        should_be_forced = ticker in live_unmeasured
        is_forced = status == "relationship_measurement_required"
        if should_be_forced and not is_forced:
            errors.append(
                f"{ticker}.policy_areas.overlap_and_concentration.primary_status must be 'relationship_measurement_required' -- {ticker} is live-recomputed as structurally unmeasured (TIER-0009 SS G.6/SS I.3.d), got {status!r}"
            )
        if is_forced and not should_be_forced:
            errors.append(
                f"{ticker}.policy_areas.overlap_and_concentration.primary_status is 'relationship_measurement_required' but {ticker} is live-recomputed as structurally measured -- stale forcing, drift against current targets.yaml/issuer_lookthrough.yaml/intelligence/relationships/ state"
            )


def _recompute_aggregate(rows: list[dict]) -> dict:
    primary_values = sorted(_PRIMARY_STATUSES)
    secondary_values = sorted(_SECONDARY_CONDITIONS)
    primary_counts: dict[str, dict[str, list[str]]] = {area: {pv: [] for pv in primary_values} for area in _AREA_KEYS}
    secondary_counts: dict[str, dict[str, list[str]]] = {area: {sv: [] for sv in secondary_values} for area in _AREA_KEYS}
    for entry in rows:
        if not isinstance(entry, dict):
            continue
        ticker = entry.get("ticker")
        areas = entry.get("policy_areas")
        if not _non_empty_str(ticker) or not isinstance(areas, dict):
            continue
        for area in _AREA_KEYS:
            area_entry = areas.get(area)
            if not isinstance(area_entry, dict):
                continue
            primary = area_entry.get("primary_status")
            if primary in primary_counts[area]:
                primary_counts[area][primary].append(ticker)
            for sv in area_entry.get("secondary_conditions") or []:
                if sv in secondary_counts[area]:
                    secondary_counts[area][sv].append(ticker)
    return {"per_area_primary_status_counts": primary_counts, "per_area_secondary_condition_counts": secondary_counts}


def _check_aggregate_reconciles(data: dict, rows: list[dict], errors: list[str]) -> None:
    aggregate = data.get("aggregate")
    if not isinstance(aggregate, dict):
        errors.append("aggregate must be a mapping")
        return

    if not _non_empty_str(aggregate.get("cross_tabulation_disclaimer")):
        errors.append("aggregate.cross_tabulation_disclaimer must be a non-empty string")

    recomputed = _recompute_aggregate(rows)
    recorded_primary = aggregate.get("per_area_primary_status_counts")
    recorded_secondary = aggregate.get("per_area_secondary_condition_counts")

    if not isinstance(recorded_primary, dict):
        errors.append("aggregate.per_area_primary_status_counts must be a mapping")
    else:
        for area in _AREA_KEYS:
            recorded = recorded_primary.get(area)
            expected = recomputed["per_area_primary_status_counts"][area]
            if not isinstance(recorded, dict):
                errors.append(f"aggregate.per_area_primary_status_counts.{area} must be a mapping")
                continue
            for pv, expected_tickers in expected.items():
                got = sorted(recorded.get(pv) or [])
                if got != sorted(expected_tickers):
                    errors.append(
                        f"aggregate.per_area_primary_status_counts.{area}.{pv} does not reconcile with raw ticker entries: recorded {got}, recomputed {sorted(expected_tickers)}"
                    )

    if not isinstance(recorded_secondary, dict):
        errors.append("aggregate.per_area_secondary_condition_counts must be a mapping")
    else:
        for area in _AREA_KEYS:
            recorded = recorded_secondary.get(area)
            expected = recomputed["per_area_secondary_condition_counts"][area]
            if not isinstance(recorded, dict):
                errors.append(f"aggregate.per_area_secondary_condition_counts.{area} must be a mapping")
                continue
            for sv, expected_tickers in expected.items():
                got = sorted(recorded.get(sv) or [])
                if got != sorted(expected_tickers):
                    errors.append(
                        f"aggregate.per_area_secondary_condition_counts.{area}.{sv} does not reconcile with raw ticker entries: recorded {got}, recomputed {sorted(expected_tickers)}"
                    )


def validate_recommendation_data(
    data: object,
    *,
    canonical_universe: frozenset[str] = frozenset(),
    sealed_universe: frozenset[str] = frozenset(),
    repo_root: str | Path | None = None,
) -> ValidationResult:
    errors: list[str] = []

    if not isinstance(data, dict):
        return ValidationResult(valid=False, errors=["recommendation artifact must be a mapping"], source=_ARTIFACT_FILENAME)

    unknown_top = set(data.keys()) - _TOP_LEVEL_ALLOWED_KEYS
    if unknown_top:
        errors.append(f"top level contains unexpected key(s) {sorted(unknown_top)} -- only {sorted(_TOP_LEVEL_ALLOWED_KEYS)} are permitted")
    missing_top = _TOP_LEVEL_REQUIRED_KEYS - set(data.keys())
    if missing_top:
        errors.append(f"top level is missing required key(s) {sorted(missing_top)}")

    if data.get("governing_decision") != "TIER-0009":
        errors.append(f"governing_decision must be 'TIER-0009', got {data.get('governing_decision')!r}")

    if not _non_empty_str(data.get("source_main_sha")):
        errors.append("source_main_sha must be a non-empty exact commit SHA")

    if data.get("chart_evidence_used") is not False:
        errors.append("chart_evidence_used must be exactly `false` -- TIER-0009 SS F prohibits chart evidence in Milestone 8")

    if data.get("cohort_size") != 27:
        errors.append(f"cohort_size must be exactly 27, got {data.get('cohort_size')!r}")

    disclosure = data.get("equity_scope_disclosure")
    if not _non_empty_str(disclosure) or _EQUITY_SCOPE_REQUIRED_SUBSTRING not in disclosure:
        errors.append(f"equity_scope_disclosure must be present and contain {_EQUITY_SCOPE_REQUIRED_SUBSTRING!r} in substance (TIER-0009 SS E.2)")

    milestone_refs = data.get("milestone_references")
    if not isinstance(milestone_refs, dict):
        errors.append("milestone_references must be a mapping")
    else:
        missing_refs = _REQUIRED_MILESTONE_REF_KEYS - set(milestone_refs.keys())
        if missing_refs:
            errors.append(f"milestone_references is missing required key(s) {sorted(missing_refs)}")
        if milestone_refs.get("milestone6_governing_decision") != "TIER-0006":
            errors.append("milestone_references.milestone6_governing_decision must be 'TIER-0006'")
        if milestone_refs.get("milestone6_sealed_at_merge_commit") != _KNOWN_TIER0006_MERGE_COMMIT:
            errors.append(f"milestone_references.milestone6_sealed_at_merge_commit does not match the known TIER-0006 merge commit ({_KNOWN_TIER0006_MERGE_COMMIT})")
        if milestone_refs.get("milestone7_governing_decision") != "TIER-0008":
            errors.append("milestone_references.milestone7_governing_decision must be 'TIER-0008'")
        if not _non_empty_str(milestone_refs.get("milestone7_artifact")):
            errors.append("milestone_references.milestone7_artifact must be a non-empty string")
        if not _non_empty_str(milestone_refs.get("milestone7_source_main_sha")):
            errors.append("milestone_references.milestone7_source_main_sha must be a non-empty exact commit SHA")

    integrity = data.get("integrity_checks_performed")
    if not isinstance(integrity, dict) or not integrity:
        errors.append("integrity_checks_performed must be a non-empty mapping")

    rows = data.get("recommendations")
    if not isinstance(rows, list):
        errors.append("recommendations must be a list")
        rows = []

    seen: list[str] = []
    for i, entry in enumerate(rows):
        result = validate_ticker_entry(entry, index=i)
        errors.extend(result.errors)
        if isinstance(entry, dict) and _non_empty_str(entry.get("ticker")):
            seen.append(entry["ticker"])

    if len(seen) != len(set(seen)):
        dupes = sorted({t for t in seen if seen.count(t) > 1})
        errors.append(f"recommendations contains duplicate ticker(s): {dupes}")

    if seen != sorted(seen):
        errors.append("recommendations is not in deterministic alphabetical ticker order")

    target_universe = sealed_universe or canonical_universe
    if target_universe:
        missing = target_universe - set(seen)
        extra = set(seen) - target_universe
        if missing:
            errors.append(f"recommendations is missing required ticker(s): {sorted(missing)}")
        if extra:
            errors.append(f"recommendations contains ticker(s) outside the sealed 27-name population: {sorted(extra)}")

    if len(seen) != 27:
        errors.append(f"recommendations must cover exactly 27 tickers, found {len(seen)}")

    repo_root_path = Path(repo_root) if repo_root is not None else None
    _check_forced_and_live_recompute(
        [e for e in rows if isinstance(e, dict)],
        canonical_universe=(sealed_universe or canonical_universe),
        repo_root=repo_root_path,
        errors=errors,
    )

    if isinstance(rows, list):
        _check_aggregate_reconciles(data, [e for e in rows if isinstance(e, dict)], errors)

    return ValidationResult(valid=not errors, errors=errors, source=_ARTIFACT_FILENAME)


def _read_yaml(path: Path) -> tuple[object, list[str]]:
    try:
        text = path.read_text()
    except OSError as exc:
        return None, [f"could not read {path}: {exc}"]
    try:
        return yaml.safe_load(text), []
    except yaml.YAMLError as exc:
        return None, [f"YAML parse error in {path}: {exc}"]


def validate_recommendation_file(
    path: str | Path,
    *,
    canonical_universe: frozenset[str] = frozenset(),
    sealed_universe: frozenset[str] = frozenset(),
    repo_root: str | Path | None = None,
) -> ValidationResult:
    path = Path(path)
    data, read_errors = _read_yaml(path)
    if read_errors:
        return ValidationResult(valid=False, errors=read_errors, source=str(path))
    return validate_recommendation_data(
        data, canonical_universe=canonical_universe, sealed_universe=sealed_universe, repo_root=repo_root
    )


if __name__ == "__main__":
    import sys

    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from relationship_validator import load_canonical_universe  # noqa: E402

    _repo_root = Path(__file__).resolve().parent
    _canonical = load_canonical_universe(_repo_root)
    _artifact_path = _repo_root / "intelligence" / "recommendations" / _ARTIFACT_FILENAME
    _result = validate_recommendation_file(
        _artifact_path, canonical_universe=_canonical, sealed_universe=_canonical, repo_root=_repo_root
    )
    if _result.valid:
        print("recommendation_validator: OK (27 tickers)")
        sys.exit(0)
    else:
        print("recommendation_validator: FAILED")
        for _err in _result.errors:
            print(f"  - {_err}")
        sys.exit(1)
