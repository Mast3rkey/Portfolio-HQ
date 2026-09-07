"""valuation_archetype_sanitizer.py -- blind-drafting evidence isolation for WS-0005/WS-0015
valuation-archetype assignment, authorized by VALUATION-0003
(governance/decisions/VALUATION-0003-equity-valuation-archetype-assignment-authorization.md).

Freshly authored for this schema (VALUATION-0003 SS F.2) -- not a copy of
intelligence_classification_sanitizer.py. The prohibited-field set and the
permitted-evidence set both differ from Milestone 6's classification axis, and
this repository's convention is that each Intelligence schema owns its own
sanitizer/validator (XASSET-0002, crypto_classification_validator.py).

Design choice, disclosed: rather than a strip-from-everything (denylist)
approach, this module extracts only VALUATION-0003 SS D's *permitted* evidence
fields (allow-list extraction) from an already whole-key-stripped copy of the
source data, then runs item-level pattern scanning/redaction on the extracted
text as a second layer, then a mechanistically independent third-stage scan
over the assembled packet. Allow-list extraction is a stronger default-deny
posture than a pure strip-list, and is used here in addition to (not instead
of) the whole-key strip and item-level scan/redact SS F.1/F.2 require.

Isolation boundary disclosed per SS F.4 (matching TIER-0004 SS 9.2's and
Milestone 6's own disclosure): this is an INSTRUCTIONAL isolation boundary,
not a filesystem-sandboxed one. A blind-drafting session is handed exactly one
sanitized packet's text and instructed to use nothing else; this module cannot
prove a drafting session did not consult other material before sealing.
"""

from __future__ import annotations

import copy
import hashlib
import json
import re
from dataclasses import dataclass, field

SANITIZER_VERSION = "1.0"

# ---------------------------------------------------------------------------
# SS F.1 -- whole-key strip
# ---------------------------------------------------------------------------

_YAML_STRIP_TOP_LEVEL_KEYS = ("portfolio_role_ref", "conviction", "review")


def strip_yaml_data(data: dict) -> dict:
    """Return a copy of a Company Intelligence YAML mapping with
    portfolio_role_ref, conviction (whole block), and review.log narrative
    (whole `review` block, including cadence/dates -- none of it is permitted
    evidence for this axis) removed wholesale. Never mutates the input."""
    out = copy.deepcopy(data)
    for key in _YAML_STRIP_TOP_LEVEL_KEYS:
        out.pop(key, None)
    return out


# ---------------------------------------------------------------------------
# Forbidden-language detection, shared by the item-level pass and reused
# (as data, not as a shared decision function) by the independent scan.
# ---------------------------------------------------------------------------

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
        r"git diff --check.{0,20}gate",
    ]
]

_BARE_GATE_PATTERN = re.compile(r"\bgates?\b", re.IGNORECASE)
_BARE_CONVICTION_PATTERN = re.compile(r"\bconviction\b", re.IGNORECASE)

_CONFIG_KEY_PATTERNS = [
    re.compile(p, re.IGNORECASE)
    for p in [
        r"portfolio_role_ref",
        r"target_pct",
        r"targets\.yaml",
        r"holdings\.yaml",
        r"gates\.yaml",
        r"next_gate",
        r"allow_add",
        r"issuer_lookthrough\.yaml",
    ]
]

_TARGET_ALLOCATION_PATTERNS = [
    re.compile(p, re.IGNORECASE)
    for p in [
        r"%\s*of\s+(the\s+)?book",
        r"%\s*of\s+portfolio",
        r"target\s+weight",
        r"destination\s+weight",
        r"target\s+percentage",
    ]
]

# Milestone 7/8 finding vocabulary -- should never appear in a Company
# Intelligence business-model narrative anyway (it lives in separate
# reconciliation/recommendations files this sanitizer never reads), scanned
# for defense-in-depth per VALUATION-0003 SS I.
_MILESTONE_FINDING_PATTERNS = [
    re.compile(p, re.IGNORECASE)
    for p in [
        r"primary_disposition",
        r"case_for_review",
        r"maintain_current_weight",
        r"divergence_requires_review",
        r"baseline_assumption_stale",
        r"structural_measurement_gap",
        r"relationship_measurement_required",
    ]
]

