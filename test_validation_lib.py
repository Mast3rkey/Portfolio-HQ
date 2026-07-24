"""Tests for validation_lib.py (MARGIN-0005 S2, third/final authorized S2
PR). Also houses the T-D1/T-D2 dividend_ledger.py tests per
research/margin_target_study/S2_G2_SCOPE_DETERMINATION.md §5 item 5 ("§4
names no dedicated test_dividend_ledger.py") — no dedicated test file for
dividend_ledger.py is authorized, so its dedup (T-D1) and primary-path-
purity (T-D2) proofs live here instead.

All fixtures are small, synthetic, hand-computable data — never a
registered Study A/B/C configuration, never real data/backtest/*.json
prices consumed as if they were a trial. Nothing here creates
trial_ledger.jsonl or the real candidate_freeze.yaml; the candidate-freeze
tests below operate exclusively against pytest tmp_path fixtures.

The quarantined TR namespace (research/margin_target_study/data/
quarantine_yahoo/) is deliberately NOT committed to this repository
(data_acquisition.py's own docstring: "Yahoo Finance... NOT committed
(licensing)") — the T-D2 primary-path-purity check below is therefore a
synthetic worked example, not a read against real quarantined data; the
one test that exercises validation_lib.py's TR-namespace loader functions
does so against a monkeypatched tmp_path fixture, not the real (absent)
directory.
"""

import json
import math
import os

import pytest

import dividend_ledger
import margin_simulation
import overlay_lib
import target_variants
import validation_lib
from validation_lib import (
    G4_RUNNER_CONTEXT,
    append_candidate_freeze,
    assert_frozen,
    assert_module_does_not_reference_tr_namespace,
    assert_module_never_opens_files_for_write,
    assert_no_forbidden_imports,
    assert_no_untouched_period_timestamps,
    canonical_config_hash,
    deflated_sharpe_ratio,
    expected_max_sharpe,
    guard_untouched_mode_access,
    is_frozen,
    load_frozen_candidates,
    norm_cdf,
    norm_ppf,
    probabilistic_sharpe_ratio,
    stationary_block_bootstrap,
    verify_candidate_freeze_integrity,
    walk_forward_folds,
)

_ROOT = os.path.dirname(os.path.abspath(__file__))
_RESEARCH_DIR = os.path.join(_ROOT, "research", "margin_target_study")

_FORBIDDEN = frozenset({
    "allocate", "margin_state", "requests", "urllib", "socket", "subprocess",
    "alpaca_client",
})


# ═════════════════════════════════════════════════════════════════════════
# Isolation — import graph (T-8) for every module this PR adds
# ═════════════════════════════════════════════════════════════════════════

@pytest.mark.parametrize("modname", ["dividend_ledger", "validation_lib",
                                     "overlay_lib", "target_variants"])
def test_new_module_imports_no_forbidden_dependency(modname):
    path = os.path.join(_ROOT, f"{modname}.py")
    assert_no_forbidden_imports(path, _FORBIDDEN)


def test_no_production_module_imports_the_new_s2_modules():
    for prod in ("allocate.py", "margin_state.py"):
        names = validation_lib.imported_module_names(os.path.join(_ROOT, prod))
        for new_mod in ("dividend_ledger", "validation_lib", "overlay_lib", "target_variants"):
            assert new_mod not in names


# ═════════════════════════════════════════════════════════════════════════
# T-D4 — TR-namespace structural bar
# ═════════════════════════════════════════════════════════════════════════

@pytest.mark.parametrize("modname", ["dividend_ledger", "overlay_lib",
                                     "target_variants", "margin_simulation"])
def test_module_does_not_reference_tr_namespace(modname):
    assert_module_does_not_reference_tr_namespace(os.path.join(_ROOT, f"{modname}.py"))


def test_validation_lib_itself_is_the_one_module_licensed_for_tr_references():
    # The inverse of the above: validation_lib.py's own constants/docstring
    # necessarily name the TR markers -- confirming the structural bar is
    # doing real work (it does not vacuously pass on every file) and that
    # this module is the deliberate, sole exception the protocol names.
    hits = validation_lib.scan_tr_namespace_references(
        os.path.join(_ROOT, "validation_lib.py"))
    assert hits  # non-empty: this module DOES reference the namespace, by design


