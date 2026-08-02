"""DashboardModel — the repository-native, read-only view-model.

Loads the repository's own authoritative files and reuses production functions
(``allocate.build_roster``, ``allocate._margin_buffer_age_days``,
``intelligence_report.*``) to derive displayed state. It computes NO allocation
recommendation of its own — the allocator needs live market data and reconciled
holdings that this offline, read-only layer deliberately does not touch, so the
Allocation Check surfaces a labelled "unavailable" explanation instead of
inventing numbers or building a second allocator.

Every loader is defensive: a missing or malformed input is recorded as a
warning and the dashboard still renders. Nothing here writes any file.
"""

from __future__ import annotations

import csv
import io
from dataclasses import dataclass, field
from datetime import date, datetime, timezone
from pathlib import Path

import yaml

from . import decisions as decisions_mod
from .provenance import Provenance, collect_provenance

# ── authoritative inputs (repo-relative) ────────────────────────────────────
HOLDINGS_REL = "holdings.yaml"
TARGETS_REL = "targets.yaml"
# Live actionable-gate state (PHQ-2026-02) — distinct from GATED_DISPOSITION_REL
# below, which is frozen PHQ-2026-01 point-in-time evidence. gates.yaml is the
# CURRENT authority for "is this ticker gated right now" (e.g. a name whose
# gate was later retired, like SPCX per PHQ-2026-04, is absent here even
# though it still appears in the frozen evidence CSV).
GATES_REL = "gates.yaml"
DECISIONS_REL = "governance/decisions.yaml"
WORKSTREAMS_REL = "operations/WORKSTREAMS.yaml"
FRESHNESS_REGISTRY_REL = "intelligence/freshness_registry.yaml"
COMPANIES_REL = "intelligence/companies"
THEMES_REL = "intelligence/themes"
# PHQ-2026-01 gated-name disposition is *governance policy evidence*, point-in-time.
# It is displayed as approved gating policy only, NEVER merged into live holdings
# or fed into any allocation computation (PHQ-2026-01 design-note §9).
GATED_DISPOSITION_REL = (
    "governance/evidence/PHQ-2026-01/final_due_diligence/"
    "Portfolio_HQ_Gated_Name_Disposition_v1_32.csv"
)
# Structured source for the 8%/40% ceilings and the measured AI/platform figure
# (see `_lookthrough_summary` below) — point-in-time governance evidence, same
# disclosure treatment as GATED_DISPOSITION_REL.
DUE_DILIGENCE_JSON_REL = (
    "governance/evidence/PHQ-2026-01/final_due_diligence/"
    "Portfolio_HQ_Final_Due_Diligence_and_Approval_v1_32.json"
)
PHQ_2026_01_DECISION_REL = (
    "governance/decisions/PHQ-2026-01-canonical-architecture-and-transition-policy-approval.md"
)

INPUT_FILES = [
    HOLDINGS_REL,
    TARGETS_REL,
    GATES_REL,
    DECISIONS_REL,
    WORKSTREAMS_REL,
    FRESHNESS_REGISTRY_REL,
    GATED_DISPOSITION_REL,
    DUE_DILIGENCE_JSON_REL,
    PHQ_2026_01_DECISION_REL,
]

STALE_HOLDINGS_WARN_DAYS = 3  # margin/holdings sync older than this → prominent warning

SEVERITY_BLOCKER = "blocker"
SEVERITY_WARNING = "warning"
SEVERITY_INFO = "info"


# ── data records ─────────────────────────────────────────────────────────────

@dataclass(frozen=True)
class Notice:
    """A warning/blocker/info banner item. `severity` drives presentation."""

    severity: str
    title: str
    detail: str


@dataclass(frozen=True)
class HoldingRow:
    ticker: str
    kind: str  # "equity" | "crypto" | "manual"
    tier: str | None
    quantity: float | None
    manual_value: float | None  # only for the manual `holdings:` fallback layer


@dataclass(frozen=True)
class MarginInfo:
    debt: float | None
    buffer_pct: float | None
    synced_at: str | None
    age_days: int | None
    age_unverifiable: bool
    leverage_cap: float | None
    buffer_floor_pct: float | None
    stale: bool

    @property
    def below_buffer_floor(self) -> bool | None:
        if self.buffer_pct is None or self.buffer_floor_pct is None:
            return None
        return self.buffer_pct < self.buffer_floor_pct


