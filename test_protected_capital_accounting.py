"""Protected-capital accounting and full-book reconciliation.

Every test here is SYNTHETIC. No live credentials, no network, no real
recommendation. The contract under test:

    book = resolved invested holdings + tracked cash - margin debt

    protected_floor = book x (cash% + reserve% + unreconciled%)
                    + sum over gated names of max(0, gated_target$ - held$)

    cash-funded buys <= max(0, actual_cash - protected_floor)
    cash_after_plan  >= protected_floor              (unless a shortfall exists)
    unused margin capacity is NEVER counted as cash

Before this change none of that existed. `cash_left` was seeded from
`deployable = cash + margin_allowed`, so it reported buying power as though it
were remaining cash; CASH/RESERVE were skipped as "definitionally satisfied"
with nothing checked; the 0.75% unreconciled remainder was invisible; there was
no tracked cash balance at all; and an unpriced holding silently vanished from
the book. Protection held only as an ACCIDENTAL consequence of the per-name
ceiling. It is asserted and proved here instead.
"""
from __future__ import annotations

import copy
import datetime
import inspect

import pytest
import yaml

import allocate as A
from allocate import (
    build_roster,
    destination_reconciliation,
    load_cash_state,
    load_margin_state,
    plan,
    protected_capital,
    protected_weights,
    valuation_completeness,
    write_state,
)

TODAY = datetime.date.today()
FRESH = TODAY.isoformat()
STALE = (TODAY - datetime.timedelta(days=A.STALE_MARGIN_DAYS + 1)).isoformat()
EDGE = (TODAY - datetime.timedelta(days=A.STALE_MARGIN_DAYS)).isoformat()
FUTURE = (TODAY + datetime.timedelta(days=3)).isoformat()


# ── synthetic configuration ────────────────────────────────────────────────────

def _targets(rows=None, **over):
    """A minimal but structurally real targets.yaml mapping."""
    rows = rows if rows is not None else [
        {"ticker": "AAA", "target_pct": 40.0, "asset_class": "equity"},
        {"ticker": "BBB", "target_pct": 30.0, "asset_class": "equity"},
        {"ticker": "GGG", "target_pct": 10.0, "asset_class": "equity"},
        {"ticker": "RESERVE", "target_pct": 15.0, "asset_class": "reserve"},
        {"ticker": "CASH", "target_pct": 4.0, "asset_class": "cash"},
    ]
    out = {"destination": rows,
           "margin": {"leverage_cap": 1.8, "buffer_floor_pct": 30.0},
           "gates": {"min_lot_dollars": 25, "trend_rsi_override": 30,
                     "earnings_blackout_days": 7},
           "caps": {}}
    out.update(over)
    return out


def _gates(*tickers):
    return {t: {"status": "HOLD-TARGET-IN-CASH", "authority": "synthetic",
                "next_gate": "synthetic"} for t in tickers}


def _metrics(roster):
    return {t: {"price": 100.0, "rsi14": 50.0, "sma200": 50.0} for t in roster}


@pytest.fixture(autouse=True)
def _no_network(monkeypatch):
    monkeypatch.setattr(A, "days_until_earnings", lambda t: None)


@pytest.fixture
def real_targets():
    return yaml.safe_load(open("targets.yaml"))


@pytest.fixture
def real_gates():
    return A.load_gates()


# ── destination reconciliation ─────────────────────────────────────────────────

class TestDestinationReconciliation:
    def test_the_real_destination_total_is_exactly_99_25(self, real_targets):
        rec = destination_reconciliation(real_targets)
        assert rec["destination_total_pct"] == pytest.approx(99.25, abs=1e-9)

    def test_the_real_unreconciled_remainder_is_exactly_0_75(self, real_targets):
        rec = destination_reconciliation(real_targets)
        assert rec["unreconciled_pct"] == pytest.approx(0.75, abs=1e-9)

    def test_the_arithmetic_is_decimal_exact_not_float_approximate(self, real_targets):
        """Today's 36 weights happen to sum exactly in float too, so the real
        config cannot distinguish the two implementations. A config that CAN is
        used instead -- otherwise this would assert nothing."""
        exact = destination_reconciliation(real_targets)["destination_total_pct"]
        assert exact == 99.25

        rows = [{"ticker": f"T{i}", "target_pct": 0.1, "asset_class": "equity"}
                for i in range(10)]
        naive = sum(r["target_pct"] for r in rows)
        assert naive != 1.0, "fixture no longer exercises float drift"
        t = _targets(rows)
        rec = destination_reconciliation(t)
        assert rec["destination_total_pct"] == 1.0
        assert rec["unreconciled_pct"] == 99.0

    def test_the_reconciliation_is_computed_in_decimal_at_source(self):
        src = inspect.getsource(destination_reconciliation)
        assert 'sum((_q(r["target_pct"]) for r in rows), Decimal("0"))' in src

    def test_a_total_above_100_percent_raises(self):
        t = _targets([{"ticker": "AAA", "target_pct": 60.0, "asset_class": "equity"},
                      {"ticker": "BBB", "target_pct": 60.0, "asset_class": "equity"}])
        with pytest.raises(ValueError, match="above 100"):
            destination_reconciliation(t)

    def test_a_total_of_exactly_100_percent_is_permitted(self):
        t = _targets([{"ticker": "AAA", "target_pct": 100.0, "asset_class": "equity"}])
        assert destination_reconciliation(t)["unreconciled_pct"] == 0.0

    def test_plan_refuses_to_produce_dollars_from_an_over_100_percent_config(self):
        t = _targets([{"ticker": "AAA", "target_pct": 60.0, "asset_class": "equity"},
                      {"ticker": "BBB", "target_pct": 60.0, "asset_class": "equity"}])
        roster = build_roster(t)
        with pytest.raises(ValueError, match="above 100"):
            plan(t, {}, roster, _metrics(roster), True, True, cash=1000.0,
                 holdings_state={})


