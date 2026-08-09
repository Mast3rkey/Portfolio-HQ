"""Structured per-ticker research data -> valuation_evidence records.

Sourced from the WS-0015 VALUATION-0005 Stage-3 research shards (see
governance/audits/WS0015_VALUATION_EVIDENCE_POPULATION_20260809.md for the
full research trail and every disclosed conflict/gap). Every fact traces to
a real WebSearch result gathered in this implementation's own research
session; nothing is invented from model memory. WebFetch was blocked by
this environment's network egress policy for every finance/SEC/IR domain
attempted across all shards -- every source below is therefore labeled
source_type="secondary", access_status="consulted_via_search_aggregation".

Conventions:
- AS_OF is the single evidence-gathering date used for every provenance
  source and market/peer as_of_date in this population pass (the actual
  historical fiscal periods described vary; the date this evidence was
  *gathered* does not).
- discount_rate_evidence is abstained for every ticker: this Stage-3 pass
  gathered financial-statement, market-price, segment, peer-candidate and
  catalyst/scenario evidence -- it did not conduct dedicated discount-rate-
  component research (risk-free rate, cost of debt, tax rate, capital-
  structure weights, beta). That is a disclosed, honest scope limitation,
  not a schema gap or a fabrication risk to route around.
"""
from __future__ import annotations

from valuation_evidence_generator import (
    build_record, src, prov, reported, derived, abstain_item,
    period, market_input, market_input_abstain, peer, scenario_var, scenario,
    segment,
)

AS_OF = "2026-08-09"
DISCOUNT_ABSTAIN_REASON = (
    "No dedicated discount-rate-component research (risk-free rate, cost of "
    "debt, tax rate, capital-structure weights, beta observation) was "
    "conducted in this evidence-gathering pass -- this domain requires a "
    "separate research effort beyond the financial-statement, market-price, "
    "segment, peer-candidate, and catalyst/scenario research performed here."
)


def S(identifier, limitation=None):
    return src(identifier, "secondary", AS_OF, "consulted_via_search_aggregation", limitation)


def P(identifier, limitation=None):
    return prov(S(identifier, limitation))


def R(category, value, unit, source_id, limitation=None, conflicts=None):
    return reported(category, value, unit, P(source_id, limitation), conflicts)


def D(category, value, unit, note, source_id, limitation=None):
    return derived(category, value, unit, note, P(source_id, limitation))


def mk_period(fy_end, items, ptype="annual", restated=False, restated_note=None):
    return period(ptype, fy_end, AS_OF, items, restated=restated, restated_note=restated_note)


def mk_price(value, note=None):
    return market_input(
        "observed_share_price", value, "usd_per_share", AS_OF, P("WebSearch aggregation, current stock price", note),
    )


def mk_peers(rows):
    return [
        peer(identity, rationale, P("WebSearch aggregation, candidate peer identification"),
             AS_OF, "included", "Disclosed as a comparability candidate only; no peer set has been selected or applied to any valuation.")
        for identity, rationale in rows
    ]


def mk_scenarios(rows):
    return [
        scenario(name, [scenario_var(name.lower().replace(" ", "_")[:60], evidence, "historically_observed")])
        for name, evidence in rows
    ]


def build(ticker, *, periods, segments=None, segment_abstain=None,
          price=None, price_abstain=None, peers_data=None, peer_abstain=None,
          scenarios_data=None, scenario_abstain=None, uncertainty_summary,
          shared_unallocated=None, intersegment=None):
    market_inputs = [price] if price else None
    market_abstain = price_abstain if not price else None
    return build_record(
        ticker,
        financial_periods=periods,
        financial_abstain=None,
        segments=segments,
        segment_abstain=segment_abstain,
        shared_unallocated_costs=shared_unallocated,
        intersegment_eliminations=intersegment,
        market_inputs=market_inputs,
        market_abstain=market_abstain,
        discount_components=None,
        discount_abstain=DISCOUNT_ABSTAIN_REASON,
        peer_candidates=mk_peers(peers_data) if peers_data else None,
        peer_abstain=peer_abstain,
        scenarios_list=mk_scenarios(scenarios_data) if scenarios_data else None,
        scenario_abstain=scenario_abstain,
        uncertainty_summary=uncertainty_summary,
    )


RECORDS = {}

# ============================================================
# Batch A -- shard 1: ISRG, LLY, NVDA, PANW, SNPS
# ============================================================

RECORDS["ISRG"] = build(
    "ISRG",
    periods=[
        mk_period("2021-12-31", [R("revenue", 5710, "usd_millions", "ISRG FY2021 revenue (press-release aggregation)")]),
        mk_period("2022-12-31", [
            R("revenue", 6220, "usd_millions", "ISRG FY2022 revenue"),
            R("earnings", 1320, "usd_millions", "ISRG FY2022 net income"),
            D("operating_margin", 0.254, "ratio", "Derived: FY2022 operating income $1,580M divided by revenue $6,220M equals 25.4 percent.", "ISRG FY2022 operating income $1,580M"),
        ]),
        mk_period("2023-12-31", [
            R("revenue", 7120, "usd_millions", "ISRG FY2023 revenue"),
            R("earnings", 1800, "usd_millions", "ISRG FY2023 net income"),
            D("operating_margin", 0.249, "ratio", "Derived: FY2023 operating income $1,770M divided by revenue $7,120M equals 24.9 percent.", "ISRG FY2023 operating income $1,770M"),
        ]),
        mk_period("2024-12-31", [
            R("revenue", 8350, "usd_millions", "ISRG FY2024 revenue"),
            R("earnings", 2323, "usd_millions", "ISRG FY2024 net income"),
            D("operating_margin", 0.281, "ratio", "Derived: FY2024 operating income $2,349M divided by revenue $8,350M equals 28.1 percent.", "ISRG FY2024 operating income $2,349M"),
            R("free_cash_flow", 2490.7, "usd_millions", "ISRG FY2024 operating cash flow $3,030.5M less capex $539.8M (company-reported line items)"),
            R("capex", 539.8, "usd_millions", "ISRG FY2024 capital expenditures"),
        ]),
        mk_period("2025-12-31", [
            R("revenue", 10065, "usd_millions", "ISRG FY2025 revenue"),
            R("earnings", 2856, "usd_millions", "ISRG FY2025 net income"),
            D("operating_margin", 0.293, "ratio", "Derived: FY2025 operating income $2,950M divided by revenue $10,065M equals 29.3 percent.", "ISRG FY2025 operating income $2,950M"),
            R("free_cash_flow", 2834.3, "usd_millions", "ISRG FY2025 operating cash flow $3,360.8M less capex $526.5M; internally consistent (3,360.8-526.5=2,834.3)"),
            R("capex", 526.5, "usd_millions", "ISRG FY2025 capital expenditures"),
            R("debt", 0, "usd_millions", "ISRG carries no debt (company-reported)"),
            R("share_count_diluted", 354.5, "shares_millions", "ISRG diluted shares outstanding, Oct 16 2025"),
            R("total_equity", 17900, "usd_millions", "ISRG total equity (recent balance sheet)"),
            R("total_assets", 20500, "usd_millions", "ISRG total assets (recent balance sheet)"),
            R("total_liabilities", 2500, "usd_millions", "ISRG total liabilities (recent balance sheet)"),
        ]),
    ],
    segment_abstain="ISRG does not report classic business segments; it discloses revenue by product category (Instruments & Accessories / Systems / Service). A clean full-year dollar breakdown across all three categories was not found despite searching -- only partial data (e.g. I&A revenue +19% YoY, system placement counts) surfaced.",
    price=mk_price(375.26, "Observed Aug 5 2026; a later Aug 6 2026 market-cap figure of ~$133.93B is consistent (375.26 x ~354.5M shares implies ~$133.1B)."),
    peers_data=[
        ("SYK", "Stryker -- direct robotic-surgery overlap (Mako system) plus a broad medtech portfolio."),
        ("MDT", "Medtronic -- large medtech competitor building its own soft-tissue robotic platform (Hugo RAS)."),
        ("JNJ", "Johnson & Johnson -- developing a competing robotic surgery platform (Ottava)."),
    ],
    scenarios_data=[
        ("da Vinci 5 cardiac clearance", "FDA clearance (Jan 22 2026 investor call) for da Vinci 5 use in several cardiac procedures (mitral valve repair, ASD/PFO closure) using non-Force-Feedback instruments."),
        ("Tariff exposure", "Q3 2025 non-GAAP gross margin outlook incorporated an estimated ~0.7% of revenue tariff impact."),
    ],
    uncertainty_summary=(
        "All figures secondary/search-aggregation-sourced; WebFetch was blocked for every finance domain "
        "attempted, so no primary document (10-K/press-release PDF) was directly opened by this research "
        "session. Full-year diluted EPS was not confirmed for any fiscal year despite multiple search "
        "attempts -- only quarterly EPS points surfaced, and summing quarterly EPS is not a valid annual "
        "figure given share-count weighting, so diluted EPS is omitted from this record rather than "
        "estimated. Cash-and-investments figures across two sources were not fully reconciled to each "
        "other (different scopes -- short-term-only vs. total). No IPO/spin-off/restructuring affects "
        "ISRG's own 5-year comparability."
    ),
)

RECORDS["LLY"] = build(
    "LLY",
    periods=[
        mk_period("2022-12-31", [
            R("revenue", 28540, "usd_millions", "LLY FY2022 revenue"),
            D("operating_margin", 0.290, "ratio", "Derived: FY2022 operating income $8,280M divided by revenue $28,540M equals 29.0 percent.", "LLY FY2022 operating income $8,280M"),
            abstain_item("earnings", "FY2021/FY2022 net income could not be reliably confirmed -- one search result appeared to erroneously repeat the FY2025 net income figure when queried about FY2021, and the FY2022 figure was not independently corroborated; discarded rather than reported as fact."),
        ]),
        mk_period("2023-12-31", [
            R("revenue", 34120, "usd_millions", "LLY FY2023 revenue"),
            D("operating_margin", 0.303, "ratio", "Derived: FY2023 operating income $10,330M divided by revenue $34,120M equals 30.3 percent.", "LLY FY2023 operating income $10,330M"),
        ]),
        mk_period("2024-12-31", [
            R("revenue", 45040, "usd_millions", "LLY FY2024 revenue"),
            R("earnings", 10590, "usd_millions", "LLY FY2024 net income"),
            D("operating_margin", 0.378, "ratio", "Derived: FY2024 operating income $17,040M divided by revenue $45,040M equals 37.8 percent.", "LLY FY2024 operating income $17,040M"),
        ]),
        mk_period("2025-12-31", [
            R("revenue", 65180, "usd_millions", "LLY FY2025 revenue (also cited as $65.2B)"),
            R("earnings", 20640, "usd_millions", "LLY FY2025 net income (corroborated by two independent searches)"),
            D("operating_margin", 0.456, "ratio", "Derived: FY2025 operating income $29,700M divided by revenue $65,180M equals 45.6 percent.", "LLY FY2025 operating income $29,700M"),
            abstain_item("free_cash_flow", "FY2025 capex was not found as a specific dollar figure (only a vague 'meaningfully higher capex' characterization and an unclear TTM figure), so free cash flow cannot be reliably derived from the $16.8B FY2025 operating cash flow figure."),
            R("cash", 7300, "usd_millions", "LLY cash & equivalents, year-end 2025 (vs. $3.3B year-end 2024)"),
            R("debt", 42500, "usd_millions", "LLY total debt, 2025 (secondary aggregator); long-term debt specifically cited at $40,868M, +43.26% YoY"),
            D("net_debt", 35200, "usd_millions", "Derived: total debt $42.5B minus cash $7.3B equals ~$35.2B; approximate, ignores short-term investments (figure not available).", "LLY FY2025 cash and debt figures above"),
            R("share_count_diluted", 894, "shares_millions", "LLY diluted shares outstanding, mid-2025"),
        ]),
    ],
    segment_abstain="LLY discloses revenue predominantly by product/therapeutic area (Mounjaro, Zepbound, Trulicity, Verzenios, Jardiance, etc.) rather than classic business/geographic segments. Mounjaro + Zepbound alone were 56% of FY2025 revenue (reported), but a clean full product-revenue table was not obtained this session.",
    price=mk_price(1123.0, "Price observed alongside a 52-week high of $1,249.45 on Jul 7 2026 -- this is recent-2026 context, not necessarily the exact observation date of the price itself."),
    peers_data=[
        ("NVO", "Novo Nordisk -- direct GLP-1/obesity-drug competitor (Ozempic/Wegovy vs. Mounjaro/Zepbound)."),
        ("PFE", "Pfizer -- comparable large-cap diversified pharmaceutical company."),
        ("MRK", "Merck -- comparable large-cap pharmaceutical company with its own oncology/vaccine franchise concentration dynamics."),
    ],
    scenarios_data=[
        ("Orforglipron oral GLP-1 approval", "FDA approved Lilly's oral GLP-1 pill for obesity/overweight on Apr 1 2026 -- the first GLP-1 pill approved with no food/water timing restriction; Phase 3 ATTAIN data showed up to 12.4% average weight loss at 72 weeks. Will compete against Novo Nordisk's oral semaglutide (approved Dec 2025)."),
    ],
    uncertainty_summary=(
        "All figures secondary/search-aggregation-sourced; no primary document directly opened. FY2021 net "
        "income and FY2022 net income could not be reliably confirmed and are abstained rather than "
        "reported (one search result appears to have erroneously repeated the FY2025 net-income figure "
        "when the FY2021 figure was requested). FY2025 capex and therefore free cash flow could not be "
        "pinned down to a specific dollar figure. Revenue/earnings growth 2021-2025 is extremely steep "
        "(driven by GLP-1 franchise growth), disclosed as organic growth concentrated in two products "
        "(56% of FY2025 revenue), not a structural discontinuity -- but multi-year trend comparisons "
        "should be read with that concentration in mind."
    ),
)

RECORDS["NVDA"] = build(
    "NVDA",
    periods=[
        mk_period("2022-01-30", [
            R("revenue", 26910, "usd_millions", "NVDA FY2022 (ended late Jan 2022) revenue"),
            R("earnings", 9800, "usd_millions", "NVDA FY2022 net income"),
            D("operating_margin", 0.372, "ratio", "Derived: FY2022 operating income $10,000M divided by revenue $26,910M equals 37.2 percent.", "NVDA FY2022 operating income $10,000M"),
        ], restated=False),
        mk_period("2023-01-29", [
            R("revenue", 26970, "usd_millions", "NVDA FY2023 (ended late Jan 2023) revenue"),
            R("earnings", 9200, "usd_millions", "NVDA FY2023 net income"),
        ]),
        mk_period("2024-01-28", [
            R("revenue", 60922, "usd_millions", "NVDA FY2024 (ended late Jan 2024) revenue"),
            R("earnings", 19300, "usd_millions", "NVDA FY2024 net income"),
        ]),
        mk_period("2025-01-26", [
            R("revenue", 130497, "usd_millions", "NVDA FY2025 (ended late Jan 2025) revenue"),
            R("earnings", 72880, "usd_millions", "NVDA FY2025 net income"),
            D("operating_margin", 0.624, "ratio", "Derived: FY2025 operating income $81,453M divided by revenue $130,497M equals 62.4 percent.", "NVDA FY2025 operating income $81,453M"),
        ]),
        mk_period("2026-01-25", [
            R("revenue", 215900, "usd_millions", "NVDA FY2026 (ended Jan 25 2026) revenue, +65% YoY"),
            R("earnings", 120070, "usd_millions", "NVDA FY2026 net income", limitation="Secondary aggregator figure, not independently re-confirmed from a second source; a rough cross-check via diluted EPS x implied share count is directionally consistent."),
            D("operating_margin", 0.604, "ratio", "Derived: FY2026 operating income $130,390M divided by revenue $215,900M equals 60.4 percent.", "NVDA FY2026 operating income $130,390M (one-source synthesis)"),
            R("free_cash_flow", 96600, "usd_millions", "NVDA FY2026 free cash flow; internal consistency check passes (operating cash flow $102,700M minus capex $6,040M = $96,660M ~= $96,600M reported)"),
            R("capex", 6040, "usd_millions", "NVDA FY2026 capital expenditures"),
            R("cash", 10600, "usd_millions", "NVDA cash & equivalents, Jan 25 2026"),
            D("cash", 62600, "usd_millions", "Derived: cash $10,600M plus marketable securities $51,950M equals $62,600M total cash+investments.", "NVDA balance sheet, Jan 25 2026"),
            D("debt", 8468, "usd_millions", "Derived: short-term debt $999M plus long-term debt $7,469M equals ~$8,468M total debt.", "NVDA balance sheet, Jan 25 2026"),
            D("net_debt", -54100, "usd_millions", "Derived: total cash+investments $62.6B minus total debt $8.468B equals ~$54.1B net CASH position (negative net debt).", "NVDA balance sheet figures above"),
        ]),
    ],
    segments=[
        segment("Data Center", revenue=R("revenue", 193740, "usd_millions", "NVDA FY2026 Data Center segment revenue, 89.7% of total, +68.2% YoY")),
        segment("Gaming", revenue=R("revenue", 16000, "usd_millions", "NVDA FY2026 Gaming segment revenue")),
        segment("Professional Visualization", revenue=R("revenue", 3190, "usd_millions", "NVDA FY2026 Professional Visualization segment revenue, 1.5% of total")),
        segment("Automotive", revenue=R("revenue", 2350, "usd_millions", "NVDA FY2026 Automotive segment revenue, 1.1% of total, +38.7% YoY")),
        segment("OEM & Other", revenue=R("revenue", 619, "usd_millions", "NVDA FY2026 OEM & Other segment revenue")),
    ],
    price=mk_price(221.54, "Early-August 2026 context (52-week high $236.54/low $164.07); cross-check 221.54 x ~24.5B implied shares ~= $5.43T, consistent with reported ~$5.424T market cap."),
    peers_data=[
        ("AMD", "Direct GPU/AI-accelerator competitor."),
        ("AVGO", "Broadcom -- custom AI silicon (ASICs) and networking, adjacent AI-infrastructure competitor."),
        ("TSM", "NVDA's foundry manufacturer -- different business model (pure-play foundry vs. fabless designer), useful as a capacity/demand cross-check rather than a direct comparable."),
    ],
    scenarios_data=[
        ("China export-control / H20-Blackwell dynamics", "$4.5B charge in Q1 FY2026 tied to H20 excess inventory/purchase obligations as China demand collapsed under export restrictions; a reported Malaysia/Singapore/UAE subsidiary routing pathway for Blackwell/Rubin chips was reportedly closed by the Commerce Department in May 2026."),
    ],
    uncertainty_summary=(
        "All figures secondary/search-aggregation-sourced; no primary document directly opened. NVDA "
        "executed a 10-for-1 stock split effective June 2024 -- diluted EPS figures found for FY2022-FY2024 "
        "appear to be PRE-SPLIT scale while FY2025-FY2026 figures are POST-SPLIT scale, a material "
        "comparability discontinuity; diluted EPS is therefore omitted from this record entirely rather "
        "than reported inconsistently across the split boundary (revenue and net income, unaffected by "
        "the split, are reported normally). FY2026 net income and FY2026 operating income both trace to "
        "single-source synthesis and were not independently corroborated from a second source, though "
        "internal consistency checks (FCF, price x shares) are directionally supportive."
    ),
)