@dataclass(frozen=True)
class DestinationTarget:
    """One row of targets.yaml's canonical `destination:` list (PHQ-2026-02)
    — the flat, per-name architecture that replaced the retired T1/T2/ETF/
    band/spec tier structure. No tier/grouping concept exists in this
    schema; each name carries only its own target weight and asset class."""

    ticker: str
    target_pct: float | None
    asset_class: str | None


@dataclass(frozen=True)
class LiveGate:
    """One row of the CURRENT gates.yaml (PHQ-2026-02) — a ticker's live
    actionable-gate state. Distinct from GatedName below, which is frozen
    PHQ-2026-01 point-in-time evidence and may list a name (e.g. SPCX) whose
    gate has since been retired."""

    ticker: str
    status: str | None
    authority: str | None
    allow_add: bool | None
    holds_existing_shares: bool | None
    next_gate: str | None


@dataclass(frozen=True)
class TickerCurrentState:
    """Current, file-derived state for one ticker — used to decide what (if
    anything) to say about it, instead of a hardcoded, always-shown claim."""

    ticker: str
    live_gate: LiveGate | None
    currently_held: bool
    has_destination_target: bool


@dataclass(frozen=True)
class ClusterCap:
    name: str
    pct: float | None
    tickers: tuple[str, ...]


@dataclass(frozen=True)
class GatedName:
    ticker: str
    target_weight: float | None
    status: str
    reason: str
    next_gate: str


@dataclass(frozen=True)
class DecisionRow:
    decision_id: str
    date: str | None
    status: str | None
    category: str | None
    file: str | None


@dataclass(frozen=True)
class WorkstreamRow:
    ws_id: str
    title: str | None
    status: str | None
    priority: str | None
    next_action: str | None


@dataclass(frozen=True)
class IntelligenceSummary:
    company_yaml_count: int
    company_markdown_count: int
    theme_yaml_count: int
    theme_markdown_count: int
    companies_scanned: int
    overdue_reviews: tuple[tuple[str, str], ...]  # (ticker, detail)
    schema_invalid: tuple[str, ...]
    role_drift_mismatches: tuple[tuple[str, str], ...]  # (ticker, detail)
    freshness_rows: int
    monitoring_enabled_rows: int
    available: bool
    note: str | None


@dataclass(frozen=True)
class DashboardModel:
    provenance: Provenance
    generated_at_iso: str
    holdings_effective_date: str | None
    holdings_effective_source: str  # human description of what that date means
    notices: tuple[Notice, ...]
    holdings: tuple[HoldingRow, ...]
    crypto_sleeve_pct: float | None
    margin: MarginInfo
    destination_targets: tuple[DestinationTarget, ...]
    clusters: tuple[ClusterCap, ...]
    gates: dict
    live_gates: tuple[LiveGate, ...]
    gated_names: tuple[GatedName, ...]
    gated_names_source: str
    spcx_state: TickerCurrentState
    single_issuer_ceiling_pct: float | None
    ai_platform_ceiling_pct: float | None
    ai_platform_measured_pct: float | None
    skhy_unresolved: bool
    allocation_available: bool
    allocation_unavailable_reasons: tuple[str, ...]
    decisions: tuple[DecisionRow, ...]
    controlling_decisions: tuple[str, ...]
    decision_catalog: decisions_mod.DecisionCatalog
    workstreams: tuple[WorkstreamRow, ...]
    intelligence: IntelligenceSummary
    input_files: tuple[str, ...]
    phq_2026_02_filed: bool

    @property
    def blockers(self) -> tuple[Notice, ...]:
        return tuple(n for n in self.notices if n.severity == SEVERITY_BLOCKER)

    @property
    def warnings(self) -> tuple[Notice, ...]:
        return tuple(n for n in self.notices if n.severity == SEVERITY_WARNING)

    @property
    def infos(self) -> tuple[Notice, ...]:
        return tuple(n for n in self.notices if n.severity == SEVERITY_INFO)


# ── helpers ──────────────────────────────────────────────────────────────────

def _safe_load_yaml(path: Path) -> tuple[object, str | None]:
    """Return (data, error). Never raises. Missing file → (None, msg)."""
    if not path.exists():
        return None, f"{path.name} not found"
    try:
        return yaml.safe_load(path.read_text()) or {}, None
    except (yaml.YAMLError, OSError) as exc:  # pragma: no cover - defensive
        return None, f"{path.name} failed to parse: {exc}"


