from datetime import date, timedelta
from decimal import Decimal as D
import math
import pytest
from pathlib import Path
from whole_portfolio_robustness_v2_engine import *
from whole_portfolio_robustness_v2_engine import _cell_ids, _rebalance_day

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
    closes={date(2021,6,7):__import__('datetime').datetime.fromisoformat('2021-06-07T20:00:00+00:00')}
    assert align_crypto(bars,[date(2021,6,7)],closes)["2021-06-07"]==10

def test_metrics_undefined_variance_is_nonfinite():
    m=metrics([.01,.01,.01],elapsed_days=3);assert math.isnan(m['sharpe'])

def test_subwindow_requires_and_uses_preceding_anchor():
    rows=[{'date':'2025-01-02','anchor_nav':'200000','anchor_date':'2024-12-31','nav':'200000','events':[],'risk_free_return':'0'},{'date':'2025-01-03','nav':'199000','events':[],'risk_free_return':'0'}]
    assert complete_metrics(rows)['cumulative_twr']==pytest.approx(-.005)
    with pytest.raises(ValueError):complete_metrics([{k:v for k,v in row.items() if k!='anchor_nav'} for row in rows])

def test_recovery_days_is_peak_to_first_full_recovery_and_censors():
    recovered=[{'date':'2025-01-02','anchor_nav':'100000','anchor_date':'2024-12-31','nav':'100000','risk_free_return':'0'}, {'date':'2025-01-03','nav':'99000','risk_free_return':'0'}, {'date':'2025-01-13','nav':'100000','risk_free_return':'0'}]
    assert complete_metrics(recovered)['recovery_days']==11
    unrecovered=[*recovered[:-1],{'date':'2025-01-13','nav':'98000','risk_free_return':'0'}]
    assert complete_metrics(unrecovered)['recovery_days'] is None
    flat=[recovered[0],{'date':'2025-01-03','nav':'100000','risk_free_return':'0'}]
    assert complete_metrics(flat)['recovery_days']==0
    multiple=[{'date':'2025-01-02','anchor_nav':'100000','anchor_date':'2024-12-31','nav':'100000','risk_free_return':'0'}, {'date':'2025-01-03','nav':'99000','risk_free_return':'0'}, {'date':'2025-01-06','nav':'100000','risk_free_return':'0'}, {'date':'2025-01-07','nav':'97000','risk_free_return':'0'}, {'date':'2025-01-13','nav':'100000','risk_free_return':'0'}]
    assert complete_metrics(multiple)['recovery_days']==7

def test_calendar_cagr_and_excess_downside_use_dated_boundary():
    rows=[{'date':'2025-01-02','anchor_nav':'100','anchor_date':'2024-12-31','nav':'101','risk_free_return':'.02'},
          {'date':'2025-01-06','nav':'100.5','risk_free_return':'.02'}]
    result=complete_metrics(rows,[.02,.02])
    assert result['net_twr_cagr']==pytest.approx(1.005**(365.2425/6)-1)
    returns=[.01,100.5/101-1]
    expected=(sum(min(r-.02,0)**2 for r in returns)/2)**.5*math.sqrt(252)
    assert result['downside_deviation']==pytest.approx(expected)
    with pytest.raises(ValueError):metrics(returns,[.02,.02],elapsed_days=0)

def test_stationary_bootstrap_is_deterministic_and_paired():
    b=[-.02,.01,.03,-.01]*8;a=[-.01,.012,.031,-.005]*8;rf=[.0001]*32
    assert stationary_bootstrap(b,a,rf,draws=50,elapsed_days=32)==stationary_bootstrap(b,a,rf,draws=50,elapsed_days=32)

def test_support_14_vs_15_and_context_cannot_replace_correction():
    boot={"NET_TWR_CAGR_DELTA":.8,"SHARPE_DELTA":.8,"MAX_DRAWDOWN_DELTA":.8,"DAILY_CVAR_95_DELTA":0}
    assert not decide_variant(cells(14),good(),good(),boot,True,True)
    assert decide_variant(cells(15),good(),good(),boot,True,True)
    # Context has 18 hypothetical supports; correction still owns the only support count.
    assert not decide_variant(cells(0),good(),good(),boot,True,True)

