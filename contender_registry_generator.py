"""
contender_registry_generator.py — deterministic generator for
`intelligence/contenders/registry.yaml`, implementing the future
implementation unit `governance/decisions/CONTENDER-0002-contender-normalization-and-readiness-screening-authorization.md`
authorizes: `XASSET-0001` §J step 1, "contender normalization plus
research-readiness screening" (`WS-0014` objective items (1)+(2) together).

MECHANICAL SCREENING ONLY. This module never researches, classifies, ranks,
recommends, revives, targets, tiers, allocates, buys, trims, sells, or
trades any asset (CONTENDER-0002 §M). It reports what already-governed
repository sources already say, through the disposition/flag model CONTENDER-0002
§E defines, and never harmonizes conflicting facts into a new investment
conclusion of its own (§H.3).

── Source set (CONTENDER-0002 §B, sixteen categories) ──────────────────────

Sixteen role-tagged categories, `discovery` / `corroboration` / `context`,
are scanned. This generator additionally scans **CLAUDE.md as a disclosed
17th source** (`discovery` role) — not one of CONTENDER-0002's own sixteen
named categories, but squarely within its "at minimum" framing (§B: "must
mechanically inventory ticker-shaped references from, at minimum, the
following sixteen categories") and within `CONTENDER-0001` §A's own
eligibility language, which explicitly names "a prior holding" and "other
governed project reference" as eligible provenance. Two genuine prior
holdings this repository has fully exited (VMC, LHX) and one prior crypto
target (HYPE) are recorded **only** in CLAUDE.md's own Standing Queue /
Decisions Log text, in no `governance/decisions/*.md`, audit, or other §B
source this session could find — omitting CLAUDE.md would silently miss
instruments CONTENDER-0001 itself names as eligible. This extension is
disclosed here and in the retained audit artifact, not silently assumed;
it is a narrow, single-document addition, not a redesign of §B's source
set, and is a proportionate response to a mechanically observed gap rather
than a §K.2 "materially incomplete source-set" halt condition.

── Structured vs. prose discovery ───────────────────────────────────────────

Structured sources (targets.yaml, gates.yaml, holdings.yaml,
issuer_lookthrough.yaml, intelligence/companies filenames,
intelligence/relationships filenames, intelligence/classification filenames
[context only, §D], earnings.py's alias map, governance/evidence/CHART-0002
package identities) are parsed programmatically — fully mechanical, fully
reproducible from the same source commit.

Prose sources (governance/decisions/*.md, governance/audits/*.md,
intelligence/BATCH*_COMPARISON.md, decision_log.yaml, research/**/*.md
excluding the sealed untouched_sealed/ directory, operations/WORKSTREAMS.yaml,
CLAUDE.md) are scanned with a deterministic ticker-shaped-token regex. Every
raw token surviving that regex is then classified exactly one of three ways,
with no silent middle ground:

1. already a known anchor (found in a structured source) — recorded as
   `corroboration` provenance on that symbol's existing entry, never a
   second entry;
2. present in `_PROSE_DISCOVERIES` below — a small, explicit, individually
   cited table this session built by directly reading every prose source
   category and manually verifying context (not guessed) — becomes a new
   registry entry;
3. anything else — auto-excluded as a repository-specific acronym/
   decision-ID/structural-token false-positive prose match (CONTENDER-0002
   §J's own named exclusion-reason category), recorded in the retained
   audit's exclusion log, never silently dropped and never force-fit into a
   registry entry.

**Disclosed limitation**, not a hidden gap: bucket 3's auto-exclusion is a
blanket rule, not a per-token manual review — on a future regeneration
against a materially changed `main`, a genuinely new ticker-shaped mention
that is not yet in `_PROSE_DISCOVERIES` would be auto-excluded rather than
surfaced. This session verified, by direct inspection, that every non-
anchor token found in the CURRENT prose corpus is correctly classified by
one of buckets 2 or 3 (see the retained audit's full token inventory) — the
limitation applies to *future* regenerations, not to this generation's own
completeness. A future implementation extending coverage should re-run the
raw-token scan and manually re-triage bucket 3 before trusting it blind.

── Determinism scope (§I) and clone-depth handling (§G) ────────────────────

The sixteen-plus-one *ordinary* source categories require no git history —
they read tree content at `source_commit_sha` only, so the portion of
`entries` they produce is fully reproducible byte-for-byte (excluding
`generated_at`) regardless of which environment performs the generation.

**§G step 2 legacy recovery is a disclosed, intentional, environment-
dependent exception to that guarantee — for BOTH `legacy_gap` and,
potentially, `entries` itself.** `detect_clone_depth()` below reports the
*executing environment's* own live git clone depth, every generation — a
shallow local development clone and a `fetch-depth: 0` CI checkout of the
identical source commit correctly report `"shallow"` and `"complete"`
respectively. When `"complete"`, `perform_legacy_recovery()` ALWAYS
attempts §G step 2's mandatory bounded, mechanical diff of `holdings.yaml`
across the PHQ-2026-02 reconciliation commit — a genuinely conditional
requirement, not skipped or deferred. If that attempt succeeds, every
mechanically-recovered legacy ticker becomes a real, fully-dispositioned
registry entry (routed through the same §E.2 precedence engine as every
other discovered identity) — meaning `entries` itself can legitimately
differ between a shallow environment (recovery impossible, no legacy
entries added) and a complete environment (recovery attempted; zero or
more legacy entries added, depending on what the mechanical diff actually
finds). This is not a determinism *defect*: git-history reachability is
genuinely environment-dependent runtime state, not part of the tree
content the rest of this registry is built from, and §G's own text
requires the live re-verification and, where reachable, the attempt,
rather than trusting or skipping based on a prior finding. Every recovery
outcome fails closed to an honest `recovery_ambiguous` (zero entries
added, `registry_entries_created: 0`) rather than guessing, whenever the
reconciliation commit, a single resolvable parent, or a non-empty diff
cannot be mechanically established — see `perform_legacy_recovery()`'s own
docstring for the exact conditions.
"""

