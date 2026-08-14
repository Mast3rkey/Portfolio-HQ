"""Deterministic, network-free RISK-0001 data gate and metric primitives."""

from __future__ import annotations

import hashlib
import json
import math
import statistics
from collections import defaultdict
from datetime import date, datetime, time, timedelta, timezone
from decimal import Decimal
from pathlib import Path
from typing import Any, Iterable, Mapping
from zoneinfo import ZoneInfo

import exchange_calendars as xcals
import pandas as pd
import yaml
from pandas.tseries.holiday import USFederalHolidayCalendar
from pandas.tseries.offsets import CustomBusinessDay


ROOT = Path(__file__).resolve().parent
STUDY = ROOT / "research/level1_sleeve_robustness"
DATA = STUDY / "data"
CONFIG_PATH = STUDY / "implementation_config.yaml"
PREREG_PATH = STUDY / "pre_registration.yaml"
PROTOCOL_PATH = STUDY / "PROTOCOL_V1.md"
AUTHORITY_PATH = ROOT / "governance/decisions/RISK-0001-level1-investable-sleeve-robustness-charter.md"
SOURCE_INVENTORY_PATH = DATA / "source_inventory.json"
MANIFEST_PATH = STUDY / "data_manifest.yaml"
ELIGIBILITY_PATH = STUDY / "eligibility_matrix.json"
TRIAL_REGISTRY_PATH = STUDY / "trial_registry.json"
ATTEMPT_1_ID = "RISK-0001-EXECUTION-ATTEMPT-001"
ATTEMPT_2_ID = "RISK-0001-EXECUTION-ATTEMPT-002"
ATTEMPTS = STUDY / "attempts"
ATTEMPT_1 = ATTEMPTS / ATTEMPT_1_ID
ATTEMPT_2 = ATTEMPTS / ATTEMPT_2_ID
ATTEMPT_1_FREEZE_PATH = ATTEMPT_1 / "data_gate_freeze.json"
ATTEMPT_2_STAGE_A_PATH = ATTEMPT_2 / "stage_a_integrity_attestation.json"
ATTEMPT_2_METADATA_PATH = ATTEMPT_2 / "preexecution_metadata.json"
ATTEMPT_2_TRANSPLANT_MANIFEST_PATH = ATTEMPT_2 / "frozen_artifact_transplant_manifest.json"
ATTEMPT_2_REVIEW_RECEIPT_PATH = ATTEMPT_2 / "independent_preexecution_review.json"
FREEZE_PATH = ATTEMPT_2_STAGE_A_PATH
RESULTS = ATTEMPT_2 / "results"
WINDOWS = ("ASSET_AVAILABLE_HISTORY", "FAMILY_COMMON_OVERLAP", "GFC_2008", "Q4_2018", "COVID_2020", "RATE_INFLATION_2022", "CRYPTO_STRESS_2022")
SCENARIOS = ("LOWER", "HISTORICAL_REFERENCE", "HIGHER")
FAMILIES = ("EQUITY", "FUND_BROAD_MARKET", "FUND_GLD_DEFENSIVE", "CRYPTO")
VOTING_PLAN = (
    ("EXPOSURE_SCALED_DRAWDOWN_LOSS", "ASSET_AVAILABLE_HISTORY"),
    ("EXPOSURE_SCALED_DRAWDOWN_LOSS", "FAMILY_COMMON_OVERLAP"),
    ("EXPOSURE_SCALED_STRESS_LOSS", "GFC_2008"),
    ("EXPOSURE_SCALED_STRESS_LOSS", "Q4_2018"),
    ("EXPOSURE_SCALED_STRESS_LOSS", "COVID_2020"),
    ("EXPOSURE_SCALED_STRESS_LOSS", "RATE_INFLATION_2022"),
    ("EXPOSURE_SCALED_STRESS_LOSS", "CRYPTO_STRESS_2022"),
    ("EXPOSURE_SCALED_UNDERWATER_BURDEN", "ASSET_AVAILABLE_HISTORY"),
    ("EXPOSURE_SCALED_UNDERWATER_BURDEN", "FAMILY_COMMON_OVERLAP"),
    ("EXPOSURE_SCALED_EXCESS_CONTRIBUTION", "ASSET_AVAILABLE_HISTORY"),
    ("EXPOSURE_SCALED_EXCESS_CONTRIBUTION", "FAMILY_COMMON_OVERLAP"),
)
MISSINGNESS = ("ELIGIBLE", "NOT_APPLICABLE_PRE_INCEPTION", "MISSING_SOURCE_DATA", "KNOWN_DATA_GAP", "CORPORATE_ACTION_UNRESOLVED", "CONDITIONAL_ASSET_NOT_ACQUIRED", "QUALITY_GATE_FAILED")


