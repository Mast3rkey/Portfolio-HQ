# WS-0015 — VALUATION-0003 archetype-assignment implementation (retained audit)

**Date:** 2026-08-08
**Authorizing decision:** `governance/decisions/VALUATION-0003-equity-valuation-archetype-assignment-authorization.md`
(merged PR #278, merge SHA `0d0252021ded7f18a44c8688148606c9ee39fad4`, final exact-head
delta review `4889166749` — APPROVED FOR PRINCIPAL EXACT-HEAD ACCEPTANCE, 0/0/0 — principal
acceptance `issuecomment-5226982097`, merge-commit CI run `31266841966` success)
**This filing:** implementation only, gated entirely on the above authorization. This document
performs no governance act of its own and authorizes nothing beyond what VALUATION-0003 already
granted.

## 1. Preflight, independently verified

- `origin/main` fetched; local branch `claude/valuation-archetype-27-equities-1y28my` confirmed a
  fresh checkout of `origin/main` at `0d0252021ded7f18a44c8688148606c9ee39fad4`, zero divergence.
- Zero open pull requests confirmed before any edit.
- `governance/decisions/VALUATION-0003-...md` read in full from the live repository (not assumed
  from the authorizing task's own summary) — §§A–N, Rationale, Alternatives, and the Bounded
  Correction section all independently re-derived the operative requirements below directly from
  that text.
- Canonical 27-name equity roster independently re-derived from `targets.yaml`'s `destination:`
  list, `asset_class: equity` rows: `AMZN, ASML, AVGO, CEG, COST, ETN, GEV, GNRC, GOOGL, ICE,
  ISRG, KLAC, LLY, META, MSFT, NVDA, PANW, PWR, RKLB, RTX, SNPS, SPGI, TMO, TSLA, TSM, V, WM` —
  zero drift from VALUATION-0003 §B's own snapshot.
- Zero `intelligence/valuation_archetype/` content existed anywhere in the repository at the
  start of this session.
- Full repository `pytest` baseline independently reproduced before any edit: 3341 passed.

## 2. Artifact/schema structure selected

Single-YAML-per-ticker, filesystem-is-the-index — `intelligence/valuation_archetype/<TICKER>.yaml`
plus one `COHORT_MANIFEST.yaml` — matching `intelligence/classification/`,
`intelligence/etf_classification/`, and `intelligence/crypto_classification/`'s identical
convention (VALUATION-0003 §H), not the paired-YAML+Markdown Company Intelligence convention.

## 3. Blind sanitizer design (`valuation_archetype_sanitizer.py`)

Freshly authored — not a copy of `intelligence_classification_sanitizer.py` (VALUATION-0003
§F.2) — and, disclosed as a deliberate strengthening beyond the minimum required, built as
**allow-list extraction** rather than a pure strip-from-everything design:

1. **Whole-key strip** (§F.1): `strip_yaml_data()` removes `portfolio_role_ref`, `conviction`,
   and `review` (the whole block, including `review.log` narrative) from a copy of the raw
   Company Intelligence YAML, wholesale, before anything downstream ever sees it.
2. **Allow-list extraction** (§D): from the *already-stripped* data, only `sector`, `industry`,
   `competitive_advantages`, `risks[].risk`, `catalysts[].catalyst`, and the `## Business summary`
   markdown section (via `extract_business_summary()`, an exact-title match — no other section
   title is ever extracted, so an undisclosed section elsewhere in the document cannot leak) are
   pulled into the packet. The sealed Milestone 6 `economic_role.role_basis` narrative is
   optionally included as disclosed context.
3. **Item-level scan/redact** (§F.2): every extracted string is independently checked by
   `item_text_is_forbidden()` — bare-noun gate-policy leakage (with a whitelist for legitimate
   technical/process uses: "technological gate," "gate-all-around," "customer-qualification
   gate," "stop-before-drafting gate," etc., carried forward directly from the exact defect class
   `TIER-0004`'s Milestone 6 corrections found and fixed), bare `conviction`, config-key literals
   (`portfolio_role_ref`, `target_pct`, `targets.yaml`, `gates.yaml`, `next_gate`, `allow_add`,
   `issuer_lookthrough.yaml`, `holdings.yaml`), target/allocation numeric patterns, Milestone
   7/8 finding vocabulary, and the full chart-domain term list. A tripped item is *wholly*
   excluded (a placeholder, never partial masking).
4. **Mechanistically independent second-stage scan** (§F.3): `independent_policy_scan()` is a
   materially separate implementation — its own pattern set, its own gate-whitelist re-scrub, and
   proven (by a dedicated AST-level test) to never call and never be called by
   `item_text_is_forbidden()`/`redact_item()` — run over the assembled packet text before drafting
   and again over every sealed record's free-text fields after drafting.
5. `sector`/`industry` pass through unredacted by design (§D permits them as suggestive context).

**Bug found and fixed during this session, disclosed rather than silently corrected**: the
packet's own instructional header text ("do not consult...gate status...conviction rating")
originally tripped the independent scanner on its own meta-instructions (a self-inflicted false
positive, not a real leak) — reworded to avoid the literal trigger words before any packet was
used for drafting; re-verified clean across all 27 tickers afterward.

## 4. Sanitized-input generation and proof (§F.4)

All 27 sanitized packets were generated and independently verified leak-free (`verify_packet()`
returned `[]` for all 27) **before** any blind-drafting session began. Real, substantive
redactions occurred and were manually spot-checked as genuine (not over-triggering): ETN (1 —
"...carry no decision-bearing weight in this record's conviction rationale"), KLAC (1 — a
gate-policy self-reference), PWR (1 — a legacy-litigation risk item carrying prohibited language),
ICE (3), RKLB (3), SNPS (2), SPGI (5 — SPGI's own record had been directly gate-policy-annotated
in a prior WS-0005 correction pass, correctly caught).

**Isolation boundary disclosed as instructional, not filesystem-sandboxed** (§F.4, matching
`TIER-0004` §9.2's and Milestone 6's own identical disclosure): each of the five blind-drafting
subagents was a freshly-spawned session with no memory of this conversation, instructed not to
call any tool, read any file, or use any prior knowledge of portfolio weight/tier/conviction/gate
status, and given *only* the sanitized packet text embedded directly in its prompt (never a file
path to read). This cannot be proven at the filesystem level; the proof that matters is
downstream — every sealed record's own free-text fields were independently re-scanned after
sealing and found clean.

## 5. Shard structure

Five internal shards of 5–6 tickers each (VALUATION-0003 §G, matching Milestone 6's own
precedent), alphabetically split:

| Shard | Tickers |
|---|---|
| 1 | AMZN, ASML, AVGO, CEG, COST, ETN |
| 2 | GEV, GNRC, GOOGL, ICE, ISRG |
| 3 | KLAC, LLY, META, MSFT, NVDA |
| 4 | PANW, PWR, RKLB, RTX, SNPS |
| 5 | SPGI, TMO, TSLA, TSM, V, WM |

One primary session (this one) integrated and sealed all shard output; no shard carried
independent governance authority or opened its own PR.

## 6. Assignment results — 27/27, zero abstentions, zero silent contraction

Primary archetype distribution: **A: 6** (ISRG, LLY, META, NVDA, PANW, SNPS), **B: 5** (CEG, GEV,
PWR, TSM, WM), **C: 2** (ICE, V), **D: 3** (ASML, GNRC, KLAC), **E: 1** (RKLB), **F: 8** (AMZN,
AVGO, ETN, GOOGL, MSFT, RTX, SPGI, TSLA), **G: 2** (COST, TMO). 22 of 27 carry a secondary
archetype; all 22 carry the mandatory archetype-F disclosure. Zero `unable_to_determine_archetype`
records — the evidence in every sanitized packet was rich enough to support a determined primary
archetype, disclosed honestly rather than forced or manufactured.

Every record's `disclosed_evidence_conflicts` and `evidence_quality.uncertainty_statement` are
populated from the shard's own drafting judgment, not fabricated post-hoc.

## 7. Portfolio-context mechanical facts (six gated tickers)

`gate_fact_for_ticker()` computed, directly against `gates.yaml`, **after** the archetype
judgment was already sealed — never passed to a drafting shard, never used as archetype-determining
evidence (VALUATION-0003 §D/§E):

| Ticker | gate_exists | next_gate_references_valuation |
|---|---|---|
| SNPS | true | true |
| ICE | true | false |
| SPGI | true | true |
| WM | true | true |
| RKLB | true | false |
| TSLA | true | true |

The literal `next_gate` text (e.g. SPGI's own peer-comparator and methodology-framing language,
the exact risk the Bounded Correction on VALUATION-0003 itself flagged) never reached a drafting
shard and never appears in any sealed record — confirmed by the independent post-sealing scan.

## 8. Validator (`valuation_archetype_validator.py`)

Freshly authored, zero import coupling with `allocate.py`/`margin_state.py`, and — per
VALUATION-0003 §I and this repository's own established lesson (`TIER-0004`'s corrected design)
— zero import coupling with `valuation_archetype_sanitizer.py` either: the validator's own
prohibited-content scan is a wholly separate implementation, not a second call into the
sanitizer's scan (proven by a dedicated AST-based test). Covers: closed schema at every level
(top-level, `evidence_quality`, `portfolio_context`, manifest rows) with extra-key rejection;
primary vocabulary (8 closed values); secondary vocabulary/cardinality (0 or 1 of A–G, `!=`
primary, forced `null` on abstention); abstention-requires-`evidence_gap_statement` and its
converse; the archetype-F disclosure check (mechanical for the secondary-present case, a
disclosed best-effort heuristic for the no-secondary-but-segment-language case); a live 27-name
roster reconciliation via `relationship_validator.load_canonical_universe()` (reused, not
re-derived); an independently-implemented prohibited-field/chart-domain/directive-word scan;
content-hash reproduction; and full cohort-manifest reconciliation (duplicate detection, missing/
extra population, orphan-record detection, hash cross-check in both directions).

**Two real bugs found and fixed by the validator's own first run against the real corpus**,
disclosed rather than smoothed over: (1) the bare directive-word scan for "stage" originally
false-positived on legitimate taxonomy vocabulary (`early-stage`, `pipeline-stage`,
`venture-stage` — archetype E is literally named "Early-stage / binary-outcome") — fixed with a
targeted whitelist for hyphenated compounds, verified against all 27 real records with zero
remaining false positives and zero loss of real-directive-word detection; (2) the manifest
orphan-record check originally treated `COHORT_MANIFEST.yaml` itself as an orphan record via an
unfiltered glob — fixed.

## 9. Full validation, this session's own head

- `valuation_archetype_validator.py`: `OK (28 result(s))` (27 records + manifest).
- `classification_validator.py`: `OK (28 result(s))`; `reconciliation_validator.py`: `OK (27
  tickers)`; `recommendation_validator.py`: `OK (27 tickers)`; `relationship_validator.py`: `OK
  (13 record(s))`; `intelligence_validator.py`: clean (exit 0); `freshness_validator.py`: `OK`;
  `contender_registry_validator.py`: `OK (84 entries)`; `etf_classification_validator.py`: `OK (5
  result(s))`; `crypto_classification_validator.py`: `OK (4 result(s))` — all unaffected.
- `test_valuation_archetype_sanitizer.py` + `test_valuation_archetype_validator.py`: **183 passed,
  0 failed** (new tests only).
- Full repository `pytest`: **3524 passed, 0 failed**, 1 pre-existing unrelated
  `DeprecationWarning` (`intelligence_classification_sanitizer.py`'s own `\d`-escape docstring —
  unrelated to this implementation, already disclosed elsewhere in this repository's history).
- `test_portfolio_hq_dashboard_decisions.py`: **95 passed** — decision catalog unaffected (no new
  governance decision filed by this implementation).
- Repo-wide YAML/YML and JSON parse: 0 errors across every file.
- `git diff --check`: clean.
- `git status --porcelain`: only new, untracked files — zero diff on every protected path
  (`allocate.py`, `levels.py`, `margin_state.py`, `targets.yaml`, `holdings.yaml`, `gates.yaml`,
  `issuer_lookthrough.yaml`, every existing `intelligence/**` record, `PROTOCOL_V1.md`,
  `METHODOLOGY_EVALUATION_REPORT.md`, every `governance/decisions/*.md`) confirmed automatically.

## 10. Exact changed-file inventory

New files only:

- `valuation_archetype_sanitizer.py`
- `valuation_archetype_validator.py`
- `test_valuation_archetype_sanitizer.py`
- `test_valuation_archetype_validator.py`
- `intelligence/valuation_archetype/{AMZN,ASML,AVGO,CEG,COST,ETN,GEV,GNRC,GOOGL,ICE,ISRG,KLAC,LLY,META,MSFT,NVDA,PANW,PWR,RKLB,RTX,SNPS,SPGI,TMO,TSLA,TSM,V,WM}.yaml` (27 records)
- `intelligence/valuation_archetype/COHORT_MANIFEST.yaml`
- `governance/audits/WS0015_VALUATION0003_ARCHETYPE_ASSIGNMENT_IMPLEMENTATION_20260808.md` (this file)

Modified (Lane M, additive only, no existing gate's own text edited):

- `operations/WORKSTREAMS.yaml` (`WS-0015` entry)
- `CLAUDE.md` (one Decisions Log pointer entry)

## 11. Explicit non-authority restatement

No real-company valuation, fair value, price target, expected return, discount rate, peer
multiple, or scenario-probability assignment was performed. No RQ4 evidence-category schema
design was performed. `TIER-0009` §K's `valuation_required` status is unchanged on all 27
equities. No `PROTOCOL_V1.md`, `METHODOLOGY_EVALUATION_REPORT.md`, `VALUATION-0001`, or
`VALUATION-0002` file was edited. No target, tier, holdings, gate, cap, cluster, allocator,
margin, or ladder value changed. No chart evidence of any kind was consumed. This session does
not review its own PR, mark it ready, or merge it — that lifecycle remains for a separate,
independent, exact-head review per `OPS-0007` §1.