def test_primary_and_linked_tail_must_pass():
    boot={"NET_TWR_CAGR_DELTA":.8,"SHARPE_DELTA":.8,"MAX_DRAWDOWN_DELTA":.2,"DAILY_CVAR_95_DELTA":.8}
    context=good();context['daily_cvar_95_delta_pp']=-1
    assert not decide_variant(cells(),good(),context,boot,True,True)
    assert not decide_variant(cells(),good(False),good(),boot,True,True)

def test_adversarial_registry_nonfinite_probability_and_string_boolean():
    boot={"NET_TWR_CAGR_DELTA":.8,"SHARPE_DELTA":.8,"MAX_DRAWDOWN_DELTA":.8,"DAILY_CVAR_95_DELTA":0}
    bad=cells();bad[0]["cell_id"]="UNREGISTERED"
    with pytest.raises(ValueError):decide_variant(bad,good(),good(),boot,True,True)
    bad=cells();bad[-1]["sharpe_delta"]=math.nan
    with pytest.raises(ValueError):decide_variant(bad,good(),good(),boot,True,True)
    with pytest.raises(ValueError):decide_variant(cells(),good(),good(),dict(boot,MAX_DRAWDOWN_DELTA=math.inf),True,True)
    cases={c:{a:'False' for a in ALTERNATIVES} for c in FOREIGN_CASES}
    assert disposition(cases)["disposition"]=="UNABLE_TO_DETERMINE"

def test_bootstrap_undefined_sharpe_fails_closed():
    with pytest.raises(ValueError):stationary_bootstrap([.01]*4,[.02]*4,[0.]*4,draws=10,elapsed_days=4)

def test_crypto_close_after_session_is_deferred():
    bars=[{"close_at":"2021-06-07T00:00:00Z","close":1},{"close_at":"2021-06-07T22:00:00Z","close":2}]
    closes={date(2021,6,7):__import__('datetime').datetime.fromisoformat('2021-06-07T20:00:00+00:00')}
    assert align_crypto(bars,[date(2021,6,7)],closes)["2021-06-07"]==1

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
    fixture={'start':days[0],'end':days[-1],'sessions':days,'session_closes':{d:d+'T21:00:00Z' for d in days},'prices':{t:{d:'100' for d in days} for t in tickers},'fed_business_days':['2025-01-01','2025-01-02'],'dff_records':[{'observation_date':'2024-12-31','published_at':'2025-01-01T16:15:00Z','value':'5'}]}
    for variant in ('BASELINE',)+ALTERNATIVES:
        result=simulate(root,fixture,variant=variant,cost_bps=D(0))
        assert result['initial_nav']=='100000' and len(result['ledger'])==2
        assert all(D(row['cash'])>=0 for row in result['ledger'])
        assert sum(D(v) for v in result['weights'].values())==1

def test_integrated_golden_initial_cost_weekend_payable_and_split():
    root=Path(__file__).parent;days=['2025-01-02','2025-01-03','2025-01-06'];tickers=[t for t in derive_weights(root,'BASELINE') if t!='CASH']
    fixture={'start':'2025-01-02','end':'2025-01-06','sessions':days,'session_closes':{d:d+'T21:00:00Z' for d in days},'prices':{t:{d:'100' for d in days} for t in tickers},'fed_business_days':['2025-01-01','2025-01-02'],'dff_records':[{'observation_date':'2024-12-31','published_at':'2025-01-01T16:15:00Z','value':'.25'}],'dividends':[{'ticker':'TMO','ex_date':'2025-01-03','payable_date':'2025-01-04','gross_per_share':'1','withholding_rate':'0'}],'splits':[{'ticker':'NVDA','date':'2025-01-06','factor':'10'}]}
    result=simulate(root,fixture,profile={k:D(0) for k in ('ordinary_income_rate','qualified_dividend_rate','qualified_dividend_fraction','short_gain_rate','long_gain_rate','gold_gain_rate')},cost_bps=D(10))
    assert D(result['ledger'][0]['nav'])==D('99912.5000')
    assert result['summary']['cumulative_twr']==pytest.approx(float(D(result['ledger'][-1]['nav'])/D(100000)-1))
    assert any(e['type']=='receivable_settlement' for e in result['calendar_ledger'][2]['events'])
    assert result['calendar_ledger'][2]['date']=='2025-01-04'
    from whole_portfolio_robustness_v2_result_validator import validate_ledger
    assert validate_ledger(result)==[]
    fixture['dividends'][0]['payable_date']='2025-01-07'
    unpaid=simulate(root,fixture,profile={k:D(0) for k in ('ordinary_income_rate','qualified_dividend_rate','qualified_dividend_fraction','short_gain_rate','long_gain_rate','gold_gain_rate')},cost_bps=D(10))
    assert unpaid['ledger'][-1]['receivables'] and not any(e['type']=='receivable_settlement' for row in unpaid['calendar_ledger'] for e in row['events'])

