from copy import deepcopy
import pytest
from whole_portfolio_robustness_v2_result_validator import *
from whole_portfolio_robustness_v2_result_validator import _XNYS, _SUMMARY_FIELDS, _compare_metric_tree, _compare_probability_claim, _concentration, _concentration_window_pass, _derived_windows, _fixed_evaluations, _path_identity, _path_stats, _replay_simulation

def test_replay_window_derivation_binds_predecessor_and_every_field():
    full=[]
    for item in _XNYS:
        if '2021-06-01'<=item['session']<='2026-07-31':
            full.append({'date':item['session'],'nav':str(100000+len(full)),
                         'risk_free_return':'0.0001','concentration':{'effective_issuer_max':.06},
                         'operations':{'turnover_notional':'0','rebalance_count':'0','taxable_realized_gain':'0','cost_drag':'0','tax_drag':'0','cash_drag':'0'}})
    full[0]['anchor_date']='2021-05-28'
    windows=_derived_windows(full);correction=windows['correction_replication']
    first=next(i for i,x in enumerate(full) if x['date']==correction[0]['date'])
    assert correction[0]['anchor_nav']==full[first-1]['nav']
    detached=deepcopy(correction);detached[0]['nav']='999999'
    assert _path_identity(detached)!=_path_identity(correction)

def test_validator_effective_issuer_excludes_non_issuer_sleeves():
    for sleeve in ('GLD','BTC','ETH','SOL'):
        result=_concentration(D('100'),{'COST':D(1),'NVDA':D(1),'SPY':D(1),sleeve:D(1)},
                              {'COST':D(6),'NVDA':D(3),'SPY':D(10),sleeve:D(35)})
        assert result['effective_issuer_max']==.06

def test_primitive_replay_rejects_source_and_stored_economic_mutations():
    """A full-calendar simulation is bound to independent source reconstruction."""
    from pathlib import Path
    import yaml
    import whole_portfolio_robustness_v2_engine as engine
    from test_whole_portfolio_robustness_v2_engine import full_synthetic_fixture
    fixture=full_synthetic_fixture();prereg=yaml.safe_load(Path('research/whole_portfolio_robustness_v2/pre_registration.yaml').read_text());cell=prereg['frictions']['cell_registry'][0]
    profile={key:D(value) for key,value in prereg['frictions']['tax_profile_parameters'][cell['tax_profile']].items()}
    actual=engine.simulate(Path('.'),fixture,'BASELINE',D(cell['one_way_cost_bps']),profile,cell['rebalance_cadence'],CASES[0])
    expected=_replay_simulation(fixture,CASES[0],cell['cell_id'],'BASELINE')
    projection=lambda rows:[{k:v for k,v in row.items() if not k.startswith('_')} for row in rows]
    assert [row for row in actual['calendar_ledger'] if row['events']]==expected['calendar_ledger']
    compact=[]
    for row in actual['ledger']:
        keep={key:row[key] for key in ('date','nav','cash','risk_free_return','operations')}
        if 'anchor_operations' in row:keep['anchor_operations']=row['anchor_operations']
        if row.get('anchor_date') is not None:keep['anchor_date']=row['anchor_date']
        if row.get('events'):keep.update(events=row['events'],positions=row['positions'],receivables=row['receivables'])
        compact.append(keep)
    assert compact==projection(expected['ledger'])
    original_anchor=fixture['anchor_date'];fixture['anchor_date']='2026-08-03'
    with pytest.raises(ValueError,match='retained XNYS predecessor'):_replay_simulation(fixture,CASES[0],cell['cell_id'],'BASELINE')
    with pytest.raises(ValueError,match='retained XNYS predecessor'):engine.simulate(Path('.'),fixture,'BASELINE',D(cell['one_way_cost_bps']),profile,cell['rebalance_cadence'],CASES[0])
    fixture['anchor_date']=original_anchor
    assert _replay_simulation(fixture,CASES[0],cell['cell_id'],'BASELINE')==expected
    for bad in (True,None,'not-a-date','2021-06-01','2021-05-27'):
        fixture['anchor_date']=bad
        with pytest.raises((ValueError,TypeError)):_replay_simulation(fixture,CASES[0],cell['cell_id'],'BASELINE')
    fixture['anchor_date']=original_anchor
    assert set(actual['summary'])==set(_SUMMARY_FIELDS)
    claimed=deepcopy(actual['summary']);claimed['annualized_volatility']=True
    assert _compare_metric_tree(actual['summary'],claimed,'summary')
    del claimed['worst_year'];assert _compare_metric_tree(actual['summary'],claimed,'summary')
    for collection,key,value in ((fixture['dff_records'][0],'value','5'),(fixture['dividends'][0],'gross_per_share','2'),(fixture['splits'][0],'factor','2')):
        original=collection[key];collection[key]=value
        changed=_replay_simulation(fixture,CASES[0],cell['cell_id'],'BASELINE')
        assert changed!=expected
        collection[key]=original
        assert _replay_simulation(fixture,CASES[0],cell['cell_id'],'BASELINE')==expected
    btc=fixture['crypto_bars']['BTC'][7];original=btc['close'];btc['close']=str(D(original)*2)
    with pytest.raises(ValueError,match='detached from bars'):_replay_simulation(fixture,CASES[0],cell['cell_id'],'BASELINE')
    btc['close']=original;assert _replay_simulation(fixture,CASES[0],cell['cell_id'],'BASELINE')==expected
    for bad in (True,'NaN','Infinity','0'):
        original=btc['close'];btc['close']=bad
        with pytest.raises(ValueError):_replay_simulation(fixture,CASES[0],cell['cell_id'],'BASELINE')
        btc['close']=original
    removed=fixture['crypto_bars']['ETH'].pop(10)
    with pytest.raises(ValueError,match='coverage/order'):_replay_simulation(fixture,CASES[0],cell['cell_id'],'BASELINE')
    fixture['crypto_bars']['ETH'].insert(10,removed)
    original=removed['close_at'];removed['close_at']='2021-06-11T22:00:00-04:00'
    with pytest.raises(ValueError):_replay_simulation(fixture,CASES[0],cell['cell_id'],'BASELINE')
    removed['close_at']=original;assert _replay_simulation(fixture,CASES[0],cell['cell_id'],'BASELINE')==expected
    mutated=deepcopy(compact);row=next(x for x in mutated if x.get('positions'));row['positions'][0]['lots'][0]['basis']='999999'
    assert mutated!=projection(expected['ledger'])