def _as_float(value: object) -> float | None:
    try:
        return float(value)  # type: ignore[arg-type]
    except (TypeError, ValueError):
        return None


# ── section loaders ──────────────────────────────────────────────────────────

def _load_roster(targets: dict) -> dict[str, dict]:
    """Reuse allocate.build_roster; fall back to a local build if allocate can't
    be imported (keeps the dashboard renderable in a stripped environment).
    The fallback mirrors allocate.build_roster's canonical `destination:`
    schema (PHQ-2026-02) — the retired `tiers:` schema is not read here or
    anywhere else in this module."""
    try:
        import allocate  # local production module
        return allocate.build_roster(targets)
    except Exception:  # pragma: no cover - defensive fallback
        roster: dict[str, dict] = {}
        for row in targets.get("destination", []) or []:
            if not isinstance(row, dict):
                continue
            tk = row.get("ticker")
            if not isinstance(tk, str) or not tk.strip():
                continue
            roster[tk.strip().upper()] = {
                "target_pct": _as_float(row.get("target_pct")),
                "asset_class": row.get("asset_class"),
            }
        return roster


def _margin_age(synced_at) -> tuple[int | None, bool]:
    """Reuse allocate's single source of truth for margin sync age."""
    try:
        import allocate
        age = allocate._margin_buffer_age_days(synced_at)
        unverifiable = allocate._margin_buffer_age_unverifiable(synced_at)
        return age, unverifiable
    except Exception:  # pragma: no cover - defensive
        if not synced_at:
            return None, True
        try:
            age = (date.today() - date.fromisoformat(str(synced_at))).days
        except ValueError:
            return None, True
        return (age, False) if age >= 0 else (None, True)


def _build_holdings(holdings_data: dict, roster: dict[str, dict]) -> list[HoldingRow]:
    rows: list[HoldingRow] = []
    shares = holdings_data.get("shares") or {}
    crypto = holdings_data.get("crypto_shares") or {}
    manual = holdings_data.get("holdings") or {}
    for ticker, qty in sorted(shares.items()):
        tier = (roster.get(str(ticker).upper()) or {}).get("tier")
        rows.append(HoldingRow(str(ticker), "equity", tier, _as_float(qty), None))
    for coin, qty in sorted(crypto.items()):
        rows.append(HoldingRow(str(coin), "crypto", "crypto", _as_float(qty), None))
    for ticker, val in sorted(manual.items()):
        rows.append(HoldingRow(str(ticker), "manual", None, None, _as_float(val)))
    return rows


def _build_margin(holdings_data: dict, targets: dict) -> MarginInfo:
    m = holdings_data.get("margin") or {}
    synced_at = m.get("synced_at")
    age, unverifiable = _margin_age(synced_at)
    margin_cfg = targets.get("margin") or {}
    lev = _as_float(margin_cfg.get("leverage_cap"))
    floor = _as_float(margin_cfg.get("buffer_floor_pct"))
    stale = age is not None and age > STALE_HOLDINGS_WARN_DAYS
    return MarginInfo(
        debt=_as_float(m.get("debt")),
        buffer_pct=_as_float(m.get("buffer_pct")),
        synced_at=str(synced_at) if synced_at else None,
        age_days=age,
        age_unverifiable=unverifiable,
        leverage_cap=lev,
        buffer_floor_pct=floor,
        stale=stale,
    )


def _build_destination_targets(roster: dict[str, dict]) -> list[DestinationTarget]:
    """One row per canonical `destination:` ticker (PHQ-2026-02), built from
    the already-loaded, already-validated roster — no separate parse of
    targets.yaml and no invented grouping. Sorted by asset class, then by
    target weight descending, then ticker, for a stable and legible table."""
    rows = [
        DestinationTarget(
            ticker=tk,
            target_pct=_as_float(info.get("target_pct")),
            asset_class=(str(info["asset_class"]) if info.get("asset_class") else None),
        )
        for tk, info in roster.items()
    ]
    return sorted(
        rows,
        key=lambda r: (r.asset_class or "", -(r.target_pct or 0.0), r.ticker),
    )


