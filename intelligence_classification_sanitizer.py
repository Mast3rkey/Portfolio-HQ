"""
intelligence_classification_sanitizer.py -- deterministic redaction of
Company Intelligence records into blind-drafting evidence packages for
WS-0005 Milestone 6 (blind classification), implementing the mechanics
specified (not implemented) by
`governance/decisions/TIER-0004-ws0005-milestone6-population-and-blindness-preflight.md`
Sec7, and authorized for this one implementation PR by
`governance/decisions/TIER-0005-ws0005-milestone6-fresh-authorization.md`.

Purpose: given a ticker's `intelligence/companies/<TICKER>.yaml` and paired
`.md` thesis narrative, produce a sanitized evidence package that a blind
judgment-drafting session (economic_role / capital_priority only) may see,
with every TIER-0004 Sec6.2 answer-key field mechanically absent -- never
merely instructed against.

Applied to the `.yaml` file (TIER-0004 Sec7.2 steps 1-3):
  1. Strip wholesale: `portfolio_role_ref` and the entire `conviction` block.
  2. Strip wholesale: `review.log`'s free-text `note` entries, retaining only
     `review.cadence_days` / `review.last_reviewed` / `review.next_due`.
  3. Retain unchanged: `sector`, `industry`, `themes`, `competitive_advantages`,
     `risks[]` (all sub-fields), `sources[]`.

Applied to the `.md` file (TIER-0004 Sec7.2 steps 4-5, corrected scope -- the
`.md` file is not exempt from redaction and is not assumed safe by
construction):
  4. Strip any paragraph containing a marker from `_MD_STRIP_MARKERS`.
  5. Mandatory post-redaction re-scan against the same marker list --
     any surviving match is a hard failure for that ticker's `.md`, not a
     tolerated miss.

Applied to both files: a defensive chart-domain scan (`_CHART_MARKERS`),
specified because live inspection found zero chart references in any of the
27 records today, but a future record change must not silently reintroduce
one.

Fail-closed complete-package scan: after building a ticker's sanitized
package (redacted `.yaml` content plus redacted `.md` content), the *entire*
assembled package is re-scanned for the full forbidden-field/marker set
before it may be released to a shard. Any surviving match blocks release.

This module is a sanitizer, not a data producer or a validator of sealed
classification records (see `classification_validator.py` for that). It
never writes into `intelligence/companies/`, never mutates a Company
Intelligence record, and has zero import relationship with `allocate.py` or
`margin_state.py` in either direction. Its own output packages are drafting
aids -- ephemeral by design (TIER-0004 Sec7.2 step 7: "written to a location
outside intelligence/companies/... never committed as a tracked
evidence-of-record file") -- this module itself is the retained, reusable,
auditable capability; its *output* is not committed to this repository.
"""

from __future__ import annotations

import copy
import hashlib
import re
from dataclasses import dataclass, field
from pathlib import Path

import yaml

# ── Sec7.2 step 1-2: YAML fields stripped wholesale ─────────────────────────

_YAML_STRIP_TOP_LEVEL_KEYS = ("portfolio_role_ref", "conviction")
_REVIEW_RETAIN_KEYS = ("cadence_days", "last_reviewed", "next_due")

# ── Section-level strip: some markers never appear in the section's own
# prose (e.g. a "## Conviction" section whose body reads only "**Rating:
# High**", with no literal word "conviction" anywhere in that paragraph) --
# discovered live against the real 27-ticker corpus, matching TIER-0004's
# own Sec7.1 precedent ("a plausible-sounding claim can be wrong when
# checked against the actual corpus"). These headers are dropped wholesale,
# header through end-of-section (next "## " line or EOF), before the
# paragraph-level pass below ever runs.
_MD_FORBIDDEN_SECTION_HEADER_PATTERNS = [
    re.compile(p, re.IGNORECASE) for p in (
        r"\bconviction\b",
        r"\bgoverned policy\b",
        r"\bcurrent governed tier\b",
        r"\bcapital-priority discipline\b",
        r"\bcapital priority and next-dollar\b",
        r"\bnext-best use of capital\b",
        r"\bportfolio role reference\b",
        r"\brelationship to the gate\b",
        r"\bcommittee review\b",
        r"\bbatch membership\b",
        r"\bdiversification versus existing roster\b",
        r"\boverlap and diversification versus\b",
    )
]
_MD_HEADER_LINE = re.compile(r"^##\s+.*$", re.MULTILINE)


