from copy import deepcopy
from whole_portfolio_robustness_v2_result_validator import *
from whole_portfolio_robustness_v2_result_validator import _XNYS, _concentration, _derived_windows, _path_identity

def test_replay_window_derivation_binds_predecessor_and_every_field():
    full=[]
    for item in _XNYS:
        if '2021-06-01'<=item['session']<='2026-07-31':
            full.append({'date':item['session'],'nav':str(100000+len(full)),
                         'risk_free_return':'0.0001','concentration':{'effective_issuer_max':.06}})
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