class IntegrityError(RuntimeError):
    pass


def load_yaml(path: Path) -> dict[str, Any]:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if type(value) is not dict:
        raise IntegrityError(f"{path}: mapping required")
    return value


def _unique_object_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    """Preserve JSON object order while rejecting duplicate keys at every depth."""
    value: dict[str, Any] = {}
    for key, item in pairs:
        if key in value:
            raise IntegrityError(f"duplicate JSON object key: {key!r}")
        value[key] = item
    return value


def load_schema_json_bytes(payload: bytes) -> dict[str, Any]:
    """Load schema-bearing JSON bytes without changing insertion order."""
    value = json.loads(payload.decode("utf-8"), object_pairs_hook=_unique_object_pairs)
    if type(value) is not dict:
        raise IntegrityError("schema JSON root mapping required")
    return value


def load_schema_json(path: Path) -> dict[str, Any]:
    """Load schema-bearing JSON without changing insertion order."""
    return load_schema_json_bytes(path.read_bytes())


def load_json(path: Path) -> dict[str, Any]:
    """Compatibility name for the strict schema-bearing JSON loader."""
    return load_schema_json(path)


def canonical_json_bytes(value: Any) -> bytes:
    """Order-insensitive canonical bytes used only for canonical hashes."""
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n").encode()


def schema_json_bytes(value: Any) -> bytes:
    """Deterministic persistence bytes that preserve registered mapping order."""
    return (json.dumps(value, sort_keys=False, separators=(",", ":"), ensure_ascii=False) + "\n").encode()


def write_schema_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(schema_json_bytes(value))


def write_json(path: Path, value: Any) -> None:
    """Compatibility name for order-sensitive schema persistence."""
    write_schema_json(path, value)


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def canonical_hash(value: Any) -> str:
    return sha256_bytes(canonical_json_bytes(value))


def family_representations(prereg: Mapping[str, Any]) -> dict[str, list[str]]:
    return {
        "EQUITY": list(prereg["representations"]["EQUITY"]["ids"]),
        "FUND_BROAD_MARKET": list(prereg["representations"]["FUND_BROAD_MARKET"]["ids"]),
        "FUND_GLD_DEFENSIVE": list(prereg["representations"]["FUND_GLD_DEFENSIVE"]["core_ids"])
        + list(prereg["representations"]["FUND_GLD_DEFENSIVE"]["conditional_ids"]),
        "CRYPTO": list(prereg["representations"]["CRYPTO"]["ids"]),
    }


def representation_family(prereg: Mapping[str, Any]) -> dict[str, str]:
    return {rep: family for family, reps in family_representations(prereg).items() for rep in reps}


def xny_schedule(start: str, end: str) -> list[dict[str, str]]:
    calendar = xcals.get_calendar("XNYS", start="2004-11-18", end="2026-07-31")
    schedule = calendar.schedule.loc[start:end]
    rows = []
    for session, row in schedule.iterrows():
        rows.append({"session": session.date().isoformat(), "open_utc": row["open"].isoformat(), "close_utc": row["close"].isoformat()})
    return rows


def federal_business_days(start: str, end: str) -> list[str]:
    offset = CustomBusinessDay(calendar=USFederalHolidayCalendar())
    return [value.date().isoformat() for value in pd.date_range(start=start, end=end, freq=offset)]