RECORDS["PANW"] = build(
    "PANW",
    periods=[
        mk_period("2021-07-31", [
            R("revenue", 4260, "usd_millions", "PANW FY2021 (ended Jul 31 2021) revenue"),
            R("earnings", -498.9, "usd_millions", "PANW FY2021 net loss"),
        ]),
        mk_period("2022-07-31", [
            R("revenue", 5500, "usd_millions", "PANW FY2022 revenue"),
            R("earnings", -267.0, "usd_millions", "PANW FY2022 net loss"),
        ]),
        mk_period("2023-07-31", [
            R("revenue", 6890, "usd_millions", "PANW FY2023 revenue"),
            R("earnings", 439.7, "usd_millions", "PANW FY2023 net income"),
        ]),
        mk_period("2024-07-31", [
            R("revenue", 8030, "usd_millions", "PANW FY2024 revenue"),
            R("earnings", 2580, "usd_millions", "PANW FY2024 net income", limitation="Includes a disclosed ~$1.5B one-time net tax benefit from release of a valuation allowance -- not a clean operating result."),
        ]),
        mk_period("2025-07-31", [
            R("revenue", 9220, "usd_millions", "PANW FY2025 (\"$9.2 billion\") revenue"),
            abstain_item("earnings", "Two irreconcilable FY2025 GAAP net-income figures were found ($1,133.9M derived from a cited income-before-taxes/tax-provision pair vs. a separately-cited $1,577.6M 'FY2024 comparison' figure that itself contradicts the corroborated $2,580M FY2024 figure above) -- likely a search-synthesis error reading the wrong column/period. Not reported as fact pending direct 10-K inspection."),
            R("free_cash_flow", 3470, "usd_millions", "PANW FY2025 free cash flow, +11.9% YoY"),
            R("capex", 423.2, "usd_millions", "PANW FY2025 capital expenditures", limitation="A derived cross-check (OCF $3.7B minus capex $423.2M = $3.28B) does not exactly match the stated $3.47B FCF; a minor inconsistency in the underlying search snippets that could not be resolved."),
            R("cash", 2370, "usd_millions", "PANW cash, end of FY2025 (Jul 31 2025)"),
        ]),
    ],
    segment_abstain="PANW does not report classic geographic/business-unit segments in what was found; it discloses Product revenue vs. a recurring services/subscription revenue line plus a headline Next-Generation Security ARR metric, but only at the quarterly level (Q4 FY2025: Product $573.9M +19% YoY, the recurring line ~$2.0B +15% YoY) -- a full-year segment split was not found.",
    price=mk_price(364.27, "Aug 9 2026 (well-sourced, day range $359.15-$370.50)."),
    peers_data=[
        ("CRWD", "CrowdStrike -- cloud-native cybersecurity platform, direct competitive overlap in endpoint/XDR."),
        ("FTNT", "Fortinet -- network security appliance/platform competitor."),
        ("ZS", "Zscaler -- cloud/SASE security competitor, overlaps with PANW's Prisma SASE push."),
    ],
    scenarios_data=[
        ("CyberArk acquisition", "Definitive agreement announced Jul 30 2025 (~$25B deal, $45.00 cash + 2.2005 PANW shares per CyberArk share); completed Feb 11 2026, establishing Identity Security as a new core platform pillar."),
    ],
    uncertainty_summary=(
        "All figures secondary/search-aggregation-sourced; no primary document directly opened. FY2025 "
        "GAAP net income and diluted EPS are genuinely unresolved between two irreconcilable search "
        "results and are abstained rather than reported. Operating income/margin was not found for any "
        "fiscal year. FY2024 net income is disclosed as containing a large one-time tax benefit, not a "
        "clean operating result. The CyberArk acquisition, closed Feb 2026, will materially change the "
        "FY2026 balance sheet (added debt/goodwill) and consolidated results -- FY2026-forward figures "
        "will not be cleanly comparable to the FY2021-FY2025 history above."
    ),
)

RECORDS["SNPS"] = build(
    "SNPS",
    periods=[
        mk_period("2021-10-31", [
            R("revenue", 4204, "usd_millions", "SNPS FY2021 (ended late Oct 2021) revenue"),
            R("earnings", 757.5, "usd_millions", "SNPS FY2021 net income"),
        ]),
        mk_period("2022-10-31", [
            R("revenue", 4615.7, "usd_millions", "SNPS FY2022 revenue"),
            abstain_item("earnings", "The FY2022 net income figure returned by search ($757.5M) is identical to the independently-reported FY2021 figure, which is implausible for two different fiscal years to the tenth of a million -- treated as a likely data-extraction error and not reported as fact."),
        ]),
        mk_period("2023-10-31", [
            R("revenue", 5318.0, "usd_millions", "SNPS FY2023 revenue"),
            R("earnings", 984.6, "usd_millions", "SNPS FY2023 net income"),
        ]),
        mk_period("2024-10-31", [
            R("revenue", 6127, "usd_millions", "SNPS FY2024 revenue"),
            R("earnings", 1442, "usd_millions", "SNPS FY2024 net income"),
        ]),
        mk_period("2025-10-31", [
            R("revenue", 7054, "usd_millions", "SNPS FY2025 revenue, includes $756.6M from the newly-acquired Ansys"),
            R("earnings", 1336, "usd_millions", "SNPS FY2025 net income"),
            D("operating_margin", 0.130, "ratio", "Derived: FY2025 operating income $914.9M divided by revenue $7,054M equals 13.0 percent -- notably below the 18.9% implied net margin, an unusual pattern likely reflecting a below-the-line gain (plausibly related to the Sept 30 2024 Software Integrity Group divestiture and/or Ansys-deal items), but the specific gain amount was not confirmed this session.", "SNPS FY2025 operating income $914.9M"),
            R("free_cash_flow", 1420, "usd_millions", "SNPS FY2025 free cash flow", limitation="A derived cross-check (OCF $1.74B minus capex $169M = $1.571B) does not cleanly match the stated $1.42B FCF; a minor unresolved inconsistency in the underlying search snippets."),
            R("capex", 169, "usd_millions", "SNPS FY2025 capital expenditures"),
            R("cash", 1420, "usd_millions", "SNPS cash, Oct 31 2025"),
            R("debt", 13500, "usd_millions", "SNPS total debt, end of FY2025 (Oct 2025)", limitation="A later, post-paydown snapshot (Q2 FY2026, ~Apr 2026) showed total debt of $10.0B -- both figures disclosed, different dates; debt was raised specifically to fund the ~$35B Ansys acquisition."),
            D("share_count_diluted", 165.6, "shares_millions", "Derived (approximate): FY2025 net income $1,336M divided by diluted EPS $8.07 equals ~165.6M diluted shares. Not a directly reported figure.", "SNPS FY2025 net income and diluted EPS figures above"),
        ]),
    ],
    segment_abstain="Segment (Design Automation vs. Design IP, and post-Ansys potentially a simulation/systems-design category) revenue breakdown for FY2025 was not obtained -- the research session's search budget was exhausted before this could be located. A genuine gap, not filled with an estimate.",
    price_abstain="Current SNPS stock price and market capitalization were not obtained this session -- the research session's search budget was exhausted before a reliable figure could be retrieved.",
    peers_data=[
        ("CDNS", "Cadence Design Systems -- the closest direct peer, the other dominant player in electronic design automation (EDA) software."),
        ("KEYS", "Keysight Technologies -- electronic design/test/measurement software and instruments, adjacent to SNPS's chip-design tooling."),
        ("PTC", "PTC Inc -- engineering/product-lifecycle design software, less direct than CDNS but a reasonable comparable given SNPS's expanded post-Ansys simulation/systems-design footprint."),
    ],
    scenarios_data=[
        ("Ansys acquisition", "~$35B deal, closed Q3 FY2025; materially reshapes SNPS's revenue base, debt load, and competitive positioning (moving from pure EDA into simulation/'Silicon to Systems' design). Ansys contributed $756.6M of FY2025 revenue ($667.7M in Q4 FY2025 alone)."),
        ("Software Integrity Group divestiture", "Sold to Clearlake Capital and Francisco Partners for $1.65B total consideration ($1.48B upfront cash plus deferred/earnout payments), transaction completed Sept 30 2024."),
    ],
    uncertainty_summary=(
        "All figures secondary/search-aggregation-sourced; no primary document directly opened. FY2022 net "
        "income is abstained as an apparent data-extraction error (identical to FY2021's figure). Current "
        "stock price, market cap, and full-year segment revenue were not obtained -- genuine gaps, not "
        "estimated. This is the most significant comparability case in this research pass: Synopsys "
        "underwent two major structural events within ~18 months of FY2025 (the Sept 2024 Software "
        "Integrity Group divestiture, reclassified as discontinued operations, and the ~$35B Ansys "
        "acquisition, closed Q3 FY2025) -- only FY2021-FY2023 (three years) can be considered clean, "
        "pre-transformation comparable history; FY2024 reflects the divestiture transition and FY2025 "
        "reflects partial-year Ansys consolidation. This is the disclosed IPO/restructuring shortened-"
        "history exception under VALUATION-0005 SS C.1, applied here for a genuine structural limitation "
        "rather than forcing a misleading 5-year like-for-like comparison."
    ),
)

# ============================================================
# Batch B -- shard 2 (partial): META, MSFT, GOOGL. (AMZN, AVGO pending supplemental research)
# ============================================================

RECORDS["META"] = build(
    "META",
    periods=[
        mk_period("2021-12-31", [
            R("revenue", 117929, "usd_millions", "META FY2021 revenue"),
            R("earnings", 39370, "usd_millions", "META FY2021 net income"),
            D("operating_margin", 0.396, "ratio", "Derived: FY2021 operating income $46,753M divided by revenue $117,929M equals 39.6 percent.", "META FY2021 operating income $46,753M"),
        ]),
        mk_period("2022-12-31", [
            R("revenue", 116609, "usd_millions", "META FY2022 revenue"),
            R("earnings", 23200, "usd_millions", "META FY2022 net income"),
            D("operating_margin", 0.248, "ratio", "Derived: FY2022 operating income $28,944M divided by revenue $116,609M equals 24.8 percent.", "META FY2022 operating income $28,944M"),
        ]),
        mk_period("2023-12-31", [
            R("revenue", 134902, "usd_millions", "META FY2023 revenue"),
            R("earnings", 39098, "usd_millions", "META FY2023 net income"),
            D("operating_margin", 0.347, "ratio", "Derived: FY2023 operating income $46,751M divided by revenue $134,902M equals 34.7 percent.", "META FY2023 operating income $46,751M"),
        ]),
        mk_period("2024-12-31", [
            R("revenue", 164501, "usd_millions", "META FY2024 revenue"),
            R("earnings", 62360, "usd_millions", "META FY2024 net income"),
            D("operating_margin", 0.422, "ratio", "Derived: FY2024 operating income $69,380M divided by revenue $164,501M equals 42.2 percent.", "META FY2024 operating income $69,380M"),
        ]),
        mk_period("2025-12-31", [
            R("revenue", 200966, "usd_millions", "META FY2025 revenue"),
            R("earnings", 60458, "usd_millions", "META FY2025 net income", limitation="Lower than FY2024's $62,360M despite operating income rising 20%; press coverage links this to a large one-time Q4 2025 US tax-law-related charge, but the exact mechanism was not independently verified this session."),
            R("operating_margin", 0.414, "ratio", "META FY2025 operating margin (company-reported ~41%, matching the derived calc of $83,276M/$200,966M=41.4%)"),
            R("free_cash_flow", 43590, "usd_millions", "META FY2025 free cash flow (also ties out: OCF $115,800M minus capex $72,220M = $43,580M, consistent)"),
            R("capex", 72220, "usd_millions", "META FY2025 capital expenditures", limitation="Company disclosure notes this figure includes principal payments on finance leases, not pure capex."),
            R("debt", 58740, "usd_millions", "META long-term debt, Dec 31 2025"),
            D("share_count_diluted", 2573, "shares_millions", "Derived (approximate): FY2025 net income $60,458M divided by diluted EPS $23.49 equals ~2,573M diluted shares.", "META FY2025 net income and diluted EPS figures"),
        ]),
    ],
    segments=[
        segment("Family of Apps", revenue=D("revenue", 198696, "usd_millions", "Derived: total revenue $200,966M minus Reality Labs revenue $2,270M equals $198,696M.", "META FY2025 total and Reality Labs revenue"),
                 profit=D("earnings", 102469, "usd_millions", "Derived: total operating income $83,276M minus Reality Labs operating loss of -$19,193M equals $102,469M.", "META FY2025 total and Reality Labs operating income")),
        segment("Reality Labs", revenue=R("revenue", 2270, "usd_millions", "META FY2025 Reality Labs segment revenue"),
                 profit=R("earnings", -19193, "usd_millions", "META FY2025 Reality Labs segment operating loss")),
    ],
    price=mk_price(591.93, "Observed ~Aug 8 2026 (day range $584.95-$598.74, 52-week range $520.26-$796.25)."),
    peers_data=[
        ("GOOGL", "Direct digital-advertising duopoly peer, similar ad-auction/targeting business model."),
        ("SNAP", "Smaller social/short-form-video advertising peer with comparable engagement-driven ad monetization."),
        ("PINS", "Pinterest -- visual-discovery social advertising peer, similar ad-load/engagement dynamics."),
    ],
    scenarios_data=[
        ("AI capex trajectory", "META raised FY2026 capex guidance to $130-145B (narrowed from a prior $125-145B range), citing higher component pricing and data-center buildout costs."),
        ("Antitrust/regulatory posture", "META prevailed in the FTC's antitrust case challenging its Instagram/WhatsApp acquisitions; EU Digital Markets Act 'pay-or-consent' pressure and youth-related litigation remain live regulatory/legal risks."),
    ],
    uncertainty_summary=(
        "All figures secondary/search-aggregation-sourced (accessed via WebSearch's own retrieval layer, "
        "not a directly-opened primary document -- SEC.gov and Meta's own IR pages were blocked for direct "
        "fetch). FY2025 net income is lower than FY2024's despite higher operating income; the specific "
        "tax mechanism driving that is disclosed as unverified. Pure cash-only balance (vs. combined "
        "cash+marketable-securities) and a sourced FY2025 buyback dollar figure were not found. META's "
        "current two-segment structure (Family of Apps/Reality Labs) has been used since 2021, so all "
        "five years shown are internally comparable; pre-2021 historicals under the prior single-segment "
        "structure would not be."
    ),
)