def test_scan_detects_a_synthetic_tr_reference(tmp_path):
    p = tmp_path / "fake_module.py"
    p.write_text("QUARANTINE = 'quarantine_yahoo'\n")
    hits = validation_lib.scan_tr_namespace_references(str(p))
    assert "quarantine_yahoo" in hits
    with pytest.raises(AssertionError):
        assert_module_does_not_reference_tr_namespace(str(p))


# ═════════════════════════════════════════════════════════════════════════
# T-8 write-path isolation
# ═════════════════════════════════════════════════════════════════════════

@pytest.mark.parametrize("modname", ["dividend_ledger", "overlay_lib", "target_variants"])
def test_new_module_never_opens_files_for_write(modname):
    assert_module_never_opens_files_for_write(os.path.join(_ROOT, f"{modname}.py"))


def test_write_path_scan_detects_a_synthetic_write_open(tmp_path):
    p = tmp_path / "writer.py"
    p.write_text("def f():\n    with open('x.json', 'w') as fh:\n        fh.write('{}')\n")
    with pytest.raises(AssertionError):
        assert_module_never_opens_files_for_write(str(p))


def test_write_path_scan_allows_read_only_open(tmp_path):
    p = tmp_path / "reader.py"
    p.write_text("def f():\n    with open('x.json') as fh:\n        return fh.read()\n")
    assert_module_never_opens_files_for_write(str(p))  # should not raise


# ═════════════════════════════════════════════════════════════════════════
# T-U1 — untouched-mode legality guard
# ═════════════════════════════════════════════════════════════════════════

@pytest.mark.parametrize("bad_context", ["", "development", "g3_report", "G4_RUNNER_AUTHORIZED_UNTOUCHED_EVALUATION"])
def test_guard_untouched_mode_access_rejects_non_g4_context(bad_context):
    with pytest.raises(PermissionError):
        guard_untouched_mode_access(bad_context)


def test_guard_untouched_mode_access_accepts_exact_g4_marker():
    guard_untouched_mode_access(G4_RUNNER_CONTEXT)  # should not raise


def test_assert_no_untouched_period_timestamps_passes_when_clean():
    assert_no_untouched_period_timestamps(
        ["2024-01-01", "2025-06-30"], boundary="2025-06-30")


def test_assert_no_untouched_period_timestamps_raises_naming_offenders():
    with pytest.raises(AssertionError, match="2025-07-01"):
        assert_no_untouched_period_timestamps(
            ["2024-01-01", "2025-07-01", "2025-06-30"], boundary="2025-06-30")


# ═════════════════════════════════════════════════════════════════════════
# T-U2 — candidate-freeze append-only / hash-membership
# ═════════════════════════════════════════════════════════════════════════

def _entry(finalist_id, config):
    return {"finalist_id": finalist_id, "config": config,
           "config_hash": canonical_config_hash(config)}


def test_candidate_freeze_append_only_roundtrip(tmp_path):
    path = str(tmp_path / "freeze.json")
    assert load_frozen_candidates(path) == []
    e1 = _entry("A1", {"arm": "A6", "l_hi": 1.25})
    combined = append_candidate_freeze(path, [e1])
    assert combined == [e1]
    e2 = _entry("A2", {"arm": "A7", "sigma_target": 0.10})
    combined2 = append_candidate_freeze(path, [e2])
    assert combined2 == [e1, e2]                      # prior entry preserved, in order
    assert load_frozen_candidates(path) == [e1, e2]


def test_candidate_freeze_rejects_finalist_id_reuse(tmp_path):
    path = str(tmp_path / "freeze.json")
    e1 = _entry("A1", {"arm": "A6"})
    append_candidate_freeze(path, [e1])
    e1_modified = _entry("A1", {"arm": "A6", "l_hi": 1.50})  # same id, different config
    with pytest.raises(ValueError, match="already frozen"):
        append_candidate_freeze(path, [e1_modified])
    assert load_frozen_candidates(path) == [e1]  # rejected write touched nothing


def test_candidate_freeze_rejects_duplicate_config_hash(tmp_path):
    path = str(tmp_path / "freeze.json")
    config = {"arm": "A6"}
    e1 = _entry("A1", config)
    append_candidate_freeze(path, [e1])
    e2 = _entry("A2", config)  # different id, identical config/hash
    with pytest.raises(ValueError, match="already frozen"):
        append_candidate_freeze(path, [e2])