_CHART_DOMAIN_PATTERNS = [
    re.compile(p, re.IGNORECASE)
    for p in [
        r"support\s+level",
        r"resistance\s+level",
        r"breakout",
        r"trend\s*line",
        r"moving\s+average",
        r"\brsi\b",
        r"\bmacd\b",
        r"candlestick",
        r"chart\s+pattern",
        r"technical\s+analysis",
        r"oversold",
        r"overbought",
        r"fibonacci",
        r"volume\s+profile",
        r"price\s+target",
        r"momentum\s+(indicator|signal|trade)",
    ]
]


def _strip_legitimate_gate_uses(text: str) -> str:
    out = text
    for pat in _GATE_LEGITIMATE_USE_PATTERNS:
        out = pat.sub("", out)
    return out


def contains_gate_policy_leak(text: str) -> bool:
    """True if `text` contains a bare policy use of gate/gates -- i.e. a
    gate/gates mention that survives removal of every known-legitimate,
    whitelisted technical/process usage."""
    scrubbed = _strip_legitimate_gate_uses(text)
    return bool(_BARE_GATE_PATTERN.search(scrubbed))


def item_text_is_forbidden(text: str) -> bool:
    """Layer-2 (item-level) forbidden-content check, applied to each
    extracted evidence string before it is placed in a drafting packet."""
    if contains_gate_policy_leak(text):
        return True
    if _BARE_CONVICTION_PATTERN.search(text):
        return True
    for group in (_CONFIG_KEY_PATTERNS, _TARGET_ALLOCATION_PATTERNS,
                  _MILESTONE_FINDING_PATTERNS, _CHART_DOMAIN_PATTERNS):
        for pat in group:
            if pat.search(text):
                return True
    return False


_ITEM_REDACTION_PLACEHOLDER = "[REDACTED -- item excluded by valuation_archetype_sanitizer: forbidden-content pattern]"


def redact_item(text: str) -> str:
    """Return the item text unchanged if clean, or a placeholder if it trips
    the layer-2 scan. Whole-item exclusion (not partial masking) -- matching
    this repository's established practice that a partially-redacted
    evidence sentence is more misleading than a disclosed exclusion."""
    return _ITEM_REDACTION_PLACEHOLDER if item_text_is_forbidden(text) else text


# ---------------------------------------------------------------------------
# SS D -- allow-list extraction of permitted evidence only
# ---------------------------------------------------------------------------

_MD_SECTION_HEADER = re.compile(r"^##\s+(.*)$", re.MULTILINE)


def extract_business_summary(md_text: str) -> str:
    """Extract exactly the '## Business summary' section body (permitted
    business-model narrative, VALUATION-0003 SS D) from a Company Intelligence
    markdown file. Returns '' if no such section exists. No other section
    title is ever extracted -- this is allow-list, not deny-list, so a
    document with additional undisclosed section titles cannot leak."""
    headers = list(_MD_SECTION_HEADER.finditer(md_text))
    for i, m in enumerate(headers):
        title = m.group(1).strip().lower()
        if title == "business summary":
            start = m.end()
            end = headers[i + 1].start() if i + 1 < len(headers) else len(md_text)
            return md_text[start:end].strip()
    return ""


@dataclass
class SanitizedPacket:
    ticker: str
    sector: str
    industry: str
    business_summary: str
    competitive_advantages: list = field(default_factory=list)
    risks: list = field(default_factory=list)
    catalysts: list = field(default_factory=list)
    role_basis: str = ""
    redacted_item_count: int = 0
    sanitizer_version: str = SANITIZER_VERSION