RECORDS["MSFT"] = build(
    "MSFT",
    periods=[
        mk_period("2022-06-30", [
            R("revenue", 198270, "usd_millions", "MSFT FY2022 (ended Jun 30 2022) revenue"),
            R("earnings", 72700, "usd_millions", "MSFT FY2022 net income", limitation="Approximate/rounded figure from search aggregation."),
            D("operating_margin", 0.421, "ratio", "Derived: FY2022 operating income $83,383M divided by revenue $198,270M equals 42.1 percent.", "MSFT FY2022 operating income $83,383M"),
        ]),
        mk_period("2023-06-30", [
            R("revenue", 211915, "usd_millions", "MSFT FY2023 revenue"),
            R("earnings", 72361, "usd_millions", "MSFT FY2023 net income"),
            D("operating_margin", 0.418, "ratio", "Derived: FY2023 operating income $88,523M divided by revenue $211,915M equals 41.8 percent.", "MSFT FY2023 operating income $88,523M"),
        ]),
        mk_period("2024-06-30", [
            R("revenue", 245122, "usd_millions", "MSFT FY2024 revenue"),
            R("earnings", 88136, "usd_millions", "MSFT FY2024 net income"),
            D("operating_margin", 0.446, "ratio", "Derived: FY2024 operating income $109,433M divided by revenue $245,122M equals 44.6 percent.", "MSFT FY2024 operating income $109,433M"),
        ]),
        mk_period("2025-06-30", [
            R("revenue", 281700, "usd_millions", "MSFT FY2025 revenue", limitation="Rounded figure from search aggregation, not exact-to-the-million."),
            R("earnings", 101800, "usd_millions", "MSFT FY2025 net income", limitation="Rounded figure from search aggregation."),
            D("operating_margin", 0.456, "ratio", "Derived: FY2025 operating income ~$128,500M divided by revenue ~$281,700M equals ~45.6 percent (both approximate).", "MSFT FY2025 operating income ~$128,500M (approximate)"),
        ]),
        mk_period("2026-06-30", [
            R("revenue", 331800, "usd_millions", "MSFT FY2026 (ended Jun 30 2026) revenue"),
            R("earnings", 133700, "usd_millions", "MSFT FY2026 net income (GAAP)", limitation="Includes effects of OpenAI-investment-related items and one-time discrete items (Microsoft's own Q4 non-GAAP reconciliation disclosed several discrete items benefited Q4 EPS by $0.27) not fully itemized in what was found."),
            D("operating_margin", 0.468, "ratio", "Derived: FY2026 operating income $155,200M divided by revenue $331,800M equals 46.8 percent; consistent with Microsoft's own 'operating income increased 21%' framing.", "MSFT FY2026 operating income $155,200M"),
            R("free_cash_flow", 67000, "usd_millions", "MSFT FY2026 free cash flow (ties to OCF $182,900M minus capex $115,900M = $67,000M, consistent)"),
            R("capex", 115900, "usd_millions", "MSFT FY2026 capital expenditures (reported actual)", limitation="A separate source cited '~$175B in capex plus finance leases combined' for FY2026 guidance, which is inconsistent with this $115.9B actual figure; not reconciled, disclosed as a conflict."),
            R("debt", 125400, "usd_millions", "MSFT total debt (single source, notably higher than MSFT's historical debt load, plausibly new debt issuance funding AI capex in 2026, not independently corroborated)"),
            R("share_count_diluted", 7445, "shares_millions", "MSFT diluted shares outstanding, Q3 FY2026 quarter", limitation="Full-year weighted-average diluted shares implied by net income/EPS ($133,700M / $17.95 = ~7,449M) is consistent with this quarterly figure."),
        ]),
    ],
    segments=[
        segment("Productivity and Business Processes", revenue=R("revenue", 139996, "usd_millions", "MSFT FY2026 Productivity and Business Processes segment revenue"), profit=R("earnings", 83879, "usd_millions", "MSFT FY2026 Productivity and Business Processes segment operating income")),
        segment("Intelligent Cloud", revenue=R("revenue", 137791, "usd_millions", "MSFT FY2026 Intelligent Cloud segment revenue"), profit=R("earnings", 56972, "usd_millions", "MSFT FY2026 Intelligent Cloud segment operating income")),
        segment("More Personal Computing", revenue=D("revenue", 54013, "usd_millions", "Derived: total FY2026 revenue $331,800M minus Productivity and Business Processes $139,996M minus Intelligent Cloud $137,791M equals $54,013M.", "MSFT FY2026 total, PBP, and Intelligent Cloud segment revenue"), profit=D("earnings", 14349, "usd_millions", "Derived: total FY2026 operating income $155,200M minus PBP $83,879M minus Intelligent Cloud $56,972M equals $14,349M.", "MSFT FY2026 total, PBP, and Intelligent Cloud segment operating income")),
    ],
    price=mk_price(499.99, "Observed Aug 8 2026 (day range $498.73-$505.18, 52-week range $349.20-$553.72)."),
    peers_data=[
        ("AMZN", "Direct hyperscale cloud-infrastructure peer (AWS vs. Azure)."),
        ("GOOGL", "Cloud + enterprise AI comparator (Google Cloud vs. Azure), also overlapping in productivity software (Workspace vs. Microsoft 365)."),
        ("ORCL", "Oracle -- enterprise software/database and increasingly cloud-infrastructure peer with a similarly aggressive AI-datacenter capex ramp."),
    ],
    scenarios_data=[
        ("OpenAI partnership and Azure commitment", "MSFT holds a 27% equity stake in OpenAI (reported value ~$135B), restructured to a non-exclusive commercial partnership through 2032; on Oct 28 2025 OpenAI signed a definitive agreement to purchase an incremental $250B of Azure services beyond existing commitments."),
        ("AI capex trajectory and disclosure litigation", "FY2026 capex is running well above one cited analyst-consensus figure (a ~$35B beat, ~$25B attributed to component price inflation per one source, though this conflicts with the $115.9B actual capex figure above and is not reconciled); a Michigan pension fund sued MSFT in Seattle federal court (June 2026) alleging misleading disclosures about Azure growth deceleration and AI infrastructure spending pressure."),
    ],
    uncertainty_summary=(
        "All figures secondary/search-aggregation-sourced; no primary document directly opened. FY2022 "
        "and FY2025 net income and FY2025 revenue/operating-income figures are rounded/approximate rather "
        "than exact-to-the-million. Balance sheet cash is the weakest-sourced item: one source's pure-cash "
        "figure ($32,105M, unclear date) was not reconciled against a separate combined cash+short-term-"
        "investments figure ($78.272B); total debt ($125.4B) traces to a single, uncorroborated source. "
        "FY2026 capex ($115.9B actual, reported) conflicts with a separate, larger guidance-based figure "
        "found elsewhere; both are disclosed rather than one being silently chosen. Microsoft has reported "
        "under the same three-segment structure for the entire FY2022-FY2026 window shown, so the data "
        "should be comparable across all five years."
    ),
)

RECORDS["GOOGL"] = build(
    "GOOGL",
    periods=[
        mk_period("2021-12-31", [
            R("revenue", 257637, "usd_millions", "GOOGL FY2021 revenue"),
            R("earnings", 76033, "usd_millions", "GOOGL FY2021 net income"),
            D("operating_margin", 0.306, "ratio", "Derived: FY2021 operating income $78,714M divided by revenue $257,637M equals 30.6 percent.", "GOOGL FY2021 operating income $78,714M"),
        ]),
        mk_period("2022-12-31", [
            R("revenue", 282836, "usd_millions", "GOOGL FY2022 revenue"),
            R("earnings", 59972, "usd_millions", "GOOGL FY2022 net income"),
            R("operating_margin", 0.265, "ratio", "GOOGL FY2022 operating margin (Alphabet's own cited rounded figure of 26%, consistent with derived $74,842M/$282,836M=26.5%)"),
        ]),
        mk_period("2023-12-31", [
            R("revenue", 307394, "usd_millions", "GOOGL FY2023 revenue"),
            R("earnings", 73795, "usd_millions", "GOOGL FY2023 net income"),
            R("operating_margin", 0.274, "ratio", "GOOGL FY2023 operating margin (Alphabet's own cited rounded figure of 27%, consistent with derived $84,293M/$307,394M=27.4%)"),
        ]),
        mk_period("2024-12-31", [
            R("revenue", 350018, "usd_millions", "GOOGL FY2024 revenue"),
            R("earnings", 100118, "usd_millions", "GOOGL FY2024 net income"),
            R("operating_margin", 0.321, "ratio", "GOOGL FY2024 operating margin (Alphabet's own cited rounded figure of 32%, consistent with derived $112,390M/$350,018M=32.1%)"),
        ]),
        mk_period("2025-12-31", [
            R("revenue", 402836, "usd_millions", "GOOGL FY2025 revenue -- first time Alphabet's annual revenue exceeded $400B"),
            R("earnings", 132170, "usd_millions", "GOOGL FY2025 net income", limitation="Net income growth (32%) notably outpaced revenue growth (15%); the exact composition of that gap (margin expansion vs. other income/gains) was not independently verified this session."),
            R("operating_margin", 0.320, "ratio", "GOOGL FY2025 operating margin (Alphabet's own cited rounded figure of 32%, consistent with derived $129,039M/$402,836M=32.0%)"),
            R("free_cash_flow", 73266, "usd_millions", "GOOGL FY2025 free cash flow (ties exactly: OCF $164,713M minus capex $91,447M = $73,266M)"),
            R("capex", 91447, "usd_millions", "GOOGL FY2025 capital expenditures (purchases of property and equipment)"),
            R("cash", 30708, "usd_millions", "GOOGL cash and cash equivalents, Dec 31 2025"),
            D("cash", 126843, "usd_millions", "Derived: cash $30,708M plus marketable securities $96,135M equals $126,843M combined.", "GOOGL balance sheet, Dec 31 2025"),
            R("debt", 46547, "usd_millions", "GOOGL long-term debt, Dec 31 2025", limitation="This is specifically long-term debt; a total-debt-including-current-portion figure was not found, so net debt/net cash is not confidently derivable (though Alphabet is very likely in a large net-cash position given >$126B in cash/securities vs. ~$46.5B long-term debt)."),
            D("share_count_diluted", 12227, "shares_millions", "Derived (approximate): FY2025 net income $132,170M divided by diluted EPS $10.81 equals ~12,227M diluted shares. (Total shares outstanding, a different figure, was separately reported at 12,088M across Class A/B/C.)", "GOOGL FY2025 net income and diluted EPS figures"),
        ]),
    ],
    segments=[
        segment("Google Search & Other", revenue=R("revenue", 224530, "usd_millions", "GOOGL FY2025 Google Search & Other segment revenue")),
        segment("Google Cloud", revenue=R("revenue", 58710, "usd_millions", "GOOGL FY2025 Google Cloud segment revenue, up from $43.23B in 2024, +35.8% reported growth")),
        segment("Other Bets", revenue=R("revenue", 1540, "usd_millions", "GOOGL FY2025 Other Bets segment revenue")),
    ],
    price_abstain="Genuinely conflicting figures were found for GOOGL's current price/market cap ($356.72 vs. 'trading near $375-378'; market cap reported as both '$4.32T' and '$4.271T' from different sources, with mention of a GOOGL/GOOG class distinction and a stock decline tied to an AI-leadership departure) -- not resolved to a single confident figure, so abstained rather than picking one arbitrarily.",
    peers_data=[
        ("MSFT", "Cloud infrastructure (Azure vs. Google Cloud) and enterprise AI comparator."),
        ("AMZN", "Cloud infrastructure (AWS vs. Google Cloud) and, secondarily, digital advertising comparator."),
        ("META", "Direct digital-advertising duopoly peer."),
    ],
    scenarios_data=[
        ("DOJ Google Search antitrust remedies", "Final judgment entered December 2025 imposing behavioral remedies (data-sharing/syndication requirements, restrictions on distribution deals); Google appealed January 2026, DOJ and state AGs cross-appealed February 2026. Morgan Stanley estimated mandatory choice-screen remedies could cost Google 5-8% of search traffic over three years, translating to an estimated $15-25B in annual ad revenue at risk."),
    ],
    uncertainty_summary=(
        "All figures secondary/search-aggregation-sourced; no primary document directly opened. Current "
        "stock price and market cap could not be resolved to one confident figure (genuine conflict "
        "between sources) and are abstained. Full-year Google Cloud and Other Bets operating income were "
        "not obtained (only Q4-2025-alone figures were found) -- a genuine segment-evidence gap, so only "
        "segment revenue (not profit) is reported here. Net debt is not confidently derivable given only a "
        "long-term-debt figure (no total-debt-including-current-portion). Alphabet's three-segment "
        "structure has been used consistently 2021-2025, though full segment-boundary consistency across "
        "all five years was not independently verified."
    ),
)


# ============================================================
# Batch C -- shard 3: ASML, TSM, KLAC, CEG, GEV
# ============================================================

RECORDS["ASML"] = build(
    "ASML",
    periods=[
        mk_period("2021-12-31", [
            R("revenue", 18611, "eur_millions", "ASML FY2021 net sales"),
            R("earnings", 5883, "eur_millions", "ASML FY2021 net income"),
            D("operating_margin", 0.363, "ratio", "Derived: FY2021 operating income EUR6,750M divided by net sales EUR18,611M equals 36.3 percent.", "ASML FY2021 operating income EUR6,750M"),
        ]),
        mk_period("2022-12-31", [
            R("revenue", 21173, "eur_millions", "ASML FY2022 net sales"),
            R("earnings", 5624, "eur_millions", "ASML FY2022 net income"),
            D("operating_margin", 0.307, "ratio", "Derived: FY2022 operating income EUR6.5B divided by net sales EUR21,173M equals 30.7 percent.", "ASML FY2022 operating income EUR6.5B"),
        ]),
        mk_period("2023-12-31", [
            R("revenue", 27560, "eur_millions", "ASML FY2023 net sales"),
            R("earnings", 7840, "eur_millions", "ASML FY2023 net income"),
            D("operating_margin", 0.328, "ratio", "Derived: FY2023 operating income EUR9.04B divided by net sales EUR27.56B equals 32.8 percent.", "ASML FY2023 operating income EUR9.04B"),
        ]),
        mk_period("2024-12-31", [
            R("revenue", 28300, "eur_millions", "ASML FY2024 net sales"),
            R("earnings", 7600, "eur_millions", "ASML FY2024 net income"),
            abstain_item("operating_margin", "The one FY2024 operating-income figure found (~EUR9.76B, currency-tag inconsistent/suspicious across sources) was not reliable enough to derive a confident operating margin."),
        ]),
        mk_period("2025-12-31", [
            R("revenue", 32700, "eur_millions", "ASML FY2025 net sales"),
            R("earnings", 9609, "eur_millions", "ASML FY2025 net income"),
            abstain_item("operating_margin", "Full-year FY2025 operating income was not found; only gross margin (52.8%, reported) and a rough, explicitly-non-full-year Q4-based extrapolation (~35%) were located -- the latter is not reported here as a full-year figure."),
            R("cash", 10999.7, "eur_millions", "ASML cash & equivalents, Dec 31 2025"),
            D("debt", 4375, "eur_millions", "Derived: long-term debt EUR2,692.7M plus short-term debt EUR1,681.9M equals ~EUR4,375M total.", "ASML balance sheet, Dec 31 2025"),
            D("share_count_diluted", 388.5, "shares_millions", "Derived (approximate): FY2025 net income EUR9,609.4M divided by diluted EPS EUR24.73 equals ~388.5M diluted shares. (A separate '34.9 million shares' figure found elsewhere is implausibly low for ASML and was rejected as an evident error.)", "ASML FY2025 net income and diluted EPS figures"),
        ]),
    ],
    segments=[
        segment("EUV systems", revenue=R("revenue", 11600, "eur_millions", "ASML FY2025 EUV systems revenue, +39% YoY, 48 systems recognized")),
        segment("DUV systems", revenue=R("revenue", 12000, "eur_millions", "ASML FY2025 DUV systems revenue, -6% YoY, 279 systems recognized")),
        segment("Installed Base Management", revenue=R("revenue", 8200, "eur_millions", "ASML FY2025 Installed Base Management revenue, +26% YoY")),
    ],
    price=mk_price(1740.99, "Nasdaq ADR close, Aug 7 2026 (EUR1,499.00 on Euronext Amsterdam, Aug 8 2026). Market cap reported in a $640-669B range across sources."),
    peers_data=[
        ("KLAC", "KLA Corporation -- semiconductor process-control equipment, adjacent capital-equipment peer."),
        ("LRCX", "Lam Research -- semiconductor deposition/etch equipment, adjacent capital-equipment peer."),
        ("AMAT", "Applied Materials -- broad semiconductor capital equipment peer."),
    ],
    scenarios_data=[
        ("China export-control exposure", "China share of ASML revenue fell from ~36% (Q4 2025) to ~19% (Q1 2026); full-year 2025 China share ~33%. EUV has never shipped to China (restricted since 2023). A pending US MATCH Act would ban DUV immersion-system exports/servicing to China -- not yet law, and contains a 150-day window for the Netherlands/Japan to tighten their own controls first."),
    ],
    uncertainty_summary=(
        "All figures secondary/search-aggregation-sourced; no primary document directly opened. ASML "
        "reports in EUR; figures above are as-reported in that currency, not converted to USD. FY2024 and "
        "FY2025 operating margin are abstained -- the underlying operating-income figures found carried "
        "currency-tag inconsistencies or were not full-year figures. A cash-flow/capex multi-year table "
        "was attempted but the figures found were USD-labeled (suspicious for a EUR reporter) and are not "
        "used. No IPO/spin-off/restructuring affects ASML's own 5-year comparability."
    ),
)

