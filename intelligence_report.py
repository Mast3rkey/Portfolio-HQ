"""
intelligence_report.py — source-read-only reporting/checking layer for the
Portfolio Intelligence Engine (Company + Theme records under intelligence/),
authorized in bounded scope by
governance/decisions/PI-0011-intelligence-operations-v1.md.

Authority boundary: this module is **source-read-only**. It never rewrites
any Company or Theme Intelligence record, never writes `holdings.yaml` or
`targets.yaml`, and has no import relationship with `allocate.py` or
`margin_state.py` in either direction. It is permitted to overwrite exactly
one generated artifact — `intelligence/reports/staleness_report.md` — and
nothing else. Every other output (role-drift, coverage) is stdout only.

Reuses `intelligence_validator.py`'s **public** API only. The two functions
actually called directly are `validate_company_file` and
`validate_themes_directory`; `validate_themes_directory` internally performs
the existing per-file `validate_theme_file` checks (schema, closed
vocabularies, reverse-membership-key rejection) for every theme file it
scans, so those checks run without this module calling them itself. No
underscore-prefixed private function of `intelligence_validator.py` is
imported or called anywhere in this file — theme-reference resolution and
reverse-membership rejection are `intelligence_validator.py`'s own,
unmodified, already-tested behavior; this module only surfaces those
results, it does not duplicate, reinterpret, or independently reimplement
them.

`run_portfolio_check.sh` never invokes this module as an operational
reporting command and never regenerates the tracked staleness report; its
`pytest -q` run does import and exercise this module's mechanics via
`test_intelligence_report.py`, but no test there may treat an advisory
finding (a staleness or role-drift outcome) as a failure — only schema
conformance and code invariants may gate the suite.

Staleness scope is literal to `docs/PORTFOLIO_INTELLIGENCE_SPEC.md` §18:
`intelligence/companies/*.yaml` only. Theme Intelligence's own
`review.next_due` is never read or evaluated here — extending staleness to
themes would extend §18's frozen scope and needs its own separate decision
(PI-0011's Decision, item 1).

Role-drift parses only `targets.yaml`'s `tiers.*.tickers` membership —
weights, caps, clusters, crypto, and every other key are ignored. A mismatch
is an advisory human-review finding only: it never rewrites the company
record or `targets.yaml`, and `targets.yaml` always remains authoritative
for current allocator policy (PI-0011's Decision, item 3). Ticker matching
is an internal repository-key comparison (company filename stem vs.
`targets.yaml` ticker string) — no external symbol-normalization map (e.g.
`earnings.py`'s `_YAHOO_SYMBOL`) is imported, copied, or extended; a
non-matching key is reported as `NOT_IN_TARGETS`, never guessed or remapped.
"""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path

import yaml

import intelligence_validator as _validator  # public API only — see module docstring

# ── the one approved, fixed write destination ─────────────────────────────

STALENESS_REPORT_RELATIVE_PATH = Path("intelligence/reports/staleness_report.md")

# ── role-drift status vocabulary ──────────────────────────────────────────

ROLE_MATCH = "MATCH"
ROLE_MISMATCH = "MISMATCH"
ROLE_NOT_IN_TARGETS = "NOT_IN_TARGETS"
ROLE_AMBIGUOUS = "AMBIGUOUS_TARGET_MEMBERSHIP"

ROLE_DRIFT_ADVISORY_NOTE = (
    "targets.yaml controls current allocator tier policy. The company "
    "record remains unchanged until a human separately reviews it. A "
    "mismatch reports that the two sources currently differ; it does not "
    "decide which historical or research statement should be edited."
)


# ── data model (frozen — every result is an immutable snapshot) ──────────

@dataclass(frozen=True)
class OverdueReview:
    ticker: str
    next_due: str
    days_overdue: int


@dataclass(frozen=True)
class LapsedCatalyst:
    ticker: str
    catalyst: str
    expected: str
    status: str
    days_overdue: int


@dataclass(frozen=True)
class UnableToEvaluate:
    ticker: str
    field_name: str
    raw_value: object
    reason: str


@dataclass(frozen=True)
class SchemaInvalidRecord:
    ticker: str
    errors: tuple[str, ...]


