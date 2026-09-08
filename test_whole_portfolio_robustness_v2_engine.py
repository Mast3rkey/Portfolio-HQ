from datetime import date
from decimal import Decimal as D
import math
import pytest
from pathlib import Path
from whole_portfolio_robustness_v2_engine import *
from whole_portfolio_robustness_v2_engine import _cell_ids

def good(delta=True):
    return {"net_cagr_delta_pp":0,"sharpe_delta":.1,"sortino_delta":.1,"max_drawdown_delta_pp":2 if delta else 0,"daily_cvar_95_delta_pp":0}

def cells(n=18):
    result=[]
    for i,identity in enumerate(_cell_ids()): result.append(dict(good(i<n),cell_id=identity,window="correction_replication"))
    return result

def test_cash_formula_positive_zero_negative():
    assert str(cash_delta(D(100),D(5),D('.24'))).startswith('0.009861111111111111111111111111')
    assert str(cash_delta(D(100),D(0),D('.24'))).startswith('-0.0006944444444444444444444444444')
    assert str(cash_delta(D(100),D(-1),D('.24'))).startswith('-0.003472222222222222222222222222')

def test_non_xnys_settlement_and_weekend_credit_clock():
    ds={date(2025,1,9)+__import__('datetime').timedelta(days=i):D(5) for i in range(5)}
    rows=run_cash_clock(date(2025,1,9),date(2025,1,13),D(0),{date(2025,1,9):D(100)},ds,D('.24'),{date(2025,1,10),date(2025,1,13)})
    assert D(rows[1]["nav"])==100
    assert str(rows[-1]["nav"]).startswith('100.029586250674594639489026')

def test_missing_rate_fails():
    with pytest.raises(ValueError):run_cash_clock(date(2025,1,1),date(2025,1,1),D(1),{}, {},D(0),set())

def test_hifo_and_no_loss_credit_and_gold_character():
    lots=[Lot(D(1),D(10),date(2020,1,1)),Lot(D(1),D(20),date(2024,12,1))]
    gain,tax,rec=hifo_sell(lots,D('1.5'),D(15),date(2025,1,1),D('.3'),D('.2'))
    assert rec[0]["basis"]=='20' and tax==D('.5') and gain==D('2.5')
    _,gold_tax,_=hifo_sell([Lot(D(1),D(10),date(2020,1,1))],D(1),D(20),date(2025,1,1),D('.3'),D('.2'),gold_rate=D('.28'))
    assert gold_tax==D('2.80')

def test_funding_never_borrows():
    units,cost,cash=funded_purchase(D(100),D(200),D(10),D(10))
    assert cash==0 and units*10+cost==100

def test_dividend_ftc_and_entitlement():
    x=dividend_net(D(2),D(1),D('.1'),D('.8'),D('.15'),D('.24'))
    assert x['foreign_tax_credit']==D('.2') and x['net_receivable']==D('1.664')

def test_crypto_actual_close_prevents_weekend_future_lookahead():
    bars=[{"close_at":"2021-06-05T00:00:00Z","close":"10"},{"close_at":"2021-06-08T00:00:00Z","close":"20"}]
    assert align_crypto(bars,[date(2021,6,7)])["2021-06-07"]==10

def test_metrics_undefined_variance_is_nonfinite():
    m=metrics([.01,.01,.01]);assert math.isnan(m['sharpe'])

def test_stationary_bootstrap_is_deterministic_and_paired():
    b=[-.02,.01,.03,-.01]*8;a=[-.01,.012,.031,-.005]*8;rf=[.0001]*32
    assert stationary_bootstrap(b,a,rf,draws=50)==stationary_bootstrap(b,a,rf,draws=50)

def test_support_14_vs_15_and_context_cannot_replace_correction():
    boot={"SHARPE_DELTA":.8,"MAX_DRAWDOWN_DELTA":.8,"DAILY_CVAR_95_DELTA":0}
    assert not decide_variant(cells(14),good(),good(),boot,True,True)
    assert decide_variant(cells(15),good(),good(),boot,True,True)
    # Context has 18 hypothetical supports; correction still owns the only support count.
    assert not decide_variant(cells(0),good(),good(),boot,True,True)

