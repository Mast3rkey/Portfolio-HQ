"""Generates intelligence/valuation_evidence/<TICKER>.yaml records and the
cohort manifest from structured per-ticker research data (TICKER_DATA below).

Authorized by VALUATION-0005 (Stage-3 evidence-population implementation).
Reuses valuation_evidence_validator.py's schema and canonical_record_hash()
exclusively -- this module performs no independent schema logic.

Run: python3 valuation_evidence_generator.py
"""
from __future__ import annotations

import datetime
import pathlib

import yaml

import valuation_evidence_validator as vv

REPO_ROOT = pathlib.Path(__file__).resolve().parent
OUT_DIR = REPO_ROOT / "intelligence" / "valuation_evidence"
GOVERNING_DECISION = "VALUATION-0005"
SHARD_ID = "ws0015-valuation0005-stage3-implementation"


def src(identifier, source_type, as_of, access_status, limitation=None):
    entry = {
        "source_identifier": identifier,
        "source_type": source_type,
        "as_of_date": as_of,
        "access_status": access_status,
    }
    if limitation:
        entry["limitation"] = limitation
    return entry


def prov(*sources):
    return {"sources": list(sources)}


def reported(category, value, unit, provenance, conflicts=None):
    item = {
        "item_category": category,
        "value": value,
        "unit": unit,
        "value_basis": "reported",
        "provenance": provenance,
    }
    if conflicts:
        item["disclosed_conflicts"] = conflicts
    return item


def derived(category, value, unit, note, provenance, conflicts=None):
    item = {
        "item_category": category,
        "value": value,
        "unit": unit,
        "value_basis": "derived",
        "derivation_note": note,
        "provenance": provenance,
    }
    if conflicts:
        item["disclosed_conflicts"] = conflicts
    return item


def abstain_item(category, reason):
    return {"item_category": category, "abstention_reason": reason}


def period(period_type, fiscal_end, as_of, line_items, restated=False, restated_note=None):
    p = {
        "period_type": period_type,
        "fiscal_period_end_date": fiscal_end,
        "as_of_date": as_of,
        "restated": restated,
        "line_items": line_items,
    }
    if restated:
        p["restated_from_note"] = restated_note
    return p


def market_input(name, value, unit, as_of, provenance, basis="reported", note=None):
    item = {
        "input_name": name,
        "value": value,
        "unit": unit,
        "as_of_date": as_of,
        "value_basis": basis,
        "provenance": provenance,
    }
    if basis == "derived":
        item["derivation_note"] = note
    return item


def market_input_abstain(name, reason):
    return {"input_name": name, "abstention_reason": reason}


def component(value, label, provenance, note=None):
    c = {"value": value, "provenance_label": label, "provenance": provenance}
    if note:
        c["note"] = note
    return c


def tax_component(value, tax_type, label, provenance, note=None):
    c = component(value, label, provenance, note)
    c["tax_rate_type"] = tax_type
    return c


def capital_structure(debt_weight, equity_weight, label, provenance):
    return {
        "debt_weight": debt_weight,
        "equity_weight": equity_weight,
        "provenance_label": label,
        "provenance": provenance,
    }


def peer(identity, rationale, provenance, as_of, status, status_rationale):
    return {
        "identity": identity,
        "comparability_rationale": rationale,
        "provenance": provenance,
        "as_of_date": as_of,
        "inclusion_status": status,
        "inclusion_rationale": status_rationale,
    }


def scenario_var(name, evidence_basis, label):
    return {"variable_name": name, "evidence_basis": evidence_basis, "provenance_label": label}


def scenario(name, variables):
    return {"scenario_name": name, "variables": variables}


def segment(name, revenue=None, profit=None, cash_flow=None):
    s = {"segment_name": name}
    if revenue is not None:
        s["revenue"] = revenue
    if profit is not None:
        s["profit"] = profit
    if cash_flow is not None:
        s["cash_flow"] = cash_flow
    return s