@dataclass(frozen=True)
class StalenessFindings:
    as_of_date: date
    companies_scanned: tuple[str, ...]
    overdue_reviews: tuple[OverdueReview, ...] = ()
    lapsed_catalysts: tuple[LapsedCatalyst, ...] = ()
    unable_to_evaluate: tuple[UnableToEvaluate, ...] = ()
    schema_invalid: tuple[SchemaInvalidRecord, ...] = ()


@dataclass(frozen=True)
class RoleDriftFinding:
    ticker: str
    portfolio_role_ref: str
    target_tiers: tuple[str, ...]
    status: str  # one of ROLE_MATCH / ROLE_MISMATCH / ROLE_NOT_IN_TARGETS / ROLE_AMBIGUOUS


@dataclass(frozen=True)
class RoleDriftReport:
    checked: int
    matched: int
    mismatched: int
    not_in_targets: int
    ambiguous: int
    findings: tuple[RoleDriftFinding, ...]  # non-MATCH entries only — see build_arg_parser help


@dataclass(frozen=True)
class CoverageRollup:
    company_yaml_count: int
    company_markdown_count: int
    theme_yaml_count: int
    theme_markdown_count: int
    company_theme_refs: tuple[tuple[str, str], ...]
    company_validation_errors: tuple[tuple[str, tuple[str, ...]], ...]
    theme_validation_errors: tuple[tuple[str, tuple[str, ...]], ...]


# ── shared helpers ─────────────────────────────────────────────────────────

def _ticker_from_path(path: Path) -> str:
    return path.stem


def _parse_iso_date(value: object) -> date | None:
    """Accepts a valid ISO-date string, or an actual `datetime.date` value
    (PyYAML decodes an unquoted `YYYY-MM-DD` scalar into one). Narrowest
    implementation: a `datetime.datetime` (a full timestamp, decoded from a
    YAML value that also carries a time component) is deliberately NOT
    silently truncated to its calendar date — that would substitute a
    different, untested schema meaning. It is treated as unparseable here
    (surfaced as "unable to evaluate" by callers), not accepted."""
    if isinstance(value, datetime):
        return None
    if isinstance(value, date):
        return value
    if not isinstance(value, str):
        return None
    try:
        return date.fromisoformat(value.strip())
    except ValueError:
        return None


# ── stage 1: read-only scan / collection ──────────────────────────────────