from __future__ import annotations

import re
import subprocess
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path

import yaml

import intelligence_report as _ir

SCHEMA_VERSION = 1

# ── §B source labels (must match contender_registry_validator.AUTHORIZED_SOURCE_LABELS) ──

SRC_TARGETS = "targets.yaml"
SRC_GATES = "gates.yaml"
SRC_HOLDINGS = "holdings.yaml"
SRC_ISSUER_LOOKTHROUGH = "issuer_lookthrough.yaml"
SRC_COMPANIES = "intelligence/companies"
SRC_THEMES = "intelligence/themes"
SRC_RELATIONSHIPS = "intelligence/relationships"
SRC_CLASSIFICATION = "intelligence/classification"
SRC_DECISIONS = "governance/decisions"
SRC_WORKSTREAMS = "operations/WORKSTREAMS.yaml"
SRC_BATCH = "intelligence/BATCH_COMPARISON"
SRC_AUDITS = "governance/audits"
SRC_DECISION_LOG = "decision_log.yaml"
SRC_RESEARCH = "research_protocols"
SRC_EARNINGS = "earnings.py"
SRC_CHART = "governance/evidence/CHART-0002"
SRC_CLAUDE_MD = "CLAUDE.md"  # disclosed 17th source, see module docstring


def _prov(source: str, role: str) -> dict:
    return {"source": source, "role": role}


# ── §E.2 twelve-value closed vocabulary (re-imported for a single source of truth) ──

from contender_registry_validator import (  # noqa: E402
    CLONE_DEPTH_VALUES,
    PRIMARY_DISPOSITIONS_IN_PRECEDENCE_ORDER,
    RECOVERY_STATUS_VALUES,
)


# ── §G: clone-depth detection, live and environment-independent ────────────
#
# The executing environment's git clone depth is RUNTIME INPUT, never a
# repository invariant — this session's own local clone happens to be
# shallow, but a different environment generating from the identical source
# commit (e.g. GitHub Actions' `actions/checkout@v4` with `fetch-depth: 0`,
# used by this repository's own CI) legitimately sees a complete clone.
# `build_registry()` must detect this live, every generation, never assume
# or hardcode a prior finding as still current (§G step 1's own explicit
# re-verification requirement). `CLONE_DEPTH_VALUES`/`RECOVERY_STATUS_VALUES`
# are defined in contender_registry_validator.py (the schema authority) and
# imported here — see that module's own comment for the full vocabulary
# rationale.


def detect_clone_depth(repo_root: Path, *, runner=None) -> str:
    """Live, mechanical clone-depth detection (CONTENDER-0002 §G step 1).
    Returns exactly one of CLONE_DEPTH_VALUES — never a hardcoded
    assumption. `runner`, if supplied, replaces the actual `git` subprocess
    call for testability (dependency injection): it must accept
    `(args, cwd=..., text=...)` the same way `subprocess.check_output`
    does, and return the raw stdout string. Without `runner`, this calls
    the real `git rev-parse --is-shallow-repository` against `repo_root`."""
    run = runner if runner is not None else subprocess.check_output
    out = run(["git", "rev-parse", "--is-shallow-repository"], cwd=str(repo_root), text=True).strip()
    if out == "true":
        return "shallow"
    if out == "false":
        return "complete"
    raise ValueError(
        f"unexpected `git rev-parse --is-shallow-repository` output: {out!r} "
        f"(expected exactly 'true' or 'false')"
    )


def _legacy_gap_record(clone_depth: str, recovery_status: str, registry_entries_created: int) -> dict:
    """§G's exact required record shape. `registry_entries_created` is 0
    for every non-recovery outcome (§G: 'no placeholder or invented ticker
    row may be created for any UNRECOVERED legacy symbol') and equals the
    real, mechanically-diffed count when recovery succeeded — never
    invented, never a round number."""
    if clone_depth not in CLONE_DEPTH_VALUES:
        raise ValueError(f"clone_depth must be one of {sorted(CLONE_DEPTH_VALUES)} — got {clone_depth!r}")
    return {
        "known_unenumerated_legacy_gap": True,
        "reported_count": "approximately 41",
        "source_authority": "PHQ-2026-02",
        "clone_depth_at_generation": clone_depth,
        "recovery_status": recovery_status,
        "registry_entries_created": registry_entries_created,
        "next_action": (
            "none required for the recovered identities themselves — each carries its own "
            "ordinary next_required_action; if the recovered count differs from the originally "
            "reported ~41, that reflects this mechanical diff's own actual result at the one "
            "reconciliation boundary it checked, not an additional unresolved gap"
            if registry_entries_created > 0
            else "separately_authorized_history_recovery_sub_unit"
        ),
    }


def find_phq_2026_02_reconciliation_commit(repo_root: Path, *, runner=None) -> tuple[str | None, str | None]:
    """§G step 2: mechanically locate "the PHQ-2026-02 reconciliation
    commit" — the commit that performed PHQ-2026-02's holdings.yaml
    reconciliation — by searching reachable commit history for a commit
    whose own subject line names PHQ-2026-02 and which touched
    `holdings.yaml`, matching this repository's own consistent commit-
    message convention of prefixing decision-implementing commits with
    their governing decision ID (verified against real committed history,
    e.g. "PHQ-2026-06: cash-only factual sync..."). History is walked
    oldest-first so the *original* reconciliation commit is found, not a
    later commit that merely mentions PHQ-2026-02 in passing. Returns
    `(commit_sha, parent_sha)`; returns `(None, None)` if no matching
    commit is found, or `(commit_sha, None)` if the match has zero or more
    than one parent (a root or merge commit — no single unambiguous
    "before" state to diff against) — in both non-resolvable cases the
    caller must fail closed, never guess."""
    run = runner if runner is not None else subprocess.check_output
    log = run(
        ["git", "log", "--reverse", "--format=%H%x1f%P%x1f%s", "--", "holdings.yaml"],
        cwd=str(repo_root), text=True,
    )
    for line in log.splitlines():
        parts = line.split("\x1f")
        if len(parts) != 3:
            continue
        commit_sha, parents_field, subject = parts
        if "PHQ-2026-02" in subject:
            parents = parents_field.split()
            if len(parents) == 1:
                return commit_sha, parents[0]
            return commit_sha, None  # root or merge commit — ambiguous parent, fail closed
    return None, None