def build_record(ticker, *, financial_periods=None, financial_abstain=None,
                  segments=None, segment_abstain=None, shared_unallocated_costs=None,
                  intersegment_eliminations=None,
                  market_inputs=None, market_abstain=None,
                  discount_components=None, discount_abstain=None,
                  peer_candidates=None, peer_abstain=None,
                  scenarios_list=None, scenario_abstain=None,
                  uncertainty_summary, review_cadence_days=90):
    financial_evidence = {"periods": financial_periods or []}
    if not financial_periods:
        financial_evidence["abstention_reason"] = financial_abstain

    segment_evidence = {"segments": segments or []}
    if not segments:
        segment_evidence["abstention_reason"] = segment_abstain
    if shared_unallocated_costs:
        segment_evidence["shared_unallocated_costs"] = shared_unallocated_costs
    if intersegment_eliminations:
        segment_evidence["intersegment_eliminations"] = intersegment_eliminations

    market_observed_evidence = {"inputs": market_inputs or []}
    if not market_inputs:
        market_observed_evidence["abstention_reason"] = market_abstain

    discount_rate_evidence = dict(discount_components or {})
    if not discount_components:
        discount_rate_evidence["abstention_reason"] = discount_abstain

    peer_set_evidence = {"candidates": peer_candidates or []}
    if not peer_candidates:
        peer_set_evidence["abstention_reason"] = peer_abstain

    scenario_evidence = {"scenarios": scenarios_list or []}
    if not scenarios_list:
        scenario_evidence["abstention_reason"] = scenario_abstain

    # Collect every as_of_date in the document to compute freshness_state.
    dates = set()

    def _walk(obj):
        if isinstance(obj, dict):
            if "as_of_date" in obj and isinstance(obj["as_of_date"], str):
                dates.add(obj["as_of_date"])
            for v in obj.values():
                _walk(v)
        elif isinstance(obj, list):
            for v in obj:
                _walk(v)

    domains = {
        "financial_evidence": financial_evidence,
        "segment_evidence": segment_evidence,
        "market_observed_evidence": market_observed_evidence,
        "discount_rate_evidence": discount_rate_evidence,
        "peer_set_evidence": peer_set_evidence,
        "scenario_evidence": scenario_evidence,
    }
    _walk(domains)

    if dates:
        most_recent = max(dates)
    else:
        most_recent = datetime.date(2026, 8, 9).isoformat()

    next_due = (
        datetime.date.fromisoformat(most_recent) + datetime.timedelta(days=review_cadence_days)
    ).isoformat()

    abstention_index = []
    abstain_map = {
        "financial_evidence": financial_abstain if not financial_periods else None,
        "segment_evidence": segment_abstain if not segments else None,
        "market_observed_evidence": market_abstain if not market_inputs else None,
        "discount_rate_evidence": discount_abstain if not discount_components else None,
        "peer_set_evidence": peer_abstain if not peer_candidates else None,
        "scenario_evidence": scenario_abstain if not scenarios_list else None,
    }
    for domain, reason in abstain_map.items():
        if reason:
            abstention_index.append({"domain": domain, "reason": reason})

    record = {
        "schema_version": "1.0",
        "ticker": ticker,
        "asset_class": "equity",
        **domains,
        "uncertainty_summary": uncertainty_summary,
        "abstention_index": abstention_index,
        "freshness_state": {
            "most_recent_evidence_date": most_recent,
            "review_cadence_days": review_cadence_days,
            "next_review_due_date": next_due,
            "stale": False,
        },
        "record_status": "draft",
    }
    return record


def seal(record, sealed_at="2026-08-09T00:00:00Z"):
    record = dict(record)
    record["record_status"] = "sealed"
    record["sealed_at"] = sealed_at
    record["governing_decision"] = GOVERNING_DECISION
    record["drafting_session_or_shard_id"] = SHARD_ID
    record["cohort_manifest_entry"] = record["ticker"]
    record["content_sha256"] = vv.canonical_record_hash(record)
    return record


def write_records(records: dict[str, dict]):
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    manifest_rows = []
    for ticker, record in sorted(records.items()):
        sealed_record = seal(record)
        path = OUT_DIR / f"{ticker}.yaml"
        with open(path, "w") as f:
            yaml.safe_dump(sealed_record, f, sort_keys=False, allow_unicode=True, width=100)
        manifest_rows.append({
            "ticker": ticker,
            "sealed_at": sealed_record["sealed_at"],
            "content_sha256": sealed_record["content_sha256"],
            "schema_version": sealed_record["schema_version"],
            "governing_decision": GOVERNING_DECISION,
            "record_path": f"intelligence/valuation_evidence/{ticker}.yaml",
        })
    manifest = {
        "schema_version": "1.0",
        "governing_decision": GOVERNING_DECISION,
        "cohort": manifest_rows,
    }
    with open(OUT_DIR / "COHORT_MANIFEST.yaml", "w") as f:
        yaml.safe_dump(manifest, f, sort_keys=False, allow_unicode=True, width=100)
    print(f"Wrote {len(manifest_rows)} records + manifest to {OUT_DIR}")


if __name__ == "__main__":
    import ticker_data  # populated separately per shard

    write_records(ticker_data.RECORDS)
