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

import ast
import copy
import datetime
import inspect
import pathlib
import re

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
        used instead -- otherwise this would assert nothing.

        VERSION-INDEPENDENT (PHQ-2026-07). The superseded fixture guarded itself with
        ``sum(...) != 1.0``. CPython 3.12 gave the BUILTIN ``sum()`` Neumaier
        compensation, so it returns exactly 1.0 there and that guard failed -- on an
        interpreter ``requirements.txt`` explicitly supports (>=3.10). The drift being
        demonstrated is real; only the way it was elicited was interpreter-specific.
        An explicit accumulation loop is naive in EVERY version, because the
        compensation was added to ``sum()`` and not to ``+=``, so it shows the same
        drift on 3.10, 3.11 and 3.12 alike. The production assertions below are
        unchanged.
        """
        exact = destination_reconciliation(real_targets)["destination_total_pct"]
        assert exact == 99.25

        rows = [{"ticker": f"T{i}", "target_pct": 0.1, "asset_class": "equity"}
                for i in range(10)]
        naive = 0.0
        for r in rows:                      # NOT builtin sum(): see the docstring
            naive += r["target_pct"]
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
        assert st["usable"] is False
        assert st["state"] == A.STATE_UNKNOWN          # out of domain is UNKNOWN, not stale
        assert st["balance"] is None                   # and carries no number forward
        assert "minimum" in st["reason"] and "-1.0" in st["reason"]

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

    @staticmethod
    def _state(tmp_path, monkeypatch, *, cash_synced=FRESH, margin_synced=FRESH,
               balance=500.0, debt=0.0):
        """A controlled holdings.yaml, so these tests describe the WRITER's behaviour
        rather than whatever the committed baseline's freshness happens to be."""
        f = tmp_path / "holdings.yaml"
        body = {"shares": {"AAA": 10.0},
                "margin": {"debt": debt, "buffer_pct": 60.0, "synced_at": margin_synced}}
        if balance is not None:
            body["cash"] = {"balance": balance, "synced_at": cash_synced}
        f.write_text(yaml.safe_dump(body))
        monkeypatch.setattr(A, "HOLDINGS_FILE", f)
        return f

    def test_a_successful_resolution_still_writes(self, tmp_path, monkeypatch):
        perf = tmp_path / "perf.csv"
        monkeypatch.setattr(A, "PERF_LOG_FILE", perf)
        self._state(tmp_path, monkeypatch)
        monkeypatch.setattr(A, "resolve_holdings", lambda *a, **k: {"AAA": 1000.0})
        A.log_performance(client=self._Boom(), quiet=True)
        assert perf.exists()

    def test_a_caller_supplied_set_is_not_second_guessed(self, tmp_path, monkeypatch):
        """A caller that already resolved is trusted; judging its set against a
        holdings file it may not be using broke three unrelated suites."""
        perf = tmp_path / "perf.csv"
        monkeypatch.setattr(A, "PERF_LOG_FILE", perf)
        self._state(tmp_path, monkeypatch)
        A.log_performance(client=self._Boom(), quiet=True,
                          resolved_holdings={"AAA": 1000.0})
        assert perf.exists()

    def test_the_written_row_carries_cash_and_book(self, tmp_path, monkeypatch):
        perf = tmp_path / "perf.csv"
        monkeypatch.setattr(A, "PERF_LOG_FILE", perf)
        self._state(tmp_path, monkeypatch, balance=500.0, debt=100.0)
        A.log_performance(client=self._Boom(), quiet=True,
                          resolved_holdings={"AAA": 1000.0})
        import csv as _csv
        row = list(_csv.DictReader(open(perf)))[-1]
        assert "cash" in row and "book" in row
        # book = invested + cash - debt, cash counted exactly once.
        assert float(row["cash"]) == 500.0
        assert float(row["book"]) == 1000.0 + 500.0 - 100.0

    # ---- PHQ-2026-07 item 8: a row may never record stale or unknown state ----

    def test_a_STALE_cash_observation_is_never_written_as_current(self, tmp_path,
                                                                  monkeypatch, capsys):
        """The defect this closes: log_performance gated on ``balance is not None``,
        which is true for a stale reading too, so a 30-day-old balance would be
        recorded in TODAY's row as though it were today's."""
        perf = tmp_path / "perf.csv"
        monkeypatch.setattr(A, "PERF_LOG_FILE", perf)
        self._state(tmp_path, monkeypatch, cash_synced=STALE, balance=1041.23)
        A.log_performance(client=self._Boom(), quiet=True,
                          resolved_holdings={"AAA": 1000.0})
        import csv as _csv
        row = list(_csv.DictReader(open(perf)))[-1]
        assert row["cash"] == "" and row["book"] == ""      # blank, never the stale number
        assert "1041" not in open(perf).read()

    def test_an_UNKNOWN_cash_observation_is_never_written_as_zero(self, tmp_path, monkeypatch):
        perf = tmp_path / "perf.csv"
        monkeypatch.setattr(A, "PERF_LOG_FILE", perf)
        self._state(tmp_path, monkeypatch, balance=None)    # no cash block at all
        A.log_performance(client=self._Boom(), quiet=True,
                          resolved_holdings={"AAA": 1000.0})
        import csv as _csv
        row = list(_csv.DictReader(open(perf)))[-1]
        assert row["cash"] == "" and row["book"] == ""      # blank, never "0.0"

    def test_an_UNUSABLE_margin_state_writes_no_row_at_all(self, tmp_path, monkeypatch, capsys):
        """Margin debt is part of the book identity, so a stale or out-of-domain debt
        would corrupt net_equity in a RECORDED data point. Fail closed instead."""
        perf = tmp_path / "perf.csv"
        monkeypatch.setattr(A, "PERF_LOG_FILE", perf)
        self._state(tmp_path, monkeypatch, margin_synced=STALE)
        A.log_performance(client=self._Boom(), quiet=False,
                          resolved_holdings={"AAA": 1000.0})
        assert not perf.exists()
        assert "SKIPPED" in capsys.readouterr().err

    def test_a_NEGATIVE_margin_debt_writes_no_row_at_all(self, tmp_path, monkeypatch):
        """`gross - (-debt)` ADDS capital; recording that would inflate the series."""
        perf = tmp_path / "perf.csv"
        monkeypatch.setattr(A, "PERF_LOG_FILE", perf)
        self._state(tmp_path, monkeypatch, debt=-5000.0)
        A.log_performance(client=self._Boom(), quiet=True,
                          resolved_holdings={"AAA": 1000.0})
        assert not perf.exists()


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
        with pytest.raises(ValueError, match="below its accepted minimum"):
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

    def test_an_unusable_cash_state_contributes_NOTHING_and_no_zero_is_substituted(self):
        """CORRECTED under PHQ-2026-07 item 4.

        This test previously PINNED the zero-substitution it was meant to guard against:
        it required main() to contain ``... if cash_state["usable"] else 0.0``. Consuming
        a stale balance as current is one defect; fabricating a zero and then rendering it
        as ``Actual tracked cash`` is another, and the old pin enforced the second while
        closing the first. Both are closed now: the state is passed as None.
        """
        st = load_cash_state()
        assert st["usable"] is False and st["balance"], "baseline must be stale and non-zero"
        src = inspect.getsource(A.main)
        assert 'tracked_cash = cash_state["balance"] if cash_state["usable"] else None' in src
        assert "else 0.0" not in src.split("tracked_cash")[1].split("\n")[0]
        # And behaviourally, end to end: no dollar figure is derived from the unknown.
        t = _targets()
        roster = build_roster(t)
        r = plan(t, {"AAA": 1000.0}, roster, _metrics(roster), True, True, None,
                 holdings_state={"shares": {"AAA": 10.0}})
        assert r["dollars_available"] is False
        assert r["book"] is None and r["cash"] is None and r["cash_after_plan"] is None
        assert r["protection"]["protected_floor_dollars"] is None
        assert r["cash_spent"] == 0.0 and r["buys"] == []

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
        # CORRECTED: the addend is now `cash_value`, which is the tracked balance when
        # the observation is current and is never consumed at all when it is not.
        assert psrc.count("book = net_equity + cash_value") == 1
        assert psrc.count("cash_value = float(cash) if cash is not None else 0.0") == 1
        # Intent unchanged: after removing the ONE legitimate assignment, no other
        # `float(cash)` may remain -- cash is converted in exactly one place.
        assert "float(cash)" not in psrc.replace(
            "cash_value = float(cash) if cash is not None", "")

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


# ══════════════════════════════════════════════════════════════════════════════
# PHQ-2026-07 corrections — adversarial coverage for the findings the independent
# FULL review raised at head bb6701b (BLOCKING 1/2, MAJOR 1/2/3).
# ══════════════════════════════════════════════════════════════════════════════

#: Every shape a persisted numeric scalar must be REJECTED in. Each is its own
#: distinct failure mode, so each is listed separately rather than folded into a
#: single "bad input" case that one fix could accidentally satisfy.
BAD_SCALARS = [
    ("negative", -1.0),
    ("nan", float("nan")),
    ("posinf", float("inf")),
    ("neginf", float("-inf")),
    ("true", True),
    ("false", False),
    ("string", "500"),
    ("none", None),
    ("list", [500.0]),
]
#: Controls. If these ever stop being ACCEPTED the checks above have gone from
#: fail-closed to fail-shut and are no longer measuring what they claim to.
GOOD_SCALARS = [("zero", 0.0), ("int", 500), ("float", 1041.23), ("tiny", 0.01)]


class TestNumericDomainsFailClosed:
    """MAJOR 2. `float()` alone admits NaN and +Infinity, and `bool` is an `int`."""

    @pytest.mark.parametrize("label,value", BAD_SCALARS, ids=[b[0] for b in BAD_SCALARS])
    def test_cash_balance_rejects(self, label, value):
        st = load_cash_state({"cash": {"balance": value, "synced_at": FRESH}})
        assert st["usable"] is False, label
        assert st["state"] == A.STATE_UNKNOWN, label
        assert st["balance"] is None, label
        assert st["reason"], label

    @pytest.mark.parametrize("label,value", GOOD_SCALARS, ids=[g[0] for g in GOOD_SCALARS])
    def test_cash_balance_accepts_valid_values(self, label, value):
        st = load_cash_state({"cash": {"balance": value, "synced_at": FRESH}})
        assert st["usable"] is True, label
        assert st["state"] == A.STATE_CURRENT, label
        assert st["balance"] == float(value), label

    @pytest.mark.parametrize("label,value", BAD_SCALARS, ids=[b[0] for b in BAD_SCALARS])
    def test_margin_debt_rejects(self, label, value):
        st = A.load_margin_state(
            {"margin": {"debt": value, "buffer_pct": 60.0, "synced_at": FRESH}})
        assert st["usable"] is False, label
        assert st["debt"] is None, label

    def test_a_negative_debt_cannot_inflate_net_equity(self):
        """The concrete harm: `gross - (-debt)` ADDS capital. Reject, never absorb."""
        st = A.load_margin_state(
            {"margin": {"debt": -5000.0, "buffer_pct": 60.0, "synced_at": FRESH}})
        assert st["usable"] is False and "minimum" in st["reason"]

    @pytest.mark.parametrize("value", [float("nan"), float("inf"), -0.1, 100.01, True])
    def test_margin_buffer_rejects_out_of_domain(self, value):
        st = A.load_margin_state(
            {"margin": {"debt": 0.0, "buffer_pct": value, "synced_at": FRESH}})
        assert st["usable"] is False

    @pytest.mark.parametrize("value", [0.0, 30.0, 60.0, 100.0])
    def test_margin_buffer_accepts_its_whole_valid_domain(self, value):
        st = A.load_margin_state(
            {"margin": {"debt": 0.0, "buffer_pct": value, "synced_at": FRESH}})
        assert st["usable"] is True and st["buffer_pct"] == value

    def test_a_nan_buffer_would_otherwise_pass_BOTH_sides_of_the_floor(self):
        """Why finiteness is not cosmetic: NaN satisfies neither `< 30` nor `>= 30`,
        so a NaN buffer slips through a floor check by failing to trip either branch."""
        nan = float("nan")
        assert not (nan < 30.0) and not (nan >= 30.0)
        st = A.load_margin_state(
            {"margin": {"debt": 0.0, "buffer_pct": nan, "synced_at": FRESH}})
        assert st["usable"] is False

    @pytest.mark.parametrize("text", ["balance: .nan", "balance: .inf", "balance: -.inf"])
    def test_yaml_serialised_non_finite_forms_are_rejected(self, text):
        """These are the forms that would actually appear on disk."""
        data = yaml.safe_load(f"cash:\n  {text}\n  synced_at: {FRESH}\n")
        st = load_cash_state(data)
        assert st["usable"] is False and st["balance"] is None

    def test_a_nan_holding_value_is_not_treated_as_resolved(self):
        """`bool(nan)` is True, so a NaN price would read as 'priced' and poison book."""
        vc = A.valuation_completeness({"AAA": float("nan")}, {"shares": {"AAA": 1.0}})
        assert vc["complete"] is False and vc["unresolved"] == ["AAA"]

    def test_a_real_price_is_still_resolved(self):
        vc = A.valuation_completeness({"AAA": 1000.0}, {"shares": {"AAA": 1.0}})
        assert vc["complete"] is True and vc["unresolved"] == []