RECORDS["TSM"] = build(
    "TSM",
    periods=[
        mk_period("2021-12-31", [
            R("revenue", 1587.42, "twd_billions", "TSM FY2021 revenue"),
            R("earnings", 596.54, "twd_billions", "TSM FY2021 net income"),
        ]),
        mk_period("2022-12-31", [
            R("revenue", 2263.89, "twd_billions", "TSM FY2022 revenue"),
            R("earnings", 1016.53, "twd_billions", "TSM FY2022 net income"),
        ]),
        mk_period("2023-12-31", [
            R("revenue", 2161.74, "twd_billions", "TSM FY2023 revenue"),
            R("earnings", 838.50, "twd_billions", "TSM FY2023 net income"),
        ]),
        mk_period("2024-12-31", [
            R("revenue", 2894.31, "twd_billions", "TSM FY2024 revenue"),
            R("earnings", 1173.27, "twd_billions", "TSM FY2024 net income"),
            R("net_margin", 0.405, "ratio", "TSM FY2024 net margin (company-reported)"),
        ]),
        mk_period("2025-12-31", [
            R("revenue", 3809.05, "twd_billions", "TSM FY2025 revenue"),
            R("earnings", 1717.88, "twd_billions", "TSM FY2025 net income"),
            D("revenue", 122.42, "usd_billions", "USD-equivalent of the TWD-reported FY2025 revenue figure, as separately disclosed by TSMC for ADR investors (a second source cited $122.9B, ~0.4% variance, not reconciled).", "TSM FY2025 USD-equivalent revenue disclosure"),
            R("gross_margin", 0.599, "ratio", "TSM FY2025 gross margin (2024: 56.1%)"),
            R("operating_margin", 0.508, "ratio", "TSM FY2025 operating margin (2024: 45.7%)"),
            R("net_margin", 0.451, "ratio", "TSM FY2025 net margin (2024: 40.5%)"),
            R("capex", 40.9, "usd_billions", "TSM FY2025 capital expenditures (2024: $29.8B)"),
            R("total_assets", 252.291, "usd_billions", "TSM total assets, FY2025"),
            R("total_equity", 173.6, "usd_billions", "TSM total equity, FY2025"),
            R("debt", 34.07, "usd_billions", "TSM total debt (single aggregator, not cross-verified against a primary filing)"),
            D("share_count_diluted", 5186, "shares_millions_adr_equivalent", "Derived: ~25,929M ordinary shares divided by 5 (ADR ratio) equals ~5,186M ADR-equivalent diluted shares.", "TSM diluted weighted-average ordinary shares, FY2025"),
        ]),
    ],
    segment_abstain="TSM does not disclose dollar-denominated business segments in the classic sense; it discloses revenue mix by technology node (3nm 24%, 5nm 36%, 7nm 14%, mature/16nm+ 26% of FY2025 revenue) and by platform (HPC 57%, Smartphone 30%, IoT 5%, Automotive 5%, DCE 1%, Other 2%) -- percentage-of-revenue mix data, not the dollar-value segment table this schema's segment_evidence domain expects.",
    price=mk_price(422.82, "Aug 7 2026 close; market cap reported ~$2.178T."),
    peers_data=[
        ("ASML", "Critical lithography-equipment supplier to TSM, not a direct manufacturing competitor but tightly linked in the value chain."),
    ],
    scenarios_data=[
        ("Arizona fab expansion", "Up to 12 fabs planned; additional $100B+ committed for at least 4 more 2nm fabs; second Phase-2 Arizona fab volume production pulled forward to 2H2027 citing strong/urgent demand from US customers."),
        ("CoWoS advanced-packaging capacity", "CoWoS advanced packaging was the primary AI-chip production bottleneck through 2025, running at full capacity; TSMC is accelerating CoWoS/InFO/SoIC expansion."),
    ],
    uncertainty_summary=(
        "All figures secondary/search-aggregation-sourced; no primary document directly opened. TSM "
        "reports in NT$; the annual revenue/net-income trend above is in TWD as reported, with a single "
        "disclosed USD-equivalent figure for FY2025 revenue only (two sources disagreed by ~0.4%, not "
        "reconciled). A reported cash balance figure ('~$94.67B', apparently EUR-labeled for a Taiwan "
        "company) was found to be evidently garbled and is not used -- cash is abstained from the balance "
        "sheet items above as a result. Full-year operating cash flow was not found (only a single "
        "quarter's figure). Diluted EPS in TWD (2023/2024) was not found and is omitted rather than "
        "guessed. No IPO/spin-off/restructuring affects TSM's own 5-year comparability."
    ),
)

RECORDS["KLAC"] = build(
    "KLAC",
    periods=[
        mk_period("2021-06-30", [
            R("revenue", 6920, "usd_millions", "KLAC FY2021 (ended Jun 30 2021) revenue"),
            R("earnings", 2080, "usd_millions", "KLAC FY2021 net income"),
        ]),
        mk_period("2022-06-30", [
            R("revenue", 9210, "usd_millions", "KLAC FY2022 revenue"),
            R("earnings", 3320, "usd_millions", "KLAC FY2022 net income"),
        ]),
        mk_period("2023-06-30", [
            R("revenue", 10500, "usd_millions", "KLAC FY2023 revenue"),
            R("earnings", 3390, "usd_millions", "KLAC FY2023 net income"),
        ]),
        mk_period("2024-06-30", [
            R("revenue", 9810, "usd_millions", "KLAC FY2024 revenue"),
            R("earnings", 2760, "usd_millions", "KLAC FY2024 net income"),
        ]),
        mk_period("2025-06-30", [
            R("revenue", 12160, "usd_millions", "KLAC FY2025 revenue"),
            R("earnings", 4060, "usd_millions", "KLAC FY2025 net income"),
            R("free_cash_flow", 3745, "usd_millions", "KLAC FY2025 free cash flow (reported as both '$3.75B' and '$3.74B' across two sources -- rounding, not a material discrepancy)"),
            R("capex", 340, "usd_millions", "KLAC FY2025 capital expenditures"),
            D("cash", 4490, "usd_millions", "Derived: cash & equivalents $2.08B plus marketable securities $2.42B equals ~$4.49B total liquid assets.", "KLAC balance sheet, Jun 30 2025"),
            R("debt", 5880, "usd_millions", "KLAC long-term debt, Jun 30 2025"),
            D("net_debt", 1600, "usd_millions", "Derived (approximate): long-term debt $5.88B minus liquid assets ~$4.49B equals ~$1.6B net debt.", "KLAC balance sheet figures above"),
            R("share_count_diluted", 132.0, "shares_millions", "KLAC diluted shares outstanding, Jun 30 2025 -- PRE-SPLIT figure.", limitation="KLA executed a 10-for-1 forward stock split effective June 12 2026 (record date Jun 4 2026). All EPS and share-count figures in this record for FY2021-FY2025 are pre-split; the current stock price (below) is post-split. Do not compare EPS-to-price across this boundary without adjusting (pre-split share count x10 implies ~1.32B post-split shares)."),
        ]),
    ],
    segment_abstain="Only a single quarter's segment breakdown was found (Q1 FY2026 / Sept 2025: Semiconductor Process Control $2.90B, Specialty Semiconductor Process $120M, PCB & Component Inspection $189M) -- a full FY2025 annual segment split was not located.",
    price=mk_price(198.11, "Aug 7 2026, POST-split (52-week range $83.22-$307.37, all-time high Jun 30 2026). Market cap conflicting across sources: $252.45B / $258.79B / $273.54B -- not resolved to one figure."),
    peers_data=[
        ("ASML", "Semiconductor capital equipment peer -- ASML specializes in lithography, KLA in process control/inspection; adjacent, not identical business models."),
        ("LRCX", "Lam Research -- deposition/etch equipment, adjacent capital-equipment peer."),
        ("AMAT", "Applied Materials -- broad semiconductor capital equipment peer."),
    ],
    scenarios_data=[
        ("China export-control exposure", "China was ~30-31% of recent revenue (down from 34.3% a year earlier; historically 41-44% before controls tightened). US BIS export controls and a Commerce Department order to halt shipments to Chinese chipmaker Hua Hong; Jefferies estimated ~$300-350M CY2026 revenue impact."),
    ],
    uncertainty_summary=(
        "All figures secondary/search-aggregation-sourced; no primary document directly opened. KLA "
        "executed a 10-for-1 forward stock split effective June 12 2026 -- every FY2021-FY2025 EPS and "
        "share-count figure above is pre-split scale, while the current stock price is post-split; this "
        "is flagged prominently rather than silently mixed. Operating income/margin was not found for any "
        "fiscal year and is omitted rather than estimated. Full fiscal-year segment revenue was not found "
        "(only a single quarter's breakdown, disclosed as such but not used as segment_evidence here). "
        "Current market capitalization is unresolved across three conflicting sources."
    ),
)

RECORDS["CEG"] = build(
    "CEG",
    periods=[
        mk_period("2022-12-31", [
            R("revenue", 24440, "usd_millions", "CEG FY2022 revenue", limitation="CEG was spun off from Exelon Corporation on Feb 1 2022 -- FY2022 mixes ~1 month of standalone-public-company results with Exelon-carve-out predecessor-basis results for the rest of the year, so this is not a clean standalone fiscal year."),
            R("earnings", -160, "usd_millions", "CEG FY2022 GAAP net loss (approximate)"),
        ]),
        mk_period("2023-12-31", [
            R("revenue", 24918, "usd_millions", "CEG FY2023 revenue -- first clean full standalone calendar year"),
            R("earnings", 1620, "usd_millions", "CEG FY2023 GAAP net income"),
        ]),
        mk_period("2024-12-31", [
            R("revenue", 23568, "usd_millions", "CEG FY2024 revenue"),
            R("earnings", 3750, "usd_millions", "CEG FY2024 GAAP net income"),
        ]),
        mk_period("2025-12-31", [
            R("revenue", 25530, "usd_millions", "CEG FY2025 revenue"),
            R("earnings", 2320, "usd_millions", "CEG FY2025 GAAP net income", limitation="GAAP net income swung materially year to year (loss in 2022, then $1.62B, $3.75B, $2.32B); utilities like CEG typically have GAAP earnings affected by mark-to-market hedging and nuclear decommissioning trust fund gains/losses, a plausible but not independently-verified explanation for this pattern."),
            R("cash", 3640, "usd_millions", "CEG cash, Dec 31 2025"),
            R("debt", 8900, "usd_millions", "CEG total debt (short-term $1.65B plus long-term $7.25B), Dec 31 2025"),
            D("net_debt", 5260, "usd_millions", "Derived: total debt $8.90B minus cash $3.64B equals ~$5.26B net debt.", "CEG balance sheet, Dec 31 2025"),
        ]),
    ],
    segment_abstain="Only a qualitative description of CEG's generation portfolio (nuclear, wind, solar, natural gas, hydroelectric) was found -- no quantitative FY2025 generation-mix or segment-operating-profit breakdown was located.",
    price=mk_price(269.54, "Aug 7 2026. Shares outstanding 357.10M includes 50M shares issued for the Calpine acquisition (closed Jan 7 2026) -- not directly comparable to the FY2025 weighted-average share count implicit in the EPS figures above. Market cap derived: 357.10M x $269.54 = ~$96.3B."),
    peers_data=[
        ("VST", "Vistra -- independent power producer with a large nuclear/gas fleet and similar AI-data-center power-demand exposure narrative."),
        ("NRG", "NRG Energy -- independent power producer, comparable business model (not individually fundamentals-checked this session; named on business-model similarity)."),
    ],
    scenarios_data=[
        ("Crane Clean Energy Center restart", "Three Mile Island Unit 1 restart, renamed the Crane Clean Energy Center, backed by a 20-year, 835MW power purchase agreement with Microsoft to supply mid-Atlantic AI data centers. Targeted online 2028; NRC licensing-basis review expected complete 2027."),
        ("Calpine acquisition", "Closed Jan 7 2026, total consideration ~$22B (50M newly issued CEG shares plus $4.5B cash; originally announced Jan 10 2025 at ~$16.4B equity value) -- materially expands CEG's generation fleet with Calpine's natural-gas and geothermal assets, not reflected in any FY2025 figure above."),
    ],
    uncertainty_summary=(
        "All figures secondary/search-aggregation-sourced; no primary document directly opened. CEG has "
        "only ~3 clean standalone fiscal years (2023-2025) plus a partial, non-comparable 2022 -- spun off "
        "from Exelon Feb 1 2022 -- disclosed as the shortened-history exception under VALUATION-0005 SS C.1 "
        "for a genuine structural (spin-off) limitation, not forced into a misleading 5-year comparison. "
        "GAAP net-income swings across years are disclosed as a real pattern with only a plausible, "
        "unverified explanation. No quantitative generation-mix/segment breakdown was found. The Calpine "
        "acquisition, closed Jan 2026, will materially reshape CEG's FY2026-forward financials and is not "
        "reflected in any figure above."
    ),
)

RECORDS["GEV"] = build(
    "GEV",
    periods=[
        mk_period("2025-12-31", [
            R("revenue", 38100, "usd_millions", "GEV FY2025 revenue, +9% YoY (GAAP and organic)"),
            R("earnings", 4900, "usd_millions", "GEV FY2025 net income (net margin 12.8%)", limitation="Inflated by a one-time $2.9B tax benefit from a US valuation-allowance release; underlying/normalized net income is materially lower, and no clean adjusted-net-income figure was found -- this figure should not be read as a clean operating result."),
            R("free_cash_flow", 3700, "usd_millions", "GEV FY2025 free cash flow"),
            R("cash", 8800, "usd_millions", "GEV cash balance, FY2025"),
        ]),
    ],
    segment_abstain="GEV's Power/Wind/Electrification segment revenue breakdown was not found this session -- a direct gap against the segment-evidence domain, disclosed rather than estimated. This research session's WebSearch budget was exhausted before this specific search could be run.",
    price_abstain="No reliable current stock price or market capitalization for GEV was found this session -- a genuine gap, not assumed or estimated.",
    peers_data=[
        ("ETN", "Eaton -- power-infrastructure/electrification peer by rough industry analogy (not independently verified via a fresh search for this specific pairing)."),
        ("PWR", "Quanta Services -- power-infrastructure/electrification peer by rough industry analogy (not independently verified via a fresh search for this specific pairing)."),
    ],
    scenarios_data=[
        ("Backlog growth and Prolec GE acquisition", "Backlog increased to $150B as of FY2025 year-end. GE Vernova's own Q4/FY2025 results press release references a Prolec GE acquisition in its headline ('increasing outlook with Prolec GE acquisition'), indicating a real, recent transaction affecting guidance -- deal size, structure, and close date were not found this session."),
    ],
    uncertainty_summary=(
        "All figures secondary/search-aggregation-sourced; no primary document directly opened. This is "
        "the weakest-covered record in this population pass: GE Vernova has existed as a standalone "
        "public company only since approximately April 2024 (spun off from General Electric) -- the exact "
        "spin-off date was not independently re-confirmed this session -- meaning at most ~1.5-2 completed "
        "fiscal years of clean standalone history exist, nowhere near the general 5-year target. This is "
        "the disclosed IPO/spin-off shortened-history exception under VALUATION-0005 SS C.1, applied for a "
        "genuine structural limitation. FY2024 standalone revenue/net-income/EPS were not found this "
        "session (a real gap, this research session's search budget was exhausted before it could be "
        "located) and are therefore also absent from this record -- only the single available FY2025 "
        "period is populated. Segment revenue, balance-sheet detail beyond cash, capex, D&A, diluted "
        "share count, and current stock price/market cap were all not found and are abstained rather than "
        "estimated."
    ),
)

# ============================================================
# Batch D -- shard 4: ETN, PWR, WM, GNRC, RTX
# ============================================================

RECORDS["ETN"] = build(
    "ETN",
    periods=[
        mk_period("2021-12-31", [R("revenue", 19630, "usd_millions", "ETN FY2021 revenue"), R("earnings", 2146, "usd_millions", "ETN FY2021 net income")]),
        mk_period("2022-12-31", [R("revenue", 20750, "usd_millions", "ETN FY2022 revenue"), R("earnings", 2465, "usd_millions", "ETN FY2022 net income")]),
        mk_period("2023-12-31", [R("revenue", 23200, "usd_millions", "ETN FY2023 revenue"), R("earnings", 3223, "usd_millions", "ETN FY2023 net income")]),
        mk_period("2024-12-31", [R("revenue", 24880, "usd_millions", "ETN FY2024 revenue"), R("earnings", 3798, "usd_millions", "ETN FY2024 net income")]),
        mk_period("2025-12-31", [
            R("revenue", 27450, "usd_millions", "ETN FY2025 revenue, record, +10% YoY"),
            R("earnings", 4087, "usd_millions", "ETN FY2025 net income"),
            abstain_item("operating_margin", "Only an unclear, unverified 'in the 21-23% range' snippet was found for FY2025 operating margin (unclear whether GAAP or adjusted, unclear period) -- not reliable enough to report as a fact."),
            R("free_cash_flow", 3600, "usd_millions", "ETN FY2025 free cash flow, record, +1% YoY"),
            R("cash", 803.0, "usd_millions", "ETN cash & short-term investments (recent)", limitation="An earlier snippet cited $398M cash + $186M short-term investments as of Jun 30 2025, a different (and smaller) figure at a different date -- not reconciled with this $803.0M figure; both disclosed."),
            R("debt", 10680, "usd_millions", "ETN total debt (date unclear, likely recent quarter)"),
            D("share_count_diluted", 391.1, "shares_millions", "Derived (approximate): FY2025 net income $4,087M divided by diluted EPS $10.45 equals ~391.1M diluted shares.", "ETN FY2025 net income and diluted EPS ($10.45 GAAP) figures"),
        ]),
    ],
    segment_abstain="Only Q4 2025 quarterly segment figures were located (Electrical Americas, Electrical Global, Aerospace, Vehicle, eMobility) -- a full-year segment revenue/operating-profit table was not retrieved despite multiple targeted searches, a genuine gap.",
    price=mk_price(452.67, "Aug 6 2026 (market cap ~$175.63B)."),
    peers_data=[
        ("EMR", "Emerson Electric -- industrial automation/electrification overlap, direct multiples comparison used by analysts."),
        ("ROK", "Rockwell Automation -- industrial/electrical automation peer."),
        ("VRT", "Vertiv -- direct data-center power-infrastructure overlap (also a fellow member of Portfolio-HQ's own power_infra correlated cluster)."),
    ],
    scenarios_data=[
        ("Data-center power demand surge", "Q4 2025 data-center orders reportedly surged ~200% YoY; electrical backlog +48% YoY in Q1 2026; total backlog grew from $2.8B (2019) to $15.3B (2025)."),
        ("Mobility segment spin-off", "Announced planned spin-off of the Mobility (vehicle electrical) business, targeted completion by end of Q1 2027."),
    ],
    uncertainty_summary=(
        "All figures secondary/search-aggregation-sourced (WebFetch blocked for every finance domain "
        "attempted); no primary document directly opened. FY2025 operating margin is abstained -- the "
        "only figure found was unclear as to basis and period. Two inconsistent cash figures at different "
        "dates were found and both disclosed rather than one silently chosen. Full-year segment detail "
        "was not obtained despite repeated attempts. Eaton is Ireland-domiciled ('Eaton Corp plc') and "
        "announced a planned Mobility spin-off targeted for completion by end of Q1 2027 -- a real future "
        "comparability event, not reflected in the history above."
    ),
)

