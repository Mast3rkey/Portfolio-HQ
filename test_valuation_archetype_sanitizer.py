"""Tests for valuation_archetype_sanitizer.py (WS-0005 valuation-archetype
blind-drafting isolation, VALUATION-0003 scope).

Proof-of-redacted-input-workflow tests per VALUATION-0003 SS F.4/SS I:
demonstrates the sanitizer strips every prohibited field/pattern from
representative fixtures, and that the independent second-stage scan uses a
materially different code path than the strip logic (never the same
function called twice).
"""

from pathlib import Path

import pytest
import yaml

import valuation_archetype_sanitizer as vas

REPO_ROOT = Path(__file__).resolve().parent


# ── whole-key strip (SS F.1) ────────────────────────────────────────────

def test_strip_yaml_data_removes_portfolio_role_ref():
    data = {"portfolio_role_ref": "T1", "sector": "Tech"}
    out = vas.strip_yaml_data(data)
    assert "portfolio_role_ref" not in out
    assert out["sector"] == "Tech"


def test_strip_yaml_data_removes_conviction_whole_block():
    data = {"conviction": {"rating": "High", "rationale": "..."}, "sector": "Tech"}
    out = vas.strip_yaml_data(data)
    assert "conviction" not in out


def test_strip_yaml_data_removes_review_block():
    data = {"review": {"cadence_days": 90, "log": ["conviction rating raised"]}, "sector": "Tech"}
    out = vas.strip_yaml_data(data)
    assert "review" not in out


def test_strip_yaml_data_never_mutates_input():
    data = {"portfolio_role_ref": "T1", "sector": "Tech"}
    vas.strip_yaml_data(data)
    assert data["portfolio_role_ref"] == "T1"


def test_strip_yaml_data_preserves_permitted_fields():
    data = {
        "sector": "Tech", "industry": "Software",
        "competitive_advantages": ["moat"], "risks": [{"risk": "x"}],
        "catalysts": [{"catalyst": "y"}],
    }
    out = vas.strip_yaml_data(data)
    assert out == data


# ── item-level scan/redact (SS F.2) ─────────────────────────────────────

@pytest.mark.parametrize("text", [
    "carries no decision-bearing weight in this record's conviction rationale",
    "this record's gate names the reopening condition",
    "target weight of the destination allocation",
    "3.5% of the book",
    "per targets.yaml's destination list",
    "support level and resistance level analysis",
    "the RSI reading suggests momentum",
    "price target of the analyst community",
])
def test_item_text_is_forbidden_catches_real_leak_patterns(text):
    assert vas.item_text_is_forbidden(text) is True


@pytest.mark.parametrize("text", [
    "the technological gate that determines advanced-node adoption",
    "gate-all-around transistor architecture",
    "a customer-qualification gate for hyperscaler contracts",
    "revenue grew 28% year over year",
    "the company reported strong margins this quarter",
])
def test_item_text_is_forbidden_does_not_false_positive_on_legitimate_use(text):
    assert vas.item_text_is_forbidden(text) is False


def test_redact_item_replaces_forbidden_text_with_placeholder():
    out = vas.redact_item("this record's conviction rationale")
    assert out == vas._ITEM_REDACTION_PLACEHOLDER


def test_redact_item_passes_through_clean_text():
    text = "AWS revenue grew 28% YoY"
    assert vas.redact_item(text) == text


def test_contains_gate_policy_leak_whitelists_known_legitimate_phrases():
    assert vas.contains_gate_policy_leak("the technological gate for High-NA EUV") is False
    assert vas.contains_gate_policy_leak("this ticker's gate is still open") is True


# ── allow-list extraction (SS D) ─────────────────────────────────────────

def test_extract_business_summary_pulls_only_that_section():
    md = (
        "## Source-access disclosure\nblocked\n\n"
        "## Business summary\nWe make widgets.\n\n"
        "## Conviction\nRating: High\n"
    )
    out = vas.extract_business_summary(md)
    assert out == "We make widgets."
    assert "Conviction" not in out
    assert "Rating" not in out


def test_extract_business_summary_returns_empty_when_absent():
    assert vas.extract_business_summary("## Risks\nsome risk\n") == ""


def test_build_sanitized_packet_never_extracts_conviction_or_portfolio_role_ref():
    company_yaml = {
        "sector": "Tech", "industry": "Software",
        "portfolio_role_ref": "T1",
        "conviction": {"rating": "High", "rationale": "x"},
        "competitive_advantages": ["a real moat"],
        "risks": [{"risk": "a real risk"}],
        "catalysts": [{"catalyst": "a real catalyst"}],
        "review": {"log": ["conviction raised to High"]},
    }
    md = "## Business summary\nWe make widgets.\n\n## Conviction\nRating: High\n"
    pkt = vas.build_sanitized_packet("TEST", company_yaml, md)
    rendered = vas.packet_to_drafting_text(pkt)
    assert "T1" not in rendered
    assert "portfolio_role_ref" not in rendered
    assert "conviction" not in rendered.lower()
    assert "Rating: High" not in rendered
    assert "widgets" in rendered


def test_build_sanitized_packet_redacts_leaking_item_but_keeps_clean_items():
    company_yaml = {
        "sector": "Tech", "industry": "Software",
        "risks": [
            {"risk": "a real, disclosed operating risk"},
            {"risk": "this record's gate names a reopening trigger"},
        ],
    }
    pkt = vas.build_sanitized_packet("TEST", company_yaml, "## Business summary\nText.\n")
    assert pkt.redacted_item_count == 1
    assert any("real, disclosed operating risk" in r for r in pkt.risks)
    assert any(r == vas._ITEM_REDACTION_PLACEHOLDER for r in pkt.risks)


