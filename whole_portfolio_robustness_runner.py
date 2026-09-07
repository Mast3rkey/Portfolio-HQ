"""Frozen, network-free execution engine for PORTFOLIO-ROBUSTNESS-0001.

The runner has two irreversible phases. ``validate`` may use only registered
non-holdout windows and emits a receipt binding the implementation and inputs.
``execute`` refuses to expose holdout results unless that exact receipt still
matches. Results are advisory research; this module has no account, brokerage,
margin, order, or Stage-1 dependency.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
import math
import os
import random
import statistics
import subprocess
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import date, timedelta
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import yaml

import risk_level1_core as risk_core
import whole_portfolio_robustness_engine as gate


ROOT = Path(__file__).resolve().parent
STUDY = ROOT / "research/whole_portfolio_robustness"
CONFIG_PATH = STUDY / "implementation_config.yaml"
LOOKTHROUGH_PATH = ROOT / "issuer_lookthrough.yaml"
RUNNER_PATH = ROOT / "whole_portfolio_robustness_runner.py"
RESULT_VALIDATOR_PATH = ROOT / "whole_portfolio_robustness_result_validator.py"
DEFAULT_OUTPUT = STUDY / "execution"

QUARTERLY = "QUARTERLY"
ANNUAL = "ANNUAL"
class ExecutionError(RuntimeError):
    """Raised when an integrity or simulation invariant fails closed."""


def _read_yaml(path: Path) -> dict[str, Any]:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if type(value) is not dict:
        raise ExecutionError(f"{path}: YAML mapping required")
    return value


def _reject_json_constant(token: str) -> None:
    raise ExecutionError(f"nonfinite JSON token {token}")


def _read_json(path: Path) -> dict[str, Any]:
    value = json.loads(
        path.read_text(encoding="utf-8"),
        parse_constant=_reject_json_constant,
    )
    if type(value) is not dict:
        raise ExecutionError(f"{path}: JSON mapping required")
    return value


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _canonical_bytes(value: Any) -> bytes:
    return (json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=True,
        allow_nan=False,
    ) + "\n").encode()


def _canonical_hash(value: Any) -> str:
    return hashlib.sha256(_canonical_bytes(value)).hexdigest()


def _write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(_canonical_bytes(value))


def _git_commit() -> str:
    override = os.environ.get("PORTFOLIO_ROBUSTNESS_CODE_COMMIT")
    if override:
        if len(override) != 40 or any(ch not in "0123456789abcdef" for ch in override):
            raise ExecutionError("PORTFOLIO_ROBUSTNESS_CODE_COMMIT must be a lowercase 40-character SHA")
        return override
    try:
        return subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, check=True,
            capture_output=True, text=True,
        ).stdout.strip()
    except (OSError, subprocess.CalledProcessError) as exc:
        raise ExecutionError("unable to bind execution to a git commit") from exc


def load_config() -> dict[str, Any]:
    config = _read_yaml(CONFIG_PATH)
    required = {
        "schema_version": "1.0",
        "study_id": "PORTFOLIO-ROBUSTNESS-0001",
        "status": "FROZEN_BEFORE_HOLDOUT_EXECUTION",
    }
    for key, expected in required.items():
        if config.get(key) != expected:
            raise ExecutionError(f"implementation config {key} must equal {expected}")
    decision = config.get("decision_cell", {})
    if decision != {
        "cadence": "QUARTERLY", "one_way_cost_bps": "10",
        "tax_profile": "TAXABLE_MID",
        "rationale": decision.get("rationale"),
    }:
        raise ExecutionError("implementation config decision cell drift")
    if config.get("output", {}).get("advisory_only") is not True:
        raise ExecutionError("implementation must remain advisory-only")
    if config.get("output", {}).get("stage1") != "UNARMED_AND_NOT_EXECUTABLE":
        raise ExecutionError("Stage 1 boundary drift")
    return config


def _bundle_hashes() -> dict[str, str]:
    paths = [gate.PREREG_PATH, CONFIG_PATH, gate.TARGETS_PATH, gate.GATES_PATH,
             LOOKTHROUGH_PATH, gate.SOURCE_INVENTORY_PATH, gate.XNYS_PATH,
             gate.DFF_PATH, gate.ACTION_PATH, Path(gate.__file__),
             Path(gate.prereg_validator.__file__), Path(risk_core.__file__),
             ROOT / "requirements.txt", RUNNER_PATH]
    if RESULT_VALIDATOR_PATH.is_file():
        paths.append(RESULT_VALIDATOR_PATH)
    return {str(path.relative_to(ROOT)): _sha256(path) for path in paths}


def input_freeze() -> dict[str, Any]:
    ready = gate.require_ready()
    freeze = dict(ready)
    freeze.update({
        "implementation_config_sha256": _sha256(CONFIG_PATH),
        "issuer_lookthrough_sha256": _sha256(LOOKTHROUGH_PATH),
        "implementation_bundle_hashes": _bundle_hashes(),
        "code_commit": _git_commit(),
        "runtime": {
            "python": sys.version.split()[0],
            "packages": {name: importlib.metadata.version(name) for name in (
                "exchange-calendars", "pandas", "PyYAML",
            )},
        },
        "result_seed": 20260907,
        "holdout_results_emitted": False,
    })
    return freeze


@dataclass
class Lot:
    quantity: float
    basis: float
    acquired: str
    order: int


@dataclass
class SimulationResult:
    variant: str
    window: str
    cadence: str
    cost_bps: str
    tax_profile: str
    dates: list[str]
    values: list[float]
    returns: list[float]
    risk_free_returns: list[float]
    concentrations: list[dict[str, float]]
    transaction_cost: float
    tax_paid: float
    dividend_tax_paid: float
    realized_gain_tax_paid: float
    taxable_realized_gain: float
    one_way_notional: float
    rebalance_count: int
    final_cash: float
    facts: dict[str, Any] = field(default_factory=dict)


@dataclass
class MarketData:
    sessions: list[str]
    prices: dict[str, dict[str, float]]
    dividends: dict[str, dict[str, float]]
    cash_factor: dict[tuple[str, str], float]
    risk_free_factor: dict[tuple[str, str], float]
    first_available: dict[str, str]
    lookthrough: dict[str, list[tuple[str, float]]]
    caps: dict[str, Any]


def _adjusted_dividends(document: Mapping[str, Any]) -> dict[str, float]:
    dividends: dict[str, float] = defaultdict(float)
    splits: list[tuple[str, float]] = []
    for event in document.get("events", []):
        kind = event.get("action_type")
        day = str(event.get("ex_date", ""))[:10]
        if not day:
            continue
        if kind in ("cash_dividend", "cash_dividends"):
            rate = event.get("rate")
            if rate is None or not math.isfinite(float(rate)) or float(rate) < 0:
                raise ExecutionError("invalid dividend event")
            dividends[day] += float(rate)
        elif kind in ("split", "splits"):
            new_rate, old_rate = event.get("new_rate"), event.get("old_rate")
            if new_rate and old_rate:
                splits.append((day, float(new_rate) / float(old_rate)))
    if document.get("provider") == "ALPACA_MARKET_DATA":
        for day in list(dividends):
            future = math.prod(factor for split_day, factor in splits if split_day > day)
            if future:
                dividends[day] /= future
    return dict(dividends)


def _lawful_rate_factors(sessions: Sequence[str], dff: Mapping[str, Any], drag_bps: float) -> tuple[dict[tuple[str, str], float], dict[tuple[str, str], float]]:
    lookback = (date.fromisoformat(sessions[0]) - timedelta(days=10)).isoformat()
    horizon = (date.fromisoformat(sessions[-1]) + timedelta(days=7)).isoformat()
    rates = {str(row["date"]): float(row["rate_pct"]) for row in dff["rows"]
             if lookback <= str(row["date"]) <= horizon}
    business = risk_core.federal_business_days(lookback, horizon)
    required = [day for day in business if day <= sessions[-1]]
    missing = [day for day in required if day not in rates]
    if missing:
        raise ExecutionError(
            f"DFF missing {len(missing)} required federal-business-day observations"
        )
    # Observation t becomes lawful only after the close of the next federal
    # business day.  The strict comparison in the accrual loop makes it usable
    # on the following calendar day, matching the preregistered lag.
    lawful = [(business[index + 1], rates[observation])
              for index, observation in enumerate(business[:-1])
              if observation in rates]
    cash: dict[tuple[str, str], float] = {}
    rf: dict[tuple[str, str], float] = {}
    pointer = 0
    current: float | None = None
    prior_session = sessions[0]
    for session in sessions:
        if session == sessions[0]:
            cash[(session, session)] = 1.0
            rf[(session, session)] = 1.0
            continue
        cash_factor = 1.0
        rf_factor = 1.0
        cursor_day = date.fromisoformat(prior_session) + timedelta(days=1)
        end_day = date.fromisoformat(session)
        while cursor_day <= end_day:
            day = cursor_day.isoformat()
            while pointer < len(lawful) and lawful[pointer][0] < day:
                current = lawful[pointer][1]
                pointer += 1
            if current is None:
                raise ExecutionError(f"DFF unavailable lawfully for {day}")
            rf_factor *= 1.0 + current / 100.0 / 360.0
            cash_factor *= 1.0 + (current - drag_bps / 100.0) / 100.0 / 360.0
            cursor_day += timedelta(days=1)
        cash[(prior_session, session)] = cash_factor
        rf[(prior_session, session)] = rf_factor
        prior_session = session
    return cash, rf


def load_market_data(freeze: Mapping[str, Any], config: Mapping[str, Any],
                     *, max_date: str | None = None) -> MarketData:
    sessions_doc = _read_json(gate.XNYS_PATH)
    end = min("2026-07-31", max_date) if max_date else "2026-07-31"
    sessions = [str(row["session"]) for row in sessions_doc["sessions"]
                if "2016-01-04" <= str(row["session"]) <= end]
    if not sessions or sessions != sorted(set(sessions)):
        raise ExecutionError("invalid XNYS session sequence")
    prices: dict[str, dict[str, float]] = {}
    dividends: dict[str, dict[str, float]] = {}
    first: dict[str, str] = {}
    targets = _read_yaml(gate.TARGETS_PATH)
    gates_doc = _read_yaml(gate.GATES_PATH)
    gated = {str(row["ticker"]) for row in gates_doc["gates"]}
    crypto_tickers = {
        str(row["ticker"]) for row in targets["destination"]
        if row["asset_class"] == "crypto"
    }
    direct_tickers = {
        str(row["ticker"]) for row in targets["destination"]
        if row["asset_class"] == "equity" and row["ticker"] not in gated
    }
    session_set = set(sessions)
    for ticker, metadata in freeze["datasets"].items():
        path = ROOT / metadata["path"]
        if _sha256(path) != metadata["sha256"]:
            raise ExecutionError(f"{ticker}: market data drift after gate")
        document = _read_json(path)
        raw = {str(row["date"]): float(row["close"]) for row in document["rows"]}
        if ticker in crypto_tickers:
            aligned: dict[str, float] = {}
            for session in sessions:
                source_day = (date.fromisoformat(session) - timedelta(days=1)).isoformat()
                if source_day in raw:
                    aligned[session] = raw[source_day]
            prices[ticker] = aligned
            dividends[ticker] = {}
        else:
            prices[ticker] = {day: value for day, value in raw.items() if day in session_set}
            dividends[ticker] = _adjusted_dividends(document)
        if not prices[ticker] and min(raw) <= end:
            raise ExecutionError(f"{ticker}: no aligned prices despite lawful inception")
        # A current-roster security whose inception follows a truncated
        # non-holdout validation horizon is intentionally all cash there.
        first[ticker] = min(prices[ticker]) if prices[ticker] else min(raw)
    dff = _read_json(gate.DFF_PATH)
    cash_factor, risk_free_factor = _lawful_rate_factors(
        sessions, dff, float(config["simulation"]["cash_operating_drag_bps_annual"]),
    )
    look = _read_yaml(LOOKTHROUGH_PATH)
    lookthrough = {
        str(row["ticker"]): [
            (str(item["fund"]), float(item["fund_holding_weight"]))
            for item in row.get("funds", [])
        ] for row in look["issuers"]
    }
    return MarketData(
        sessions=sessions, prices=prices, dividends=dividends,
        cash_factor=cash_factor, risk_free_factor=risk_free_factor,
        first_available=first, lookthrough=lookthrough,
        caps={
            "issuer": float(look["issuer_ceiling_pct"]) / 100.0,
            "ai": float(look["common_driver_ceiling_pct"]) / 100.0,
            "ai_tickers": frozenset(lookthrough),
            "direct_tickers": frozenset(direct_tickers),
            "clusters": {row["name"]: {
                "cap": float(row["pct"]) / 100.0,
                "tickers": frozenset(row["tickers"]),
            } for row in targets["caps"]["clusters"]},
        },
    )


def _scheduled_sessions(sessions: Sequence[str], cadence: str, config: Mapping[str, Any]) -> set[str]:
    months = set(config["simulation"]["quarterly_months" if cadence == QUARTERLY else "annual_months"])
    result: set[str] = set()
    seen: set[tuple[int, int]] = set()
    for day in sessions:
        parsed = date.fromisoformat(day)
        key = (parsed.year, parsed.month)
        if parsed.month in months and key not in seen:
            result.add(day)
            seen.add(key)
    return result


def _tax_profile(prereg: Mapping[str, Any], profile_id: str) -> Mapping[str, Any]:
    matches = [row for row in prereg["frictions"]["tax_profiles"] if row["id"] == profile_id]
    if len(matches) != 1:
        raise ExecutionError(f"unknown tax profile {profile_id}")
    return matches[0]


def _estimate_sale_tax(lots: Sequence[Lot], quantity: float, price: float, day: str,
                       ticker: str, tax: Mapping[str, Any], config: Mapping[str, Any]) -> tuple[float, float]:
    remaining = quantity
    taxable_gain = 0.0
    tax_due = 0.0
    ordered = sorted(lots, key=lambda lot: (-lot.basis, lot.acquired, lot.order))
    for lot in ordered:
        used = min(lot.quantity, remaining)
        gain = max(0.0, (price - lot.basis) * used)
        if ticker == config["tax"]["gold_instrument"]:
            rate = float(tax["gold_gain_rate"])
        else:
            held = (date.fromisoformat(day) - date.fromisoformat(lot.acquired)).days
            rate = float(tax["long_gain_rate"] if held >= int(config["tax"]["long_term_holding_days_minimum"])
                         else tax["short_gain_rate"])
        taxable_gain += gain
        tax_due += gain * rate
        remaining -= used
        if remaining <= 1e-10:
            break
    if remaining > 1e-7:
        raise ExecutionError("sale exceeds available lots")
    return tax_due, taxable_gain


def _consume_hifo(lots: list[Lot], quantity: float) -> None:
    remaining = quantity
    for lot in sorted(lots, key=lambda item: (-item.basis, item.acquired, item.order)):
        used = min(lot.quantity, remaining)
        lot.quantity -= used
        remaining -= used
        if remaining <= 1e-10:
            break
    lots[:] = [lot for lot in lots if lot.quantity > 1e-10]
    if remaining > 1e-7:
        raise ExecutionError("HIFO consumption exceeded available lots")


def _concentration(shares: Mapping[str, float], prices: Mapping[str, float], cash: float,
                   market: MarketData) -> dict[str, float]:
    values = {ticker: quantity * prices[ticker] for ticker, quantity in shares.items()}
    nav = cash + sum(values.values())
    if nav <= 0:
        raise ExecutionError("nonpositive portfolio NAV")
    weights = {ticker: value / nav for ticker, value in values.items()}
    direct = {ticker: weights.get(ticker, 0.0) for ticker in market.caps["direct_tickers"]}
    effective: dict[str, float] = dict(direct)
    for issuer, funds in market.lookthrough.items():
        effective[issuer] = effective.get(issuer, 0.0) + sum(weights.get(fund, 0.0) * weight for fund, weight in funds)
    ai = sum(effective.get(ticker, 0.0) for ticker in market.caps["ai_tickers"])
    semis = sum(weights.get(ticker, 0.0) for ticker in market.caps["clusters"].get("semis", {}).get("tickers", ()))
    power = sum(weights.get(ticker, 0.0) for ticker in market.caps["clusters"].get("power_infra", {}).get("tickers", ()))
    return {
        "DIRECT_HHI": sum(value * value for value in direct.values()),
        "MAX_DIRECT_NAME": max(direct.values(), default=0.0),
        "EFFECTIVE_ISSUER_MAX": max(effective.values(), default=0.0),
        "AI_PLATFORM_COMMON_DRIVER": ai,
        "SEMIS_CLUSTER": semis,
        "POWER_INFRA_CLUSTER": power,
    }


def _rebalance(day: str, target_weights: Mapping[str, float], current_prices: Mapping[str, float],
               shares: dict[str, float], lots: dict[str, list[Lot]], cash: float,
               cost_rate: float, tax: Mapping[str, Any], config: Mapping[str, Any],
               order_counter: int) -> tuple[float, float, float, float, int, float]:
    pre_nav = cash + sum(shares.get(ticker, 0.0) * price for ticker, price in current_prices.items())
    eligible = {ticker for ticker in target_weights if ticker != "CASH" and ticker in current_prices}
    guess = pre_nav
    tolerance = float(config["simulation"]["fixed_point_tolerance_dollars"])
    max_iterations = int(config["simulation"]["fixed_point_max_iterations"])
    estimate_tax = estimate_gain = trade = 0.0
    for _ in range(max_iterations):
        targets = {ticker: guess * target_weights[ticker] for ticker in eligible}
        current = {ticker: shares.get(ticker, 0.0) * current_prices[ticker] for ticker in eligible}
        estimate_tax = estimate_gain = trade = 0.0
        for ticker in eligible:
            delta = targets[ticker] - current[ticker]
            trade += abs(delta)
            if delta < -tolerance:
                due, gain = _estimate_sale_tax(lots[ticker], -delta / current_prices[ticker],
                                               current_prices[ticker], day, ticker, tax, config)
                estimate_tax += due
                estimate_gain += gain
        updated = pre_nav - trade * cost_rate - estimate_tax
        if updated <= 0:
            raise ExecutionError("friction exhausted portfolio")
        if abs(updated - guess) <= tolerance:
            guess = updated
            break
        guess = updated
    else:
        raise ExecutionError("post-friction target fixed point did not converge")
    targets = {ticker: guess * target_weights[ticker] for ticker in eligible}
    total_trade = total_tax = total_gain = 0.0
    # Sales first so the cash ledger never depends on iteration order.
    for ticker in sorted(eligible):
        price = current_prices[ticker]
        current_value = shares.get(ticker, 0.0) * price
        delta = targets[ticker] - current_value
        if delta < -tolerance:
            quantity = -delta / price
            due, gain = _estimate_sale_tax(lots[ticker], quantity, price, day, ticker, tax, config)
            _consume_hifo(lots[ticker], quantity)
            shares[ticker] -= quantity
            cash += quantity * price
            total_trade += quantity * price
            total_tax += due
            total_gain += gain
    for ticker in sorted(eligible):
        price = current_prices[ticker]
        current_value = shares.get(ticker, 0.0) * price
        delta = targets[ticker] - current_value
        if delta > tolerance:
            quantity = delta / price
            cash -= delta
            shares[ticker] = shares.get(ticker, 0.0) + quantity
            lots[ticker].append(Lot(quantity, price, day, order_counter))
            order_counter += 1
            total_trade += delta
    transaction_cost = total_trade * cost_rate
    cash -= transaction_cost + total_tax
    if cash < -max(tolerance, 1e-5):
        raise ExecutionError(f"rebalance would borrow {-cash:.6f} dollars")
    cash = max(0.0, cash)
    post_nav = cash + sum(shares.get(ticker, 0.0) * current_prices[ticker] for ticker in eligible)
    if abs(post_nav - (pre_nav - transaction_cost - total_tax)) > 1e-4:
        raise ExecutionError("rebalance ledger failed to reconcile")
    return cash, transaction_cost, total_tax, total_gain, order_counter, total_trade


def simulate(variant: str, window: str, start: str, end: str, cadence: str,
             cost_bps: str, tax_profile_id: str, weights: Mapping[str, Any],
             prereg: Mapping[str, Any], config: Mapping[str, Any], market: MarketData,
             *, cash_yield: bool = True) -> SimulationResult:
    sessions = [day for day in market.sessions if start <= day <= end]
    if len(sessions) < 2:
        raise ExecutionError(f"{window}: fewer than two XNYS sessions")
    target = {ticker: float(value) / 100.0 for ticker, value in weights.items()}
    if abs(sum(target.values()) - 1.0) > 1e-10:
        raise ExecutionError("target weights do not sum to one")
    tax = _tax_profile(prereg, tax_profile_id)
    cost_rate = float(cost_bps) / 10000.0
    scheduled = _scheduled_sessions(sessions, cadence, config)
    scheduled.add(sessions[0])
    shares: dict[str, float] = defaultdict(float)
    lots: dict[str, list[Lot]] = defaultdict(list)
    cash = float(prereg["portfolio_mechanics"]["starting_value"])
    values: list[float] = []
    returns: list[float] = []
    risk_free_returns: list[float] = []
    concentrations: list[dict[str, float]] = []
    transaction_cost = tax_paid = dividend_tax = realized_tax = realized_gain = one_way = 0.0
    rebalances = 0
    order_counter = 0
    prior_value = cash
    prior_day = sessions[0]
    dividend_rate = (float(tax["qualified_dividend_fraction"]) * float(tax["qualified_dividend_rate"])
                     + (1.0 - float(tax["qualified_dividend_fraction"])) * float(tax["ordinary_income_rate"]))
    for index, day in enumerate(sessions):
        if index:
            cash *= market.cash_factor[(prior_day, day)] if cash_yield else 1.0
        current_prices: dict[str, float] = {}
        for ticker in target:
            if ticker == "CASH":
                continue
            price = market.prices[ticker].get(day)
            if price is not None:
                current_prices[ticker] = price
            elif shares.get(ticker, 0.0) > 1e-10:
                raise ExecutionError(f"{ticker}: held position lacks required price on {day}")
        for ticker, quantity in list(shares.items()):
            amount = market.dividends[ticker].get(day, 0.0) * quantity
            if amount:
                due = amount * dividend_rate
                cash += amount - due
                tax_paid += due
                dividend_tax += due
        if day in scheduled:
            cash, cost, due, gain, order_counter, traded = _rebalance(
                day, target, current_prices, shares, lots, cash, cost_rate,
                tax, config, order_counter,
            )
            transaction_cost += cost
            tax_paid += due
            realized_tax += due
            realized_gain += gain
            one_way += traded
            rebalances += 1
        nav = cash + sum(quantity * current_prices[ticker] for ticker, quantity in shares.items())
        if not math.isfinite(nav) or nav <= 0:
            raise ExecutionError(f"invalid NAV on {day}")
        values.append(nav)
        returns.append(nav / prior_value - 1.0)
        risk_free_returns.append((market.risk_free_factor[(prior_day, day)] - 1.0) if index else 0.0)
        concentrations.append(_concentration(shares, current_prices, cash, market))
        prior_value = nav
        prior_day = day
    return SimulationResult(
        variant=variant, window=window, cadence=cadence, cost_bps=str(cost_bps),
        tax_profile=tax_profile_id, dates=sessions, values=values, returns=returns,
        risk_free_returns=risk_free_returns, concentrations=concentrations,
        transaction_cost=transaction_cost, tax_paid=tax_paid,
        dividend_tax_paid=dividend_tax, realized_gain_tax_paid=realized_tax,
        taxable_realized_gain=realized_gain, one_way_notional=one_way,
        rebalance_count=rebalances, final_cash=cash,
        facts={"starting_value": float(prereg["portfolio_mechanics"]["starting_value"]),
               "ending_value": values[-1], "max_market_date_used": sessions[-1]},
    )


def _period_worst(dates: Sequence[str], returns: Sequence[float], kind: str) -> float | None:
    factors: dict[str, float] = defaultdict(lambda: 1.0)
    for day, value in zip(dates, returns):
        parsed = date.fromisoformat(day)
        if kind == "month":
            key = day[:7]
        elif kind == "quarter":
            key = f"{parsed.year}-Q{(parsed.month - 1) // 3 + 1}"
        else:
            key = str(parsed.year)
        factors[key] *= 1.0 + value
    return min((factor - 1.0 for factor in factors.values()), default=None)


def metric_record(result: SimulationResult, config: Mapping[str, Any], *,
                  cash_cost_shadow_return: float | None = None,
                  tax_deferred_return: float | None = None) -> dict[str, Any]:
    start_value = float(result.facts["starting_value"])
    cumulative = result.values[-1] / start_value - 1.0
    elapsed = (date.fromisoformat(result.dates[-1]) - date.fromisoformat(result.dates[0])).days
    cagr = (result.values[-1] / start_value) ** (float(config["metrics"]["cagr_day_basis"]) / elapsed) - 1.0
    excess = [value - rf for value, rf in zip(result.returns, result.risk_free_returns)]
    annualization = int(config["metrics"]["annualization_sessions"])
    vol = statistics.stdev(result.returns) * math.sqrt(annualization) if len(result.returns) >= 2 else None
    excess_std = statistics.stdev(excess) if len(excess) >= 2 else 0.0
    mean_excess = statistics.fmean(excess)
    downside = math.sqrt(statistics.fmean(min(0.0, value) ** 2 for value in excess)) * math.sqrt(annualization)
    sharpe = mean_excess / excess_std * math.sqrt(annualization) if excess_std > 0 else None
    sortino = mean_excess * annualization / downside if downside > 0 else None
    peak = start_value
    max_dd = 0.0
    peak_date = result.dates[0]
    trough_date = result.dates[0]
    deepest_peak_date = peak_date
    deepest_peak_value = peak
    for day, value in zip(result.dates, result.values):
        if value > peak:
            peak, peak_date = value, day
        dd = value / peak - 1.0
        if dd < max_dd:
            max_dd, trough_date, deepest_peak_date = dd, day, peak_date
            deepest_peak_value = peak
    recovery = next((day for day, value in zip(result.dates, result.values)
                     if day > trough_date and value >= deepest_peak_value), None) if max_dd < 0 else result.dates[0]
    recovery_days = ((date.fromisoformat(recovery) - date.fromisoformat(deepest_peak_date)).days
                     if recovery else None)
    ordered = sorted(result.returns)
    cutoff_index = max(1, math.ceil(len(ordered) * 0.05))
    cvar = statistics.fmean(ordered[:cutoff_index])
    concentration = {key: max(row[key] for row in result.concentrations)
                     for key in result.concentrations[0]}
    return {
        "variant": result.variant, "window": result.window, "cadence": result.cadence,
        "one_way_cost_bps": result.cost_bps, "tax_profile": result.tax_profile,
        "NET_TWR_CAGR": cagr, "CUMULATIVE_TWR": cumulative,
        "CASH_AND_COST_DRAG": (cash_cost_shadow_return - cumulative
                               if cash_cost_shadow_return is not None else None),
        "TAX_DRAG": (tax_deferred_return - cumulative if tax_deferred_return is not None else None),
        "ANNUALIZED_VOLATILITY": vol, "DOWNSIDE_DEVIATION": downside,
        "SHARPE_VS_LAGGED_DFF": sharpe, "SORTINO_VS_LAGGED_DFF": sortino,
        "CALMAR": cagr / abs(max_dd) if max_dd < 0 else None,
        "MAX_DRAWDOWN": max_dd, "RECOVERY_DAYS": recovery_days,
        "RECOVERY_CENSORED": recovery is None, "WORST_MONTH": _period_worst(result.dates, result.returns, "month"),
        "WORST_QUARTER": _period_worst(result.dates, result.returns, "quarter"),
        "WORST_YEAR": _period_worst(result.dates, result.returns, "year"),
        "DAILY_CVAR_95": cvar, **concentration,
        "ONE_WAY_TURNOVER": result.one_way_notional / start_value,
        "REBALANCE_COUNT": result.rebalance_count,
        "TAXABLE_REALIZED_GAIN": result.taxable_realized_gain,
        "TRANSACTION_COST_DOLLARS": result.transaction_cost,
        "TAX_PAID_DOLLARS": result.tax_paid,
        "DIVIDEND_TAX_DOLLARS": result.dividend_tax_paid,
        "REALIZED_GAIN_TAX_DOLLARS": result.realized_gain_tax_paid,
        "ENDING_VALUE": result.values[-1], "FINAL_CASH": result.final_cash,
        "FACTS_ONLY": True,
    }


def registered_windows(prereg: Mapping[str, Any]) -> list[tuple[str, str, str]]:
    windows: list[tuple[str, str, str]] = []
    for name in ("development_context", "confirmation", "holdout_all_current_assets", "full_context"):
        row = prereg["windows"][name]
        windows.append((name, str(row["start"]), str(row["end"])))
    walk = prereg["windows"]["walk_forward"]
    for year in range(int(walk["first_evaluation_year"]), int(walk["last_evaluation_year"]) + 1):
        windows.append((f"WALK_FORWARD_{year}", f"{year}-01-01", f"{year}-12-31"))
    for row in prereg["windows"]["fixed_regimes"]:
        windows.append((str(row["id"]), str(row["start"]), str(row["end"])))
    if len({name for name, _, _ in windows}) != len(windows):
        raise ExecutionError("registered window identities are not unique")
    return windows


def _cell_id(variant: str, window: str, cadence: str, cost: str, tax: str) -> str:
    return "|".join((variant, window, cadence, str(cost), tax))


def run_non_holdout_validation(output_dir: Path) -> dict[str, Any]:
    config = load_config()
    freeze = input_freeze()
    prereg = _read_yaml(gate.PREREG_PATH)
    targets = _read_yaml(gate.TARGETS_PATH)
    gates = _read_yaml(gate.GATES_PATH)
    weights = gate.derive_instrument_weights(targets, gates, prereg)
    cutoff = str(prereg["windows"]["confirmation"]["end"])
    market = load_market_data(freeze, config, max_date=cutoff)
    decision = config["decision_cell"]
    validation_windows = [
        (name, start, end) for name, start, end in registered_windows(prereg)
        if end <= cutoff
    ]
    def evaluate() -> list[dict[str, Any]]:
        evaluated: list[dict[str, Any]] = []
        for name, start, end in validation_windows:
            for variant, variant_weights in weights.items():
                result = simulate(variant, name, start, end, decision["cadence"],
                                  decision["one_way_cost_bps"], decision["tax_profile"],
                                  variant_weights, prereg, config, market)
                evaluated.append({
                    "cell": _cell_id(variant, name, decision["cadence"],
                                     decision["one_way_cost_bps"], decision["tax_profile"]),
                    "ending_value": round(result.values[-1], 10),
                    "rebalance_count": result.rebalance_count,
                    "max_market_date_used": result.facts["max_market_date_used"],
                })
        return evaluated

    cases = evaluate()
    replay = evaluate()
    if _canonical_hash(cases) != _canonical_hash(replay):
        raise ExecutionError("non-deterministic non-holdout simulation")
    if any(case["max_market_date_used"] > cutoff for case in cases):
        raise ExecutionError("non-holdout validation accessed a future market date")
    receipt = {
        "schema_version": "1.0", "study_id": prereg["study_id"],
        "phase": "NON_HOLDOUT_VALIDATION", "status": "PASS",
        "input_freeze_sha256": _canonical_hash(freeze), "input_freeze": freeze,
        "validation_cutoff": cutoff, "max_market_date_used": max(case["max_market_date_used"] for case in cases),
        "validation_case_count": len(cases), "validation_summary_sha256": _canonical_hash(cases),
        "validation_cases": cases,
        "determinism_replay_sha256": _canonical_hash(replay),
        "holdout_results_emitted": False,
        "advisory_only": True, "stage1": "UNARMED_AND_NOT_EXECUTABLE",
    }
    _write_json(output_dir / "validation_receipt.json", receipt)
    return receipt


def verify_validation_receipt(path: Path) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    receipt = _read_json(path)
    if (receipt.get("schema_version") != "1.0"
            or receipt.get("study_id") != "PORTFOLIO-ROBUSTNESS-0001"
            or receipt.get("phase") != "NON_HOLDOUT_VALIDATION"
            or receipt.get("status") != "PASS"):
        raise ExecutionError("valid non-holdout PASS receipt required")
    if receipt.get("holdout_results_emitted") is not False:
        raise ExecutionError("validation receipt improperly exposed holdout results")
    current = input_freeze()
    if receipt.get("input_freeze_sha256") != _canonical_hash(current) or receipt.get("input_freeze") != current:
        raise ExecutionError("implementation or input changed after non-holdout validation")
    prereg = _read_yaml(gate.PREREG_PATH)
    config = load_config()
    if receipt.get("validation_cutoff") != prereg["windows"]["confirmation"]["end"]:
        raise ExecutionError("validation cutoff drift")
    if receipt.get("advisory_only") is not True or receipt.get("stage1") != "UNARMED_AND_NOT_EXECUTABLE":
        raise ExecutionError("validation receipt safety boundary drift")
    cutoff = str(receipt["validation_cutoff"])
    cases = receipt.get("validation_cases")
    if not isinstance(cases, list):
        raise ExecutionError("validation receipt cases missing")
    weights = gate.derive_instrument_weights(
        _read_yaml(gate.TARGETS_PATH), _read_yaml(gate.GATES_PATH), prereg
    )
    decision = config["decision_cell"]
    expected = {
        _cell_id(variant, window, decision["cadence"],
                 decision["one_way_cost_bps"], decision["tax_profile"])
        for window, _start, end in registered_windows(prereg) if end <= cutoff
        for variant in weights
    }
    found = {str(row.get("cell")) for row in cases if isinstance(row, Mapping)}
    if (found != expected or len(cases) != len(expected)
            or receipt.get("validation_case_count") != len(expected)):
        raise ExecutionError("validation receipt case registry mismatch")
    if (receipt.get("validation_summary_sha256") != _canonical_hash(cases)
            or receipt.get("determinism_replay_sha256") != _canonical_hash(cases)):
        raise ExecutionError("validation receipt determinism evidence mismatch")
    if any(
        not math.isfinite(float(row.get("ending_value", math.nan)))
        or not isinstance(row.get("rebalance_count"), int)
        or str(row.get("max_market_date_used", "")) > cutoff
        for row in cases
    ):
        raise ExecutionError("validation receipt contains invalid or future evidence")
    if receipt.get("max_market_date_used") != max(str(row["max_market_date_used"]) for row in cases):
        raise ExecutionError("validation receipt maximum market date mismatch")
    return receipt, prereg, config


def _path_record(result: SimulationResult) -> dict[str, Any]:
    return {
        "cell_id": _cell_id(result.variant, result.window, result.cadence,
                            result.cost_bps, result.tax_profile),
        "variant": result.variant, "window": result.window,
        "cadence": result.cadence, "one_way_cost_bps": result.cost_bps,
        "tax_profile": result.tax_profile,
        "dates": result.dates,
        "index": [value / float(result.facts["starting_value"]) for value in result.values],
        "daily_net_returns": result.returns,
        "daily_lagged_dff_returns": result.risk_free_returns,
    }


def _bootstrap_once(base: SimulationResult, variant: SimulationResult, rng: random.Random,
                    probability: float) -> tuple[float, float, float, float]:
    n = len(base.returns)
    if variant.dates != base.dates or len(variant.returns) != n:
        raise ExecutionError("paired bootstrap paths do not align")
    indices: list[int] = []
    cursor = rng.randrange(n)
    for _ in range(n):
        if indices and rng.random() < probability:
            cursor = rng.randrange(n)
        indices.append(cursor)
        cursor = (cursor + 1) % n
    b = [base.returns[i] for i in indices]
    v = [variant.returns[i] for i in indices]
    rf = [base.risk_free_returns[i] for i in indices]
    def cagr(values: Sequence[float]) -> float:
        return math.prod(1.0 + value for value in values) ** (252.0 / len(values)) - 1.0
    def sharpe(values: Sequence[float]) -> float:
        excess = [value - rate for value, rate in zip(values, rf)]
        sd = statistics.stdev(excess)
        return statistics.fmean(excess) / sd * math.sqrt(252.0) if sd else 0.0
    def drawdown(values: Sequence[float]) -> float:
        level = peak = 1.0
        worst = 0.0
        for value in values:
            level *= 1.0 + value
            peak = max(peak, level)
            worst = min(worst, level / peak - 1.0)
        return worst
    def cvar(values: Sequence[float]) -> float:
        ordered = sorted(values)
        return statistics.fmean(ordered[:max(1, math.ceil(len(ordered) * 0.05))])
    return cagr(v) - cagr(b), sharpe(v) - sharpe(b), drawdown(v) - drawdown(b), cvar(v) - cvar(b)


def bootstrap_records(paths: Mapping[str, SimulationResult], prereg: Mapping[str, Any],
                      config: Mapping[str, Any]) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    resamples = int(prereg["bootstrap"]["resamples"])
    probability = float(config["bootstrap"]["geometric_restart_probability"])
    seed = int(prereg["bootstrap"]["seed"])
    for window in prereg["bootstrap"]["windows"]:
        base = paths[f"BASELINE|{window}"]
        for variant in sorted(name for name in {result.variant for result in paths.values()} if name != "BASELINE"):
            candidate = paths[f"{variant}|{window}"]
            local_seed = seed + int(hashlib.sha256(f"{window}|{variant}".encode()).hexdigest()[:8], 16)
            rng = random.Random(local_seed)
            draws = [_bootstrap_once(base, candidate, rng, probability) for _ in range(resamples)]
            names = ["NET_TWR_CAGR_DELTA", "SHARPE_DELTA", "MAX_DRAWDOWN_DELTA", "DAILY_CVAR_95_DELTA"]
            record: dict[str, Any] = {
                "window": window, "variant": variant, "resamples": resamples,
                "seed": local_seed, "mean_block_sessions": prereg["bootstrap"]["mean_block_sessions"],
            }
            for index, name in enumerate(names):
                values = sorted(row[index] for row in draws)
                record[name] = {
                    "mean": statistics.fmean(values),
                    "p05": values[int(0.05 * (len(values) - 1))],
                    "p50": values[int(0.50 * (len(values) - 1))],
                    "p95": values[int(0.95 * (len(values) - 1))],
                    "probability_positive": sum(value > 0 for value in values) / len(values),
                }
            output.append(record)
    return output


def _metric_lookup(records: Iterable[Mapping[str, Any]]) -> dict[str, Mapping[str, Any]]:
    return {_cell_id(str(row["variant"]), str(row["window"]), str(row["cadence"]),
                     str(row["one_way_cost_bps"]), str(row["tax_profile"])): row for row in records}


def build_sensitivity(records: Sequence[Mapping[str, Any]], prereg: Mapping[str, Any],
                      config: Mapping[str, Any]) -> dict[str, Any]:
    lookup = _metric_lookup(records)
    decision = config["decision_cell"]
    variants = sorted(
        name for name in gate.derive_instrument_weights(
            _read_yaml(gate.TARGETS_PATH), _read_yaml(gate.GATES_PATH), prereg
        ) if name != "BASELINE"
    )
    rows: list[dict[str, Any]] = []
    for window in sorted({str(row["window"]) for row in records}):
        for cadence in (QUARTERLY, ANNUAL):
            for cost in prereg["frictions"]["one_way_cost_bps"]:
                for tax in (row["id"] for row in prereg["frictions"]["tax_profiles"]):
                    base = lookup[_cell_id("BASELINE", window, cadence, str(cost), tax)]
                    for variant in variants:
                        candidate = lookup[_cell_id(variant, window, cadence, str(cost), tax)]
                        deltas = {
                            "NET_TWR_CAGR_DELTA": candidate["NET_TWR_CAGR"] - base["NET_TWR_CAGR"],
                            "SHARPE_DELTA": candidate["SHARPE_VS_LAGGED_DFF"] - base["SHARPE_VS_LAGGED_DFF"],
                            "SORTINO_DELTA": candidate["SORTINO_VS_LAGGED_DFF"] - base["SORTINO_VS_LAGGED_DFF"],
                            "MAX_DRAWDOWN_DELTA": candidate["MAX_DRAWDOWN"] - base["MAX_DRAWDOWN"],
                            "DAILY_CVAR_95_DELTA": candidate["DAILY_CVAR_95"] - base["DAILY_CVAR_95"],
                        }
                        rows.append({
                            "variant": variant, "window": window, "cadence": cadence,
                            "one_way_cost_bps": str(cost), "tax_profile": tax, **deltas,
                            "same_direction_support": (
                                deltas["SHARPE_DELTA"] > 0 and deltas["SORTINO_DELTA"] > 0
                                and (deltas["MAX_DRAWDOWN_DELTA"] > 0 or deltas["DAILY_CVAR_95_DELTA"] > 0)
                            ),
                            "decision_cell": cadence == decision["cadence"] and str(cost) == decision["one_way_cost_bps"] and tax == decision["tax_profile"],
                        })
    return {
        "schema_version": "1.0", "study_id": prereg["study_id"],
        "facts_inference_separation": "FACTS_ONLY", "rows": rows,
    }


def _concentration_pass(metric: Mapping[str, Any], market: MarketData) -> tuple[bool, dict[str, bool]]:
    tests = {
        "EFFECTIVE_ISSUER_MAX": metric["EFFECTIVE_ISSUER_MAX"] <= market.caps["issuer"] + 1e-12,
        "AI_PLATFORM_COMMON_DRIVER": metric["AI_PLATFORM_COMMON_DRIVER"] <= market.caps["ai"] + 1e-12,
        "SEMIS_CLUSTER": metric["SEMIS_CLUSTER"] <= market.caps["clusters"]["semis"]["cap"] + 1e-12,
        "POWER_INFRA_CLUSTER": metric["POWER_INFRA_CLUSTER"] <= market.caps["clusters"]["power_infra"]["cap"] + 1e-12,
    }
    return all(tests.values()), tests


def decide(records: Sequence[Mapping[str, Any]], sensitivity: Mapping[str, Any],
           bootstraps: Sequence[Mapping[str, Any]], prereg: Mapping[str, Any],
           config: Mapping[str, Any], market: MarketData) -> dict[str, Any]:
    lookup = _metric_lookup(records)
    decision = config["decision_cell"]
    threshold = prereg["review_thresholds"]["required_for_recommend_policy_review"]
    def cell(variant: str, window: str) -> Mapping[str, Any]:
        return lookup[_cell_id(variant, window, decision["cadence"],
                               decision["one_way_cost_bps"], decision["tax_profile"])]
    variants = sorted({row["variant"] for row in records} - {"BASELINE"})
    candidate_results: list[dict[str, Any]] = []
    for variant in variants:
        base_h, var_h = cell("BASELINE", "holdout_all_current_assets"), cell(variant, "holdout_all_current_assets")
        base_c, var_c = cell("BASELINE", "confirmation"), cell(variant, "confirmation")
        delta = {
            "NET_TWR_CAGR_DELTA": var_h["NET_TWR_CAGR"] - base_h["NET_TWR_CAGR"],
            "SHARPE_DELTA": var_h["SHARPE_VS_LAGGED_DFF"] - base_h["SHARPE_VS_LAGGED_DFF"],
            "SORTINO_DELTA": var_h["SORTINO_VS_LAGGED_DFF"] - base_h["SORTINO_VS_LAGGED_DFF"],
            "MAX_DRAWDOWN_DELTA": var_h["MAX_DRAWDOWN"] - base_h["MAX_DRAWDOWN"],
            "DAILY_CVAR_95_DELTA": var_h["DAILY_CVAR_95"] - base_h["DAILY_CVAR_95"],
        }
        eligible_tails = []
        if delta["MAX_DRAWDOWN_DELTA"] >= float(threshold["tail_improvement_either"]["max_drawdown_min_improvement_pp"]) / 100.0:
            eligible_tails.append("MAX_DRAWDOWN_DELTA")
        if delta["DAILY_CVAR_95_DELTA"] >= float(threshold["tail_improvement_either"]["daily_cvar_95_min_improvement_pp"]) / 100.0:
            eligible_tails.append("DAILY_CVAR_95_DELTA")
        confirmation = {
            "SHARPE_DELTA": var_c["SHARPE_VS_LAGGED_DFF"] - base_c["SHARPE_VS_LAGGED_DFF"],
            "SORTINO_DELTA": var_c["SORTINO_VS_LAGGED_DFF"] - base_c["SORTINO_VS_LAGGED_DFF"],
            "MAX_DRAWDOWN_DELTA": var_c["MAX_DRAWDOWN"] - base_c["MAX_DRAWDOWN"],
            "DAILY_CVAR_95_DELTA": var_c["DAILY_CVAR_95"] - base_c["DAILY_CVAR_95"],
        }
        confirmation_pass = (confirmation["SHARPE_DELTA"] > 0 and confirmation["SORTINO_DELTA"] > 0
                             and bool(eligible_tails) and all(confirmation[name] > 0 for name in eligible_tails))
        regime_deltas = []
        for regime in ("Q4_2018", "COVID_2020", "RATE_INFLATION_2022", "CONCENTRATION_RALLY_2023_2026"):
            b, v = cell("BASELINE", regime), cell(variant, regime)
            regime_deltas.append({"regime": regime, "MAX_DRAWDOWN_DELTA": v["MAX_DRAWDOWN"] - b["MAX_DRAWDOWN"]})
        regime_pass = all(row["MAX_DRAWDOWN_DELTA"] >= -float(threshold["regime_max_drawdown_max_worsening_pp"]) / 100.0 for row in regime_deltas)
        support_rows = [row for row in sensitivity["rows"] if row["variant"] == variant and row["window"] == "holdout_all_current_assets"]
        support_fraction = sum(bool(row["same_direction_support"]) for row in support_rows) / len(support_rows)
        bootstrap = next(row for row in bootstraps if row["variant"] == variant and row["window"] == "holdout_all_current_assets")
        bootstrap_pass = (bootstrap["SHARPE_DELTA"]["probability_positive"] >= float(threshold["bootstrap_min_probability_sharpe_positive"])
                          and bool(eligible_tails)
                          and all(bootstrap[name]["probability_positive"] >= float(threshold["bootstrap_min_probability_tail_metric_positive"])
                                  for name in eligible_tails))
        concentration_pass, concentration_tests = _concentration_pass(var_h, market)
        gates = {
            "holdout_cagr_floor": delta["NET_TWR_CAGR_DELTA"] >= float(threshold["holdout_net_cagr_floor_delta_pp_per_year"]) / 100.0,
            "holdout_sharpe": delta["SHARPE_DELTA"] >= float(threshold["holdout_sharpe_min_delta"]),
            "holdout_sortino": delta["SORTINO_DELTA"] >= float(threshold["holdout_sortino_min_delta"]),
            "holdout_tail": bool(eligible_tails), "confirmation_direction": confirmation_pass,
            "regime_drawdown": regime_pass,
            "sensitivity_fraction": support_fraction >= float(threshold["friction_cadence_cells_min_fraction_same_direction"]),
            "bootstrap": bootstrap_pass, "concentration": concentration_pass,
            "data_integrity": True,
        }
        candidate_results.append({
            "variant": variant, "holdout_deltas": delta,
            "eligible_tail_metrics": eligible_tails,
            "confirmation_deltas": confirmation, "regime_deltas": regime_deltas,
            "sensitivity_support_fraction": support_fraction,
            "bootstrap_probabilities": {name: bootstrap[name]["probability_positive"]
                                        for name in ("SHARPE_DELTA", "MAX_DRAWDOWN_DELTA", "DAILY_CVAR_95_DELTA")},
            "concentration_tests": concentration_tests,
            "gates": gates, "passes_all_gates": all(gates.values()),
        })
    passing = [row["variant"] for row in candidate_results if row["passes_all_gates"]]
    disposition = "RECOMMEND_POLICY_REVIEW" if passing else "RETAIN_BASELINE"
    return {
        "schema_version": "1.0", "study_id": prereg["study_id"],
        "disposition": disposition, "passing_variants": passing,
        "candidate_results": candidate_results,
        "automatic_adoption": "PROHIBITED", "targets_changed": False,
        "advisory_only": True, "stage1": "UNARMED_AND_NOT_EXECUTABLE",
        "inference": (
            "At least one preregistered variant merits a separate policy review; no target changes here."
            if passing else
            "No preregistered alternative cleared every gate; retain the accepted baseline."
        ),
    }


def _limitations_text(prereg: Mapping[str, Any], disposition: Mapping[str, Any]) -> str:
    return f"""# Limitations — {prereg['study_id']}