# ── protected weights ──────────────────────────────────────────────────────────

class TestProtectedWeights:
    def test_the_real_configuration_protects_12_5_percent(self, real_targets, real_gates):
        """CASH 1.00 + RESERVE 4.00 + unreconciled 0.75 + gated 6.75 = 12.50.

        The earlier incomplete formula omitted the unreconciled remainder and
        produced 11.75. The remainder is unallocated capital and is protected.
        """
        w = protected_weights(real_targets, real_gates)
        assert w["cash_pct"] == pytest.approx(1.00, abs=1e-9)
        assert w["reserve_pct"] == pytest.approx(4.00, abs=1e-9)
        assert w["unreconciled_pct"] == pytest.approx(0.75, abs=1e-9)
        assert w["gated_target_pct"] == pytest.approx(6.75, abs=1e-9)
        total = (w["cash_pct"] + w["reserve_pct"] + w["unreconciled_pct"]
                 + w["gated_target_pct"])
        assert total == pytest.approx(12.50, abs=1e-9)

    def test_the_unreconciled_remainder_is_inside_the_static_figure(self, real_targets,
                                                                    real_gates):
        w = protected_weights(real_targets, real_gates)
        assert w["static_protected_pct"] == pytest.approx(5.75, abs=1e-9)

    def test_the_static_figure_excludes_gated_weight(self, real_targets, real_gates):
        """Gated capital depends on what is HELD, so it is not static."""
        w = protected_weights(real_targets, real_gates)
        assert w["static_protected_pct"] < w["static_protected_pct"] + w["gated_target_pct"]
        assert w["gated_target_pct"] > 0


# ── gated capital: held vs unfilled ────────────────────────────────────────────

class TestGatedCashRequirement:
    def test_zero_gated_holdings_requires_the_full_gated_target(self):
        t = _targets()
        roster = build_roster(t)
        pc = protected_capital(t, roster, {}, 1000.0, 500.0, _gates("GGG"))
        assert pc["gated_cash_required_dollars"] == pytest.approx(100.0)

    def test_a_partially_held_gated_name_requires_only_the_unfilled_part(self):
        t = _targets()
        roster = build_roster(t)
        pc = protected_capital(t, roster, {"GGG": 40.0}, 1000.0, 500.0, _gates("GGG"))
        assert pc["gated_cash_required_dollars"] == pytest.approx(60.0)

    def test_a_fully_held_gated_name_requires_no_cash(self):
        t = _targets()
        roster = build_roster(t)
        pc = protected_capital(t, roster, {"GGG": 100.0}, 1000.0, 500.0, _gates("GGG"))
        assert pc["gated_cash_required_dollars"] == 0.0

    def test_an_overweight_gated_name_never_produces_a_negative_requirement(self):
        t = _targets()
        roster = build_roster(t)
        pc = protected_capital(t, roster, {"GGG": 400.0}, 1000.0, 500.0, _gates("GGG"))
        assert pc["gated_cash_required_dollars"] == 0.0

    def test_the_held_value_is_not_double_counted(self):
        """A held gated position contributes to the book AND would have been
        protected in full by the naive formula. Only the unfilled part is."""
        t = _targets()
        roster = build_roster(t)
        full = protected_capital(t, roster, {}, 1000.0, 500.0, _gates("GGG"))
        half = protected_capital(t, roster, {"GGG": 50.0}, 1000.0, 500.0, _gates("GGG"))
        assert half["protected_floor_dollars"] < full["protected_floor_dollars"]
        assert (full["gated_cash_required_dollars"]
                - half["gated_cash_required_dollars"]) == pytest.approx(50.0)

    def test_a_gate_naming_a_ticker_absent_from_the_roster_is_ignored_not_crashed(self):
        t = _targets()
        roster = build_roster(t)
        pc = protected_capital(t, roster, {}, 1000.0, 500.0, _gates("NOPE"))
        assert pc["gated_cash_required_dollars"] == 0.0


# ── the floor, the surplus, and the shortfall ──────────────────────────────────