def test_primary_and_linked_tail_must_pass():
    boot={"SHARPE_DELTA":.8,"MAX_DRAWDOWN_DELTA":.2,"DAILY_CVAR_95_DELTA":.8}
    context=good();context['daily_cvar_95_delta_pp']=-1
    assert not decide_variant(cells(),good(),context,boot,True,True)
    assert not decide_variant(cells(),good(False),good(),boot,True,True)

def test_adversarial_registry_nonfinite_probability_and_string_boolean():
    boot={"SHARPE_DELTA":.8,"MAX_DRAWDOWN_DELTA":.8,"DAILY_CVAR_95_DELTA":0}
    bad=cells();bad[0]["cell_id"]="UNREGISTERED"
    with pytest.raises(ValueError):decide_variant(bad,good(),good(),boot,True,True)
    bad=cells();bad[-1]["sharpe_delta"]=math.nan
    with pytest.raises(ValueError):decide_variant(bad,good(),good(),boot,True,True)
    with pytest.raises(ValueError):decide_variant(cells(),good(),good(),dict(boot,MAX_DRAWDOWN_DELTA=math.inf),True,True)
    cases={c:{a:'False' for a in ALTERNATIVES} for c in FOREIGN_CASES}
    assert disposition(cases)["disposition"]=="UNABLE_TO_DETERMINE"

def test_bootstrap_undefined_sharpe_fails_closed():
    with pytest.raises(ValueError):stationary_bootstrap([.01]*4,[.02]*4,[0.]*4,draws=10)

def test_crypto_close_after_session_is_deferred():
    bars=[{"close_at":"2021-06-07T00:00:00Z","close":1},{"close_at":"2021-06-07T22:00:00Z","close":2}]
    assert align_crypto(bars,[date(2021,6,7)])["2021-06-07"]==1

def test_dff_publication_later_that_day_not_available_at_midnight():
    fed={date(2025,1,2),date(2025,1,3)}
    records=[{'observation_date':'2025-01-02','published_at':'2025-01-03T16:15:00Z','value':'9'},
             {'observation_date':'2024-12-31','published_at':'2025-01-02T16:15:00Z','value':'1'}]
    assert lawful_dff(records,[date(2025,1,3),date(2025,1,4)],fed)=={date(2025,1,3):D(1),date(2025,1,4):D(9)}

def test_multiple_passers_and_every_foreign_veto():
    standard={a:a in ALTERNATIVES[:2] for a in ALTERNATIVES}
    cases={c:dict(standard) for c in FOREIGN_CASES}
    assert disposition(cases)=={"disposition":"RECOMMEND_POLICY_REVIEW","passing_set":list(ALTERNATIVES[:2])}
    for case in FOREIGN_CASES[1:]:
        altered={c:dict(standard) for c in FOREIGN_CASES};altered[case][ALTERNATIVES[0]]=False
        assert disposition(altered)['disposition']=='UNABLE_TO_DETERMINE'

def test_integrated_simulation_derives_all_constructions_and_conserves():
    root=Path(__file__).parent
    tickers=[t for t in derive_weights(root,'BASELINE') if t!='CASH']
    days=['2025-01-02','2025-01-03']
    fixture={'start':days[0],'end':days[-1],'sessions':days,'prices':{t:{d:'100' for d in days} for t in tickers},'dff':{d:'5' for d in days}}
    for variant in ('BASELINE',)+ALTERNATIVES:
        result=simulate(root,fixture,variant=variant,cost_bps=D(0))
        assert result['initial_nav']=='100000' and len(result['ledger'])==2
        assert all(D(row['cash'])>=0 for row in result['ledger'])
        assert sum(D(v) for v in result['weights'].values())==1