def _strip_forbidden_sections(text: str) -> tuple[str, int]:
    """Drops every section (header line through the line before the next
    '## ' header, or EOF) whose header matches a forbidden pattern. Returns
    (text_with_sections_removed, sections_removed_count)."""
    headers = list(_MD_HEADER_LINE.finditer(text))
    if not headers:
        return text, 0

    removed = 0
    keep_spans: list[tuple[int, int]] = []
    cursor = 0
    for i, h in enumerate(headers):
        section_end = headers[i + 1].start() if i + 1 < len(headers) else len(text)
        header_text = h.group(0)
        if any(p.search(header_text) for p in _MD_FORBIDDEN_SECTION_HEADER_PATTERNS):
            keep_spans.append((cursor, h.start()))
            cursor = section_end
            removed += 1
    keep_spans.append((cursor, len(text)))

    kept = "".join(text[a:b] for a, b in keep_spans)
    return kept, removed


# ── Sec7.2 step 4 / mandatory step-5 re-scan: paragraph-level markers ───────
# Deliberately broad (over-redaction on the .md side is safe -- the fail-
# closed re-scan below is the actual safety net, not this list's precision).
_MD_STRIP_PATTERNS = [
    re.compile(p, re.IGNORECASE) for p in (
        r"portfolio_role_ref",
        r"\bT1\b",
        r"\bT2\b",
        r"\bband tier\b",
        r"\bspec tier\b",
        r"\bETF tier\b",
        r"\bgated\b",
        r"\bconviction\.rating\b",
        r"\bconviction rating\b",
        r"\bconviction is (?:high|medium|low|very high)\b",
        r"\bconviction (?:stays|remains|preserved)\b",
        r"\bRating:\s*(?:Low|Medium|High|Very High)\b",
        r"\bkeep current policy\b",
        r"\bcommittee review\b",
        r"\bpromoted to\b",
        r"\bpromoted from\b",
        r"\bretained at\b",
        r"\bapproved by the human principal\b",
        r"\btarget_pct\b",
        r"\btargets\.yaml\b",
        r"\bholdings\.yaml\b",
        r"\bgates\.yaml\b",
        r"\bcaps\.clusters\b",
        r"\bissuer_lookthrough\b",
        r"\ballocate\.py\b",
    )
]

# ── defensive chart-domain scan (both files) ────────────────────────────────
_CHART_PATTERNS = [
    re.compile(p, re.IGNORECASE) for p in (
        r"governance/evidence/CHART-000[12]",
        r"\bCHART-000[12]\b",
        r"\bchart[- ]?evidence\b",
        r"\bsupport[/ -]resistance\b",
        r"\btechnical indicator",
        r"\bprice[- ]action\b",
        r"\.png\b",
        r"\btradingview\b",
    )
]

# ── fail-closed complete-package scan (superset: MD markers + chart markers
#    + a direct structural check that no forbidden YAML key survived) ──────
_PACKAGE_FORBIDDEN_PATTERNS = _MD_STRIP_PATTERNS + _CHART_PATTERNS
_PACKAGE_FORBIDDEN_YAML_KEYS = frozenset({"portfolio_role_ref", "conviction", "target_pct"})


@dataclass
class SanitizedPackage:
    ticker: str
    yaml_data: dict
    markdown_text: str
    removed_yaml_fields: list[str] = field(default_factory=list)
    removed_md_paragraph_count: int = 0
    md_excluded: bool = False
    md_exclusion_reason: str | None = None
    source_yaml_path: str = ""
    source_md_path: str = ""


@dataclass
class SanitizationRecord:
    """Auditable record of one ticker's sanitization pass -- the smallest
    auditable record TIER-0004/TIER-0005 call for. Not itself a retained
    repository artifact; folded into the implementation PR's own body/
    checkpoint disclosure per TIER-0004 Sec7.2 step 7's ephemeral-output rule."""
    ticker: str
    source_yaml_path: str
    source_md_path: str
    source_commit: str
    sanitizer_version: str
    removed_yaml_fields: list[str]
    removed_md_paragraph_count: int
    md_excluded: bool
    md_exclusion_reason: str | None
    complete_package_scan_passed: bool
    complete_package_scan_findings: list[str]
    sanitized_package_sha256: str
    shard_destination: str = ""