def test_independent_replay_etn_cases_and_malformed_actions():
    from test_whole_portfolio_robustness_v2_engine import full_synthetic_fixture
    fixture=full_synthetic_fixture();cell='COST_0_TAX_TAXABLE_MID_CADENCE_QUARTERLY'
    for case in CASES:
        replay=_replay_simulation(fixture,case,cell,'BASELINE')
        event=next(e for row in replay['calendar_ledger'] for e in row['events'] if e['type']=='dividend_recognition')
        ratio=D(event['withholding'])/D(event['gross'])
        assert ratio==(D('.25') if 'ETN_25' in case else D(0))
        assert (D(event['foreign_tax_credit'])>0)==('ZERO' not in case and 'ETN_25' in case)
        assert any(e['type']=='receivable_settlement' for row in replay['calendar_ledger'] for e in row['events'])
    dividend=fixture['dividends'][0];split=fixture['splits'][0]
    dividend_attacks=[dict(dividend,gross_per_share=x) for x in (0,-1,True,'NaN')]
    dividend_attacks += [dict(dividend,withholding_rate=True),dict(dividend,ex_date='2023-02-30'),dict(dividend,ex_date='2023-01-15'),dict(dividend,payable_date='2023-01-12')]
    for bad in dividend_attacks:
        fixture['dividends']=[bad]
        with pytest.raises(ValueError):_replay_simulation(fixture,CASES[0],cell,'BASELINE')
    fixture['dividends']=[dividend,dict(dividend)]
    with pytest.raises(ValueError,match='duplicate'):_replay_simulation(fixture,CASES[0],cell,'BASELINE')
    fixture['dividends']=[dividend]
    for bad in (0,-1,True,'NaN'):
        fixture['splits']=[dict(split,factor=bad)]
        with pytest.raises(ValueError):_replay_simulation(fixture,CASES[0],cell,'BASELINE')
    fixture['splits']=[split,dict(split)]
    with pytest.raises(ValueError,match='duplicate'):_replay_simulation(fixture,CASES[0],cell,'BASELINE')
    fixture['splits']=[split]
    assert _replay_simulation(fixture,CASES[0],cell,'BASELINE')