def _crypto_sleeve_pct(roster: dict[str, dict]) -> float | None:
    """Sum of the crypto-asset-class destination rows (BTC/ETH/SOL each carry
    their own weight since PHQ-2026-02 retired the prior aggregate `crypto:`
    sleeve config) — a straight sum of already-authoritative source values,
    not a new calculation. None (not 0) when no crypto row exists at all."""
    crypto_pcts = [
        _as_float(info.get("target_pct"))
        for info in roster.values()
        if info.get("asset_class") == "crypto"
    ]
    if not crypto_pcts:
        return None
    return sum(p for p in crypto_pcts if p is not None)


def _load_live_gates(path: Path) -> tuple[dict[str, LiveGate], str | None]:
    """Parse the CURRENT gates.yaml (PHQ-2026-02) — the live authority for
    "is this ticker gated right now." Returns ({ticker: LiveGate}, error).
    Unlike allocate.py's fail-loud convention for the live allocator (a
    missing gates.yaml there would let a gated ticker silently become an
    ordinary buy candidate — unacceptable for a system that places orders),
    this read-only dashboard never raises: a missing/unreadable file is
    surfaced as a visible warning (same defensive convention as every other
    loader in this module) and every ticker is then treated as having no
    live gate, so the dashboard still renders."""
    data, err = _safe_load_yaml(path)
    if err:
        return {}, err
    entries = (data or {}).get("gates") or []
    out: dict[str, LiveGate] = {}
    for e in entries:
        if not isinstance(e, dict):
            continue
        raw_ticker = e.get("ticker")
        if not isinstance(raw_ticker, str) or not raw_ticker.strip():
            continue
        tk = raw_ticker.strip().upper()
        out[tk] = LiveGate(
            ticker=tk,
            status=e.get("status"),
            authority=e.get("authority"),
            allow_add=e.get("allow_add") if isinstance(e.get("allow_add"), bool) else None,
            holds_existing_shares=(
                e.get("holds_existing_shares")
                if isinstance(e.get("holds_existing_shares"), bool)
                else None
            ),
            next_gate=e.get("next_gate"),
        )
    return out, None


def _ticker_current_state(
    ticker: str,
    *,
    live_gates: dict[str, LiveGate],
    holdings: list[HoldingRow],
    destination_tickers: set[str],
) -> TickerCurrentState:
    """General, ticker-agnostic current-state derivation — reused for any
    ticker whose dashboard display must reflect live repository truth rather
    than a hardcoded assumption (PHQ-2026-04 correction: SPCX's gate was
    retired after a verified exit, so a name present in frozen PHQ-2026-01
    evidence is not necessarily gated today)."""
    tk = ticker.strip().upper()
    return TickerCurrentState(
        ticker=tk,
        live_gate=live_gates.get(tk),
        currently_held=any(h.ticker.upper() == tk for h in holdings),
        has_destination_target=tk in destination_tickers,
    )


def _build_clusters(targets: dict) -> list[ClusterCap]:
    caps = ((targets.get("caps") or {}).get("clusters")) or []
    out: list[ClusterCap] = []
    for c in caps:
        if not isinstance(c, dict):
            continue
        out.append(
            ClusterCap(
                name=str(c.get("name", "?")),
                pct=_as_float(c.get("pct")),
                tickers=tuple(str(t) for t in (c.get("tickers") or [])),
            )
        )
    return out


def _load_gated_names(path: Path) -> tuple[list[GatedName], str | None]:
    """Parse the PHQ-2026-01 gated-name disposition CSV as *policy reference*
    only. Returns (rows, error). This is never merged into holdings."""
    if not path.exists():
        return [], "gated-name disposition evidence not found"
    try:
        text = path.read_text()
    except OSError as exc:  # pragma: no cover - defensive
        return [], f"could not read gated disposition: {exc}"
    rows: list[GatedName] = []
    reader = csv.DictReader(io.StringIO(text))
    for r in reader:
        rows.append(
            GatedName(
                ticker=(r.get("ticker") or "").strip(),
                target_weight=_as_float(r.get("target_weight")),
                status=(r.get("status") or "").strip(),
                reason=(r.get("reason") or "").strip(),
                next_gate=(r.get("next_gate") or "").strip(),
            )
        )
    return rows, None


