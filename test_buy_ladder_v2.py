from pathlib import Path

import pytest

import allocate
from research.buy_ladder_backtest import ladder_v2 as engine


def test_frozen_validation_is_result_blind_and_reconstructs_inputs(tmp_path, monkeypatch):
    monkeypatch.setattr(engine, "RECEIPT", tmp_path / "receipt.json")
    monkeypatch.setattr(engine, "simulate", lambda *_args, **_kwargs: pytest.fail("validate exposed the holdout"))
    receipt = engine.validate()
    assert receipt["validation_scope"] == "INPUT_RECONSTRUCTION_AND_NON_HOLDOUT_INVARIANTS_ONLY"
    assert receipt["reconstruction"]["status"] == "EXACT_BYTE_IDENTITY_VERIFIED"
    assert receipt["holdout_results_emitted"] is False
    assert receipt["holdout_metrics"] is None
    assert receipt["disposition"] is None
    assert receipt["stage1"] == "UNARMED_AND_NOT_EXECUTABLE"


def test_execute_rejects_missing_receipt(tmp_path, monkeypatch):
    monkeypatch.setattr(engine, "RECEIPT", tmp_path / "missing.json")
    with pytest.raises(engine.StudyError, match="validation receipt missing"):
        engine.execute()


def test_indicator_uses_only_rows_through_decision_date():
    _, prices, _, _ = engine.load_inputs()
    bars = prices["SPY"]
    before = engine.indicators(bars, 300)
    changed_future = [dict(row) for row in bars]
    changed_future[301]["close"] *= 100
    assert engine.indicators(changed_future, 300) == before


def test_first_eligible_date_is_bounded_by_simulation_start():
    cfg, prices, _sessions, _actions = engine.load_inputs()
    dates = engine.first_eligible_decision_dates(prices, cfg)
    assert dates["NVDA"] == "2021-06-01"
    assert dates["CEG"] == "2022-12-01"
    assert dates["GEV"] == "2025-01-31"


@pytest.mark.parametrize("budget,bps", [(25.0, 0), (123.45, 10), (2000.0, 25)])
def test_transaction_cost_is_inside_budget(budget, bps):
    notional, cost = engine.transaction(budget, bps)
    assert notional + cost == pytest.approx(budget)
    assert cost == pytest.approx(notional * bps / 10000)


def test_monthly_flow_is_excluded_from_twr():
    account = engine.Account(cash=100.0)
    path = []
    engine._append_path_v2(path, account, "2023-01-03", {}, 0.0)
    engine._apply_flow_v2(path, account, "2023-01-03", 50.0)
    account.cash = 165.0
    engine._append_path_v2(path, account, "2023-01-04", {}, 0.0)
    assert path[-1]["return"] == pytest.approx(0.10)
    assert path[-1]["index"] == pytest.approx(1.10)


def test_ex_date_uses_prior_close_shares_and_payable_date_settles():
    account = engine.Account(cash=0.0)
    account.shares["ETN"] = 10.0
    account.prior_shares["ETN"] = 2.0
    event = {"symbol": "ETN", "anchor_gross": 1.0, "anchor_withholding": 0.25, "payable_date": "2023-01-05"}
    engine.recognize_dividend(account, event, "2023-01-03", "baseline", 0.168)
    assert account.dividend_events[0]["gross"] == pytest.approx(2.0)
    assert account.cash == 0.0
    net = account.dividend_events[0]["net"]
    engine.settle_and_accrue(account, "2023-01-03", "2023-01-05", {"2023-01-04": 1.0, "2023-01-05": 1.0})
    assert account.cash == pytest.approx(net)
    assert account.receivables == []
    assert account.settlement_events[0]["date"] == "2023-01-05"


def test_foreign_tax_credit_sensitivities_are_mechanical():
    event = {"symbol": "ETN", "anchor_gross": 1.0, "anchor_withholding": 0.25, "payable_date": "2023-01-05"}
    rows = {}
    for mode in ("baseline", "no_credit", "etn_no_exemption"):
        account = engine.Account(prior_shares={"ETN": 1.0})
        engine.recognize_dividend(account, event, "2023-01-03", mode, 0.168)
        rows[mode] = account.dividend_events[0]
    assert rows["baseline"]["foreign_tax_credit"] == pytest.approx(0.168)
    assert rows["no_credit"]["foreign_tax_credit"] == 0.0
    assert rows["etn_no_exemption"]["source_withholding"] == pytest.approx(0.25)