class TestThreeStateObservation:
    """MAJOR 1. current / stale / unknown are distinct, and zero is none of them."""

    def test_current_stale_and_unknown_are_three_distinct_states(self):
        cur = load_cash_state({"cash": {"balance": 500.0, "synced_at": FRESH}})
        stale = load_cash_state({"cash": {"balance": 500.0, "synced_at": STALE}})
        unknown = load_cash_state({})
        assert (cur["state"], stale["state"], unknown["state"]) == (
            A.STATE_CURRENT, A.STATE_STALE, A.STATE_UNKNOWN)
        assert len({cur["state"], stale["state"], unknown["state"]}) == 3

    def test_a_stale_observation_keeps_its_value_and_its_date(self):
        """Stale is a real past fact. It is retained AS evidence -- and marked unusable."""
        st = load_cash_state({"cash": {"balance": 1041.23, "synced_at": STALE}})
        assert st["state"] == A.STATE_STALE
        assert st["balance"] == 1041.23 and st["synced_at"] == STALE
        assert st["usable"] is False

    def test_an_unknown_observation_carries_no_number_at_all(self):
        for data in ({}, {"cash": {"balance": "x", "synced_at": FRESH}},
                     {"cash": {"balance": 5.0, "synced_at": "not-a-date"}}):
            st = load_cash_state(data)
            assert st["state"] == A.STATE_UNKNOWN and st["balance"] is None

    def test_zero_is_a_real_observation_not_an_absence(self):
        """A genuine $0.00 balance is CURRENT and usable -- the point of the three-state
        model is that a fabricated zero and an observed zero are not the same thing."""
        st = load_cash_state({"cash": {"balance": 0.0, "synced_at": FRESH}})
        assert st["state"] == A.STATE_CURRENT and st["usable"] is True
        assert st["balance"] == 0.0

    def test_plan_withholds_every_dollar_figure_when_cash_is_not_current(self):
        t = _targets(); roster = build_roster(t)
        r = plan(t, {"AAA": 1000.0}, roster, _metrics(roster), True, True, None,
                 holdings_state={"shares": {"AAA": 10.0}})
        for key in ("book", "cash", "cash_left", "cash_after_plan"):
            assert r[key] is None, key
        p = r["protection"]
        assert p["cash_known"] is False
        for key in ("book", "actual_cash", "protected_floor_dollars",
                    "cash_shortfall_dollars", "cash_surplus_dollars",
                    "static_protected_dollars", "gated_cash_required_dollars"):
            assert p[key] is None, key
        # Percentages are config-derived and stay knowable in every state.
        assert p["static_protected_pct"] > 0 and p["unreconciled_pct"] >= 0

    def test_nothing_is_funded_while_cash_is_not_current(self):
        t = _targets(); roster = build_roster(t)
        r = plan(t, {"AAA": 1.0}, roster, _metrics(roster), True, True, None,
                 holdings_state={"shares": {"AAA": 10.0}})
        assert r["buys"] == [] and r["cash_spent"] == 0.0

    def test_the_render_never_labels_a_withheld_figure_actual(self):
        t = _targets(); roster = build_roster(t)
        r = plan(t, {"AAA": 1000.0}, roster, _metrics(roster), True, True, None,
                 holdings_state={"shares": {"AAA": 10.0}})
        r["cash_state"] = load_cash_state({"cash": {"balance": 1041.23, "synced_at": STALE}})
        r["actionable"] = False
        r["actionable_blocks"] = ["CASH STATE: stale"]
        out = A.render(r, review=True)
        assert "UNAVAILABLE" in out
        assert "Actual tracked cash | $0.00" not in out
        assert "$0.00" not in out.split("### Protected-capital")[1].split("|---|---:|")[1][:600]
        # The stale number may appear ONLY inside its own dated evidence disclaimer.
        for line in out.splitlines():
            if "1,041.23" in line:
                assert "Stale historical evidence" in line, line


    def test_the_no_funding_invariant_actually_fires_under_unknown_cash(self, monkeypatch):
        """The backstop assertion, exercised rather than merely present.

        ``deployable = surplus or 0.0`` already prevents spending while cash is
        unknown, so the ``assert cash_spent == 0.0`` guard behind it is unreachable in
        normal operation -- and an unreachable guard can be weakened without any test
        noticing. Here the upstream protection is deliberately made to LIE (a surplus
        reported while cash_known is False), so the backstop is the only thing left
        standing. Weakening it to ``>= 0.0`` makes this test pass silently, which is
        exactly the regression being pinned.
        """
        real = A.protected_capital

        def lying(*a, **k):
            out = real(*a, **k)
            if not out["cash_known"]:
                out = dict(out, cash_surplus_dollars=10_000.0)
            return out

        monkeypatch.setattr(A, "protected_capital", lying)
        t = _targets()
        roster = build_roster(t)
        with pytest.raises(AssertionError, match="stale or unknown"):
            # BBB carries the book so AAA is genuinely underweight by more than
            # one minimum lot; with a $1 book no candidate clears min_lot_dollars
            # and cash_spent would stay 0 for a reason unrelated to the guard.
            A.plan(t, {"BBB": 10_000.0}, roster, _metrics(roster), True, True, None,
                   holdings_state={"shares": {"BBB": 100.0}})

    def test_no_book_shaped_dollar_value_escapes_when_cash_is_unknown(self):
        """A speculative ``ranking_scale_dollars`` key was carrying net equity out of
        plan() under unknown cash -- unread, honestly named, and still exactly the
        "a number that looks like the book but is not the book" shape MAJOR 1 is about.
        Removed. This pins that no top-level key leaks that value again."""
        t = _targets(); roster = build_roster(t)
        gross = 1234.5
        r = plan(t, {"AAA": gross}, roster, _metrics(roster), True, True, None,
                 holdings_state={"shares": {"AAA": 10.0}})
        leaked = [k for k, v in r.items()
                  if isinstance(v, (int, float)) and not isinstance(v, bool)
                  and abs(float(v) - gross) < 1e-6]
        assert leaked == [], leaked
        assert "ranking_scale_dollars" not in r

    def test_a_current_run_still_reports_real_dollar_figures(self):
        """The complement: the withholding must not have broken the normal path."""
        t = _targets(); roster = build_roster(t)
        r = plan(t, {"AAA": 1000.0}, roster, _metrics(roster), True, True, 5000.0,
                 holdings_state={"shares": {"AAA": 10.0}})
        assert r["dollars_available"] is True
        assert r["book"] == 6000.0 and r["cash"] == 5000.0
        assert r["protection"]["protected_floor_dollars"] > 0
        assert r["cash_after_plan"] >= r["protection"]["protected_floor_dollars"] - 1e-6


class TestTheCliMigrationIsComplete:
    """MAJOR 3. The canonical `how` documentation must match the shipped interface."""

    def test_the_readme_documents_update_cash_and_not_the_retired_flag(self):
        readme = (pathlib.Path(__file__).parent / "README.md").read_text(encoding="utf-8")
        workflow = readme.split("## Allocation workflow")[1].split("\n## ")[0]
        assert "update-cash" in workflow
        assert "allocate.py --cash 2000" not in readme

    def test_every_command_the_readme_prescribes_is_a_real_command(self):
        """Behavioural, not textual: each documented invocation must actually parse."""
        readme = (pathlib.Path(__file__).parent / "README.md").read_text(encoding="utf-8")
        # Subcommands only -- flags are checked separately by argparse itself.
        prescribed = re.findall(r"python allocate\.py (?!--)([a-z][a-z-]+)", readme)
        known = {"update-cash", "update-shares", "update-crypto-shares",
                 "update-holdings", "update-margin", "log-performance",
                 "log-cashflow", "log-interest"}
        assert prescribed, "the README must actually prescribe commands"
        assert "update-cash" in prescribed
        for cmd in set(prescribed):
            assert cmd in known, cmd
        # And the flags it prescribes must all still parse.
        flags = set(re.findall(r"python allocate\.py (--[a-z-]+)", readme))
        assert flags, "the README must actually prescribe flags"
        assert "--cash" not in flags
        for flag in flags:
            assert flag in inspect.getsource(A.main), flag

    def test_the_dashboard_no_longer_instructs_the_retired_flag(self):
        src = (pathlib.Path(__file__).parent / "portfolio_hq" / "dashboard"
               / "render.py").read_text(encoding="utf-8")
        assert "--cash" not in src
        assert "update-cash" in src

    def test_the_module_usage_docstring_matches_the_shipped_interface(self):
        assert "--cash 2000" not in (A.__doc__ or "")
        assert "update-cash" in (A.__doc__ or "")

    def test_no_fabricated_cash_value_survives_argument_parsing(self):
        """`args.cash = 0.0` after the retirement check re-introduced the exact
        fabricated zero this correction exists to remove, even though inert."""
        src = inspect.getsource(A.main)
        assert "args.cash = 0.0" not in src

    def test_historical_evidence_that_mentions_the_flag_is_left_alone(self):
        """Accepted decisions record what was true when they were filed. Migrating an
        interface must never rewrite them."""
        root = pathlib.Path(__file__).parent
        for rel in ("governance/decisions/PHQ-2026-02-holdings-reconciliation-and-"
                    "actionable-allocation-policy.md",
                    "governance/decisions/OPS-0014-routine-operational-sync.md"):
            assert "--cash" in (root / rel).read_text(encoding="utf-8"), rel