def diff_holdings_tickers_across_commit(
    repo_root: Path, commit_sha: str, parent_sha: str, *, runner=None,
) -> list[tuple[str, str]]:
    """§G step 2's own "bounded, mechanical diff of holdings.yaml" —
    tickers present in `shares:`/`crypto_shares:` at `parent_sha` but
    absent at `commit_sha` (PHQ-2026-02's own disclosed "removed, not
    zeroed" reconciliation shape). Propagates any exception from a failed
    `git show` or unparseable YAML — callers must treat that as
    `recovery_ambiguous`, never guess a partial result."""
    run = runner if runner is not None else subprocess.check_output
    before = yaml.safe_load(run(["git", "show", f"{parent_sha}:holdings.yaml"], cwd=str(repo_root), text=True)) or {}
    after = yaml.safe_load(run(["git", "show", f"{commit_sha}:holdings.yaml"], cwd=str(repo_root), text=True)) or {}
    removed: list[tuple[str, str]] = []
    for key, asset_type in (("shares", "equity"), ("crypto_shares", "crypto")):
        before_syms = set((before.get(key) or {}).keys())
        after_syms = set((after.get(key) or {}).keys())
        for sym in sorted(before_syms - after_syms):
            removed.append((sym, asset_type))
    return removed


def perform_legacy_recovery(
    repo_root: Path, clone_depth: str, *, runner=None,
) -> tuple[list[tuple[str, str, str]], dict]:
    """CONTENDER-0002 §G steps 2-3, orchestrated. Returns
    `(recovered, legacy_gap)`. `recovered` is a list of
    `(canonical_symbol, asset_type, provenance_note)` raw mechanical-fact
    tuples — no disposition is assigned here; `build_registry()` routes
    every recovered symbol through the same §E.2 precedence engine as
    every other discovered identity, so a symbol that happens to already
    carry other governed evidence (e.g. it was later re-added and already
    has a Company Intelligence record) is never incorrectly forced into a
    disposition this function would have guessed. `recovered` is empty
    unless `clone_depth == "complete"` AND the reconciliation commit AND a
    single resolvable parent were both found AND the diff itself found at
    least one removed ticker without raising. Every recovered tuple's own
    provenance note carries the real git commit SHAs — never guessed,
    never a placeholder. When `clone_depth == "shallow"`, or when any step
    fails to resolve unambiguously, this fails closed to an honest
    `recovery_ambiguous`/`unavailable_in_current_clone` gap record with
    zero recovered entries — matching §G step 3's own "stop and disclose"
    instruction."""
    if clone_depth not in CLONE_DEPTH_VALUES:
        raise ValueError(f"clone_depth must be one of {sorted(CLONE_DEPTH_VALUES)} — got {clone_depth!r}")

    if clone_depth == "shallow":
        return [], _legacy_gap_record("shallow", "unavailable_in_current_clone", 0)

    commit_sha, parent_sha = find_phq_2026_02_reconciliation_commit(repo_root, runner=runner)
    if commit_sha is None or parent_sha is None:
        return [], _legacy_gap_record("complete", "recovery_ambiguous", 0)

    try:
        removed = diff_holdings_tickers_across_commit(repo_root, commit_sha, parent_sha, runner=runner)
    except Exception:
        return [], _legacy_gap_record("complete", "recovery_ambiguous", 0)

    if not removed:
        return [], _legacy_gap_record("complete", "recovery_ambiguous", 0)

    note = f"present in holdings.yaml at {parent_sha}, absent at {commit_sha} (the PHQ-2026-02 reconciliation commit)"
    recovered = [(sym, asset_type, note) for sym, asset_type in removed]
    status = f"recovered_{len(recovered)}_of_41"
    return recovered, _legacy_gap_record("complete", status, len(recovered))


@dataclass
class _Entry:
    canonical_symbol: str
    asset_type: str
    primary_disposition: str
    secondary_flags: dict = field(default_factory=dict)
    provenance: list = field(default_factory=list)
    investability_status: str = "investable"
    research_status: str = ""
    evidence_freshness_status: str = "not_applicable"
    classification_status: str = "not_applicable"
    current_policy_status: dict = field(default_factory=dict)
    existing_disposition: str | None = None
    duplicate_of: str | None = None
    reason: str = ""
    review_trigger: str | None = None
    next_required_action: str = ""

    def add_prov(self, source: str, role: str) -> None:
        key = (source, role)
        if key not in {(p["source"], p["role"]) for p in self.provenance}:
            self.provenance.append(_prov(source, role))

    def to_dict(self) -> dict:
        return {
            "canonical_symbol": self.canonical_symbol,
            "asset_type": self.asset_type,
            "primary_disposition": self.primary_disposition,
            "secondary_flags": dict(sorted(self.secondary_flags.items())),
            "provenance": sorted(self.provenance, key=lambda p: (p["source"], p["role"])),
            "investability_status": self.investability_status,
            "research_status": self.research_status,
            "evidence_freshness_status": self.evidence_freshness_status,
            "classification_status": self.classification_status,
            "current_policy_status": dict(sorted(self.current_policy_status.items())),
            "existing_disposition": self.existing_disposition,
            "duplicate_of": self.duplicate_of,
            "reason": self.reason,
            "review_trigger": self.review_trigger,
            "next_required_action": self.next_required_action,
        }