def selected_record(source_inventory: Mapping[str, Any], representation: str) -> Mapping[str, Any]:
    rows = list(source_inventory["stock_and_etf_datasets"]) + list(source_inventory["crypto_datasets"])
    matches = [row for row in rows if row["instrument"] == representation]
    if len(matches) != 1:
        raise IntegrityError(f"source inventory identity {representation}: exactly one record required")
    return matches[0]


def selected_document(record: Mapping[str, Any]) -> dict[str, Any] | None:
    path_text = record.get("selected_path")
    if not path_text:
        return None
    path = ROOT / path_text
    if not path.is_file() or sha256_file(path) != record["selected_transformed_sha256"]:
        raise IntegrityError(f"selected input missing or hash mismatch: {path_text}")
    return load_json(path)


def _date_range(start: str, end: str) -> list[str]:
    first, last = date.fromisoformat(start), date.fromisoformat(end)
    return [(first + timedelta(days=index)).isoformat() for index in range((last - first).days + 1)]


def _window_bounds(prereg: Mapping[str, Any], family: str, representation: str, window_id: str, first_observation: str | None, lawful_inception: str | None) -> tuple[str, str] | None:
    window = next(item for item in prereg["scenario_windows"]["windows"] if item["id"] == window_id)
    end = window["end"]
    if window_id == "ASSET_AVAILABLE_HISTORY":
        candidates = [window["start"]]
        if first_observation:
            candidates.append(first_observation)
        if lawful_inception:
            candidates.append(lawful_inception)
        return max(candidates), end
    start = window["start_by_family"][family] if window_id == "FAMILY_COMMON_OVERLAP" else window["start"]
    if lawful_inception and lawful_inception > start:
        return None
    if first_observation and first_observation > start:
        return None
    return start, end


def _gap_intersects(quality: Mapping[str, Any] | None, start: str, end: str) -> bool:
    if not quality:
        return True
    return any(block["start"] <= end and block["end"] >= start for block in quality.get("gap_blocks", []))


def _action_date(row: Mapping[str, Any]) -> str | None:
    for key in ("ex_date", "process_date", "effective_date"):
        value = row.get(key)
        if isinstance(value, str) and len(value) >= 10:
            return value[:10]
    return None


def unresolved_actions(document: Mapping[str, Any], representation: str, config: Mapping[str, Any]) -> list[str]:
    dates = []
    for row in document.get("events", []):
        kind = row.get("action_type")
        if kind not in ("cash_dividend", "split", "cash_dividends", "splits"):
            value = _action_date(row)
            if value:
                dates.append(value)
    known = config.get("known_action_boundaries", {}).get(representation)
    if known and known["treatment"].startswith("UNRESOLVED"):
        dates.append(known["event_date"])
    return sorted(set(dates))


def _max_drawdown(index: list[tuple[str, float]]) -> float:
    if len(index) < 2:
        raise IntegrityError("at least two index values required")
    peak = index[0][1]
    worst = 0.0
    for _, value in index:
        peak = max(peak, value)
        worst = min(worst, value / peak - 1.0)
    return worst


def _annualized_return(index: list[tuple[str, float]]) -> float:
    days = (date.fromisoformat(index[-1][0]) - date.fromisoformat(index[0][0])).days
    if days <= 0 or index[0][1] <= 0 or index[-1][1] <= 0:
        raise IntegrityError("annualized return requires positive multi-day path")
    return (index[-1][1] / index[0][1]) ** (365.0 / days) - 1.0


def _returns(index: list[tuple[str, float]]) -> list[tuple[str, float]]:
    return [(index[i][0], index[i][1] / index[i - 1][1] - 1.0) for i in range(1, len(index))]