class TestTheGoverningDecisionIsFiled:
    """BLOCKING 1. The Class-4 authority must exist, be accepted, and be catalogued."""

    DECISION_ID = "PHQ-2026-07"
    RELPATH = ("governance/decisions/PHQ-2026-07-protected-capital-accounting-"
               "and-persisted-cash.md")

    @pytest.fixture
    def decision(self):
        return (pathlib.Path(__file__).parent / self.RELPATH).read_text(encoding="utf-8")

    def test_the_decision_file_exists_and_is_accepted(self, decision):
        assert decision.startswith("---")
        front = decision.split("---")[1]
        assert f"decision_id: {self.DECISION_ID}" in front
        assert "status: Accepted" in front

    def test_the_catalog_lists_it_exactly_once_and_points_at_the_real_file(self):
        root = pathlib.Path(__file__).parent
        rows = yaml.safe_load((root / "governance/decisions.yaml").read_text())["decisions"]
        matches = [r for r in rows if r["decision_id"] == self.DECISION_ID]
        assert len(matches) == 1
        assert matches[0]["file"] == self.RELPATH
        assert (root / matches[0]["file"]).exists()

    @staticmethod
    def _flat(text: str) -> str:
        """Line-wrapped Markdown, flattened, so a phrase split across lines still matches."""
        return re.sub(r"\s+", " ", text.replace("**", "")).lower()

    def test_it_supersedes_prospectively_without_editing_history(self, decision):
        flat = self._flat(decision)
        assert "prospectively supersedes" in flat
        assert "are not edited" in flat

    def test_it_names_every_behaviour_this_pr_implements(self, decision):
        for clause in ("Cash source of truth", "Book identity", "Protected floor",
                       "State semantics", "Freshness", "Margin", "CLI",
                       "Performance logging", "Valuation completeness"):
            assert clause in decision, clause

    def test_it_hardcodes_no_policy_percentage(self, decision):
        """NUM-0001: governed percentages live in targets.yaml, not duplicated as an
        operative value here. Scoped to the OPERATIVE section -- the Alternatives
        section names 12.50% precisely to record that hardcoding it was REJECTED."""
        body = decision.split("## Decision")[1].split("## Rationale")[0]
        for pct in ("12.50%", "1.00%", "4.00%", "0.75%", "6.75%"):
            assert pct not in body, pct
        assert "derived at runtime from the current" in self._flat(body)
        assert "hardcode 12.50%" in self._flat(decision.split("## Alternatives")[1])

    def test_it_authorises_no_policy_number_change(self, decision):
        flat = self._flat(decision)
        assert "1.8x leverage cap and 30% buffer floor are untouched" in flat
        assert "no new margin-deployment policy" in flat
        # The closed list of things it explicitly does NOT authorise.
        for forbidden in ("holdings membership", "targets", "gates", "issuer limits",
                          "cluster caps", "stage-1 authority", "orders", "trades"):
            assert forbidden in flat, forbidden


# ── PHQ-2026-07 correction round 2 — independent FULL review 5079067543 ────────
# MAJOR 1: current-dollar availability was gated by CASH ALONE, so a stale margin
# reading or an unresolved tracked position still published a numeric book,
# protected floor, target dollars and gap dollars. MAJOR 2: the fail-closed
# numeric boundary guarded the READ path but not the WRITE path, not a missing
# buffer, not resolved values outside shares/crypto_shares, and not a
# caller-supplied performance set.


class TestCurrentDollarsRequireEveryRequiredState:
    """The three-dimensional availability matrix the review asked for.

    Each case makes exactly ONE required observation unusable and requires that NO
    current book-derived dollar escapes; the fourth is the positive control that
    proves the gate is fail-closed rather than fail-shut.
    """

    TODAY = datetime.date.today().isoformat()
    STALE = "2026-01-01"

    def _run(self, cash_synced, margin_synced, shares, resolved):
        data = {"shares": shares,
                "cash": {"balance": 1000.0, "synced_at": cash_synced},
                "margin": {"debt": 200.0, "buffer_pct": 60.0, "synced_at": margin_synced}}
        cs = A.load_cash_state(data)
        ms = A.load_margin_state(data)
        val = A.valuation_completeness(resolved, data)
        avail = A.current_dollar_availability(cs, ms, val)
        t = _targets()
        roster = build_roster(t)
        res = plan(t, resolved, roster, _metrics(roster), True, True,
                   cash=(cs["balance"] if cs["usable"] else None),
                   margin_debt=(ms["debt"] or 0.0),
                   margin_buffer_pct=(ms["buffer_pct"] or 0.0),
                   holdings_state=data, dollars_available=avail["available"])
        res["margin_state_check"] = ms
        res["cash_state"] = cs
        res["dollar_availability"] = avail
        res["margin"]["synced_at"] = margin_synced
        return res, avail

    #: The keys under which ``plan()`` ACTUALLY publishes per-name rows.
    #:
    #: The superseded helper scanned ``res["rows"]``. ``plan()`` has never emitted that
    #: key -- independent review reproduced the consequence: a gated row published
    #: ``target=560.0`` derived from an unavailable book while every assertion built on
    #: the helper passed, because it was iterating an empty default. These names are
    #: verified against the live return value below, so the list cannot silently rot
    #: the same way twice.
    ROW_KEYS = ("buys", "trims", "underweight", "blocked", "no_add_gated",
                "no_add_issuer", "no_add_common_driver")

    #: Per-row fields that are DERIVED FROM BOOK and therefore withheld with it.
    #: ``current`` is deliberately absent -- a position's own resolved value is not
    #: book-derived, and the availability fact already required it to be complete.
    ROW_DOLLAR_FIELDS = ("target", "gap", "amount", "trim_to", "headroom",
                         "max_by_name", "want", "pct_of_book")

    @classmethod
    def _escaped_dollars(cls, res):
        """Every current book-derived dollar the result could publish."""
        prot = res.get("protection") or {}
        candidates = [res.get("book"), res.get("cash"), res.get("cash_left"),
                      prot.get("book"), prot.get("actual_cash"),
                      prot.get("protected_floor_dollars"),
                      prot.get("cash_surplus_dollars"),
                      prot.get("cash_shortfall_dollars")]
        for key in cls.ROW_KEYS:
            for r in res.get(key) or []:
                if not isinstance(r, dict):
                    continue
                candidates += [r.get(f) for f in cls.ROW_DOLLAR_FIELDS]
        return [c for c in candidates if c is not None]

    def test_the_row_keys_this_suite_scans_are_the_ones_plan_actually_emits(self):
        """Positive control for the helper above -- the defect it exists to prevent.

        A helper that iterates a key the producer does not emit asserts nothing while
        reporting success. This pins the scanned names against a REAL result, so
        renaming or dropping a row collection fails here rather than silently
        hollowing every check that depends on it.
        """
        res, _ = self._run(self.TODAY, self.TODAY, {"AAA": 10.0}, {"AAA": 600.0})
        assert "rows" not in res, "plan() grew a 'rows' key; the helper must scan it"
        for key in self.ROW_KEYS:
            assert key in res, f"plan() no longer emits {key!r}"

        # Naming the right keys is not enough -- the helper must actually READ them.
        # Blank every TOP-LEVEL candidate, leaving only per-row dollars in place: a
        # helper iterating a key the producer does not emit now returns nothing, and
        # this fails. That is the exact defect the superseded version had.
        rows_only = dict(res)
        rows_only["book"] = rows_only["cash"] = rows_only["cash_left"] = None
        rows_only["protection"] = {}
        found = self._escaped_dollars(rows_only)
        assert found, (
            "the helper reported no per-row dollars from a fully available result -- "
            "it is not reading the collections plan() actually emits")

    def test_bad_cash_good_margin_complete_valuation_withholds_dollars(self):
        res, avail = self._run(self.STALE, self.TODAY, {"AAA": 10.0}, {"AAA": 600.0})
        assert avail["available"] is False
        assert res["dollars_available"] is False
        assert not self._escaped_dollars(res), self._escaped_dollars(res)

    def test_good_cash_bad_margin_complete_valuation_withholds_dollars(self):
        """The first case the review reproduced: book was $1,400 and the floor $280."""
        res, avail = self._run(self.TODAY, self.STALE, {"AAA": 10.0}, {"AAA": 600.0})
        assert avail["available"] is False, avail
        assert res["cash_state"]["usable"] is True, "cash itself must be current here"
        assert res["dollars_available"] is False
        assert not self._escaped_dollars(res), self._escaped_dollars(res)

    def test_good_cash_good_margin_incomplete_valuation_withholds_dollars(self):
        """The second case: BBB is tracked but unpriced, so gross is understated."""
        res, avail = self._run(self.TODAY, self.TODAY,
                               {"AAA": 10.0, "BBB": 5.0}, {"AAA": 600.0})
        assert avail["available"] is False, avail
        assert res["cash_state"]["usable"] is True
        assert res["dollars_available"] is False
        assert not self._escaped_dollars(res), self._escaped_dollars(res)

    def test_all_three_good_still_publishes_dollars(self):
        """POSITIVE CONTROL. The gate must be fail-closed, never fail-shut."""
        res, avail = self._run(self.TODAY, self.TODAY, {"AAA": 10.0}, {"AAA": 600.0})
        assert avail["available"] is True, avail
        assert res["dollars_available"] is True
        assert res["book"] is not None
        assert self._escaped_dollars(res), "the control published no dollars at all"

    def test_the_rendered_advisory_publishes_no_dollar_book_when_unavailable(self):
        for cash_s, margin_s, shares, resolved in [
            (self.STALE, self.TODAY, {"AAA": 10.0}, {"AAA": 600.0}),
            (self.TODAY, self.STALE, {"AAA": 10.0}, {"AAA": 600.0}),
            (self.TODAY, self.TODAY, {"AAA": 10.0, "BBB": 5.0}, {"AAA": 600.0}),
        ]:
            res, _ = self._run(cash_s, margin_s, shares, resolved)
            out = A.render(res, review=True)
            assert "UNAVAILABLE" in out
            assert "**Book:** $" not in out, out[:200]

    def test_the_reason_names_the_actual_blocking_state_not_always_cash(self):
        """The banner said "cash observation is not current" even when cash was fine."""
        res, _ = self._run(self.TODAY, self.STALE, {"AAA": 10.0}, {"AAA": 600.0})
        out = A.render(res, review=True)
        assert "MARGIN STATE" in out, out[:400]

    def test_an_independently_knowable_margin_diagnostic_still_renders(self):
        """Withholding a CASH-derived dollar must never silence a margin warning."""
        res, _ = self._run(self.STALE, self.TODAY, {"AAA": 10.0}, {"AAA": 600.0})
        out = A.render(res, review=True)
        assert "Margin" in out

    def test_net_equity_is_withheld_when_the_margin_reading_is_unusable(self):
        """`net equity = gross - debt` is DERIVED from the debt, so a stale debt
        makes it a current-dollar figure computed from an unverified term."""
        res, _ = self._run(self.TODAY, self.STALE, {"AAA": 10.0}, {"AAA": 600.0})
        out = A.render(res, review=True)
        leaked = [l for l in out.splitlines()
                  if "net equity" in l.lower() and "$" in l and "UNAVAILABLE" not in l]
        assert not leaked, leaked
        assert any("dated evidence" in l for l in out.splitlines()), \
            "a stale debt must be shown as dated evidence, not as a current reading"


class TestTheAvailabilityFactHasExactlyOneOwner:
    def test_every_required_state_is_represented(self):
        good_cash = {"usable": True}
        good_marg = {"usable": True}
        good_val = {"complete": True}
        assert A.current_dollar_availability(good_cash, good_marg, good_val)["available"]
        for bad in [({"usable": False, "reason": "c"}, good_marg, good_val),
                    (good_cash, {"usable": False, "reason": "m"}, good_val),
                    (good_cash, good_marg, {"complete": False, "reason": "v"})]:
            out = A.current_dollar_availability(*bad)
            assert out["available"] is False
            assert out["blocked_by"], out

    def test_main_hands_plan_the_computed_fact_rather_than_re_deriving_it(self):
        """No parallel rule: plan() must be TOLD, and main() must tell it."""
        src = inspect.getsource(A.main)
        assert "current_dollar_availability(cash_state, margin_status, valuation)" in src
        assert 'dollars_available=availability["available"]' in src
        # Strip the docstring first: it legitimately NAMES the owner, and matching
        # prose would make this assert vacuous in the wrong direction.
        plan_ast = ast.parse(inspect.getsource(A.plan).lstrip()).body[0]
        if (plan_ast.body and isinstance(plan_ast.body[0], ast.Expr)
                and isinstance(plan_ast.body[0].value, ast.Constant)):
            plan_ast.body = plan_ast.body[1:]
        plan_code = ast.dump(plan_ast)
        assert "current_dollar_availability" not in plan_code, \
            "plan() must consume the fact, never re-derive it"