_EMPTY_FLAGS = {
    "has_current_gate": False,
    "has_historical_intelligence": False,
    "has_prior_deferral_superseded": False,
    "freshness_due": False,
    "classification_exists": False,
    "chart_evidence_exists": False,
    "current_holding": False,
    "current_target": False,
}


# ── §C: canonicalization / alias handling ───────────────────────────────────

def load_alias_map(repo_root: Path) -> dict[str, str]:
    """earnings.py's own _YAHOO_SYMBOL map, reused per §C ('must be reused,
    not reinvented'). Maps a non-canonical form -> canonical form."""
    text = (repo_root / "earnings.py").read_text()
    m = re.search(r"_YAHOO_SYMBOL\s*=\s*(\{[^}]*\})", text)
    if not m:
        return {}
    yahoo_to_canonical = {}
    mapping = eval(m.group(1), {"__builtins__": {}})  # noqa: S307 — trusted local repo file, static literal
    for canonical, yahoo_form in mapping.items():
        yahoo_to_canonical[yahoo_form] = canonical
    return yahoo_to_canonical


# ── §B item 5/9: PI-0035's 26-name "retained/historical-advisory/non-current" set,
# read here directly from PI-0035's own committed decision text (a §H.1-permitted
# "existing governed decision's own recorded text" citation), used only to
# populate has_historical_intelligence — never re-derived by guessing. ──────

_PI0035_RETAINED_NAMES = frozenset({
    "AAPL", "ABBV", "AMAT", "AMD", "BRK.B", "CRM", "CRWD", "CVX", "GILD",
    "IBM", "INTC", "JNJ", "JPM", "LRCX", "MA", "MLM", "MRK", "MRVL", "MU",
    "NOW", "ORCL", "SKHY", "VRT", "WDC", "WMT", "XOM",
})

# ── §E.2 tier 7 supersession precedent: PI-0036 (GNRC/RTX) and PI-0038
# (RKLB/TSLA) each narrowly superseded a PI-0033 deferral for research
# purposes only, per each decision's own explicit text (§E.2 tier 7 / §E.4). ──

_PI0033_SUPERSEDED_FOR_RESEARCH = frozenset({"GNRC", "RTX", "RKLB", "TSLA"})

# ── §E.2 tier 11: PI-0038's own text states all six gated-name records
# "disclose their own research session's source-access failure in full" —
# the repository's own explicit, blanket per-record insufficiency finding.
# No other single governance decision makes an equivalent blanket
# insufficiency declaration for any other ticker's own record (individual
# narrower disclosures, e.g. one fact "attempted but not directly
# inspected," do not rise to this bar — see the generator module docstring
# and the retained audit's own LLY discussion for the boundary reasoning). ──

_PI0038_INSUFFICIENT_EVIDENCE = frozenset({"SNPS", "ICE", "SPGI", "WM", "RKLB", "TSLA"})

# ── §B item 9/13: prose-discovered candidates. Every entry here was found
# via the deterministic regex scan (see module docstring), then manually
# verified by directly reading its cited source text before being accepted
# — never guessed. `tier` must be one of the twelve §E.2 values. ───────────

_PROSE_DISCOVERIES: dict[str, dict] = {
    # PI-0033's fourteen individually-reasoned dispositions minus the four
    # (GNRC, RTX, RKLB, TSLA) that already have Company Intelligence
    # coverage and land via the structured scan instead, plus the three
    # restated-unedited deferrals (DHR/SYK per PI-0014, EQIX per PI-0027) —
    # thirteen names, all §E.2 tier 7, unsuperseded as of this scan.
    "CAT": dict(tier="explicitly_deferred_or_excluded", asset_type="equity",
                cite="PI-0033 (governance/decisions/PI-0033-ws0005-milestone3-residual-deferrals.md)"),
    "NFLX": dict(tier="explicitly_deferred_or_excluded", asset_type="equity", cite="PI-0033"),
    "SHOP": dict(tier="explicitly_deferred_or_excluded", asset_type="equity", cite="PI-0033"),
    "UBER": dict(tier="explicitly_deferred_or_excluded", asset_type="equity", cite="PI-0033"),
    "HOOD": dict(tier="explicitly_deferred_or_excluded", asset_type="equity", cite="PI-0033"),
    "DELL": dict(tier="explicitly_deferred_or_excluded", asset_type="equity", cite="PI-0033"),
    "PLTR": dict(tier="explicitly_deferred_or_excluded", asset_type="equity", cite="PI-0033"),
    "SPCX": dict(
        tier="explicitly_deferred_or_excluded", asset_type="equity",
        cite="PI-0033; former targets.yaml/gates.yaml row retired by PHQ-2026-04 after verified manual "
             "exit — PHQ-2026-03 restricts SPCX to 'research candidate only'",
    ),
    "BABA": dict(tier="explicitly_deferred_or_excluded", asset_type="equity",
                 cite="PI-0033 — flagged there for materially longer, particular-care treatment as the "
                      "roster's only foreign private issuer"),
    "UNH": dict(tier="explicitly_deferred_or_excluded", asset_type="equity",
                cite="PI-0029 (excluded from Batch7 biopharmaceuticals on payer-economics-mechanism "
                     "grounds) restated with an explicit reopening trigger by PI-0033"),
    "DHR": dict(tier="explicitly_deferred_or_excluded", asset_type="equity",
                cite="PI-0014 (bounded evidence review), restated unedited by PI-0033"),
    "SYK": dict(tier="explicitly_deferred_or_excluded", asset_type="equity",
                cite="PI-0014 (bounded evidence review), restated unedited by PI-0033"),
    "EQIX": dict(tier="explicitly_deferred_or_excluded", asset_type="equity",
                 cite="PI-0027 (deferred as a data-center-REIT candidate, untested REIT evidence regime), "
                      "restated unedited by PI-0033"),
    # §E.2 tier 2 worked example, verbatim from CONTENDER-0002's own text.
    "QQQ": dict(tier="benchmark_or_index", asset_type="fund",
                cite="targets.yaml's own regime_ticker: QQQ config field ('informational' per its own "
                     "comment); CLAUDE.md's regime-gate/trend-gate backtest Decisions Log entries; absent "
                     "from targets.yaml destination:, holdings.yaml, gates.yaml, and every Intelligence "
                     "record"),
    # §E.2 tier 5's own corrected worked example, verbatim.
    "SNDK": dict(tier="requires_research", asset_type="equity",
                 cite="PI-0032 — explicitly and repeatedly classified as candidate research only, not a "
                      "holding, not authorized for purchase under any circumstance; no prior identity of "
                      "its own (WDC's Feb-2025 spinoff), so not stale_or_superseded per CONTENDER-0002 "
                      "§E.2 tier 5's own corrected text"),
    # Genuine prior holdings/targets, found only in CLAUDE.md (the disclosed
    # 17th source) — explicitly eligible under CONTENDER-0001 §A's "a prior
    # holding" language. The repository's own text records a deliberate
    # exit/removal decision for each, so §E.2 tier 7 applies (a specific,
    # already-made disposition), not tier 9 (no disposition made).
    "VMC": dict(tier="explicitly_deferred_or_excluded", asset_type="equity",
                cite="CLAUDE.md Standing Queue #2 / Decisions Log ('VMC consolidated into MLM, VMC "
                     "exited' — 'redundant sector exposure,' consolidated into MLM 2026-07-13); also named "
                     "in governance/decisions/OPS-0016 ('the VMC->MLM consolidation precedent')"),
    "LHX": dict(tier="explicitly_deferred_or_excluded", asset_type="equity",
                cite="CLAUDE.md Standing Queue #6 ('LHX full exit -- done 2026-07-13, confirmed absent "
                     "from every holdings sync since')"),
    "HYPE": dict(tier="explicitly_deferred_or_excluded", asset_type="crypto",
                 cite="CLAUDE.md Portfolio Doctrine / Standing Queue #5 ('HYPE removed from targets... "
                      "HYPE sold' -- deliberate crypto-sleeve exclusion, July 2026 decision)"),
    "ZORA": dict(tier="explicitly_deferred_or_excluded", asset_type="crypto",
                 cite="CLAUDE.md Standing Queue #5 ('Robinhood's unsellable sub-cent dust (ZORA/WIF/BONK/"
                      "PEPE, $0.00) is display noise -- permanently ignored, never synced')"),
    "WIF": dict(tier="explicitly_deferred_or_excluded", asset_type="crypto", cite="CLAUDE.md Standing Queue #5, same citation as ZORA"),
    "BONK": dict(tier="explicitly_deferred_or_excluded", asset_type="crypto", cite="CLAUDE.md Standing Queue #5, same citation as ZORA"),
    "PEPE": dict(tier="explicitly_deferred_or_excluded", asset_type="crypto", cite="CLAUDE.md Standing Queue #5, same citation as ZORA"),
}