def collect_staleness_findings(
    companies_dir: Path | str, as_of_date: date
) -> StalenessFindings:
    """Read-only scan of `intelligence/companies/*.yaml`. Calls only
    `intelligence_validator.validate_company_file` (public API). Performs
    no writes anywhere. A missing or empty directory is a valid,
    zero-coverage state (spec §16), not an error."""
    companies_dir = Path(companies_dir)

    if not companies_dir.exists() or not companies_dir.is_dir():
        return StalenessFindings(as_of_date=as_of_date, companies_scanned=())

    scanned: list[str] = []
    overdue: list[OverdueReview] = []
    lapsed: list[LapsedCatalyst] = []
    unable: list[UnableToEvaluate] = []
    invalid: list[SchemaInvalidRecord] = []

    for path in sorted(companies_dir.glob("*.yaml")):
        ticker = _ticker_from_path(path)
        scanned.append(ticker)

        result = _validator.validate_company_file(path)
        if not result.valid:
            invalid.append(SchemaInvalidRecord(ticker=ticker, errors=tuple(result.errors)))
            continue

        data = yaml.safe_load(path.read_text()) or {}

        review = data.get("review")
        if review is None:
            # No `review:` key at all, or an explicit `review: null` — both
            # are schema-valid (review is an optional field per spec §9),
            # but leave nothing to evaluate. Never silently skipped, and
            # never classified as overdue (PI-0011 correction 2).
            unable.append(UnableToEvaluate(
                ticker=ticker,
                field_name="review.next_due",
                raw_value=None,
                reason="review block is missing (no review key, or review is null) — cannot evaluate staleness",
            ))
        else:
            # A non-None `review` is guaranteed by
            # intelligence_validator.py's own required-keys check to be a
            # dict already containing a `next_due` key if this record is
            # schema-valid (which it is, by this point in the loop).
            next_due_raw = review.get("next_due")
            next_due = _parse_iso_date(next_due_raw)
            if next_due is None:
                unable.append(UnableToEvaluate(
                    ticker=ticker,
                    field_name="review.next_due",
                    raw_value=next_due_raw,
                    reason="missing, unparseable, or non-date/non-string ISO date",
                ))
            elif next_due < as_of_date:
                overdue.append(OverdueReview(
                    ticker=ticker,
                    next_due=next_due.isoformat(),
                    days_overdue=(as_of_date - next_due).days,
                ))
            # next_due == as_of_date, or next_due > as_of_date: not overdue.

        for catalyst in data.get("catalysts") or []:
            if not isinstance(catalyst, dict):
                continue
            label = catalyst.get("catalyst", "<unlabeled catalyst>")
            expected_raw = catalyst.get("expected")
            expected = _parse_iso_date(expected_raw)
            status = catalyst.get("status")

            if expected is None:
                unable.append(UnableToEvaluate(
                    ticker=ticker,
                    field_name=f"catalysts[].expected ({label!r})",
                    raw_value=expected_raw,
                    reason="missing, unparseable, or non-date/non-string ISO date",
                ))
                continue
            if not isinstance(status, str):
                unable.append(UnableToEvaluate(
                    ticker=ticker,
                    field_name=f"catalysts[].status ({label!r})",
                    raw_value=status,
                    reason="non-string catalyst status",
                ))
                continue
            if expected < as_of_date and status == "pending":
                lapsed.append(LapsedCatalyst(
                    ticker=ticker,
                    catalyst=label,
                    expected=expected.isoformat(),
                    status=status,
                    days_overdue=(as_of_date - expected).days,
                ))
            # any other string status: received some update, not classified as lapsed.

    return StalenessFindings(
        as_of_date=as_of_date,
        companies_scanned=tuple(scanned),
        overdue_reviews=tuple(sorted(overdue, key=lambda o: o.ticker)),
        lapsed_catalysts=tuple(sorted(lapsed, key=lambda c: (c.ticker, c.catalyst))),
        unable_to_evaluate=tuple(sorted(unable, key=lambda u: (u.ticker, u.field_name))),
        schema_invalid=tuple(sorted(invalid, key=lambda i: i.ticker)),
    )


def _load_targets_tiers(targets_path: Path | str) -> dict[str, tuple[str, ...]]:
    """Parse only `tiers.*.tickers` from targets.yaml. Ignores weights,
    caps, clusters, crypto, and every other key (PI-0011 scope)."""
    data = yaml.safe_load(Path(targets_path).read_text()) or {}
    tiers = data.get("tiers") or {}
    result: dict[str, tuple[str, ...]] = {}
    for tier_name, tier_body in tiers.items():
        if isinstance(tier_body, dict):
            tickers = tier_body.get("tickers") or []
            if isinstance(tickers, list):
                result[tier_name] = tuple(t for t in tickers if isinstance(t, str))
    return result


def check_portfolio_role_drift(
    companies_dir: Path | str, targets_path: Path | str
) -> RoleDriftReport:
    """Read-only. Compares each schema-valid company record's
    `portfolio_role_ref` against its ticker's actual tier membership in
    targets.yaml (internal repository-key comparison — company filename
    stem vs. targets.yaml ticker string; no symbol normalization). Never
    writes back to either source. targets.yaml always wins."""
    companies_dir = Path(companies_dir)

    if not companies_dir.exists() or not companies_dir.is_dir():
        return RoleDriftReport(
            checked=0, matched=0, mismatched=0, not_in_targets=0, ambiguous=0, findings=()
        )

    tiers = _load_targets_tiers(targets_path)

    findings: list[RoleDriftFinding] = []
    matched = mismatched = not_in_targets = ambiguous = 0

    for path in sorted(companies_dir.glob("*.yaml")):
        ticker = _ticker_from_path(path)
        result = _validator.validate_company_file(path)
        if not result.valid:
            continue  # schema-invalid records are surfaced by the staleness report, not here

        data = yaml.safe_load(path.read_text()) or {}
        role_ref = data.get("portfolio_role_ref")
        if not isinstance(role_ref, str) or not role_ref.strip():
            continue  # nothing to compare

        member_tiers = tuple(t for t, tickers in tiers.items() if ticker in tickers)

        if len(member_tiers) == 0:
            status = ROLE_NOT_IN_TARGETS
            not_in_targets += 1
        elif len(member_tiers) > 1:
            status = ROLE_AMBIGUOUS
            ambiguous += 1
        elif member_tiers[0] == role_ref:
            status = ROLE_MATCH
            matched += 1
        else:
            status = ROLE_MISMATCH
            mismatched += 1

        if status != ROLE_MATCH:
            findings.append(RoleDriftFinding(
                ticker=ticker,
                portfolio_role_ref=role_ref,
                target_tiers=member_tiers,
                status=status,
            ))

    checked = matched + mismatched + not_in_targets + ambiguous
    return RoleDriftReport(
        checked=checked,
        matched=matched,
        mismatched=mismatched,
        not_in_targets=not_in_targets,
        ambiguous=ambiguous,
        findings=tuple(sorted(findings, key=lambda f: f.ticker)),
    )


