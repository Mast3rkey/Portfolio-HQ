"""Build the owner-interface presentation export.

Where this runs, and why that matters
-------------------------------------
This module is the **build-time, in-repository, trusted** half of the owner
interface. It runs beside the repository, reuses the repository's own canonical
calculations, and emits one JSON document. It is the *only* module in
``portfolio_hq.owner`` permitted to import investment code.

The **hosted** half (``service``/``render``/``chart_inbox``/``auth``) consumes
that JSON and nothing else. It never imports ``allocate``, never reads
``holdings.yaml``/``targets.yaml``/``gates.yaml``, and therefore cannot compute
a portfolio number of its own even by mistake. That split is the trust boundary,
and ``test_portfolio_hq_owner_interface.py`` asserts it from the import graph.

Canonical reuse — no second allocator
-------------------------------------
Every fact below comes from an existing, accepted Portfolio-HQ function:

* ``portfolio_hq.dashboard.model.build_model``  — notices, holdings, gates,
  destination targets, clusters, Intelligence summary, decisions, workstreams.
* ``level1_policy_summary.build_policy_summary`` — the Level-1 sleeve
  aggregation of accepted ``targets.yaml`` weights.
* ``allocate.load_cash_state`` / ``load_margin_state`` /
  ``current_dollar_availability`` / ``protected_weights`` — the canonical
  three-state observation classifiers, the single "may current dollars be
  published at all" gate, and the protected-capital percentages.

Nothing here re-derives a target, a weight, a recommendation, a book value or a
protected-capital dollar. Where a canonical input is unavailable the export says
so, with the canonical reason attached, and carries no number.
"""

from __future__ import annotations

import hashlib
from datetime import datetime, timezone
from pathlib import Path

from ..dashboard import model as model_mod
from .export_io import (  # re-exported for callers
    EXPORT_SCHEMA_VERSION,
    load_export,
    write_export,
)

__all__ = [
    "EXPORT_SCHEMA_VERSION",
    "build_owner_export",
    "load_export",
    "write_export",
]

#: The offline export has no market-data feed by construction: it is generated
#: from committed repository state, with no network and no brokerage connection.
#: Position valuation therefore cannot be completed, which is a genuine fact fed
#: to the canonical availability gate rather than a number invented to fill a gap.
_VALUATION_UNAVAILABLE = {
    "complete": False,
    "reason": (
        "no live market-data feed in the offline presentation export — "
        "position values, and therefore book value, cannot be computed here"
    ),
}

#: Chart timeframes the repository's own accepted chart evidence already uses
#: (the CHART-0002 cohort is daily). Offering only this avoids inventing a new
#: capture convention inside an interface unit.
ACCEPTED_CHART_TIMEFRAMES = ("1D",)

#: Instrument classes that can have a price chart at all. CASH and RESERVE
#: rows are accounting placeholders, not chartable instruments.
_CHARTABLE_ASSET_CLASSES = frozenset({"equity", "fund", "crypto"})


def _full_digests(repo_root: Path, rel_paths: list[str]) -> list[dict]:
    """Full 64-character SHA-256 for each canonical input.

    ``dashboard.provenance`` deliberately truncates to 12 characters for
    display. The machine-readable export retains the complete digest so a
    reviewer can verify exactly which bytes produced this export, without
    changing the dashboard's own display behaviour.
    """
    out: list[dict] = []
    for rel in rel_paths:
        path = repo_root / rel
        try:
            data = path.read_bytes()
        except OSError:
            out.append({"path": rel, "exists": False, "sha256": None, "size_bytes": None})
            continue
        out.append({
            "path": rel,
            "exists": True,
            "sha256": hashlib.sha256(data).hexdigest(),
            "size_bytes": len(data),
        })
    return out


def _notices(model) -> dict:
    def rows(items):
        return [{"title": n.title, "detail": n.detail} for n in items]

    return {
        "blockers": rows(model.blockers),
        "warnings": rows(model.warnings),
        "infos": rows(model.infos),
    }