# ── §B: raw ticker-shaped token regex, and the exact source-file set. ──────

_TOKEN_RE = re.compile(r"\b[A-Z]{1,5}(?:[.\-][A-Z]{1,2})?\b")
_DECISION_ID_RE = re.compile(
    r"^(PI|TIER|REL|CHART|OPS|GOV|PHQ|WS|AUTO|LADDER|MARGIN|XASSET|CONTENDER|ONTO|NUM)-?\d"
)


def _prose_source_files(repo_root: Path) -> list[tuple[Path, str, str]]:
    """Returns (path, source_label, role) for every prose source CONTENDER-0002
    §B names (items 9, 10, 11, 12, 13, 14) plus the disclosed 17th (CLAUDE.md)."""
    out: list[tuple[Path, str, str]] = []
    for p in sorted((repo_root / "governance" / "decisions").glob("*.md")):
        out.append((p, SRC_DECISIONS, "discovery"))
    for p in sorted((repo_root / "governance" / "audits").glob("*.md")):
        if p.name == "README.md":
            continue
        out.append((p, SRC_AUDITS, "discovery"))
    for p in sorted((repo_root / "intelligence").glob("BATCH*_COMPARISON.md")):
        out.append((p, SRC_BATCH, "discovery"))
    for p in sorted((repo_root / "research").glob("**/*.md")):
        if "untouched_sealed" in p.parts:
            continue
        out.append((p, SRC_RESEARCH, "discovery"))
    out.append((repo_root / "operations" / "WORKSTREAMS.yaml", SRC_WORKSTREAMS, "discovery"))
    out.append((repo_root / "decision_log.yaml", SRC_DECISION_LOG, "discovery"))
    out.append((repo_root / "CLAUDE.md", SRC_CLAUDE_MD, "discovery"))
    return [(p, label, role) for p, label, role in out if p.is_file()]


def scan_prose_sources(repo_root: Path, anchors: frozenset[str]) -> tuple[dict[str, set[str]], dict[str, set[str]]]:
    """Deterministic regex scan of every prose source. Returns
    (accepted_hits, excluded_hits): both are {token: {file_paths}}.
    `accepted_hits` covers only tokens already known as anchors
    (corroboration, no new entry) or present in `_PROSE_DISCOVERIES`
    (a new entry). `excluded_hits` covers every other raw token found —
    recorded, never silently dropped (§J)."""
    accepted: dict[str, set[str]] = {}
    excluded: dict[str, set[str]] = {}
    for path, _label, _role in _prose_source_files(repo_root):
        text = path.read_text(errors="ignore")
        for m in _TOKEN_RE.finditer(text):
            tok = m.group(0)
            if _DECISION_ID_RE.match(tok):
                continue
            rel = str(path.relative_to(repo_root))
            if tok in anchors or tok in _PROSE_DISCOVERIES:
                accepted.setdefault(tok, set()).add(rel)
            else:
                excluded.setdefault(tok, set()).add(rel)
    return accepted, excluded


# ── structured scanners (§B items 1-4, 5, 7, 8, 15, 16) ─────────────────────