def _load_decisions(path: Path) -> tuple[list[DecisionRow], str | None]:
    data, err = _safe_load_yaml(path)
    if err:
        return [], err
    entries = (data or {}).get("decisions") or []
    rows = [
        DecisionRow(
            decision_id=str(e.get("decision_id", "?")),
            date=str(e.get("date")) if e.get("date") else None,
            status=e.get("status"),
            category=e.get("category"),
            file=e.get("file"),
        )
        for e in entries
        if isinstance(e, dict)
    ]
    return rows, None


def _load_workstreams(path: Path) -> tuple[list[WorkstreamRow], str | None]:
    data, err = _safe_load_yaml(path)
    if err:
        return [], err
    entries = (data or {}).get("workstreams") or []
    rows: list[WorkstreamRow] = []
    for e in entries:
        if not isinstance(e, dict):
            continue
        na = e.get("next_action")
        rows.append(
            WorkstreamRow(
                ws_id=str(e.get("id", "?")),
                title=(str(e.get("title")).strip() if e.get("title") else None),
                status=e.get("status"),
                priority=e.get("priority"),
                next_action=(str(na).strip() if na else None),
            )
        )
    return rows, None


def _load_intelligence(repo_root: Path) -> IntelligenceSummary:
    companies_dir = repo_root / COMPANIES_REL
    themes_dir = repo_root / THEMES_REL
    registry_path = repo_root / FRESHNESS_REGISTRY_REL

    freshness_rows = 0
    monitoring_enabled = 0
    reg, reg_err = _safe_load_yaml(registry_path)
    if not reg_err and isinstance(reg, dict):
        for row in reg.get("tickers") or []:
            if isinstance(row, dict):
                freshness_rows += 1
                if row.get("monitoring_enabled") is True:
                    monitoring_enabled += 1

    try:
        import intelligence_report as ir

        rollup = ir.build_coverage_rollup(companies_dir, themes_dir)
        findings = ir.collect_staleness_findings(companies_dir, date.today())
        drift = ir.check_portfolio_role_drift(companies_dir, repo_root / TARGETS_REL)

        overdue = tuple(
            (o.ticker, f"review due {o.next_due} ({o.days_overdue}d overdue)")
            for o in findings.overdue_reviews
        )
        invalid = tuple(sorted({r.ticker for r in findings.schema_invalid}))
        mismatches = tuple(
            (
                f.ticker,
                f"record role {f.portfolio_role_ref}, targets.yaml tier(s) "
                f"{', '.join(f.target_tiers) or '—'}",
            )
            for f in drift.findings
            if f.status == "MISMATCH"
        )
        return IntelligenceSummary(
            company_yaml_count=rollup.company_yaml_count,
            company_markdown_count=rollup.company_markdown_count,
            theme_yaml_count=rollup.theme_yaml_count,
            theme_markdown_count=rollup.theme_markdown_count,
            companies_scanned=len(findings.companies_scanned),
            overdue_reviews=overdue,
            schema_invalid=invalid,
            role_drift_mismatches=mismatches,
            freshness_rows=freshness_rows,
            monitoring_enabled_rows=monitoring_enabled,
            available=True,
            note=None,
        )
    except Exception as exc:  # pragma: no cover - defensive
        # Fall back to a raw filesystem count so the section still renders.
        yml = len(list(companies_dir.glob("*.yaml"))) if companies_dir.is_dir() else 0
        md = len(list(companies_dir.glob("*.md"))) if companies_dir.is_dir() else 0
        tyml = len(list(themes_dir.glob("*.yaml"))) if themes_dir.is_dir() else 0
        tmd = len(list(themes_dir.glob("*.md"))) if themes_dir.is_dir() else 0
        return IntelligenceSummary(
            company_yaml_count=yml,
            company_markdown_count=md,
            theme_yaml_count=tyml,
            theme_markdown_count=tmd,
            companies_scanned=0,
            overdue_reviews=(),
            schema_invalid=(),
            role_drift_mismatches=(),
            freshness_rows=freshness_rows,
            monitoring_enabled_rows=monitoring_enabled,
            available=False,
            note=f"Intelligence reporting API unavailable ({type(exc).__name__}); "
            "showing raw file counts only.",
        )


def _pct_from_fraction(value: object) -> float | None:
    """PHQ-2026-01 look-through figures are stored as fractions (0.08, 0.4003).
    Convert to percent; pass through values already expressed as percent."""
    v = _as_float(value)
    if v is None:
        return None
    return v * 100 if v <= 1.0 else v