class TestWriteBoundariesValidateBeforeTheyWrite:
    """MAJOR 2. An update command must never report success after persisting poison."""

    BAD_CASH = [float("nan"), float("inf"), float("-inf"), True, -1.0, "500", None]
    GOOD_CASH = [0.0, 1234.0, 7]

    @pytest.fixture
    def state(self, tmp_path, monkeypatch):
        f = tmp_path / "holdings.yaml"
        f.write_text(yaml.safe_dump(
            {"shares": {"AAA": 10.0},
             "cash": {"balance": 500.0, "synced_at": "2026-09-01"},
             "margin": {"debt": 0.0, "buffer_pct": 60.0, "synced_at": "2026-09-01"}},
            sort_keys=False))
        monkeypatch.setattr(A, "HOLDINGS_FILE", f)
        # update_margin now requires canonical state and its append-only audit
        # history to agree.  Isolate both sides of that durable pair; otherwise
        # this fixture combines temporary holdings with the repository ledger
        # and correctly triggers the production divergence refusal.
        monkeypatch.setattr(A, "MARGIN_LOG_FILE", tmp_path / "margin_log.csv")
        return f

    @pytest.mark.parametrize("bad", BAD_CASH)
    def test_update_cash_rejects_and_leaves_the_file_byte_identical(self, state, bad):
        before = state.read_bytes()
        with pytest.raises(ValueError):
            A.update_cash(bad)
        assert state.read_bytes() == before, "a rejected update still rewrote the file"

    @pytest.mark.parametrize("good", GOOD_CASH)
    def test_update_cash_still_accepts_valid_values(self, state, good, monkeypatch):
        monkeypatch.setattr(A, "log_performance", lambda *a, **k: None)
        A.update_cash(good)
        assert yaml.safe_load(state.read_text())["cash"]["balance"] == float(good)

    @pytest.mark.parametrize("debt,buf", [
        (-1.0, 120.0), (float("nan"), float("nan")), (0.0, 101.0), (0.0, -1.0),
        (0.0, float("inf")), (True, 30.0), (0.0, True), (0.0, None),
    ])
    def test_update_margin_rejects_and_preserves_the_file(self, state, debt, buf):
        before = state.read_bytes()
        with pytest.raises(ValueError):
            A.update_margin(debt, buf)
        assert state.read_bytes() == before

    @pytest.mark.parametrize("debt,buf", [(0.0, 0.0), (0.0, 100.0), (0.0, 30.0),
                                          (1234.5, 45.25)])
    def test_update_margin_accepts_valid_boundaries(self, state, debt, buf, monkeypatch):
        monkeypatch.setattr(A, "log_performance", lambda *a, **k: None)
        A.update_margin(debt, buf)
        m = yaml.safe_load(state.read_text())["margin"]
        assert (m["debt"], m["buffer_pct"]) == (debt, buf)


class TestTheMarginBufferIsRequiredNotOptional:
    TODAY = datetime.date.today().isoformat()

    @pytest.mark.parametrize("block", [
        {"debt": 100.0, "synced_at": TODAY},                      # key absent
        {"debt": 100.0, "buffer_pct": None, "synced_at": TODAY},   # explicitly null
    ])
    def test_a_current_debt_without_a_buffer_is_not_usable(self, block):
        """The 30% floor consumes this value; an absent buffer cannot satisfy it."""
        st = A.load_margin_state({"margin": block})
        assert st["usable"] is False
        assert "buffer_pct" in st["reason"]

    def test_a_complete_current_block_is_still_usable(self):
        st = A.load_margin_state(
            {"margin": {"debt": 100.0, "buffer_pct": 45.0, "synced_at": self.TODAY}})
        assert st["usable"] is True
        assert st["buffer_pct"] == 45.0

    def test_yaml_serialized_non_finite_forms_are_rejected(self):
        doc = yaml.safe_load(
            f"margin:\n  debt: .nan\n  buffer_pct: .inf\n  synced_at: {self.TODAY}\n")
        assert A.load_margin_state(doc)["usable"] is False


class TestEveryResolvedValueIsValidated:
    def test_a_manual_or_orphan_non_finite_value_blocks(self):
        """Only shares/crypto_shares symbols were scanned, so an entry tracked
        nowhere was never examined at all."""
        vc = A.valuation_completeness(
            {"MAN": float("nan")},
            {"holdings": {"MAN": float("nan")}, "shares": {}, "crypto_shares": {}})
        assert vc["complete"] is False
        assert vc["invalid"] == ["MAN"]

    def test_the_expected_symbol_coverage_proof_is_retained_separately(self):
        vc = A.valuation_completeness({"AAA": 600.0},
                                      {"shares": {"AAA": 10.0, "BBB": 5.0},
                                       "crypto_shares": {}})
        assert vc["unresolved"] == ["BBB"]
        assert vc["invalid"] == []
        assert vc["complete"] is False

    def test_a_fully_valid_set_is_complete(self):
        vc = A.valuation_completeness({"AAA": 600.0},
                                      {"shares": {"AAA": 10.0}, "crypto_shares": {}})
        assert vc["complete"] is True
        assert vc["invalid"] == [] and vc["unresolved"] == []


class TestTheLedgerRejectsPoisonFromASuppliedSet:
    TODAY = datetime.date.today().isoformat()

    class _Client:
        def get_bars(self, *a, **k):
            return [{"c": 100.0}]

    @pytest.fixture
    def paths(self, tmp_path, monkeypatch):
        h = tmp_path / "holdings.yaml"
        h.write_text(yaml.safe_dump(
            {"shares": {"AAA": 10.0},
             "cash": {"balance": 500.0, "synced_at": self.TODAY},
             "margin": {"debt": 0.0, "buffer_pct": 60.0, "synced_at": self.TODAY}}))
        monkeypatch.setattr(A, "HOLDINGS_FILE", h)
        monkeypatch.setattr(A, "PERF_LOG_FILE", tmp_path / "performance_log.csv")
        return tmp_path

    def test_a_caller_supplied_non_finite_value_writes_no_row(self, paths):
        A.log_performance(note="p", client=self._Client(), quiet=True,
                          resolved_holdings={"MAN": float("nan")})
        assert not (paths / "performance_log.csv").exists()

    def test_a_valid_supplied_set_still_writes_even_without_full_coverage(self, paths):
        """Coverage is the caller's business; only VALUE validity is enforced here,
        so this must not over-block."""
        A.log_performance(note="p", client=self._Client(), quiet=True,
                          resolved_holdings={"ZZZ": 900.0})
        assert (paths / "performance_log.csv").exists()
        text = (paths / "performance_log.csv").read_text()
        assert "nan" not in text.lower()


# ── PHQ-2026-07 correction round 3 — independent DELTA review 5085019004 ───────
# MAJOR 1 (reproduced): with a CURRENT cash observation, a STALE margin reading and
# a complete valuation, current_dollar_availability() correctly returned available
# False -- and plan() still published a gated name's ``target`` of $560, computed as
# ``book * target_pct`` from the very book it had just withheld. render() published
# that figure in the gated table while the protected-capital section simultaneously
# described the cash observation as current and unavailable.
#
# The tests below pin the corrected contract at its OUTPUT boundary rather than at
# an intermediate structure: the computed sentinel must not appear anywhere in
# render() or render_health(), in either unavailable state.


class TestTheComputedGatedTargetNeverReachesAnyRenderedSurface:
    """The exact escape independent review reproduced, pinned at both render surfaces.

    A gated name is the sharpest case: the allocator never buys it, so its published
    ``target`` has no operational use at all -- it exists purely as a book-derived
    figure, which is precisely the class the availability fact withholds.
    """

    TODAY = datetime.date.today().isoformat()
    STALE = "2026-01-01"

    #: Chosen so that ``book * target_pct`` lands on a value that cannot occur by
    #: coincidence in unrelated output. book = 600 held + 1000 cash - 200 debt = 1400;
    #: AAA's canonical weight is 40%; 1400 * 0.40 = 560.
    SENTINEL_NUMERALS = ("560", "1,400", "1400")

    def _plan(self, cash_synced, margin_synced, shares, resolved):
        data = {"shares": shares,
                "cash": {"balance": 1000.0, "synced_at": cash_synced},
                "margin": {"debt": 200.0, "buffer_pct": 60.0, "synced_at": margin_synced}}
        cs = A.load_cash_state(data)
        ms = A.load_margin_state(data)
        val = A.valuation_completeness(resolved, data)
        avail = A.current_dollar_availability(cs, ms, val)
        t = _targets()
        roster = build_roster(t)
        gates = _gates("AAA")
        res = plan(t, resolved, roster, _metrics(roster), True, True,
                   cash=(cs["balance"] if cs["usable"] else None),
                   margin_debt=(ms["debt"] or 0.0),
                   margin_buffer_pct=(ms["buffer_pct"] or 0.0),
                   gates_cfg=gates,
                   holdings_state=data, dollars_available=avail["available"])
        res["cash_state"] = cs
        res["margin_state_check"] = ms
        res["dollar_availability"] = avail
        res["margin"]["synced_at"] = margin_synced
        return res, avail

    @staticmethod
    def _numerals(text):
        """Digit runs with separators stripped, so ``$560`` and ``560.00`` both match."""
        return set(re.findall(r"\d[\d,]*", text))

    def test_the_positive_control_actually_computes_the_sentinel(self):
        """Without this the sentinel checks below could pass by never arising at all.

        With EVERY observation current, the same inputs must produce the $560 gated
        target -- proving the figure is real, reachable, and genuinely suppressed in
        the unavailable cases rather than absent for an unrelated reason.
        """
        res, avail = self._plan(self.TODAY, self.TODAY, {"AAA": 10.0}, {"AAA": 600.0})
        assert avail["available"] is True, avail
        gated = res["no_add_gated"]
        assert gated, "the gated row must exist for this control to mean anything"
        assert gated[0]["target"] == pytest.approx(560.0), gated[0]
        assert "560" in A.render(res, review=True)

    @pytest.mark.parametrize("case,cash_synced,margin_synced,shares,resolved", [
        ("stale margin, current cash, complete valuation",
         TODAY, STALE, {"AAA": 10.0}, {"AAA": 600.0}),
        ("current margin, current cash, INCOMPLETE valuation",
         TODAY, TODAY, {"AAA": 10.0, "BBB": 5.0}, {"AAA": 600.0}),
        ("stale cash, current margin, complete valuation",
         STALE, TODAY, {"AAA": 10.0}, {"AAA": 600.0}),
    ])
    def test_no_render_surface_publishes_the_computed_gated_target(
            self, case, cash_synced, margin_synced, shares, resolved):
        """The sentinel must appear in NEITHER render() NOR render_health()."""
        res, avail = self._plan(cash_synced, margin_synced, shares, resolved)
        assert avail["available"] is False, (case, avail)
        for name, text in (("render", A.render(res, review=True)),
                           ("render_health", A.render_health(res))):
            found = self._numerals(text) & set(self.SENTINEL_NUMERALS)
            assert not found, f"{case}: {name} published {sorted(found)}"

    @pytest.mark.parametrize("case,cash_synced,margin_synced,shares,resolved", [
        ("stale margin", TODAY, STALE, {"AAA": 10.0}, {"AAA": 600.0}),
        ("incomplete valuation", TODAY, TODAY, {"AAA": 10.0, "BBB": 5.0}, {"AAA": 600.0}),
        ("stale cash", STALE, TODAY, {"AAA": 10.0}, {"AAA": 600.0}),
    ])
    def test_the_gated_row_itself_carries_no_dollar_figure(
            self, case, cash_synced, margin_synced, shares, resolved):
        """The structural counterpart: withheld at the source, not merely unprinted."""
        res, _ = self._plan(cash_synced, margin_synced, shares, resolved)
        for r in res["no_add_gated"]:
            assert r["target"] is None, (case, r)
            assert r["gap"] is None, (case, r)
            # ...while the position's own resolved value, which is NOT book-derived,
            # survives. Withholding it would suppress an independently valid
            # observation, which the correction is explicitly not allowed to do.
            assert r["current"] is not None, (case, r)

    def test_the_gated_table_renders_the_unavailable_word_not_a_zero(self):
        """A withheld target must read as unavailable -- never as ``$0``.

        ``$0`` is a claim about the world ("this name's destination is nothing"),
        and it is false. This is the same substitution PHQ-2026-07 forbids for cash.
        """
        res, _ = self._plan(self.TODAY, self.STALE, {"AAA": 10.0}, {"AAA": 600.0})
        out = A.render(res, review=True)
        gated_lines = [ln for ln in out.splitlines()
                       if ln.startswith("| AAA") and "HOLD-TARGET-IN-CASH" in ln]
        assert gated_lines, out
        for ln in gated_lines:
            assert "UNAVAILABLE" in ln, ln
            assert "$0 " not in ln and "| $0" not in ln, ln

    @pytest.mark.parametrize("cash_synced,margin_synced,shares,resolved,blocker", [
        (TODAY, STALE, {"AAA": 10.0}, {"AAA": 600.0}, "margin"),
        (TODAY, TODAY, {"AAA": 10.0, "BBB": 5.0}, {"AAA": 600.0}, "valuation"),
    ])
    def test_a_current_cash_observation_is_never_described_as_unavailable(
            self, cash_synced, margin_synced, shares, resolved, blocker):
        """The contradiction the review named, at every surface that reports cash.

        When cash itself is current and something ELSE blocks the dollar figures,
        the output must say so. Reporting the cash observation as unavailable is a
        false statement about a reading the system actually holds.
        """
        res, avail = self._plan(cash_synced, margin_synced, shares, resolved)
        assert avail["available"] is False
        assert res["cash_state"]["usable"] is True
        for name, text in (("render", A.render(res, review=True)),
                           ("render_health", A.render_health(res))):
            for ln in text.splitlines():
                low = ln.lower()
                if "cash" in low and "UNAVAILABLE" in ln:
                    assert "actual tracked cash" not in low and "tracked cash" not in low, (
                        f"{name} called a CURRENT cash observation unavailable: {ln}")

    def test_the_explanation_names_the_actual_blocking_state(self):
        """One fact, one reason -- and the reason must be the true one.

        Before the correction the explanation always blamed cash, so a stale margin
        reading produced a sentence contradicted by the line directly above it.
        """
        res, _ = self._plan(self.TODAY, self.STALE, {"AAA": 10.0}, {"AAA": 600.0})
        out = A.render(res, review=True)
        reason = [ln for ln in out.splitlines() if "unavailable" in ln.lower()
                  and ("not zero" in ln.lower() or "not estimated" in ln.lower())]
        assert reason, out
        joined = " ".join(reason).lower()
        assert "margin" in joined, joined