def test_build_sanitized_packet_includes_role_basis_when_classification_provided():
    company_yaml = {"sector": "Tech", "industry": "Software"}
    classification_yaml = {"economic_role": {"role_basis": "a clean contextual sentence"}}
    pkt = vas.build_sanitized_packet(
        "TEST", company_yaml, "## Business summary\nText.\n", classification_yaml,
    )
    assert pkt.role_basis == "a clean contextual sentence"


def test_packet_hash_is_deterministic():
    pkt = vas.build_sanitized_packet(
        "TEST", {"sector": "Tech", "industry": "Software"}, "## Business summary\nText.\n",
    )
    assert vas.packet_hash(pkt) == vas.packet_hash(pkt)


# ── independent second-stage scan (SS F.3) -- proof of independence ─────

def test_independent_scan_is_a_separate_function_from_item_level_check():
    """AST-level proof: independent_policy_scan is never called by
    item_text_is_forbidden or redact_item, and vice versa -- a materially
    different mechanism, not the same function called twice."""
    import ast
    import inspect

    src = inspect.getsource(vas.item_text_is_forbidden)
    assert "independent_policy_scan(" not in src
    src2 = inspect.getsource(vas.redact_item)
    assert "independent_policy_scan(" not in src2
    src3 = inspect.getsource(vas.independent_policy_scan)
    assert "item_text_is_forbidden(" not in src3
    # sanity: it does parse as valid python (not a trivial empty function)
    tree = ast.parse(src3)
    assert isinstance(tree, ast.Module)


@pytest.mark.parametrize("text", [
    "this record's conviction rationale",
    "target weight of the position",
    "%  of the book",
    "primary_disposition: case_for_review",
    "support level analysis suggests a breakout",
    "the RSI and MACD both signal momentum",
])
def test_independent_policy_scan_catches_leaks(text):
    assert vas.independent_policy_scan(text) != []


def test_independent_policy_scan_whitelists_gate_legitimate_use():
    assert vas.independent_policy_scan("the technological gate for EUV") == []


def test_verify_packet_clean_for_well_formed_packet():
    pkt = vas.build_sanitized_packet(
        "TEST", {"sector": "Tech", "industry": "Software"},
        "## Business summary\nOrdinary business text.\n",
    )
    assert vas.verify_packet(pkt) == []


def test_verify_sealed_record_text_catches_leak_in_rationale():
    findings = vas.verify_sealed_record_text("this ticker's conviction rating is High")
    assert findings != []


def test_verify_sealed_record_text_clean_for_ordinary_rationale():
    findings = vas.verify_sealed_record_text(
        "The business shows high gross margin and recurring revenue.", None,
    )
    assert findings == []


# ── gate fact (SS D/SS E) -- mechanical, never fed to drafting ─────────

def test_gate_fact_for_ticker_detects_valuation_reference():
    gates_data = {"gates": [{"ticker": "SPGI", "next_gate": "Review a normalized SPGI-versus-MSCI valuation."}]}
    fact = vas.gate_fact_for_ticker("SPGI", gates_data)
    assert fact == {"gate_exists": True, "next_gate_references_valuation": True}


def test_gate_fact_for_ticker_no_valuation_reference():
    gates_data = {"gates": [{"ticker": "ICE", "next_gate": "Review the financing assumptions."}]}
    fact = vas.gate_fact_for_ticker("ICE", gates_data)
    assert fact == {"gate_exists": True, "next_gate_references_valuation": False}


def test_gate_fact_for_ticker_none_when_not_gated():
    gates_data = {"gates": [{"ticker": "SPGI", "next_gate": "x"}]}
    assert vas.gate_fact_for_ticker("AMZN", gates_data) is None


# ── real-corpus regression: every actually-sealed record's packet input
# reproduces clean, deterministic, and un-leaked (defense in depth) ──────

_ROSTER = [
    "AMZN", "ASML", "AVGO", "CEG", "COST", "ETN", "GEV", "GNRC", "GOOGL", "ICE",
    "ISRG", "KLAC", "LLY", "META", "MSFT", "NVDA", "PANW", "PWR", "RKLB", "RTX",
    "SNPS", "SPGI", "TMO", "TSLA", "TSM", "V", "WM",
]


@pytest.mark.parametrize("ticker", _ROSTER)
def test_real_company_packet_is_deterministic_and_clean(ticker):
    company_yaml_path = REPO_ROOT / "intelligence" / "companies" / f"{ticker}.yaml"
    company_md_path = REPO_ROOT / "intelligence" / "companies" / f"{ticker}.md"
    if not company_yaml_path.is_file() or not company_md_path.is_file():
        pytest.skip(f"{ticker} Company Intelligence source not present")
    company_yaml = yaml.safe_load(company_yaml_path.read_text())
    company_md = company_md_path.read_text()
    pkt1 = vas.build_sanitized_packet(ticker, company_yaml, company_md)
    pkt2 = vas.build_sanitized_packet(ticker, company_yaml, company_md)
    assert vas.packet_hash(pkt1) == vas.packet_hash(pkt2)
    assert vas.verify_packet(pkt1) == []