def _lookthrough_summary(
    repo_root: Path,
) -> tuple[float | None, float | None, float | None, str | None]:
    """Read the PHQ-2026-01 concentration ceilings and the measured AI/platform
    figure from the accepted decision's own structured evidence JSON
    (`lookthrough_summary`), the single authoritative structured source. Returns
    (single_issuer_ceiling_pct, ai_ceiling_pct, ai_measured_pct, load_error).
    Point-in-time, never live-computed. Falls back to the decision's stated
    policy constants (8% / 40%) if the structured summary is unreadable or
    missing its expected key — `load_error` is non-None in that case so the
    caller can surface a visible notice instead of silently substituting the
    fallback; never fabricates the measured figure (None if absent)."""
    single_issuer: float | None = 8.0   # PHQ-2026-01 point 8 (policy constant fallback)
    ai_ceiling: float | None = 40.0     # PHQ-2026-01 point 9 (policy constant fallback)
    ai_measured: float | None = None
    lookthrough_json = repo_root / DUE_DILIGENCE_JSON_REL
    data, err = _safe_load_yaml(lookthrough_json)  # JSON is valid YAML
    if not err and isinstance(data, dict):
        summary = data.get("lookthrough_summary")
        if isinstance(summary, dict):
            si = _pct_from_fraction(summary.get("approved_single_issuer_ceiling"))
            if si is not None:
                single_issuer = si
            ac = _pct_from_fraction(summary.get("approved_ai_platform_common_driver_ceiling"))
            if ac is not None:
                ai_ceiling = ac
            ai_measured = _pct_from_fraction(
                summary.get("effective_ai_platform_common_driver_estimate")
            )
        else:
            err = f"{DUE_DILIGENCE_JSON_REL}: missing 'lookthrough_summary' key"
    elif not err:
        err = f"{DUE_DILIGENCE_JSON_REL}: not a mapping"
    return single_issuer, ai_ceiling, ai_measured, err


# ── notice computation ───────────────────────────────────────────────────────