SANITIZER_VERSION = "1.0"


_ITEM_REDACTION_PLACEHOLDER = (
    "[item excluded from this drafting package -- contained a forbidden "
    "marker that could not be safely stripped in place]"
)


def _redact_retained_text_fields(out: dict, removed: list[str]) -> None:
    """Live inspection (this implementation) found that a marker can leak
    into a *retained* field's own free text -- e.g. a risks[] entry
    discussing "its conviction rating's own exclusions", or a sources[]
    citation note that happens to name a marker-matched outlet. Top-level
    key stripping (portfolio_role_ref/conviction/review.log) does not catch
    this. Applies the same strip discipline at item granularity: any
    risks[].risk, competitive_advantages[] entry, or sources[].note whose
    text matches a marker is replaced with a placeholder -- the rest of the
    entry's structural fields (severity, identified, status, url, date) are
    retained since none of those are forbidden. Scanned against both the
    answer-key marker list and the defensive chart-domain marker list --
    a source citation naming a chart/quote aggregator by name (e.g.
    "tradingview.com" cited only as a WebSearch-snippet outlet) is excluded
    at the item level just as a true answer-key leak would be, matching
    this module's fail-closed-over-permissive discipline."""
    item_patterns = _MD_STRIP_PATTERNS + _CHART_PATTERNS

    risks = out.get("risks")
    if isinstance(risks, list):
        for i, r in enumerate(risks):
            if isinstance(r, dict) and isinstance(r.get("risk"), str):
                if _paragraph_matches_any(r["risk"], item_patterns):
                    r["risk"] = _ITEM_REDACTION_PLACEHOLDER
                    removed.append(f"risks[{i}].risk")

    advantages = out.get("competitive_advantages")
    if isinstance(advantages, list):
        for i, a in enumerate(advantages):
            if isinstance(a, str) and _paragraph_matches_any(a, item_patterns):
                advantages[i] = _ITEM_REDACTION_PLACEHOLDER
                removed.append(f"competitive_advantages[{i}]")

    sources = out.get("sources")
    if isinstance(sources, list):
        for i, s in enumerate(sources):
            if isinstance(s, dict) and isinstance(s.get("note"), str):
                if _paragraph_matches_any(s["note"], item_patterns):
                    s["note"] = _ITEM_REDACTION_PLACEHOLDER
                    removed.append(f"sources[{i}].note")

    # themes[] is a list of bare theme_id strings (PI-0006) -- never prose,
    # nothing to scan.


# ── YAML sanitization (Sec7.2 steps 1-3, extended per the above) ───────────

def sanitize_yaml_data(data: dict) -> tuple[dict, list[str]]:
    """Returns (sanitized_copy, removed_field_labels). Never mutates the
    input dict."""
    if not isinstance(data, dict):
        raise TypeError("company YAML root must be a mapping")

    removed: list[str] = []
    out = copy.deepcopy(data)

    for key in _YAML_STRIP_TOP_LEVEL_KEYS:
        if key in out:
            del out[key]
            removed.append(key)

    review = out.get("review")
    if isinstance(review, dict) and "log" in review:
        new_review = {k: v for k, v in review.items() if k in _REVIEW_RETAIN_KEYS}
        out["review"] = new_review
        removed.append("review.log")

    _redact_retained_text_fields(out, removed)

    return out, removed


# ── Markdown sanitization (Sec7.2 steps 4-5) ────────────────────────────────

def _split_paragraphs(text: str) -> list[str]:
    # Blank-line-delimited blocks; preserves original block text verbatim
    # (including internal newlines) so rejoining reconstructs faithfully.
    return re.split(r"\n\s*\n", text)


def _paragraph_matches_any(paragraph: str, patterns: list[re.Pattern]) -> bool:
    return any(p.search(paragraph) for p in patterns)


