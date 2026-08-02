---
decision_id: CHART-0002
date: 2026-08-02
status: Proposed
category: chart_evidence_governance
related_decisions: [GOV-0001, GOV-0002, OPS-0001, OPS-0007, OPS-0009, CHART-0001, PI-0001, PI-0011, LADDER-0001]
supporting_artifact: null
---

## Context

**Preflight performed this session, independently verified, not assumed.** Repository confirmed
`Mast3rkey/Portfolio-HQ`; branch `claude/chart-0002-scale-governance-proposal`; working tree clean;
`origin` fetched and pruned; local `HEAD` and `origin/main` both confirmed at
`9d5d4766a1861e94ddc3aa515578adfd58de5e2e` (the merge commit of PR #221, CHART-0001's pilot
lifecycle-closure sync), zero divergence in either direction. **Zero open pull requests**
(`gh pr list --state open` returns empty). A full local-and-remote branch enumeration (`git branch
-a`, ~90 remote branches) found none naming or concerning `chart-0002`, chart scale-up, or a second
chart pilot. `gh pr list --state all --limit 10` confirms PR #221 `MERGED`. A repository-wide grep of
`governance/decisions/`, `governance/decisions.yaml`, `CLAUDE.md`, and `operations/WORKSTREAMS.yaml`
for `CHART-0002` returns zero hits — the identifier is genuinely unclaimed. The same grep for
`WS-0012` returns zero hits — unused, though its use here is a proposal evaluated in §26 below, not
an assumption. `governance/decisions.yaml` carries 59 entries (one `decision_id:` per file, 1:1
against the 59 files under `governance/decisions/` excluding `README.md`), confirming `CHART-0001` as
the most recently filed decision and `CHART-0002` as the next unused identifier in this domain.
`operations/WORKSTREAMS.yaml` carries `WS-0011` (`status: complete`) as the highest-numbered
workstream — confirming `WS-0012` as the next unused workstream identifier, checked live, not
assumed. `~/Projects/Chart-Automation` exists on disk and is confirmed **not a git repository**
(`git rev-parse --is-inside-work-tree` returns `fatal: not a git repository`) — unchanged from
CHART-0001's own disclosure of the same fact, independently reconfirmed this session rather than
carried over.