def _compute_notices(
    *,
    provenance: Provenance,
    margin: MarginInfo,
    load_errors: list[str],
    phq_2026_02_filed: bool,
    live_gates: dict[str, LiveGate],
    ai_measured: float | None,
    ai_ceiling: float | None,
    lookthrough_err: str | None,
    intelligence: IntelligenceSummary,
) -> list[Notice]:
    notices: list[Notice] = []

    if provenance.dirty:
        notices.append(
            Notice(
                SEVERITY_WARNING,
                "Generated from a dirty worktree",
                "The repository had uncommitted changes when this page was "
                "generated, so it is NOT an authoritative snapshot of any "
                f"committed state. {len(provenance.dirty_paths)} path(s) were "
                "modified/untracked. Commit or stash, then regenerate.",
            )
        )
    if not provenance.git_available:
        notices.append(
            Notice(
                SEVERITY_WARNING,
                "Git metadata unavailable",
                "Could not read git provenance (commit / branch / worktree "
                "status). The source commit cannot be verified for this page.",
            )
        )

    # Stale holdings / margin sync.
    if margin.age_unverifiable:
        notices.append(
            Notice(
                SEVERITY_WARNING,
                "Holdings sync date unverifiable",
                "holdings.yaml has no valid margin sync date, so the effective "
                "date of the displayed state cannot be confirmed.",
            )
        )
    elif margin.stale:
        notices.append(
            Notice(
                SEVERITY_WARNING,
                "Holdings may not be reconciled after manual execution",
                f"holdings.yaml was last synced {margin.age_days} day(s) ago "
                f"({margin.synced_at}). Recent manual Robinhood orders may not "
                "be reflected. Displayed positions and any comparison to targets "
                "are only as current as that sync.",
            )
        )

    # Buffer floor breach (forced de-lever) — repository truth only.
    if margin.below_buffer_floor is True:
        notices.append(
            Notice(
                SEVERITY_BLOCKER,
                "Margin buffer below floor (forced de-lever)",
                f"Last-synced buffer {margin.buffer_pct}% is below the "
                f"{margin.buffer_floor_pct}% floor. Per doctrine this is a "
                "forced de-lever signal. (Verify live on Robinhood before acting.)",
            )
        )

    # PHQ-2026-02 not yet filed.
    if not phq_2026_02_filed:
        notices.append(
            Notice(
                SEVERITY_INFO,
                "PHQ-2026-02 is not yet filed or implemented in GitHub",
                "No PHQ-2026-02 decision exists in this repository. Any policy "
                "change it may contain is not reflected here.",
            )
        )

    # Allocation recommendation unavailable (always, in this offline layer).
    notices.append(
        Notice(
            SEVERITY_INFO,
            "Allocation recommendation not computed by this dashboard",
            "This read-only dashboard does not run the allocator: that requires "
            "live market data (Alpaca) and reconciled holdings. Run "
            "`python allocate.py --review` in a networked session for a current "
            "recommendation. No orders are ever produced here.",
        )
    )

    # Gated names hold target capital in cash — current fact from the live
    # gates.yaml (PHQ-2026-02), not a claim about implementation status.
    if live_gates:
        notices.append(
            Notice(
                SEVERITY_INFO,
                f"{len(live_gates)} gated name(s) hold target capital in cash",
                "Per gates.yaml (current), each gated name's destination-target "
                "capital is held as ordinary cash and is never renormalized into "
                "other positions. See the Gates panel for current status per name.",
            )
        )

    # Structured PHQ-2026-01 look-through evidence unreadable — the displayed
    # ceilings are the hardcoded policy-constant fallback (8% / 40%), not read
    # from evidence, and no measured figure could be read at all.
    if lookthrough_err:
        notices.append(
            Notice(
                SEVERITY_WARNING,
                "PHQ-2026-01 look-through evidence unreadable",
                f"{lookthrough_err}. Single-issuer/AI-platform ceilings shown "
                "are the hardcoded PHQ-2026-01 policy-constant fallback "
                "(8% / 40%), not read from structured evidence, and no "
                "measured AI/platform figure could be read.",
            )
        )

    # AI/platform ceiling near/over.
    if ai_measured is not None and ai_ceiling is not None and ai_measured >= ai_ceiling:
        notices.append(
            Notice(
                SEVERITY_WARNING,
                "AI/platform common-driver exposure at/over the approved ceiling",
                f"PHQ-2026-01 recorded effective AI/platform exposure at "
                f"~{ai_measured:.2f}% against the {ai_ceiling:.0f}% ceiling — a "
                "monitoring item, recorded as measured (point-in-time).",
            )
        )

    # Intelligence issues.
    if intelligence.available and intelligence.schema_invalid:
        notices.append(
            Notice(
                SEVERITY_WARNING,
                "Schema-invalid Intelligence records",
                "One or more Company Intelligence records failed schema "
                f"validation: {', '.join(intelligence.schema_invalid)}.",
            )
        )

    for err in load_errors:
        notices.append(
            Notice(
                SEVERITY_WARNING,
                "Input file could not be read",
                err,
            )
        )

    return notices


# ── the builder ──────────────────────────────────────────────────────────────