RECORDS["PWR"] = build(
    "PWR",
    periods=[
        mk_period("2021-12-31", [R("revenue", 12980, "usd_millions", "PWR FY2021 revenue")]),
        mk_period("2022-12-31", [
            R("revenue", 17070, "usd_millions", "PWR FY2022 revenue"),
            R("earnings", 491.2, "usd_millions", "PWR FY2022 net income attributable to common"),
        ]),
        mk_period("2023-12-31", [R("revenue", 20880, "usd_millions", "PWR FY2023 revenue")]),
        mk_period("2024-12-31", [
            R("revenue", 23670, "usd_millions", "PWR FY2024 revenue"),
            R("earnings", 904.8, "usd_millions", "PWR FY2024 net income attributable to common"),
        ]),
        mk_period("2025-12-31", [
            R("revenue", 28480, "usd_millions", "PWR FY2025 revenue", limitation="PWR restructured its reportable segments starting Q1 2025, moving from three segments (Electric Power / Underground & Infrastructure / Pipeline) to two (Electric / Underground and Infrastructure) -- a structural change affecting segment comparability with pre-2025 data."),
            R("earnings", 1030, "usd_millions", "PWR FY2025 net income attributable to common", conflicts=[
                {"value": 6.80, "source_identifier": "PWR FY2025 GAAP diluted EPS, one source (press-release aggregation)", "source_type": "secondary", "access_status": "consulted_via_search_aggregation", "as_of_date": AS_OF, "note": "Two irreconcilable FY2025 diluted EPS figures were found ($6.80 vs $6.91); net income $1.03B is corroborated independently of either EPS figure."},
                {"value": 6.91, "source_identifier": "PWR FY2025 GAAP diluted EPS, a second source", "source_type": "secondary", "access_status": "consulted_via_search_aggregation", "as_of_date": AS_OF},
            ]),
            R("free_cash_flow", 1200, "usd_millions", "PWR FY2025 free cash flow"),
            R("capex", 500, "usd_millions", "PWR FY2025 net capital expenditures"),
            R("cash", 506.4, "usd_millions", "PWR cash, ~Q4 2025/early 2026"),
            R("debt", 6600, "usd_millions", "PWR total debt, ~Q4 2025/early 2026", limitation="A separate Q1 2026 snippet showed total debt of $5.89B, a different (later) data point -- both disclosed, not reconciled."),
        ]),
    ],
    segments=[
        segment("Electric", revenue=R("revenue", 23000, "usd_millions", "PWR FY2025 Electric segment revenue")),
    ],
    segment_abstain=None,
    shared_unallocated=None,
    price=mk_price(673.46, "Recent observation (~Aug 2026 context); market cap ~$100.41B."),
    peers_data=[
        ("MTZ", "MasTec -- direct infrastructure/electrical construction peer, similar end markets."),
        ("EME", "EMCOR Group -- electrical/mechanical construction services peer."),
        ("MYRG", "MYR Group -- smaller pure-play electrical/transmission construction peer."),
    ],
    scenarios_data=[
        ("Record backlog on electrification demand", "Year-end 2025 total backlog $43.98B, growing to ~$48.5B by Q1 2026, driven by grid modernization, utility transmission, and hyperscale data-center/large-load electrification demand. Electric segment year-end backlog alone was $36.2B (record)."),
    ],
    uncertainty_summary=(
        "All figures secondary/search-aggregation-sourced; no primary document directly opened. FY2025 "
        "diluted EPS carries a genuine, unresolved two-source conflict ($6.80 vs $6.91), disclosed rather "
        "than resolved; total debt has a similar unreconciled discrepancy across dates. PWR restructured "
        "its reportable segments in Q1 2025 (three segments to two) -- the FY2025 Underground and "
        "Infrastructure segment's full-year revenue was not found (only a Q3 2025 quarterly figure), so "
        "only the Electric segment is populated in segment_evidence above; this is a partial, disclosed "
        "gap, not a full domain abstention, since at least one genuine segment figure is available."
    ),
)

RECORDS["WM"] = build(
    "WM",
    periods=[
        mk_period("2021-12-31", [R("revenue", 17930, "usd_millions", "WM FY2021 revenue")]),
        mk_period("2022-12-31", [
            R("revenue", 19700, "usd_millions", "WM FY2022 revenue"),
            R("earnings", 2238, "usd_millions", "WM FY2022 net income"),
        ]),
        mk_period("2023-12-31", [
            R("revenue", 20430, "usd_millions", "WM FY2023 revenue"),
            R("earnings", 2304, "usd_millions", "WM FY2023 net income"),
        ]),
        mk_period("2024-12-31", [
            R("revenue", 22060, "usd_millions", "WM FY2024 revenue"),
            R("earnings", 2746, "usd_millions", "WM FY2024 net income"),
        ]),
        mk_period("2025-12-31", [
            R("revenue", 25200, "usd_millions", "WM FY2025 revenue", limitation="WM acquired Stericycle (announced Jun 2024, closed Nov 2024, ~$7.2B enterprise value including ~$1.4B assumed net debt) -- FY2025 is the first full year including it (via the new WM Healthcare Solutions segment); FY2024 and earlier do not include it or only partially do."),
            R("earnings", 2710, "usd_millions", "WM FY2025 net income", limitation="Lower than FY2024's $2,746M despite higher revenue and operating income -- plausibly reflecting Stericycle-acquisition-financing interest expense/integration costs, but the specific mechanism was not independently verified this session."),
            R("operating_margin", 0.171, "ratio", "WM FY2025 operating margin (derived from reported operating income $4.31B / revenue $25.20B = 17.1%; reported operating income figure itself sourced directly)"),
            R("free_cash_flow", 2940, "usd_millions", "WM FY2025 free cash flow, +26.8% YoY"),
            R("capex", 2600, "usd_millions", "WM FY2025 capital expenditures", limitation="A separately-cited $633M 'sustainability growth' investment figure was found; unclear if included in or additive to this $2.6B figure -- not reconciled."),
            R("cash", 440, "usd_millions", "WM cash, Jun 30 2025", limitation="This is a mid-year figure, several months stale relative to a fiscal-year-end balance; the more current figure was not found."),
            R("debt", 23800, "usd_millions", "WM total debt (Q1 2025 10-Q cited $23.84B; a Q3 2025 snippet cited long-term debt alone of $22.482B) -- materially elevated post-Stericycle acquisition financing, consistent across sources."),
            D("share_count_diluted", 404.5, "shares_millions", "Derived (approximate): FY2025 net income $2,710M divided by diluted EPS $6.70 equals ~404.5M diluted shares.", "WM FY2025 net income and diluted EPS figures", ),
        ]),
    ],
    segment_abstain="Only partial/quarterly segment data were found this session: Collection & Disposal margin was quarterly-only (Q2 2025: 37.9%), Recycling Processing & Sales/WM Renewable Energy growth was qualitative only ('double-digit' EBITDA growth, no dollar figure), and the new WM Healthcare Solutions segment (from Stericycle) had only a Q2 2025 quarterly revenue figure ($646M) -- a full-year FY2025 segment revenue/operating-income table was not located.",
    price=mk_price(230.54, "Recent observation (~Aug 2026 context); market cap ~$91.01B; 52-week range $194.11-$248.13."),
    peers_data=[
        ("RSG", "Republic Services -- closest direct comparable, #2 US waste company."),
        ("GFL", "GFL Environmental -- comparable North American waste/recycling operator (not separately searched this session, named from general market knowledge; treat as unverified for current-session figures)."),
        ("WCN", "Waste Connections -- comparable large-cap solid-waste peer (not separately searched this session; same caveat as GFL)."),
    ],
    scenarios_data=[
        ("Stericycle integration", "Full realization of medical-waste/healthcare-solutions commercial and cost synergies remains an ongoing, disclosed integration story into 2026."),
        ("PFAS regulatory exposure", "EPA is actively developing PFAS destruction/disposal guidance and potential Superfund-related cost exposure for landfill operators including WM -- a real, disclosed regulatory risk, though no WM-specific dollar figure was found this session."),
    ],
    uncertainty_summary=(
        "All figures secondary/search-aggregation-sourced; no primary document directly opened. WM's "
        "Nov 2024 Stericycle acquisition (~$7.2B EV) is the dominant comparability event in this record -- "
        "FY2025 is the first full year including it, while FY2024 and earlier largely predate it. "
        "Full-year segment revenue/operating-income detail is a genuine, disclosed gap (only quarterly "
        "figures were found for each segment). Balance-sheet cash is several months stale relative to any "
        "fiscal-year-end figure. FY2025 net income being lower than FY2024's despite higher revenue and "
        "operating income is disclosed as a real pattern without a fully verified explanation."
    ),
)

RECORDS["GNRC"] = build(
    "GNRC",
    periods=[
        mk_period("2021-12-31", [
            R("revenue", 3740, "usd_millions", "GNRC FY2021 revenue"),
            abstain_item("earnings", "The only FY2021 diluted EPS figure found (~$8.23) was itself derived by a search aggregator working backward from a cited '-34.7% decline to 2022' statistic, not independently confirmed -- not reported as fact."),
        ]),
        mk_period("2022-12-31", [
            R("revenue", 4560, "usd_millions", "GNRC FY2022 revenue"),
        ]),
        mk_period("2023-12-31", [
            R("revenue", 4020, "usd_millions", "GNRC FY2023 revenue"),
        ]),
        mk_period("2024-12-31", [
            R("revenue", 4300, "usd_millions", "GNRC FY2024 revenue"),
        ]),
        mk_period("2025-12-31", [
            R("revenue", 4210, "usd_millions", "GNRC FY2025 revenue, -2% YoY", limitation="Decline attributed (per company commentary in search results) to weaker residential/home-standby generator demand following a lower-outage environment vs. a strong hurricane-driven 2024 comparison -- a real, disclosed demand-cyclicality factor for this business."),
            R("earnings", 160, "usd_millions", "GNRC FY2025 GAAP net income (adjusted non-GAAP net income separately reported at $376M)"),
            D("operating_margin", 0.110, "ratio", "Derived: FY2025 operating income $465.04M divided by revenue $4,210M equals 11.0 percent.", "GNRC FY2025 operating income $465.04M"),
            R("free_cash_flow", 268.13, "usd_millions", "GNRC trailing-twelve-month free cash flow (basis/period ambiguous, may not equal clean FY2025)", limitation="A separate, more recent snippet cited $331M FCF for the trailing-twelve-months through March 2026 -- these don't fully reconcile, likely reflecting different trailing windows rather than a contradiction, but the exact FY2025-standalone figure could not be confirmed."),
            R("capex", 169.85, "usd_millions", "GNRC trailing-twelve-month capital expenditures", limitation="FY2024 capex was separately cited at $137M, a different period, not reconciled."),
            R("cash", 341.4, "usd_millions", "GNRC cash (recent)"),
            R("debt", 1200, "usd_millions", "GNRC total debt (recent; a range of $1.2-1.38B was found across sources)"),
            D("share_count_diluted", 59.5, "shares_millions", "Derived (approximate): FY2025 net income $160M divided by diluted EPS $2.69 equals ~59.5M diluted shares.", "GNRC FY2025 net income and diluted EPS figures"),
        ]),
    ],
    segment_abstain="The only segment figures found ('Domestic revenue $1.07B +20% YoY, International revenue $187.5M -1% YoY') appear to be a single quarter's results mislabeled as full-year -- $1.07B + $187.5M is far short of the $4.21B FY2025 total. Flagged as likely bad/mislabeled data and not used, rather than reported as fact.",
    price=mk_price(202.01, "Recent observation (~Aug 2026 context); market cap ~$11.89B; 52-week range $134.80-$296.44, a wide range consistent with 2025's demand-driven volatility."),
    peers_data=[
        ("CMI", "Cummins -- engine/power-generation equipment maker, partial overlap in stationary/standby power (much larger scale)."),
        ("CAT", "Caterpillar -- has a power-generation/electric-power division; broader industrial equipment peer, weaker pure-play match given its vastly larger scale."),
    ],
    scenarios_data=[
        ("Hyperscale data-center backup power deal", "Generac announced (Jun 2026) a global supply agreement with a major/unnamed hyperscale data-center operator to supply backup power generators -- a real, disclosed new demand vector distinct from its traditional residential/storm-driven business. Also raised 2026 net sales growth guidance to 'mid-to-high teens %' from a prior 'mid-teens' guidance, partly citing data-center/C&I demand."),
    ],
    uncertainty_summary=(
        "All figures secondary/search-aggregation-sourced; no primary document directly opened. FY2021 "
        "diluted EPS is abstained as an unreliable, aggregator-derived figure. FY2025 free cash flow and "
        "capex are trailing-twelve-month figures with an ambiguous exact period basis, not confirmed as "
        "clean FY2025-standalone numbers, disclosed as such. Segment revenue is abstained entirely -- the "
        "only figures found appear to be a mislabeled single quarter, not a genuine full-year breakdown, "
        "and using them would risk presenting bad data as fact. Note that Briggs & Stratton, a candidate "
        "peer named in the original research brief, is not a current public comparable (acquired by KPS "
        "Capital Partners and delisted) and is correctly excluded from the peer list above."
    ),
)

RECORDS["RTX"] = build(
    "RTX",
    periods=[
        mk_period("2021-12-31", [
            abstain_item("revenue", "FY2021 revenue was not found this session; only net income was located for this year."),
            R("earnings", 3864, "usd_millions", "RTX FY2021 net income", limitation="RTX was formed by the April 2020 merger of Raytheon Company and United Technologies Corp; FY2020 itself was a net-loss year (-$3,519M, reflecting merger/integration costs and pandemic-era aerospace demand collapse) and is a poor comparison-year baseline. Pre-2020 standalone 'Raytheon' or 'UTC' historical financials are not directly comparable to post-merger RTX consolidated financials."),
        ]),
        mk_period("2022-12-31", [R("earnings", 5197, "usd_millions", "RTX FY2022 net income")]),
        mk_period("2023-12-31", [
            R("revenue", 68920, "usd_millions", "RTX FY2023 revenue"),
            R("earnings", 3195, "usd_millions", "RTX FY2023 net income"),
        ]),
        mk_period("2024-12-31", [
            R("revenue", 80740, "usd_millions", "RTX FY2024 revenue"),
            R("earnings", 4774, "usd_millions", "RTX FY2024 net income"),
        ]),
        mk_period("2025-12-31", [
            R("revenue", 88600, "usd_millions", "RTX FY2025 revenue, +9.8-10% YoY, +11% organic"),
            R("earnings", 6732, "usd_millions", "RTX FY2025 net income, +41% YoY"),
            D("operating_margin", 0.105, "ratio", "Derived: FY2025 operating income $9.3B divided by revenue $88.60B equals 10.5 percent (matches company-reported margin).", "RTX FY2025 operating income $9.3B"),
            R("free_cash_flow", 8460, "usd_millions", "RTX trailing-twelve-month (through ~early 2026) free cash flow -- closest available proxy for FY2025, not confirmed as an exact calendar-year figure"),
            R("capex", 2660, "usd_millions", "RTX trailing-twelve-month capital expenditures"),
            R("cash", 6820, "usd_millions", "RTX cash (~Q4 2025/early 2026)"),
            R("debt", 38940, "usd_millions", "RTX total debt (~Q4 2025/early 2026)"),
            D("net_debt", 32120, "usd_millions", "Derived: total debt $38.94B minus cash $6.82B equals ~$32.12B net debt.", "RTX balance sheet figures above"),
            D("share_count_diluted", 1357, "shares_millions", "Derived (approximate): FY2025 net income $6,732M divided by diluted EPS $4.96 (GAAP) equals ~1,357M diluted shares.", "RTX FY2025 net income and diluted EPS figures"),
        ]),
    ],
    segments=[
        segment("Collins Aerospace", revenue=R("revenue", 30200, "usd_millions", "RTX FY2025 Collins Aerospace segment sales"), profit=R("earnings", 1402, "usd_millions", "RTX FY2025 Collins Aerospace GAAP operating profit (+27% YoY; adjusted figure separately cited at $1,223M, +1% YoY)", limitation="The implied operating margin (~4-5% of segment revenue) is anomalously low for an aerospace supplier and may reflect heavy acquisition-amortization/restructuring drag specific to GAAP reporting, or an aggregation/parsing error in the underlying search snippet -- this figure is reported with lower confidence than the segment's revenue figure.")),
        segment("Pratt & Whitney", revenue=R("revenue", 32920, "usd_millions", "RTX FY2025 Pratt & Whitney segment sales"), profit=R("earnings", 776, "usd_millions", "RTX FY2025 Pratt & Whitney adjusted (non-GAAP) operating profit, +8% YoY (GAAP figure not found)")),
        segment("Raytheon", revenue=R("revenue", 28040, "usd_millions", "RTX FY2025 Raytheon segment sales")),
    ],
    price=mk_price(223.03, "Recent observation (~Aug 2026 context); market cap ~$300.89B."),
    peers_data=[
        ("LMT", "Lockheed Martin -- direct defense-sector peer (Raytheon segment overlap)."),
        ("GE", "GE Aerospace -- direct commercial-engine peer (Pratt & Whitney overlap), larger market cap than RTX."),
        ("SAF", "Safran (Paris-listed, EUR) -- direct commercial-engine/aerostructures peer (Pratt & Whitney/Collins overlap), international comparable."),
    ],
    scenarios_data=[
        ("Pratt & Whitney GTF powder-metal engine issue", "A 2023-disclosed contamination issue in powder metal used for certain PW1100 GTF engine parts (powers the A320neo family) triggered an accelerated inspection/removal campaign. RTX took a ~$3B pre-tax charge in Q3 2023, with total projected gross costs of $6-7B over several years. As of late October 2025, the global count of stored/grounded GTF-powered aircraft reportedly reached 835 (up from 748 mid-2025); Q1 2026 saw a reported 15% decline in groundings as maintenance capacity ramped. Some analyst commentary projects full fleet recovery not until 2027 or later -- this remains an active, material, ongoing operational and cash-flow issue for Pratt & Whitney specifically."),
    ],
    uncertainty_summary=(
        "All figures secondary/search-aggregation-sourced; no primary document directly opened. RTX was "
        "formed by the April 2020 Raytheon-UTC merger and renamed from Raytheon Technologies to RTX "
        "Corporation in July 2023 -- FY2021/FY2022 revenue was not found and only net income is reported "
        "for those years; FY2020 (a net-loss merger/integration year) and any pre-merger standalone "
        "Raytheon/UTC data are excluded entirely as not comparable. The large GAAP-vs-adjusted-EPS gap "
        "each period is a direct, disclosed consequence of merger purchase-accounting amortization, not an "
        "anomaly. Collins Aerospace's segment operating-profit figure carries a specific, disclosed "
        "low-confidence flag (anomalously low implied margin, possibly a parsing error)."
    ),
)