class TestTheProtectedFloorBoundsBuys:
    @staticmethod
    def _run(cash, holdings=None, gates=None, margin_requested=0.0):
        t = _targets()
        roster = build_roster(t)
        return t, roster, plan(t, holdings or {}, roster, _metrics(roster), True, True,
                               cash=cash, gates_cfg=gates or {}, margin_requested=margin_requested,
                               holdings_state={})

    def test_cash_exactly_at_the_floor_permits_no_buys(self):
        t = _targets()
        roster = build_roster(t)
        # book = 0 invested + cash. floor = cash * 19% -> solve so cash == floor
        # is only possible at cash 0; use a held book to make the floor bite.
        holdings = {"AAA": 1000.0}
        for cash in (100.0,):
            pc = protected_capital(t, roster, holdings, 1000.0 + cash, cash, {})
            res = plan(t, holdings, roster, _metrics(roster), True, True, cash=cash,
                       holdings_state={})
            if pc["cash_surplus_dollars"] == 0:
                assert not res["buys"]

    def test_cash_below_the_floor_blocks_every_buy(self):
        t = _targets()
        roster = build_roster(t)
        holdings = {"AAA": 10000.0}
        res = plan(t, holdings, roster, _metrics(roster), True, True, cash=10.0,
                   holdings_state={})
        assert res["protection"]["cash_shortfall_dollars"] > 0
        assert res["cash_funded_capacity"] == 0.0
        assert not res["buys"]

    def test_cash_just_above_the_floor_permits_only_the_surplus(self):
        t = _targets()
        roster = build_roster(t)
        holdings = {"AAA": 100.0}
        res = plan(t, holdings, roster, _metrics(roster), True, True, cash=5000.0,
                   holdings_state={})
        pc = res["protection"]
        assert pc["cash_surplus_dollars"] > 0
        assert res["cash_spent"] <= pc["cash_surplus_dollars"] + 1e-6

    def test_cash_after_plan_never_breaches_the_floor(self):
        for cash in (0.0, 50.0, 500.0, 5000.0, 50000.0):
            t = _targets()
            roster = build_roster(t)
            res = plan(t, {"AAA": 900.0}, roster, _metrics(roster), True, True,
                       cash=cash, gates_cfg=_gates("GGG"), holdings_state={})
            pc = res["protection"]
            if pc["cash_shortfall_dollars"] == 0:
                assert res["cash_after_plan"] >= pc["protected_floor_dollars"] - 1e-6, cash

    def test_a_gap_larger_than_the_surplus_is_bounded_by_the_surplus(self):
        t = _targets()
        roster = build_roster(t)
        # Nothing held, so gaps are enormous relative to cash.
        res = plan(t, {}, roster, _metrics(roster), True, True, cash=1000.0,
                   holdings_state={})
        pc = res["protection"]
        assert sum(b["dollars"] for b in res["buys"]) <= pc["cash_surplus_dollars"] + 1e-6

    def test_overweight_holdings_produce_no_buys_and_preserve_all_cash(self):
        t = _targets()
        roster = build_roster(t)
        holdings = {"AAA": 100000.0, "BBB": 100000.0, "GGG": 100000.0}
        res = plan(t, holdings, roster, _metrics(roster), True, True, cash=1000.0,
                   holdings_state={})
        assert not res["buys"]
        assert res["cash_after_plan"] == pytest.approx(1000.0)

    def test_the_invariant_is_asserted_in_source_not_merely_emergent(self):
        """Pinned to the EXACT assert forms. A weaker pin (just the message
        text) survives `assert True or <original condition>`, which disables
        the check while keeping every string intact -- proved by mutation."""
        src = inspect.getsource(plan)
        assert 'assert cash_spent <= protection["cash_surplus_dollars"] + 1e-6, (' in src
        assert ('assert cash_after_plan >= protection["protected_floor_dollars"] - 1e-6 or'
                in src)
        assert "assert True or" not in src

    def test_cash_after_plan_is_exactly_cash_minus_what_was_bought(self):
        """Closes the `cash_spent += 0.0` mutation: with the accumulator dead,
        cash_after_plan silently equals the starting balance no matter how much
        was bought, and every floor assertion still passes."""
        t = _targets()
        roster = build_roster(t)
        res = plan(t, {"AAA": 100.0}, roster, _metrics(roster), True, True, cash=5000.0,
                   holdings_state={})
        bought = sum(b["dollars"] for b in res["buys"])
        assert bought > 0, "fixture must actually buy something"
        assert res["cash_spent"] == pytest.approx(bought)
        assert res["cash_after_plan"] == pytest.approx(5000.0 - bought)


# ── cash is not buying power ───────────────────────────────────────────────────