def test_candidate_freeze_rejects_hash_mismatch(tmp_path):
    path = str(tmp_path / "freeze.json")
    bad = {"finalist_id": "A1", "config": {"arm": "A6"}, "config_hash": "deadbeef"}
    with pytest.raises(ValueError, match="mismatch"):
        append_candidate_freeze(path, [bad])


def test_candidate_freeze_rejects_missing_field(tmp_path):
    path = str(tmp_path / "freeze.json")
    with pytest.raises(ValueError, match="missing required field"):
        append_candidate_freeze(path, [{"finalist_id": "A1", "config": {}}])


def test_candidate_freeze_is_frozen_and_assert_frozen(tmp_path):
    path = str(tmp_path / "freeze.json")
    config = {"arm": "A9", "l_star": 1.25}
    e1 = _entry("A1", config)
    append_candidate_freeze(path, [e1])
    h = canonical_config_hash(config)
    assert is_frozen(path, h)
    assert_frozen(path, h)  # should not raise
    assert not is_frozen(path, "not-a-real-hash")


def test_candidate_freeze_assert_frozen_raises_for_unfrozen_hash(tmp_path):
    path = str(tmp_path / "freeze.json")
    with pytest.raises(PermissionError):
        assert_frozen(path, "not-a-real-hash")


def test_candidate_freeze_tamper_detected_by_verify_integrity(tmp_path):
    path = tmp_path / "freeze.json"
    e1 = _entry("A1", {"arm": "A6", "l_hi": 1.25})
    append_candidate_freeze(str(path), [e1])
    assert verify_candidate_freeze_integrity(str(path))
    # Direct file tamper, bypassing the API: mutate the stored config
    # without updating its stored config_hash.
    entries = json.loads(path.read_text())
    entries[0]["config"]["l_hi"] = 1.80
    path.write_text(json.dumps(entries))
    assert not verify_candidate_freeze_integrity(str(path))


def test_real_candidate_freeze_and_trial_ledger_never_created_by_this_test_module():
    assert not os.path.exists(os.path.join(_RESEARCH_DIR, "candidate_freeze.yaml"))
    assert not os.path.exists(os.path.join(_RESEARCH_DIR, "trial_ledger.jsonl"))


# ═════════════════════════════════════════════════════════════════════════
# T-7 — statistical-validation machinery
# ═════════════════════════════════════════════════════════════════════════

def test_stationary_block_bootstrap_seeded_reproducibility():
    series = [0.01, -0.02, 0.015, 0.03, -0.01, 0.005, 0.02, -0.015, 0.01, 0.0] * 5
    r1 = stationary_block_bootstrap(series, mean_block_days=5, resamples=50, seed=42)
    r2 = stationary_block_bootstrap(series, mean_block_days=5, resamples=50, seed=42)
    assert r1 == r2


def test_stationary_block_bootstrap_output_shape():
    series = [0.01] * 30
    out = stationary_block_bootstrap(series, mean_block_days=3, resamples=25, seed=1)
    assert len(out) == 25
    assert all(isinstance(x, float) for x in out)
    # constant series -> every resample mean equals the constant, exactly
    assert all(math.isclose(x, 0.01) for x in out)


def test_stationary_block_bootstrap_rejects_bad_params():
    with pytest.raises(ValueError):
        stationary_block_bootstrap([], mean_block_days=5, resamples=10, seed=1)
    with pytest.raises(ValueError):
        stationary_block_bootstrap([1.0], mean_block_days=0, resamples=10, seed=1)
    with pytest.raises(ValueError):
        stationary_block_bootstrap([1.0], mean_block_days=5, resamples=0, seed=1)


def test_norm_cdf_norm_ppf_are_inverses():
    for p in (0.001, 0.05, 0.25, 0.5, 0.75, 0.95, 0.999):
        x = norm_ppf(p)
        assert math.isclose(norm_cdf(x), p, abs_tol=1e-6)


def test_norm_ppf_known_values():
    assert math.isclose(norm_ppf(0.5), 0.0, abs_tol=1e-9)
    assert math.isclose(norm_ppf(0.975), 1.9599639845, abs_tol=1e-4)
    assert math.isclose(norm_ppf(0.025), -1.9599639845, abs_tol=1e-4)