def _capital(repo_root: Path, model) -> dict:
    """Dated cash/margin observations and protected-capital percentages.

    Uses ``allocate``'s own three-state classifiers so a stale balance is
    presented as dated historical evidence and never as a current figure, and
    an unknown one carries no number at all.
    """
    unavailable = {
        "available": False,
        "reason": None,
        "cash": None,
        "margin_observation": None,
        "protected_percentages": None,
    }
    try:
        import allocate  # local production module (build-time only)
        import yaml
    except Exception as exc:  # pragma: no cover - environment-dependent
        unavailable["reason"] = (
            f"canonical accounting module unavailable ({type(exc).__name__}); "
            "no cash, margin or protected-capital figure is shown"
        )
        return {**unavailable, "book": _book_block(None)}

    try:
        holdings_raw = yaml.safe_load((repo_root / model_mod.HOLDINGS_REL).read_text()) or {}
        targets_raw = yaml.safe_load((repo_root / model_mod.TARGETS_REL).read_text()) or {}
    except (OSError, ValueError, yaml.YAMLError) as exc:
        unavailable["reason"] = (
            f"canonical accounting inputs could not be read ({type(exc).__name__})"
        )
        return {**unavailable, "book": _book_block(None)}

    # The actionable-gate set is keyed by TICKER and lives in gates.yaml.
    # model.gates is a different thing entirely -- targets.yaml's allocator
    # tuning block (min_lot_dollars, trend_rsi_override, ...) -- so passing it
    # here would silently report a gated protected requirement of 0%.
    # allocate.load_gates()'s own docstring is explicit that treating an
    # absent gate set as empty is "a silent policy breach, not a benign
    # absence", so an unavailable gates.yaml yields None below, never zero.
    gates_unavailable = bool(getattr(model.spcx_state, "gates_unavailable", False))
    gates_cfg = {gate.ticker: {"status": gate.status} for gate in model.live_gates}
    try:
        cash_state = allocate.load_cash_state(holdings_raw)
        margin_state = allocate.load_margin_state(holdings_raw)
        availability = allocate.current_dollar_availability(
            cash_state, margin_state, _VALUATION_UNAVAILABLE
        )
        weights = allocate.protected_weights(targets_raw, gates_cfg)
    except Exception as exc:  # pragma: no cover - defensive
        unavailable["reason"] = (
            f"canonical accounting raised {type(exc).__name__}; no figure is shown"
        )
        return {**unavailable, "book": _book_block(None)}

    margin = model.margin
    return {
        "available": True,
        "reason": None,
        "cash": {
            "state": cash_state.get("state"),
            "usable_as_current": bool(cash_state.get("usable")),
            "balance": cash_state.get("balance"),
            "synced_at": _isoformat(cash_state.get("synced_at")),
            "age_days": cash_state.get("age_days"),
            "reason": cash_state.get("reason"),
        },
        "margin_observation": {
            "state": margin_state.get("state"),
            "usable_as_current": bool(margin_state.get("usable")),
            "debt": margin.debt,
            "buffer_pct": margin.buffer_pct,
            "synced_at": _isoformat(margin.synced_at),
            "age_days": margin.age_days,
            "age_unverifiable": margin.age_unverifiable,
            "stale": margin.stale,
            "leverage_cap": margin.leverage_cap,
            "buffer_floor_pct": margin.buffer_floor_pct,
            "below_buffer_floor": margin.below_buffer_floor,
            "reason": margin_state.get("reason"),
        },
        "protected_percentages": {
            "cash_pct": weights.get("cash_pct"),
            "reserve_pct": weights.get("reserve_pct"),
            "unreconciled_pct": weights.get("unreconciled_pct"),
            "static_protected_pct": weights.get("static_protected_pct"),
            "gated_target_pct": (
                None if gates_unavailable else weights.get("gated_target_pct")
            ),
            "gated_names": sorted(gates_cfg),
            "gated_target_pct_reason": (
                "gates.yaml could not be read, so the gated share of protected "
                "capital is unknown -- it is not zero"
                if gates_unavailable else None
            ),
            "destination_total_pct": weights.get("destination_total_pct"),
            "note": (
                "Percentages of book, derived from accepted targets.yaml. The "
                "matching dollar amounts require a current book value, which "
                "this offline export does not have."
            ),
        },
        "book": _book_block(availability),
    }