# ============================================================
# Batch E -- shard 5 (partial): ICE, V, SPGI, TMO
# ============================================================

RECORDS["ICE"] = build(
    "ICE",
    periods=[
        mk_period("2021-12-31", [
            R("revenue", 7146, "usd_millions", "ICE FY2021 net revenue (ICE's own headline metric, net of transaction-based expenses)"),
            R("earnings", 4100, "usd_millions", "ICE FY2021 net income attributable to ICE", limitation="Inflated by a large one-time gain from the Coinbase divestment/Bakkt deconsolidation, disclosed in the underlying source commentary explaining the 2021-to-2022 net income collapse."),
        ]),
        mk_period("2022-12-31", [
            R("revenue", 7292, "usd_millions", "ICE FY2022 net revenue"),
            R("earnings", 1400, "usd_millions", "ICE FY2022 net income attributable to ICE", limitation="Sharp decline from 2021 explained in source commentary by net losses from Bakkt in 2022 plus the absence of 2021's one-time gain."),
        ]),
        mk_period("2023-12-31", [
            R("revenue", 7988, "usd_millions", "ICE FY2023 net revenue"),
            R("earnings", 2400, "usd_millions", "ICE FY2023 net income attributable to ICE"),
        ]),
        mk_period("2024-12-31", [
            R("revenue", 9279, "usd_millions", "ICE FY2024 net revenue", limitation="A separate aggregator (macrotrends) showed '2025 revenue $12.64B,' very likely gross revenue before transaction-based expenses rather than ICE's own headlined net-revenue convention -- not reconciled, net revenue used consistently here per ICE's own convention."),
            R("earnings", 2800, "usd_millions", "ICE FY2024 net income attributable to ICE"),
            R("operating_margin", 0.46, "ratio", "ICE FY2024 GAAP operating margin (GAAP operating income $4.3B; adjusted operating margin separately reported at 59%, adjusted operating income $5.5B)"),
        ]),
        mk_period("2025-12-31", [
            R("revenue", 9930, "usd_millions", "ICE FY2025 net revenue"),
            R("earnings", 3300, "usd_millions", "ICE FY2025 net income attributable to ICE"),
            R("operating_margin", 0.50, "ratio", "ICE FY2025 GAAP operating margin (GAAP operating income $4.9B; adjusted operating margin separately reported at 60%, adjusted operating income $6.0B)"),
            R("free_cash_flow", 4200, "usd_millions", "ICE FY2025 'adjusted free cash flow' (company's own non-GAAP figure)", limitation="A simple operating-cash-flow-minus-capex calculation ($4.7B - $791M = $3.9B) does not match this $4.2B 'adjusted' figure; ICE's own adjusted-FCF methodology differs from a plain subtraction and the reconciliation was not found."),
            R("capex", 791, "usd_millions", "ICE FY2025 capital expenditures"),
            R("cash", 850, "usd_millions", "ICE cash & short-term investments, Dec 31 2025"),
            R("debt", 19000, "usd_millions", "ICE total debt, Dec 31 2025"),
            D("net_debt", 18150, "usd_millions", "Derived: total debt $19.0B minus cash & short-term investments $850M equals ~$18.15B net debt.", "ICE balance sheet, Dec 31 2025"),
            D("share_count_diluted", 572, "shares_millions", "Derived (approximate): FY2025 net income $3,300M divided by diluted EPS $5.77 equals ~572M diluted shares.", "ICE FY2025 net income and diluted EPS figures"),
            R("total_equity", 28700, "usd_millions", "ICE shareholder equity, Dec 31 2025"),
        ]),
    ],
    segments=[
        segment("Exchanges", revenue=R("revenue", 5000, "usd_millions", "ICE FY2024 Exchanges segment revenue, +12% YoY")),
        segment("Fixed Income & Data Services", revenue=R("revenue", 2300, "usd_millions", "ICE FY2024 Fixed Income & Data Services segment revenue")),
        segment("Mortgage Technology", revenue=R("revenue", 2000, "usd_millions", "ICE FY2024 Mortgage Technology segment revenue"), profit=R("earnings", -170, "usd_millions", "ICE FY2024 Mortgage Technology segment operating loss (-8% margin); adjusted operating income separately reported at $724M, 36% adjusted margin", limitation="This segment table is for FY2024, the most recent full breakdown found -- a FY2025 segment split was not located.")),
    ],
    price=mk_price(149.84, "Aug 5 2026. A market cap figure of $89.14B was dated March 2026 (stale); a derived current estimate at this price x ~572M shares is ~$85.7B (derived, low confidence)."),
    peers_data=[
        ("CME", "CME Group -- largest US derivatives/futures exchange operator."),
        ("NDAQ", "Nasdaq Inc -- exchange plus market-data/technology hybrid business model."),
        ("CBOE", "Cboe Global Markets -- options/equities exchange operator."),
    ],
    scenarios_data=[
        ("Pending MarketAxess acquisition", "Announced ~Jul 30 2026, $167/share, $5.7B enterprise value, unanimous board approval on both sides, expected close H1 2027 pending shareholder/regulatory approval."),
        ("Black Knight acquisition", "Completed September 2023, $13.1B deal value, forms the core of the ICE Mortgage Technology segment alongside prior Ellie Mae (2020), Simplifile (2019), and MERS (2018) deals -- a major restructuring event limiting clean pre/post comparability for that segment."),
    ],
    uncertainty_summary=(
        "All figures secondary/search-aggregation-sourced; no primary document directly opened. ICE's own "
        "net-revenue convention (net of transaction-based expenses) is used consistently for the revenue "
        "trend above; a separate gross-revenue figure found for 2025 was not reconciled and is disclosed, "
        "not used. FY2025 segment revenue was not located (only FY2024's), so segment_evidence reflects "
        "FY2024 with that limitation disclosed. ICE's own 'adjusted free cash flow' methodology does not "
        "reconcile to a simple OCF-minus-capex calculation and the gap is disclosed rather than resolved. "
        "Current market capitalization is a low-confidence derived estimate, since the only directly "
        "reported figure found was several months stale."
    ),
)

RECORDS["V"] = build(
    "V",
    periods=[
        mk_period("2021-09-30", [
            D("revenue", 24110, "usd_millions", "Derived (low confidence): reverse-engineered from later years' stated growth-rate percentages, not a directly reported figure.", "V FY2022-FY2024 stated YoY revenue growth percentages"),
            D("earnings", 12310, "usd_millions", "Derived (low confidence): reverse-engineered from later years' stated growth-rate percentages, not a directly reported figure.", "V FY2022-FY2024 stated YoY net-income growth percentages"),
        ]),
        mk_period("2022-09-30", [
            R("revenue", 29310, "usd_millions", "V FY2022 (ended Sept 30 2022) revenue"),
            R("earnings", 14957, "usd_millions", "V FY2022 net income"),
        ]),
        mk_period("2023-09-30", [
            R("revenue", 32653, "usd_millions", "V FY2023 revenue"),
            R("earnings", 17273, "usd_millions", "V FY2023 net income"),
        ]),
        mk_period("2024-09-30", [
            R("revenue", 35926, "usd_millions", "V FY2024 revenue"),
            R("earnings", 19743, "usd_millions", "V FY2024 net income"),
        ]),
        mk_period("2025-09-30", [
            abstain_item("revenue", "One search pass returned FY2025 total revenue of '$43.03B, +11%,' but this is internally inconsistent with the FY2024 base ($35.926B x 1.11 = $39.9B, not $43.03B). A separate pass gave only Q4 FY2025 net revenue ($10.7B, +12% YoY), directionally consistent with a high-$30Bs/low-$40Bs full year but not an exact, internally-consistent figure. Not reported as fact."),
            R("earnings", 20100, "usd_millions", "V FY2025 GAAP net income", limitation="An initial search synthesis claimed FY2025 net income of $22.03B (EPS $11.22), which is internally consistent with no other figure found and was contradicted by a follow-up search giving $20.1B (EPS $10.20); the $20.1B/$10.20 pair is internally consistent (implies ~1.97B diluted shares, a sane figure) and was used, with the $22.03B figure explicitly treated as a likely AI-search-synthesis error and rejected."),
            R("free_cash_flow", 21580, "usd_millions", "V FY2025 free cash flow", limitation="A derived cross-check (OCF $23,059M minus capex $970M = $22,090M) does not exactly match this reported $21,580M figure; a small, unexplained gap."),
            R("capex", 970, "usd_millions", "V FY2025 capital expenditures"),
            D("cash", 19600, "usd_millions", "Derived: cash & equivalents $17.2B plus available-for-sale debt securities $2.4B equals ~$19.6B.", "V balance sheet, Sept 30 2025"),
            D("share_count_diluted", 1970, "shares_millions", "Derived (approximate): FY2025 net income $20,100M divided by diluted EPS $10.20 equals ~1,970M diluted shares.", "V FY2025 net income and diluted EPS figures"),
        ]),
    ],
    segment_abstain="Visa's segment structure was not independently verified via search this session (Visa has historically reported as a single operating/reportable segment per general market knowledge, but this was not confirmed by a search result gathered this session and is therefore not asserted as sourced fact).",
    price=mk_price(362.50, "Aug 7 2026; market cap $676.8B, same date."),
    peers_data=[
        ("MA", "Mastercard -- near-identical four-party payment-network model, direct scale comparable."),
        ("AXP", "American Express -- closed-loop three-party payment-network model, a useful structural contrast case."),
        ("PYPL", "PayPal -- platform/digital-wallet competitor, structurally different but frequently compared."),
    ],
    scenarios_data=[
        ("Visa Stablecoin Platform launch", "Launched July 2026 (Open USD/OUSD); stablecoin settlement pilot expanded to 9 blockchains, ~$7B annualized settlement run rate (+50% quarter-over-quarter); Aug 5 2026 rollout of stablecoin settlement across Visa Direct (18B+ endpoints, 195 countries)."),
        ("DOJ debit-network litigation", "DOJ debit-network monopolization lawsuit filed Sept 2024, ongoing; a separate new 2026 merchant class-action (Southern District of NY) challenges the scope of a prior 2019 interchange-fee settlement's legal-immunity protection."),
    ],
    uncertainty_summary=(
        "All figures secondary/search-aggregation-sourced; no primary document directly opened. FY2021 "
        "revenue and net income are low-confidence derived estimates, reverse-engineered from later "
        "years' stated growth rates rather than directly reported. FY2025 revenue is abstained entirely -- "
        "the only figure found was internally inconsistent with the prior-year base and not reported as "
        "fact. FY2025 net income required catching and rejecting an apparent AI-search-synthesis "
        "fabrication ($22.03B/EPS $11.22) in favor of an internally-consistent, corroborated figure "
        "($20.1B/EPS $10.20) -- a concrete instance of the verify-before-trusting-an-external-inference "
        "discipline this repository's own guardrails require. Segment structure is not asserted since it "
        "was not independently confirmed by search this session."
    ),
)

RECORDS["SPGI"] = build(
    "SPGI",
    periods=[
        mk_period("2021-12-31", [
            R("revenue", 8300, "usd_millions", "SPGI FY2021 revenue"),
            D("earnings", 3020, "usd_millions", "Derived (approximate): reverse-engineered from later years' stated figures/context, not a directly reported number.", "SPGI FY2021 context surrounding the 2022 IHS Markit merger"),
        ]),
        mk_period("2022-12-31", [
            R("revenue", 11181, "usd_millions", "SPGI FY2022 revenue", limitation="The FY2021-to-FY2022 revenue jump (+35%) is almost entirely attributable to the Feb 28 2022 IHS Markit all-stock merger (~$43.5B consideration, 113.8M new shares issued), not organic growth -- a major comparability break."),
            R("earnings", 3248, "usd_millions", "SPGI FY2022 net income"),
        ]),
        mk_period("2023-12-31", [
            R("revenue", 12497, "usd_millions", "SPGI FY2023 revenue"),
            R("earnings", 2626, "usd_millions", "SPGI FY2023 net income, -19.15% YoY"),
        ]),
        mk_period("2024-12-31", [
            R("revenue", 14208, "usd_millions", "SPGI FY2024 revenue"),
            R("earnings", 3852, "usd_millions", "SPGI FY2024 net income, +46.69% YoY"),
        ]),
        mk_period("2025-12-31", [
            R("revenue", 15336, "usd_millions", "SPGI FY2025 revenue"),
            R("earnings", 4471, "usd_millions", "SPGI FY2025 net income, +16% YoY"),
            R("free_cash_flow", 5560, "usd_millions", "SPGI trailing-twelve-month free cash flow (basis/period ambiguous, may not equal clean FY2025); company's own FY2025 FCF guidance range was $5.4-5.6B operating-based / $5.6-5.8B adjusted"),
            R("cash", 1810, "usd_millions", "SPGI cash (recent)"),
            R("debt", 13900, "usd_millions", "SPGI total debt (recent)"),
            D("net_debt", 12090, "usd_millions", "Derived: total debt $13.90B minus cash $1.81B equals ~$12.09B net debt.", "SPGI balance sheet figures above"),
            D("share_count_diluted", 305, "shares_millions", "Derived (approximate): FY2025 net income $4,471M divided by diluted EPS $14.66 (GAAP) equals ~305M diluted shares.", "SPGI FY2025 net income and diluted EPS figures"),
        ]),
    ],
    segments=[
        segment("Market Intelligence", revenue=R("revenue", 4920, "usd_millions", "SPGI FY2025 Market Intelligence segment revenue")),
        segment("Ratings", revenue=R("revenue", 4720, "usd_millions", "SPGI FY2025 Ratings segment revenue")),
        segment("Mobility", revenue=R("revenue", 1750, "usd_millions", "SPGI FY2025 Mobility segment revenue", limitation="The Mobility segment was spun off as Mobility Global Inc. (NYSE: MBGL) effective Jul 1 2026, removing it from SPGI's go-forward segment structure -- not reflected in this FY2025 figure.")),
        segment("Indices", revenue=R("revenue", 1850, "usd_millions", "SPGI FY2025 Indices segment revenue")),
    ],
    price=mk_price(405.24, "Aug 6 2026; market cap reported as both $123.96B (Jul 2026) and $122.7B (a second source), minor variance."),
    peers_data=[
        ("MCO", "Moody's Corporation -- closest direct peer, core credit-ratings overlap."),
        ("MSCI", "MSCI Inc -- index/ESG-data overlap with SPGI's Indices segment."),
        ("CME", "CME Group -- was SPGI's 50/50 OSTTRA joint-venture partner (now divested), an adjacent market-data/derivatives-infrastructure business."),
    ],
    scenarios_data=[
        ("Mobility Global spin-off", "Completed Jul 1 2026; 1:1 pro-rata share distribution to holders of record Jun 15 2026; now trades independently on NYSE as MBGL, removing the Mobility segment from SPGI going forward."),
        ("OSTTRA joint-venture divestiture", "The CME/SPGI 50-50 post-trade joint venture was sold to KKR-managed funds for $3.1B total enterprise value, split evenly between the two parents, completed 2026."),
    ],
    uncertainty_summary=(
        "All figures secondary/search-aggregation-sourced; no primary document directly opened. FY2021 "
        "net income is a low-confidence derived estimate. Operating income/margin was not found as a "
        "clean dollar figure for any year despite qualitative commentary ('operating margin grew... driven "
        "by revenue growth across all five divisions') and is omitted rather than estimated. Segment "
        "figures mix full-year (revenue, where found) and margin-only H1-2025 detail in the underlying "
        "research -- only full-year revenue is reported in segment_evidence above (Commodity Insights "
        "full-year revenue was not found and is therefore not included as a fifth segment entry). The Feb "
        "2022 IHS Markit merger (~$43.5B all-stock) is the dominant structural discontinuity in this "
        "5-year history -- FY2021-to-FY2022 revenue and share-count changes are merger-driven, not organic."
    ),
)