def redact_markdown(text: str) -> tuple[str, int]:
    """Sec7.2 step 4, extended: first drop whole forbidden sections (a
    marker word need not appear in the section's own body -- e.g. a
    "## Conviction" section reading only "**Rating: High**"), then strip
    any remaining paragraph matching a marker. Returns (redacted_text,
    removed_count) where removed_count is sections-plus-paragraphs."""
    text, sections_removed = _strip_forbidden_sections(text)

    paragraphs = _split_paragraphs(text)
    kept = []
    removed_count = sections_removed
    for para in paragraphs:
        if _paragraph_matches_any(para, _MD_STRIP_PATTERNS):
            removed_count += 1
            continue
        kept.append(para)
    return "\n\n".join(kept), removed_count


def verify_markdown_redaction(redacted_text: str) -> list[str]:
    """Sec7.2 step 5: mandatory re-scan. Returns a list of surviving marker
    descriptions (empty list == clean). Never mutates, never trusts the
    strip pass alone."""
    findings = []
    for p in _MD_STRIP_PATTERNS:
        m = p.search(redacted_text)
        if m:
            findings.append(f"surviving marker {p.pattern!r} at {m.start()}")
    return findings


def scan_chart_domain(text: str) -> list[str]:
    findings = []
    for p in _CHART_PATTERNS:
        m = p.search(text)
        if m:
            findings.append(f"chart-domain marker {p.pattern!r} at {m.start()}")
    return findings


# ── fail-closed complete-package scan ───────────────────────────────────────

def _canonical_package_text(pkg: SanitizedPackage) -> str:
    yaml_text = yaml.safe_dump(pkg.yaml_data, sort_keys=True, allow_unicode=True)
    return yaml_text + "\n\n" + pkg.markdown_text


def complete_package_scan(pkg: SanitizedPackage) -> list[str]:
    """TIER-0005 fail-closed requirement: scan the *complete assembled*
    package (yaml + markdown together) for every forbidden marker plus a
    structural check that no forbidden YAML key survived. Any finding means
    the package must not be released to a shard."""
    findings: list[str] = []

    for key in _PACKAGE_FORBIDDEN_YAML_KEYS:
        if key in pkg.yaml_data:
            findings.append(f"forbidden YAML key survived: {key!r}")

    text = _canonical_package_text(pkg)
    for p in _PACKAGE_FORBIDDEN_PATTERNS:
        m = p.search(text)
        if m:
            findings.append(f"forbidden marker survived in package text: {p.pattern!r} at {m.start()}")

    return findings


# ── top-level orchestration: one ticker end-to-end ──────────────────────────

def build_sanitized_package(
    ticker: str,
    yaml_data: dict,
    markdown_text: str,
    *,
    source_yaml_path: str = "",
    source_md_path: str = "",
) -> tuple[SanitizedPackage, list[str]]:
    """Builds one ticker's sanitized package and returns
    (package, complete_package_scan_findings). If findings is non-empty the
    package MUST NOT be released to a drafting shard (fail closed) -- the
    caller is responsible for enforcing that; this function only reports."""
    sanitized_yaml, removed_yaml_fields = sanitize_yaml_data(yaml_data)

    redacted_md, removed_count = redact_markdown(markdown_text)
    verify_findings = verify_markdown_redaction(redacted_md)

    md_excluded = False
    md_exclusion_reason = None
    if verify_findings:
        # Sec7.2 step 5: a surviving marker after the strip pass is a hard
        # failure for the .md specifically -- exclude the narrative rather
        # than ship contaminated evidence (never a silent pass-through).
        md_excluded = True
        md_exclusion_reason = (
            "post-redaction re-scan found surviving marker(s): "
            + "; ".join(verify_findings)
        )
        redacted_md = (
            "[.md thesis narrative excluded from this drafting package -- "
            "mandatory post-redaction re-scan found a surviving forbidden "
            "marker that could not be safely stripped. See evidence_quality "
            "for this ticker's coverage note.]"
        )

    chart_findings_yaml = scan_chart_domain(yaml.safe_dump(sanitized_yaml, sort_keys=True))
    chart_findings_md = scan_chart_domain(redacted_md)
    # Defensive: live inspection found zero chart references in any of the
    # 27 records (TIER-0004 Sec7.2 step 6) -- if one is ever found, exclude
    # exactly as a surviving marker would be excluded, never silently kept.
    if chart_findings_yaml or chart_findings_md:
        md_excluded = True
        md_exclusion_reason = (
            (md_exclusion_reason + "; " if md_exclusion_reason else "")
            + "chart-domain marker(s) found: "
            + "; ".join(chart_findings_yaml + chart_findings_md)
        )
        redacted_md = (
            "[.md thesis narrative excluded from this drafting package -- "
            "defensive chart-domain scan found a marker. See evidence_quality "
            "for this ticker's coverage note.]"
        )

    pkg = SanitizedPackage(
        ticker=ticker,
        yaml_data=sanitized_yaml,
        markdown_text=redacted_md,
        removed_yaml_fields=removed_yaml_fields,
        removed_md_paragraph_count=removed_count,
        md_excluded=md_excluded,
        md_exclusion_reason=md_exclusion_reason,
        source_yaml_path=source_yaml_path,
        source_md_path=source_md_path,
    )

    findings = complete_package_scan(pkg)
    return pkg, findings