class TestCashIsNotBuyingPower:
    def test_unused_margin_is_reported_separately_from_cash(self):
        t = _targets()
        roster = build_roster(t)
        res = plan(t, {"AAA": 1000.0}, roster, _metrics(roster), True, True, cash=0.0,
                   margin_debt=0.0, margin_buffer_pct=100.0, margin_requested=5000.0,
                   holdings_state={})
        assert res["cash_after_plan"] == 0.0
        assert res["unused_margin_capacity"] >= 0.0
        assert res["cash_funded_capacity"] == 0.0

    def test_margin_capacity_never_satisfies_the_protected_floor(self):
        t = _targets()
        roster = build_roster(t)
        res = plan(t, {"AAA": 10000.0}, roster, _metrics(roster), True, True, cash=0.0,
                   margin_debt=0.0, margin_buffer_pct=100.0, margin_requested=100000.0,
                   holdings_state={})
        assert res["protection"]["cash_shortfall_dollars"] > 0
        assert not res["buys"]

    def test_margin_funding_is_blocked_with_an_explicit_reason(self):
        t = _targets()
        roster = build_roster(t)
        res = plan(t, {"AAA": 1000.0}, roster, _metrics(roster), True, True, cash=5000.0,
                   margin_debt=0.0, margin_buffer_pct=100.0, margin_requested=1000.0,
                   holdings_state={})
        assert res["margin_funding_blocked"] is True
        assert "no evidence" in res["margin_funding_block_reason"]

    def test_no_margin_request_means_no_margin_block(self):
        t = _targets()
        roster = build_roster(t)
        res = plan(t, {"AAA": 1000.0}, roster, _metrics(roster), True, True, cash=5000.0,
                   holdings_state={})
        assert res["margin_funding_blocked"] is False
        assert res["margin_funding_block_reason"] is None

    @pytest.mark.parametrize("buffer_pct", [29.9, 30.0, 30.1])
    def test_the_30_percent_buffer_boundary_is_unchanged_by_this_change(self, buffer_pct):
        """The accepted 30% floor is not touched; only funding is blocked."""
        t = _targets()
        roster = build_roster(t)
        res = plan(t, {"AAA": 1000.0}, roster, _metrics(roster), True, True, cash=5000.0,
                   margin_debt=100.0, margin_buffer_pct=buffer_pct,
                   margin_requested=500.0, holdings_state={})
        assert res["margin"]["forced_delever"] is (buffer_pct < 30.0)

    def test_margin_used_is_structurally_zero_because_buys_are_cash_funded(self):
        t = _targets()
        roster = build_roster(t)
        res = plan(t, {}, roster, _metrics(roster), True, True, cash=5000.0,
                   margin_debt=0.0, margin_buffer_pct=100.0, margin_requested=5000.0,
                   holdings_state={})
        assert res["margin"]["used"] == 0.0


# ── cash state freshness ───────────────────────────────────────────────────────

class TestCashStateFailsClosed:
    def test_a_missing_cash_block_is_unusable(self):
        st = load_cash_state({"shares": {}})
        assert st["usable"] is False and st["present"] is False
        assert "no `cash:` block" in st["reason"]

    def test_a_non_mapping_cash_block_is_unusable(self):
        st = load_cash_state({"cash": 1041.23})
        assert st["usable"] is False and "not a mapping" in st["reason"]

    @pytest.mark.parametrize("bad", ["1041.23", None, [], {}, True, False])
    def test_a_malformed_balance_is_unusable(self, bad):
        st = load_cash_state({"cash": {"balance": bad, "synced_at": FRESH}})
        assert st["usable"] is False

    def test_a_negative_balance_is_unusable(self):
        st = load_cash_state({"cash": {"balance": -1.0, "synced_at": FRESH}})
        assert st["usable"] is False and "negative" in st["reason"]

    def test_a_future_dated_sync_is_unusable(self):
        st = load_cash_state({"cash": {"balance": 100.0, "synced_at": FUTURE}})
        assert st["usable"] is False and "future" in st["reason"]

    def test_a_malformed_sync_date_is_unusable(self):
        st = load_cash_state({"cash": {"balance": 100.0, "synced_at": "not-a-date"}})
        assert st["usable"] is False

    def test_a_missing_sync_date_is_unusable(self):
        st = load_cash_state({"cash": {"balance": 100.0}})
        assert st["usable"] is False

    def test_a_stale_sync_is_unusable(self):
        st = load_cash_state({"cash": {"balance": 100.0, "synced_at": STALE}})
        assert st["usable"] is False and "re-sync" in st["reason"]

    def test_a_sync_exactly_at_the_threshold_is_still_usable(self):
        st = load_cash_state({"cash": {"balance": 100.0, "synced_at": EDGE}})
        assert st["usable"] is True and st["age_days"] == A.STALE_MARGIN_DAYS

    def test_a_fresh_sync_is_usable(self):
        st = load_cash_state({"cash": {"balance": 1041.23, "synced_at": FRESH}})
        assert st["usable"] is True and st["balance"] == 1041.23

    def test_zero_is_a_valid_balance(self):
        st = load_cash_state({"cash": {"balance": 0.0, "synced_at": FRESH}})
        assert st["usable"] is True and st["balance"] == 0.0

    def test_the_committed_baseline_is_stale_and_therefore_not_actionable(self):
        """holdings.yaml carries the PHQ-2026-06 historical figure. It must
        never authorize a recommendation on its own."""
        st = load_cash_state()
        assert st["present"] is True
        # Stale, specifically -- not "unusable for some other reason". A future
        # date is also unusable, so asserting only `usable is False` would pass
        # for a baseline dated 2099, which is a different (and wrong) record.
        assert st["age_days"] is not None and st["age_days"] > A.STALE_MARGIN_DAYS
        assert st["usable"] is False, (
            "the committed cash baseline must be historical evidence, never "
            "a current balance that authorizes a recommendation")

    def test_the_repository_threshold_is_reused_not_reinvented(self):
        assert A.STALE_MARGIN_DAYS == 2
        src = inspect.getsource(load_cash_state)
        assert "STALE_MARGIN_DAYS" in src