def build_model(repo_root: Path | str, *, now: datetime | None = None) -> DashboardModel:
    """Assemble the DashboardModel from repository files + git provenance.

    Pure read: never writes anything. `now` is injectable so the single
    non-deterministic field (generation time) can be pinned in tests."""
    repo_root = Path(repo_root).resolve()
    now = now or datetime.now(timezone.utc)

    provenance = collect_provenance(repo_root, INPUT_FILES, now=now)

    load_errors: list[str] = []

    holdings_data, h_err = _safe_load_yaml(repo_root / HOLDINGS_REL)
    if h_err:
        load_errors.append(h_err)
        holdings_data = {}
    if not isinstance(holdings_data, dict):
        holdings_data = {}

    targets, t_err = _safe_load_yaml(repo_root / TARGETS_REL)
    if t_err:
        load_errors.append(t_err)
        targets = {}
    if not isinstance(targets, dict):
        targets = {}

    roster = _load_roster(targets)
    holdings = _build_holdings(holdings_data, roster)
    margin = _build_margin(holdings_data, targets)
    destination_targets = _build_destination_targets(roster)
    clusters = _build_clusters(targets)
    gates = dict((targets.get("gates") or {}))
    crypto_sleeve = _crypto_sleeve_pct(roster)

    live_gates, lg_err = _load_live_gates(repo_root / GATES_REL)
    if lg_err:
        load_errors.append(lg_err)

    gated_names, g_err = _load_gated_names(repo_root / GATED_DISPOSITION_REL)
    if g_err:
        load_errors.append(g_err)

    decisions, d_err = _load_decisions(repo_root / DECISIONS_REL)
    if d_err:
        load_errors.append(d_err)

    try:
        decision_catalog = decisions_mod.build_catalog(repo_root)
    except Exception as exc:  # pragma: no cover - defensive
        decision_catalog = decisions_mod.DecisionCatalog(
            decisions=(),
            legacy=(),
            valid_ids=frozenset(),
            legacy_ids=frozenset(),
            issues=(
                decisions_mod.LoadIssue(
                    decisions_mod.SEVERITY_ERROR,
                    "catalog-build-failed",
                    "Governance Decision Explorer catalog failed to build: "
                    f"{type(exc).__name__}: {exc}",
                ),
            ),
        )

    workstreams, w_err = _load_workstreams(repo_root / WORKSTREAMS_REL)
    if w_err:
        load_errors.append(w_err)

    intelligence = _load_intelligence(repo_root)

    single_issuer, ai_ceiling, ai_measured, lookthrough_err = _lookthrough_summary(repo_root)

    phq_2026_02_filed = (repo_root / DECISIONS_REL).exists() and any(
        d.decision_id.upper().startswith("PHQ-2026-02") for d in decisions
    )

    # SKHY unresolved: it is a live band holding but explicitly not addressed by
    # PHQ-2026-01 (see the accepted decision) — surface that plainly.
    skhy_unresolved = any(h.ticker.upper() == "SKHY" for h in holdings)

    # Controlling decisions to spotlight (present in the index).
    spotlight_ids = ["PHQ-2026-01", "OPS-0006", "GOV-0002", "MARGIN-0005"]
    present_ids = {d.decision_id for d in decisions}
    controlling = tuple(i for i in spotlight_ids if i in present_ids)

    holdings_effective_date = margin.synced_at
    holdings_effective_source = (
        "holdings.yaml margin.synced_at (last confirmed sync; no separate "
        "position-sync date is stored)"
    )

    allocation_reasons = (
        "The allocator requires live market data from Alpaca (not fetched by "
        "this offline dashboard).",
        "Current holdings may not be reconciled after recent manual Robinhood "
        "execution.",
        "This read-only dashboard displays gates.yaml/targets.yaml configuration "
        "only; it does not run or duplicate allocate.py's buy/trim recommendation "
        "logic.",
    )

    notices = _compute_notices(
        provenance=provenance,
        margin=margin,
        load_errors=load_errors,
        phq_2026_02_filed=phq_2026_02_filed,
        live_gates=live_gates,
        ai_measured=ai_measured,
        ai_ceiling=ai_ceiling,
        lookthrough_err=lookthrough_err,
        intelligence=intelligence,
    )

    spcx_state = _ticker_current_state(
        "SPCX",
        live_gates=live_gates,
        holdings=holdings,
        destination_tickers=set(roster.keys()),
    )

    return DashboardModel(
        provenance=provenance,
        generated_at_iso=provenance.generated_at_iso,
        holdings_effective_date=holdings_effective_date,
        holdings_effective_source=holdings_effective_source,
        notices=tuple(notices),
        holdings=tuple(holdings),
        crypto_sleeve_pct=crypto_sleeve,
        margin=margin,
        destination_targets=tuple(destination_targets),
        clusters=tuple(clusters),
        gates=gates,
        live_gates=tuple(live_gates.values()),
        gated_names=tuple(gated_names),
        gated_names_source=(
            "PHQ-2026-01 gated-name disposition evidence (approved gating policy, "
            "point-in-time; not live holdings)"
        ),
        spcx_state=spcx_state,
        single_issuer_ceiling_pct=single_issuer,
        ai_platform_ceiling_pct=ai_ceiling,
        ai_platform_measured_pct=ai_measured,
        skhy_unresolved=skhy_unresolved,
        allocation_available=False,
        allocation_unavailable_reasons=allocation_reasons,
        decisions=tuple(decisions),
        controlling_decisions=controlling,
        decision_catalog=decision_catalog,
        workstreams=tuple(workstreams),
        intelligence=intelligence,
        input_files=tuple(INPUT_FILES),
        phq_2026_02_filed=phq_2026_02_filed,
    )