RECORDS["TMO"] = build(
    "TMO",
    periods=[
        mk_period("2021-12-31", [
            R("revenue", 39210, "usd_millions", "TMO FY2021 revenue, +22% YoY, including $2.45B of COVID-testing-related response revenue"),
            R("earnings", 7730, "usd_millions", "TMO FY2021 net income"),
        ]),
        mk_period("2022-12-31", [
            R("revenue", 44915, "usd_millions", "TMO FY2022 revenue, +14.55% YoY"),
            R("earnings", 6950, "usd_millions", "TMO FY2022 net income, -10.03% YoY"),
        ]),
        mk_period("2023-12-31", [
            R("revenue", 42857, "usd_millions", "TMO FY2023 revenue, -4.58% YoY (COVID-testing revenue fading)"),
            R("earnings", 5995, "usd_millions", "TMO FY2023 net income, -13.74% YoY"),
        ]),
        mk_period("2024-12-31", [
            R("revenue", 42879, "usd_millions", "TMO FY2024 revenue, +0.05% YoY, essentially flat"),
            R("earnings", 6335, "usd_millions", "TMO FY2024 net income, +5.67% YoY"),
        ]),
        mk_period("2025-12-31", [
            R("revenue", 44560, "usd_millions", "TMO FY2025 revenue, +4% YoY"),
            R("earnings", 6704, "usd_millions", "TMO FY2025 net income"),
            D("operating_margin", 0.174, "ratio", "Derived: FY2025 GAAP operating income $7.75B divided by revenue $44.56B equals 17.4 percent (adjusted operating margin separately reported at 22.7%, adjusted operating income $10.11B).", "TMO FY2025 GAAP operating income $7.75B"),
            R("free_cash_flow", 6340, "usd_millions", "TMO FY2025 free cash flow (stated directly as operating cash flow minus capex, internally consistent)"),
            R("capex", 1480, "usd_millions", "TMO FY2025 net capital expenditures"),
            R("cash", 9879, "usd_millions", "TMO cash & equivalents, year-end 2025"),
            R("debt", 39380, "usd_millions", "TMO total debt, year-end 2025"),
            D("net_debt", 29500, "usd_millions", "Derived: total debt $39.38B minus cash $9.879B equals ~$29.5B net debt.", "TMO balance sheet, year-end 2025"),
            R("share_count_diluted", 371.484244, "shares_millions", "TMO diluted shares outstanding (precise secondary-sourced figure, treat with some caution given source type)"),
        ]),
    ],
    segments=[
        segment("Life Sciences Solutions", revenue=R("revenue", 4840, "usd_millions", "TMO H1 2025 Life Sciences Solutions segment revenue", limitation="This is a half-year (H1 2025), not full fiscal-year, figure -- a full FY2025 segment table was not located.")),
        segment("Analytical Instruments", revenue=R("revenue", 5339, "usd_millions", "TMO 9-months-2025 Analytical Instruments segment revenue", limitation="This is a 9-month, not full fiscal-year, figure."), profit=R("earnings", 1153, "usd_millions", "TMO 9-months-2025 Analytical Instruments segment income", limitation="This is a 9-month, not full fiscal-year, figure.")),
        segment("Specialty Diagnostics", revenue=R("revenue", 2282, "usd_millions", "TMO H1 2025 Specialty Diagnostics segment revenue", limitation="This is a half-year, not full fiscal-year, figure.")),
        segment("Laboratory Products and Biopharma Services", revenue=R("revenue", 11635, "usd_millions", "TMO H1 2025 'Laboratory Products and Biopharma Services' segment revenue", limitation="This is a half-year, not full fiscal-year, figure. Note this segment name appears recently renamed from the prior 'Laboratory Products and Services' -- plausibly tied to the Solventum/Clario integration below; not independently confirmed.")),
    ],
    price=mk_price(579.00, "Aug 6 2026; market cap ~$215.89B (date basis for this figure unclear, approximate)."),
    peers_data=[
        ("DHR", "Danaher Corporation -- closest-scale life-sciences/diagnostics conglomerate."),
        ("A", "Agilent Technologies -- analytical instruments overlap."),
        ("WAT", "Waters Corporation -- liquid chromatography/analytical instruments overlap."),
    ],
    scenarios_data=[
        ("Clario acquisition", "Clinical-trial imaging/eCOA technology acquisition completed Q2 2026; deal value cited inconsistently across sources ('$8.9B' at a 'late March' close vs. '$9.1B' in Q2 2026 context) -- possibly enterprise value vs. equity value, or a revised figure, not reconciled."),
        ("Solventum and microbiology portfolio changes", "Acquired Solventum's Purification & Filtration business for ~$4.0B cash, completed 2025 (the acquired business generated ~$1B revenue in 2024). Separately, TMO is divesting its microbiology business for ~$1.075B, expected to close Q3 2026, expected to reduce 2026 revenue by ~$200M (net of a retained channel business) and 2026 adjusted EPS by $0.05."),
    ],
    uncertainty_summary=(
        "All figures secondary/search-aggregation-sourced; no primary document directly opened. The "
        "2021-peak-to-2023-trough revenue pattern reflects COVID-testing revenue fading, a real and "
        "disclosed pattern, not an error -- multi-year comparisons should account for it rather than "
        "treating it as a clean organic trend. Full-year FY2025 segment revenue was not found -- only "
        "partial-year (H1 or 9-month) figures were located for each segment and are disclosed as such "
        "in segment_evidence above rather than presented as full-year data. Three real M&A/divestiture "
        "events fall inside the last 12 months of this record (Solventum acquisition, Clario acquisition, "
        "microbiology divestiture), making segment and total-revenue trends genuinely hard to compare "
        "cleanly year over year without further adjustment."
    ),
)

# ============================================================
# Batch F -- supplemental shards 6/7: AMZN, AVGO, COST, TSLA, RKLB
# ============================================================

RECORDS["AMZN"] = build(
    "AMZN",
    periods=[
        mk_period("2021-12-31", [
            R("revenue", 469822, "usd_millions", "AMZN FY2021 revenue"),
            R("earnings", 33360, "usd_millions", "AMZN FY2021 net income", limitation="Moderate confidence only -- the underlying search snippet was internally contradictory (stating net income 'increased by $33.4bn from $21.3bn a year earlier,' which would imply ~$54.7B, not $33.36B). $33.36B is used because it is the widely-cited actual figure and cross-checks reasonably via EPS math ($33.36B / $64.81 pre-split EPS = ~515M pre-split shares, a plausible AMZN 2021 share count)."),
            D("operating_margin", 0.053, "ratio", "Derived: FY2021 operating income $24,879M divided by revenue $469,822M equals 5.3 percent.", "AMZN FY2021 operating income $24,879M"),
        ]),
        mk_period("2022-12-31", [
            R("revenue", 513983, "usd_millions", "AMZN FY2022 revenue"),
            R("earnings", -2722, "usd_millions", "AMZN FY2022 net loss"),
            D("operating_margin", 0.024, "ratio", "Derived: FY2022 operating income $12,248M divided by revenue $513,983M equals 2.4 percent.", "AMZN FY2022 operating income $12,248M"),
        ]),
        mk_period("2023-12-31", [
            R("revenue", 574785, "usd_millions", "AMZN FY2023 revenue (rounded, cited as '$575B')"),
            R("earnings", 30400, "usd_millions", "AMZN FY2023 net income"),
            D("operating_margin", 0.064, "ratio", "Derived: FY2023 operating income $36,900M divided by revenue $574,785M equals 6.4 percent.", "AMZN FY2023 operating income $36,900M"),
        ]),
        mk_period("2024-12-31", [
            R("revenue", 638000, "usd_millions", "AMZN FY2024 revenue"),
            R("earnings", 59200, "usd_millions", "AMZN FY2024 net income"),
            D("operating_margin", 0.108, "ratio", "Derived: FY2024 operating income $68,600M divided by revenue $638,000M equals 10.75 percent.", "AMZN FY2024 operating income $68,600M"),
            R("free_cash_flow", 38200, "usd_millions", "AMZN FY2024 free cash flow"),
        ]),
        mk_period("2025-12-31", [
            R("revenue", 716900, "usd_millions", "AMZN FY2025 revenue"),
            R("earnings", 77700, "usd_millions", "AMZN FY2025 net income"),
            D("operating_margin", 0.112, "ratio", "Derived: FY2025 operating income $80,000M divided by revenue $716,900M equals 11.16 percent (one source cited $79.9B, a rounding variance).", "AMZN FY2025 operating income $80,000M"),
            R("free_cash_flow", 11200, "usd_millions", "AMZN FY2025 free cash flow"),
            R("capex", 131820, "usd_millions", "AMZN FY2025 'purchases of property and equipment'", limitation="A derived cross-check (operating cash flow $139,500M minus FCF $11,200M = ~$128,300M) does not exactly reconcile with this $131,820M figure (~$3.5B gap) -- likely because AMZN's disclosed FCF is capex net of proceeds from sales/incentives while $131.82B may be the gross line; not resolved."),
            D("cash", 123029, "usd_millions", "Derived: cash & equivalents $86,810M plus marketable securities $36,200M equals $123,029M combined (internally consistent, 86.81+36.2=123.01).", "AMZN balance sheet, Dec 31 2025"),
            D("debt", 68396, "usd_millions", "Derived: long-term debt $65,648M plus current portion of long-term debt $2,748M equals ~$68,396M total debt.", "AMZN balance sheet, Dec 31 2025", limitation="A separate aggregator claim of 'total debt $209.88B / net debt $66.18B' was investigated and rejected as likely wrong (probably conflates total liabilities or lease obligations with debt); this record uses the directly-reported long-term-debt components instead."),
            D("net_debt", -54700, "usd_millions", "Derived (approximate, net CASH position): total cash+securities $123,029M minus total debt $68,396M equals ~$54.6B net cash (negative net debt).", "AMZN balance sheet figures above"),
            R("share_count_diluted", 10830, "shares_millions", "AMZN diluted weighted-average shares, Q4 2025"),
        ]),
    ],
    segments=[
        segment("North America", revenue=R("revenue", 426300, "usd_millions", "AMZN FY2025 North America segment net sales, +10% YoY"), profit=R("earnings", 29600, "usd_millions", "AMZN FY2025 North America segment operating income (vs. $25,000M FY2024)")),
        segment("International", revenue=R("revenue", 161900, "usd_millions", "AMZN FY2025 International segment net sales, +13% YoY"), profit=R("earnings", 4700, "usd_millions", "AMZN FY2025 International segment operating income (vs. $3,800M FY2024)")),
        segment("AWS", revenue=R("revenue", 128700, "usd_millions", "AMZN FY2025 AWS segment net sales, +20% YoY"), profit=R("earnings", 45600, "usd_millions", "AMZN FY2025 AWS segment operating income (vs. $39,800M FY2024; AWS was 57% of total FY2025 operating income)")),
    ],
    price=mk_price(274.34, "Aug 8 2026; market cap ~$2.96T. Stock briefly crossed a $3T market cap on Aug 3 2026 (all-time-high close $284.02) before pulling back; 52-week range $196.00-$287.20."),
    peers_data=[
        ("MSFT", "Closest direct AWS-vs-Azure cloud-infrastructure comparable."),
        ("GOOGL", "Comparable diversified big-tech profile (Cloud plus a large core business, similar scale)."),
        ("WMT", "Closest large-scale physical/omnichannel retail comparable for the e-commerce side of the business."),
    ],
    scenarios_data=[
        ("AWS/AI capex trajectory", "CEO guided ~$220B cash capex for 2026, up from an originally-planned ~$200B (~$20B increase attributed to rising memory prices); Trainium in-house AI chips have deals with Anthropic/OpenAI, with early exploratory conversations about offering Trainium to customers outside AWS's own cloud."),
        ("FTC antitrust litigation", "FTC and 18 state Attorneys General's monopoly-power suit against Amazon; bench trial now scheduled for Feb 9 2027, delayed from an earlier October 2026 date (Amazon lost its bid to keep the earlier date)."),
    ],
    uncertainty_summary=(
        "All figures secondary/search-aggregation-sourced; no primary document directly opened. FY2021 "
        "net income is moderate-confidence only (the underlying snippet was internally contradictory, "
        "cross-checked via EPS-implied share count instead). AMZN executed a 20-for-1 stock split "
        "effective June 2022 -- FY2021 EPS is not reported in this record to avoid a pre/post-split "
        "comparability trap (revenue and net income, unaffected by the split, are reported normally). "
        "AMZN's own reported capex and the capex figure implied by OCF minus FCF disagree by ~$3.5B, "
        "disclosed rather than reconciled. A materially wrong-looking aggregator claim about total debt "
        "($209.88B) and net debt ($66.18B net DEBT) was investigated and explicitly rejected in favor of "
        "a directly-reported-component-based derivation showing AMZN in a net CASH position instead."
    ),
)

RECORDS["AVGO"] = build(
    "AVGO",
    periods=[
        mk_period("2021-10-31", [
            R("revenue", 27450, "usd_millions", "AVGO FY2021 (ended Oct 31 2021) revenue"),
            D("earnings", 6437, "usd_millions", "Derived from a reported FY2021 net margin figure (secondary aggregator), not a directly reported dollar figure.", "AVGO FY2021 net margin (secondary aggregator)"),
        ]),
        mk_period("2022-10-30", [
            R("revenue", 33203, "usd_millions", "AVGO FY2022 revenue"),
            D("earnings", 11223, "usd_millions", "Derived from a reported FY2022 net margin figure (secondary aggregator); a second metric on the same source ('income from continuing operations') showed $11,495M, a small unresolved gap.", "AVGO FY2022 net margin (secondary aggregator)"),
        ]),
        mk_period("2023-10-29", [
            R("revenue", 35819, "usd_millions", "AVGO FY2023 revenue"),
            R("earnings", 14082, "usd_millions", "AVGO FY2023 net income"),
            R("operating_margin", 0.4525, "ratio", "AVGO FY2023 operating margin (operating income $16,207M / revenue $35,819M = 45.25%, matches an independent aggregator figure exactly)"),
        ]),
        mk_period("2024-11-03", [
            R("revenue", 51574, "usd_millions", "AVGO FY2024 (ended ~Nov 3 2024) revenue", limitation="VMware acquisition closed Nov 22 2023; FY2024 is the first full fiscal year of consolidation. A 10-for-1 forward stock split also took effect Jul 15 2024, mid-way through this fiscal year, so even within-FY2024 per-share figures are not on a single consistent share basis without adjustment."),
            R("earnings", 5895, "usd_millions", "AVGO FY2024 net income", limitation="GAAP net income cratered from FY2023's $14,082M largely due to VMware acquisition-related intangible amortization and restructuring charges, not underlying operating deterioration (operating income only fell from $16,207M to $13,463M over the same period)."),
            R("operating_margin", 0.261, "ratio", "AVGO FY2024 operating margin (operating income $13,463M / revenue $51,574M = 26.10%, matches an independent aggregator figure exactly)"),
        ]),
        mk_period("2025-11-02", [
            R("revenue", 64000, "usd_millions", "AVGO FY2025 (ended Nov 2 2025) revenue (rounded; one snippet cited '$63,887M,' unconfirmed to the exact million)"),
            R("earnings", 23130, "usd_millions", "AVGO FY2025 net income (secondary aggregator)"),
            abstain_item("operating_margin", "Two aggregator figures for FY2025 operating margin disagree by ~1 percentage point (39.89% vs. 40.75%) and were not reconciled -- not reported as a single confident figure."),
            R("free_cash_flow", 26900, "usd_millions", "AVGO FY2025 free cash flow"),
            D("capex", 637, "usd_millions", "Derived (approximate): operating cash flow ~$27,537M (summed from four quarters) minus free cash flow $26,900M equals ~$637M; a separate sum of quarterly capex disclosures (~$623M) is reasonably consistent.", "AVGO quarterly cash-flow disclosures, FY2025"),
            R("cash", 16178, "usd_millions", "AVGO cash & equivalents, Nov 2 2025 (FY2025 fiscal year-end)"),
            R("debt", 37621, "usd_millions", "AVGO long-term debt, cited to the FY2025 10-K (Nov 2 2025)", limitation="A separate, much larger total-debt figure (~$64.9-66.1B) was found, but appears to be dated to Feb 1 2026 (Q1 FY2026), i.e. a subsequent quarter after this fiscal year-end -- not used as a FY2025 fiscal-year-end figure; disclosed as a later data point only, not reconciled."),
            R("share_count_diluted", 4850, "shares_millions", "AVGO diluted weighted-average shares, FY2025 (post-split)"),
        ]),
    ],
    segments=[
        segment("Semiconductor Solutions", revenue=R("revenue", 37000, "usd_millions", "AVGO FY2025 Semiconductor Solutions segment revenue (approximate; AI semiconductor revenue reported at ~$20B within this, +65% YoY)")),
        segment("Infrastructure Software", revenue=R("revenue", 27000, "usd_millions", "AVGO FY2025 Infrastructure Software segment revenue (approximate; includes VMware)")),
    ],
    price=mk_price(426.29, "Aug 8 2026 (day range $421.61-$430.82); market cap ~$2.18T; trailing P/E cited at 65.30."),
    peers_data=[
        ("NVDA", "Dominant AI accelerator/GPU peer, though a different business model (merchant GPU vs. Broadcom's custom ASIC/XPU model)."),
        ("MRVL", "Marvell -- closest direct peer in custom AI silicon (ASIC) and networking/optical interconnect."),
        ("QCOM", "Qualcomm -- comparable large diversified semiconductor peer with meaningful connectivity/IP-licensing exposure."),
    ],
    scenarios_data=[
        ("Custom AI accelerator (XPU) customer concentration", "Broadcom has disclosed deep collaboration with six hyperscale customers on custom AI XPUs (reportedly including Google, Meta, OpenAI, Anthropic, and possibly Apple per one unconfirmed source). Secured a ~$11B order from Anthropic for late-2026 delivery; management cited 'line of sight' to over $100B of AI-chip revenue in 2027 -- customer concentration in a small hyperscaler set is a disclosed risk factor in secondary commentary."),
        ("VMware integration", "Management has targeted more than doubling VMware's EBITDA to $8.5B within three years of the November 2023 close, framed as enabling a full-stack silicon-to-virtualization offering."),
    ],
    uncertainty_summary=(
        "All figures secondary/search-aggregation-sourced; no primary document directly opened. Two "
        "structural discontinuities affect this whole record: the VMware acquisition (closed Nov 22 2023, "
        "purchase price reported inconsistently as ~$61B vs. '$69 billion' in a separate headline, not "
        "reconciled) and a 10-for-1 forward stock split effective Jul 15 2024, which falls mid-way through "
        "FY2024 itself. FY2021/FY2022 net income are derived from margin percentages rather than directly "
        "reported dollar figures and are lower-confidence as a result; FY2021/FY2022 diluted EPS were not "
        "reported at all given unresolved uncertainty about the underlying split-adjustment. FY2025 total "
        "debt carries a large, unresolved, disclosed discrepancy between a FY2025-fiscal-year-end figure "
        "and a later, materially larger figure from an early-2026 quarter -- only the FY2025-dated figure "
        "is used here. Segment operating income (as opposed to revenue) was not found for either segment."
    ),
)