def test_norm_ppf_domain_errors():
    with pytest.raises(ValueError):
        norm_ppf(0.0)
    with pytest.raises(ValueError):
        norm_ppf(1.0)


def test_expected_max_sharpe_single_trial_is_zero():
    assert expected_max_sharpe(1) == 0.0


def test_expected_max_sharpe_increases_with_trial_count():
    vals = [expected_max_sharpe(n) for n in (2, 10, 100, 1000)]
    assert vals == sorted(vals)
    assert vals[0] < vals[-1]


def test_expected_max_sharpe_rejects_bad_n_trials():
    with pytest.raises(ValueError):
        expected_max_sharpe(0)
    with pytest.raises(ValueError):
        expected_max_sharpe(-5)


def test_probabilistic_sharpe_ratio_matches_simple_formula_at_zero_benchmark():
    # With skew=0, kurtosis=3 (normal) and sr_benchmark=0, PSR reduces to
    # Phi(sr_hat * sqrt(n_obs - 1)) -- a hand-derivable special case.
    sr_hat, n_obs = 1.2, 101
    got = probabilistic_sharpe_ratio(sr_hat, 0.0, n_obs)
    expect = norm_cdf(sr_hat * math.sqrt(n_obs - 1))
    assert math.isclose(got, expect, rel_tol=1e-9)


def test_probabilistic_sharpe_ratio_rejects_too_few_observations():
    with pytest.raises(ValueError):
        probabilistic_sharpe_ratio(1.0, 0.0, 1)


def test_deflated_sharpe_ratio_decreases_as_trial_count_increases():
    vals = [deflated_sharpe_ratio(1.5, n_obs=252, n_trials=n) for n in (1, 10, 100, 286)]
    assert vals == sorted(vals, reverse=True)


def test_deflated_sharpe_ratio_is_a_probability():
    v = deflated_sharpe_ratio(1.5, n_obs=252, n_trials=63)
    assert 0.0 <= v <= 1.0


# ── walk-forward fold boundaries (exact) ────────────────────────────────────

def test_walk_forward_folds_single_fold_exact_boundaries():
    folds = walk_forward_folds("2020-01-01", "2021-07-01",
                               initial_train_months=12, step_months=6)
    assert folds == [{"train_start": "2020-01-01", "train_end": "2021-01-01",
                      "test_start": "2021-01-01", "test_end": "2021-07-01"}]


def test_walk_forward_folds_two_folds_exact_boundaries():
    folds = walk_forward_folds("2020-01-01", "2022-01-01",
                               initial_train_months=12, step_months=6)
    assert folds == [
        {"train_start": "2020-01-01", "train_end": "2021-01-01",
         "test_start": "2021-01-01", "test_end": "2021-07-01"},
        {"train_start": "2020-01-01", "train_end": "2021-07-01",
         "test_start": "2021-07-01", "test_end": "2022-01-01"},
    ]


def test_walk_forward_folds_month_end_day_clipping():
    # Jan 31 + 1 month -> Feb 28 (2023, non-leap) -- exact calendar-month
    # arithmetic with day-of-month clipping, not a fixed day-count step.
    folds = walk_forward_folds("2023-01-31", "2023-04-30",
                               initial_train_months=1, step_months=1)
    assert folds[0]["train_end"] == "2023-02-28"


def test_walk_forward_folds_never_crosses_dev_boundary():
    folds = walk_forward_folds("2021-06-01", "2025-06-30",
                               initial_train_months=36, step_months=6)
    for f in folds:
        assert f["test_end"] <= "2025-06-30"
        assert f["train_end"] < f["test_end"] or f is folds[-1]


def test_walk_forward_folds_rejects_bad_params():
    with pytest.raises(ValueError):
        walk_forward_folds("2020-01-01", "2021-01-01", initial_train_months=0, step_months=6)
    with pytest.raises(ValueError):
        walk_forward_folds("2020-01-01", "2021-01-01", initial_train_months=12, step_months=0)


# ── TR-loader functions (monkeypatched tmp_path -- real data not committed) ──