def _load_yaml(path: Path) -> dict:
    return yaml.safe_load(path.read_text()) or {}


def build_registry(
    repo_root: str | Path, source_commit_sha: str, generated_at: str, *, runner=None,
) -> dict:
    """Deterministic given (repo_root contents at source_commit_sha,
    source_commit_sha, generated_at, AND the executing environment's own
    git clone depth — see the module docstring's "Determinism scope"
    section for the disclosed exception this last dependency creates).
    Running this twice against an unchanged `main` in the SAME clone-depth
    environment must produce byte-identical `entries` (CONTENDER-0002 §I)
    — `generated_at` is the only field expected to vary run-to-run within
    one environment and is excluded from that determinism guarantee.
    `runner`, if supplied, replaces every `git` subprocess call this
    function makes (clone-depth detection and §G step 2 legacy recovery)
    for end-to-end testability without depending on the real environment."""
    repo_root = Path(repo_root)
    entries: dict[str, _Entry] = {}

    def entry(symbol: str, asset_type: str) -> _Entry:
        if symbol not in entries:
            e = _Entry(canonical_symbol=symbol, asset_type=asset_type,
                        primary_disposition="", secondary_flags=dict(_EMPTY_FLAGS))
            entries[symbol] = e
        return entries[symbol]

    alias_map = load_alias_map(repo_root)  # e.g. {"BRK-B": "BRK.B"}

    # §B item 1: targets.yaml destination: list.
    targets = _load_yaml(repo_root / "targets.yaml")
    destination = targets.get("destination", [])
    canonical_equities: set[str] = set()
    current_targets: set[str] = set()
    for row in destination:
        sym = row["ticker"]
        ac = row["asset_class"]
        asset_type = {"equity": "equity", "fund": "fund", "crypto": "crypto",
                       "reserve": "reserve", "cash": "cash"}.get(ac, "other")
        e = entry(sym, asset_type)
        e.add_prov(SRC_TARGETS, "discovery")
        e.secondary_flags["current_target"] = True
        current_targets.add(sym)
        if ac == "equity":
            canonical_equities.add(sym)

    # §B item 2: gates.yaml.
    gates_data = _load_yaml(repo_root / "gates.yaml")
    gated: set[str] = set()
    for g in gates_data.get("gates", []):
        sym = g["ticker"]
        e = entry(sym, "equity")
        e.add_prov(SRC_GATES, "discovery")
        e.secondary_flags["has_current_gate"] = True
        e.existing_disposition = f"gates.yaml: status={g.get('status')!r}, next_gate={g.get('next_gate')!r}"
        gated.add(sym)

    # §B item 3: holdings.yaml shares:/crypto_shares:.
    holdings = _load_yaml(repo_root / "holdings.yaml")
    current_holdings: set[str] = set()
    for sym in holdings.get("shares", {}):
        e = entry(sym, "equity" if sym not in {"SPY", "VEA", "VWO", "GLD"} else "fund")
        e.add_prov(SRC_HOLDINGS, "discovery")
        e.secondary_flags["current_holding"] = True
        current_holdings.add(sym)
    for sym in holdings.get("crypto_shares", {}):
        e = entry(sym, "crypto")
        e.add_prov(SRC_HOLDINGS, "discovery")
        e.secondary_flags["current_holding"] = True
        current_holdings.add(sym)

    # §B item 4: issuer_lookthrough.yaml constituents (e.g. AAPL, embedded-only via SPY).
    lookthrough = _load_yaml(repo_root / "issuer_lookthrough.yaml")
    for iss in lookthrough.get("issuers", []):
        sym = iss["ticker"]
        e = entry(sym, "equity")
        e.add_prov(SRC_ISSUER_LOOKTHROUGH, "discovery")

    # §B item 5: intelligence/companies/*.yaml (53 records).
    companies_dir = repo_root / "intelligence" / "companies"
    company_symbols: set[str] = set()
    for p in sorted(companies_dir.glob("*.yaml")):
        sym = p.stem
        company_symbols.add(sym)
        e = entry(sym, "equity")
        e.add_prov(SRC_COMPANIES, "discovery")
        e.secondary_flags["has_historical_intelligence"] = sym in _PI0035_RETAINED_NAMES

    # §F: freshness, read (never recomputed) from intelligence_report's own
    # public staleness API — the owning system for this fact.
    findings = _ir.collect_staleness_findings(companies_dir, date.today())
    freshness_due_symbols = {o.ticker for o in findings.overdue_reviews} | {c.ticker for c in findings.lapsed_catalysts}
    for sym in freshness_due_symbols:
        if sym in entries:
            entries[sym].secondary_flags["freshness_due"] = True

    # §B item 6: intelligence/themes — corroboration role only; these
    # records carry no direct member-ticker field (verified this session),
    # so they introduce zero new discoveries. Recorded as corroboration on
    # whichever symbols the theme's own evidence text already names, if any
    # — none found this generation.

    # §B item 7: intelligence/relationships/*.yaml filenames (pairwise tickers).
    rel_dir = repo_root / "intelligence" / "relationships"
    for p in sorted(rel_dir.glob("*.yaml")):
        a, b = p.stem.split("_")
        for sym in (a, b):
            e = entry(sym, "equity")
            e.add_prov(SRC_RELATIONSHIPS, "corroboration")

    # §B item 8: intelligence/classification/*.yaml — context only, never a
    # new-discovery source, never rescanned/reopened (§D).
    classification_dir = repo_root / "intelligence" / "classification"
    classified_symbols: set[str] = set()
    for p in sorted(classification_dir.glob("*.yaml")):
        if p.stem == "COHORT_MANIFEST":
            continue
        sym = p.stem
        classified_symbols.add(sym)
        if sym in entries:
            entries[sym].secondary_flags["classification_exists"] = True
            entries[sym].classification_status = "sealed_milestone6_reference_only"
            entries[sym].add_prov(SRC_CLASSIFICATION, "context")

    # §B item 16: governance/evidence/CHART-0002/ package manifests.
    chart_dir = repo_root / "governance" / "evidence" / "CHART-0002"
    chart_symbols: set[str] = set()
    if chart_dir.is_dir():
        for pkg_dir in sorted(p for p in chart_dir.iterdir() if p.is_dir()):
            record_path = pkg_dir / "record.yaml"
            if not record_path.is_file():
                continue
            rec = _load_yaml(record_path)
            sym = rec.get("identity_and_capture", {}).get("ticker")
            if sym:
                chart_symbols.add(sym)
                e = entry(sym, "equity")
                e.secondary_flags["chart_evidence_exists"] = True
                e.add_prov(SRC_CHART, "discovery")

    # §B item 15: earnings.py's alias map (context, resolves identity).
    for yahoo_form, canonical in alias_map.items():
        e = entry(canonical, "equity")
        e.add_prov(SRC_EARNINGS, "context")
        e.existing_disposition = (e.existing_disposition or "") + f"; alias {yahoo_form!r} -> {canonical!r} (earnings.py._YAHOO_SYMBOL)"

    anchors = frozenset(entries.keys())

    # §B items 9-14, 17 (disclosed): prose scan.
    accepted, excluded = scan_prose_sources(repo_root, anchors)
    for tok, files in accepted.items():
        if tok in anchors:
            for f in sorted(files):
                label = _label_for_prose_path(f)
                entries[tok].add_prov(label, "corroboration")
        elif tok in _PROSE_DISCOVERIES:
            spec = _PROSE_DISCOVERIES[tok]
            e = entry(tok, spec["asset_type"])
            for f in sorted(files):
                e.add_prov(_label_for_prose_path(f), "discovery")
            e.existing_disposition = spec["cite"]

    # §G steps 1-3: live, mechanical, environment-independent clone-depth
    # detection plus the mandatory recovery attempt when history is
    # reachable — run BEFORE disposition assignment so any genuinely new
    # recovered symbol is routed through the same §E.2 precedence engine
    # as every other discovered identity, not hardcoded to one tier.
    clone_depth = detect_clone_depth(repo_root, runner=runner)
    recovered, legacy_gap = perform_legacy_recovery(repo_root, clone_depth, runner=runner)
    for sym, asset_type, note in recovered:
        if sym in entries:
            # Already tracked via a live, current source (e.g. later
            # re-added to holdings/targets, or already carries a Company
            # Intelligence record) — never overwrite an existing,
            # already-provenanced entry with a historical recovery stub;
            # §H.3 step 4 ("never overwrite... only cite").
            continue
        e = entry(sym, asset_type)
        e.add_prov(SRC_HOLDINGS, "discovery")
        e.existing_disposition = f"Recovered via CONTENDER-0002 §G step 2's mechanical diff: {note}."
        accepted.setdefault(sym, set()).add(f"holdings.yaml (historical, §G step 2 recovery: {note})")

    # ── §E.2: assign exactly one primary disposition per identity, top to
    # bottom precedence order, mechanically. ────────────────────────────────
    for sym, e in entries.items():
        _assign_disposition(sym, e, canonical_equities, gated, company_symbols,
                             freshness_due_symbols, alias_map)

    # §C: dedupe alias forms — earnings.py's alias map already resolves
    # BRK-B -> BRK.B by construction (only the canonical form ever gets its
    # own entry() call above), so no separate duplicate_or_alias row exists
    # to dedupe; this is asserted in tests.

    sorted_entries = [entries[s].to_dict() for s in sorted(entries)]

    return {
        "schema_version": SCHEMA_VERSION,
        "source_commit_sha": source_commit_sha,
        "generated_at": generated_at,
        "governing_authority": "governance/decisions/CONTENDER-0002-contender-normalization-and-readiness-screening-authorization.md",
        "legacy_gap": legacy_gap,
        "entries": sorted_entries,
    }, accepted, excluded