def build_sanitized_packet(
    ticker: str,
    company_yaml: dict,
    company_md: str,
    classification_yaml: dict | None = None,
) -> SanitizedPacket:
    """Build the complete sanitized, blind-drafting evidence packet for one
    ticker. `company_yaml`/`company_md` are the raw parsed Company
    Intelligence record; `classification_yaml` is the sealed Milestone 6
    intelligence/classification/<TICKER>.yaml record (optional, read only for
    its economic_role.role_basis context field per VALUATION-0003 SS D)."""
    stripped = strip_yaml_data(company_yaml)

    redacted_count = 0

    def _redact_scalar(text: str) -> str:
        nonlocal redacted_count
        out = redact_item(text)
        if out != text:
            redacted_count += 1
        return out

    sector = _redact_scalar(str(stripped.get("sector", "")))
    industry = _redact_scalar(str(stripped.get("industry", "")))
    business_summary = _redact_scalar(extract_business_summary(company_md))

    comp_adv = [_redact_scalar(str(x)) for x in stripped.get("competitive_advantages", []) or []]
    risks = [_redact_scalar(str(r.get("risk", ""))) for r in stripped.get("risks", []) or []]
    catalysts = [_redact_scalar(str(c.get("catalyst", ""))) for c in stripped.get("catalysts", []) or []]

    role_basis = ""
    if classification_yaml:
        role_basis = _redact_scalar(
            str((classification_yaml.get("economic_role") or {}).get("role_basis", ""))
        )

    return SanitizedPacket(
        ticker=ticker,
        sector=sector,
        industry=industry,
        business_summary=business_summary,
        competitive_advantages=comp_adv,
        risks=risks,
        catalysts=catalysts,
        role_basis=role_basis,
        redacted_item_count=redacted_count,
    )


def packet_to_drafting_text(pkt: SanitizedPacket) -> str:
    """Render a SanitizedPacket as the plain-text artifact handed to a blind
    drafting session -- the *only* file that session is instructed to read
    (VALUATION-0003 SS F.4)."""
    lines = [
        f"# Sanitized evidence packet -- {pkt.ticker}",
        "# Generated by valuation_archetype_sanitizer.py; VALUATION-0003-governed.",
        "# This is the ONLY evidence you may use. Do not consult any other file,",
        "# any prior knowledge of this company's allocation weight, actionable",
        "# status, or committee-assigned rating, or any chart/technical evidence.",
        "",
        f"## Sector\n{pkt.sector}",
        f"\n## Industry\n{pkt.industry}",
        f"\n## Business summary\n{pkt.business_summary or '(none disclosed)'}",
    ]
    if pkt.competitive_advantages:
        lines.append("\n## Competitive advantages")
        lines.extend(f"- {x}" for x in pkt.competitive_advantages)
    if pkt.risks:
        lines.append("\n## Disclosed risks")
        lines.extend(f"- {x}" for x in pkt.risks)
    if pkt.catalysts:
        lines.append("\n## Disclosed catalysts")
        lines.extend(f"- {x}" for x in pkt.catalysts)
    if pkt.role_basis:
        lines.append(
            "\n## Portfolio-relationship economic-role context (Milestone 6, "
            "context only -- NOT a valuation-archetype substitute)\n" + pkt.role_basis
        )
    return "\n".join(lines) + "\n"


def canonical_packet_text(pkt: SanitizedPacket) -> str:
    """Deterministic canonical JSON encoding for hashing/reproducibility
    checks -- independent of packet_to_drafting_text's own formatting."""
    payload = {
        "ticker": pkt.ticker,
        "sector": pkt.sector,
        "industry": pkt.industry,
        "business_summary": pkt.business_summary,
        "competitive_advantages": pkt.competitive_advantages,
        "risks": pkt.risks,
        "catalysts": pkt.catalysts,
        "role_basis": pkt.role_basis,
        "sanitizer_version": pkt.sanitizer_version,
    }
    return json.dumps(payload, sort_keys=True, separators=(",", ":"))


def packet_hash(pkt: SanitizedPacket) -> str:
    return hashlib.sha256(canonical_packet_text(pkt).encode("utf-8")).hexdigest()


