# WS-0005 Milestone 6 — Population Reconciliation and Blindness-Process Preflight (TIER-0004 Bounded Unit)

**Implementation output of this session — not an independent review.**

| Field | Value |
|---|---|
| Authority | `governance/decisions/TIER-0004-ws0005-milestone6-population-and-blindness-preflight.md`; `operations/WORKSTREAMS.yaml` `WS-0005`, `milestone6-prereq5-population-reconciliation` gate |
| Scope | Pre-Milestone-6 roadmap Step 5: reconcile the final eligible classification population from live repository truth; define the blindness boundary, redacted-evidence mechanics, sealing/contamination controls, abstention mechanics; close the narrow `economic_role` schema gap; determine validator requirements; preserve the Step 6 authorization requirement. No ticker is classified. No sanitized evidence package is created. No validator is implemented. |
| Repository state audited | `origin/main` @ `ecd1e89d1278432874dab0d5440a9a8eecbc57d1` (PR #250 merge commit — `TIER-0003` effective), verified clean, working tree clean, zero open PRs |
| Mode | Design and reconciliation only. Every mechanism below is a specification for future, separately authorized use — nothing here is applied, sealed, or made operative by this artifact. |

---

## 0. Preflight summary

- `origin` fetched; local `main` confirmed identical to `origin/main` at `ecd1e89d1278432874dab0d5440a9a8eecbc57d1` (matching the exact SHA reported in the authorizing task, independently re-derived, not trusted). Working tree clean.
- Zero open pull requests (`mcp__github__list_pull_requests`, `state: open` → `[]`). No active mutation lane.
- `TIER-0004` confirmed the correct next identifier: `governance/decisions.yaml` and `portfolio_hq.dashboard.decisions.build_catalog('.')` both independently re-derived 77 decisions, `issues == ()`, before this filing's own new row; `TIER-0001`/`TIER-0002`/`TIER-0003` are the only existing `TIER-####` entries; `TIER` remains the correct, already-established prefix for Milestone 5/6 classification-architecture decisions.
- `PR #250` (`TIER-0003`) independently re-confirmed via the GitHub API: `merged: true`, merge commit `ecd1e89d1278432874dab0d5440a9a8eecbc57d1` (matching `origin/main`'s current tip exactly, parents `71dab2d2...` and `94ce0f930ecd44b32e09d20ed53c3d545aa2b96a`), independent exact-head review `4865299395` (0 BLOCKING / 0 MAJOR / 0 MINOR / 2 NOTE, verdict "APPROVED FOR PRINCIPAL EXACT-HEAD ACCEPTANCE"), retained principal-acceptance comment `issuecomment-5193111879` (explicit acceptance quoted verbatim at exact head `94ce0f930ecd44b32e09d20ed53c3d545aa2b96a`), and retained post-merge-verification comment `issuecomment-5193183437` (merge-tree identity confirmed, 5-file scope confirmed, 77 decisions/`issues == ()`, full suite 2581/2581, merge-commit CI `31015769683` `success`). All independently re-confirmed this session, not copied from the authorizing task's own summary.
- `relationship_validator.py` — OK (13 records), unaffected; `intelligence_validator.py` — 53/53 valid, unaffected; `freshness_validator.py` — OK, unaffected.
- `operations/WORKSTREAMS.yaml`'s `milestone6-prereq4-chart-evidence-scope-decision` gate, as merged, reads `status: in_progress`, `pr: 250` — accurate as of `TIER-0003`'s own filing (a filing never marks its own still-unmerged work complete), but stale now that PR #250 has since merged, been reviewed, and been accepted. Per that PR's own post-merge-verification comment, this synchronization is "deferred to the next WS-0005 filing's own Lane M synchronization pass (expected to be the Step 5 filing)" — this filing performs it (§8 below).
- **Discrepancy disclosed against the authorizing task's own assumed live state, not silently corrected to match the task:** the task's own text states `milestone6-prereq6-fresh-authorization-required` should be "kept... proposed." Live `operations/WORKSTREAMS.yaml` (as merged by `PI-0038`, unedited since) instead reads `status: blocked` for that gate — a materially equivalent, already-correct non-authorization state (no literal `blocked` enum conflicts with this repository's status vocabulary; `TIER-0003`'s own independent review, finding 4865299395 NOTE 2, already confirmed `status: proposed` is used elsewhere for the same non-authorization meaning and both are acceptable). Per this repository's own "never trust copied state over live repository truth" discipline and its convention of never rewriting another gate's own historical, already-accurate text, `milestone6-prereq6`'s `status: blocked` is left exactly as merged — not "corrected" to `proposed`. See §8 for the full gate-by-gate synchronization record.

No condition met a Stop bar. This unit proceeded.

---

## 1. Authorizing scope (restated, not expanded)

The principal authorized exactly one bounded Step 5 filing: reconcile the final eligible Milestone 6 classification population; define the exact blindness boundary; define redacted evidence-input mechanics; define sealing and contamination controls; define abstention mechanics; close any narrow schema gap that must be resolved before drafting; determine validator requirements; preserve the requirement for a separate future Step 6 authorization. This filing does not authorize classification of any ticker, does not create `intelligence/classification/` or any file inside it, does not create a redacted evidence package, and does not implement a validator.

This artifact is the retained design and reconciliation record; `governance/decisions/TIER-0004-*.md` is the governing decision that authorizes and frames it.

---

## 2. Final eligible Milestone 6 classification population

### 2.1 Derivation

Derived live from `targets.yaml`'s `destination:` list (36 rows total), excluding the 9 non-equity rows (`SPY`, `VEA`, `VWO`, `RESERVE`, `CASH`, `GLD`, `BTC`, `ETH`, `SOL`):

```
NVDA, TSM, ASML, AVGO, SNPS, KLAC, MSFT, GOOGL, AMZN, META, PANW, LLY, ISRG,
TMO, ICE, SPGI, V, COST, WM, CEG, ETN, GEV, GNRC, PWR, RTX, RKLB, TSLA
```

**27 canonical equities — matching the authorizing task's expected list exactly, zero drift.** Cross-checked against `intelligence/companies/*.yaml`: all 27 carry a governed Company Intelligence record (0 missing). No exclusion candidate was found.

### 2.2 Eligibility standard applied

Per the authorizing instruction, a canonical equity is **eligible** if it carries governed Company Intelligence, regardless of `PROVISIONAL` status, partial or blocked primary-source access, a bounded unresolved factual gap, or current gate status. None of those conditions removes a ticker from the population; each is instead represented inside that ticker's own future `evidence_quality` axis (§5 below) or, where the permitted evidence genuinely cannot support a judgment, via the narrow abstention path (§6).

### 2.3 Eligibility result, per ticker

| Ticker | CI record | Gated? | Evidence posture (from record's own disclosure) |
|---|---|---|---|
| NVDA | Yes | No | Comprehensive; refreshed under `PI-0018`/freshness pass |
| TSM | Yes | No | Comprehensive |
| ASML | Yes | No | Comprehensive; refreshed under freshness pass |
| AVGO | Yes | No | Comprehensive |
| SNPS | Yes | **Yes** | `PI-0038` — WebFetch fully blocked; WebSearch-sourced only, disclosed |
| KLAC | Yes | No | Comprehensive; refreshed under freshness pass |
| MSFT | Yes | No | Comprehensive; refreshed under freshness pass |
| GOOGL | Yes | No | Refreshed under freshness pass (evidence-currency gap found and closed) |
| AMZN | Yes | No | Refreshed under freshness pass; one uncorroborated claim explicitly excluded |
| META | Yes | No | Refreshed under freshness pass (most significant gap closed: two new risk entries) |
| PANW | Yes | No | Comprehensive |
| LLY | Yes | No | **Partial** — unresolved patent/exclusivity-timeline question (batch-wide, not independently verified); Wisconsin production-start date omitted per bounded abstention. See §4. |
| ISRG | Yes | No | Refreshed under freshness pass (OTTAVA De Novo authorization added) |
| TMO | Yes | No | Refreshed under freshness pass (Q2 2026 results added; two new risk entries) |
| ICE | Yes | **Yes** | `PI-0038` — WebFetch fully blocked; WebSearch-sourced only, disclosed |
| SPGI | Yes | **Yes** | `PI-0038` — WebFetch fully blocked; corrected mid-flight per independent review (Mobility-scope clarification, revenue-reconciliation gap closed) |
| V | Yes | No | Refreshed under freshness pass (new risk entry: workforce reduction/restructuring charge) |
| COST | Yes | No | Comprehensive |
| WM | Yes | **Yes** | `PI-0038` — WebFetch fully blocked; FY2025 revenue-mix breakdown disclosed as incomplete |
| CEG | Yes | No | Comprehensive |
| ETN | Yes | No | Refreshed under freshness pass (Q2 2026 margin recovery added; pre-existing margin-quality dispute left explicitly unresolved) |
| GEV | Yes | No | Refreshed under `PI-0020` (Q2 2026 results, debt/tariff disclosures, capital-allocation facts) |
| GNRC | Yes | No | Comprehensive (`PI-0036`) |
| PWR | Yes | No | Refreshed under freshness pass (Q2 2026 catalyst resolved; pre-existing FY2025 adjusted-EBITDA ambiguity left explicitly unresolved) |
| RTX | Yes | No | Comprehensive (`PI-0036`) |
| RKLB | Yes | **Yes** | **Limited** — WebFetch completely blocked at network-policy layer; multiple `[UNVERIFIED-CONFLICT]` flags (share count, Neutron milestone timing); freshness pass left explicitly `UNRESOLVED` (not edited, evidence insufficient/conflicting). See §4. |
| TSLA | Yes | **Yes** | `PI-0038` — WebFetch fully blocked; refreshed under freshness pass; a pre-existing `[UNVERIFIED-CONFLICT]` (US EV market-share figures) remains open |

**Result: 27 of 27 eligible. Zero exclusions.**

---

## 3. LLY and RKLB — explicit treatment, verified live

Both **remain in the full 27-name population** and are **eligible for full classification** on all four future axes. Neither carries a blanket exclusion. Their disclosed evidence limitations belong in `evidence_quality`, not in a population cut:

- **LLY**: `intelligence/companies/LLY.yaml`'s own `review.log` records an unresolved, batch-wide patent/exclusivity-timeline question (not independently verified claim-by-claim) and a deliberately omitted Wisconsin production-start date (network-policy blocked, bounded-abstention instruction followed at authoring time). `LLY.md` §"Unresolved questions" names both explicitly. `conviction.rating: High` stands unedited. None of this is a reason to exclude LLY from Milestone 6 — it is exactly the kind of "partial primary-source coverage under a real thesis" case `TIER-0002`'s own `evidence_quality` axis (§3.6, "a `High`-conviction thesis can carry `limited` primary-source coverage") was designed to represent.
- **RKLB**: `intelligence/companies/RKLB.yaml`'s `review.log` (most recently touched by `PI-0039`'s freshness pass, 2026-08-05) explicitly classifies RKLB `UNRESOLVED` — WebFetch fully blocked, share-count and Neutron-milestone conflicts left open, not silently resolved. `RKLB.md` §"Uncertainty and open items" names four conflicting current-share-outstanding figures and two large unresolved execution questions. `conviction.rating: Medium` stands unedited. RKLB is also one of the six formerly-gated names (§4).

**No automatic `capital_priority: no_assessment` is triggered for either ticker by this filing or by any future one solely because a bounded unresolved evidence item exists.** Whether a future Milestone 6 drafting session, applying `TIER-0002`'s `capital_priority.status` enum to the *permitted* evidence available for LLY or RKLB, lands on `maintain_current_weight`, `case_for_review`, or `no_assessment` is that session's own judgment call at drafting time — this filing does not pre-determine it, and does not treat "evidence is imperfect" as equivalent to "no assessment is possible." The same non-cascading rule applies to `economic_role` (§6).

---

## 4. The formerly gated six — treatment

SNPS, ICE, SPGI, WM, RKLB, and TSLA (`gates.yaml`, `PHQ-2026-01`/`PI-0038`) are **fully included in the 27-name population, with no special carve-out**. `PI-0038`'s own gated-name research disclosed, for all six, that every WebFetch attempt was blocked at either the domain or network-policy layer this session, so no primary-source document was directly opened for any of the six — every fact traces to WebSearch-returned snippets, with cross-source numeric inconsistencies disclosed rather than silently resolved (`PI-0038`'s own bounded correction pass, resolving 5 MAJOR findings from independent review `4860559002`, further tightened several of these claims). All six carry `conviction.rating: Medium` and `portfolio_role_ref: gated`.

Being gated for buying (`allow_add: false`) is a **buy-eligibility fact, not a research-eligibility fact** — `gates.yaml` itself states a gated name's "existing shares of a gated name are held, not force-exited," and nothing in `PHQ-2026-01`/`PHQ-2026-02`/`PI-0038` conditions Company Intelligence coverage, or future classification eligibility, on gate status. This resolves `TIER-0001`'s own open question #5 ("does the 6-name gated set need any classification at all while gated, given they carry destination weight but zero Company Intelligence coverage") — that question was live at `TIER-0001`'s authoring time (2026-08-04) because all six then had zero coverage; `PI-0038` closed the coverage gap the same day, and this filing now closes the eligibility question directly: **yes, include them, on the same terms as every other canonical name.** A gated name's weaker evidence base (WebSearch-only, no direct primary-source inspection) is represented in `evidence_quality`, exactly as it is for LLY/RKLB — never as a population exclusion.

---

## 5. Excluded names — confirmed, and why they are not part of this population

No canonical equity is excluded. The only tickers *not* in the 27-name population are structurally outside `targets.yaml`'s equity rows entirely, not evidence-based exclusions:

- **Non-equity destination rows** (`SPY`, `VEA`, `VWO`, `RESERVE`, `CASH`, `GLD`, `BTC`, `ETH`, `SOL`) — funds, cash, reserve, and crypto carry no `economic_role`/`capital_priority` classification target under `TIER-0002`'s design (built for individual company holdings; `docs/INVESTMENT_ONTOLOGY.md` §D's five economic systems are company-role vocabulary, not fund/crypto vocabulary).
- **Deferred non-canonical names** (`EQIX`, `UNH`, `DHR`, `SYK`, `AAPL`, `CEG`'s peers, and the ~26 other Company-Intelligence-covered tickers no longer in the canonical roster per `PI-0035`) — none carries a current `targets.yaml` destination row, so none is a Milestone 6 subject. `PI-0033`'s and `PI-0035`'s own dispositions for these names are unedited and not reopened by this filing.
- **SKHY** — deliberately unresolved policy per `CLAUDE.md` Open Items; carries a Company Intelligence record but no canonical destination weight; outside this population for the same structural reason as the deferred names above.

---

## 6. Permitted and forbidden Milestone 6 drafting inputs

### 6.1 Permitted (restates `TIER-0003` §A, applied to Step 5's own redaction design)

- Governed Company Intelligence — business model, segments, economics, financial facts, disclosed risks, catalysts, and sources (`sector`, `industry`, `themes`, `competitive_advantages`, `risks[]`, `sources[]`);
- Theme Intelligence (`intelligence/themes/`) where directly relevant to a ticker's economic role;
- governed `intelligence/relationships/*.yaml`/`.md` records, where permitted by sequencing (§9 — never before `economic_role`/`capital_priority` are sealed, per `TIER-0002` §3.5's own "risk_concentration computed after judgment axes" design);
- `docs/INVESTMENT_ONTOLOGY.md` §D/§A/§E vocabulary (economic systems, company-role terms);
- accepted comparison artifacts (`intelligence/BATCH*_COMPARISON.md`) **only for their evidence content** — business-model, overlap, and mechanism descriptions — never for any prior policy conclusion embedded in the same document (e.g. a comparison artifact's own advisory capital-priority language, where present, is forbidden — see §6.2).

### 6.2 Forbidden — the answer-key list

The judgment-drafting process (both `economic_role` and `capital_priority`) must not receive or use:

- `targets.yaml` or any `target_pct` value;
- `holdings.yaml` or any current portfolio weight;
- `portfolio_role_ref` (any Company Intelligence record's stale tier label);
- `conviction.rating` (any Company Intelligence record's conviction field);
- `gates.yaml` or gate membership/status;
- any prior tier or historical tier label (`T1`/`T2`/`band`/`spec`/`ETF`/`gated`);
- any prior promotion, demotion, retain, remove, or target conclusion (e.g. `TGT-0002`'s COST promotion, `PI-0035`'s roster dispositions);
- `caps.clusters` membership **during `economic_role` or `capital_priority` drafting** (permitted only afterward, computationally, for `risk_concentration` — §9);
- `issuer_lookthrough.yaml` **during `economic_role` or `capital_priority` drafting** (same rule);
- any current `risk_concentration` output, including the `unmeasured_flag` computation itself, before the judgment axes are sealed;
- chart images, filenames, manifests, coverage/inventory status, technical indicators, S/R levels, momentum/trend descriptions, technical interpretations, or price-action conclusions of any kind (`TIER-0003` §B, restated without narrowing);
- the CLAUDE.md Decisions Log's prior placement conclusions (e.g. "AMZN kept at T2," "COST promoted T1," "AAPL promoted band → T2");
- any output of a stopped or prior classification-drafting session, including the two untracked local drafts named in §10.

---

## 7. Redacted evidence-input mechanics

### 7.1 Problem

`intelligence/companies/<TICKER>.yaml` mixes permitted evidence (§6.1) with forbidden answer-key fields (§6.2) in the same file — `portfolio_role_ref` and `conviction` are both top-level keys alongside `sector`, `industry`, `themes`, `competitive_advantages`, `risks`, `review`, and `sources`. A future blind-drafting session handed the raw file would see the answer key by construction.

### 7.2 Mechanical redaction, specified (not implemented in this filing)

A single deterministic redaction procedure, reused identically across all 27 tickers, applied to each `intelligence/companies/<TICKER>.yaml` (the paired `.md` thesis narrative is evidence-only by construction — Company Intelligence's own frozen spec never embeds tier/target/gate conclusions in the Markdown file — and passes through unredacted, subject to the same chart-content scan below):

1. **Strip wholesale**: the entire `portfolio_role_ref` key and the entire `conviction` block (`rating` and `rationale` both — `rationale` prose routinely restates or explains the rating, which is itself forbidden).
2. **Strip wholesale**: `review.log`'s narrative entries (free-text `note` fields). Rationale: this is precisely where prior committee/portfolio-policy conclusions leak into prose — e.g. `PI-0018`/`PI-0020`/`PI-0022`'s own "Keep current policy" advisory language is recorded inside exactly this kind of log note on other records. Retain only the structural fields `review.cadence_days`, `review.last_reviewed`, `review.next_due` — dates and cadence carry no policy conclusion.
3. **Scan and strip**: any reference, anywhere in the retained content, to a chart image filename, a `governance/evidence/CHART-0001/` or `governance/evidence/CHART-0002/` path, or a technical/price-action term — a defensive pass; live inspection of all 27 Company Intelligence records found zero such references today (chart evidence lives exclusively under `governance/evidence/CHART-*/`, never inside `intelligence/companies/`), but the mechanical scan step is specified so a future record change cannot silently reintroduce a leak.
4. **Retain unchanged**: `sector`, `industry`, `themes`, `competitive_advantages`, `risks[]` (all sub-fields, including `severity`), `sources[]`. These are the permitted evidence.
5. **Output**: one sanitized YAML per ticker, `<TICKER>.redacted.yaml`, containing only the retained keys above, written to a location outside `intelligence/companies/` (e.g. an ephemeral drafting workspace, never committed as a tracked evidence-of-record file — the redacted package is a drafting aid, not a retained artifact; the retained artifact is the sealed classification record itself plus its evidence citations back to the original, unredacted Company Intelligence record for later Milestone-7 audit).

### 7.3 Determinism and auditability

Because steps 1-4 operate on a fixed, named key list rather than free-form judgment, the same script or process run twice against the same source `main` commit produces byte-identical redacted output — auditable by any future independent reviewer by re-running the same deterministic procedure and diffing. **No redacted package is created and no such script is implemented by this filing** — §7.2 is a complete specification for a future, separately authorized implementation PR to build against, matching this repository's established design-then-implement pattern (`TIER-0002` designed the classification schema itself without creating a single `intelligence/classification/` file).

---

## 8. Sequencing — judgment axes before risk-concentration

Per the authorizing instruction and `TIER-0002` §3.5's own existing design ("risk_concentration is a pure cross-reference rollup... computed after"), a future Milestone 6 per-ticker drafting session must follow this order, with no step skipped or reordered:

1. Generate the sanitized evidence package for the ticker (§7.2).
2. Draft `economic_role` from the sanitized package only (§6.2's forbidden list fully in force, including `caps.clusters`/`issuer_lookthrough.yaml`).
3. Draft `capital_priority` from the sanitized package only (same forbidden list; comparator selection reasoned from `economic_role`'s own output, per `TIER-0002` §3.3's rationale, not from cluster/look-through membership).
4. **Seal both judgment axes** — record them as drafted, timestamped, before any further computation touches the record (§9's sealing metadata applies at this point to the judgment portion).
5. **Only then**, compute `risk_concentration` mechanically from `targets.yaml caps.clusters`, `issuer_lookthrough.yaml`, and `intelligence/relationships/*.yaml` — a pure, deterministic rollup with no discretion, per `TIER-0002` §3.5.
6. Complete `evidence_quality` (`primary_source_coverage`, `highest_disclosed_risk_severity` rollup, and the required `thesis_uncertainty_statement`/optional `review_trigger_notes`).
7. Seal the full four-axis ticker record.
8. Record the record's content hash in the batch's cohort manifest (§9.4).
9. **Stop.** Milestone 7 (baseline reconciliation — comparing the sealed record against current `target_pct`/`portfolio_role_ref`/cluster membership) does not begin in the same PR, session, or drafting pass. A future Milestone 6 implementation PR delivers sealed records only; unblinding and comparison is its own separately authorized future unit.

**Why this order matters.** `risk_concentration`'s three computed sub-fields (`cluster_cap_membership`, `issuer_lookthrough_membership`, `relationship_record_coverage`) are themselves partial signals about which names the allocator's existing policy already treats as concentrated or correlated — reading them before drafting `economic_role`/`capital_priority` would let policy-adjacent structure quietly anchor the two judgment axes the whole blind-classification exercise exists to keep independent. Computing `risk_concentration` only after both judgment axes are sealed removes that channel entirely, without needing to trust drafting-session discipline alone.

---

## 9. Sealing and contamination controls

### 9.1 Per-ticker sealing metadata (specification)

Every sealed Milestone 6 record carries, at minimum, the following seal block (naming convention deliberately mirrors this repository's own `CHART-0002` package-manifest and `intelligence/relationships/*.yaml` lifecycle conventions, so a future reviewer already familiar with either recognizes the shape):

| Field | Purpose |
|---|---|
| `lifecycle_status` | `draft` while a shard session is actively drafting; `sealed` once step 8 above completes; never mutated back to `draft` after sealing (a correction requires a new, separately dated record version, not an in-place rewrite — matching this repository's "never silently rewrite a retained artifact" convention) |
| `sealed_at` | ISO 8601 timestamp of the drafting session's own sealing action |
| `governing_decision` | Pointer to the future Milestone 6 implementation-authorizing decision (not `TIER-0004` itself, which authorizes no classification) |
| `drafting_session_or_shard_id` | Which of the ~5 blind-drafting shards (§11) produced this record — enables later isolation if one shard is found to have a contamination defect without invalidating the other four |
| `schema_version` | Which version of `TIER-0002`'s four-axis schema (plus this filing's `economic_role` abstention amendment, §6) was in force at drafting time |
| `content_sha256` | SHA-256 of the canonical serialized record content, **excluding the seal block itself** (avoiding circular self-hashing) |
| `cohort_manifest_entry` | Pointer to the batch's own cohort manifest file (§9.4) recording this ticker's hash alongside all 26 others |

### 9.2 What this sealing standard does and does not claim

This is a **content-hash-and-timestamp audit trail**, not cryptographic immutability. The repository can enforce that a later diff against a sealed record's own recorded `content_sha256` reveals any post-sealing edit — the same mechanism `CHART-0002`'s `governed_source_sha256`/`retained_sha256` pair already relies on for image integrity. It cannot, on its own, prove a drafting session did not consult forbidden evidence before sealing (§6.2) — that assurance comes from the redaction mechanics (§7, evidence never reaching the session in the first place) and from independent review at merge time, not from the hash. No claim beyond that is made here, matching this repository's own disclosed-limits convention (`CHART-0002`'s own `verifiability_boundary` field draws an identical distinction between what a hash proves and what it cannot).

### 9.3 Contamination controls

- **Redaction-first, not discipline-first**: per §7, the forbidden fields are mechanically absent from the drafting session's own input, not merely instructed-against — the primary control is structural, not behavioral.
- **Shard isolation**: each of the ~5 drafting shards (§11) sees only its own 5-6 tickers' sanitized packages, never another shard's, and never the full 27-ticker set at once during judgment-axis drafting — limiting any single contamination event's blast radius to one shard's tickers.
- **No cross-ticker peeking during judgment drafting**: a shard drafting `economic_role`/`capital_priority` for its own tickers must not consult another ticker's current `target_pct`/tier/gate status even incidentally (e.g. while reading a shared comparison artifact) — comparison artifacts used as evidence (§6.1) must themselves be screened for embedded prior-conclusion language before use, same as any other input.
- **Sealed-before-comparison**: §8 step 9's hard stop before Milestone 7 is itself a contamination control — no reconciliation-driven "let me just double check against the current weight" can occur once a record is sealed, because reconciliation is a structurally separate future unit.

### 9.4 Cohort manifest

One retained manifest per future implementation batch (mirroring `CHART-0002`'s `MANIFEST.json` convention, adapted — no image fields), recording for all 27 tickers: `package_id`, `ticker`, `shard_id`, `sealed_at`, `content_sha256`, `schema_version`, `governing_decision`. **Not created by this filing** — specified for the future implementation PR.

---

## 10. Prior stopped session — contamination result

A prior, separate, unpushed local session reportedly left two untracked files in its own working tree: `classification_validator.py` and `test_classification_validator.py`. Verified this session:

- `git status --porcelain` on this session's own working tree: clean, zero untracked files.
- `find` for `*classification_validator*` anywhere under this repository's working tree: zero matches.
- The reported files were never committed, never pushed to `origin`, and never opened in a PR — they exist, if at all, only in a different session's own local, unreachable filesystem state, outside this session's or any future session's ability to read, copy, adapt, move, stage, delete, clean, or reuse them from here.

**Result: no contamination risk from this source reaches this filing or any future Milestone 6 implementation drawing on this repository's own tracked state.** No cleanup PR is warranted — there is nothing in this repository to clean up. The future validator (§11) must be authored fresh from current `main`, independently, and independently reviewed; it must not be assumed to resemble, and must not attempt to locate or incorporate, the prior session's untracked drafts.

---

## 11. Future validator requirement

A future Milestone 6 implementation PR requires a fresh `classification_validator.py` plus a dedicated `test_classification_validator.py`, authored against `TIER-0002`'s schema as amended by §6 of this filing, from current `main` at implementation time — not adapted from any prior draft (§10). At minimum, the validator must enforce:

- the required four-axis structure (`economic_role`, `capital_priority`, `risk_concentration`, `evidence_quality`) on every sealed record;
- each axis's closed vocabularies (`capital_priority.status` ∈ `{maintain_current_weight, case_for_review, no_assessment}`; `economic_role.economic_system_ref` ∈ the five `ONTO-0001` §D systems, `other: <label>`, or `unable_to_determine` per §6; `evidence_quality.primary_source_coverage` ∈ `{comprehensive, partial, limited, blocked}`);
- the §6 abstention requirements — an `economic_system_ref: unable_to_determine` record must carry both `abstention_reason` and `evidence_gap_statement`, non-empty;
- **no numeric score, weight, or target field anywhere in the schema** — a structural check that the record contains no field parseable as a `target_pct`-shaped number;
- **no forbidden answer-key field** — a record must not contain `portfolio_role_ref`, `conviction`, `target_pct`, or any `caps.clusters`/`issuer_lookthrough.yaml` reference inside the `economic_role` or `capital_priority` blocks specifically (their presence inside `risk_concentration`, computed after sealing per §8, is expected and required);
- valid sealing metadata (§9.1's seven fields, all present, `content_sha256` recomputable and matching);
- manifest/hash consistency — every sealed record's `content_sha256` matches its entry in the batch's cohort manifest (§9.4), and every manifest entry has a corresponding sealed record;
- permitted `lifecycle_status` values only (`draft`, `sealed` — no other value, no silent third state).

**This filing does not implement the validator.** Per this repository's established design-then-implement precedent (`TIER-0002` designed a full four-axis schema with zero `intelligence/classification/` files created; `PI-0002` similarly designed before `PI-0003` implemented), the validator is deferred to the future implementation PR — nothing in the current schema amendment (a single new enum value plus two conditional fields, §6) requires code to exist before the schema itself can be reviewed and accepted.

---

## 12. Economic-role abstention — narrow schema amendment

### 12.1 The gap

`TIER-0002` §3.4's `capital_priority.status` already has a `no_assessment` default value for exactly this situation. `TIER-0002` §3.6's `evidence_quality.primary_source_coverage` already expresses a `blocked` state. `TIER-0002` §3.3's `economic_role`, by contrast, has **no abstention path at all** — its three sub-fields (`economic_system_ref`, `company_role`, `role_basis`) are effectively required, with no value representing "the permitted evidence genuinely does not support determining a role." Live review of the 27-name population (§2.3) found real candidates where this gap could bite: a gated name with only WebSearch-sourced, cross-conflicting evidence (SNPS, ICE, SPGI, WM, RKLB, TSLA), or a company whose disclosed segment structure spans more than one `ONTO-0001` §D system without an evident dominant driver — this filing does not pre-judge which, if any, of the 27 will actually need it, only that the schema must be able to represent the case honestly rather than forcing a low-confidence guess dressed as a determination.

### 12.2 The amendment (smallest compatible change)

Add one new allowed value to `economic_role.economic_system_ref`'s existing enum, alongside the five named `ONTO-0001` §D systems and the existing `other: <label>` escape:

- `unable_to_determine`

When and only when `economic_system_ref: unable_to_determine` is set, the record must additionally carry two new required sub-fields (both absent, and both forbidden, on every non-abstaining record — an abstaining record and a determined record are structurally distinguishable, not just value-distinguishable):

| New sub-field | Type | Requirement |
|---|---|---|
| `abstention_reason` | one sentence | Required when abstaining. States *why* the permitted evidence (§6.1) cannot support a role determination — e.g. "disclosed segments span two ONTO-0001 systems with no evident dominant driver in the permitted evidence" or "primary-source access was blocked and available secondary evidence conflicts on the company's core business description." |
| `evidence_gap_statement` | one sentence | Required when abstaining. Names the *specific* missing or blocked evidence that would resolve the determination — mirroring the same disclosure standard LLY's and RKLB's own Company Intelligence records already apply to their own unresolved items (§3), not a vaguer "insufficient information" placeholder. |

`company_role` and `role_basis` remain **attempted on a best-effort basis** even when abstaining on `economic_system_ref` specifically — a drafting session might still be able to write a short factual `company_role` description ("power-generation and nuclear-services company") while genuinely unable to place the company inside one of the five closed systems. The two are independent: `economic_system_ref: unable_to_determine` does not force `company_role`/`role_basis` to also abstain, and a filled-in `company_role` does not by itself resolve the `economic_system_ref` abstention.

### 12.3 Guardrails against abstention becoming an easy default

- Both new fields are **required, non-empty, one-sentence, specific** — a bare `economic_system_ref: unable_to_determine` with no reason or gap statement is an invalid record under the validator (§11).
- Abstention is scoped to `economic_role` only. It does **not** cascade automatically to `capital_priority` (§3, restated) or to `evidence_quality` — each axis is sealed on its own evidence sufficiency, independently judged.
- The future validator (§11) enforces the structural requirement (fields present when the enum value is used) but cannot, and is not asked to, judge whether an abstention was *substantively* justified — that remains an independent-review-time question, same as every other judgment field in this schema, not a mechanical check.
- This amendment adds **zero** new top-level fields, no fifth axis, no score, and no weighting — it is a single new enum value plus two conditional sub-fields nested inside the existing first axis, the smallest change that closes the identified gap.

### 12.4 What this amendment does not do

It does not redesign `TIER-0002`'s four-axis framework, reopen `capital_priority`'s or `evidence_quality`'s already-adequate abstention/degraded-state paths, or classify any ticker. Whether any of the 27 population members actually uses `unable_to_determine` is a future Milestone 6 drafting-session question, not decided or predicted here.

---

## 13. Future batch and shard structure (recommended, not authorized)

- **All 27 tickers, one coherent future implementation PR** — matching this repository's own `PI-0038`/`PI-0032`/`REL-0003` precedent of bundling multiple independent per-ticker research units into one governance-and-implementation package when each unit is small and the population is already fixed, rather than one-PR-per-ticker (27 PRs) or one-PR-per-pair overhead.
- **Approximately five internal blind-drafting shards of five to six tickers each** — matching `CHART-0002`'s own already-established shard-review precedent (four-to-five-ticker shards, one shard per bounded read-only subagent), reused here for the same reason: keeps each shard's drafting session small enough to review individually while bounding contamination blast radius (§9.3) to one shard's tickers if a defect is later found.
- **One integration and sealing pass** — a single primary session collects all five shards' sealed records, verifies each against the validator (§11), assembles the cohort manifest (§9.4), and confirms no cross-shard duplication or gap across the 27-name population.
- **One independent exact-head review** of the complete batch, under `OPS-0007` §1's capability-based standard — not five separate shard-level reviews, matching `CHART-0002`'s own "one final integration review" convention rather than a review-per-shard design.
- **No separate pilot** — unless that single independent review discovers a genuine architectural defect requiring a scoped redo, in which case the correction follows this repository's own standard bounded-correction-and-re-review cycle, not a new pilot phase.
- **No one-PR-per-ticker design** — rejected as disproportionate process overhead for a fixed, already-reconciled 27-name population with a shared schema and shared redaction mechanics.

**This filing does not authorize this batch.** It is recorded here as the recommended shape for whatever future, separately authorized implementation PR performs Milestone 6 — subject to that future authorization's own scope, which may adopt, modify, or reject this recommendation.

---

## 14. What this filing explicitly does not do

- Does not classify NVDA, LLY, RKLB, or any other ticker under this or any framework.
- Does not create `intelligence/classification/` or any file inside it.
- Does not create a redacted/sanitized evidence package for any ticker.
- Does not implement `classification_validator.py` or its test file.
- Does not read, copy, adapt, move, stage, delete, clean, or reuse the prior stopped session's untracked drafts (§10).
- Does not modify `docs/INVESTMENT_ONTOLOGY.md`, `docs/PORTFOLIO_INTELLIGENCE_SPEC.md`, `TIER-0001`, `TIER-0002`, `TIER-0003`, or any existing Company/Theme/relationship record.
- Does not modify `targets.yaml`, `holdings.yaml`, `gates.yaml`, `issuer_lookthrough.yaml`, `allocate.py`, `levels.py`, or `margin_state.py`.
- Does not perform blind classification, sealing, or any Milestone 7 comparison.
- Does not compute a mechanical score or ranking of any kind.
- Does not authorize Milestone 6 (a future, separate, explicit Step 6 authorization remains required per `operations/WORKSTREAMS.yaml`'s `milestone6-prereq6-fresh-authorization-required` gate, unedited by this filing) or any later WS-0005 milestone.

---

_Retained per `governance/audits/README.md` convention, alongside `WS0005_M5_CLASSIFICATION_QUESTION_INVENTORY_20260804.md`, `WS0005_M5_CANDIDATE_CLASSIFICATION_FRAMEWORK_DESIGN_20260805.md`, `WS0005_M6PREREQ2_CURRENT_ROSTER_FRESHNESS_VERIFICATION_20260805.md`, and `WS0005_M6PREREQ3_CLASSIFICATION_MATERIAL_RELATIONSHIP_GAP_CHECK_20260805.md` — a self-authored implementation-output design and reconciliation artifact, not an independent reviewer's output. Independent review of this artifact and its accompanying PR is the pending next step, per `TIER-0004`._