_SOURCE_LABEL_FOR_PATH_PREFIX = [
    ("governance/decisions/", SRC_DECISIONS),
    ("governance/audits/", SRC_AUDITS),
    ("intelligence/BATCH", SRC_BATCH),
    ("research/", SRC_RESEARCH),
    ("operations/WORKSTREAMS.yaml", SRC_WORKSTREAMS),
    ("decision_log.yaml", SRC_DECISION_LOG),
    ("CLAUDE.md", SRC_CLAUDE_MD),
]


def _label_for_prose_path(rel_path: str) -> str:
    for prefix, label in _SOURCE_LABEL_FOR_PATH_PREFIX:
        if rel_path.startswith(prefix):
            return label
    return SRC_DECISIONS


def _assign_disposition(
    sym: str, e: _Entry, canonical_equities: set[str], gated: set[str],
    company_symbols: set[str], freshness_due_symbols: set[str], alias_map: dict[str, str],
) -> None:
    flags = e.secondary_flags
    # §E.3: read independently of which primary tier the symbol lands on —
    # "never omitted merely because a higher-precedence primary disposition
    # applied instead." Applies to all four PI-0036/PI-0038 names
    # regardless of gated status (§E.4's own worked example).
    flags["has_prior_deferral_superseded"] = sym in _PI0033_SUPERSEDED_FOR_RESEARCH

    # tier 1: synthetic_or_test_fixture — structural CASH/RESERVE rows.
    if sym in {"CASH", "RESERVE"}:
        e.primary_disposition = "synthetic_or_test_fixture"
        e.investability_status = "not_applicable_structural_row"
        e.research_status = "not_applicable"
        e.reason = "targets.yaml structural accounting row, not a tradeable instrument (CONTENDER-0001 §C.7)"
        e.next_required_action = "none — not an investable candidate"
        return

    # tier 2: benchmark_or_index.
    if sym in _PROSE_DISCOVERIES and _PROSE_DISCOVERIES[sym]["tier"] == "benchmark_or_index":
        e.primary_disposition = "benchmark_or_index"
        e.investability_status = "not_applicable_benchmark"
        e.research_status = "not_applicable"
        e.reason = _PROSE_DISCOVERIES[sym]["cite"]
        e.next_required_action = "none — used only as a comparison benchmark, not a position candidate"
        return

    # tiers 3, 4, 5, 6: none found this generation (see module docstring/audit).

    # tier 7: explicitly_deferred_or_excluded, with the mandatory supersession check.
    if sym in _PROSE_DISCOVERIES and _PROSE_DISCOVERIES[sym]["tier"] == "explicitly_deferred_or_excluded":
        e.primary_disposition = "explicitly_deferred_or_excluded"
        e.investability_status = "investable"
        e.research_status = "no_governed_evidence_record"
        e.existing_disposition = _PROSE_DISCOVERIES[sym]["cite"]
        e.reason = _PROSE_DISCOVERIES[sym]["cite"]
        e.review_trigger = "per the cited decision's own reopening condition, if any"
        e.next_required_action = "none authorized — deferred/excluded; reopening requires its own separate future authorization"
        return

    # tier 11: PI-0038's six gated-name records, explicit blanket insufficiency.
    if sym in _PI0038_INSUFFICIENT_EVIDENCE:
        e.primary_disposition = "insufficient_evidence"
        e.investability_status = "investable"
        e.research_status = "record_exists_but_discloses_material_access_gap"
        e.evidence_freshness_status = "insufficient_per_record_own_disclosure"
        e.existing_disposition = (
            "PI-0038 — gated-six Company Intelligence completion; record discloses its own research "
            "session's primary-source access failure in full"
        )
        e.reason = e.existing_disposition
        e.next_required_action = "insufficient for evaluation_ready; a future, separately authorized " \
            "evidence-remediation unit is required before this tier can change"
        return

    # tier 9: requires_research — genuine investable instrument, no governed
    # record of any kind (funds, crypto with no framework yet, or a named
    # candidate with no record).
    if sym in _PROSE_DISCOVERIES and _PROSE_DISCOVERIES[sym]["tier"] == "requires_research":
        e.primary_disposition = "requires_research"
        e.investability_status = "investable"
        e.research_status = "no_governed_evidence_record"
        e.existing_disposition = _PROSE_DISCOVERIES[sym]["cite"]
        e.reason = _PROSE_DISCOVERIES[sym]["cite"]
        e.next_required_action = "requires its own separate future research authorization before any evidence exists"
        return

    if sym not in company_symbols:
        # funds and crypto with a current target/holding but no equity-style
        # Company Intelligence framework, and no ETF/crypto-appropriate
        # equivalent exists yet (XASSET-0001) — or a §G step 2 recovered
        # legacy equity ticker with no Company Intelligence record of its
        # own (existing_disposition, set before this loop ran, already
        # carries its git-commit provenance and is left untouched here).
        e.primary_disposition = "requires_research"
        e.investability_status = "investable"
        e.research_status = "no_governed_evidence_record"
        e.reason = "genuine investable instrument; no Company/Theme Intelligence equivalent exists for " \
            f"asset_type={e.asset_type!r} yet (XASSET-0001 — ETF/crypto require their own, separately " \
            "governed, asset-appropriate framework, not yet built)"
        e.next_required_action = "requires a future, separately authorized asset-appropriate research framework"
        return

    # tiers 10/12: has a Company Intelligence record; mechanical freshness
    # decides which. Freshness is read, never recomputed (§F).
    if sym in freshness_due_symbols:
        e.primary_disposition = "requires_freshness_review"
        e.investability_status = "investable"
        e.research_status = "governed_record_exists"
        e.evidence_freshness_status = "stale_or_due_per_owned_freshness_fields"
        e.reason = "intelligence_report.collect_staleness_findings reports an overdue review or a " \
            "lapsed pending catalyst for this record as of generation time"
        e.next_required_action = "a future, separately authorized Intelligence-refresh unit"
        return

    e.primary_disposition = "evaluation_ready"
    e.investability_status = "investable"
    e.research_status = "governed_record_exists"
    e.evidence_freshness_status = "current_per_owned_freshness_fields"
    e.reason = "genuine investable instrument with an adequate, sufficiently current governed evidence base"
    e.next_required_action = "eligible for a future, separately authorized research-readiness-consuming step (e.g. an additional blind-classification cohort)"