# ---------------------------------------------------------------------------
# SS F.3 -- mandatory, mechanistically independent second-stage re-scan.
#
# This function is NEVER called by item_text_is_forbidden/redact_item above
# and never calls them either -- it is built from its own pattern set and its
# own control flow, so a regression in the layer-2 strip logic has an
# independent backstop, per VALUATION-0003 SS F.3 and the TIER-0004 lesson it
# cites (reusing one function for both strip and verify is a false
# independence claim).
# ---------------------------------------------------------------------------

_INDEPENDENT_VERIFY_PATTERNS = [
    re.compile(p, re.IGNORECASE)
    for p in [
        r"\bconviction\b",
        r"portfolio_role_ref",
        r"target_pct",
        r"targets\.yaml",
        r"holdings\.yaml",
        r"gates\.yaml",
        r"next_gate",
        r"allow_add",
        r"%\s*of\s+(the\s+)?book",
        r"%\s*of\s+portfolio",
        r"target\s+weight",
        r"destination\s+weight",
        r"primary_disposition",
        r"case_for_review",
        r"maintain_current_weight",
        r"divergence_requires_review",
        r"baseline_assumption_stale",
        r"support\s+level",
        r"resistance\s+level",
        r"breakout",
        r"trend\s*line",
        r"moving\s+average",
        r"\brsi\b",
        r"\bmacd\b",
        r"candlestick",
        r"chart\s+pattern",
        r"technical\s+analysis",
        r"oversold",
        r"overbought",
        r"fibonacci",
        r"volume\s+profile",
        r"price\s+target",
    ]
]


def independent_policy_scan(text: str) -> list[str]:
    """Independent (materially different mechanism from item_text_is_forbidden)
    scan for prohibited content. Returns the list of pattern descriptions that
    matched -- empty if clean. Also independently re-implements the
    bare-gate-word check using its own whitelist pass, rather than importing
    contains_gate_policy_leak, to keep the two mechanisms genuinely separate."""
    findings = []
    for pat in _INDEPENDENT_VERIFY_PATTERNS:
        if pat.search(text):
            findings.append(pat.pattern)

    scrubbed = text
    for legit in _GATE_LEGITIMATE_USE_PATTERNS:
        scrubbed = legit.sub("", scrubbed)
    if re.search(r"\bgates?\b", scrubbed, re.IGNORECASE):
        findings.append("bare-gate-word")

    return findings


def verify_packet(pkt: SanitizedPacket) -> list[str]:
    """Run the independent second-stage scan over an assembled packet's full
    rendered text."""
    return independent_policy_scan(packet_to_drafting_text(pkt))


def verify_sealed_record_text(*free_text_fields: str) -> list[str]:
    """Run the independent second-stage scan over a sealed record's own
    free-text fields (rationale, disclosed_evidence_conflicts,
    evidence_gap_statement) after drafting -- the post-sealing half of the
    proof VALUATION-0003 SS F.4 requires."""
    findings: list[str] = []
    for text in free_text_fields:
        if text:
            findings.extend(independent_policy_scan(text))
    return findings


# ---------------------------------------------------------------------------
# SS D -- mechanical, gate-derived portfolio_context fact. Computed directly
# from gates.yaml, NEVER passed into a drafting packet, NEVER an input to
# archetype selection -- attached only to a sealed record's own
# portfolio_context metadata after the archetype judgment is already sealed.
# ---------------------------------------------------------------------------


def gate_fact_for_ticker(ticker: str, gates_data: dict) -> dict | None:
    """Return {'gate_exists': True, 'next_gate_references_valuation': bool}
    for a gated ticker, or None if the ticker carries no gate. Mechanical
    substring check on the word 'valuation' in the gate's own next_gate text
    -- the literal text itself is never returned or retained anywhere."""
    for row in (gates_data or {}).get("gates", []) or []:
        if row.get("ticker") == ticker:
            next_gate_text = str(row.get("next_gate", ""))
            return {
                "gate_exists": True,
                "next_gate_references_valuation": "valuation" in next_gate_text.lower(),
            }
    return None