# ── PHQ-2026-07 correction round 4 — independent DELTA review 5090097708 ──────
# MAJOR 1 (reproduced three ways): the availability contract stopped short of the
# actual result and render boundary.
#
#   A. plan() withheld a row's `target`/`gap`/`want`/`max_by_name` and then
#      returned `_rank_gap=990.0` and `_rank_max_by_name=990.0` in the SAME public
#      row. An underscore is a naming convention, not a boundary.
#   B. With an incomplete valuation, render() printed `Gross / net equity |
#      $600 / $400` and `Leverage 1.50x` from the deliberately understated gross.
#   C. With stale margin, render() withheld net equity but BOTH surfaces still
#      printed `Leverage 1.50x` — computed from the denominator just refused.


class TestNoInternalValueEscapesTheResultBoundary:
    """Structural, over the returned object — not a search of rendered text.

    A sentinel search cannot see a private key, and a fixed field list cannot see
    one introduced later. This asserts the SHAPE invariant instead: nothing whose
    name marks it internal leaves plan(), whatever it is called.
    """

    TODAY = datetime.date.today().isoformat()
    STALE = "2026-01-01"

    ROW_KEYS = ("buys", "trims", "underweight", "blocked", "no_add_gated",
                "no_add_issuer", "no_add_common_driver")

    def _plan(self, cash_synced, margin_synced, shares, resolved):
        data = {"shares": shares,
                "cash": {"balance": 1000.0, "synced_at": cash_synced},
                "margin": {"debt": 200.0, "buffer_pct": 60.0, "synced_at": margin_synced}}
        cs = A.load_cash_state(data)
        ms = A.load_margin_state(data)
        val = A.valuation_completeness(resolved, data)
        avail = A.current_dollar_availability(cs, ms, val)
        t = _targets()
        roster = build_roster(t)
        res = plan(t, resolved, roster, _metrics(roster), True, True,
                   cash=(cs["balance"] if cs["usable"] else None),
                   margin_debt=(ms["debt"] or 0.0),
                   margin_buffer_pct=(ms["buffer_pct"] or 0.0),
                   holdings_state=data, dollars_available=avail["available"])
        res["cash_state"] = cs
        res["margin_state_check"] = ms
        res["dollar_availability"] = avail
        res["margin"]["synced_at"] = margin_synced
        return res, avail

    @staticmethod
    def _private_keys(res):
        """Every leading-underscore key on every emitted row, wherever it lives."""
        found = []
        for key, rows in res.items():
            if not isinstance(rows, list):
                continue
            for r in rows:
                if not isinstance(r, dict):
                    continue
                for f, v in r.items():
                    if isinstance(f, str) and f.startswith("_"):
                        found.append((key, r.get("ticker"), f, v))
        return found

    @pytest.mark.parametrize("case,cash_synced,margin_synced,shares,resolved", [
        ("stale margin", TODAY, STALE, {"AAA": 10.0}, {"AAA": 600.0}),
        ("incomplete valuation", TODAY, TODAY, {"AAA": 10.0, "BBB": 5.0}, {"AAA": 600.0}),
        ("stale cash", STALE, TODAY, {"AAA": 10.0}, {"AAA": 600.0}),
        ("all current — control", TODAY, TODAY, {"AAA": 10.0}, {"AAA": 600.0}),
    ])
    def test_no_row_in_any_collection_carries_a_private_key(
            self, case, cash_synced, margin_synced, shares, resolved):
        """Discovered by shape, so a NEW private name is covered automatically.

        Asserted in the available case too: ranking state has no business in a
        published row regardless of whether dollars happen to be withheld.
        """
        res, _ = self._plan(cash_synced, margin_synced, shares, resolved)
        assert not self._private_keys(res), (case, self._private_keys(res))

    def test_the_underweight_ordering_still_holds_when_dollars_are_withheld(self):
        """The complement: stripping ranking state must not cost the ordering.

        plan()'s contract is that the OBSERVATIONAL view survives an unavailable
        book — names still rank by gap — while no dollar escapes. Both at once.
        """
        res, avail = self._plan(self.TODAY, self.STALE, {"AAA": 10.0}, {"AAA": 600.0})
        assert avail["available"] is False
        uw = res["underweight"]
        assert len(uw) >= 2, uw
        # Every published dollar is withheld...
        for r in uw:
            assert r["target"] is None and r["gap"] is None
            assert r.get("want") is None and r.get("max_by_name") is None
        # ...and the order still matches the order the available run produces.
        avail_res, avail_fact = self._plan(self.TODAY, self.TODAY,
                                           {"AAA": 10.0}, {"AAA": 600.0})
        assert avail_fact["available"] is True
        assert [r["ticker"] for r in uw] == [r["ticker"] for r in avail_res["underweight"]]


class TestBookDerivedFiguresHonourTheirOwnDependencies:
    """Behavioral, over BOTH render surfaces, for each unavailable state.

    gross depends on the valuation alone; net equity and leverage depend on the
    valuation AND the margin observation. Collapsing the three into one boolean
    is what produced a printed 1.50x beside an UNAVAILABLE net equity.
    """

    TODAY = datetime.date.today().isoformat()
    STALE = "2026-01-01"

    _plan = TestNoInternalValueEscapesTheResultBoundary._plan

    def test_the_dependency_map_is_stated_per_figure_not_collapsed(self):
        """Unit-level: the helper itself, before any rendering."""
        res, _ = self._plan(self.TODAY, self.STALE, {"AAA": 10.0}, {"AAA": 600.0})
        bd = A.book_derived_availability(res)
        assert bd["valuation_complete"] is True
        assert bd["margin_usable"] is False
        assert bd["gross"] is True, "gross depends on the valuation alone"
        assert bd["net_equity"] is False and bd["leverage"] is False

        res, _ = self._plan(self.TODAY, self.TODAY,
                            {"AAA": 10.0, "BBB": 5.0}, {"AAA": 600.0})
        bd = A.book_derived_availability(res)
        assert bd["valuation_complete"] is False
        assert bd["gross"] is False and bd["net_equity"] is False
        assert bd["leverage"] is False

        res, _ = self._plan(self.TODAY, self.TODAY, {"AAA": 10.0}, {"AAA": 600.0})
        bd = A.book_derived_availability(res)
        assert all(bd[k] for k in ("gross", "net_equity", "leverage", "book_ratios"))

    @pytest.mark.parametrize("surface", ["render", "render_health"])
    def test_stale_margin_withholds_net_equity_and_leverage_on_both_surfaces(self, surface):
        res, avail = self._plan(self.TODAY, self.STALE, {"AAA": 10.0}, {"AAA": 600.0})
        assert avail["available"] is False
        text = A.render(res, review=True) if surface == "render" else A.render_health(res)
        lev = [ln for ln in text.splitlines() if "Leverage (gross/equity)" in ln]
        assert lev, text
        for ln in lev:
            assert "UNAVAILABLE" in ln, f"{surface}: {ln}"
            assert "1.50x" not in ln, f"{surface}: {ln}"
        ne = [ln for ln in text.splitlines() if "Net equity" in ln]
        assert ne, text
        for ln in ne:
            assert "UNAVAILABLE" in ln, f"{surface}: {ln}"
        # Gross survives: only the debt term is unusable.
        gr = [ln for ln in text.splitlines() if "Invested gross" in ln]
        assert gr and any("$600" in ln for ln in gr), (surface, gr)

    @pytest.mark.parametrize("surface", ["render", "render_health"])
    def test_incomplete_valuation_withholds_gross_net_equity_and_leverage(self, surface):
        res, avail = self._plan(self.TODAY, self.TODAY,
                                {"AAA": 10.0, "BBB": 5.0}, {"AAA": 600.0})
        assert avail["available"] is False
        text = A.render(res, review=True) if surface == "render" else A.render_health(res)
        for label in ("Invested gross", "Net equity", "Leverage (gross/equity)"):
            lines = [ln for ln in text.splitlines() if label in ln]
            assert lines, (surface, label, text)
            for ln in lines:
                assert "UNAVAILABLE" in ln, f"{surface}: {ln}"
        # The understated figures must not appear anywhere at all.
        for bad in ("$600 / $400", "1.50x"):
            assert bad not in text, f"{surface} published {bad}"

    @pytest.mark.parametrize("surface", ["render", "render_health"])
    def test_all_current_still_prints_every_figure(self, surface):
        """Positive control: fail-closed, not fail-shut."""
        res, avail = self._plan(self.TODAY, self.TODAY, {"AAA": 10.0}, {"AAA": 600.0})
        assert avail["available"] is True
        text = A.render(res, review=True) if surface == "render" else A.render_health(res)
        lev = [ln for ln in text.splitlines() if "Leverage (gross/equity)" in ln]
        assert lev and all("UNAVAILABLE" not in ln for ln in lev), (surface, lev)
        assert "1.50x" in text, surface

    @pytest.mark.parametrize("surface", ["render", "render_health"])
    def test_book_denominated_ratios_are_withheld_with_the_book(self, surface):
        """Cluster %-of-book, ratio-to-cap and the common-driver percentage.

        All three are `value / book`, so each inherits the book's availability —
        the dependency the review asked to be inspected alongside leverage.
        """
        res, avail = self._plan(self.TODAY, self.STALE, {"AAA": 10.0}, {"AAA": 600.0})
        assert avail["available"] is False
        text = A.render(res, review=True) if surface == "render" else A.render_health(res)
        for ln in text.splitlines():
            if "Common-driver current" in ln or "Current calculated" in ln:
                assert "UNAVAILABLE" in ln, f"{surface}: {ln}"
            if "% of book" in ln:
                assert "n/a" in ln or "UNAVAILABLE" in ln, f"{surface}: {ln}"

    @pytest.mark.parametrize("surface", ["render", "render_health"])
    def test_both_surfaces_stay_internally_consistent_and_do_not_crash(self, surface):
        """No state may produce a report that contradicts itself or raises."""
        cases = [(self.TODAY, self.STALE, {"AAA": 10.0}, {"AAA": 600.0}),
                 (self.TODAY, self.TODAY, {"AAA": 10.0, "BBB": 5.0}, {"AAA": 600.0}),
                 (self.STALE, self.TODAY, {"AAA": 10.0}, {"AAA": 600.0}),
                 (self.TODAY, self.TODAY, {"AAA": 10.0}, {"AAA": 600.0})]
        for c in cases:
            res, _ = self._plan(*c)
            text = A.render(res, review=True) if surface == "render" else A.render_health(res)
            assert text and isinstance(text, str)
            bd = A.book_derived_availability(res)
            # If net equity is withheld, leverage must be too — never one without
            # the other, since one is computed from the other.
            ne_lines = [ln for ln in text.splitlines() if "Net equity" in ln]
            lev_lines = [ln for ln in text.splitlines() if "Leverage (gross/equity)" in ln]
            if ne_lines and any("UNAVAILABLE" in ln for ln in ne_lines):
                assert all("UNAVAILABLE" in ln for ln in lev_lines), (c, text)
            assert bd["leverage"] == bd["net_equity"]