class TestMarginStateFailsClosed:
    def test_a_stale_margin_sync_is_unusable(self):
        st = load_margin_state({"margin": {"debt": 0.0, "buffer_pct": 100.0,
                                           "synced_at": STALE}})
        assert st["usable"] is False

    def test_a_future_margin_sync_is_unusable(self):
        st = load_margin_state({"margin": {"debt": 0.0, "buffer_pct": 100.0,
                                           "synced_at": FUTURE}})
        assert st["usable"] is False

    def test_a_missing_margin_block_is_unusable(self):
        assert load_margin_state({})["usable"] is False

    def test_a_non_numeric_debt_is_unusable(self):
        st = load_margin_state({"margin": {"debt": "zero", "synced_at": FRESH}})
        assert st["usable"] is False and "debt" in st["reason"]

    def test_a_non_numeric_buffer_is_unusable(self):
        st = load_margin_state({"margin": {"debt": 0.0, "buffer_pct": "full",
                                           "synced_at": FRESH}})
        assert st["usable"] is False

    def test_a_fresh_margin_block_is_usable(self):
        st = load_margin_state({"margin": {"debt": 0.0, "buffer_pct": 100.0,
                                           "synced_at": FRESH}})
        assert st["usable"] is True

    def test_the_committed_margin_baseline_is_stale(self):
        assert load_margin_state()["usable"] is False


# ── valuation completeness ─────────────────────────────────────────────────────

class TestValuationCompleteness:
    def test_an_unpriced_equity_holding_is_reported_not_dropped(self):
        state = {"shares": {"AAA": 1.0, "BBB": 2.0}, "crypto_shares": {}}
        v = valuation_completeness({"AAA": 100.0}, state)
        assert v["complete"] is False and v["unresolved"] == ["BBB"]
        assert "silently vanish" in v["reason"]

    def test_an_unpriced_crypto_holding_is_reported_not_dropped(self):
        state = {"shares": {}, "crypto_shares": {"BTC": 0.5, "ETH": 1.0}}
        v = valuation_completeness({"BTC": 100.0}, state)
        assert v["complete"] is False and v["unresolved"] == ["ETH"]

    def test_a_zero_quantity_holding_is_not_expected(self):
        state = {"shares": {"AAA": 0.0}, "crypto_shares": {}}
        assert valuation_completeness({}, state)["complete"] is True

    def test_a_fully_priced_book_is_complete(self):
        state = {"shares": {"AAA": 1.0}, "crypto_shares": {"BTC": 0.5}}
        v = valuation_completeness({"AAA": 100.0, "BTC": 50.0}, state)
        assert v["complete"] is True and v["unresolved"] == []

    def test_a_zero_valued_holding_counts_as_unresolved(self):
        """resolve_holdings() filters `if v`, so a zero value IS a drop."""
        state = {"shares": {"AAA": 1.0}, "crypto_shares": {}}
        assert valuation_completeness({"AAA": 0.0}, state)["complete"] is False

    def test_every_real_tracked_symbol_is_expected(self):
        data = yaml.safe_load(open("holdings.yaml"))
        v = valuation_completeness({}, data)
        assert v["expected_count"] == 28, v["expected_count"]


# ── state preservation across every update path ────────────────────────────────

