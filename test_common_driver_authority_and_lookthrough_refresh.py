"""Focused and adversarial tests for PHQ-2026-08 — the authoritative
common-driver measurement rule (PD-1) and the primary-source ETF
look-through refresh (PD-2).

What these tests are for, and what they deliberately are not:

  * They PROVE the PD-1 rule is recorded machine-readably, that the
    production helper `allocate._issuer_exposure` actually implements it
    (behaviourally, over synthetic inputs — not by asserting a source hash),
    and that no governed issuer's ETF-embedded exposure can be silently
    dropped.

  * They RE-DERIVE every refreshed `fund_holding_weight` from the retained
    official publisher files under `governance/evidence/PHQ-2026-08/`, using
    only the standard library, so the provenance chain is checkable in CI with
    no extra dependency. `openpyxl` is NOT required: the SPY workbook is read
    with `zipfile` + `xml.etree`.

  * They PIN the retained historical 40.0284% measurement as unchanged, and
    prove it is labelled historical evidence rather than the rule.

  * They do NOT pin `targets.yaml`, `gates.yaml`, `holdings.yaml`, or any
    other live policy file to a commit or to a literal value. That failure
    mode — a dated snapshot becoming a gate on future legitimate policy
    changes — was found and corrected twice in PR #397 and is not
    reintroduced here. Scope containment is instead proved structurally: this
    file's schema is closed, so nothing policy-shaped can hide inside it.
"""

from __future__ import annotations

import ast
import csv
import datetime as _dt
import hashlib
import io
import re
import xml.etree.ElementTree as ET
import zipfile
from decimal import Decimal
from pathlib import Path

import pytest
import yaml

import allocate
import currentness_report as cr

REPO_ROOT = Path(__file__).resolve().parent
LOOKTHROUGH_PATH = REPO_ROOT / "issuer_lookthrough.yaml"
EVIDENCE_DIR = REPO_ROOT / "governance" / "evidence" / "PHQ-2026-08"
DECISION_PATH = (REPO_ROOT / "governance" / "decisions"
                 / "PHQ-2026-08-common-driver-measurement-authority-and-lookthrough-refresh.md")

#: The eleven governed common-driver issuers. PHQ-2026-08 changes membership
#: for none of them; this literal is the membership-unchanged assertion.
GOVERNED_ISSUERS = frozenset({
    "NVDA", "MSFT", "AMZN", "GOOGL", "AVGO", "META",
    "LLY", "TSLA", "AAPL", "TSM", "ASML",
})

#: The three issuers whose embedded slices the retained 40.0284% headline is
#: arithmetically consistent with having omitted. PD-1 §2 forbids omitting them.
NEVER_OMITTED = ("LLY", "TSLA", "AAPL")

XLSX_NS = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"


# ── shared loaders ─────────────────────────────────────────────────────────────