RECORDS["COST"] = build(
    "COST",
    periods=[
        mk_period("2021-08-29", [
            R("revenue", 195929, "usd_millions", "COST FY2021 (ended late Aug 2021) revenue"),
            R("earnings", 5007, "usd_millions", "COST FY2021 net income"),
            abstain_item("operating_margin", "Only a rounded '~$6.7B, +20.7%' operating-income figure was found for FY2021; an exact dollar figure was not confirmed, so a confident operating margin is not derived here."),
        ]),
        mk_period("2022-08-28", [
            R("revenue", 226954, "usd_millions", "COST FY2022 revenue"),
            R("earnings", 5844, "usd_millions", "COST FY2022 net income"),
            D("operating_margin", 0.0343, "ratio", "Derived: FY2022 operating income $7,793M divided by revenue $226,954M equals 3.43 percent.", "COST FY2022 operating income $7,793M"),
        ]),
        mk_period("2023-09-03", [
            R("revenue", 242290, "usd_millions", "COST FY2023 revenue"),
            R("earnings", 6292, "usd_millions", "COST FY2023 net income"),
            D("operating_margin", 0.0335, "ratio", "Derived: FY2023 operating income $8,114M divided by revenue $242,290M equals 3.35 percent.", "COST FY2023 operating income $8,114M"),
        ]),
        mk_period("2024-09-01", [
            R("revenue", 254453, "usd_millions", "COST FY2024 revenue"),
            R("earnings", 7367, "usd_millions", "COST FY2024 net income"),
            D("operating_margin", 0.0365, "ratio", "Derived: FY2024 operating income $9,285M divided by revenue $254,453M equals 3.65 percent.", "COST FY2024 operating income $9,285M"),
        ]),
        mk_period("2025-08-31", [
            R("revenue", 275235, "usd_millions", "COST FY2025 total revenue (net sales $269,912M plus membership fee revenue $5,323M)"),
            R("earnings", 8099, "usd_millions", "COST FY2025 net income"),
            D("operating_margin", 0.0377, "ratio", "Derived and resolved: FY2025 operating income $10,383M divided by total revenue $275,235M equals 3.77 percent (3.85% on a net-sales-only basis excluding membership fees). A separately-found '3.14%' figure was investigated and rejected as unreliable -- it does not reconcile against any fiscal year's reported revenue/operating-income pair (FY2022: 3.43%, FY2023: 3.35%, FY2024: 3.65%, FY2025: 3.77-3.85%).", "COST FY2025 operating income $10,383M"),
            R("free_cash_flow", 7837, "usd_millions", "Derived: FY2025 operating cash flow $13,335M minus capex $5,498M equals $7,837M."),
            R("capex", 5498, "usd_millions", "COST FY2025 capital expenditures"),
            R("cash", 14161, "usd_millions", "COST cash & equivalents, Aug 31 2025"),
            D("debt", 5788, "usd_millions", "Derived: long-term debt $5,713M plus current portion $75M equals $5,788M total debt.", "COST balance sheet, Aug 31 2025"),
            D("net_debt", -8373, "usd_millions", "Derived (net CASH position): cash $14,161M minus total debt $5,788M equals ~$8,373M net cash.", "COST balance sheet figures above"),
            D("share_count_diluted", 444.8, "shares_millions", "Derived (approximate): FY2025 net income $8,099M divided by diluted EPS $18.21 equals ~444.8M diluted shares.", "COST FY2025 net income and diluted EPS figures"),
        ]),
    ],
    segment_abstain="Costco discloses three geographic segments (US, Canada, Other International) but only growth percentages (US +9%, Canada +6%, Other International +8% for FY2025) and a qualitative statement ('US and Canadian operations accounted for 86% of net sales and 84% of operating income') were found -- no precise dollar-value segment breakdown was located.",
    price=mk_price(950.5, "~Aug 6 2026 (reported range ~$949-952); market cap ~$422.1B (sanity check: 444.8M shares x $951 = ~$423B, consistent)."),
    peers_data=[
        ("WMT", "Walmart (including Sam's Club) -- largest general/warehouse retailer, direct membership-club overlap via Sam's Club, trades at a lower multiple than Costco per one source (~31x vs. ~40x earnings)."),
        ("BJ", "BJ's Wholesale Club -- closest pure-play warehouse-club peer, smaller footprint, trades at a materially lower multiple."),
        ("TGT", "Target -- a weaker structural comparable than Walmart/BJ's for a membership warehouse model, since it is a general-merchandise retailer rather than a warehouse club."),
    ],
    scenarios_data=[
        ("Membership fee growth and renewal trends", "FY2025 membership fee revenue grew 10.3% YoY to $5,323M (Q4 fee income +14% YoY to $1,724M); company guiding to ~9.1% fee growth in FY2026. Worldwide renewal rate eased slightly to 89.8% from 90.2%, attributed partly to a mix shift toward online sign-ups."),
        ("E-commerce growth", "FY2025 e-commerce sales exceeded $19.6B, +15.6% YoY, ~7.3% of total sales -- an eighth straight quarter of 10%+ e-commerce growth; the company added deferred-payment/installment financing via Affirm. Warehouse count reached 914 locations after 24 net new openings in FY2025 (15 US, 2 Canada, 7 Other International)."),
    ],
    uncertainty_summary=(
        "All figures secondary/search-aggregation-sourced; no primary document directly opened. FY2021 "
        "operating margin is abstained -- only a rounded operating-income figure was found. FY2025 "
        "operating margin required resolving a genuine prior conflict between a 3.77% derived figure and "
        "a previously-circulated, unreliable 3.14% figure that does not reconcile against any fiscal "
        "year's reported numbers -- 3.77% (total-revenue basis) is used, with the rejected figure "
        "disclosed rather than silently dropped. Precise dollar-value geographic segment data was not "
        "found (only growth percentages and a qualitative statement)."
    ),
)

RECORDS["TSLA"] = build(
    "TSLA",
    periods=[
        mk_period("2021-12-31", [
            R("revenue", 53823, "usd_millions", "TSLA FY2021 revenue"),
            R("earnings", 5519, "usd_millions", "TSLA FY2021 net income attributable to common"),
            D("operating_margin", 0.1212, "ratio", "Derived: FY2021 operating income $6,523M divided by revenue $53,823M equals 12.12 percent.", "TSLA FY2021 operating income $6,523M"),
        ]),
        mk_period("2022-12-31", [
            R("revenue", 81462, "usd_millions", "TSLA FY2022 revenue"),
            R("earnings", 12556, "usd_millions", "TSLA FY2022 net income attributable to common"),
            D("operating_margin", 0.1677, "ratio", "Derived: FY2022 operating income $13,656M divided by revenue $81,462M equals 16.77 percent.", "TSLA FY2022 operating income $13,656M"),
        ]),
        mk_period("2023-12-31", [
            R("revenue", 96773, "usd_millions", "TSLA FY2023 revenue"),
            R("earnings", 14997, "usd_millions", "TSLA FY2023 net income attributable to common", limitation="Includes a one-time, non-cash $5.9B deferred-tax valuation-allowance release; excluding that item, non-GAAP-adjusted net income for FY2023 was reported at ~$10.9B -- FY2023 GAAP net income/EPS is not directly comparable to other years in this record without adjustment for that item."),
            D("operating_margin", 0.0919, "ratio", "Derived: FY2023 operating income $8,891M divided by revenue $96,773M equals 9.19 percent.", "TSLA FY2023 operating income $8,891M"),
        ]),
        mk_period("2024-12-31", [
            R("revenue", 97690, "usd_millions", "TSLA FY2024 revenue"),
            R("earnings", 7000, "usd_millions", "TSLA FY2024 net income attributable to common (rounded)"),
            D("operating_margin", 0.0724, "ratio", "Derived: FY2024 operating income $7,076M divided by revenue $97,690M equals 7.24 percent.", "TSLA FY2024 operating income $7,076M"),
            R("free_cash_flow", 3584, "usd_millions", "TSLA FY2024 free cash flow (operating cash flow $14,923M minus capex $11,339M; reported and derived figures match)"),
            R("capex", 11339, "usd_millions", "TSLA FY2024 capital expenditures"),
        ]),
        mk_period("2025-12-31", [
            R("revenue", 94827, "usd_millions", "TSLA FY2025 revenue, -3% YoY, a second consecutive annual delivery decline"),
            R("earnings", 3790, "usd_millions", "TSLA FY2025 net income attributable to common"),
            D("operating_margin", 0.0459, "ratio", "Derived: FY2025 operating income $4,355M divided by revenue $94,827M equals 4.59 percent (matches an independently-reported '~4.6%' figure).", "TSLA FY2025 operating income $4,355M"),
            R("free_cash_flow", 6220, "usd_millions", "TSLA FY2025 free cash flow (operating cash flow $14,747M minus capex $8,527M; matches an independently-reported '$6.22B, +74% YoY' figure)"),
            R("capex", 8527, "usd_millions", "TSLA FY2025 capital expenditures"),
            D("cash", 44059, "usd_millions", "Derived: cash & equivalents $16,513M plus short-term investments $27,546M equals $44,059M combined.", "TSLA balance sheet, Dec 31 2025"),
            D("debt", 8376, "usd_millions", "Derived: current debt & finance leases $1,640M plus long-term debt & finance leases $6,736M equals $8,376M total.", "TSLA balance sheet, Dec 31 2025"),
            D("net_debt", -35683, "usd_millions", "Derived (net CASH position): cash+investments $44,059M minus total debt $8,376M equals ~$35.68B net cash.", "TSLA balance sheet figures above"),
            R("share_count_diluted", 3751, "shares_millions", "TSLA shares outstanding (issued, year-end, not weighted-average diluted)", limitation="This is a year-end issued-share count, not the weighted-average diluted count used to compute EPS; a diluted weighted-average cross-check via net income/EPS implies ~3.51B shares."),
        ]),
    ],
    segments=[
        segment("Automotive", revenue=R("revenue", 69520, "usd_millions", "TSLA FY2025 Automotive segment revenue, -10% YoY")),
        segment("Energy Generation & Storage", revenue=R("revenue", 12800, "usd_millions", "TSLA FY2025 Energy Generation & Storage segment revenue, +27% YoY")),
        segment("Services & Other", revenue=R("revenue", 12530, "usd_millions", "TSLA FY2025 Services & Other segment revenue, +19% YoY")),
    ],
    price=mk_price(328.58, "Aug 8 2026; market cap ~$1.26T (sanity check: 3,751M shares x $328.58 = ~$1.233T, in the right range but not exact, likely a slightly different/more current share count is used by market-cap providers).", ),
    peers_data=[
        ("F", "Ford / GM / Toyota (traditional automakers) -- legacy ICE/hybrid manufacturers now building EVs; useful for auto-industry multiples but a very different growth/margin profile than TSLA."),
        ("BYDDY", "BYD -- largest EV maker by global unit volume (reported ~17.1% global EV share vs. Tesla), direct EV competitor with a China-centric geographic mix."),
        ("RIVN", "Rivian -- much smaller (~$20B market cap reported) pure-play EV startup, an early-growth rather than scale comparable."),
    ],
    scenarios_data=[
        ("Robotaxi/FSD rollout", "Unsupervised robotaxi service active in Austin (full metro, ~245 sq mi) plus expansion confirmed to Dallas and Houston as of late April 2026, with additional cities (Phoenix, Miami, Orlando, Tampa, Las Vegas) targeted for H1 2026 -- some of this reflects company guidance rather than confirmed completed rollout, disclosed as mixed-quality sourcing. ~700,000 paid robotaxi miles logged since the June 2025 launch."),
        ("Energy storage growth and deliveries", "Q2 2026 energy storage deployments of 13.5 GWh, up over 40% YoY from 9.6 GWh in Q2 2025; SpaceX purchased $269M of Megapacks in April 2026 for xAI data-center power in Memphis. FY2025 vehicle deliveries were ~1.64M, a second consecutive annual decline, though Q2 2026 deliveries rebounded to 480,126 units (+25% YoY), the first quarterly YoY growth since the 2023 sales peak."),
    ],
    uncertainty_summary=(
        "All figures secondary/search-aggregation-sourced; no primary document directly opened. FY2023 "
        "net income includes a disclosed one-time $5.9B tax benefit and is not directly comparable to "
        "other years without adjustment (a non-GAAP-adjusted ~$10.9B figure was separately reported for "
        "that year). Some search results returned stale market-cap figures ($1.46-1.49T) from apparently "
        "older articles; the most recently-dated observation ($328.58/$1.26T, Aug 8 2026) was used instead "
        "and the rejected stale figures are disclosed here rather than silently discarded. FY2025 shares "
        "outstanding is a year-end issued-share count, not the weighted-average diluted count actually "
        "used to compute EPS."
    ),
)

RECORDS["RKLB"] = build(
    "RKLB",
    periods=[
        mk_period("2021-12-31", [
            R("revenue", 62.2, "usd_millions", "RKLB FY2021 revenue, +77% YoY"),
            R("earnings", -117.3, "usd_millions", "RKLB FY2021 net loss"),
        ]),
        mk_period("2022-12-31", [
            R("revenue", 211.0, "usd_millions", "RKLB FY2022 revenue"),
            R("earnings", -135.2, "usd_millions", "RKLB FY2022 net loss"),
        ]),
        mk_period("2023-12-31", [
            R("revenue", 244.6, "usd_millions", "RKLB FY2023 revenue"),
            R("earnings", -178.9, "usd_millions", "RKLB FY2023 net loss"),
        ]),
        mk_period("2024-12-31", [
            R("revenue", 436.2, "usd_millions", "RKLB FY2024 revenue, +78% YoY"),
            R("earnings", -189.4, "usd_millions", "RKLB FY2024 net loss"),
        ]),
        mk_period("2025-12-31", [
            R("revenue", 601.8, "usd_millions", "RKLB FY2025 revenue, +38% YoY"),
            R("earnings", -198.2, "usd_millions", "RKLB FY2025 net loss, widened ~4.2% from FY2024"),
            R("free_cash_flow", -321, "usd_millions", "RKLB FY2025 free cash flow (negative -- cash burn), described as a '210.72% increase in cash burn from 2024'"),
            R("capex", 49.7, "usd_millions", "RKLB Q4 2025 capital expenditures (quarterly figure, not full-year)"),
            R("cash", 1100, "usd_millions", "RKLB cash & equivalents, year-end 2025"),
            R("debt", 152.4, "usd_millions", "RKLB convertible senior notes, net, Dec 31 2025 (down from an original $355M issuance)"),
            R("share_count_diluted", 589.5, "shares_millions", "RKLB shares issued (common stock) as of Dec 31 2025 -- not necessarily the same as a weighted-average diluted count."),
        ]),
    ],
    segments=[
        segment("Space Systems", revenue=R("revenue", 402.8, "usd_millions", "RKLB FY2025 Space Systems segment revenue, 66.9% of total")),
        segment("Launch Services", revenue=R("revenue", 199.0, "usd_millions", "RKLB FY2025 Launch Services segment revenue, 33.1% of total")),
    ],
    price=mk_price(75.97, "Aug 4 2026; market cap ~$47.28B (sanity check: 589.5M shares x $75.97 = ~$44.8B, ~$2.5B under the reported cap, plausibly because the share count has grown further in 2026 via option/convertible-note conversions beyond the Dec 31 2025 figure used here). 52-week range $37.57-$151.00, all-time high $150.23 (May 27 2026) -- a genuinely volatile stock."),
    peers_data=[
        ("SPACEX", "SpaceX -- dominant private competitor, far larger, not a public-market valuation comparable but the obvious market-position benchmark."),
        ("FLY", "Firefly Aerospace -- closest maturity/size public peer, smaller than RKLB (FY2025 revenue $160M vs. RKLB's $601.8M) but with a similarly young, high-growth profile."),
    ],
    scenarios_data=[
        ("Neutron rocket development", "First orbital launch has slipped multiple times; as of the most recent (Jul 2026) reporting, Rocket Lab is targeting Q4 2026 for first flight, after a January 2026 tank failure removed an earlier window. Program cost originally guided at $250-300M, but delays mean cumulative spend was reported at likely ~$360M by end of 2025. Structural-test qualification and the Wallops Island, VA launch site are reported complete."),
        ("Pending Iridium acquisition", "Announced Jun 29 2026 -- Rocket Lab to acquire Iridium Communications for ~$8.0B enterprise value, a cash-and-stock deal at $54.00/share for Iridium common stock, with $3.6B in acquisition financing from Deutsche Bank and Wells Fargo. Reported 'expected to close next year' (2027) -- not yet closed as of this research. Rationale reported as vertical integration, combining launch and satellite manufacturing with Iridium's L-band spectrum/network and subscriber base."),
        ("Government contract backlog", "FY2025 total backlog grew 73% YoY to $1.85B; Rocket Lab was awarded an $816M Space Development Agency contract to design and build 18 satellites for the 'Tracking Layer Tranche 3' program."),
    ],
    uncertainty_summary=(
        "All figures secondary/search-aggregation-sourced; no primary document directly opened. Rocket "
        "Lab's public listing was fact-checked and confirmed: SPAC merger with Vector Acquisition "
        "Corporation, trading commenced under 'RKLB' on Aug 25 2021 -- a full loss history is available "
        "for all fiscal years since listing (no data gaps), so no shortened-history exception is needed on "
        "listing-age grounds, though this remains an archetype E (scenario/binary-outcome-relevant) record "
        "given the young, historically unprofitable, launch-milestone-dependent nature of the business -- "
        "cash-runway and scenario evidence (Neutron timeline, the pending Iridium acquisition, backlog) "
        "are prioritized accordingly. FY2025 capex is a Q4-only quarterly figure, not a full-year total "
        "(a full-year figure was not found and this is disclosed rather than annualized/estimated). The "
        "Iridium acquisition is real and pending, explicitly not yet closed."
    ),
)