def sanitize_company_files(
    repo_root: str | Path,
    ticker: str,
    *,
    source_commit: str = "",
) -> tuple[SanitizedPackage | None, SanitizationRecord]:
    """Reads intelligence/companies/<TICKER>.yaml + .md from repo_root,
    sanitizes, runs the fail-closed complete-package scan, and returns
    (package_or_None, record). package is None exactly when the scan found
    a forbidden survivor (fail closed -- never release a failing package)."""
    repo_root = Path(repo_root)
    yaml_path = repo_root / "intelligence" / "companies" / f"{ticker}.yaml"
    md_path = repo_root / "intelligence" / "companies" / f"{ticker}.md"

    yaml_data = yaml.safe_load(yaml_path.read_text())
    md_text = md_path.read_text()

    pkg, findings = build_sanitized_package(
        ticker, yaml_data, md_text,
        source_yaml_path=str(yaml_path.relative_to(repo_root)),
        source_md_path=str(md_path.relative_to(repo_root)),
    )

    package_hash = ""
    if not findings:
        canonical = _canonical_package_text(pkg).encode("utf-8")
        package_hash = hashlib.sha256(canonical).hexdigest()

    record = SanitizationRecord(
        ticker=ticker,
        source_yaml_path=pkg.source_yaml_path,
        source_md_path=pkg.source_md_path,
        source_commit=source_commit,
        sanitizer_version=SANITIZER_VERSION,
        removed_yaml_fields=pkg.removed_yaml_fields,
        removed_md_paragraph_count=pkg.removed_md_paragraph_count,
        md_excluded=pkg.md_excluded,
        md_exclusion_reason=pkg.md_exclusion_reason,
        complete_package_scan_passed=not findings,
        complete_package_scan_findings=findings,
        sanitized_package_sha256=package_hash,
    )

    if findings:
        return None, record
    return pkg, record


def package_to_drafting_text(pkg: SanitizedPackage) -> str:
    """Renders a sanitized package as the plain-text form handed to a
    blind-drafting shard -- deterministic, byte-identical across runs
    against the same source commit."""
    yaml_text = yaml.safe_dump(pkg.yaml_data, sort_keys=False, allow_unicode=True)
    return (
        f"=== {pkg.ticker} — sanitized Company Intelligence evidence ===\n\n"
        f"--- structured facts (sanitized .yaml) ---\n{yaml_text}\n"
        f"--- thesis narrative (sanitized .md) ---\n{pkg.markdown_text}\n"
    )


if __name__ == "__main__":
    import subprocess
    import sys

    _repo_root = Path(__file__).resolve().parent
    try:
        _source_commit = subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=_repo_root, text=True
        ).strip()
    except Exception:
        _source_commit = "unknown"

    _tickers = sys.argv[1:]
    if not _tickers:
        print("usage: python intelligence_classification_sanitizer.py TICKER [TICKER ...]")
        sys.exit(1)

    _any_failed = False
    for _t in _tickers:
        _pkg, _rec = sanitize_company_files(_repo_root, _t, source_commit=_source_commit)
        if _pkg is None:
            _any_failed = True
            print(f"{_t}: FAIL-CLOSED — {_rec.complete_package_scan_findings}")
        else:
            print(
                f"{_t}: OK — removed_yaml_fields={_rec.removed_yaml_fields} "
                f"removed_md_paragraphs={_rec.removed_md_paragraph_count} "
                f"md_excluded={_rec.md_excluded} hash={_rec.sanitized_package_sha256[:12]}"
            )
    sys.exit(1 if _any_failed else 0)