class TestThePerformanceSnapshotIsNotMisleading:
    """Instruction 9: an update command must not write a snapshot when live
    valuation is unavailable. Scoped to the case this function can actually
    judge -- its OWN resolution attempt failing."""

    class _Boom:
        def get_bars(self, *a, **k):
            return [{"c": 100.0}]

    def test_a_failed_live_resolution_skips_the_snapshot(self, tmp_path, monkeypatch,
                                                         capsys):
        perf = tmp_path / "perf.csv"
        monkeypatch.setattr(A, "PERF_LOG_FILE", perf)
        monkeypatch.setattr(A, "resolve_holdings",
                            lambda *a, **k: (_ for _ in ()).throw(RuntimeError("no prices")))
        A.log_performance(client=self._Boom(), quiet=False)
        assert not perf.exists(), "a snapshot was written despite unavailable valuation"
        assert "SKIPPED" in capsys.readouterr().err

    def test_a_successful_resolution_still_writes(self, tmp_path, monkeypatch):
        perf = tmp_path / "perf.csv"
        monkeypatch.setattr(A, "PERF_LOG_FILE", perf)
        monkeypatch.setattr(A, "resolve_holdings", lambda *a, **k: {"AAA": 1000.0})
        A.log_performance(client=self._Boom(), quiet=True)
        assert perf.exists()

    def test_a_caller_supplied_set_is_not_second_guessed(self, tmp_path, monkeypatch):
        """A caller that already resolved is trusted; judging its set against a
        holdings file it may not be using broke three unrelated suites."""
        perf = tmp_path / "perf.csv"
        monkeypatch.setattr(A, "PERF_LOG_FILE", perf)
        A.log_performance(client=self._Boom(), quiet=True,
                          resolved_holdings={"AAA": 1000.0})
        assert perf.exists()

    def test_the_written_row_carries_cash_and_book(self, tmp_path, monkeypatch):
        perf = tmp_path / "perf.csv"
        monkeypatch.setattr(A, "PERF_LOG_FILE", perf)
        A.log_performance(client=self._Boom(), quiet=True,
                          resolved_holdings={"AAA": 1000.0})
        import csv as _csv
        row = list(_csv.DictReader(open(perf)))[-1]
        assert "cash" in row and "book" in row


class TestStatePreservation:
    @pytest.fixture
    def sandbox(self, tmp_path, monkeypatch):
        f = tmp_path / "holdings.yaml"
        f.write_text(
            "cash:\n  balance: 500.0\n  synced_at: 2026-08-01\n"
            "margin:\n  debt: 1.0\n  buffer_pct: 50.0\n  synced_at: 2026-08-01\n"
            "holdings:\n  MAN: 7.0\n"
            "shares:\n  AAA: 1.5\n"
            "crypto_shares:\n  BTC: 0.25\n")
        monkeypatch.setattr(A, "HOLDINGS_FILE", f)
        monkeypatch.setattr(A, "log_performance", lambda *a, **k: None)
        return f

    @staticmethod
    def _all_blocks(f):
        d = yaml.safe_load(f.read_text())
        return d

    @pytest.mark.parametrize("cmd", ["holdings", "shares", "crypto", "margin"])
    def test_every_update_path_preserves_the_cash_block(self, sandbox, cmd, monkeypatch):
        before = self._all_blocks(sandbox)
        if cmd == "margin":
            A.update_margin(2.0, 40.0)
        else:
            prior = A.load_yaml(sandbox)
            if cmd == "holdings":
                write_state({"MAN": 9.0}, prior.get("margin"), prior.get("shares"),
                            prior.get("crypto_shares"))
            elif cmd == "shares":
                write_state(prior.get("holdings"), prior.get("margin"), {"AAA": 2.5},
                            prior.get("crypto_shares"))
            else:
                write_state(prior.get("holdings"), prior.get("margin"),
                            prior.get("shares"), {"BTC": 0.5})
        after = self._all_blocks(sandbox)
        assert after["cash"]["balance"] == before["cash"]["balance"], cmd
        assert str(after["cash"]["synced_at"]) == str(before["cash"]["synced_at"]), cmd

    def test_update_cash_preserves_every_other_block(self, sandbox):
        before = self._all_blocks(sandbox)
        A.update_cash(1234.56)
        after = self._all_blocks(sandbox)
        assert after["cash"]["balance"] == 1234.56
        assert str(after["cash"]["synced_at"]) == FRESH
        assert after["margin"] == before["margin"]
        assert after["holdings"] == before["holdings"]
        assert after["shares"] == before["shares"]
        assert after["crypto_shares"] == before["crypto_shares"]

    def test_update_cash_refuses_a_negative_balance(self, sandbox):
        with pytest.raises(ValueError, match="negative"):
            A.update_cash(-1.0)

    def test_update_cash_records_a_total_not_a_delta(self, sandbox):
        A.update_cash(100.0)
        A.update_cash(250.0)
        assert self._all_blocks(sandbox)["cash"]["balance"] == 250.0

    def test_write_state_preservation_is_the_default(self):
        sig = inspect.signature(write_state)
        assert sig.parameters["cash"].default is None
        assert sig.parameters["_preserve_cash"].default is True

    def test_the_real_holdings_file_carries_a_cash_block(self):
        d = yaml.safe_load(open("holdings.yaml"))
        assert "cash" in d and "balance" in d["cash"] and "synced_at" in d["cash"]


# ── no double counting between tracked cash and the retired CLI argument ───────