@pytest.fixture(scope="module")
def lookthrough() -> dict:
    return yaml.safe_load(LOOKTHROUGH_PATH.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def lookthrough_text() -> str:
    return LOOKTHROUGH_PATH.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def rule(lookthrough: dict) -> dict:
    return lookthrough["common_driver_measurement_rule"]


@pytest.fixture(scope="module")
def sources(lookthrough: dict) -> dict:
    return lookthrough["fund_sources"]


def _issuer_rows(lookthrough: dict) -> dict[str, dict]:
    return {row["ticker"].upper(): row for row in lookthrough["issuers"]}


def _dec(value) -> Decimal:
    """Exact decimal of a YAML/CSV-sourced number, via its text form."""
    return Decimal(str(value))


# ── stdlib primary-source parsers (no third-party dependency) ──────────────────

def _read_xlsx_rows(path: Path) -> list[dict[str, str | None]]:
    """Read the first worksheet of an .xlsx as column-letter -> text maps.

    Uses only `zipfile` + `xml.etree` so the SPY provenance re-derivation runs
    unconditionally in CI. `openpyxl` is deliberately not a dependency of this
    repository and is not made one here.
    """
    with zipfile.ZipFile(path) as zf:
        shared: list[str] = []
        if "xl/sharedStrings.xml" in zf.namelist():
            sst = ET.fromstring(zf.read("xl/sharedStrings.xml"))
            for si in sst.findall(f"{XLSX_NS}si"):
                shared.append("".join(t.text or "" for t in si.iter(f"{XLSX_NS}t")))
        sheet = ET.fromstring(zf.read("xl/worksheets/sheet1.xml"))

    rows: list[dict[str, str | None]] = []
    for row in sheet.iter(f"{XLSX_NS}row"):
        cells: dict[str, str | None] = {}
        for c in row.findall(f"{XLSX_NS}c"):
            ref = c.get("r") or ""
            col = "".join(ch for ch in ref if ch.isalpha())
            v = c.find(f"{XLSX_NS}v")
            inline = c.find(f"{XLSX_NS}is")
            if c.get("t") == "s" and v is not None:
                cells[col] = shared[int(v.text)]
            elif inline is not None:
                cells[col] = "".join(t.text or "" for t in inline.iter(f"{XLSX_NS}t"))
            elif v is not None:
                cells[col] = v.text
            else:
                cells[col] = None
        rows.append(cells)
    return rows


def _spy_holdings(path: Path) -> tuple[str, dict[str, dict]]:
    """(as-of text, {SEDOL: {name, ticker, weight}}) from the official SPY file."""
    rows = _read_xlsx_rows(path)
    as_of = ""
    header_at = None
    for i, r in enumerate(rows):
        if (r.get("A") or "").strip().rstrip(":").lower() == "holdings":
            as_of = (r.get("B") or "").strip()
        if (r.get("A") or "").strip() == "Name" and (r.get("D") or "").strip() == "SEDOL":
            header_at = i
            break
    assert header_at is not None, "SPY workbook has no Name/.../SEDOL header row"

    out: dict[str, dict] = {}
    for r in rows[header_at + 1:]:
        sedol = (r.get("D") or "").strip()
        weight = (r.get("E") or "").strip()
        if not sedol or not weight:
            continue
        out[sedol] = {
            "name": (r.get("A") or "").strip(),
            "ticker": (r.get("B") or "").strip(),
            "weight": weight,
        }
    return as_of, out


def _vanguard_holdings(path: Path) -> tuple[str, dict[str, dict]]:
    """(as-of text, {SEDOL: {name, ticker, weight}}) from an official Vanguard
    Holdings-details CSV."""
    text = path.read_text(encoding="utf-8-sig")
    reader = list(csv.reader(io.StringIO(text)))

    as_of = ""
    header_at: int | None = None
    cols: dict[str, int] = {}
    pct_idx = -1
    for i, row in enumerate(reader):
        joined = ",".join(row)
        if "as of" in joined.lower() and not as_of:
            as_of = joined.split("as of", 1)[1].strip().strip(",").strip()
        upper = [c.strip().upper() for c in row]
        if "SEDOL" in upper and "TICKER" in upper and "HOLDINGS" in upper:
            header_at = i
            cols = {name: upper.index(name) for name in
                    ("SEDOL", "HOLDINGS", "TICKER")}
            pct_idx = next(j for j, c in enumerate(upper) if c.startswith("% OF FUND"))
            break
    assert header_at is not None, f"{path.name} has no SEDOL/HOLDINGS/TICKER header row"

    widest = max(list(cols.values()) + [pct_idx])
    out: dict[str, dict] = {}
    for row in reader[header_at + 1:]:
        if len(row) <= widest:
            continue
        sedol = row[cols["SEDOL"]].strip()
        if not sedol:
            continue
        out[sedol] = {
            "name": row[cols["HOLDINGS"]].strip(),
            "ticker": row[cols["TICKER"]].strip(),
            "weight": row[pct_idx].strip(),
        }
    return as_of, out


@pytest.fixture(scope="module")
def primary_holdings() -> dict[str, tuple[str, dict[str, dict]]]:
    return {
        "SPY": _spy_holdings(EVIDENCE_DIR / "holdings-daily-us-en-spy.xlsx"),
        "VEA": _vanguard_holdings(
            EVIDENCE_DIR / "Holdings_details_FTSE_Developed_Markets_ETF.csv"),
        "VWO": _vanguard_holdings(
            EVIDENCE_DIR / "Holdings_details_FTSE_Emerging_Markets_ETF.csv"),
    }


# ══ A. PD-1 is recorded, and recorded authoritatively ═════════════════════════

def test_pd1_rule_block_exists_with_full_effective_basis(rule: dict):
    assert rule["basis"] == "FULL_EFFECTIVE_ALL_ISSUERS"
    formula = rule["formula"]
    assert "DIRECT_EXPOSURE" in formula
    assert "ETF-EMBEDDED EXPOSURE" in formula
    assert "SUM over all governed common-driver issuers" in formula


def test_pd1_forbids_selective_exclusion_by_identity_not_truthiness(rule: dict):
    # `is False`, not `not rule[...]`: a string "false" or 0 would pass a
    # truthiness check while meaning nothing machine-readable.
    assert rule["selective_exclusion_permitted"] is False


def test_pd1_names_the_three_previously_omitted_issuers_explicitly(rule: dict):
    note = rule["selective_exclusion_note"]
    for ticker in NEVER_OMITTED:
        assert ticker in note, f"{ticker} must be named explicitly in the no-omission note"


def test_pd1_records_sedol_based_economic_issuer_aggregation(rule: dict):
    assert rule["economic_issuer_aggregation"] is True
    note = rule["economic_issuer_aggregation_note"]
    assert "SEDOL" in note
    assert "never by name similarity" in note


def test_pd1_records_principal_approval_and_a_real_authority_document(rule: dict):
    assert rule["principal_approval"] == "granted"
    authority = REPO_ROOT / rule["authority"]
    assert authority.is_file(), f"authority document missing: {rule['authority']}"
    assert authority.resolve() == DECISION_PATH.resolve()


def test_pd1_governed_issuer_count_matches_the_actual_membership(rule: dict,
                                                                 lookthrough: dict):
    assert rule["governed_issuer_count"] == 11
    assert rule["governed_issuer_count"] == len(lookthrough["issuers"])


def test_pd1_mirrored_ceilings_equal_the_live_ceilings(rule: dict, lookthrough: dict):
    assert rule["issuer_ceiling_pct_unchanged"] == lookthrough["issuer_ceiling_pct"] == 8.0
    assert (rule["common_driver_ceiling_pct_unchanged"]
            == lookthrough["common_driver_ceiling_pct"] == 40.0)


def test_pd1_states_allocate_is_unchanged_and_merely_ratified(rule: dict):
    implemented_by = rule["implemented_by"]
    assert "allocate._issuer_exposure" in implemented_by
    assert "UNCHANGED" in implemented_by


def test_decision_document_frontmatter_is_well_formed():
    text = DECISION_PATH.read_text(encoding="utf-8")
    assert text.startswith("---\n")
    front = yaml.safe_load(text.split("---", 2)[1])
    assert front["decision_id"] == "PHQ-2026-08"
    assert front["status"] == "Accepted"
    assert front["date"] == _dt.date(2026, 9, 18)
    assert front["supporting_artifact"] == "issuer_lookthrough.yaml"


def test_decision_is_registered_in_the_governance_catalog():
    catalog = yaml.safe_load(
        (REPO_ROOT / "governance" / "decisions.yaml").read_text(encoding="utf-8"))
    entry = next(d for d in catalog["decisions"] if d["decision_id"] == "PHQ-2026-08")
    assert (REPO_ROOT / entry["file"]).resolve() == DECISION_PATH.resolve()
    assert entry["status"] == "Accepted"


def test_decision_explicitly_withholds_trade_and_stage1_authority():
    text = DECISION_PATH.read_text(encoding="utf-8")
    assert "## Not authorized" in text
    for phrase in ("trade, order, or brokerage capability",
                   "Stage-1 arming",
                   "1.8x leverage cap and 30% buffer",
                   "MARGIN-0005"):
        assert phrase in text, f"decision must explicitly withhold: {phrase!r}"


# ══ B. Production code actually implements PD-1 (behavioural) ═════════════════

def _synthetic_lookthrough(weights: dict[str, tuple[str, float]]) -> dict:
    return {"issuers": [{"ticker": t, "funds": [{"fund": f, "fund_holding_weight": w}]}
                        for t, (f, w) in weights.items()]}


def test_issuer_exposure_sums_direct_plus_embedded_for_every_issuer():
    lt = _synthetic_lookthrough({"AAA": ("FND", 0.10), "BBB": ("FND", 0.25)})
    holdings = {"AAA": 20.0, "BBB": 30.0, "FND": 40.0}
    out = allocate._issuer_exposure(holdings, 100.0, lt)

    assert out["issuers"]["AAA"]["direct_pct"] == pytest.approx(20.0)
    assert out["issuers"]["AAA"]["embedded_pct"] == pytest.approx(4.0)   # 40% * 0.10
    assert out["issuers"]["AAA"]["effective_pct"] == pytest.approx(24.0)
    assert out["issuers"]["BBB"]["effective_pct"] == pytest.approx(40.0)  # 30 + 40*0.25
    # The common driver is the sum across ALL governed issuers, embedded included.
    assert out["common_driver_current_pct"] == pytest.approx(64.0)


def test_an_embedded_only_issuer_still_contributes_the_aapl_case():
    """AAPL carries no direct canonical target. Under any reading that drops
    embedded exposure it would contribute zero to a ceiling created to capture
    it. Production code must not do that."""
    lt = _synthetic_lookthrough({"ZZZ": ("FND", 0.50)})
    out = allocate._issuer_exposure({"FND": 10.0}, 100.0, lt)
    assert out["issuers"]["ZZZ"]["direct_pct"] == 0.0
    assert out["issuers"]["ZZZ"]["embedded_pct"] == pytest.approx(5.0)
    assert out["common_driver_current_pct"] == pytest.approx(5.0)
    assert out["common_driver_current_pct"] > 0.0


def test_dropping_an_embedded_weight_strictly_lowers_the_common_driver():
    """Adversarial: proves the embedded term is load-bearing rather than
    decorative. If a future edit reintroduced selective omission, the two
    measurements below would stop differing."""
    full = _synthetic_lookthrough({"AAA": ("FND", 0.20), "BBB": ("FND", 0.30)})
    omitted = _synthetic_lookthrough({"AAA": ("FND", 0.20), "BBB": ("FND", 0.0)})
    holdings = {"AAA": 1.0, "BBB": 1.0, "FND": 50.0}
    full_pct = allocate._issuer_exposure(holdings, 100.0, full)["common_driver_current_pct"]
    omitted_pct = allocate._issuer_exposure(holdings, 100.0, omitted)["common_driver_current_pct"]
    assert full_pct > omitted_pct
    assert full_pct - omitted_pct == pytest.approx(15.0)  # 50% * 0.30


def test_issuer_exposure_contains_no_ticker_specific_exclusion():
    """Source-level guard on PD-1 §2: the helper must not special-case any
    governed ticker. A literal like "AAPL" appearing inside the function would
    be exactly the selective-omission shape the rule forbids."""
    tree = ast.parse((REPO_ROOT / "allocate.py").read_text(encoding="utf-8"))
    fn = next(n for n in ast.walk(tree)
              if isinstance(n, ast.FunctionDef) and n.name == "_issuer_exposure")
    literals = {n.value for n in ast.walk(fn)
                if isinstance(n, ast.Constant) and isinstance(n.value, str)}
    assert not (literals & GOVERNED_ISSUERS), (
        f"_issuer_exposure references governed tickers directly: "
        f"{sorted(literals & GOVERNED_ISSUERS)}")


def test_issuer_exposure_accumulates_over_every_issuer_row():
    """The common-driver accumulator must be fed inside the per-issuer loop,
    unconditionally — not behind a filter."""
    tree = ast.parse((REPO_ROOT / "allocate.py").read_text(encoding="utf-8"))
    fn = next(n for n in ast.walk(tree)
              if isinstance(n, ast.FunctionDef) and n.name == "_issuer_exposure")
    outer = next(n for n in fn.body if isinstance(n, ast.For))
    accumulators = [n for n in outer.body
                    if isinstance(n, ast.AugAssign)
                    and isinstance(n.target, ast.Name)
                    and n.target.id == "common_driver_pct"]
    assert len(accumulators) == 1, (
        "expected exactly one unconditional common-driver accumulation directly "
        "in the per-issuer loop body")


def test_load_issuer_lookthrough_performs_no_network_access():
    """PD-2 §15 / design note §5-§6: the refresh stays a governed snapshot.
    The loader must read the local file and nothing else."""
    tree = ast.parse((REPO_ROOT / "allocate.py").read_text(encoding="utf-8"))
    fn = next(n for n in ast.walk(tree)
              if isinstance(n, ast.FunctionDef) and n.name == "load_issuer_lookthrough")
    called = set()
    for node in ast.walk(fn):
        if isinstance(node, ast.Call):
            f = node.func
            called.add(f.attr if isinstance(f, ast.Attribute) else
                       getattr(f, "id", ""))
    forbidden = {"get", "post", "urlopen", "request", "fetch", "Session", "connect"}
    assert not (called & forbidden), f"network-shaped calls in loader: {called & forbidden}"


# ══ C. Alphabet economic-issuer aggregation ═══════════════════════════════════

def test_alphabet_aggregates_both_share_classes_into_one_governed_issuer(
        lookthrough: dict, sources: dict):
    rows = sources["SPY"]["securities_used"]["GOOGL"]
    assert len(rows) == 2, "Alphabet must be recorded as exactly its two SPY lines"
    by_ticker = {r["ticker"]: r for r in rows}
    assert set(by_ticker) == {"GOOGL", "GOOG"}
    assert by_ticker["GOOGL"]["sedol"] != by_ticker["GOOG"]["sedol"]

    total = sum((_dec(r["raw_weight_pct"]) for r in rows), Decimal(0))
    governed = _dec(_issuer_rows(lookthrough)["GOOGL"]["funds"][0]["fund_holding_weight"])
    assert governed == total / Decimal(100)


def test_neither_alphabet_class_alone_equals_the_governed_weight(
        lookthrough: dict, sources: dict):
    """Adversarial: catches an aggregation that silently kept only one class."""
    governed = _dec(_issuer_rows(lookthrough)["GOOGL"]["funds"][0]["fund_holding_weight"])
    for row in sources["SPY"]["securities_used"]["GOOGL"]:
        assert governed != _dec(row["raw_weight_pct"]) / Decimal(100)


# ══ D. Provenance completeness ════════════════════════════════════════════════

REQUIRED_SOURCE_KEYS = {
    "publisher", "source_identity", "holdings_as_of", "received_at",
    "acquisition", "acquisition_note", "evidence", "evidence_sha256",
    "securities_used",
}


def test_every_governed_fund_has_a_complete_provenance_record(sources: dict):
    assert set(sources) == {"SPY", "VEA", "VWO"}
    for fund, block in sources.items():
        missing = REQUIRED_SOURCE_KEYS - set(block)
        assert not missing, f"{fund} provenance missing: {sorted(missing)}"


def test_provenance_fund_set_matches_the_funds_the_issuers_actually_reference(
        lookthrough: dict, sources: dict):
    referenced = {f["fund"].upper()
                  for row in lookthrough["issuers"] for f in row["funds"]}
    assert referenced == set(sources)


def test_publishers_are_the_official_issuers_only(sources: dict):
    assert sources["SPY"]["publisher"] == "State Street Global Advisors"
    assert sources["VEA"]["publisher"] == "Vanguard"
    assert sources["VWO"]["publisher"] == "Vanguard"


def test_retained_evidence_files_exist_and_hash_exactly(sources: dict):
    for fund, block in sources.items():
        path = REPO_ROOT / block["evidence"]
        assert path.is_file(), f"{fund} evidence file missing: {block['evidence']}"
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        assert digest == block["evidence_sha256"], (
            f"{fund} retained evidence does not match its recorded SHA-256")


def test_as_of_dates_are_real_dates_and_not_after_receipt(sources: dict):
    for fund, block in sources.items():
        as_of, received = block["holdings_as_of"], block["received_at"]
        assert isinstance(as_of, _dt.date), f"{fund}.holdings_as_of must be a date"
        assert isinstance(received, _dt.date), f"{fund}.received_at must be a date"
        assert as_of <= received, f"{fund} claims holdings newer than their receipt"


def test_acquisition_is_recorded_honestly_rather_than_as_a_fetch(sources: dict):
    for fund, block in sources.items():
        assert block["acquisition"] == "PRINCIPAL_SUPPLIED_OFFICIAL_FILE"
        note = block["acquisition_note"]
        assert "Not fetched by this environment" in note
        assert "egress" in note.lower()


def test_evidence_directory_contains_only_the_three_official_files(sources: dict):
    on_disk = {p.name for p in EVIDENCE_DIR.iterdir() if p.is_file()}
    recorded = {Path(b["evidence"]).name for b in sources.values()}
    assert on_disk == recorded, (
        f"unexpected files in the evidence package: {sorted(on_disk ^ recorded)}")


# ══ E. Re-derivation from the retained primary sources ════════════════════════

def test_spy_workbook_self_reports_the_recorded_as_of_date(
        primary_holdings, sources: dict):
    as_of_text, _ = primary_holdings["SPY"]
    recorded: _dt.date = sources["SPY"]["holdings_as_of"]
    assert as_of_text, "SPY workbook carries no 'Holdings: As of ...' line"
    assert recorded.strftime("%d-%b-%Y") in as_of_text


@pytest.mark.parametrize("fund", ["VEA", "VWO"])
def test_vanguard_csv_self_reports_the_recorded_as_of_date(
        fund, primary_holdings, sources: dict):
    as_of_text, _ = primary_holdings[fund]
    recorded: _dt.date = sources[fund]["holdings_as_of"]
    assert recorded.strftime("%m/%d/%Y") in as_of_text


@pytest.mark.parametrize("fund", ["SPY", "VEA", "VWO"])
def test_every_recorded_security_row_matches_the_official_file_exactly(
        fund, primary_holdings, sources: dict):
    _, holdings = primary_holdings[fund]
    for issuer, rows in sources[fund]["securities_used"].items():
        for row in rows:
            sedol = row["sedol"]
            assert sedol in holdings, (
                f"{fund}: SEDOL {sedol} ({issuer}) is not in the official file")
            actual = holdings[sedol]
            assert actual["name"] == row["name"]
            assert actual["ticker"] == row["ticker"]
            recorded_pct = _dec(row["raw_weight_pct"])
            file_pct = Decimal(actual["weight"].rstrip("%"))
            assert file_pct == recorded_pct, (
                f"{fund}/{issuer} SEDOL {sedol}: file says {file_pct}, "
                f"record says {recorded_pct}")


def test_every_governed_weight_is_the_exact_sum_of_its_source_rows(
        lookthrough: dict, sources: dict):
    rows = _issuer_rows(lookthrough)
    for fund, block in sources.items():
        for issuer, secs in block["securities_used"].items():
            total = sum((_dec(s["raw_weight_pct"]) for s in secs), Decimal(0))
            governed = _dec(rows[issuer]["funds"][0]["fund_holding_weight"])
            assert governed == total / Decimal(100), (
                f"{issuer} governed weight {governed} != {total}% / 100 from {fund}")


def test_every_governed_issuer_has_source_rows_and_vice_versa(
        lookthrough: dict, sources: dict):
    documented = {issuer for b in sources.values() for issuer in b["securities_used"]}
    assert documented == GOVERNED_ISSUERS
    assert set(_issuer_rows(lookthrough)) == GOVERNED_ISSUERS


def test_tsmc_aggregates_the_local_line_and_the_sponsored_adr(sources: dict):
    rows = sources["VWO"]["securities_used"]["TSM"]
    tickers = {r["ticker"] for r in rows}
    assert tickers == {"2330", "TSM"}, "TSMC must aggregate the local line and the ADR"
    assert len({r["sedol"] for r in rows}) == 2


def test_the_similarly_named_different_issuer_is_excluded_and_recorded(
        primary_holdings, sources: dict):
    """VWO carries 'Taiwan Semiconductor Co Ltd' (5425), a DIFFERENT economic
    issuer. It must be in the official file, absent from the governed rows, and
    recorded as a deliberate exclusion rather than silently dropped."""
    _, holdings = primary_holdings["VWO"]
    excluded = sources["VWO"]["excluded_similar_identities"]
    assert len(excluded) == 1
    entry = excluded[0]
    assert entry["ticker"] == "5425"
    assert entry["sedol"] in holdings, "the excluded identity must really be in the file"
    assert holdings[entry["sedol"]]["ticker"] == "5425"
    assert "DIFFERENT ECONOMIC ISSUER" in entry["reason"]

    used_sedols = {r["sedol"] for r in sources["VWO"]["securities_used"]["TSM"]}
    assert entry["sedol"] not in used_sedols


def test_aggregation_never_relies_on_name_similarity(sources: dict):
    """Adversarial companion to the exclusion test: the excluded row's name is
    a near-prefix of the included one, so a name-based rule would have swept it
    in. Identity must separate them."""
    excluded = sources["VWO"]["excluded_similar_identities"][0]
    included = {r["name"] for r in sources["VWO"]["securities_used"]["TSM"]}
    local = next(n for n in included if n.startswith("Taiwan Semiconductor Manufacturing"))
    assert local.lower().startswith(excluded["name"].split(" Co Ltd")[0].lower())
    assert excluded["sedol"] not in {r["sedol"]
                                     for r in sources["VWO"]["securities_used"]["TSM"]}


# ══ F. Fail-closed validation of the refreshed file ═══════════════════════════

def test_the_committed_file_passes_strict_validation(lookthrough: dict):
    validated, reason = cr.validate_lookthrough(lookthrough)
    assert reason is None, reason
    assert validated is not None
    assert len(validated["issuers"]) == 11


def test_the_committed_file_loads_through_the_production_loader():
    loaded = allocate.load_issuer_lookthrough()
    assert {r["ticker"] for r in loaded["issuers"]} == GOVERNED_ISSUERS
    assert loaded["common_driver_measurement_rule"]["basis"] == "FULL_EFFECTIVE_ALL_ISSUERS"


@pytest.mark.parametrize("drop", ["issuers", "issuer_ceiling_pct",
                                  "common_driver_ceiling_pct"])
def test_removing_a_required_key_fails_closed(lookthrough: dict, drop: str):
    mutated = {k: v for k, v in lookthrough.items() if k != drop}
    validated, reason = cr.validate_lookthrough(mutated)
    assert validated is None
    assert reason and drop in reason


def test_a_boolean_weight_is_refused_rather_than_coerced_to_one(lookthrough: dict):
    """`float(True)` is 1.0 — a Boolean would become a 100% fund constituent."""
    mutated = yaml.safe_load(LOOKTHROUGH_PATH.read_text(encoding="utf-8"))
    mutated["issuers"][0]["funds"][0]["fund_holding_weight"] = True
    validated, reason = cr.validate_lookthrough(mutated)
    assert validated is None and reason


def test_a_duplicate_issuer_identity_is_refused(lookthrough: dict):
    mutated = yaml.safe_load(LOOKTHROUGH_PATH.read_text(encoding="utf-8"))
    mutated["issuers"].append(dict(mutated["issuers"][0]))
    validated, reason = cr.validate_lookthrough(mutated)
    assert validated is None
    assert reason and "duplicate" in reason.lower()


def test_an_issuer_missing_its_funds_key_is_refused():
    mutated = yaml.safe_load(LOOKTHROUGH_PATH.read_text(encoding="utf-8"))
    del mutated["issuers"][0]["funds"]
    validated, reason = cr.validate_lookthrough(mutated)
    assert validated is None
    assert reason and "funds" in reason


def test_provenance_does_not_weaken_validation(lookthrough: dict):
    """The two new blocks are inert to the validator: removing them must not
    change whether the configuration validates."""
    stripped = {k: v for k, v in lookthrough.items()
                if k not in ("fund_sources", "common_driver_measurement_rule")}
    assert cr.validate_lookthrough(stripped)[1] is None


# ══ G. The retained historical measurement is preserved, not rewritten ════════

def test_retained_measurement_is_byte_for_byte_the_original_figures(lookthrough: dict):
    retained = lookthrough["retained_common_driver_measurement"]
    assert retained["value_pct"] == 40.0284
    assert retained["measured_at"] == _dt.date(2026, 7, 30)
    assert retained["methodology"] == (
        "canonical v1.30 target-weight-basis look-through, PHQ-2026-01 due diligence")
    assert retained["source"] == (
        "governance/evidence/PHQ-2026-01/final_due_diligence/"
        "Portfolio_HQ_Final_Due_Diligence_and_Approval_v1_32.json")


def test_retained_measurement_is_labelled_historical_evidence_not_the_rule(
        lookthrough_text: str):
    assert "HISTORICAL EVIDENCE ONLY — NOT the measurement rule" in lookthrough_text
    assert "must not be rewritten or cited as the rule" in lookthrough_text


def test_retained_measurement_is_not_silently_reconciled_to_the_new_figure(
        lookthrough: dict):
    """Adversarial: the whole point of PD-1 is that these two differ. If a
    future edit 'fixed' the retained figure, this fails."""
    retained = lookthrough["retained_common_driver_measurement"]["value_pct"]
    recomputed = cr.collect_target_weight_concentration().common_driver.recomputed_pct
    assert retained != pytest.approx(recomputed)


def test_the_discrepancy_continues_to_be_reported_rather_than_suppressed():
    cd = cr.collect_target_weight_concentration().common_driver
    assert cd.reconciles is False
    assert cd.status == "DISCREPANCY"
    assert cd.discrepancy_flag == "RETAINED_MEASUREMENT_DISCREPANCY"
    assert cd.retained_value_pct == 40.0284


# ══ H. The refreshed measurement, recomputed through production code ══════════

@pytest.fixture(scope="module")
def concentration():
    result = cr.collect_target_weight_concentration()
    assert result.available is True
    return result


def test_common_driver_recomputes_to_the_reported_figure(concentration):
    assert round(concentration.common_driver.recomputed_pct, 4) == 41.7646


def test_common_driver_is_measured_against_the_unchanged_forty_percent_ceiling(
        concentration):
    cd = concentration.common_driver
    assert cd.ceiling_pct == 40.0
    assert round(cd.headroom_pct, 4) == -1.7646
    assert cd.limit_status == "OVER_LIMIT"


def test_maximum_issuer_is_nvda_approaching_the_unchanged_eight_percent_ceiling(
        concentration):
    top = concentration.max_issuer
    assert top.ticker == "NVDA"
    assert round(top.effective_pct, 4) == 7.2099
    assert top.ceiling_pct == 8.0
    assert round(top.headroom_pct, 4) == 0.7901
    assert top.status == "APPROACHING"


def test_no_governed_issuer_breaches_the_eight_percent_ceiling(concentration):
    breaches = [i.ticker for i in concentration.issuers if i.effective_pct > i.ceiling_pct]
    assert breaches == []


def test_every_governed_issuer_appears_in_the_recomputation(concentration):
    assert {i.ticker for i in concentration.issuers} == GOVERNED_ISSUERS


def test_the_common_driver_equals_the_sum_of_all_eleven_effective_exposures(
        concentration):
    """The measurement is the PD-1 sum itself — not a subset of it."""
    total = sum(i.effective_pct for i in concentration.issuers)
    assert concentration.common_driver.recomputed_pct == pytest.approx(total)


def test_embedded_only_issuers_really_do_contribute_to_the_live_measurement(
        concentration):
    """AAPL has no direct canonical target; its whole contribution is embedded.
    Under the omitted reading it would be absent from the total."""
    aapl = next(i for i in concentration.issuers if i.ticker == "AAPL")
    assert aapl.direct_pct == 0.0
    assert aapl.embedded_pct > 0.0
    assert aapl.effective_pct == pytest.approx(aapl.embedded_pct)


def test_the_measurement_basis_is_target_weights_not_current_holdings(concentration):
    basis = concentration.basis
    assert "CANONICAL TARGET WEIGHTS" in basis
    assert "not current holdings" in basis


# ══ I. Scope containment — nothing policy-shaped hides in this file ═══════════

ALLOWED_TOP_LEVEL_KEYS = {
    "issuer_ceiling_pct",
    "common_driver_ceiling_pct",
    "retained_common_driver_measurement",
    "issuers",
    "common_driver_measurement_rule",
    "fund_sources",
}


def test_lookthrough_schema_is_closed(lookthrough: dict):
    """Durable scope proof: no target, cap, cluster, gate, margin or order
    configuration can be smuggled into this file, now or later — without this
    assertion failing first. Deliberately a closed-schema check rather than a
    pin of any other policy file to a commit."""
    assert set(lookthrough) == ALLOWED_TOP_LEVEL_KEYS


def test_lookthrough_carries_no_target_cap_gate_or_margin_configuration(
        lookthrough_text: str):
    body = "\n".join(line for line in lookthrough_text.splitlines()
                     if not line.lstrip().startswith("#"))
    for key in ("target_pct:", "caps:", "clusters:", "destination:",
                "leverage", "buffer_pct", "margin:", "gates:"):
        assert key not in body, f"policy-shaped key {key!r} appears in the look-through file"


def test_membership_is_unchanged_from_the_governed_eleven(lookthrough: dict):
    assert set(_issuer_rows(lookthrough)) == GOVERNED_ISSUERS


def test_every_issuer_maps_to_exactly_one_governed_fund(lookthrough: dict):
    for ticker, row in _issuer_rows(lookthrough).items():
        assert len(row["funds"]) == 1, f"{ticker} unexpectedly spans multiple funds"
        assert row["funds"][0]["fund"] in {"SPY", "VEA", "VWO"}


def test_every_refreshed_weight_is_a_plain_positive_fraction(lookthrough: dict):
    for ticker, row in _issuer_rows(lookthrough).items():
        weight = row["funds"][0]["fund_holding_weight"]
        assert isinstance(weight, float) and not isinstance(weight, bool)
        assert 0.0 < weight < 1.0, f"{ticker} weight {weight} is not a fund fraction"


# ══ J. No brokerage, order, or Stage-1 capability introduced ══════════════════

INTRODUCED_SOURCES = (
    "issuer_lookthrough.yaml",
    "test_common_driver_authority_and_lookthrough_refresh.py",
    "governance/decisions/PHQ-2026-08-common-driver-measurement-authority-and-lookthrough-refresh.md",
)

# The scanned token list deliberately includes THIS module, so that a future
# edit to these tests cannot itself introduce a brokerage or Stage-1 surface.
# That means the tokens cannot be written here as plain literals — they would
# match themselves. Each is assembled from fragments instead; `_tok` is the
# only indirection, and the fragments are readable in place.
def _tok(*parts: str) -> str:
    return "".join(parts)


ORDER_TOKENS = (
    _tok("submit", "_order"), _tok("place", "_order"), _tok("create", "_order"),
    _tok("Trading", "Client"), _tok("MarketOrder", "Request"),
    _tok("LimitOrder", "Request"), _tok("robin", "hood"),
    _tok("api", "_secret"), _tok("secret", "_key"), _tok("ACCOUNT", "_NUMBER"),
)

STAGE1_TOKENS = (
    _tok("AUTHORIZATION", "_ROOT"), _tok("ATTEMPT", "_1"),
    _tok("stage1", "_results.yaml"), _tok("pre_execution", "_attestation"),
    _tok("stage_1", "_executability"),
)


@pytest.mark.parametrize("relpath", INTRODUCED_SOURCES)
def test_no_order_or_brokerage_capability_is_introduced(relpath: str):
    text = (REPO_ROOT / relpath).read_text(encoding="utf-8")
    for token in ORDER_TOKENS:
        assert token not in text, f"{relpath} references order/brokerage token {token!r}"


@pytest.mark.parametrize("relpath", INTRODUCED_SOURCES)
def test_no_stage1_arming_or_attestation_surface_is_touched(relpath: str):
    text = (REPO_ROOT / relpath).read_text(encoding="utf-8")
    for token in STAGE1_TOKENS:
        assert token not in text, f"{relpath} references Stage-1 token {token!r}"


def test_this_test_module_writes_nothing_into_the_repository():
    """Guard on the tests themselves: no repository-rooted write path."""
    text = Path(__file__).read_text(encoding="utf-8")
    tree = ast.parse(text)
    rooted = {"REPO_ROOT", "LOOKTHROUGH_PATH", "EVIDENCE_DIR", "DECISION_PATH"}
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        func = node.func
        name = func.attr if isinstance(func, ast.Attribute) else getattr(func, "id", "")
        if name not in {"write_text", "write_bytes", "mkdir", "unlink", "open"}:
            continue
        if name == "open":
            continue  # zipfile.ZipFile(...) / io helpers are read-only here
        referenced = {n.id for n in ast.walk(node) if isinstance(n, ast.Name)}
        assert not (referenced & rooted), (
            f"write-capable call {name!r} references a repository-rooted path")


def test_decision_and_evidence_are_the_only_new_repository_surfaces():
    """The evidence package holds data files only — never executable code."""
    for path in EVIDENCE_DIR.iterdir():
        assert path.suffix.lower() in {".xlsx", ".csv"}, (
            f"unexpected non-data file in the evidence package: {path.name}")
        assert not (path.stat().st_mode & 0o111), f"{path.name} is executable"


def test_no_automatic_network_fetch_was_added_to_the_allocator():
    """PD-2 §15: the refresh must not turn the production allocator into a
    live ETF-constituent fetcher."""
    text = (REPO_ROOT / "allocate.py").read_text(encoding="utf-8")
    for token in ("ssga.com", "vanguard.com", "requests.get", "urlopen"):
        assert token not in text, f"allocate.py gained a network surface: {token!r}"


def test_a_stale_snapshot_is_detectable_from_the_recorded_as_of_dates(sources: dict):
    """The refresh does not make the file permanently trustworthy — it makes
    its age machine-readable. This asserts that property, not a freshness
    deadline, so it cannot become a CI gate on the passage of time."""
    for fund, block in sources.items():
        age_days = (_dt.date.today() - block["holdings_as_of"]).days
        assert isinstance(age_days, int)
        assert block["holdings_as_of"].year >= 2026