def total_return_index(document: Mapping[str, Any], start: str, end: str) -> list[tuple[str, float]]:
    rows = [row for row in document["rows"] if start <= row["date"] <= end]
    if len(rows) < 2:
        raise IntegrityError("window has fewer than two observations")
    events_by_date: dict[str, float] = defaultdict(float)
    split_events = []
    for event in document.get("events", []):
        kind = event.get("action_type")
        ex_date = event.get("ex_date")
        if not ex_date:
            continue
        if kind in ("cash_dividend", "cash_dividends"):
            rate = event.get("rate")
            if rate is None:
                raise IntegrityError("dividend amount missing")
            events_by_date[str(ex_date)[:10]] += float(rate)
        elif kind in ("split", "splits"):
            new_rate, old_rate = event.get("new_rate"), event.get("old_rate")
            if new_rate and old_rate:
                split_events.append((str(ex_date)[:10], float(new_rate) / float(old_rate)))
    # Alpaca dividends are declared in then-current shares while its historical
    # bars are split-adjusted. Bring each dividend onto the same share basis.
    if document.get("provider") == "ALPACA_MARKET_DATA":
        adjusted: dict[str, float] = {}
        for ex_date, amount in events_by_date.items():
            future_factor = math.prod(factor for split_date, factor in split_events if split_date > ex_date)
            adjusted[ex_date] = amount / future_factor if future_factor else amount
        events_by_date = defaultdict(float, adjusted)
    index = [(rows[0]["date"], 1.0)]
    prior_close = float(rows[0]["close"])
    value = 1.0
    for row in rows[1:]:
        close = float(row["close"])
        gross = (close + events_by_date[row["date"]]) / prior_close
        if not math.isfinite(gross) or gross <= 0:
            raise IntegrityError("nonpositive total-return factor")
        value *= gross
        index.append((row["date"], value))
        prior_close = close
    return index


def align_crypto_to_xnys(document: Mapping[str, Any], start: str, end: str, schedule: list[Mapping[str, str]]) -> list[tuple[str, float]]:
    closes = {row["date"]: float(row["close"]) for row in document["rows"]}
    completed = sorted((datetime.combine(date.fromisoformat(day) + timedelta(days=1), time.min, tzinfo=timezone.utc), day, close)
                       for day, close in closes.items())
    selected: list[tuple[str, float]] = []
    cursor = -1
    latest: tuple[datetime, str, float] | None = None
    for session in schedule:
        session_date = session["session"]
        if not (start <= session_date <= end):
            continue
        close_ts = datetime.fromisoformat(session["close_utc"].replace("Z", "+00:00"))
        while cursor + 1 < len(completed) and completed[cursor + 1][0] <= close_ts:
            cursor += 1
            latest = completed[cursor]
        if latest is None:
            continue
        selected.append((session_date, latest[2]))
    if len(selected) < 2:
        raise IntegrityError("crypto alignment has fewer than two sessions")
    base = selected[0][1]
    return [(day, close / base) for day, close in selected]


def _dff_rows(document: Mapping[str, Any]) -> dict[str, Decimal]:
    return {row["date"]: Decimal(row["rate_pct"]) for row in document["rows"]}


def dff_total_return(document: Mapping[str, Any], start: str, end: str) -> tuple[float | None, list[str]]:
    rates = _dff_rows(document)
    lookback_start = (date.fromisoformat(start) - timedelta(days=10)).isoformat()
    required_business_days = federal_business_days(lookback_start, end)
    missing = [day for day in required_business_days if day not in rates]
    if missing:
        return None, missing
    business = set(required_business_days)
    offset = CustomBusinessDay(calendar=USFederalHolidayCalendar())
    lawful: list[tuple[str, Decimal]] = []
    for observation_day in sorted(day for day in rates if lookback_start <= day <= end and day in business):
        candidate = (pd.Timestamp(observation_day) + offset).date().isoformat()
        lawful.append((candidate, rates[observation_day]))
    factor = Decimal("1")
    unavailable: list[str] = []
    for accrual_day in _date_range((date.fromisoformat(start) + timedelta(days=1)).isoformat(), end):
        # The observation is lawful only at 23:59:59 America/New_York on the
        # lagged business day, after that day's XNYS close.  It can therefore
        # first inform the following calendar-day evaluation.
        available = [rate for lawful_day, rate in lawful if lawful_day < accrual_day]
        if not available:
            unavailable.append(accrual_day)
            continue
        factor *= Decimal("1") + (available[-1] / Decimal("100")) / Decimal("360")
    if unavailable:
        return None, unavailable
    return float(factor - Decimal("1")), []