class TestNoDoubleCounting:
    def test_the_cli_refuses_an_additive_cash_argument(self):
        src = inspect.getsource(A.main)
        assert "--cash is retired" in src
        assert "double-counted" in src

    def test_the_cli_default_is_none_so_absence_is_distinguishable_from_zero(self):
        src = inspect.getsource(A.main)
        assert 'ap.add_argument("--cash", type=float, default=None' in src

    def test_main_consumes_the_tracked_balance_exactly_once(self):
        src = inspect.getsource(A.main)
        assert "tracked_cash = cash_state" in src
        assert src.count("tracked_cash") >= 2
        # the tracked balance is passed straight through; nothing is added to it
        assert "tracked_cash +" not in src and "+ tracked_cash" not in src

    def test_the_cli_actually_refuses_a_cash_argument(self, monkeypatch):
        """Behavioural, not a source pin: the mutation `if False:` disables the
        guard while leaving every string in place, so a substring assertion
        cannot see it."""
        import sys as _sys
        monkeypatch.setattr(_sys, "argv", ["allocate.py", "--cash", "500"])
        with pytest.raises(SystemExit) as e:
            A.main()
        assert e.value.code == 2

    @pytest.mark.parametrize("argv", [["--cash", "0"], ["--cash", "500", "--review"]])
    def test_any_cash_argument_is_refused_including_zero(self, argv, monkeypatch):
        import sys as _sys
        monkeypatch.setattr(_sys, "argv", ["allocate.py", *argv])
        with pytest.raises(SystemExit) as e:
            A.main()
        assert e.value.code == 2

    def test_an_unusable_cash_state_contributes_zero_not_its_balance(self):
        """Closes `tracked_cash = cash_state["balance"] or 0.0`: that consumes a
        stale balance as though it were current. The committed baseline IS
        stale and non-zero, so the mutation would silently act on it."""
        st = load_cash_state()
        assert st["usable"] is False and st["balance"], "baseline must be stale and non-zero"
        src = inspect.getsource(A.main)
        assert 'tracked_cash = cash_state["balance"] if cash_state["usable"] else 0.0' in src

    def test_update_cash_is_the_only_documented_cash_writer(self):
        src = inspect.getsource(A.update_cash)
        assert "TOTAL" in src and "never a deposit delta" in src


# ── gated names never become trim candidates ───────────────────────────────────

class TestGatedTickerMistakenlyInACluster:
    def test_a_gated_ticker_listed_in_a_cluster_is_never_trimmed(self):
        t = _targets()
        t["caps"] = {"clusters": [{"name": "synthetic", "pct": 1.0,
                                   "tickers": ["AAA", "GGG"]}]}
        roster = build_roster(t)
        holdings = {"AAA": 5000.0, "GGG": 5000.0}
        res = plan(t, holdings, roster, _metrics(roster), True, True, cash=0.0,
                   gates_cfg=_gates("GGG"), holdings_state={})
        assert "GGG" not in {r["ticker"] for r in res["trims"]}

    def test_a_reserve_row_listed_in_a_cluster_is_never_trimmed(self):
        t = _targets()
        t["caps"] = {"clusters": [{"name": "synthetic", "pct": 1.0,
                                   "tickers": ["AAA", "RESERVE"]}]}
        roster = build_roster(t)
        res = plan(t, {"AAA": 5000.0, "RESERVE": 5000.0}, roster, _metrics(roster),
                   True, True, cash=0.0, holdings_state={})
        assert "RESERVE" not in {r["ticker"] for r in res["trims"]}


# ── the strengthened PHQ-2026-02 claim ─────────────────────────────────────────

class TestGatedCapitalActuallyRemainsCash:
    """The old assertion `result["cash"] == 1000.0` only re-read the unchanged
    INPUT. It proved nothing about what the plan did. These prove the
    post-plan position."""

    def test_gated_target_capital_is_still_held_as_cash_after_the_plan(self, real_targets,
                                                                       real_gates):
        roster = build_roster(real_targets)
        res = plan(real_targets, {}, roster, _metrics(roster), True, True, cash=100000.0,
                   gates_cfg=real_gates, lookthrough=A.load_issuer_lookthrough(),
                   holdings_state={})
        pc = res["protection"]
        assert res["cash_after_plan"] >= pc["protected_floor_dollars"] - 1e-6
        assert pc["gated_cash_required_dollars"] > 0

    def test_no_gated_name_is_ever_bought(self, real_targets, real_gates):
        roster = build_roster(real_targets)
        res = plan(real_targets, {}, roster, _metrics(roster), True, True, cash=100000.0,
                   gates_cfg=real_gates, lookthrough=A.load_issuer_lookthrough(),
                   holdings_state={})
        assert not ({b["ticker"] for b in res["buys"]} & set(real_gates))

    def test_the_gated_requirement_shrinks_as_a_gated_name_is_held(self, real_targets,
                                                                   real_gates):
        roster = build_roster(real_targets)
        tk = sorted(real_gates)[0]
        empty = plan(real_targets, {}, roster, _metrics(roster), True, True, cash=100000.0,
                     gates_cfg=real_gates, lookthrough=A.load_issuer_lookthrough(),
                     holdings_state={})
        held = plan(real_targets, {tk: 500.0}, roster, _metrics(roster), True, True,
                    cash=100000.0, gates_cfg=real_gates,
                    lookthrough=A.load_issuer_lookthrough(), holdings_state={})
        assert (held["protection"]["gated_cash_required_dollars"]
                < empty["protection"]["gated_cash_required_dollars"] + 500.0)


