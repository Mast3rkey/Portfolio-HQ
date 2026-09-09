from copy import deepcopy
import pytest
from whole_portfolio_robustness_v2_result_validator import *
from whole_portfolio_robustness_v2_result_validator import _XNYS, _SUMMARY_FIELDS, _compare_metric_tree, _compare_probability_claim, _concentration, _derived_windows, _path_identity, _replay_simulation

def test_replay_window_derivation_binds_predecessor_and_every_field():
    full=[]
    for item in _XNYS:
        if '2021-06-01'<=item['session']<='2026-07-31':
            full.append({'date':item['session'],'nav':str(100000+len(full)),
                         'risk_free_return':'0.0001','concentration':{'effective_issuer_max':.06},
                         'operations':{'turnover_notional':'0','rebalance_count':'0','taxable_realized_gain':'0','cost_drag':'0','tax_drag':'0','cash_drag':'0'}})
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
        if row.get('events'):keep.update(events=row['events'],positions=row['positions'],receivables=row['receivables'])
        compact.append(keep)
    assert compact==projection(expected['ledger'])
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
    mutated=deepcopy(compact);row=next(x for x in mutated if x.get('positions'));row['positions'][0]['lots'][0]['basis']='999999'
    assert mutated!=projection(expected['ledger'])

def test_fixed_evaluation_uses_replayed_operational_economics():
    from pathlib import Path
    import yaml
    import whole_portfolio_robustness_v2_engine as engine
    from test_whole_portfolio_robustness_v2_engine import REGIMES,full_synthetic_fixture
    prereg=yaml.safe_load(Path('research/whole_portfolio_robustness_v2/pre_registration.yaml').read_text());cell=next(x for x in prereg['frictions']['cell_registry'] if x['cell_id']=='COST_10_TAX_TAXABLE_MID_CADENCE_QUARTERLY');profile={k:D(v) for k,v in prereg['frictions']['tax_profile_parameters'][cell['tax_profile']].items()}
    result=engine.simulate(Path('.'),full_synthetic_fixture(),'BASELINE',D(10),profile,'QUARTERLY',CASES[0]);metrics=engine.fixed_evaluations(result['ledger'],REGIMES)['CALENDAR_2023']
    assert metrics['cost_drag']==pytest.approx(.30491598718183627)
    assert metrics['tax_drag']==pytest.approx(3.9731247866407537)
    assert metrics['rebalance_count']==4
    assert metrics['one_way_turnover']==pytest.approx(.0030288705385554133)

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