def test_split_anchor_and_same_day_basis_are_explicit():
    source = {"id": "d1", "ex_date": "2023-01-03", "gross_rate_usd": 4.0, "source_withholding_usd": 1.0, "same_day_split_basis": "PRE_SPLIT"}
    split = {"ex_date": "2023-01-03", "old_rate": 1.0, "new_rate": 4.0}
    anchored = engine.anchor_dividend(source, [split])
    assert anchored["anchor_gross"] == 1.0
    assert anchored["anchor_withholding"] == 0.25
    with pytest.raises(engine.StudyError, match="ambiguous same-day"):
        engine.anchor_dividend({**source, "same_day_split_basis": "UNKNOWN"}, [split])


def test_dff_uses_one_federal_business_day_publication_lag(monkeypatch):
    rows = {"rows": [{"date": "2022-12-30", "rate_pct": 4.0}, {"date": "2023-01-03", "rate_pct": 5.0}, {"date": "2023-01-04", "rate_pct": 6.0}]}
    monkeypatch.setattr(engine, "read_json", lambda _path: rows)
    monkeypatch.setattr(engine.risk_level1_core, "federal_business_days", lambda _start, _end: ["2022-12-30", "2023-01-03", "2023-01-04"])
    cash, risk_free = engine.dff_rates(["2023-01-04"], {"cash_drag_bps": 25, "cash_tax_rate": 0.24})
    assert risk_free["2023-01-04"] == pytest.approx(1 + 0.04 / 360)
    assert cash["2023-01-04"] == pytest.approx(1 + ((0.04 - 0.0025) * 0.76) / 360)


def test_price_only_nav_excludes_receivable_and_settled_dividend_cash():
    account = engine.Account(cash=100.0)
    account.receivables.append({"ticker": "SPY", "net": 5.0, "payable_date": "2023-01-05"})
    assert account.nav({}) == 105.0
    assert account.price_only_nav({}) == 100.0
    engine.settle_and_accrue(account, "2023-01-04", "2023-01-05", {"2023-01-05": 1.0})
    assert account.nav({}) == 105.0
    assert account.price_only_nav({}) == 100.0


def test_selector_protected_cash_binds_before_ladder_branches():
    shadow = engine.Account(cash=2000.0)
    comparison_accounts = [engine.Account(cash=2000.0) for _ in range(9)]
    targets = {ticker: (1.0 if ticker == "NVDA" else 0.0) for ticker in engine.EXPECTED}
    order = {ticker: index for index, ticker in enumerate(engine.EXPECTED)}
    allocations, remaining, events = engine.select_allocations(
        shadow, comparison_accounts, {"NVDA": 1.0}, targets, order,
        {"NVDA": (1.0, 1.0, 0.1, 50.0)}, [],
        {"issuers": [], "issuer_ceiling_pct": 100, "common_driver_ceiling_pct": 100},
        2000.0, 0.165, 25.0,
    )
    assert allocations[0]["ticker"] == "NVDA"
    assert allocations[0]["budget"] == pytest.approx(1670.0)
    assert remaining == pytest.approx(0.0)
    assert shadow.cash - allocations[0]["budget"] == pytest.approx(330.0)
    assert events == []


@pytest.mark.parametrize(
    "issuer_ceiling,common_ceiling",
    [(30.0, 25.0), (25.0, 100.0)],
)
def test_selector_matches_frozen_production_greedy_fixture(
    monkeypatch, issuer_ceiling, common_ceiling,
):
    """Differential fixture for protection, clusters, and look-through caps."""
    monkeypatch.setattr(allocate, "days_until_earnings", lambda _ticker: None)
    targets_doc = {
        "destination": [
            {"ticker": "NVDA", "target_pct": 60.0, "asset_class": "equity"},
            {"ticker": "SPY", "target_pct": 23.5, "asset_class": "fund"},
            {"ticker": "CASH", "target_pct": 16.5, "asset_class": "cash"},
        ],
        "caps": {"clusters": [{"name": "semis", "pct": 25.0, "tickers": ["NVDA"]}]},
        "gates": {
            "min_lot_dollars": 25.0,
            "trend_rsi_override": 30.0,
            "earnings_blackout_days": 7,
        },
        "margin": {"leverage_cap": 1.8, "buffer_floor_pct": 30.0},
    }
    roster = allocate.build_roster(targets_doc)
    lookthrough = {
        "issuer_ceiling_pct": issuer_ceiling,
        "common_driver_ceiling_pct": common_ceiling,
        "issuers": [{"ticker": "NVDA", "funds": [{"fund": "SPY", "fund_holding_weight": 0.1}]}],
    }
    metrics = {
        ticker: {"price": 1.0, "sma200": 1.0, "rsi14": 50.0}
        for ticker in ("NVDA", "SPY")
    }
    production = allocate.plan(
        targets_doc, {}, roster, metrics, True, True, 2000.0,
        gates_cfg={}, lookthrough=lookthrough,
    )

    shadow = engine.Account(cash=2000.0)
    comparison_accounts = [engine.Account(cash=2000.0) for _ in range(9)]
    allocations, remaining, _events = engine.select_allocations(
        shadow, comparison_accounts, {"NVDA": 1.0, "SPY": 1.0},
        {"NVDA": 0.60, "SPY": 0.235}, {"NVDA": 0, "SPY": 1},
        {
            "NVDA": (1.0, 1.0, 0.1, 50.0),
            "SPY": (1.0, 1.0, 0.1, 50.0),
        },
        targets_doc["caps"]["clusters"], lookthrough,
        2000.0, 0.165, 25.0,
    )
    actual = [(row["ticker"], row["budget"]) for row in allocations]
    expected = [(row["ticker"], row["dollars"]) for row in production["buys"]]
    assert [ticker for ticker, _value in actual] == [ticker for ticker, _value in expected]
    assert [value for _ticker, value in actual] == pytest.approx([value for _ticker, value in expected])
    assert remaining == pytest.approx(production["protection"]["cash_surplus_dollars"] - sum(value for _, value in expected))


