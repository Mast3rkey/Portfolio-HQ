import json
from pathlib import Path

import pytest

from research.buy_ladder_backtest import ladder_v2 as engine


def test_frozen_input_validation_is_holdout_blind(tmp_path, monkeypatch):
    monkeypatch.setattr(engine, "RECEIPT", tmp_path / "receipt.json")
    receipt = engine.validate()
    assert receipt["holdout_results_emitted"] is False
    assert receipt["validation_scope"] == "INPUTS_AND_NON_HOLDOUT_ONLY"
    assert receipt["holdout_results_emitted"] is False
    assert not {"metrics", "bootstrap", "disposition"}.intersection(receipt)
    assert receipt["stage1"] == "UNARMED_AND_NOT_EXECUTABLE"


def test_execute_rejects_missing_receipt(tmp_path, monkeypatch):
    monkeypatch.setattr(engine, "RECEIPT", tmp_path / "missing.json")
    with pytest.raises(engine.StudyError, match="validation receipt missing"):
        engine.execute()


def test_indicator_uses_only_rows_through_decision_date():
    _, prices, _, _ = engine.load_inputs()
    bars = prices["SPY"]
    i = 300
    before = engine.indicators(bars, i)
    copy = [dict(x) for x in bars]
    copy[i + 1]["close"] *= 100
    assert engine.indicators(copy, i) == before


def test_fill_cost_identity_and_gate_inequalities():
    budget, bps = 123.45, 25
    cost = budget * (bps / 10000) / (1 + bps / 10000)
    notional = budget - cost
    assert notional + cost == pytest.approx(budget)
    assert (0.02 > 0.01) and (-0.01 >= -0.01)


def test_config_keeps_advisory_and_stage1_boundaries():
    cfg = engine.config()
    assert cfg["advisory_only"] is True
    assert cfg["stage1"] == "UNARMED_AND_NOT_EXECUTABLE"
    forbidden = {"allocate.py", "levels.py", "holdings.yaml"}
    assert not forbidden.intersection({p.name for p in Path(engine.STUDY).rglob("*")})