def build_coverage_rollup(companies_dir: Path | str, themes_dir: Path | str) -> CoverageRollup:
    """Read-only. Every count and reference is derived from the filesystem
    on this call — nothing is cached, nothing is hard-coded, no index file
    is read or written. Theme-reference and reverse-membership checks reuse
    intelligence_validator.py's public API only."""
    companies_dir = Path(companies_dir)
    themes_dir = Path(themes_dir)

    company_yaml = sorted(companies_dir.glob("*.yaml")) if companies_dir.is_dir() else []
    company_md = sorted(companies_dir.glob("*.md")) if companies_dir.is_dir() else []
    theme_yaml = sorted(themes_dir.glob("*.yaml")) if themes_dir.is_dir() else []
    theme_md = sorted(themes_dir.glob("*.md")) if themes_dir.is_dir() else []

    refs: list[tuple[str, str]] = []
    company_errors: list[tuple[str, tuple[str, ...]]] = []
    for path in company_yaml:
        ticker = _ticker_from_path(path)
        result = _validator.validate_company_file(path)
        if not result.valid:
            company_errors.append((ticker, tuple(result.errors)))
            continue
        data = yaml.safe_load(path.read_text()) or {}
        for theme_id in data.get("themes") or []:
            if isinstance(theme_id, str):
                refs.append((ticker, theme_id))

    theme_errors: list[tuple[str, tuple[str, ...]]] = []
    theme_dir_result = _validator.validate_themes_directory(themes_dir)
    for r in theme_dir_result.results:
        if not r.valid:
            theme_id = Path(r.source).stem if r.source else "?"
            theme_errors.append((theme_id, tuple(r.errors)))

    return CoverageRollup(
        company_yaml_count=len(company_yaml),
        company_markdown_count=len(company_md),
        theme_yaml_count=len(theme_yaml),
        theme_markdown_count=len(theme_md),
        company_theme_refs=tuple(sorted(refs)),
        company_validation_errors=tuple(sorted(company_errors)),
        theme_validation_errors=tuple(sorted(theme_errors)),
    )


# ── stage 2: pure rendering — no filesystem I/O of any kind ──────────────

def _escape_markdown_cell(value: object) -> str:
    """Rendering-only escaping so a human-authored value (a catalyst label,
    a validator error message, a raw field value) can never break a
    Markdown table's row/column structure. Does not alter any source
    record and adds no schema restriction — output formatting only."""
    text = str(value)
    text = text.replace("\r\n", " ").replace("\r", " ").replace("\n", " ")
    text = text.replace("|", "\\|")
    return text