def test_selector_counts_only_final_binding_constraints():
    shadow = engine.Account(cash=2000.0)
    allocations, _remaining, events = engine.select_allocations(
        shadow, [engine.Account(cash=2000.0)], {"NVDA": 1.0},
        {"NVDA": 1.0}, {"NVDA": 0},
        {"NVDA": (1.0, 1.0, 0.1, 50.0)},
        [{"name": "broad", "pct": 50.0, "tickers": ["NVDA"]}],
        {
            "issuer_ceiling_pct": 25.0,
            "common_driver_ceiling_pct": 100.0,
            "issuers": [{"ticker": "NVDA", "funds": []}],
        },
        2000.0, 0.0, 25.0,
    )
    assert allocations[0]["budget"] == pytest.approx(500.0)
    assert [(event["constraint"], event["subject"]) for event in events] == [
        ("effective_issuer", "NVDA")
    ]


def test_fill_refuses_negative_cash_and_retains_event():
    order = {"arm": "A_ATR", "bps": 10, "ticker": "SPY", "budget": 100.0, "selection_date": "2023-01-03", "segment": "broad_funds"}
    with pytest.raises(engine.StudyError, match="negative cash"):
        engine._fill_v2(engine.Account(cash=99.0), order, "2023-01-04", 10.0)
    account = engine.Account(cash=100.0)
    engine._fill_v2(account, order, "2023-01-04", 10.0)
    assert account.cash == 0.0
    assert account.fills[0]["notional"] + account.fills[0]["cost"] == pytest.approx(100.0)


def test_segment_mirror_caps_fill_at_cash_after_negative_carry():
    order = {"arm": "C_IMMEDIATE", "bps": 0, "ticker": "VEA", "budget": 140.0, "selection_date": "2021-06-01", "segment": "broad_funds"}
    account = engine.Account(cash=139.9981422222222)
    engine._fill_v2(account, order, "2021-06-02", 50.0, segment_mirror=True)
    assert account.cash == pytest.approx(0.0)
    assert account.fills[0]["budget"] == pytest.approx(139.9981422222222)
    assert account.fills[0]["requested_budget"] == pytest.approx(140.0)
    assert account.fills[0]["segment_mirror"] is True


def test_bootstrap_is_deterministic_and_cost_cells_are_separate():
    paths = {}
    for arm_index, arm in enumerate(engine.ARMS):
        for bps in (0, 10, 25):
            paths[engine.cell_key(arm, bps)] = [
                {"date": "2024-04-02", "return": 0.0},
                {"date": "2024-04-03", "return": 0.001 * arm_index - bps / 1_000_000},
                {"date": "2024-04-04", "return": -0.0005 + 0.001 * arm_index},
            ]
    cfg = {"friction_bps": [0, 10, 25], "bootstrap": {"resamples": 20, "mean_block_sessions": 2}}
    first = engine.bootstrap(paths, cfg)
    assert first == engine.bootstrap(paths, cfg)
    assert {row["cost_bps"] for row in first} == {0, 10, 25}
    assert all(row["resamples"] == 20 for row in first)


def _synthetic_result():
    dates = ("2021-06-01", "2021-06-02", "2022-01-03", "2022-01-04", "2023-12-29", "2024-04-02", "2024-04-03", "2026-07-31")
    accounts = {}
    paths = {}
    for arm in engine.ARMS:
        for bps in (0, 10, 25):
            for scope in engine.SCOPES:
                cell = engine.cell_key(arm, bps, scope)
                accounts[cell] = engine.Account()
                paths[cell] = [{
                    "date": day, "index": 1.0, "price_only_index": 1.0,
                    "return": 0.0, "risk_free_return": 0.0,
                    "preflow_nav": 100.0, "postflow_nav": 100.0,
                    "price_only_preflow_nav": 100.0, "price_only_postflow_nav": 100.0,
                    "external_flow": 0.0, "cash": 100.0, "whole_nav": 100.0,
                    "receivables": 0.0, "receivables_by_ticker": {}, "position_values": {},
                } for day in dates]
    return {"accounts": accounts, "paths": paths, "cycles": [], "orders": [], "constraint_events": []}