def _book_block(availability: dict | None) -> dict:
    if availability is None:
        return {
            "available": False,
            "blocked_by": [],
            "reason": "canonical availability gate could not be evaluated",
            "value": None,
        }
    return {
        "available": bool(availability.get("available")),
        "blocked_by": list(availability.get("blocked_by") or []),
        "reason": availability.get("reason"),
        # Never populated by this export: a book value needs live position
        # valuation, which is deliberately outside this offline layer.
        "value": None,
    }


def _isoformat(value: object) -> str | None:
    if value is None:
        return None
    if hasattr(value, "isoformat"):
        return value.isoformat()
    return str(value)


def _level2(model, sleeve_of: dict[str, str]) -> list[dict]:
    """One row per accepted destination instrument, joined to its live gate and
    to whether it is currently held. Every value is copied from the canonical
    model; nothing is recomputed."""
    gates = {g.ticker: g for g in model.live_gates}
    held = {h.ticker: h for h in model.holdings}
    rows = []
    for target in model.destination_targets:
        gate = gates.get(target.ticker)
        holding = held.get(target.ticker)
        rows.append({
            "ticker": target.ticker,
            "asset_class": target.asset_class,
            "sleeve": sleeve_of.get(target.ticker),
            "target_pct": target.target_pct,
            "gated": gate is not None,
            "gate_status": None if gate is None else gate.status,
            "gate_allow_add": None if gate is None else gate.allow_add,
            "gate_authority": None if gate is None else gate.authority,
            "gate_next": None if gate is None else gate.next_gate,
            "held": holding is not None,
            "held_quantity": None if holding is None else holding.quantity,
            "held_kind": None if holding is None else holding.kind,
        })
    return rows


def _level1(repo_root: Path) -> dict:
    try:
        import level1_policy_summary as lps

        summary = lps.load_policy_summary(repo_root / model_mod.TARGETS_REL)
    except Exception as exc:
        return {
            "available": False,
            "reason": (
                f"canonical Level-1 sleeve summary unavailable ({type(exc).__name__})"
            ),
            "sleeves_pct": {},
            "members": {},
            "reconciliation": {},
            "policy_basis": [],
        }
    return {
        "available": True,
        "reason": None,
        "status": summary.get("status"),
        "policy_source": summary.get("policy_source"),
        "policy_basis": summary.get("policy_basis", []),
        "units": summary.get("units"),
        "sleeves_pct": summary.get("sleeves_pct", {}),
        "members": summary.get("members", {}),
        "reconciliation": summary.get("reconciliation", {}),
    }


def _sleeve_index(level1: dict) -> dict[str, str]:
    index: dict[str, str] = {}
    for sleeve, members in (level1.get("members") or {}).items():
        for ticker in members or []:
            index[str(ticker)] = sleeve
    return index


def _intelligence(model) -> dict:
    intel = model.intelligence
    return {
        "available": intel.available,
        "note": intel.note,
        "company_records": intel.company_yaml_count,
        "company_notes": intel.company_markdown_count,
        "theme_records": intel.theme_yaml_count,
        "companies_scanned": intel.companies_scanned,
        "overdue_reviews": [
            {"ticker": t, "detail": d} for t, d in intel.overdue_reviews
        ],
        "schema_invalid": list(intel.schema_invalid),
        "role_drift": [{"ticker": t, "detail": d} for t, d in intel.role_drift_mismatches],
        "freshness_rows": intel.freshness_rows,
        "monitoring_enabled_rows": intel.monitoring_enabled_rows,
    }