def render_staleness_report(findings: StalenessFindings) -> str:
    as_of = findings.as_of_date.isoformat()
    lines: list[str] = [
        "# Intelligence Staleness Report",
        f"_As of: {as_of}. Generated output; overwritten in place — not a "
        f"historical record._",
        "",
        "## Overdue company reviews",
    ]

    if findings.overdue_reviews:
        lines.append("| Ticker | next_due | Days overdue |")
        lines.append("|---|---|---|")
        for o in findings.overdue_reviews:
            lines.append(
                f"| {_escape_markdown_cell(o.ticker)} | {_escape_markdown_cell(o.next_due)} | "
                f"{_escape_markdown_cell(o.days_overdue)} |"
            )
    else:
        lines.append(f"No companies have an overdue review as of {as_of}.")
    lines.append("")

    lines.append("## Lapsed pending catalysts")
    if findings.lapsed_catalysts:
        lines.append("| Ticker | Catalyst | Expected | Status | Days overdue |")
        lines.append("|---|---|---|---|---|")
        for c in findings.lapsed_catalysts:
            lines.append(
                f"| {_escape_markdown_cell(c.ticker)} | {_escape_markdown_cell(c.catalyst)} | "
                f"{_escape_markdown_cell(c.expected)} | {_escape_markdown_cell(c.status)} | "
                f"{_escape_markdown_cell(c.days_overdue)} |"
            )
    else:
        lines.append(f"No lapsed catalysts as of {as_of}.")
    lines.append("")

    lines.append("## Unable to evaluate")
    if findings.unable_to_evaluate:
        lines.append("| Ticker | Field | Raw value | Reason |")
        lines.append("|---|---|---|---|")
        for u in findings.unable_to_evaluate:
            lines.append(
                f"| {_escape_markdown_cell(u.ticker)} | {_escape_markdown_cell(u.field_name)} | "
                f"{_escape_markdown_cell(repr(u.raw_value))} | {_escape_markdown_cell(u.reason)} |"
            )
    else:
        lines.append(f"Nothing flagged as unable to evaluate as of {as_of}.")
    lines.append("")

    lines.append("## Schema-invalid company records")
    if findings.schema_invalid:
        lines.append("| Ticker | Validator error(s) |")
        lines.append("|---|---|")
        for i in findings.schema_invalid:
            errors_cell = "; ".join(_escape_markdown_cell(e) for e in i.errors)
            lines.append(f"| {_escape_markdown_cell(i.ticker)} | {errors_cell} |")
    else:
        lines.append(f"No schema-invalid company records as of {as_of}.")
    lines.append("")

    lines.append("## Coverage note")
    n = len(findings.companies_scanned)
    if n:
        roster = ", ".join(findings.companies_scanned)
        plural = "y" if n == 1 else "ies"
        lines.append(
            f"{n} compan{plural} scanned: {roster}. Absence of a file for "
            "any other portfolio holding is not a gap — coverage is opt-in "
            "(docs/PORTFOLIO_INTELLIGENCE_SPEC.md §16)."
        )
    else:
        lines.append(
            "0 companies scanned — intelligence/companies/ is missing or "
            "empty. This is a valid, opt-in zero-coverage state, not an "
            "error (docs/PORTFOLIO_INTELLIGENCE_SPEC.md §16)."
        )
    lines.append("")

    return "\n".join(lines)


def _format_role_drift(report: RoleDriftReport) -> str:
    lines = [
        f"Role-drift check: {report.checked} checked — "
        f"{report.matched} {ROLE_MATCH}, {report.mismatched} {ROLE_MISMATCH}, "
        f"{report.not_in_targets} {ROLE_NOT_IN_TARGETS}, "
        f"{report.ambiguous} {ROLE_AMBIGUOUS}.",
        "",
        ROLE_DRIFT_ADVISORY_NOTE,
    ]
    if report.findings:
        lines.append("")
        lines.append("Findings requiring attention:")
        for f in report.findings:
            tiers = ", ".join(f.target_tiers) if f.target_tiers else "(none)"
            lines.append(
                f"  {f.ticker}: {f.status} — portfolio_role_ref={f.portfolio_role_ref!r}, "
                f"targets.yaml tier(s)={tiers}"
            )
    else:
        lines.append("")
        lines.append("No findings requiring attention.")
    return "\n".join(lines)