def test_retained_events_and_paths_recompute_metric_matrix():
    original = _synthetic_result()
    paths_doc = {f"{arm}|{bps}|{scope}": rows for (arm, bps, scope), rows in original["paths"].items()}
    reconstructed = engine.retained_result(paths_doc, engine.account_events(original), [], [], [])
    cfg = {"friction_bps": [0, 10, 25]}
    assert engine.metrics(reconstructed, cfg) == engine.metrics(original, cfg)
    assert len(engine.metrics(reconstructed, cfg)) == 108


def test_target_deviation_includes_zero_weight_eligible_names():
    result = _synthetic_result()
    cfg = {"friction_bps": [0, 10, 25]}
    whole = engine._metric_row(result, cfg, "A_ATR", 10, "whole", "context", "2021-06-01", "2023-12-29")
    equity = engine._metric_row(result, cfg, "A_ATR", 10, "equity", "context", "2021-06-01", "2023-12-29")
    assert whole["max_target_deviation"] == pytest.approx(0.15)
    assert equity["max_target_deviation"] == pytest.approx(0.06)


def test_every_consumed_support_input_is_pinned_in_manifest():
    cfg = engine.config()
    manifest = engine.bundle(cfg, False)
    assert set(cfg["configuration_hashes"]).issubset(manifest["files"])
    assert set(cfg["support_hashes"]).issubset(manifest["files"])
    assert str(engine.ANOMALIES.relative_to(engine.ROOT)) in manifest["files"]


def test_retained_result_refuses_missing_event_cell():
    original = _synthetic_result()
    paths_doc = {f"{arm}|{bps}|{scope}": rows for (arm, bps, scope), rows in original["paths"].items()}
    events = engine.account_events(original)
    events.pop("A_ATR|0|whole")
    with pytest.raises(engine.StudyError, match="missing event ledger"):
        engine.retained_result(paths_doc, events, [], [], [])


def test_gate_boundaries_are_strict_for_return_and_inclusive_for_drawdown():
    metric = {}
    for arm in engine.ARMS:
        for bps in (0, 10, 25):
            metric[f"{arm}|{bps}|whole|holdout"] = {"annualized_twr": 0.10, "max_drawdown": -0.20}
    for bps in (0, 10, 25):
        metric[f"B_FIXED|{bps}|whole|holdout"] = {"annualized_twr": 0.11, "max_drawdown": -0.21}
    boot = [{"challenger": a, "baseline": b, "cost_bps": c, "probability_challenger_exceeds": 0.90} for a in engine.ARMS for b in engine.ARMS if a != b for c in (0, 10, 25)]
    result = engine.evaluate_gates(metric, boot, {"friction_bps": [0, 10, 25], "decision_friction_bps": 10})
    comparison = next(row for row in result["pairwise_gates"] if row["challenger"] == "B_FIXED" and row["baseline"] == "A_ATR")
    assert comparison["passed"] is False


def test_canonical_json_rejects_nonfinite_numbers():
    with pytest.raises(ValueError):
        engine.canonical({"bad": float("inf")})


def test_config_keeps_advisory_and_stage1_boundaries():
    cfg = engine.config()
    assert cfg["schema_version"] == "2.0"
    assert cfg["study_id"] == "LADDER-V2-0001"
    assert cfg["window"] == {
        "simulation_start": engine.date(2021, 6, 1), "context_end": engine.date(2023, 12, 29),
        "holdout_start": engine.date(2024, 4, 2), "end": engine.date(2026, 7, 31),
    }
    assert cfg["friction_bps"] == [0, 10, 25]
    assert cfg["monthly_contribution"] == 2000.0
    assert cfg["protected_weight"] == 0.165
    assert cfg["bootstrap"] == {"seed": 20260907, "resamples": 2000, "mean_block_sessions": 21}
    assert cfg["authority"][-1] == "LADDER-0004"
    assert cfg["holdout_previously_exposed"] is True
    assert cfg["advisory_only"] is True
    assert cfg["stage1"] == "UNARMED_AND_NOT_EXECUTABLE"
    forbidden = {"allocate.py", "levels.py", "holdings.yaml"}
    assert not forbidden.intersection({path.name for path in Path(engine.STUDY).rglob("*")})