def _chart_request(model) -> dict:
    """The instruments a chart may legitimately be attached to.

    This is an *allowlist for intake validation*, derived from accepted
    ``targets.yaml`` rows — not a research instruction and not a request for a
    production batch. No batch is requested by this unit.
    """
    eligible = sorted(
        t.ticker for t in model.destination_targets
        if (t.asset_class or "") in _CHARTABLE_ASSET_CLASSES
    )
    return {
        "eligible_tickers": eligible,
        "accepted_timeframes": list(ACCEPTED_CHART_TIMEFRAMES),
        "requested_batch_specified": False,
        "instructions": (
            "Capture the whole chart window, unobscured, and include the "
            "instrument and timeframe labels. Do not include account balances, "
            "positions, order history, buying power or margin figures anywhere "
            "in the image."
        ),
        "note": (
            "No production chart batch has been requested. Uploads are accepted "
            "now so the intake path itself can be reviewed; a chart is evidence "
            "receipt only and adopts nothing."
        ),
    }


def build_owner_export(repo_root: Path | str, *, now: datetime | None = None) -> dict:
    """Build the complete presentation export for one accepted source state."""
    repo_root = Path(repo_root).resolve()
    model = model_mod.build_model(repo_root, now=now)
    provenance = model.provenance
    level1 = _level1(repo_root)
    generated_at = (now or datetime.now(timezone.utc)).astimezone(timezone.utc)

    return {
        "schema_version": EXPORT_SCHEMA_VERSION,
        "meta": {
            "generated_at": generated_at.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "repo_name": provenance.repo_name,
            "source_commit": provenance.commit_sha,
            "source_commit_short": provenance.commit_short,
            "source_commit_iso": provenance.commit_iso,
            "source_commit_subject": provenance.commit_subject,
            "branch": provenance.branch,
            "git_available": provenance.git_available,
            "worktree_dirty": provenance.dirty,
            "worktree_dirty_path_count": len(provenance.dirty_paths),
        },
        "input_digests": _full_digests(repo_root, list(model_mod.INPUT_FILES)),
        "attention": _notices(model),
        "recommendation_state": {
            "allocation_available": model.allocation_available,
            "unavailable_reasons": list(model.allocation_unavailable_reasons),
            "disclosure": (
                "Portfolio-HQ is recommendation-only. It never places, routes or "
                "submits an order, and it holds no brokerage connection."
            ),
        },
        "capital": _capital(repo_root, model),
        "holdings_effective": {
            "date": model.holdings_effective_date,
            "source": model.holdings_effective_source,
        },
        "level1": level1,
        "level2": _level2(model, _sleeve_index(level1)),
        "concentration": {
            "clusters": [
                {"name": c.name, "cap_pct": c.pct, "tickers": list(c.tickers)}
                for c in model.clusters
            ],
            "single_issuer_ceiling_pct": model.single_issuer_ceiling_pct,
            "ai_platform_ceiling_pct": model.ai_platform_ceiling_pct,
            "ai_platform_measured_pct": model.ai_platform_measured_pct,
            "crypto_sleeve_pct": model.crypto_sleeve_pct,
        },
        "gates": [
            {
                "ticker": g.ticker,
                "status": g.status,
                "authority": g.authority,
                "allow_add": g.allow_add,
                "holds_existing_shares": g.holds_existing_shares,
                "next_gate": g.next_gate,
            }
            for g in model.live_gates
        ],
        "intelligence": _intelligence(model),
        "decisions_index": [
            {
                "decision_id": d.decision_id,
                "date": d.date,
                "status": d.status,
                "category": d.category,
            }
            for d in model.decisions
        ],
        "workstreams": [
            {
                "id": w.ws_id,
                "title": w.title,
                "status": w.status,
                "priority": w.priority,
                "next_action": w.next_action,
            }
            for w in model.workstreams
        ],
        "chart_request": _chart_request(model),
        "boundaries": {
            "recommendation_only": True,
            "places_orders": False,
            "brokerage_connected": False,
            "reads_live_account": False,
            "arms_or_executes_stage1": False,
            "mutates_repository_state": False,
        },
    }