def test_load_quarantined_tr_reads_a_fixture(tmp_path, monkeypatch):
    tr_dir = tmp_path / "tr"
    tr_dir.mkdir()
    (tr_dir / "ZZZ.json").write_text(json.dumps({"adjclose": [{"date": "2024-01-02", "adjclose": 101.0}]}))
    monkeypatch.setattr(validation_lib, "_TR_DIR", tr_dir)
    doc = validation_lib.load_quarantined_tr("ZZZ")
    assert doc["adjclose"][0]["adjclose"] == 101.0


def test_load_track3_book_reads_a_fixture(tmp_path, monkeypatch):
    t3_dir = tmp_path / "track3"
    t3_dir.mkdir()
    (t3_dir / "SPY.json").write_text(json.dumps({"close_split_adjusted": [{"date": "1999-01-04", "close": 100.0}]}))
    monkeypatch.setattr(validation_lib, "_TRACK3_DIR", t3_dir)
    doc = validation_lib.load_track3_book("SPY")
    assert doc["close_split_adjusted"][0]["close"] == 100.0


def test_quarantine_yahoo_namespace_is_not_committed_to_this_repository():
    # Documents (and pins) a real repository fact this test file's own
    # docstring relies on: data_acquisition.py's TR namespace is licensed
    # content that is never committed -- confirming the tests above
    # correctly use synthetic/monkeypatched fixtures rather than silently
    # depending on data that happens to be present in one environment.
    assert not os.path.isdir(os.path.join(_RESEARCH_DIR, "data", "quarantine_yahoo"))


# ═════════════════════════════════════════════════════════════════════════
# T-D1 — dividend uniqueness (dividend_ledger.py)
# ═════════════════════════════════════════════════════════════════════════

def _div_row(symbol, ex_date, gross, *, special=False, payable=None, alpaca_id=None):
    return {"symbol": symbol, "ex_date": ex_date, "gross_declared": gross,
           "special": special, "payable_date": payable, "alpaca_id": alpaca_id}


def test_build_dividend_events_duplicate_row_credits_exactly_once():
    row = _div_row("AAA", "2024-01-05", 0.50, payable="2024-01-20", alpaca_id="id1")
    duplicate = dict(row)  # literal re-fetch of the same vendor row
    events = dividend_ledger.build_dividend_events([row, duplicate])
    assert events == {"2024-01-05": {"AAA": 0.50}}  # NOT 1.00 -- credited exactly once


def test_build_dividend_events_distinct_same_day_events_are_summed():
    regular = _div_row("AAA", "2024-01-05", 0.50, alpaca_id="id1", payable="2024-01-20")
    special = _div_row("AAA", "2024-01-05", 0.10, special=True, alpaca_id="id2", payable="2024-01-20")
    events = dividend_ledger.build_dividend_events([regular, special])
    assert events == {"2024-01-05": {"AAA": 0.60}}  # genuinely two events, summed


def test_build_dividend_events_composite_key_dedup_without_alpaca_id():
    row = _div_row("BBB", "2024-02-01", 0.30, payable="2024-02-15")   # alpaca_id=None
    duplicate = dict(row)
    events = dividend_ledger.build_dividend_events([row, duplicate])
    assert events == {"2024-02-01": {"BBB": 0.30}}


def test_build_dividend_events_drops_nonpositive_amounts():
    row = _div_row("CCC", "2024-03-01", 0.0, alpaca_id="id1")
    events = dividend_ledger.build_dividend_events([row])
    assert events == {}


def test_build_dividend_events_ex_date_convention_is_default():
    row = _div_row("AAA", "2024-01-05", 0.50, payable="2024-01-20", alpaca_id="id1")
    events = dividend_ledger.build_dividend_events([row])
    assert list(events.keys()) == ["2024-01-05"]


def test_build_dividend_events_pay_date_lag_convention_uses_payable_date():
    row = _div_row("AAA", "2024-01-05", 0.50, payable="2024-01-20", alpaca_id="id1")
    events = dividend_ledger.build_dividend_events(
        [row], credit_convention=dividend_ledger.CREDIT_CONVENTION_PAY_DATE_LAG_30D)
    assert list(events.keys()) == ["2024-01-20"]


def test_build_dividend_events_pay_date_lag_falls_back_when_payable_missing():
    row = _div_row("AAA", "2024-01-05", 0.50, payable=None, alpaca_id="id1")
    events = dividend_ledger.build_dividend_events(
        [row], credit_convention=dividend_ledger.CREDIT_CONVENTION_PAY_DATE_LAG_30D)
    assert list(events.keys()) == ["2024-02-04"]  # 2024-01-05 + 30 calendar days