def path_metrics(index: list[tuple[str, float]], annualization: int) -> dict[str, Any]:
    returns = _returns(index)
    total = index[-1][1] / index[0][1] - 1.0
    peak = index[0][1]
    peak_index = 0
    underwater = 0.0
    deepest_drawdown = 0.0
    deepest_peak_index = 0
    deepest_trough_index = 0
    for idx, (day, value) in enumerate(index):
        interval = 0 if idx == 0 else (date.fromisoformat(day) - date.fromisoformat(index[idx - 1][0])).days
        if value > peak:
            peak = value
            peak_index = idx
        depth = max(0.0, 1.0 - value / peak)
        underwater += depth * interval
        if -depth < deepest_drawdown:
            deepest_drawdown = -depth
            deepest_peak_index = peak_index
            deepest_trough_index = idx
    recovery_index = None
    if deepest_drawdown < 0:
        deepest_peak_value = index[deepest_peak_index][1]
        recovery_index = next((idx for idx in range(deepest_trough_index + 1, len(index))
                               if index[idx][1] >= deepest_peak_value), None)
    period_factors: dict[str, float] = defaultdict(lambda: 1.0)
    quarter_factors: dict[str, float] = defaultdict(lambda: 1.0)
    for day, value in returns:
        period_factors[day[:7]] *= 1.0 + value
        year, month_num = map(int, day[:7].split("-"))
        quarter_factors[f"{year}-Q{(month_num - 1) // 3 + 1}"] *= 1.0 + value
    month_returns = [factor - 1.0 for factor in period_factors.values()]
    quarter_returns = [factor - 1.0 for factor in quarter_factors.values()]
    volatility = statistics.stdev([value for _, value in returns]) * math.sqrt(annualization) if len(returns) >= 2 else None
    recovery_days = (None if recovery_index is None else
                     (date.fromisoformat(index[recovery_index][0]) - date.fromisoformat(index[deepest_peak_index][0])).days)
    return {"asset_total_return": total, "max_drawdown": deepest_drawdown,
            "worst_month": min(month_returns) if month_returns else None,
            "worst_quarter": min(quarter_returns) if quarter_returns else None,
            "volatility": volatility, "underwater_area_days": underwater,
            "recovery_duration_days": recovery_days,
            "recovery_censor_status": "CENSORED_AT_WINDOW_END" if recovery_index is None and deepest_drawdown < 0 else "RECOVERED",
            "deepest_trough_date": index[deepest_trough_index][0]}


def gold_peer_evidence(documents: Mapping[str, Mapping[str, Any] | None], eligibility_quality: Mapping[str, Any], schedule: list[Mapping[str, str]]) -> list[dict[str, Any]]:
    output = []
    gld = documents.get("GLD")
    for peer in ("IAU", "SGOL", "GLDM"):
        document = documents.get(peer)
        complete = gld is not None and document is not None
        correlation = Decimal("0")
        return_diff = Decimal("999")
        drawdown_diff = Decimal("999")
        gaps = int((eligibility_quality.get(peer) or {}).get("missing_count", 999999))
        if complete:
            start = "2018-06-26"
            end = "2026-07-31"
            try:
                gld_index = total_return_index(gld, start, end)
                peer_index = total_return_index(document, start, end)
                gld_returns = dict(_returns(gld_index))
                peer_returns = dict(_returns(peer_index))
                common = sorted(set(gld_returns) & set(peer_returns))
                if len(common) >= 2:
                    correlation = Decimal(str(pd.Series([gld_returns[d] for d in common]).corr(pd.Series([peer_returns[d] for d in common]))))
                    return_diff = Decimal(str((_annualized_return(peer_index) - _annualized_return(gld_index)) * 100.0))
                    drawdown_diff = Decimal(str((_max_drawdown(peer_index) - _max_drawdown(gld_index)) * 100.0))
            except (IntegrityError, ValueError, ArithmeticError):
                complete = False
        output.append({"peer_id": peer,
                       "identity_and_inception": "COMPLETE" if complete else "INCOMPLETE",
                       "unresolved_required_session_gaps": gaps,
                       "dividend_split_action_treatment": "COMPLETE" if complete else "INCOMPLETE",
                       "overlap_total_return_correlation": str(correlation),
                       "overlap_annualized_return_difference_pp": str(return_diff),
                       "overlap_max_drawdown_difference_pp": str(drawdown_diff)})
    return output