def test_independent_replay_reconstructs_post_friction_targets_and_price_basis():
    from test_whole_portfolio_robustness_v2_engine import full_synthetic_fixture
    fixture=full_synthetic_fixture();cell='COST_10_TAX_TAXABLE_MID_CADENCE_QUARTERLY'
    replay=_replay_simulation(fixture,CASES[0],cell,'BASELINE');first=replay['ledger'][0]
    assert abs(D(first['nav'])-D(100000)/(D(1)+D('.001')*D('.86')))<D('.000001')
    assert all(D(lot['basis'])==D(position['price']) for position in first['_positions'] for lot in position['lots'])
    july=next(row for row in replay['calendar_ledger'] if row['date']=='2021-07-01')
    sale=next(event for event in july['events'] if event['type']=='sell' and event['ticker']=='NVDA');lot=sale['lots'][0]
    assert D(lot['gain'])==D(lot['units'])*(D(sale['price'])-D(lot['basis']))
    assert D(lot['tax'])==D(lot['gain'])*D(lot['rate'])

def test_independent_replay_accepts_converged_shock_after_provisional_shortfall():
    from test_whole_portfolio_robustness_v2_engine import full_synthetic_fixture
    fixture=full_synthetic_fixture();original=dict(fixture['prices']['NVDA']);cell='COST_10_TAX_TAXABLE_HIGH_CADENCE_QUARTERLY'
    positive=_replay_simulation(fixture,CASES[0],cell,'BASELINE')
    for day,value in fixture['prices']['NVDA'].items():
        if day>='2021-07-01':fixture['prices']['NVDA'][day]=str(D(str(value))*20)
    replay=_replay_simulation(fixture,CASES[0],cell,'BASELINE');row=next(x for x in replay['ledger'] if x['date']=='2021-07-01')
    assert abs(D(row['nav'])-D('181307.168064881328718800860129927659184437878829177997151134'))<D('.000001')
    assert abs(D(row['cash'])-D('25383.0035290833860206321204181898722858213030360849196011587'))<D('.000001')
    fixture['prices']['NVDA']=original
    assert _replay_simulation(fixture,CASES[0],cell,'BASELINE')==positive

def test_complete_ledgers_use_canonical_nav_grouping_and_reject_material_tampering():
    from pathlib import Path
    import json,yaml
    import whole_portfolio_robustness_v2_engine as engine
    from test_whole_portfolio_robustness_v2_engine import full_synthetic_fixture
    prereg=yaml.safe_load(Path('research/whole_portfolio_robustness_v2/pre_registration.yaml').read_text());profiles={k:{name:D(value) for name,value in values.items()} for k,values in prereg['frictions']['tax_profile_parameters'].items()}
    fixture=full_synthetic_fixture();original=dict(fixture['prices']['NVDA'])
    cases=[('TAX_DEFERRED',D(0),'ANNUAL',False),('TAX_DEFERRED',D(10),'QUARTERLY',False),('TAXABLE_MID',D(0),'QUARTERLY',False),('TAX_DEFERRED',D(0),'QUARTERLY',True),('TAXABLE_MID',D(10),'ANNUAL',True)]
    for profile,cost,cadence,shock in cases:
        fixture['prices']['NVDA']=dict(original)
        if shock:
            for day,value in fixture['prices']['NVDA'].items():
                if day>='2021-07-01':fixture['prices']['NVDA'][day]=str(D(str(value))*20)
        artifact=json.loads(json.dumps(engine.simulate(Path('.'),fixture,'BASELINE',cost,profiles[profile],cadence,CASES[0]),allow_nan=False))
        assert validate_ledger(artifact)==[]
        row=artifact['ledger'][409];saved=row['nav'];row['nav']=str(D(saved)+D('.01'));assert any('NAV does not reconcile' in error for error in validate_ledger(artifact));row['nav']=saved
        row['cash']=str(D(row['cash'])+D('.01'));assert validate_ledger(artifact);row['cash']=str(D(row['cash'])-D('.01'))
        assert validate_ledger(artifact)==[]
    fixture['prices']['NVDA']=original