def _format_coverage(rollup: CoverageRollup) -> str:
    lines = [
        f"Company YAML files:     {rollup.company_yaml_count}",
        f"Company Markdown files: {rollup.company_markdown_count}",
        f"Theme YAML files:       {rollup.theme_yaml_count}",
        f"Theme Markdown files:   {rollup.theme_markdown_count}",
        "",
        "Company -> Theme references (company authority only; a theme "
        "never lists its member companies):",
    ]
    if rollup.company_theme_refs:
        for ticker, theme_id in rollup.company_theme_refs:
            lines.append(f"  {ticker} -> {theme_id}")
    else:
        lines.append("  (none)")

    if rollup.company_validation_errors:
        lines.append("")
        lines.append("Company records with schema errors (excluded from the reference list above):")
        for ticker, errors in rollup.company_validation_errors:
            lines.append(f"  {ticker}: {'; '.join(errors)}")

    if rollup.theme_validation_errors:
        lines.append("")
        lines.append("Theme records with schema errors:")
        for theme_id, errors in rollup.theme_validation_errors:
            lines.append(f"  {theme_id}: {'; '.join(errors)}")

    return "\n".join(lines)


# ── stage 3: single fixed-path writer ─────────────────────────────────────

def write_staleness_report(report_text: str, repo_root: Path | str) -> Path:
    """The only function in this module that opens a file in write mode.
    Computes exactly `repo_root / STALENESS_REPORT_RELATIVE_PATH` — no
    other destination is accepted or exposed by any caller, including the
    CLI. Does not create directories at runtime; a missing approved report
    directory is a genuine I/O failure, raised clearly rather than silently
    worked around by writing elsewhere."""
    repo_root = Path(repo_root)
    output_path = repo_root / STALENESS_REPORT_RELATIVE_PATH
    if not output_path.parent.is_dir():
        raise FileNotFoundError(
            f"approved report directory does not exist: {output_path.parent} "
            "(this module does not create directories at runtime — see PI-0011)"
        )
    output_path.write_text(report_text)
    return output_path


# ── CLI ─────────────────────────────────────────────────────────────────

DEFAULT_COMPANIES_DIR = "intelligence/companies"
DEFAULT_THEMES_DIR = "intelligence/themes"
DEFAULT_TARGETS_PATH = "targets.yaml"


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="intelligence_report.py",
        description=(
            "Source-read-only reporting/checking layer over intelligence/ "
            "(PI-0011). Writes exactly one generated artifact: "
            "intelligence/reports/staleness_report.md. Every other output "
            "is stdout only. Never invoked by allocate.py, margin_state.py, "
            "or run_portfolio_check.sh."
        ),
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--staleness", action="store_true",
        help="Regenerate intelligence/reports/staleness_report.md and echo it to stdout.",
    )
    group.add_argument(
        "--role-drift", action="store_true",
        help="Stdout-only: portfolio_role_ref vs. targets.yaml tier membership.",
    )
    group.add_argument(
        "--coverage", action="store_true",
        help="Stdout-only: filesystem-derived company/theme coverage rollup.",
    )
    group.add_argument(
        "--all", action="store_true",
        help="Run staleness, role-drift, and coverage together.",
    )
    parser.add_argument(
        "--as-of", type=str, default=None, metavar="YYYY-MM-DD",
        help="As-of date override for the staleness component only. "
             "Valid only together with --staleness or --all.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_arg_parser()
    args = parser.parse_args(argv)

    if args.as_of is not None and not (args.staleness or args.all):
        parser.error("--as-of is only valid together with --staleness or --all")

    as_of_date = date.today()
    if args.as_of is not None:
        try:
            as_of_date = date.fromisoformat(args.as_of)
        except ValueError:
            parser.error(f"invalid --as-of date {args.as_of!r} (expected YYYY-MM-DD)")

    repo_root = Path(__file__).resolve().parent
    companies_dir = repo_root / DEFAULT_COMPANIES_DIR
    themes_dir = repo_root / DEFAULT_THEMES_DIR
    targets_path = repo_root / DEFAULT_TARGETS_PATH

    try:
        if args.staleness or args.all:
            findings = collect_staleness_findings(companies_dir, as_of_date)
            report_text = render_staleness_report(findings)
            output_path = write_staleness_report(report_text, repo_root)
            print(report_text)
            print(f"(written to {output_path.relative_to(repo_root)})", file=sys.stderr)

        if args.role_drift or args.all:
            role_report = check_portfolio_role_drift(companies_dir, targets_path)
            print(_format_role_drift(role_report))

        if args.coverage or args.all:
            rollup = build_coverage_rollup(companies_dir, themes_dir)
            print(_format_coverage(rollup))

    except Exception as exc:  # genuine I/O or unexpected execution failure
        print(f"error: {exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