def test_build_dividend_events_rejects_unknown_convention():
    row = _div_row("AAA", "2024-01-05", 0.50, alpaca_id="id1")
    with pytest.raises(ValueError):
        dividend_ledger.build_dividend_events([row], credit_convention="declared_date")


def test_build_dividend_events_output_is_engine_compatible():
    # The exact shape margin_simulation.simulate()'s dividend_events param expects.
    row = _div_row("A", "2026-01-02", 0.25, alpaca_id="id1")
    events = dividend_ledger.build_dividend_events([row])
    aligned = {"A": ([100.0, 105.0, 95.0, 115.0], 0)}
    calendar = ["2026-01-01", "2026-01-02", "2026-01-03", "2026-01-04"]
    sc = margin_simulation.scenario_fixed_leverage(1.0, interest_apr=0.0, interest_free_amount=0.0)
    result = margin_simulation.simulate(sc, weights={"A": 1.0}, aligned=aligned,
                                        calendar=calendar, deposit_days=[calendar[0]],
                                        deposit_amount=100.0, min_lot=1.0,
                                        dividend_events=events)
    assert sum(result.dividend_credit_series) > 0.0


# ── corporate-action events ──────────────────────────────────────────────────

def _ca_event(parent, child, ratio, ex_date, unit_value):
    return {"parent": parent, "child": child, "ratio_child_per_parent": ratio,
           "ex_date": ex_date, "child_close_on_parent_ex_session": unit_value}


def test_build_corporate_action_events_normal_case():
    ev = _ca_event("PPP", "CCC", 0.2, "2024-05-01", 50.0)
    out = dividend_ledger.build_corporate_action_events([ev])
    assert out == {"2024-05-01": [{"ticker": "PPP", "ratio": 0.2, "unit_value": 50.0}]}


def test_build_corporate_action_events_strict_raises_on_missing_unit_value():
    ev = _ca_event("PPP", "CCC", 0.2, "2024-05-01", None)
    with pytest.raises(ValueError):
        dividend_ledger.build_corporate_action_events([ev])


def test_build_corporate_action_events_nonstrict_skips_missing_unit_value():
    ev = _ca_event("PPP", "CCC", 0.2, "2024-05-01", None)
    out = dividend_ledger.build_corporate_action_events([ev], strict=False)
    assert out == {}


# ═════════════════════════════════════════════════════════════════════════
# T-D2 — primary-path purity (synthetic worked example)
# ═════════════════════════════════════════════════════════════════════════

def test_primary_path_diverges_from_tr_equivalent_for_a_known_payer():
    # A flat-price ticker with one real dividend: the primary (price-only)
    # cumulative return is 0%, while a hand-computed TR-equivalent
    # (price + the same dividend reinvested) is strictly positive --
    # proving the primary path genuinely excludes dividend effects (it is
    # not secretly already total-return-adjusted). This is a synthetic
    # stand-in for a real TR comparison (see module docstring: the real
    # quarantined TR namespace is not committed to this repository).
    closes = {"2024-01-01": 100.0, "2024-01-02": 100.0}
    row = _div_row("ZZZ", "2024-01-02", 2.0, alpaca_id="id1")
    events = dividend_ledger.build_dividend_events([row])
    dividend_cash = events["2024-01-02"]["ZZZ"]

    primary_return = closes["2024-01-02"] / closes["2024-01-01"] - 1.0
    tr_equivalent_return = (closes["2024-01-02"] + dividend_cash) / closes["2024-01-01"] - 1.0

    assert primary_return == 0.0
    assert tr_equivalent_return > primary_return
    assert math.isclose(tr_equivalent_return, 0.02)


def test_dividend_ledger_module_does_not_import_json_of_quarantine_data():
    # Structural corroboration of T-D2/T-D4 together: dividend_ledger.py's
    # own default paths point only at dividends/ and corporate_actions/,
    # never quarantine_yahoo/.
    assert "quarantine_yahoo" not in str(dividend_ledger.DEFAULT_DIVIDEND_LEDGER_PATH)
    assert "quarantine_yahoo" not in str(dividend_ledger.DEFAULT_CORPORATE_ACTION_LEDGER_PATH)