def test_quarterly_first_session_boundaries():
    sessions=list(map(date.fromisoformat,['2025-02-28','2025-03-03','2025-03-31','2025-04-01']))
    assert not _rebalance_day(sessions[1],'QUARTERLY',sessions)
    assert _rebalance_day(sessions[3],'QUARTERLY',sessions)

def test_exact_close_required_and_later_available_asset_stays_cash():
    with pytest.raises(ValueError):align_crypto([{'close_at':'2025-07-03T19:00:00Z','close':999}],[date(2025,7,3)])
    root=Path(__file__).parent;fixture=full_synthetic_fixture()
    simulate(root,fixture,cost_bps=D(0))

def test_pinned_fund_lookthrough_is_used():
    import yaml
    look=yaml.safe_load(Path('issuer_lookthrough.yaml').read_text())
    result=concentration({'nav':'100','positions':[{'ticker':'SPY','shares':'1','price':'100'}]},look)
    assert result['effective_issuer_max']==pytest.approx(.0766) and result['ai_platform_common_driver']>0

@pytest.mark.parametrize('sleeve',['GLD','BTC','ETH','SOL'])
def test_non_issuer_sleeves_do_not_control_effective_issuer_max(sleeve):
    import yaml
    look=yaml.safe_load(Path('issuer_lookthrough.yaml').read_text())
    positions=[{'ticker':'COST','shares':'1','price':'6'},{'ticker':'NVDA','shares':'1','price':'3'},
               {'ticker':'SPY','shares':'1','price':'10'},{'ticker':sleeve,'shares':'1','price':'35'}]
    result=concentration({'nav':'100','positions':positions},look)
    assert result['effective_issuer_max']==pytest.approx(.06)

def test_concentration_uses_independent_window_maxima_not_same_day_pairs():
    keys=('direct_hhi','max_direct_name','effective_issuer_max','ai_platform_common_driver','semis_cluster','power_infra_cluster')
    def row(hhi,name):return dict(zip(keys,(hhi,name,name,name,.10,.10)))
    baseline=[row(.10,.20),row(.05,.10)];alternative=[row(.06,.15),row(.07,.16)]
    assert concentration_window_pass(baseline,alternative)
    bad=[dict(x) for x in alternative];bad[1]['semis_cluster']=.2501
    assert not concentration_window_pass(baseline,bad)

def test_etn_withholding_cases_and_action_registry_fail_closed():
    root=Path(__file__).parent;fixture=full_synthetic_fixture();fixture['end']='2023-01-16'
    fixture['sessions']=[d for d in fixture['sessions'] if d<=fixture['end']];fixture['session_closes']={d:v for d,v in fixture['session_closes'].items() if d<=fixture['end']}
    for ticker in fixture['prices']:fixture['prices'][ticker]={d:v for d,v in fixture['prices'][ticker].items() if d<=fixture['end']}
    for ticker in fixture['crypto_bars']:fixture['crypto_bars'][ticker]=[x for x in fixture['crypto_bars'][ticker] if x['close_at'][:10]<=fixture['end']]
    fixture['splits']=[]
    observed={}
    for case in FOREIGN_CASES:
        result=simulate(root,fixture,'BASELINE',D(0),foreign_case=case)
        event=next(e for row in result['calendar_ledger'] for e in row['events'] if e['type']=='dividend_recognition')
        settlement=next(e for row in result['calendar_ledger'] for e in row['events'] if e['type']=='receivable_settlement')
        gross=D(event['gross']);observed[case]=(D(event['withholding'])/gross,D(event['foreign_tax_credit'])/gross,D(event['us_tax'])/gross,D(settlement['net']))
    assert observed[FOREIGN_CASES[0]][0]==0 and observed[FOREIGN_CASES[1]][0]==0
    assert observed[FOREIGN_CASES[2]][0]==D('.25') and observed[FOREIGN_CASES[3]][0]==D('.25')
    assert observed[FOREIGN_CASES[2]][1]>0 and observed[FOREIGN_CASES[3]][1]==0
    original=fixture['dividends'][0]
    attacks=[dict(original,gross_per_share=x) for x in (0,-1,True,'NaN')]
    attacks += [dict(original,withholding_rate=x) for x in (True,'Infinity')]
    attacks += [dict(original,ex_date='2023-02-30'),dict(original,ex_date='2023-01-15'),dict(original,payable_date='2023-01-12')]
    for bad in attacks:
        fixture['dividends']=[bad]
        with pytest.raises(ValueError):simulate(root,fixture,'BASELINE',D(0))
    fixture['dividends']=[original,dict(original)]
    with pytest.raises(ValueError,match='duplicate'):simulate(root,fixture,'BASELINE',D(0))
    fixture['dividends']=[original];split={'ticker':'NVDA','date':'2023-01-13','factor':'2'}
    for bad in (0,-1,True,'NaN'):
        fixture['splits']=[dict(split,factor=bad)]
        with pytest.raises(ValueError):simulate(root,fixture,'BASELINE',D(0))
    fixture['splits']=[split,dict(split)]
    with pytest.raises(ValueError,match='duplicate'):simulate(root,fixture,'BASELINE',D(0))
    fixture['splits']=[];assert len(simulate(root,fixture,'BASELINE',D(0))['ledger'])==len(fixture['sessions'])