def admitted_gold_peers(prereg: Mapping[str, Any], evidence: Iterable[Mapping[str, Any]]) -> list[str]:
    params = {row["parameter_id"]: row["value"] for row in prereg["consequential_parameter_registry"]["parameters"]}
    admitted = []
    for row in evidence:
        if (row["identity_and_inception"] == "COMPLETE"
                and row["unresolved_required_session_gaps"] == int(params["GOLD_UNRESOLVED_SESSION_GAPS_ALLOWED"])
                and row["dividend_split_action_treatment"] == "COMPLETE"
                and Decimal(row["overlap_total_return_correlation"]) >= Decimal(params["GOLD_PARITY_CORRELATION_MIN"])
                and abs(Decimal(row["overlap_annualized_return_difference_pp"])) <= Decimal(params["GOLD_PARITY_RETURN_MAX_PP"])
                and abs(Decimal(row["overlap_max_drawdown_difference_pp"])) <= Decimal(params["GOLD_PARITY_DRAWDOWN_MAX_PP"])):
            admitted.append(row["peer_id"])
    return admitted


def build_eligibility(prereg: Mapping[str, Any], config: Mapping[str, Any], source_inventory: Mapping[str, Any], documents: Mapping[str, Mapping[str, Any] | None], gold_admitted: set[str]) -> dict[str, Any]:
    rep_family = representation_family(prereg)
    records = []
    quality_map = {}
    for rep in rep_family:
        source = selected_record(source_inventory, rep)
        quality = source.get("primary_quality") if source.get("selected_provider", "").startswith("ALPACA") else source.get("fallback_quality")
        quality_map[rep] = quality
        document = documents.get(rep)
        inception = source.get("lawful_inception") or (config.get("identity_boundaries", {}).get(rep) or {}).get("lawful_inception")
        first = (quality or {}).get("first_observation")
        unresolved = unresolved_actions(document or {"events": []}, rep, config)
        for scenario in SCENARIOS:
            for window_id in WINDOWS:
                bounds = _window_bounds(prereg, rep_family[rep], rep, window_id, first, inception)
                if document is None:
                    state, reason, start, end = "MISSING_SOURCE_DATA", "NO_SELECTED_WHOLE_PATH_SOURCE", None, None
                elif rep in ("IAU", "SGOL", "GLDM") and rep not in gold_admitted:
                    state, reason, start, end = "CONDITIONAL_ASSET_NOT_ACQUIRED", "FAILED_OR_INCOMPLETE_GOLD_ADMISSION_GATE", None, None
                elif bounds is None:
                    window = next(item for item in prereg["scenario_windows"]["windows"] if item["id"] == window_id)
                    registered_start = (window["start_by_family"][rep_family[rep]]
                                        if window_id == "FAMILY_COMMON_OVERLAP" else window["start"])
                    if inception and inception > registered_start:
                        state, reason = "NOT_APPLICABLE_PRE_INCEPTION", "WINDOW_STARTS_BEFORE_LAWFUL_INCEPTION"
                    else:
                        state, reason = "MISSING_SOURCE_DATA", "SOURCE_COVERAGE_STARTS_AFTER_REGISTERED_WINDOW_START"
                    start, end = None, None
                else:
                    start, end = bounds
                    if _gap_intersects(quality, start, end):
                        state, reason = "KNOWN_DATA_GAP", "VALIDATED_GAP_INTERSECTS_WINDOW"
                    elif any(start <= value <= end for value in unresolved):
                        state, reason = "CORPORATE_ACTION_UNRESOLVED", "UNRESOLVED_ACTION_INTERSECTS_WINDOW"
                    elif (quality or {}).get("duplicates", 0) or (quality or {}).get("invalid_ohlc", 0):
                        state, reason = "QUALITY_GATE_FAILED", "DUPLICATE_OR_INVALID_OHLC"
                    else:
                        state, reason = "ELIGIBLE", "ALL_STAGE_B_PATH_GATES_PASS"
                records.append({"representation_id": rep, "research_family": rep_family[rep],
                                "scenario_id": scenario, "window_id": window_id,
                                "cell_missingness_state": state, "reason": reason,
                                "effective_start": start, "effective_end": end,
                                "source_provider": source.get("selected_provider"),
                                "source_data_sha256": source.get("selected_transformed_sha256")})
    if len(records) != 777:
        raise IntegrityError(f"eligibility inventory {len(records)} != 777")
    identities = [(row["representation_id"], row["scenario_id"], row["window_id"]) for row in records]
    if len(set(identities)) != 777:
        raise IntegrityError("eligibility inventory duplicate identity")
    return {"schema_version": "1.0", "study_id": "RISK-0001", "registered_cell_count": 777,
            "records": records, "state_counts": {state: sum(row["cell_missingness_state"] == state for row in records) for state in MISSINGNESS}}