def test_fixed_evaluation_uses_replayed_operational_economics():
    from pathlib import Path
    import yaml
    import whole_portfolio_robustness_v2_engine as engine
    from test_whole_portfolio_robustness_v2_engine import REGIMES,full_synthetic_fixture
    prereg=yaml.safe_load(Path('research/whole_portfolio_robustness_v2/pre_registration.yaml').read_text());cell=next(x for x in prereg['frictions']['cell_registry'] if x['cell_id']=='COST_10_TAX_TAXABLE_MID_CADENCE_QUARTERLY');profile={k:D(v) for k,v in prereg['frictions']['tax_profile_parameters'][cell['tax_profile']].items()}
    result=engine.simulate(Path('.'),full_synthetic_fixture(),'BASELINE',D(10),profile,'QUARTERLY',CASES[0]);metrics=engine.fixed_evaluations(result['ledger'],REGIMES)['CALENDAR_2023']
    days=[x for x in result['calendar_ledger'] if '2023-01-03'<=x['date']<='2023-12-29'];events=[event for row in days for event in row['events']]
    costs=sum((D(str(x.get('cost',0))) for x in events),D(0));taxes=sum((D(str(x.get('tax',0)))+D(str(x.get('withholding',0)))+D(str(x.get('us_tax',0))) for x in events),D(0));notional=sum((D(str(x.get('notional',x.get('proceeds',0)))) for x in events if x.get('type') in {'buy','sell'}),D(0))
    anchor=D(next(x['nav'] for x in result['ledger'] if x['date']=='2022-12-30'));rebalances=sum(any(x.get('type')=='rebalance' for x in row['events']) for row in days)
    assert costs==D('0.3057172696484120559175052198') and metrics['cost_drag']==pytest.approx(float(costs))
    assert taxes==D('4.002144282150124469610132306') and metrics['tax_drag']==pytest.approx(float(taxes))
    assert metrics['rebalance_count']==rebalances==4
    assert metrics['one_way_turnover']==pytest.approx(float(notional/anchor))
    evaluations=engine.fixed_evaluations(result['ledger'],REGIMES)
    assert tuple(evaluations['walk_forward'])==('2022','2023','2024','2025','2026')
    independent=_fixed_evaluations(result['ledger'],REGIMES)
    assert tuple(independent['walk_forward'])==('2022','2023','2024','2025','2026')

def test_independent_recovery_uses_real_anchor_and_censors():
    zero={'turnover_notional':'0','rebalance_count':'0','taxable_realized_gain':'0','cost_drag':'0','tax_drag':'0','cash_drag':'0'}
    rows=[{'date':'2025-01-02','anchor_nav':'100000','anchor_date':'2024-12-31','anchor_operations':zero,'operations':zero,'nav':'100000','risk_free_return':'0'}, {'date':'2025-01-03','operations':zero,'nav':'99000','risk_free_return':'0'}, {'date':'2025-01-13','operations':zero,'nav':'100000','risk_free_return':'0'}]
    assert _fixed_evaluations(rows,[{'id':'X','start':'2025-01-02','end':'2025-01-13'}])['X']['recovery_days']==11
    rows[-1]['nav']='98000'
    assert _fixed_evaluations(rows,[{'id':'X','start':'2025-01-02','end':'2025-01-13'}])['X']['recovery_days'] is None

def test_independent_calendar_cagr_downside_and_concentration_maxima():
    zero={'turnover_notional':'0','rebalance_count':'0','taxable_realized_gain':'0','cost_drag':'0','tax_drag':'0','cash_drag':'0'}
    rows=[{'date':'2025-01-02','anchor_nav':'100','anchor_date':'2024-12-31','anchor_operations':zero,'operations':zero,'nav':'101','risk_free_return':'.02'}, {'date':'2025-01-06','operations':zero,'nav':'100.5','risk_free_return':'.02'}]
    result=_fixed_evaluations(rows,[{'id':'X','start':'2025-01-02','end':'2025-01-06'}])['X'];returns=[.01,100.5/101-1]
    assert result['net_twr_cagr']==pytest.approx(1.005**(365.2425/6)-1)
    assert result['downside_deviation']==pytest.approx((sum(min(r-.02,0)**2 for r in returns)/2)**.5*252**.5)
    keys=('direct_hhi','max_direct_name','effective_issuer_max','ai_platform_common_driver','semis_cluster','power_infra_cluster');row=lambda h,n:dict(zip(keys,(h,n,n,n,.1,.1)))
    assert _concentration_window_pass([row(.1,.2),row(.05,.1)],[row(.06,.15),row(.07,.16)])

def test_path_metric_admission_rejects_nonfinite_actual_and_claimed_values():
    assert _compare_metric_tree({'x':float('nan')},{'x':1.},'metrics')
    assert _compare_metric_tree({'x':1.},{'x':float('nan')},'metrics')
    rows=[{'date':'2025-01-02','anchor_nav':'100','anchor_date':'2024-12-31','nav':'101','risk_free_return':'0'}, {'date':'2025-01-03','nav':'99','risk_free_return':'0'}]
    for location,bad in (('nav','NaN'),('nav',0),('nav',False),('anchor_nav','Infinity'),('anchor_nav',-1)):
        attacked=deepcopy(rows);target=attacked[0] if location=='anchor_nav' else attacked[1];target[location]=bad
        with pytest.raises(ValueError):_path_stats(attacked)

