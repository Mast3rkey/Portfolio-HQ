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

## 12. Bounded correction (same PR, following independent review 4889352085)

An independent exact-head review of this PR's original head (`8dc8250c577713f946834bd16bf57df442cccad4`)
returned **CHANGES REQUIRED** — 0 BLOCKING / 4 MAJOR / 5 MINOR / 5 NOTE. This section records the
bounded correction pass performed in response, independently re-verifying each finding against
`VALUATION-0003`, `PROTOCOL_V1.md` §5, and the ticker's own permitted evidence before editing —
not mechanically adopting the reviewer's suggested outcome. All 27 names, the blind/redacted
workflow, the closed schema, and every prohibited-scope boundary (no valuation, no chart
evidence, no portfolio-policy leakage, no exhaustiveness claim) are unchanged.

### MAJOR findings

**1. ASML — primary/secondary reordered (D/B → B/D).** Independently re-read ASML's permitted
`risks[]` evidence and confirmed the reviewer's underlying point on different grounds than the
review itself cited: the review pointed to `ASML.md`'s non-permitted "Margin-relevance evidence"
section (explicitly excluded from this axis's evidence boundary, VALUATION-0003 §D — it is not
business-model narrative, competitive advantage, risk, catalyst, or `role_basis`). That section
was correctly never given to the blind drafter and this correction does not import it. However,
the *same* substantive fact — that ASML's long order-to-delivery lead time structurally smooths
recognized revenue relative to the broader order cycle, so a guidance-driven stock drop is not
evidence of sustained revenue-cycle sensitivity — is independently present in ASML's own
*permitted* `risks[]` text ("a long (12-24 month) order-to-delivery lead time, which smooths
ASML's recognized revenue relative to the broader WFE order cycle but does not eliminate
demand-timing risk to guidance"). The original D-primary rationale did not engage this
permitted-evidence disclosure and effectively mischaracterized it. Re-derived, from permitted
evidence only: primary **B** (capital-intensive infrastructure — sole EUV supplier building
constrained, multi-year capacity into a structural fab-capex buildout, ROIC/reinvestment framing
needed given guidance-timing sensitivity), secondary **D** (the underlying demand driver remains
a real semiconductor-capex cycle; the 2026 discontinuation of quarterly bookings disclosure means
a future downturn may surface later via revenue/guidance rather than earlier via bookings).
`evidence_quality` recalibrated `partial` → `limited` (see §13 below — no primary document was
ever directly opened for ASML by any researcher).

**2. RKLB — Iridium acquisition now explicitly disclosed in the rationale and F-test.**
Independently confirmed the pending, unclosed Iridium acquisition was never mentioned in the
original rationale. Traced why: the one CI `risks[]` item describing the deal in detail was
correctly redacted by the sanitizer (it contains the bare-noun phrase "this gate's original
drafting," a genuine self-reference to RKLB's own `gates.yaml` governance entry, not a false
positive) — the blind shard genuinely never received it. The permitted Milestone 6
`role_basis` context sentence *did* disclose the deal at a high level ("has signed a definitive
agreement to acquire Iridium's operating satellite-communications network and licensed
spectrum"), but the shard's rationale did not engage even that. The correction adds an explicit
paragraph, using only permitted evidence (the `role_basis` context and the surviving catalyst-item
fragment), disclosing the deal, explaining why it is excluded from the *current-state* archetype
(not closed, not reflected in reported segment structure, regulatory/shareholder approval
outstanding) rather than silently omitted, and noting the pending, conditional transaction itself
reinforces rather than undermines the existing E-primary/F-secondary call. Primary `E` and
secondary `F` are unchanged — the exclusion is defensible on the merits, not merely convenient.
`evidence_quality` unchanged (`limited`, already correctly set).

**3. SPGI — secondary archetype reordered (C → A).** Independently re-read `PROTOCOL_V1.md` §5's
literal archetype-C definition: businesses whose *own* capital structure and regulatory-capital
requirements make FCFF-DCF theoretically inappropriate because financing flows are the business
itself. S&P Global Ratings holds no loan book, deposits, or float requiring its own regulatory
capital treatment — its moat is a regulatory-license (NRSRO/ESMA) requirement that *others* rely
on for their own capital calculations, a licensing/market-structure barrier, not archetype C's own
defining mechanism. Re-derived secondary **A** (asset-light, high-incremental-margin
licensing/subscription/data economics, shared by Ratings, Indices, and Market Intelligence — the
three highest-margin segments). Primary **F** independently re-confirmed strongly supported
(genuine 19%–70% margin spread across four segments) and left unchanged, exactly as the review
itself found. `evidence_quality` recalibrated `partial` → `limited` (see §13 — no primary document
was ever directly opened for SPGI by any researcher).

### MINOR findings

- **KLAC** — secondary `A` removed (set to `null`). Re-examined against protocol §5's actual A
  definition ("subscription or platform-network economics"): KLAC's cited evidence (62.3% gross
  margin, a 17-year dividend-growth streak, backlog-conversion disclosure) is financial-quality
  signal, not subscription/platform-network economics — KLA is a capital-equipment manufacturer
  selling discrete systems and services. No equally well-supported alternative secondary was found;
  removed rather than forced. Primary `D` and the F-test (correctly rejecting F given 90.3%
  single-segment concentration) unchanged.
- **LLY** — secondary `E` removed (set to `null`). Protocol's E is defined at the whole-company
  cash-flow level ("not yet stable, predictable, or positive"); Lilly's own permitted evidence
  shows the opposite (56% YoY revenue growth on an already-commercial, profitable franchise). The
  cited pipeline acquisitions, Foundayo's safety label, and unresolved patent-exclusivity dates are
  ordinary disclosed risk on an already-commercial business, not E's defining condition. Removed
  rather than forced; those facts are retained as disclosed risk/uncertainty within the unchanged
  primary-`A` rationale. F-test (already correctly rejecting F — revenue is concentrated, not
  diversified) unchanged.
- **GNRC** — secondary `B` removed (set to `null`). Re-examined: the cited evidence (Enercon
  acquisition, Belvidere/Sussex capacity expansion) is a growth-leg capex story for one
  still-developing C&I product line, not evidence that Generac's *own* core economics are those of
  a long-lived-asset infrastructure operator with utility-like recurring demand — archetype B's
  actual defining mechanism. Generac remains fundamentally a cyclical durable-goods equipment
  manufacturer. Removed rather than forced (independently agreed with the review's characterization
  as the weakest-grounded secondary in the batch alongside KLAC's). Primary `D` and F-test
  unchanged.
- **PWR** — independently re-examined; no change made. The rationale already transparently
  discloses the exact taxonomy-fit tension the review flagged ("even though its capital intensity
  is expressed through labor/backlog rather than owned heavy assets") and `secondary_archetype` was
  already `null`. Confirmed this is the right way to handle a genuinely imperfect fit — disclosed,
  not concealed — and left unchanged, exactly matching the review's own MINOR (not MAJOR)
  classification and its reasoning for why.
- **WM** — inline-caveated. The `rationale`'s "large majority of revenue" framing supporting
  B-over-F now explicitly states it does not rely on WM's own line-of-business revenue breakdown
  (which `WM.md` itself says could not be reconciled to a complete, non-overlapping accounting) —
  the B-primary call is restated to rest instead on the independently-disclosed structural-scarcity
  and permitting-barrier facts about the landfill network, which do not depend on the unreconciled
  percentage. Primary `B` and secondary `F` unchanged (not disputed by the review).

### 13. Evidence-quality calibration rule (MAJOR finding 4)

**Derivation.** `VALUATION-0003` §H specifies only that `primary_source_coverage` reuses the
existing four-value vocabulary (`comprehensive`/`partial`/`limited`/`blocked`) "matching
`TIER-0002`/`XASSET-0002`" — it does not itself define the boundary between the values. Inspected
each of the 27 companies' own Company Intelligence `Source-access disclosure` section (the
authoritative, per-ticker record of what was and was not directly opened by any researcher across
that ticker's entire research history — this session, a prior CI-authoring session, or a disclosed
independent evidence-recovery researcher, e.g. "GPT-5.6 Thinking," a principal-supplied
checksum-verified evidence bundle). This is a factual, mechanically-checkable record already
present in every one of the 27 source files, not a new field or new judgment.

**Adopted rule** (a bounded implementation convention, not new governance, per this session's own
explicit authorization to adopt one where the schema is under-specified):

- **`limited`** — the ticker's own Source-access disclosure states primary-source access was
  tested and confirmed **completely blocked for the entire research history**, with **no instance,
  anywhere in the record, of a primary document being directly opened** by any researcher. Every
  fact, including the load-bearing facts the archetype rationale itself relies on, traces to
  WebSearch-returned snippet synthesis, one layer removed from primary text, for the whole record.
- **`partial`** — at least one primary document was directly opened by some researcher, covering
  some but not all of the record's material facts, **and** a specific, named evidentiary gap
  remains that bears materially on the archetype determination itself (not merely "the very latest
  quarter's headline figure is still secondary-only pending confirmation" — an ordinary, expected
  staleness pattern present in most records that does not by itself change an archetype call).
- **`comprehensive`** — primary documents were directly opened covering essentially the full
  evidentiary base the archetype rationale actually relies on, with no named gap that bears
  materially on the archetype call; an ordinary "latest quarter is secondary-only" caveat alone
  does not prevent this tier.
- **`blocked`** — reserved for "no usable *permitted* evidence exists at all" (would force
  abstention). Explicitly **not** used anywhere in this cohort and not forced merely because the
  label exists: every one of the 27 records has usable business-model/competitive/risk/catalyst
  evidence regardless of how that evidence was sourced — a web-access failure alone never triggers
  `blocked` under this rule, consistent with the zero-abstention result being genuine rather than
  an artifact of a miscalibrated vocabulary.

**Verification against the six formerly-gated names** (the group the review specifically
scrutinized): all six — ICE, RKLB, SNPS, SPGI, TSLA, WM — have Source-access disclosures stating,
in near-identical terms, that WebFetch was tested and confirmed blocked on every domain attempted
(including a neutral control domain used specifically to rule out a domain-specific block), with
no exception anywhere in the record. Under the rule above, all six independently resolve to
`limited`, uniformly — directly resolving the review's specific complaint (SNPS and RKLB, both
shard-4 records with comparably severe access failures, had received different tiers — `partial`
and `limited` respectively — under the original, uncalibrated application).

**Cohort-wide reapplication.** Applying the rule to all 27 records (not only the six scrutinized)
produced 13 tier changes beyond the three MAJOR-finding records (ASML, SPGI) already recalibrated
above:

| Change | Tickers | Reason |
|---|---|---|
| `partial` → `comprehensive` | AMZN, GOOGL, META, MSFT, V | Load-bearing base facts directly opened by a named evidence-recovery researcher (GPT-5.6 Thinking) from a primary filing; only the latest quarter is secondary-only, an ordinary gap that does not change the archetype call. |
| `partial` → `limited` | AVGO, GEV, KLAC, TMO, SNPS, TSLA | Source-access disclosure confirms no primary document was ever directly opened by any researcher for the entire record — the same severity class as the six formerly-gated names. |
| `partial` → `limited` (MAJOR-finding records) | ASML, SPGI | See MAJOR findings 1 and 3 above. |

Unchanged (already correctly calibrated under this rule on independent re-check): CEG, COST,
ISRG, NVDA, PANW, RTX, TSM (`comprehensive` — direct primary access with no material gap); ETN,
GNRC, LLY, PWR (`partial` — some primary access via a disclosed evidence-recovery correction pass,
but a specific named gap remains: ETN's base segment table was WebSearch-reproduced with only
later corrections GPT-5.6-inspected; GNRC's SEC-filing base data was never primary-opened, only
its Q2 2026 release; LLY's patent-exclusivity dates are unestablished; PWR's FY2025 adjusted-EBITDA
figure remains unreconciled even after an independent audit pass); ICE, RKLB, WM (`limited` —
already correctly set, matching the six-gated-name pattern).

**Final cohort-wide distribution**: `comprehensive` 12 (up from 7), `partial` 4 (down from 17),
`limited` 11 (up from 3), `blocked` 0 (unchanged). Every `uncertainty_statement` for a changed
record was rewritten to state, specifically and mechanically, the Source-access basis for its new
tier — not merely relabeled.

### 14. Post-correction regression checks

- **Primary/secondary/abstention integrity**: `valuation_archetype_validator.py` re-run clean
  (`OK (28 result(s))`) after every edit — primary vocabulary, secondary cardinality
  (`secondary != primary`, forced `null` on abstention), archetype-F disclosure requirement (all
  three MINOR-finding secondary removals left their existing, still-required F-test paragraph
  intact), and the 27-name roster all independently re-verified.
- **Leak scan**: the sanitizer's independently-implemented `independent_policy_scan()` was re-run
  directly against every changed record's free-text fields (`rationale`, `uncertainty_statement`,
  `disclosed_evidence_conflicts`) — zero findings across all 17 changed records.
- **Manifest/hash reconciliation**: `COHORT_MANIFEST.yaml` regenerated by reading each record's own
  recomputed `content_sha256` directly (not hand-edited) — exactly the 17 changed records' manifest
  rows updated, zero unrelated churn; bidirectional reconciliation independently re-verified by
  `valuation_archetype_validator.py`.
- **Final distribution**: primary `A:6 B:6 C:2 D:2 E:1 F:8 G:2` (27 total); secondary present on
  19/27 (down from 22, reflecting the three MINOR-finding removals); abstentions 0 (unchanged).

No valuation, fair value, price target, expected return, chart evidence, or portfolio-policy
content was introduced by this correction. This correction does not itself determine the PR ready,
principal-accept it, or merge it — a fresh independent exact-head review remains required per
`OPS-0007` §1 / `OPS-0009` Lane G before that may occur.