**Principal authorization (verbatim, this session):** "I authorize preparation of one narrowly
bounded Lane G governance proposal for scaling the completed CHART-0001 chart-evidence pilot,
provisionally designated CHART-0002 subject to live identifier verification. The proposal may define
a governed multi-chart analysis framework and one small first batch only. It may reuse CHART-0001's
accepted fact/observation/inference/uncertainty separation, privacy standard, provenance and hash
controls, advisory-only status, freshness treatment, and evidence-package pattern. The proposal must
evaluate, rather than assume, whether the work belongs as a new WS-0011 phase or a separate
workstream. The proposed first batch may contain no more than five deterministically selected
tickers and must remain separately gated on an implementation PR, independent exact-head review,
explicit principal acceptance, merge, and post-merge verification. This authorization permits
governance design and drafting only. It does not authorize chart analysis, copying or retaining
additional screenshots, bulk or recurring ingestion, automated chart interpretation, OCR-derived
market data, scoring, ranking, price targets, trading signals, execution instructions, dashboard
integration, Company or Theme Intelligence mutation, LADDER-0001 use, or any tier, target, holdings,
allocation, margin, allocator, brokerage, or trading change." This authorization is narrow and
explicit in the same way CHART-0001's own originating authorization was: it authorizes *preparing*
this proposal, not *accepting* its content. **Nothing in this filing constitutes principal acceptance
of CHART-0002 itself** — this decision's own `status` is `Proposed`, matching CHART-0001's original
filing convention (`governance/templates/decision_template.md`'s status vocabulary), not `Accepted`.
Filing this proposal on a branch and opening a draft PR does not change that.

**The completed CHART-0001 baseline.** CHART-0001 (`status: Accepted`, including its dated
acceptance note and bounded correction) is the accepted, controlling definition for chart-evidence
work in this repository: an advisory Chart Evidence Record logical schema (§3) separating visible
fact from observation/inference/uncertainty; a storage model reusing `governance/evidence/
<decision-id>/` (§4); a privacy standard stricter than `PHQ-2026-06`'s own retained account-summary
image (§5); provenance and claim-boundary rules (§6); a freshness/supersession rule (§7); and one
bounded one-asset/one-screenshot pilot description (§8) that was separately implemented, reviewed,
and accepted. That pilot — one NVDA daily image, `governance/evidence/CHART-0001/
nvda-daily-2026-08-01/` — is independently confirmed present, containing exactly one PNG
(`NVDA__2026-08-01__1D.png`, 656,463 bytes, redacted for a visible TradingView username per §5's
disclosure-not-repeated rule), `record.yaml`, `MANIFEST.json`, and `README.md`, plus its own focused
test module `test_chart_evidence_pilot.py` (confirmed present at the repository root this session).
`operations/WORKSTREAMS.yaml`'s `WS-0011` entry, independently read in full this session, confirms
`status: complete`, `completion_criteria: Met`, `blocker: None`, `active_branch: null`,
`active_pr: null`, and a `next_action` field stating explicitly: **"Any second screenshot,
multi-timeframe validation, batch processing, ingestion system, or other scaling of this pilot
requires its own separate future authorization and governance/design cycle — none is authorized by
this closure."** CHART-0001 §11 independently states the same boundary from the governance-decision
side: no scaling beyond the single pilot record, no batch ingestion of any size, is authorized by
that filing alone. This filing does not edit CHART-0001 or `WS-0011` — both remain closed history,
exactly as merged.

**Why existing authority is insufficient.** CHART-0001 authorizes exactly one image for exactly one
asset; its own §11 and `WS-0011`'s own closure text both say, in their own words, that any scaling
requires a new, separate governance decision. No accepted decision in this repository currently
authorizes chart evidence for more than one ticker, more than one timeframe per ticker, or any
cross-timeframe synthesis of any kind. This filing exists to supply exactly that authorization, bounded
to a governance-design layer plus one small first batch — nothing more.

**Verified governed-library inventory (`~/Projects/Chart-Automation`, read-only, this session).**
`library/governed/2026-08-01/` contains exactly **220 PNG files** across exactly **55 ticker
subdirectories**, each holding exactly 4 files, one per timeframe (`1D`, `1W`, `4H`, `1H`) — a
complete, gap-free 55×4 matrix (independently recomputed via `find`, not read from a prior report:
`find library/governed -iname '*.png' | wc -l` → 220; per-directory file-count histogram → every one
of the 55 directories has exactly 4). All 220 files carry the same capture-batch date,
`2026-08-01`, in their directory and filename structure. `output/governed_copy_manifest_2026-08-01.json`
(`run_status: "COMPLETED — 220 files copied, all post-copy checks passed"`, `entry_count: 220`,
`canonical_tickers` count 55) independently corroborates the same 220/55/4 shape and records, per
entry, a `source_sha256`/`destination_sha256` pair — the sampled entry inspected this session
(`AAPL`/`1W`) shows both hashes identical, confirming hash-verified copy integrity for at least that
entry; the manifest's own `run_status` states this held for all 220. The same manifest records **6
excluded duplicates**, **14 excluded legacy files**, and **10 excluded manual-review items** —
`output/manual_review_queue.md` lists all 10 by name; none is marked as blocking the 220-file
coverage result. A direct grep of the ten items against this filing's five selected tickers (`AMZN,
ASML, AVGO, CEG, COST`) returns zero hits for `AMZN`, `ASML`, `AVGO`, and `COST`, and exactly one hit
for `CEG` — the "Batch 03 - Financial Infrastructure" item, an administrative note that a *source
intake folder* was mislabeled ("Folder name says 'Financial Infrastructure' but contains CEG, ETN,
GEV, PWR, VRT"). That note concerns source-folder naming and organization during curation, not any
privacy, quality, hash, corruption, or chart-content defect in CEG's own canonical governed images —
CEG's four retained `1D`/`1W`/`4H`/`1H` files are independently confirmed present in
`library/governed/2026-08-01/CEG/` and absent from both the manifest's 6 excluded duplicates and 14
excluded legacy files. Accordingly, none of the five selected canonical image sets currently carries
an individual-image manual-review flag — this is disclosure, not privacy approval, and each of the
five images still requires the independent, repository-grade privacy review defined below during a
future, separately authorized implementation PR. Two of the ten manual-review items are independently notable for
this filing's privacy discussion: one flags an already-excluded non-chart screenshot showing "a
Robinhood brokerage positions/balances view containing account-level financial data," confirming the
broader source material this governed library was curated from does contain brokerage-sensitive
images that were correctly kept out of the 220-file governed set — the governed library itself is
chart-only, but nothing in its manifest asserts any of the 220 remaining chart images has itself
received the kind of individual, repository-grade privacy review CHART-0001 §5 requires before
retention (CHART-0001's own single retained image needed exactly one such review, which found and
required redacting a visible platform username). **No privacy-grade review of any of the 220 images
has occurred in this repository** — this filing performs none, and authorizes none beyond the first
batch's own future implementation PR.

**Repository-size consequence, computed directly.** `du -sh library/governed` reports **393 MB**
across the 220 governed images (~1.8 MB average per image, verified against a 4-file sample). By
contrast, the one CHART-0001 image actually retained in this repository is 656,463 bytes (~0.64 MB)
after privacy-redaction and recompression. Retaining all 220 images verbatim would add roughly 600x
the footprint of the single existing pilot artifact to this repository — a fact this filing discloses
to ground §9's storage-and-retention decision and §14's bounded first-batch scope, not to authorize
any such retention.

**Portfolio-HQ roster cross-reference (live, this session, not from a prior report).**
`targets.yaml`'s `destination` list carries 36 entries; excluding the six non-equity rows (`BTC`,
`ETH`, `SOL`, `GLD`, `CASH`, `RESERVE`) leaves **30 canonical equity/fund tickers**, of which 6 are
actionable-gated per `gates.yaml` (`SNPS`, `ICE`, `SPGI`, `WM`, `RKLB`, `TSLA`). `intelligence/
companies/*.yaml` carries **45 Company Intelligence records** (many for tickers no longer in the
canonical roster after `PHQ-2026-02`'s migration, per `PI-0035`'s own retained/historical
classification — unaffected by this filing). The intersection of canonical-destination tickers and
Company-Intelligence-covered tickers is **exactly 19 names**: `AMZN, ASML, AVGO, CEG, COST, ETN,
GEV, GOOGL, ISRG, KLAC, LLY, META, MSFT, NVDA, PANW, PWR, TMO, TSM, V`. Every one of these 19 is
independently confirmed present in the 55-ticker chart library — the three-way intersection
(canonical ∩ Company-Intelligence ∩ chart-library) is identical to the two-way one, 19 names, no
narrowing. None of the 19 is an actionable-gated name (independently confirmed: all six gated names
fail the Company-Intelligence-coverage test, since `PI-0033`/`PI-0035` left every gated name without
a Company Intelligence record). Four canonical tickers (`RKLB`, `SNPS`, `SPGI`, `WM` — all four also
gated) have no chart-library coverage at all; eleven canonical tickers (`GNRC, ICE, RKLB, RTX, SNPS,
SPGI, SPY, TSLA, VEA, VWO, WM`) have no Company Intelligence record. §18 below addresses each gap
category explicitly.

## Decision

**CHART-0002 authorizes exactly the preparation, definition, and independent review of this
proposal — nothing more.** It commits no chart evidence, retains no additional screenshot, creates no
Chart Evidence Record, creates no cross-timeframe synthesis record, and touches no image outside this
governance filing's own read-only, fact-gathering use of `~/Projects/Chart-Automation`'s existing
manifests and filesystem structure. If, and only if, this proposal is later independently reviewed
and explicitly accepted by the principal — a status change this filing does not itself make — it
would then authorize exactly one future, separate, bounded implementation PR for one small first
batch of no more than five tickers per §14 below, itself gated on its own full review and merge
cycle. No implementation begins in this session, and none may begin before that future acceptance.

### 1. Purpose and status

This is an advisory, governance-design *proposal* only, defining a controlled, bounded expansion path
from CHART-0001's single-image pilot to a governed multi-chart analysis framework. If accepted, chart
evidence produced under it remains — exactly as CHART-0001 §1 established — supplementary, dated,
non-authoritative, and subordinate to the Investment Constitution, every accepted governance decision,
`holdings.yaml`, `targets.yaml`, current Company/Theme Intelligence, and executable allocator policy,
at or below level 7-8 of `GOV-0002`'s precedence hierarchy. This filing itself commits no evidence,
retains no image, and does not become effective until independently reviewed and merged — and even
then, only the governance text (§§1-27 below) becomes effective; the first batch itself requires its
own further, separate implementation PR under its own full review cycle (§14, §19-20).

### 2. Explicit non-authority

This decision authorizes **none** of the following, now or as an implied consequence of anything
below, without its own separate, later, explicitly accepted governance decision — restated from
CHART-0001 §2 and extended to the multi-chart/batch case:

- processing, retaining, or analyzing any of the 220 governed chart images beyond the first batch's
  own five-image (or fewer) scope defined in §14;
- bulk screenshot ingestion of any kind, in this filing or the future first-batch implementation;
- recurring or automatic ingestion, scheduled capture, or any standing monitoring process;
- automatic chart interpretation (OCR-driven or otherwise) as a substitute for human-reviewed analyst
  judgment;
- OCR-derived market-data authority of any kind — no chart-derived figure may be treated as a price,
  quantity, or market datum for any production purpose;
- chart-pattern systems (flags, head-and-shoulders, wave counts, or any comparable automated pattern
  classifier) — unchanged from the Decisions Log's "not computable, not backtestable" ruling and
  CHART-0001 §2's own restatement of it;
- scoring, ranking, aggregation into a capital-priority score, or any technical-signal generation of
  any kind;
- price targets, opportunity maps, or trading signals/recommendations worded as execution
  instructions;
- any change to tiers, targets, weights, holdings, buys, trims, sells, margin, allocator output,
  brokerage behavior, or trading behavior of any kind;
- use as `LADDER-0001` study or backtest input — `LADDER-0001` protocol §8's exclusion of
  chart-pattern/screenshot-derived input is untouched, unnarrowed, and unreinterpreted by this filing;
- use as a substitute for primary-source fundamental evidence in any Company or Theme Intelligence
  record;
- direct mutation of any existing Company or Theme Intelligence record, or extension of the frozen
  Company Intelligence schema (`docs/PORTFOLIO_INTELLIGENCE_SPEC.md` §9/§20/§24) in any respect —
  chart evidence remains a wholly separate, independent record type;
- dashboard implementation, integration, or display of any kind (`OPS-0011`/`OPS-0012`/`OPS-0013`
  remain entirely unaffected and untouched);
- any order placement or brokerage action of any kind;
- authorizing the remaining 15 (of 19 eligible) or 220 (of the full library) chart images merely
  because the first batch is proposed, or later, merely because it passes review — restated in full
  in §25/§28.

### 3. Two-stage advisory evidence architecture

If this proposal is later accepted, a future implementation may define — but does not define here as
executable code, a schema file, or a validator — a two-stage logical record architecture:

- **Stage 1 — image-level Chart Evidence Record.** Exactly CHART-0001 §3's existing logical schema
  (Identity & capture; Content — fact/observation/inference/uncertainty; Governance & advisory
  content; Relationships; Lifecycle), unmodified, applied per retained image. Each Stage 1 record
  is self-contained and independently reviewable, matching CHART-0001's own single-record precedent.
- **Stage 2 — ticker-level cross-timeframe synthesis record.** A new record type, referencing two or
  more Stage 1 records for the *same ticker* across *different timeframes* (e.g., a ticker's `1D` and
  `1W` records). A Stage 2 record contains no independent visible-fact content of its own — every
  fact or observation it discusses must trace to a specific Stage 1 record it cites. Its purpose is
  narrow: reconcile what the same ticker's different timeframes show, per §5's conflict-handling rule,
  never to produce a new synthesized "view" that outranks or overrides any individual Stage 1 record.
  A Stage 2 record is optional per ticker — it exists only where a ticker's batch actually includes
  more than one timeframe (see §14: the first batch does not).

No numeric technical score, composite rating, automatic classification, or capital-priority ranking is
part of either stage, now or under any future batch without its own separate authorization. As with
CHART-0001 §3, this section describes a logical shape only — no schema file, validator, or record is
created by this filing.

### 4. Fact/observation/inference/uncertainty separation

Unmodified from CHART-0001 §3's "Content" field group, reused here by reference rather than restated:
every Stage 1 record must keep visible facts, observations, inferences, and disclosed uncertainty in
distinct, labeled fields; a Stage 2 record inherits the same discipline for whatever it says about the
relationship between two Stage 1 records' facts/observations/inferences. Nothing here loosens
CHART-0001 §3's standard.

### 5. Cross-timeframe conflict handling

A Stage 2 record, if a future batch includes one, must record, without silently resolving:

- **agreement** — where two or more timeframes' Stage 1 records show consistent visible facts or
  observations for the same ticker (e.g., both timeframes show the same directional trend);
- **conflict** — where timeframes disagree (e.g., a daily chart shows a recent pullback that a weekly
  chart's longer view does not register as significant) — recorded as a disclosed conflict, never
  averaged, scored, or silently resolved into a single "correct" reading;
- **uncertainty** — where a timeframe's own Stage 1 record already disclosed uncertainty (illegible
  detail, ambiguous level) that limits how confidently a cross-timeframe comparison can be drawn;
- **missing evidence** — where a ticker's batch does not include every timeframe needed for a
  complete comparison (e.g., only `1D` and `1W` are available, not `4H`/`1H`) — disclosed as a scope
  limitation of the Stage 2 record, never treated as agreement by default.

A Stage 2 record that cannot cleanly separate these four categories must abstain from drawing any
cross-timeframe conclusion for that ticker, per §22.

### 6. Privacy

Unmodified, and reused by reference, from CHART-0001 §5 — the same standard, including its named,
bounded username exception (approved only for the specific CHART-0001 NVDA image, recorded in that
image's own manifest, not extended by this filing to any other image). Every image considered for
retention under a future batch requires its own **independent, per-image privacy review**, recorded in
that image's own package manifest — CHART-0001's five bulleted privacy rules apply identically,
per-image, to every image in a multi-image batch; a batch does not receive one shared privacy
clearance. As the Context section discloses, **none of the 220 governed images, including the five
named in §14, has received this review yet** — this filing performs none. An image that cannot be
made safe must be rejected outright for that image specifically; a batch's other images are not
affected by one image's rejection (§21).

### 7. Provenance and hash requirements

Unmodified, and reused by reference, from CHART-0001 §6, applied per image: source platform and
capture time (with timezone); retained filename (subject to §6 above); SHA-256 of the retained copy;
analyst/model and session attribution; explicit uncertainty disclosure; an explicit statement that a
chart screenshot is secondary observational evidence, never inspected primary evidence; claim-level
linkage to any related holding, Intelligence record, or governance decision; principal acceptance
recorded as its own field, separate from authorship. A Stage 2 record additionally carries its own
provenance (which Stage 1 records it references, by evidence ID and hash) — it introduces no new
image and computes no new image hash of its own.

### 8. Storage and repository-size policy

If accepted, a future first-batch implementation is authorized to use exactly the same bounded hybrid
model CHART-0001 §4 already established — `governance/evidence/CHART-0002/<batch-slug>/` (a sibling
of, not nested inside, `governance/evidence/CHART-0001/`, since this is a separate decision), one
package per ticker (image, structured `record.yaml`, `MANIFEST.json`, `README.md`), reusing this
repository's existing evidence-package/manifest/hash pattern rather than inventing a new subsystem or
a new top-level directory. No `chart_evidence/index.yaml` or comparable index file is created — the
filesystem-as-index doctrine (`PI-0001`, reaffirmed for Theme Intelligence by `PI-0006`) remains the
default starting point for any future indexing question, not decided here. Given the Context section's
393 MB/220-image size disclosure, this filing explicitly bounds any future retention to the small
first batch defined in §14 (at most five images, an estimated ~5-9 MB based on the ~0.64-1.8 MB
per-image range already observed in this repository and the source library) — no larger retention is
authorized by this filing, and any future expansion must independently justify its own additional
repository-size cost, per §25's stopping conditions (unchanged from CHART-0001 §10's own final
bullet).

### 9. Image retention: pixels retained, not externally referenced

If accepted, a future first-batch implementation retains each selected image's **actual pixels**, as a
byte-for-byte (post-redaction) copy inside `governance/evidence/CHART-0002/<batch-slug>/` — matching
CHART-0001 §4's own choice and this repository's general evidence-retention convention (`PHQ-2026-01`
through `PHQ-2026-06`, `PHQ-2026-06`'s own retained webp). An external-reference-only model (storing a
path or hash pointing at `~/Projects/Chart-Automation`, without a repository-local copy) was
considered and rejected: `~/Projects/Chart-Automation` is confirmed not a git repository, is outside
this repository's own version control, and is explicitly out of scope for this filing to write into —
a reference-only record would be unverifiable and unreproducible the moment that external, uncontrolled
directory changes or is deleted, defeating the entire evidentiary purpose CHART-0001 §6 already
established. Retained pixels remain historical archive evidence only (CHART-0001 §4's own rule,
reused unmodified) — never live market-data authority, never read by production code as a price or
quantity source.

### 10. Advisory relationship to Company and Theme Intelligence

Unchanged from CHART-0001 §2's explicit non-authority list: chart evidence, at any scale this filing
or a future accepted batch reaches, is never written into `intelligence/companies/*.yaml` or `*.md`,
never extends the frozen Company Intelligence schema, and is never treated as a substitute for
primary-source fundamental evidence in any Company or Theme Intelligence record. A Chart Evidence
Record's "related Company/Theme Intelligence records" field (Stage 1, per §3) is reference-only — it
may name an existing record for cross-check context, and must never be read in reverse as authorizing
any edit to that record.

### 11. Freshness, expiration, and supersession

Unmodified, and reused by reference, from CHART-0001 §7, per image and per Stage 2 record: a chart
screenshot is point-in-time evidence; a review/expiration schedule proportional to the asset and
timeframe captured is required (daily goes stale faster than weekly); staleness requires disclosure
or analyst abstention, never an automatic demotion, sale, target change, or policy change; a refresh
creates a new record, never an overwrite, linked via `supersedes`/`superseded_by`. No standing
monitoring system, scheduled recapture, or automated staleness scanner is authorized — matching
`LADDER-0001`'s and `OPS-0006` §15's own explicit prohibitions.

### 12. Human-review versus safe factual automation boundary

Every Stage 1 record's content (visible facts, observations, inferences, uncertainty disclosures) is
human-authored and human-reviewed — no automated chart interpretation, OCR-derived reading, or
model-generated technical judgment substitutes for that review, per §2. Bounded, safe, purely
mechanical automation is permitted only for: computing a file's SHA-256; verifying a manifest's hash
matches its retained file; confirming a package contains the expected file set (matching
`test_chart_evidence_pilot.py`'s own existing test shape); and confirming cross-references (a Stage 2
record's citations resolve to Stage 1 records that actually exist). None of this mechanical automation
may generate, infer, or alter any fact, observation, inference, or advisory content — it may only
verify structural/hash integrity of content a human already authored.

### 13. Deterministic first-batch selection rule

The rule, applied against live repository and library data this session, not against any prior
report's claimed result: **alphabetical order among tickers that carry both (a) a canonical
`targets.yaml` destination entry and (b) an existing Company Intelligence record
(`intelligence/companies/<TICKER>.yaml`)**, further requiring (c) presence in the governed
chart-library's 55-ticker set (independently confirmed to add no narrowing — see Context) and (d)
absence from `gates.yaml`'s actionable-gated list (independently confirmed already satisfied by every
member of the (a)∩(b) intersection). This rule is neutral by construction: it does not reference
conviction rating, tier weight, expected return, price action, portfolio priority, or any analyst
preference — only two objective, independently verifiable facts (a governed destination weight exists;
a Company Intelligence record exists) and two exclusion checks (chart coverage exists; the name is not
gated). The full ordered eligible set, computed this session: `AMZN, ASML, AVGO, CEG, COST, ETN, GEV,
GOOGL, ISRG, KLAC, LLY, META, MSFT, NVDA, PANW, PWR, TMO, TSM, V` (19 names).

### 14. First batch: exact tickers and timeframe scope

**Proposed first batch (first 5 of 19 in alphabetical order): `AMZN, ASML, AVGO, CEG, COST`.** All
five independently confirmed this session to have exactly 4 governed chart images each (`1D`, `1W`,
`4H`, `1H`, captured `2026-08-01`) in `~/Projects/Chart-Automation`, with no individual-image
manual-review flag against any of the five (`CEG` appears once in the manual-review queue, but only
in the "Batch 03 - Financial Infrastructure" administrative source-folder naming note discussed in
the governed-library inventory section above — not a flag on CEG's own canonical images). `NVDA` —
already carrying a CHART-0001 record — falls later alphabetically
(6th of 19) and is not reached by this batch; no special-casing was needed to exclude it.

**Timeframe scope: `1D` (daily) only — one image per ticker, five images total, Stage 1 only.** Both
options were evaluated:

- *Five tickers × four timeframes (20 images, full Stage 1 + Stage 2 for all five).* Rejected for
  this first batch. It would exercise two genuinely new architectural axes simultaneously — multiple
  tickers (new since CHART-0001's single asset) and multiple timeframes per ticker with cross-timeframe
  synthesis (new since CHART-0001's single timeframe) — conflating two independent sources of
  implementation risk in one PR. Review cost quadruples (20 independent images plus up to 5 Stage 2
  synthesis records, versus 5 images and zero Stage 2 records). Privacy burden quadruples (20
  independent per-image reviews, per §6, versus 5) with no evidence yet that the per-image privacy
  process scales cleanly across a batch at all. Failure isolation is worse: if a systemic issue
  surfaces (a privacy-redaction gap, a hash-reconciliation bug, a fact/inference-boundary drafting
  error) partway through a 20-image batch, more work is exposed to that failure before it is caught.
- *Five tickers × one timeframe (`1D`), 5 images, Stage 1 only.* **Selected.** This is the smallest
  batch that meaningfully advances the architecture beyond CHART-0001's own single-image precedent —
  it tests the genuinely new capability (independent per-ticker Stage 1 records processed and reviewed
  as a batch, with per-image failure isolation per §21) without also taking on Stage 2 cross-timeframe
  synthesis in the same implementation PR. Review cost and privacy burden both stay at 5 independent
  units — comparable in scale to CHART-0001's own single-image review, multiplied by five, not by
  twenty. Cross-timeframe value (the entire point of Stage 2) is real but is better evaluated once
  Stage 1 is proven to work cleanly across more than one ticker — this mirrors this repository's own
  repeated incremental-axis discipline (e.g. `PI-0003`'s "one company beats every alternative... more
  companies intentionally deferred" reasoning, applied here to timeframes instead of companies).
  Stage 2 synthesis, and any batch that includes more than one timeframe per ticker, remains explicitly
  unauthorized by this filing and requires its own future, separate batch authorization once Stage 1
  at multi-ticker scale has actually been implemented, reviewed, and accepted.

This batch therefore produces, if separately implemented and accepted: 5 retained images, 5 Stage 1
Chart Evidence Records, 0 Stage 2 records, under `governance/evidence/CHART-0002/<batch-slug>/`.

### 15. Batch acceptance criteria

A future first-batch implementation, if separately authorized and attempted, must satisfy, at minimum,
before its own PR may merge — extending CHART-0001 §9 from one image to a five-image batch:

- each of the five source images is reliably identified and independently SHA-256-verified against
  the governed library's own manifest;
- each image passes its own independent privacy review per §6, with any redaction disclosed
  per-image;
- each Stage 1 record cleanly distinguishes fact, observation, inference, and uncertainty per §4 — no
  field blurs the boundary, for any of the five;
- no indicator setting, date, or price level is invented for any of the five — unknowns recorded as
  unknown;
- no numeric score, composite rating, or trading signal is produced for any ticker;
- no allocator, margin, holdings, target, Company/Theme Intelligence schema, dashboard, or brokerage
  coupling is introduced anywhere in the implementation;
- every relationship link in every record resolves to something that actually exists;
- each record's freshness/review-date and supersession fields validate against §11;
- independent review is attributable (a retained GitHub review/comment thread or a `governance/
  audits/` artifact) and anchored to the exact final head, per `OPS-0007` §1;
- the principal explicitly accepts the batch at that exact final head before merge;
- the batch contains exactly the five named tickers, one `1D` image each, and zero Stage 2 records —
  any deviation (fewer, more, a different ticker, a different timeframe, or any Stage 2 content)
  requires stopping and returning for principal amendment, not silent substitution (§21-22).

### 16. Tests and validators required for a later implementation

A future implementation PR must include focused, package-scoped tests mirroring
`test_chart_evidence_pilot.py`'s existing shape, extended for a five-package batch: package-shape
tests (each of the five package directories contains exactly one image plus `record.yaml`,
`MANIFEST.json`, `README.md`); no-second-image/no-sixth-package tests; hash-reconciliation tests per
package; fact/observation/inference/uncertainty-separation assertions per record; draft-stage
governance-invariant assertions (reviewer/reviewed_head/principal_acceptance null, `lifecycle_status:
drafted`) before acceptance. No new validator framework is authorized — extending the existing focused
test file's pattern is sufficient, matching CHART-0001 §8's own "one focused package-integrity test"
precedent.

### 17. Review weight

Full `OPS-0009` Lane G throughout, unreduced — this is a new governance authorization (this filing)
followed by a new implementation PR (the future first batch), exactly CHART-0001's own treatment.
`OPS-0007` §1's twelve-point capability-based independent-review standard applies to both this
governance filing and the future implementation PR, each requiring its own separate exact-head review.

### 18. Treatment of assets lacking targets, Intelligence, holdings, or chart coverage

Four gap categories, addressed explicitly rather than left implicit:

- **Lacking a canonical target/destination entry** (e.g., most of the 45 Company-Intelligence-covered
  tickers that predate `PHQ-2026-02`'s migration — `AAPL, ABBV, AMAT, AMD, BRK.B, CRM, CRWD, CVX,
  GILD, IBM, INTC, JNJ, JPM, LRCX, MA, MLM, MRK, MRVL, MU, NOW, ORCL, SKHY, VRT, WDC, WMT, XOM`):
  ineligible for selection under §13's rule and not addressed by this filing at all — no chart
  evidence, no batch inclusion, no disposition. A future batch proposal could name any of these
  explicitly, with its own selection rationale; none is authorized here.
- **Lacking a Company Intelligence record** (`GNRC, ICE, RKLB, RTX, SNPS, SPGI, SPY, TSLA, VEA, VWO,
  WM` — canonical but uncovered): excluded from §13's eligible set by construction (the rule requires
  a Company Intelligence record specifically so a future Stage 1 record's "fundamental cross-checking
  required" field, per CHART-0001 §3, has something to reference). Six of these eleven are also
  actionable-gated (`SNPS, ICE, SPGI, WM, RKLB, TSLA`) and independently excluded on that basis too.
  No chart evidence for any of these eleven is proposed or authorized here.
- **Lacking a current holding position:** not a §13 eligibility criterion at all — a canonical
  destination weight and a Company Intelligence record are both forward-looking/structural facts, not
  contingent on current share ownership, and CHART-0001's own record schema (§3, "related holdings")
  already treats a holding link as optional context, not a precondition. No current-holdings check was
  applied or is required.
- **Lacking chart-library coverage** (`RKLB, SNPS, SPGI, WM` — canonical but no governed images):
  independently confirmed to produce no narrowing beyond the Company-Intelligence gap above (all four
  already excluded for lacking a Company Intelligence record). At present, every canonical ∩
  Company-Intelligence ticker also has full chart-library coverage — no eligible-but-uncharted gap
  exists in the live data as of this session. If that ever changes (a future canonical/Intelligence
  addition outpaces the external chart library), a future batch proposal must disclose the gap rather
  than silently skip or substitute the affected ticker.

### 19. Separate implementation-PR requirement

Unchanged from CHART-0001 §8's own gating: if this proposal is accepted, the first batch requires its
own future, separate implementation PR — not opened, drafted, or begun by this filing — containing
exactly the five image packages, their tests, and no other repository change. That PR must itself stay
in draft state pending its own independent review.

### 20. Principal acceptance, merge, and post-merge verification requirements

Identical three-gate discipline to CHART-0001 §14 and every other Lane G filing in this log:
independent exact-head review under `OPS-0007` §1 (including disclosure of author/reviewer/session/
model overlap); any required bounded correction and exact-head re-review; explicit principal
acceptance at the exact final head before merge; and, once merged, post-merge verification per
`OPS-0009` §4(a) (hash reconciliation, focused-test re-run, full-suite re-run, protected-path diff,
decision-index reconciliation) — matching `WS-0011`'s own `post-merge-hash-and-register-verification`
milestone precedent exactly.

### 21. Failure isolation

Each of the five image packages in a future first batch is independently reviewable, independently
acceptable, and independently rejectable — a privacy, provenance, or fact/interpretation-boundary
failure discovered in one ticker's package (e.g., an unsafe image that cannot be redacted per §6) does
not by itself invalidate the other four. A future implementation PR that cannot complete all five must
disclose exactly which succeeded, which failed, and why (per §22) — it must not silently narrow the
batch to fewer tickers without disclosure, matching the "no silent scope contraction" discipline
`PI-0024`/`PI-0026`/`PI-0029`/`PI-0031` already established for Company Intelligence batches in this
repository. A batch that cannot complete at least a majority of its five tickers must stop and return
for principal amendment rather than merge a materially shrunken batch silently.

### 22. Abstention behavior

Where an image cannot be safely retained (§6), a detail cannot be established without invention (§4),
or a cross-timeframe comparison cannot cleanly separate agreement/conflict/uncertainty/missing-evidence
(§5 — not applicable to this first batch, which contains no Stage 2 records, but binding on any future
batch that does), the correct behavior is disclosed abstention for that specific item — proceeding with
no record for that ticker or that comparison — never invention, never silent omission, never a
best-guess substitute. This mirrors CHART-0001 §5's own "reject outright... the pilot proceeds with no
evidence for that asset" rule and `OPS-0006` §14's staleness-abstention precedent.

### 23. Rollback behavior

If a future first-batch implementation PR is merged and a post-merge or later independent review finds
a MATERIAL defect in one or more packages (an undisclosed privacy gap, a fabricated fact, a broken
hash), the correct remedy is a narrow, disclosed correction PR to the affected package(s) specifically
— matching this repository's own "bounded correction" convention (`OPS-0009` Lane C; CHART-0001's own
two same-PR bounded corrections) — not a silent rewrite and not treating the whole batch as
irretrievably compromised if only one package is affected. If a defect cannot be corrected without
reintroducing an unsafe image or an invented fact, the affected package must be removed (image deleted,
record marked withdrawn with the reason disclosed) rather than left in a known-bad state — mirroring
CHART-0001 §10's stopping-condition discipline applied post-merge.

### 24. Completion criteria

This proposal's own completion (this filing, Lane G) is met when: independently reviewed under
`OPS-0007` §1; any required bounded correction made and re-reviewed; explicitly principal-accepted at
the exact final head; and merged to `main`. **This alone does not complete or begin the first batch** —
the batch's own completion criteria are §15's acceptance criteria, satisfied only by its own future,
separately reviewed, separately accepted, separately merged implementation PR, plus its own post-merge
verification per §20.

### 25. Stopping conditions

A future first-batch attempt must stop, or be rejected outright, if any of the following holds —
extending CHART-0001 §10 to the five-ticker case:

- any of the five source images cannot be reliably identified;
- required metadata (capture time, source platform, asset, timeframe) cannot be established without
  invention, for any of the five;
- sensitive information in any image cannot be safely redacted consistent with §6;
- the analysis cannot cleanly separate visible fact from interpretation, for any of the five;
- the implementation attempts to introduce technical scoring, prediction, an automatic recommendation,
  or any allocator/trading coupling of any kind;
- the implementation attempts to include a sixth ticker, a second timeframe per ticker, or any Stage 2
  synthesis record — none of which this filing authorizes;
- satisfying the batch would require weakening any existing paper-only, read-only, secrets-handling, or
  no-order safeguard anywhere in this repository;
- the change cannot be implemented as a small, reversible unit;
- the claimed utility does not justify the resulting repository size, review burden, or maintenance
  cost, given §8's disclosed size figures.

### 26. Workstream treatment

**Evaluated explicitly, not assumed — see the four alternatives in the Alternatives Considered
section below.** This filing establishes a **new workstream, `WS-0012`**, in `operations/
WORKSTREAMS.yaml` (`status: proposed`, `priority: secondary` — `WS-0005` remains the repository's
sole `priority: primary` workstream, unaffected by this filing), rather than adding a phase to the
existing `WS-0011` entry. `WS-0011`'s own text — both CHART-0001 §11's governance-side prohibition and
`WS-0011`'s own `next_action`/`blocker` fields, quoted in full in the Context section above — states in
its own words that scaling "requires its own separate future authorization and governance/design
cycle" and that its own closure authorizes "none" of any second asset or scaling. `WS-0011`'s `status`
is `complete`, its `completion_criteria` is `Met`, and its `blocker` is explicitly `None`; reopening it
to host a phase of new work would require editing or reinterpreting that closure language, which the
Context section's "does not falsely rewrite or reopen the completed pilot lifecycle" concern (matching
this repository's own `governance/decisions/README.md` "never edit a file's substance after `status:
Accepted`" convention, applied here to a completed workstream register entry by the same logic) counsels
against. `WS-0012` instead follows the `LADDER-0001`/`WS-0010` precedent directly: a genuinely new,
bounded charter (there: a backtest research protocol; here: a multi-chart evidence framework), each
authorized by its own new decision-domain filing, tracked by its own new, separately-gated, initially
`proposed` workstream entry, leaving the entry it is conceptually adjacent to (`WS-0001`/margin research
in `LADDER-0001`'s case; `WS-0011`/the closed pilot in this case) completely untouched. `WS-0012`'s own
entry is modeled directly on `WS-0010`'s existing shape (title, objective, `governing_authority`,
`status: proposed`, `authorized_scope: None yet — effective only upon this decision's governance PR
merging`, `prohibited_scope` mirroring §2/§28, one `governance-pr-drafted` milestone, `completion_
criteria: Not met`, `blocker` naming this PR's own pending review, `active_branch:
claude/chart-0002-scale-governance-proposal`, `active_pr: null`, `authorized_by: null`).

### 27. Governance package scope (this filing)

This filing touches exactly:

1. `governance/decisions/CHART-0002-bounded-multi-chart-evidence-framework-proposal.md` (this file).
2. `governance/decisions.yaml` (index regeneration: one new entry for `CHART-0002`, 59→60 entries).
3. `operations/WORKSTREAMS.yaml` (one new entry, `WS-0012`, per §26 above).
4. `CLAUDE.md` (one concise Decisions Log pointer entry, worded to reflect `Proposed`, not `Accepted`,
   status — matching CHART-0001's, `LADDER-0001`'s, and every other filing's unbroken convention).
5. `test_portfolio_hq_dashboard_decisions.py` — two hardcoded decision-count assertions (and one test
   function name) bumped `59`→`60`, mechanically, to keep this existing dashboard validator's own
   real-repository reconciliation check accurate against the new entry from item 2 above. No other
   line in this file is touched. This mirrors CHART-0001's own PR (`aa66f24`), which made the
   identical `58`→`59` bump for the identical reason when it added its own entry — a precedent
   independently confirmed via `git log`/`git show` this session, not assumed.

**No other file is touched.** No chart image, no chart analysis, no `chart_evidence/` directory, no
Company/Theme Intelligence file, no other dashboard code (`portfolio_hq/dashboard/**` itself is
untouched — only the one test file's hardcoded counts, per item 5), no `holdings.yaml`/
`targets.yaml`/`gates.yaml`/`issuer_lookthrough.yaml`, no `allocate.py`/`margin_state.py`/`levels.py`,
no Constitution text, no `research/buy_ladder_backtest/**` file, no `CHART-0001` file, and no file
under `~/Projects/Chart-Automation` or `~/Downloads` is touched by this filing.

### 28. Prohibited scope, restated in full

Unless separately authorized later, this filing prohibits: processing all 220 governed images;
processing any of the remaining 14 (of the 19) eligible-but-unselected tickers, or any of the 36
canonical-but-ineligible or uncovered tickers named in §18, without a future, separate batch
authorization naming them explicitly; bulk image retention beyond the five named in §14; recurring or
scheduled ingestion; automatic screenshot capture; OCR-derived market-data authority; automated chart
interpretation; automated pattern classification; technical scoring; ranking; aggregation into a
capital-priority score; price targets; trading signals; execution instructions; dashboard integration;
portfolio-allocation coupling; tier or target changes; holdings changes; margin changes; allocator
changes; brokerage actions; `LADDER-0001` input; direct Company or Theme Intelligence mutation; frozen
Intelligence-schema extension; silently dropping a failed timeframe or package without disclosure;
treating a missing or privacy-failed image as neutral evidence; using stale chart evidence without
disclosure or abstention; and authorizing later batches, a sixth ticker, a second timeframe per
ticker, or any Stage 2 record merely because the first batch is proposed or, later, merely because it
passes review.

### 29. Effectiveness, review, and merge gates

This governance PR must remain in **draft** state. Before it may even be considered for independent
review as a candidate for merge, it requires, in this order: (a) independent, exact-head review by an
eligible reviewer per `OPS-0007` §1; (b) any required bounded correction and exact-head re-review; and
(c) **explicit principal acceptance of CHART-0002's own content** — a distinct, later step from the
principal's authorization to prepare this proposal, which this filing does not claim to have received.
**This decision does not mark itself ready, does not authorize its own merge, and does not authorize
beginning the §14 first-batch implementation.** Nothing in §§1-28 above becomes effective until this PR
merges to `main`, and even then, only the governance text itself takes effect — the first batch remains
gated on its own further, separate implementation PR and review cycle.

### 30. No chart analyzed or retained by this filing

This filing performed no chart analysis and retained no chart image. Every fact stated about the 220
governed images, the 55-ticker/4-timeframe matrix, or the five selected tickers' file presence and
capture metadata was drawn from `~/Projects/Chart-Automation`'s own existing filesystem structure and
its own pre-existing manifest/report files (`output/governed_copy_manifest_2026-08-01.json`, `output/
manual_review_queue.md`), read-only, without opening any PNG for visual/investment interpretation. No
chart image, extracted chart fact, or chart-derived observation appears anywhere in this filing.

### 31. Accepting this proposal authorizes only the first batch

If this proposal is later accepted, that acceptance authorizes exactly §14's five-ticker,
daily-only, Stage-1-only first batch — via its own further, separate, gated implementation PR — and
nothing more. It does not authorize the remaining 14 of the 19 eligible tickers, any ticker named in
§18's gap categories, any Stage 2 cross-timeframe record, any second batch, or any of the 220 governed
images beyond the five named. Every such expansion requires its own later, separately reviewed and
principal-accepted governance decision, grounded in evidence from how this first batch actually
performed — not assumed in advance from this filing, matching CHART-0001 §11's own precedent exactly.

## Rationale

**Why a new `CHART-0002` filing, not an amendment to `CHART-0001`.** `governance/decisions/README.md`'s
own convention — "never edit a file's substance after `status: Accepted`... supersede it with a new
decision file... or correct with a dated note for narrow factual corrections" — forecloses reopening
CHART-0001's substance for what is not a narrow factual correction but a genuine scope expansion (one
image to five; one asset to five; introducing a Stage 2 architecture CHART-0001 never defined). CHART-0001
§11 itself anticipates and requires exactly this: "Every such expansion requires its own later,
separately reviewed and principal-accepted governance decision." A new, sibling `CHART-####` filing
preserves CHART-0001 as closed history, exactly as the principal's own authorization frames this
filing ("scaling the completed CHART-0001... pilot," not "amending" it).

**Why `WS-0012`, not a `WS-0011` phase.** Fully reasoned in §26 above. In short: `WS-0011`'s own
closure text explicitly disclaims authorizing any scaling, and its `status: complete`/`blocker: None`
shape makes it structurally analogous to an accepted decision file whose substance should not be
reopened — while `WS-0010` (`LADDER-0001`) supplies a direct, working precedent for how this repository
already handles "a new, bounded, genuinely distinct charter needs its own workstream, filed alongside
its own new decision-domain prefix." This differs from `OPS-0012`/`OPS-0013`'s choice to add milestones
to `WS-0007` — that workstream was `status: authorized` (still open, ongoing dashboard work) at the
time, not `complete` — so extending it did not reopen a closed lifecycle the way extending `WS-0011`
would.

**Why the first batch is `AMZN, ASML, AVGO, CEG, COST` at daily-only scope.** Both fully reasoned in
§13-14 above: the selection rule is neutral and reproducible from live data (independently recomputed
this session, not copied from any prior report — though it happens to match the readiness audit's own
previously suggested result, confirming rather than assuming it); the timeframe-scope choice favors
testing the genuinely new "multiple tickers, independently failure-isolated" capability before also
introducing Stage 2 cross-timeframe synthesis in the same implementation PR, keeping review cost and
privacy burden at roughly CHART-0001's own single-image scale multiplied by five, not by twenty.

**Why pixels are retained, not externally referenced.** Fully reasoned in §9: `~/Projects/
Chart-Automation` is not version-controlled, is out of this filing's writable scope, and an
external-reference model would be unverifiable and unreproducible against a mutable, uncontrolled
external directory — defeating CHART-0001's own provenance/claim-boundary standard (§6/§7 above,
reused from CHART-0001 §6).

## Alternatives Considered

- **A. Reopen or amend `CHART-0001`.** Rejected — `governance/decisions/README.md`'s own
  never-edit-after-`Accepted` convention, CHART-0001 §11's own explicit requirement for a "later,
  separately reviewed and principal-accepted governance decision," and the principal's own framing
  ("scaling the completed CHART-0001... pilot") all point away from touching CHART-0001's substance.
- **B. File `CHART-0002` and extend `WS-0011` with a separately gated phase.** Considered seriously —
  it is the pattern `OPS-0012`/`OPS-0013` used for `WS-0007`, and it would avoid creating a second
  workstream entry for what is conceptually the same chart-evidence subject area. Rejected because
  `WS-0011`'s own `status: complete`/`completion_criteria: Met`/`blocker: None`/`next_action` fields
  already assert, in the register's own words, that the pilot is closed and that no scaling is
  authorized by that closure — unlike `WS-0007`, which was still `status: authorized` (open) when
  `OPS-0012`/`OPS-0013` extended it. Reopening `WS-0011` would require either editing that closure
  language (contradicting the spirit of the never-rewrite-accepted-history convention this repository
  applies to decision files, extended here to a completed register entry by the same logic) or leaving
  it in place while contradicting it with new open milestones — neither is clean.
- **C. File `CHART-0002` and create a separate proposed workstream, `WS-0012`.** **Selected.** Directly
  precedented by `WS-0010` (`LADDER-0001`) — a genuinely new, bounded charter gets its own new
  workstream, filed alongside its own decision, left `proposed` until the governance PR merges.
  Preserves `WS-0011` as untouched closed history; keeps `CHART-0002`'s own authority, scope, and
  stopping conditions independently auditable without cross-referencing a closed entry's contradicting
  fields.
- **D. Skip the workstream entirely, since the batch itself is not yet authorized.** Rejected —
  `WS-0010` already established the precedent of recording a `proposed`-status workstream for a
  not-yet-effective charter, keeping this proposal's status discoverable across sessions without
  asserting authority the register itself does not have (`OPS-0001`'s own founding constraint: "the
  register... coordinates work; it does not originate authority").
- **Authorize the full 220-image/55-ticker library in one batch.** Rejected outright — explicitly
  barred by the principal's own authorization ("no more than five deterministically selected
  tickers") and, independently, by the 393 MB size disclosure in the Context section and the
  unreviewed per-image privacy status of all 220 images.
- **First batch at five tickers × four timeframes (20 images, full Stage 2).** Considered and
  rejected for this filing — fully reasoned in §14: conflates two new architectural axes (multi-ticker,
  multi-timeframe) in one implementation PR, quadruples review/privacy burden, worsens failure
  isolation, with no evidence yet that either axis works cleanly alone. Not foreclosed for a future,
  separately authorized batch once this first batch's Stage-1-only results are in.
- **Select the first batch by conviction rating, tier, or portfolio priority instead of an
  alphabetical/structural rule.** Rejected — the principal's own authorization requires a
  "deterministically selected" batch, and this repository's `NUM-0001`/multiple Company Intelligence
  entries already distinguish evidence-based selection from ranking or preference-driven selection;
  using conviction or priority would smuggle a scoring judgment into what is supposed to be a neutral,
  reproducible selection mechanism.
- **Reference-only image storage (path/hash pointing at the external library, no repository-local
  copy).** Rejected — fully reasoned in §9: unverifiable and unreproducible against a mutable,
  non-version-controlled external directory.

## Consequences

**Authorized, effective only on this decision's merge, and only to the extent stated:** the
definitions in §§1-28 above (purpose/status, explicit non-authority, the two-stage advisory-record
architecture, the fact/observation/inference/uncertainty and cross-timeframe conflict-handling rules,
the privacy/provenance/freshness standards reused from CHART-0001, the storage/retention model, the
deterministic first-batch selection rule and its resulting five-ticker daily-only scope, the gap-
category dispositions, the required tests, the review/acceptance/merge/rollback/abstention/stopping
rules, and the explicit prohibited-scope and future-batch exclusions); `WS-0012` as a `proposed`
workstream tracking this authorization. **Even upon merge, no first-batch implementation is authorized
to begin** — that requires its own further, separate, later implementation PR under its own full
independent-review and principal-acceptance cycle (§14, §19-20, §29).

**Not authorized by this filing, now or ever without a further separate decision:** any chart
screenshot, chart analysis, or chart-derived fact committed to the repository beyond the five named in
§14, if and only if a future implementation PR is itself separately accepted; any Stage 2
cross-timeframe synthesis record; any sixth ticker or second timeframe per ticker in this batch; any
processing of the remaining 14 (of 19) eligible tickers or any of the gap-category tickers named in
§18; any `chart_evidence/` directory, schema, or validator beyond the focused tests §16 describes; any
Company/Theme Intelligence record edit or schema extension; any dashboard integration; any scoring,
ranking, or trading-signal generation; any tier/target/holdings/margin/allocator/brokerage change; any
use as `LADDER-0001` or any other research/backtest input; any bulk or recurring ingestion.

**Unchanged by this decision:** the Investment Constitution; every existing accepted governance
decision including `CHART-0001` and `WS-0011`, exactly as filed and merged; `docs/
PORTFOLIO_INTELLIGENCE_SPEC.md` and every existing Company/Theme Intelligence record; `targets.yaml`,
`holdings.yaml`, `gates.yaml`, `issuer_lookthrough.yaml`; `allocate.py`, `margin_state.py`,
`levels.py`; `LADDER-0001`'s research charter and its own chart-pattern/screenshot exclusion; `OPS-
0011`/`OPS-0012`/`OPS-0013`'s dashboard capability and its own boundaries; the 1.8x leverage cap and
30% buffer floor; every `PHQ-####` decision, exactly as filed; `~/Projects/Chart-Automation` itself
(read-only in this filing, not written to).

This decision — including its own acceptance, not only its merge — requires a further, explicit, later
principal step this filing does not take. This decision becomes effective, to the bounded extent stated
above, only when its implementing pull request is independently reviewed, explicitly accepted by the
principal, and merged to `main`.