def test_probability_claims_reject_bool_missing_extra_nonfinite_and_wrong_values():
    actual={'NET_TWR_CAGR_DELTA':.4315,'SHARPE_DELTA':.473,'MAX_DRAWDOWN_DELTA':.097,'DAILY_CVAR_95_DELTA':0.}
    assert _compare_probability_claim(actual,deepcopy(actual),'context_bootstrap')==[]
    attacks=[]
    for key,bad in (('DAILY_CVAR_95_DELTA',False),('NET_TWR_CAGR_DELTA',True),('SHARPE_DELTA',float('nan')),('MAX_DRAWDOWN_DELTA',float('inf')),('SHARPE_DELTA',1.1)):
        claim=deepcopy(actual);claim[key]=bad;attacks.append(claim)
    missing=deepcopy(actual);del missing['NET_TWR_CAGR_DELTA'];attacks.append(missing)
    extra=deepcopy(actual);extra['UNREGISTERED']=.5;attacks.append(extra)
    assert all(_compare_probability_claim(actual,claim,'context_bootstrap') for claim in attacks)
    assert _compare_metric_tree([0.0],[False],'nested')

def document():
    rows=[{'date':'2025-01-02','cash':'100000','positions':[],'receivables':[],'nav':'100000','events':[]}, {'date':'2025-01-03','cash':'100000','positions':[],'receivables':[],'nav':'100000','events':[],'interest_credited':'0'}]
    gates={c:{a:False for a in ALTS} for c in CASES}
    cells=[f"COST_{c}_TAX_{t}_CADENCE_{q}" for c in ('0','10','25') for t in ('TAX_DEFERRED','TAXABLE_MID','TAXABLE_HIGH') for q in ('QUARTERLY','ANNUAL')]
    bad={'net_cagr_delta_pp':0.,'sharpe_delta':0.,'sortino_delta':0.,'max_drawdown_delta_pp':0.,'daily_cvar_95_delta_pp':0.}
    named={'support_15_of_18':False,'primary':False,'context_direction':True,'bootstrap_sharpe':False,'regimes':True,'concentration':True,'linked_tail':False,'final':False}
    details={c:{a:{'cells':[dict(bad,cell_id=x,window='correction_replication') for x in cells],'primary':{'correction_replication':bad,'context':bad},'bootstrap':{'SHARPE_DELTA':0.,'MAX_DRAWDOWN_DELTA':0.,'DAILY_CVAR_95_DELTA':0.},'regime_pass':True,'concentration_pass':True,'gates':named,'final':False} for a in ALTS} for c in CASES}
    calendar=[{'date':'2025-01-02','opening_eligible_cash':'100000','dff_percent':'.25','interest_credited':'0','settled_cash':'100000','events':[]},{'date':'2025-01-03','opening_eligible_cash':'100000','dff_percent':'.25','interest_credited':'0','settled_cash':'100000','events':[]}]
    return {'initial_nav':'100000','cell':{'cost_bps':'0','profile':{'ordinary_income_rate':'0'}},'calendar_ledger':calendar,'ledger':rows,'summary':{'cumulative_twr':0.,'max_drawdown':0.},'decision_evidence':{'cell_ids':cells,'cases':details},'foreign_case_gate_booleans':gates,'disposition':{'disposition':'RETAIN_BASELINE','passing_set':[]}}

def test_invented_dictionary_without_paired_paths_is_rejected(): assert any('portfolio paths' in e for e in validate_result(document()))
def test_tampered_nav_and_summary_detected():
    x=document();x['ledger'][1]['nav']='111000';x['summary']['cumulative_twr']=.11
    e=validate_result(x);assert any('NAV' in z for z in e) and any('cumulative' in z for z in e)
def test_negative_cash_and_external_flow_detected():
    x=document();x['ledger'][1].update(cash='-1',nav='-1',external_flow='1')
    e=validate_result(x);assert any('negative' in z for z in e) and any('external' in z for z in e)
def test_missing_extra_duplicate_like_gate_evidence_fails_closed():
    x=document();del x['foreign_case_gate_booleans'][CASES[-1]]
    assert recompute_disposition(x['foreign_case_gate_booleans'])['disposition']=='UNABLE_TO_DETERMINE'