if __name__ == "__main__":
    import sys

    _repo_root = Path(__file__).resolve().parent
    _sha = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=_repo_root, text=True).strip()
    _ts = subprocess.check_output(
        ["git", "log", "-1", "--format=%cI"], cwd=_repo_root, text=True
    ).strip()
    _registry, _accepted, _excluded = build_registry(_repo_root, _sha, _ts)

    _out_dir = _repo_root / "intelligence" / "contenders"
    _out_dir.mkdir(parents=True, exist_ok=True)
    _out_path = _out_dir / "registry.yaml"
    with _out_path.open("w") as f:
        f.write(
            "# intelligence/contenders/registry.yaml — generated by "
            "contender_registry_generator.py.\n"
            "# GOVERNED SNAPSHOT, NOT INVESTMENT-POLICY TRUTH (CONTENDER-0002 §I).\n"
            "# targets.yaml, holdings.yaml, gates.yaml, issuer_lookthrough.yaml, and\n"
            "# every existing Intelligence record remain sole authority for their own\n"
            "# facts. No hand edit is permitted outside a new, explicitly governed\n"
            "# regeneration or correction (§I) — re-run this generator, do not patch\n"
            "# this file directly.\n"
        )
        yaml.safe_dump(_registry, f, sort_keys=False, default_flow_style=False, width=100)

    print(f"contender_registry_generator: wrote {len(_registry['entries'])} entries to {_out_path}")
    print(f"  discovered-accepted tokens: {len(_accepted)}")
    print(f"  discovered-excluded tokens (false-positive prose matches): {len(_excluded)}")