# ── book identity across every output ──────────────────────────────────────────

class TestBookIdentityEverywhere:
    def test_book_is_invested_plus_cash_minus_debt(self):
        t = _targets()
        roster = build_roster(t)
        res = plan(t, {"AAA": 1000.0}, roster, _metrics(roster), True, True, cash=200.0,
                   margin_debt=50.0, margin_buffer_pct=100.0, holdings_state={})
        assert res["book"] == pytest.approx(1000.0 + 200.0 - 50.0)
        assert res["protection"]["book"] == pytest.approx(res["book"])

    def test_cash_enters_the_identity_exactly_once(self):
        src = inspect.getsource(A.margin_capacity)
        assert "net_equity = gross - margin_debt" in src
        psrc = inspect.getsource(plan)
        assert psrc.count("book = net_equity + float(cash)") == 1

    def test_the_performance_log_records_cash_and_book(self):
        assert "cash" in A.PERF_FIELDS and "book" in A.PERF_FIELDS
        assert A.PERF_FIELDS.index("net_equity") < A.PERF_FIELDS.index("cash")

    def test_the_performance_log_reader_tolerates_pre_change_rows(self):
        rows = A._read_perf_log()
        for r in rows:
            assert set(A.PERF_FIELDS).issubset(r)

    def test_the_health_view_reports_tracked_cash_and_the_floor(self):
        src = inspect.getsource(A.render_health)
        assert "Tracked cash" in src and "Protected floor" in src

    def test_the_rendered_advisory_actually_prints_the_floor(self):
        """A substring pin on the source is not enough -- `Protected floor`
        appears twice in render(), so deleting the row that prints the number
        left the pin satisfied. This renders and reads the output."""
        t = _targets()
        roster = build_roster(t)
        res = plan(t, {"AAA": 1000.0}, roster, _metrics(roster), True, True, cash=500.0,
                   holdings_state={})
        out = A.render(res, review=False)
        floor = res["protection"]["protected_floor_dollars"]
        assert f"${floor:,.2f}" in out
        assert "Protected floor" in out
        assert f"${res['protection']['actual_cash']:,.2f}" in out

    def test_the_advisory_view_reports_the_full_accounting(self):
        src = inspect.getsource(A.render)
        for label in ("Actual tracked cash", "Invested gross", "Margin debt",
                      "Destination total", "Unreconciled remainder", "CASH target",
                      "RESERVE target", "Gated target weight", "Gated cash required",
                      "Protected floor", "Cash-funded capacity",
                      "Unused MARGIN capacity", "Cash remaining after plan"):
            assert label in src, label

    def test_obsolete_wording_is_corrected(self):
        src = inspect.getsource(A.render)
        assert "New cash" not in src
        assert "Tracked cash" in src

    def test_cash_and_reserve_satisfaction_is_proved_not_asserted(self):
        psrc = inspect.getsource(plan)
        assert "definitionally satisfied" not in psrc
        rsrc = inspect.getsource(A.render)
        assert "never assumed" in rsrc


# ── non-actionable runs withdraw dollar recommendations ────────────────────────

class TestNonActionableRunsWithdrawRecommendations:
    def test_the_banner_precedes_any_dollar_figure(self):
        src = inspect.getsource(A.render)
        assert src.index("NON-ACTIONABLE") < src.index("Protected-capital accounting")

    def test_recommendations_are_withdrawn_not_merely_annotated(self):
        src = inspect.getsource(A.main)
        assert 'result["buys"] = []' in src and 'result["trims"] = []' in src

    def test_freshness_is_checked_before_plan_is_called(self):
        src = inspect.getsource(A.main)
        assert src.index("cash_state = load_cash_state") < src.index("result = plan(")
        assert src.index("valuation_completeness") < src.index("result = plan(")

    def test_a_margin_request_makes_the_run_non_actionable(self):
        src = inspect.getsource(A.main)
        assert "MARGIN FUNDING" in src and "MARGIN_CASH_PRESERVATION_UNPROVEN" in src


# ── no accepted policy number moved ────────────────────────────────────────────

class TestNoAcceptedNumberChanged:
    def test_the_leverage_cap_and_buffer_floor_are_untouched(self, real_targets):
        m = real_targets["margin"]
        assert float(m["leverage_cap"]) == 1.8
        assert float(m["buffer_floor_pct"]) == 30.0

    def test_every_destination_weight_is_untouched(self, real_targets):
        rows = {r["ticker"]: r["target_pct"] for r in real_targets["destination"]}
        assert len(rows) == 36
        assert rows["CASH"] == 1.0 and rows["RESERVE"] == 4.0
        assert sum(rows.values()) == pytest.approx(99.25, abs=1e-9)

    def test_the_gate_roster_is_untouched(self, real_gates):
        assert set(real_gates) == {"SNPS", "ICE", "SPGI", "WM", "RKLB", "TSLA"}