def test_foreign_boolean_change_overrides_claim():
    x=document();x['foreign_case_gate_booleans'][CASES[1]][ALTS[0]]=True
    assert 'disposition not independently reproducible' in validate_result(x)

def test_unexplained_cash_doubling_and_missing_decision_evidence_rejected():
    x=document();x['ledger'][1].update(cash='200000',nav='200000');x['summary']['cumulative_twr']=1
    assert any('cash' in e for e in validate_result(x))
    x=document();del x['decision_evidence'];assert any('comparison evidence' in e for e in validate_result(x))

def test_complete_synthetic_driver_result_replays_and_path_mutation_fails():
    from test_whole_portfolio_robustness_v2_engine import get_full_bundle
    bundle=get_full_bundle()
    case=CASES[0];cell=bundle['decision_evidence']['cell_ids'][0]
    old=bundle['portfolio_paths'][case][cell]['BASELINE']['context'][0]['risk_free_return'];bundle['portfolio_paths'][case][cell]['BASELINE']['context'][0]['risk_free_return']='NaN'
    decision={k:bundle[k] for k in ('portfolio_paths','decision_evidence','foreign_case_gate_booleans','disposition')}
    assert validate_result(decision,decision_only=True);bundle['portfolio_paths'][case][cell]['BASELINE']['context'][0]['risk_free_return']=old
    detail=bundle['decision_evidence']['cases'][case][ALTS[0]];claim=detail['context_bootstrap'];old=claim['DAILY_CVAR_95_DELTA'];claim['DAILY_CVAR_95_DELTA']=False
    assert validate_result(decision,decision_only=True);claim['DAILY_CVAR_95_DELTA']=old
    dividend=bundle['primitive_fixture']['dividends'][0];bundle['primitive_fixture']['dividends']=[dict(dividend,gross_per_share=0)]
    assert any('corporate-action registry' in e for e in validate_study_bundle(bundle));bundle['primitive_fixture']['dividends']=[dividend]
    split=bundle['primitive_fixture']['splits'][0];bundle['primitive_fixture']['splits']=[split,dict(split)]
    assert any('corporate-action registry' in e for e in validate_study_bundle(bundle));bundle['primitive_fixture']['splits']=[split]
    attack_case=CASES[-1];attack_cell=bundle['decision_evidence']['cell_ids'][-1];attack_alt=ALTS[-1]
    row=bundle['portfolio_paths'][attack_case][attack_cell][attack_alt]['correction_replication'][10];old=row['nav'];row['nav']='NaN'
    assert validate_result(decision,decision_only=True);row['nav']=old
    evaluation=bundle['decision_evidence']['cases'][case][ALTS[0]]['evaluations']['baseline']['walk_forward'];evaluation['2021']=deepcopy(evaluation['2022'])
    assert validate_result(decision,decision_only=True);del evaluation['2021']

def test_full_bundle_rejects_calendar_identity_lot_primary_concentration_and_detachment():
    import copy
    from test_whole_portfolio_robustness_v2_engine import get_full_bundle
    bundle=get_full_bundle();case=CASES[0];cell=bundle['decision_evidence']['cell_ids'][0];alt=ALTS[0];sim=bundle['simulations'][case][cell][alt]
    old=sim['calendar_ledger'];sim['calendar_ledger']=[];assert validate_study_bundle(bundle);sim['calendar_ledger']=old
    old_variant=sim['variant'];sim['variant']='BASELINE';assert validate_study_bundle(bundle);sim['variant']=old_variant
    row=next(x for x in sim['ledger'] if x.get('positions'));old_lots=row['positions'][0]['lots'];row['positions'][0]['lots']=[{'units':'999999','basis':'0','acquired':'1900-01-01'}];assert validate_study_bundle(bundle);row['positions'][0]['lots']=old_lots
    detail=bundle['decision_evidence']['cases'][case][alt];old=detail['primary']['correction_replication']['net_cagr_delta_pp'];detail['primary']['correction_replication']['net_cagr_delta_pp']=999.;assert validate_decision_variant(bundle,case,alt);detail['primary']['correction_replication']['net_cagr_delta_pp']=old
    old=detail['concentration_path'];detail['concentration_path']=[{k:999. for k in old[0]} for _ in old];assert validate_decision_variant(bundle,case,alt);detail['concentration_path']=old
    old=sim;bundle['simulations'][case][cell][alt]=copy.deepcopy(bundle['simulations'][case][cell]['BASELINE']);assert validate_study_bundle(bundle);bundle['simulations'][case][cell][alt]=old