# ── PHQ-2026-07 correction round 5 — independent DELTA review 5091155438 ─────
# MAJOR 1 (reproduced three ways): masking selected PRESENTATION fields left the
# emitted RESULT itself carrying values derived from an unavailable book.
#
#   A. stale margin -> trims[0]["dollars"] == 640.0 and the reason text
#      "C cluster cap 20% ($820 over own target)", rendered verbatim while the
#      Dollars column said n/a.
#   B. tracked-but-unresolved BBB -> current == 0.0, holds_existing_shares False,
#      "$0 (no position)" rendered, and a cluster containing BBB reporting $600.
#   C. stale margin -> numeric margin.net_equity / margin.leverage_current,
#      cluster current_pct / ratio_to_cap, issuer_exposure percentages, and both
#      issuer tables printing 55.56% while book-ratio availability was false.
#
# The correction is ONE dependency-aware boundary immediately before plan()
# returns, driven by an explicit output schema. A numeric path with no stated
# dependency raises rather than being emitted, so a new field cannot reach a
# caller until someone says what it depends on.


class TestTheOutputBoundaryIsExhaustiveAndFailsClosed:
    """The schema itself, before any individual defect."""

    TODAY = datetime.date.today().isoformat()
    STALE = "2026-01-01"

    @staticmethod
    def _numeric_paths(node, path=""):
        """Every emitted numeric path, found recursively — not from a list."""
        out = []
        if isinstance(node, dict):
            for k, v in node.items():
                out += TestTheOutputBoundaryIsExhaustiveAndFailsClosed._numeric_paths(
                    v, f"{path}.{k}" if path else str(k))
        elif isinstance(node, list):
            for v in node:
                out += TestTheOutputBoundaryIsExhaustiveAndFailsClosed._numeric_paths(
                    v, path + "[]")
        elif isinstance(node, bool):
            pass
        elif isinstance(node, (int, float)):
            out.append(path)
        return out

    def _rich_plan(self, cash_s, margin_s, shares, resolved):
        """A result exercising every collection, nested mapping and aggregate."""
        data = {"shares": shares,
                "cash": {"balance": 1000.0, "synced_at": cash_s},
                "margin": {"debt": 200.0, "buffer_pct": 60.0, "synced_at": margin_s}}
        cs = A.load_cash_state(data)
        ms = A.load_margin_state(data)
        val = A.valuation_completeness(resolved, data)
        avail = A.current_dollar_availability(cs, ms, val)
        t = _targets()
        t["caps"] = {"clusters": [{"name": "C", "pct": 20.0, "tickers": ["AAA", "BBB"]}]}
        lt = {"issuers": [{"ticker": "AAA", "funds": []}],
              "common_driver_ceiling_pct": 40.0}
        gates = _gates("GGG")
        roster = build_roster(t)
        res = plan(t, resolved, roster, _metrics(roster), True, True,
                   cash=(cs["balance"] if cs["usable"] else None),
                   margin_debt=(ms["debt"] or 0.0),
                   margin_buffer_pct=(ms["buffer_pct"] or 0.0),
                   gates_cfg=gates, lookthrough=lt,
                   holdings_state=data, dollars_available=avail["available"])
        # Returned BEFORE the render-support keys are attached: those are added
        # by callers, not emitted by plan(), and the schema governs plan()'s own
        # output.
        raw = {k: v for k, v in res.items()}
        res["cash_state"] = cs
        res["margin_state_check"] = ms
        res["dollar_availability"] = avail
        res["margin"]["synced_at"] = margin_s
        return res, avail, raw

    @pytest.mark.parametrize("case,cash_s,margin_s,shares,resolved", [
        ("all current", TODAY, TODAY, {"AAA": 10.0, "BBB": 2.0},
         {"AAA": 1000.0, "BBB": 200.0}),
        ("stale margin", TODAY, STALE, {"AAA": 10.0, "BBB": 2.0},
         {"AAA": 1000.0, "BBB": 200.0}),
        ("stale cash", STALE, TODAY, {"AAA": 10.0, "BBB": 2.0},
         {"AAA": 1000.0, "BBB": 200.0}),
        ("incomplete valuation", TODAY, TODAY, {"AAA": 10.0, "BBB": 2.0},
         {"AAA": 1000.0}),
    ])
    def test_every_emitted_numeric_path_is_classified(
            self, case, cash_s, margin_s, shares, resolved):
        """The mechanism the review asked for: no unclassified numeric path.

        plan() raises `UnclassifiedOutputPath` rather than emitting one, so this
        passing at all IS the proof — and the assertion below makes the intent
        explicit rather than relying on the absence of an exception.
        """
        _, _, raw = self._rich_plan(cash_s, margin_s, shares, resolved)
        paths = self._numeric_paths(raw)
        assert paths, "the fixture must actually emit numbers"
        for p in paths:
            key = p
            if key not in A._OUTPUT_DEPENDENCIES:
                parts = p.split(".")
                if len(parts) == 3 and parts[0] == "issuer_exposure":
                    key = f"issuer_exposure.*.{parts[2]}"
                elif "[]." in p:
                    key = p.split("[].")[-1]
                    assert key in A._ROW_FIELD_DEPENDENCIES, p
                    continue
            assert key in A._OUTPUT_DEPENDENCIES, p

    def test_an_unclassified_numeric_field_is_refused_not_emitted(self):
        """Fail-closed, demonstrated rather than asserted in prose."""
        res = {"buys": [{"ticker": "AAA", "brand_new_dollar_field": 1.0}]}
        with pytest.raises(A.UnclassifiedOutputPath):
            A._apply_output_dependencies(
                res, {"valuation": True, "margin": True, "book": True},
                {"AAA"}, {})

    def test_an_unclassified_top_level_numeric_field_is_refused(self):
        res = {"some_new_total": 5.0}
        with pytest.raises(A.UnclassifiedOutputPath):
            A._apply_output_dependencies(
                res, {"valuation": True, "margin": True, "book": True}, set(), {})

    def test_the_row_collection_list_matches_what_plan_emits(self):
        """A new row collection cannot skip the boundary unnoticed."""
        _, _, raw = self._rich_plan(self.TODAY, self.TODAY, {"AAA": 10.0},
                                    {"AAA": 1000.0})
        emitted = {k for k, v in raw.items()
                   if isinstance(v, list) and any(isinstance(r, dict) for r in v)}
        unguarded = emitted - set(A._ROW_COLLECTIONS) - {"clusters"}
        # `gated_detail` lives under protection and is covered by the recursive
        # walk with its own explicit paths; anything else would be unguarded.
        assert not unguarded, unguarded