def test_wrong_windows_or_empty_regimes_fail_closed():
    with pytest.raises(ValueError):evaluate_study(synthetic_study_paths(),[])

REGIMES=[{'id':'RATE_INFLATION_2022','start':'2022-01-03','end':'2022-12-30'},{'id':'CALENDAR_2023','start':'2023-01-03','end':'2023-12-29'},{'id':'CALENDAR_2024','start':'2024-01-02','end':'2024-12-31'},{'id':'CALENDAR_2025','start':'2025-01-02','end':'2025-12-31'},{'id':'CALENDAR_2026_PARTIAL','start':'2026-01-02','end':'2026-07-31'}]

def synthetic_study_paths():
    dates=['2021-06-01','2021-07-01','2022-01-03','2022-06-01','2022-12-30','2023-01-03','2023-06-01','2023-12-29','2024-01-02','2024-04-02','2024-08-01','2024-12-31','2025-01-02','2025-06-02','2025-12-31','2026-01-02','2026-04-01','2026-07-31']
    full=[{'date':d,'nav':str(D(100000)+D((i%4)-1)*D(1000)+D(i)*10),'cash':str(D(100000)+D((i%4)-1)*D(1000)+D(i)*10),'positions':[],'events':[],'risk_free_return':'.00001'} for i,d in enumerate(dates)]
    windows={'full':full,'context':[x for x in full if '2021-06-01'<=x['date']<='2023-12-29'],'correction_replication':[x for x in full if '2024-04-02'<=x['date']<='2026-07-31']}
    return {case:{cell:{alt:{k:list(v) for k,v in windows.items()} for alt in ('BASELINE',)+ALTERNATIVES} for cell in _cell_ids()} for case in FOREIGN_CASES}

def test_complete_synthetic_registry_driver_is_deterministic():
    with pytest.raises(ValueError):evaluate_study(synthetic_study_paths(),REGIMES)