def trial_registry(prereg: Mapping[str, Any], config_hash: str, eligibility: Mapping[str, Any], data_bundle_hashes: Mapping[str, str]) -> dict[str, Any]:
    records = []
    for row in eligibility["records"]:
        rep = row["representation_id"]
        data_hash = data_bundle_hashes[rep]
        identity = f"RISK-0001|{rep}|{row['scenario_id']}|{row['window_id']}|config:{config_hash}|data:{data_hash}"
        records.append({"cell_id": identity, "representation_id": rep, "research_family": row["research_family"],
                        "scenario_id": row["scenario_id"], "window_id": row["window_id"],
                        "config_sha256": config_hash, "data_bundle_sha256": data_hash,
                        "preexecution_missingness_state": row["cell_missingness_state"]})
    if len(records) != 777 or len({row["cell_id"] for row in records}) != 777:
        raise IntegrityError("trial registry must contain 777 unique immutable cells")
    return {"schema_version": "1.0", "study_id": "RISK-0001", "cell_id_grammar": "RISK-0001|REPRESENTATION|SCENARIO|WINDOW|config:SHA256|data:SHA256",
            "registered_cell_count": 777, "reserve_trials": 0, "unused_capacity_reuse": "PROHIBITED", "records": records}


def eligibility_lookup(eligibility: Mapping[str, Any]) -> dict[tuple[str, str, str], Mapping[str, Any]]:
    return {(row["representation_id"], row["scenario_id"], row["window_id"]): row for row in eligibility["records"]}


def decimal_text(value: float | Decimal) -> str:
    decimal = value if isinstance(value, Decimal) else Decimal(str(value))
    return format(decimal, "f")


def scenario_report_values(prereg: Mapping[str, Any], family: str, scenario: str, metric: str, operands: Mapping[str, Any]) -> tuple[str, str]:
    exposure = Decimal(prereg["scenario_magnitudes"]["values_pct"][family][scenario])
    reference = Decimal(prereg["scenario_magnitudes"]["values_pct"][family]["HISTORICAL_REFERENCE"])
    if metric == "EXPOSURE_SCALED_DRAWDOWN_LOSS":
        raw = abs(Decimal(operands["drawdown"]))
    elif metric == "EXPOSURE_SCALED_STRESS_LOSS":
        raw = max(Decimal("0"), -Decimal(operands["stress_return"]))
    elif metric == "EXPOSURE_SCALED_UNDERWATER_BURDEN":
        raw = Decimal(operands["underwater_area_days"])
    elif metric == "EXPOSURE_SCALED_EXCESS_CONTRIBUTION":
        raw = Decimal(operands["asset_total_return"]) - Decimal(operands["comparator_total_return"])
    else:
        raise IntegrityError(f"unknown formula metric {metric}")
    return decimal_text(exposure * raw), decimal_text(reference * raw)