class TestNoBookDerivedValueSurvivesInTheEmittedResult:
    """The three exact reproductions, plus recursive checks over the result."""

    TODAY = datetime.date.today().isoformat()
    STALE = "2026-01-01"

    def _trim_case(self):
        """Review's case A: current cash, complete valuation, STALE margin."""
        t = _targets(rows=[
            {"ticker": "AAA", "target_pct": 10.0, "asset_class": "equity"},
            {"ticker": "RESERVE", "target_pct": 15.0, "asset_class": "reserve"},
            {"ticker": "CASH", "target_pct": 4.0, "asset_class": "cash"}])
        t["caps"] = {"clusters": [{"name": "C", "pct": 20.0, "tickers": ["AAA"]}]}
        data = {"shares": {"AAA": 10.0},
                "cash": {"balance": 1000.0, "synced_at": self.TODAY},
                "margin": {"debt": 200.0, "buffer_pct": 60.0, "synced_at": self.STALE}}
        cs = A.load_cash_state(data)
        ms = A.load_margin_state(data)
        val = A.valuation_completeness({"AAA": 1000.0}, data)
        avail = A.current_dollar_availability(cs, ms, val)
        roster = build_roster(t)
        res = plan(t, {"AAA": 1000.0}, roster, _metrics(roster), True, True,
                   cash=cs["balance"], margin_debt=200.0, margin_buffer_pct=60.0,
                   holdings_state=data, dollars_available=avail["available"])
        res["cash_state"] = cs
        res["margin_state_check"] = ms
        res["dollar_availability"] = avail
        res["margin"]["synced_at"] = self.STALE
        return res, avail

    def test_a_trim_dollar_is_withheld_when_the_book_is_unavailable(self):
        """Review case A, structural half."""
        res, avail = self._trim_case()
        assert avail["available"] is False
        assert res["trims"], "the cluster cap must actually produce a trim"
        assert res["trims"][0]["dollars"] is None, res["trims"][0]

    def test_a_trim_reason_never_quotes_a_book_derived_dollar(self):
        """Review case A, free-text half.

        The reason string is an OUTPUT: "$820 over own target" published the very
        figure the Dollars column had just withheld.
        """
        res, _ = self._trim_case()
        reason = res["trims"][0]["reason"]
        assert "$820" not in reason, reason
        assert "UNAVAILABLE" in reason, reason
        assert not re.search(r"\$[\d,]+(?:\.\d+)?", reason), reason

    def test_no_render_surface_prints_the_trim_dollar_or_its_reason_figure(self):
        res, _ = self._trim_case()
        for name, text in (("render", A.render(res, review=True)),
                           ("render_health", A.render_health(res))):
            assert "$820" not in text, name
            assert "$640" not in text, name

    def test_the_trim_still_happens_and_is_still_explained(self):
        """The complement: withholding a dollar must not lose the FINDING.

        The cap breach is real and independently knowable; only its dollar
        magnitude depends on the book.
        """
        res, _ = self._trim_case()
        assert len(res["trims"]) == 1
        assert res["trims"][0]["ticker"] == "AAA"
        assert "cluster cap" in res["trims"][0]["reason"]
        assert "TRIM" in A.render(res, review=True)

    def _missing_holding_case(self):
        """Review's case B: tracked BBB shares, BBB absent from resolved."""
        t = _targets()
        t["caps"] = {"clusters": [{"name": "BOTH", "pct": 50.0,
                                   "tickers": ["AAA", "BBB"]}]}
        data = {"shares": {"AAA": 6.0, "BBB": 5.0},
                "cash": {"balance": 1000.0, "synced_at": self.TODAY},
                "margin": {"debt": 200.0, "buffer_pct": 60.0, "synced_at": self.TODAY}}
        cs = A.load_cash_state(data)
        ms = A.load_margin_state(data)
        val = A.valuation_completeness({"AAA": 600.0}, data)
        avail = A.current_dollar_availability(cs, ms, val)
        roster = build_roster(t)
        res = plan(t, {"AAA": 600.0}, roster, _metrics(roster), True, True,
                   cash=cs["balance"], margin_debt=200.0, margin_buffer_pct=60.0,
                   gates_cfg=_gates("BBB"),
                   holdings_state=data, dollars_available=avail["available"])
        res["cash_state"] = cs
        res["margin_state_check"] = ms
        res["dollar_availability"] = avail
        return res, avail, val

    def test_a_missing_tracked_holding_is_unknown_not_zero(self):
        """Review case B. `$0` and `no position` were both false claims."""
        res, avail, val = self._missing_holding_case()
        assert "BBB" in (val.get("unresolved") or []), val
        row = [r for r in res["no_add_gated"] if r["ticker"] == "BBB"][0]
        assert row["current"] is None, row
        assert row["holds_existing_shares"] is not False, row

    def test_the_render_never_calls_a_missing_holding_a_zero_position(self):
        res, _, _ = self._missing_holding_case()
        text = A.render(res, review=True)
        bbb = [ln for ln in text.splitlines() if ln.startswith("| BBB")]
        assert bbb, text
        for ln in bbb:
            assert "$0 (no position)" not in ln, ln
            assert "UNAVAILABLE" in ln, ln
            # The POSITION CLAIM matters independently of the dollar figure. A
            # line reading "UNAVAILABLE (no position)" still asserts, falsely,
            # that BBB holds nothing -- while its nonzero shares are tracked.
            assert "(no position)" not in ln, ln
            assert "UNKNOWN" in ln, ln

    def test_an_aggregate_is_unavailable_when_any_member_is_unvalued(self):
        """Review case B, aggregate half: BOTH reported $600 without BBB."""
        res, _, _ = self._missing_holding_case()
        both = [c for c in res["clusters"] if c["name"] == "BOTH"][0]
        assert both["value"] is None, both
        text = A.render(res, review=True)
        assert "BOTH $600" not in text, text
        assert "UNAVAILABLE" in text

    def test_a_resolved_ticker_keeps_its_own_value_despite_another_being_missing(self):
        """Per-NAME coverage: one missing holding must not blank the rest."""
        res, _, _ = self._missing_holding_case()
        rows = {r["ticker"]: r for coll in A._ROW_COLLECTIONS
                for r in (res.get(coll) or []) if isinstance(r, dict)}
        # BBB is tracked but unpriced -> unknown.
        assert rows["BBB"]["current"] is None, rows["BBB"]
        # GGG holds nothing at all -> a KNOWN zero, which must survive. Blanking
        # it would destroy a true observation exactly as surely as printing $0
        # for BBB invented a false one.
        assert rows["GGG"]["current"] == 0.0, rows["GGG"]
        # ...and BBB's own position CLAIM is unknown rather than a false "no
        # position", which is the second half of the reproduced defect.
        assert rows["BBB"]["holds_existing_shares"] is None, rows["BBB"]

    def _issuer_case(self):
        """Review's case C: stale margin plus issuer lookthrough."""
        t = _targets(rows=[
            {"ticker": "AAA", "target_pct": 10.0, "asset_class": "equity"},
            {"ticker": "RESERVE", "target_pct": 15.0, "asset_class": "reserve"},
            {"ticker": "CASH", "target_pct": 4.0, "asset_class": "cash"}])
        t["caps"] = {"clusters": [{"name": "C", "pct": 20.0, "tickers": ["AAA"]}]}
        lt = {"issuers": [{"ticker": "AAA", "funds": []}],
              "common_driver_ceiling_pct": 40.0}
        data = {"shares": {"AAA": 10.0},
                "cash": {"balance": 1000.0, "synced_at": self.TODAY},
                "margin": {"debt": 200.0, "buffer_pct": 60.0, "synced_at": self.STALE}}
        cs = A.load_cash_state(data)
        ms = A.load_margin_state(data)
        val = A.valuation_completeness({"AAA": 1000.0}, data)
        avail = A.current_dollar_availability(cs, ms, val)
        roster = build_roster(t)
        res = plan(t, {"AAA": 1000.0}, roster, _metrics(roster), True, True,
                   cash=cs["balance"], margin_debt=200.0, margin_buffer_pct=60.0,
                   lookthrough=lt,
                   holdings_state=data, dollars_available=avail["available"])
        res["cash_state"] = cs
        res["margin_state_check"] = ms
        res["dollar_availability"] = avail
        res["margin"]["synced_at"] = self.STALE
        return res, avail

    def test_the_public_result_carries_no_book_derived_number(self):
        """Review case C, structural. Every named path, checked on the result."""
        res, avail = self._issuer_case()
        assert avail["available"] is False
        assert res["margin"]["net_equity"] is None
        assert res["margin"]["leverage_current"] is None
        for c in res["clusters"]:
            assert c["current_pct"] is None, c
            assert c["ratio_to_cap"] is None, c
        for tk, v in (res["issuer_exposure"] or {}).items():
            assert v["direct_pct"] is None, (tk, v)
            assert v["embedded_pct"] is None, (tk, v)
            assert v["effective_pct"] is None, (tk, v)
        assert res["common_driver_current_pct"] is None

    def test_independently_valid_observations_survive(self):
        """Positive control: fail-closed, never fail-shut.

        Gross depends on the valuation alone and it is complete here; the debt
        and the broker's own displayed buffer are readings, not derivations.
        """
        res, _ = self._issuer_case()
        assert res["margin"]["gross"] == pytest.approx(1000.0)
        assert res["margin"]["debt"] == pytest.approx(200.0)
        assert res["margin"]["buffer_pct"] == pytest.approx(60.0)
        assert res["margin"]["leverage_cap"] is not None
        assert res["cash_spent"] == 0.0, "a known zero, not an unknown"
        cluster = res["clusters"][0]
        assert cluster["value"] is not None, "AAA is resolved, so the value is real"
        assert cluster["pct"] == pytest.approx(20.0), "a configured cap is always true"

    @pytest.mark.parametrize("surface", ["render", "render_health"])
    def test_no_issuer_percentage_is_printed_while_book_ratios_are_unavailable(
            self, surface):
        """Review case C, presentation. Both issuer tables printed 55.56%."""
        res, _ = self._issuer_case()
        assert A.book_derived_availability(res)["book_ratios"] is False
        text = A.render(res, review=True) if surface == "render" else A.render_health(res)
        assert "55.56%" not in text, surface
        for ln in text.splitlines():
            if ln.startswith("| AAA") and "%" in ln:
                assert "UNAVAILABLE" in ln or "n/a" in ln, f"{surface}: {ln}"

    @pytest.mark.parametrize("cash_s,margin_s,shares,resolved,label", [
        ("2026-01-01", None, {"AAA": 10.0}, {"AAA": 1000.0}, "stale cash"),
        (None, "2026-01-01", {"AAA": 10.0}, {"AAA": 1000.0}, "stale margin"),
        (None, None, {"AAA": 10.0, "BBB": 5.0}, {"AAA": 1000.0}, "incomplete valuation"),
    ])
    def test_recursively_no_unavailable_number_escapes_in_any_state(
            self, cash_s, margin_s, shares, resolved, label):
        """A recursive sweep, so a nested mapping cannot hide one."""
        today = self.TODAY
        data = {"shares": shares,
                "cash": {"balance": 1000.0, "synced_at": cash_s or today},
                "margin": {"debt": 200.0, "buffer_pct": 60.0,
                           "synced_at": margin_s or today}}
        cs = A.load_cash_state(data)
        ms = A.load_margin_state(data)
        val = A.valuation_completeness(resolved, data)
        avail = A.current_dollar_availability(cs, ms, val)
        assert avail["available"] is False, label
        t = _targets()
        t["caps"] = {"clusters": [{"name": "C", "pct": 20.0, "tickers": ["AAA", "BBB"]}]}
        roster = build_roster(t)
        res = plan(t, resolved, roster, _metrics(roster), True, True,
                   cash=(cs["balance"] if cs["usable"] else None),
                   margin_debt=(ms["debt"] or 0.0),
                   margin_buffer_pct=(ms["buffer_pct"] or 0.0),
                   holdings_state=data, dollars_available=avail["available"])

        def sweep(node, path=""):
            bad = []
            if isinstance(node, dict):
                for k, v in node.items():
                    bad += sweep(v, f"{path}.{k}" if path else str(k))
            elif isinstance(node, list):
                for v in node:
                    bad += sweep(v, path + "[]")
            elif isinstance(node, str):
                if re.search(r"\$[\d,]+(?:\.\d+)?", node):
                    bad.append((path, node))
            return bad

        # Every book-dependent path must be None; free text must quote no dollar.
        assert res["book"] is None, label
        assert res["protection"]["protected_floor_dollars"] is None, label
        assert not sweep(res), (label, sweep(res))

    @pytest.mark.parametrize("surface", ["render", "render_health"])
    def test_both_surfaces_render_every_state_without_raising(self, surface):
        """The boundary hands render() Nones; neither may crash or rebuild them."""
        for maker in (self._trim_case, self._missing_holding_case, self._issuer_case):
            out = maker()
            res = out[0]
            text = (A.render(res, review=True) if surface == "render"
                    else A.render_health(res))
            assert text and isinstance(text, str)