def test_evaluate_study_fixed_regimes_inherit_complete_predecessor_boundary(monkeypatch):
    import json
    import whole_portfolio_robustness_v2_engine as engine
    sessions=[x['session'] for x in json.loads((Path(__file__).parent/'research/level1_sleeve_robustness/data/transformed/XNYS_sessions.json').read_text())['sessions'] if '2021-06-01'<=x['session']<='2026-07-31']
    zero={k:'0' for k in ('turnover_notional','rebalance_count','taxable_realized_gain','cost_drag','tax_drag','cash_drag')}
    full=[]
    for i,day in enumerate(sessions):
        row={'date':day,'nav':str(D(100000)+D(i%11-5)*10+D(i)),'risk_free_return':'.00001','operations':dict(zero),'concentration':{k:0. for k in ('direct_hhi','max_direct_name','effective_issuer_max','ai_platform_common_driver','semis_cluster','power_infra_cluster')}}
        if i==0:row.update(anchor_nav='100000',anchor_date='2021-05-28',anchor_operations=dict(zero))
        full.append(row)
    def window(start,end):
        selected=[dict(x) for x in full if start<=x['date']<=end];first=next(i for i,x in enumerate(full) if x['date']==selected[0]['date'])
        selected[0].update(anchor_nav='100000' if first==0 else full[first-1]['nav'],anchor_date='2021-05-28' if first==0 else full[first-1]['date'],anchor_operations=dict(zero) if first==0 else full[first-1]['operations'])
        return selected
    windows={'full':window('2021-06-01','2026-07-31'),'context':window('2021-06-01','2023-12-29'),'correction_replication':window('2024-04-02','2026-07-31')}
    primary='COST_10_TAX_TAXABLE_MID_CADENCE_QUARTERLY';monkeypatch.setattr(engine,'_cell_ids',lambda:(primary,));monkeypatch.setattr(engine,'stationary_bootstrap',lambda *a,**k:{x:0. for x in ('NET_TWR_CAGR_DELTA','SHARPE_DELTA','MAX_DRAWDOWN_DELTA','DAILY_CVAR_95_DELTA')})
    boundaries=[];real_complete=engine.complete_metrics
    def checked_complete(rows,risk_free=None):
        if rows[0]['date']=='2023-01-03':boundaries.append((rows[0]['anchor_date'],rows[0]['anchor_nav'],rows[0]['anchor_operations']))
        return real_complete(rows,risk_free)
    monkeypatch.setattr(engine,'complete_metrics',checked_complete)
    seen=[];real=engine.fixed_evaluations
    def checked(rows,regimes):
        result=real(rows,regimes);seen.append(result)
        assert result['CALENDAR_2023']['recovery_days'] is not None
        return result
    monkeypatch.setattr(engine,'fixed_evaluations',checked)
    paths={case:{primary:{variant:{name:[dict(x) for x in rows] for name,rows in windows.items()} for variant in ('BASELINE',)+ALTERNATIVES}} for case in FOREIGN_CASES}
    result=engine.evaluate_study(paths,REGIMES)
    assert result['decision_evidence']['cases'] and len(seen)==len(FOREIGN_CASES)*len(ALTERNATIVES)*2
    predecessor=next(x for x in full if x['date']=='2022-12-30')
    assert boundaries and all(x==('2022-12-30',predecessor['nav'],predecessor['operations']) for x in boundaries)

def full_synthetic_fixture():
    import json
    sessions=[x for x in json.loads((Path(__file__).parent/'research/level1_sleeve_robustness/data/transformed/XNYS_sessions.json').read_text())['sessions'] if '2021-06-01'<=x['session']<='2026-07-31']
    dates=[x['session'] for x in sessions]
    tickers=[t for t in derive_weights(Path(__file__).parent,'BASELINE') if t!='CASH']
    prices={t:{d:str(D(100)+D(i%17-8)/10+D(j%5)) for i,d in enumerate(dates) if t!='CEG' or d>='2022-02-02'} for j,t in enumerate(tickers)}
    crypto_bars={}
    for ticker in ('BTC','ETH','SOL'):
        bars=[];day=date(2021,6,1);last=None
        while day<=date(2026,7,31):
            if day.isoformat() in prices[ticker]:last=prices[ticker][day.isoformat()]
            bars.append({'close_at':day.isoformat()+'T00:00:00Z','close':last});day+=timedelta(days=1)
        crypto_bars[ticker]=bars
    return {'input_kind':'SYNTHETIC_TEST_ONLY','start':'2021-06-01','end':'2026-07-31','anchor_date':'2021-05-28','sessions':dates,'session_closes':{x['session']:x['close_utc'] for x in sessions},'prices':prices,'crypto_bars':crypto_bars,'available':{'CEG':'2022-02-02'},'fed_business_days':['2021-05-31'],'dff_records':[{'observation_date':'2021-05-28','published_at':'2021-05-31T16:15:00Z','value':'.25'}],'dividends':[{'ticker':'ETN','ex_date':'2023-01-13','payable_date':'2023-01-14','gross_per_share':'1','withholding_rate':'.10'}],'splits':[{'ticker':'NVDA','date':'2024-06-10','factor':'10'}]}

_FULL_BUNDLE=None
def get_full_bundle():
    global _FULL_BUNDLE
    if _FULL_BUNDLE is None:_FULL_BUNDLE=run_synthetic_study(Path(__file__).parent,full_synthetic_fixture())
    return _FULL_BUNDLE

def test_full_simulation_registry_driver_executes_synthetic_fixture():
    result=get_full_bundle()
    assert result['synthetic'] is True and len(result['simulations'])==4
    assert all(len(cells)==18 for cells in result['simulations'].values())
    from whole_portfolio_robustness_v2_result_validator import validate_study_bundle
    assert validate_study_bundle(result)==[]