- This is a current-roster historical counterfactual, not proof that the roster could have been selected prospectively.
- The ETF issuer look-through snapshot is pinned and point-in-time; it is not silently treated as current constituent data.
- Tax profiles are sensitivities, not the user's actual tax liability. Loss credits, wash-sale benefits, terminal unrealized-gain tax, and fractional-share constraints are intentionally excluded by preregistration.
- Coinbase SOL bytes are quarantined and hash-pinned; execution is reproducible from the retained workflow artifact but the bytes are not committed to the repository.
- Cash uses lagged DFF less the registered 25-bp operating drag; no brokerage-specific cash sweep is assumed.
- Bootstrap probabilities describe this frozen historical sample and do not promise future returns.
- The disposition is **{disposition['disposition']}**. It cannot change targets, gates, margin, or holdings. Stage 1 remains **UNARMED AND NOT EXECUTABLE**.
"""


def _results_text(prereg: Mapping[str, Any], disposition: Mapping[str, Any]) -> str:
    rows = disposition["candidate_results"]
    lines = [
        f"# Results — {prereg['study_id']}", "",
        "## Disposition", "", f"**{disposition['disposition']}**", "",
        disposition["inference"], "", "## Decision-cell gate summary", "",
        "| Variant | CAGR Δ | Sharpe Δ | Sortino Δ | MDD Δ | CVaR Δ | Sensitivity support | All gates |",
        "|---|---:|---:|---:|---:|---:|---:|:---:|",
    ]
    for row in rows:
        delta = row["holdout_deltas"]
        lines.append(
            f"| {row['variant']} | {delta['NET_TWR_CAGR_DELTA']:.4%} | {delta['SHARPE_DELTA']:.4f} | "
            f"{delta['SORTINO_DELTA']:.4f} | {delta['MAX_DRAWDOWN_DELTA']:.4%} | "
            f"{delta['DAILY_CVAR_95_DELTA']:.4%} | {row['sensitivity_support_fraction']:.1%} | "
            f"{'PASS' if row['passes_all_gates'] else 'FAIL'} |"
        )
    lines += [
        "", "## Boundaries", "",
        "Facts are contained in the machine-readable metrics, bootstrap, and sensitivity outputs. The disposition above is inference under the frozen thresholds. No policy is adopted automatically.",
        "", "Stage 1 remains **UNARMED AND NOT EXECUTABLE**.", "",
    ]
    return "\n".join(lines)


def execute(validation_receipt: Path, output_dir: Path) -> dict[str, Any]:
    receipt, prereg, config = verify_validation_receipt(validation_receipt)
    freeze = receipt["input_freeze"]
    targets = _read_yaml(gate.TARGETS_PATH)
    gates = _read_yaml(gate.GATES_PATH)
    weights = gate.derive_instrument_weights(targets, gates, prereg)
    market = load_market_data(freeze, config)
    metrics: list[dict[str, Any]] = []
    decision_paths: dict[str, SimulationResult] = {}
    windows = registered_windows(prereg)
    tax_profiles = [row["id"] for row in prereg["frictions"]["tax_profiles"]]
    decision = config["decision_cell"]
    for window, start, end in windows:
        for variant, variant_weights in weights.items():
            shadows: dict[tuple[str, str], float] = {}
            deferred: dict[tuple[str, str], float] = {}
            for cadence in (QUARTERLY, ANNUAL):
                for tax_profile in tax_profiles:
                    shadow = simulate(variant, window, start, end, cadence, "0", tax_profile,
                                      variant_weights, prereg, config, market, cash_yield=False)
                    shadows[(cadence, tax_profile)] = shadow.values[-1] / float(prereg["portfolio_mechanics"]["starting_value"]) - 1.0
                for cost in prereg["frictions"]["one_way_cost_bps"]:
                    deferred_result = simulate(variant, window, start, end, cadence, str(cost), "TAX_DEFERRED",
                                               variant_weights, prereg, config, market)
                    deferred[(cadence, str(cost))] = deferred_result.values[-1] / float(prereg["portfolio_mechanics"]["starting_value"]) - 1.0
                    for tax_profile in tax_profiles:
                        result = (deferred_result if tax_profile == "TAX_DEFERRED" else
                                  simulate(variant, window, start, end, cadence, str(cost), tax_profile,
                                           variant_weights, prereg, config, market))
                        metrics.append(metric_record(
                            result, config,
                            cash_cost_shadow_return=shadows[(cadence, tax_profile)],
                            tax_deferred_return=deferred[(cadence, str(cost))],
                        ))
                        if (cadence == decision["cadence"] and str(cost) == decision["one_way_cost_bps"]
                                and tax_profile == decision["tax_profile"]):
                            decision_paths[f"{variant}|{window}"] = result
    expected_cells = len(windows) * len(weights) * 2 * len(prereg["frictions"]["one_way_cost_bps"]) * len(tax_profiles)
    if len(metrics) != expected_cells or len(_metric_lookup(metrics)) != expected_cells:
        raise ExecutionError("result cell registry is incomplete or duplicated")
    bootstraps = bootstrap_records(decision_paths, prereg, config)
    sensitivity = build_sensitivity(metrics, prereg, config)
    disposition = decide(metrics, sensitivity, bootstraps, prereg, config, market)
    result_freeze = dict(freeze)
    result_freeze["holdout_results_emitted"] = True
    result_freeze["validation_receipt_sha256"] = _sha256(validation_receipt)
    paths_doc = {
        "schema_version": "1.0", "study_id": prereg["study_id"],
        "scope": config["windows"]["portfolio_paths_scope"],
        "records": [_path_record(decision_paths[key]) for key in sorted(decision_paths)],
    }
    metrics_doc = {"schema_version": "1.0", "study_id": prereg["study_id"],
                   "cell_count": len(metrics), "records": metrics,
                   "facts_inference_separation": "FACTS_ONLY"}
    bootstrap_doc = {"schema_version": "1.0", "study_id": prereg["study_id"],
                     "method": prereg["bootstrap"]["method"], "records": bootstraps,
                     "facts_inference_separation": "FACTS_ONLY"}
    _write_json(output_dir / "input_freeze.json", result_freeze)
    _write_json(output_dir / "portfolio_paths.json", paths_doc)
    _write_json(output_dir / "metrics.json", metrics_doc)
    _write_json(output_dir / "bootstrap.json", bootstrap_doc)
    _write_json(output_dir / "sensitivity_matrix.json", sensitivity)
    (output_dir / "limitations.md").write_text(_limitations_text(prereg, disposition), encoding="utf-8")
    (output_dir / "results.md").write_text(_results_text(prereg, disposition), encoding="utf-8")
    (output_dir / "disposition.yaml").write_text(yaml.safe_dump(disposition, sort_keys=False), encoding="utf-8")
    manifest = {path.name: _sha256(path) for path in sorted(output_dir.iterdir()) if path.is_file()}
    _write_json(output_dir / "output_manifest.json", {
        "schema_version": "1.0", "study_id": prereg["study_id"],
        "files": manifest, "advisory_only": True,
        "stage1": "UNARMED_AND_NOT_EXECUTABLE",
    })
    return disposition


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("phase", choices=("validate", "execute"))
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--validation-receipt", type=Path)
    args = parser.parse_args(argv)
    if args.phase == "validate":
        receipt = run_non_holdout_validation(args.output_dir)
        print(json.dumps({"status": receipt["status"], "phase": receipt["phase"]}, sort_keys=True))
        return 0
    if args.validation_receipt is None:
        raise ExecutionError("execute requires --validation-receipt")
    disposition = execute(args.validation_receipt, args.output_dir)
    print(json.dumps({"disposition": disposition["disposition"], "stage1": disposition["stage1"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