class TestAvailabilityIsDerivedFromObservationsNotFromTheArgument:
    """PHQ-2026-07 / review 5092359752 MAJOR 1.1.

    ``dollars_available=True`` is the public default. A caller that supplied a
    stale margin observation but omitted the separately precomputed flag used to
    get current-looking output anyway: `margin_usable=False` while the result
    reported `dollars_available=True` and a numeric book with numeric gated
    target/gap. The boundary already held every observation needed to reject
    that; it just deferred to the argument.

    The corrected rule, pinned here in both directions: a caller flag may
    RESTRICT further, but may never make unavailable observed state available.
    """

    def _state(self, cash_s, margin_s):
        return {"shares": {"AAA": 10.0},
                "cash": {"balance": 1000.0, "synced_at": cash_s},
                "margin": {"debt": 200.0, "buffer_pct": 60.0, "synced_at": margin_s}}

    def _plan(self, data, **kw):
        t = _targets()
        roster = build_roster(t)
        cs = load_cash_state(data)
        ms = load_margin_state(data)
        return plan(t, {"AAA": 1000.0}, roster, _metrics(roster), True, True,
                    cash=(cs["balance"] if cs["usable"] else None),
                    margin_debt=(ms["debt"] or 0.0),
                    margin_buffer_pct=(ms["buffer_pct"] or 0.0),
                    gates_cfg=_gates("AAA"), holdings_state=data, **kw)

    def test_the_exact_reproduction_no_book_derived_number_survives(self):
        """THE REQUIRED REPRODUCTION: current cash, complete valuation, stale
        margin, holdings_state supplied, `dollars_available` OMITTED."""
        data = self._state(FRESH, STALE)
        assert load_cash_state(data)["usable"] is True
        assert valuation_completeness({"AAA": 1000.0}, data)["complete"] is True
        assert load_margin_state(data)["usable"] is False
        res = self._plan(data)                       # flag omitted on purpose
        assert res["dollars_available"] is False
        assert res["book"] is None
        assert res["protection"]["book"] is None
        assert res["protection"]["protected_floor_dollars"] is None
        for row in res["no_add_gated"]:
            assert row["target"] is None, row
            assert row["gap"] is None, row

    def test_an_explicitly_true_flag_cannot_override_a_failed_observation(self):
        """Not just the default: an ACTIVELY passed True is overridden too."""
        res = self._plan(self._state(FRESH, STALE), dollars_available=True)
        assert res["dollars_available"] is False
        assert res["book"] is None

    @pytest.mark.parametrize("cash_s,margin_s,resolved,label", [
        (STALE, FRESH, {"AAA": 1000.0}, "stale cash"),
        (FRESH, STALE, {"AAA": 1000.0}, "stale margin"),
        (FRESH, FRESH, {}, "incomplete valuation"),
    ])
    def test_every_failed_observation_alone_withholds_the_book(
            self, cash_s, margin_s, resolved, label):
        data = self._state(cash_s, margin_s)
        t = _targets()
        roster = build_roster(t)
        cs = load_cash_state(data)
        ms = load_margin_state(data)
        res = plan(t, resolved, roster, _metrics(roster), True, True,
                   cash=(cs["balance"] if cs["usable"] else None),
                   margin_debt=(ms["debt"] or 0.0),
                   margin_buffer_pct=(ms["buffer_pct"] or 0.0),
                   gates_cfg=_gates("AAA"), holdings_state=data)
        assert res["dollars_available"] is False, label
        assert res["book"] is None, label

    def test_a_caller_flag_may_still_restrict_further(self):
        """The allowance is one-directional, and that direction is preserved."""
        data = self._state(FRESH, FRESH)
        assert A.current_dollar_availability(
            load_cash_state(data), load_margin_state(data),
            valuation_completeness({"AAA": 1000.0}, data))["available"] is True
        assert self._plan(data)["book"] is not None          # nothing restricts
        assert self._plan(data, dollars_available=False)["book"] is None

    def test_the_mechanics_only_caller_is_preserved_and_explicit(self):
        """An ABSENT observation is not a FAILED one.

        A caller supplying no `cash:` block made no cash claim, so there is
        nothing to contradict -- that is the legitimate mechanics-only path, and
        it stays open. It is stated here rather than left implicit, because it is
        the one place the caller's own flag is still the only switch.
        """
        t = _targets()
        roster = build_roster(t)
        res = plan(t, {"AAA": 1000.0}, roster, _metrics(roster), True, True,
                   cash=200.0, margin_debt=50.0, margin_buffer_pct=100.0,
                   holdings_state={})
        assert res["book"] == pytest.approx(1000.0 + 200.0 - 50.0)
        # ...but a SUPPLIED and FAILED observation still governs, even here.
        bad = {"margin": {"debt": 50.0, "buffer_pct": 100.0, "synced_at": STALE}}
        assert plan(t, {"AAA": 1000.0}, roster, _metrics(roster), True, True,
                    cash=200.0, margin_debt=50.0, margin_buffer_pct=100.0,
                    holdings_state=bad)["book"] is None

    def test_removing_the_derivation_makes_this_class_fail(self):
        """MUTATION PROBE: the protection is load-bearing, not decorative."""
        src = inspect.getsource(plan)
        assert "_observed_book_ok" in src
        assert "and _observed_book_ok)" in src, (
            "the derived fact is no longer conjoined into dollars_ok")


class TestTheBoundaryIsExhaustiveByPathAndShape:
    """PHQ-2026-07 / review 5092359752 MAJOR 1.2.

    The superseded walker classified by RUNTIME TYPE: it skipped scalar list
    members outright and ignored any string whose field name was not in a
    selected list. Both of the review's probes crossed unchanged. Every EMITTED
    LEAF now needs a stated contract -- of any type, at any depth, in any
    sequence -- and an unclassified one raises.
    """

    DEPS = {"valuation": True, "margin": True, "book": False}

    def _apply(self, payload):
        return A._apply_output_dependencies(payload, dict(self.DEPS), set(), {})

    def test_a_new_numeric_collection_fails_closed(self):
        """THE REQUIRED REPRODUCTION 1."""
        with pytest.raises(A.UnclassifiedOutputPath):
            self._apply({"new_collection": [42.0]})

    def test_a_renamed_prose_field_carrying_a_dollar_fails_closed(self):
        """THE REQUIRED REPRODUCTION 2."""
        with pytest.raises(A.UnclassifiedOutputPath):
            self._apply({"buys": [{"ticker": "AAA",
                                   "explanation": "derived $820 amount"}]})

    @pytest.mark.parametrize("payload,label", [
        ({"nested": {"deeper": {"amount": 5.0}}}, "nested mapping"),
        ({"seq": [[1.0, 2.0]]}, "nested scalar sequence"),
        ({"buys": [{"ticker": "AAA", "brand_new_pct": 12.0}]}, "new row field"),
        ({"clusters": [{"name": "C", "invented": 3.0}]}, "new cluster field"),
        ({"optional_thing": None}, "None-valued unknown leaf"),
        ({"some_label": "a plain string"}, "unknown string leaf"),
    ], ids=lambda v: v if isinstance(v, str) else "")
    def test_every_unclassified_shape_fails_closed(self, payload, label):
        with pytest.raises(A.UnclassifiedOutputPath):
            self._apply(payload)

    def test_a_static_leaf_that_acquires_a_number_fails_closed(self):
        """Declaring a field static is a CLAIM, and it is checked."""
        with pytest.raises(A.UnclassifiedOutputPath):
            self._apply({"regime_ok": 1.5})

    def test_recognized_static_and_config_output_is_retained(self):
        """The complement: valid observations are not broadly blanked."""
        out = self._apply({"regime_ok": True, "issuer_ceiling_pct": 8.0,
                           "cash_spent": 0.0, "valuation": {
                               "complete": False, "expected_count": 2,
                               "reason": "no current value for BBB",
                               "unresolved": ["BBB"]}})
        assert out["regime_ok"] is True
        assert out["issuer_ceiling_pct"] == 8.0
        assert out["cash_spent"] == 0.0          # a KNOWN zero, not an unknown
        assert out["valuation"]["expected_count"] == 2
        assert out["valuation"]["unresolved"] == ["BBB"]

    def test_the_frozen_config_subtree_is_a_verbatim_passthrough(self):
        """The one PREFIX rule earns its exception by PROVENANCE, and this pins it.

        `retained_common_driver_measurement` is copied verbatim out of
        issuer_lookthrough.yaml -- nothing in it is computed here -- so it cannot
        quietly acquire a derived field under cover of the prefix.
        """
        cfg = yaml.safe_load(open("issuer_lookthrough.yaml"))
        block = cfg["retained_common_driver_measurement"]
        src = inspect.getsource(plan)
        assert ('"retained_common_driver_measurement": '
                'lookthrough.get("retained_common_driver_measurement")') in src, (
            "the retained block is no longer a verbatim config passthrough")
        out = self._apply({"retained_common_driver_measurement": dict(block)})
        assert out["retained_common_driver_measurement"] == block

    def test_removing_the_raise_makes_this_class_fail(self):
        """MUTATION PROBE: fail-closed is the mechanism, not a comment."""
        src = inspect.getsource(A._leaf_contract)
        assert src.count("raise UnclassifiedOutputPath") >= 2


class TestPostPlanDerivationsHonourTheSameContract:
    """PHQ-2026-07 / review 5092359752 MAJOR 1.3.

    `margin_state` is attached AFTER plan()'s boundary. Gated only on gross, it
    recreated exactly what the boundary had withheld: with complete valuation and
    a stale margin observation the sanitized result carried `net_equity=None` and
    `leverage_current=None` while the classifier returned `net_equity=800.0`,
    `leverage_ratio=1.25`, `utilization=0.3125`, and the advisory printed
    "Margin risk state: NORMAL -- leverage and buffer within normal range".
    """

    STATE_WORDS = ("NORMAL", "CAUTION", "RESTRICTED", "FORCED_DELEVER")

    def _result(self, margin_s):
        data = {"shares": {"AAA": 10.0},
                "cash": {"balance": 1000.0, "synced_at": FRESH},
                "margin": {"debt": 200.0, "buffer_pct": 60.0, "synced_at": margin_s}}
        cs = load_cash_state(data)
        ms = load_margin_state(data)
        val = valuation_completeness({"AAA": 1000.0}, data)
        av = A.current_dollar_availability(cs, ms, val)
        t = _targets()
        roster = build_roster(t)
        res = plan(t, {"AAA": 1000.0}, roster, _metrics(roster), True, True,
                   cash=(cs["balance"] if cs["usable"] else None),
                   margin_debt=(ms["debt"] or 0.0),
                   margin_buffer_pct=(ms["buffer_pct"] or 0.0),
                   gates_cfg={}, holdings_state=data,
                   dollars_available=av["available"])
        res["cash_state"] = cs
        res["margin_state_check"] = ms
        res["dollar_availability"] = av
        res["margin"]["synced_at"] = margin_s
        return res, ms, val

    def test_main_gates_the_classifier_on_a_usable_observation_not_only_gross(self):
        """THE REQUIRED REPRODUCTION, at the gate itself."""
        res, ms, val = self._result(STALE)
        assert val["complete"] is True            # gross IS available...
        assert res["margin"]["gross"] is not None
        assert ms["usable"] is False              # ...but the reading is not
        assert res["margin"]["net_equity"] is None
        assert res["margin"]["leverage_current"] is None
        src = inspect.getsource(A.main)
        assert "_margin_conclusion_ok" in src
        assert 'bool(margin_state.get("usable"))' in src, (
            "the classifier is gated on gross alone again")

    @pytest.mark.parametrize("surface", ["render", "render_health"])
    def test_no_risk_state_is_asserted_from_an_unusable_observation(self, surface):
        res, _ms, _val = self._result(STALE)
        res["margin_state"] = None
        res["margin_state_unavailable"] = {
            "reason": "margin synced 30d ago", "reasons": [],
            "violated_constraints": ["stale_margin_data"],
            "actions": ["verify_margin_data"]}
        text = (A.render(res, review=True) if surface == "render"
                else A.render_health(res))
        for word in self.STATE_WORDS:
            assert f"Margin risk state: {word}" not in text, word
            assert f"**{word}**" not in text, word
        assert "leverage and buffer within normal range" not in text
        assert "UNAVAILABLE" in text

    @pytest.mark.parametrize("surface", ["render", "render_health"])
    def test_the_verify_and_resync_instruction_is_preserved(self, surface):
        """Withholding the CONCLUSION must not withhold the INSTRUCTION."""
        res, _ms, _val = self._result(STALE)
        res["margin_state"] = None
        res["margin_state_unavailable"] = {
            "reason": "margin synced 30d ago (> 2d)",
            "reasons": ["margin data is 30 day(s) old"],
            "violated_constraints": ["stale_margin_data"],
            "actions": ["verify_margin_data"]}
        text = (A.render(res, review=True) if surface == "render"
                else A.render_health(res))
        assert "verify_margin_data" in text
        assert "stale_margin_data" in text

    def test_the_dated_raw_margin_evidence_still_stands(self):
        """Debt and the broker's own displayed buffer are READINGS, not
        conclusions, so they are reported with their staleness disclosed."""
        res, _ms, _val = self._result(STALE)
        assert res["margin"]["debt"] == 200.0
        assert res["margin"]["buffer_pct"] == 60.0

    def test_a_usable_observation_still_produces_a_real_state(self):
        """The complement: this withholds nothing when the reading is current."""
        res, ms, _val = self._result(FRESH)
        assert ms["usable"] is True
        assert res["margin"]["net_equity"] is not None
        assert res["margin"]["leverage_current"] is not None

    def test_margin_state_py_still_has_exactly_four_states(self):
        """The advisory is NOT a fifth state value.

        Widening `margin_state.py`'s own vocabulary would let an unavailability
        marker travel anywhere a real state can. It stays four.
        """
        import margin_state as MS
        assert MS.STATES == ("NORMAL", "CAUTION", "RESTRICTED", "FORCED_DELEVER")

    def test_removing_the_usable_gate_makes_this_class_fail(self):
        """MUTATION PROBE."""
        src = inspect.getsource(A.main)
        assert "_classifiable and bool(margin_state" in src
