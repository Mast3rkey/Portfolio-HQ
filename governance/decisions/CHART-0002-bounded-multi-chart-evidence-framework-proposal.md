---
decision_id: CHART-0002
date: 2026-08-02
status: Accepted
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


---

## Scale-and-throughput amendment (2026-08-02, same governance layer, new PR)

_This is an amendment to the still-`Proposed` filing above, prepared under its own new, narrower
principal authorization, on its own branch and PR. CHART-0002 never reached `status: Accepted` —
PR #222 merged the original proposal text to `main` at `status: Proposed`; a subsequent
acceptance-recording PR (#223) was closed **unmerged** before any independent review, readiness
marking, or principal acceptance occurred (see §Q below). `governance/decisions/README.md`'s
never-edit-after-`Accepted` convention therefore does not bar direct revision of this file's
operative sections — nothing here has ever been `Accepted` — but, following this repository's own
practice of preserving prior reasoning rather than silently rewriting it (the same discipline
CHART-0001's own dated notes applied even though that document's earlier sections had already been
merged), the original Context/Decision/§§1-31/Rationale/Alternatives/Consequences text above is
left completely intact as the historical record of the original five-image proposal and its own
web-upload-influenced capacity assumption. This section supersedes specific operative provisions of
that text, precisely enumerated in §K below — it does not delete, silently contradict, or leave
ambiguous which version of any given provision now controls._

### A. Controlling new principal authorization (verbatim, this session)

"I pause the previously authorized CHART-0002 acceptance-recording PR before it begins. I clarify
that the five-image first-batch limit in the merged Proposed CHART-0002 framework was influenced by
the earlier web-interface upload constraint and should not be treated as my desired operational
ceiling now that Claude Code can directly inspect the governed chart library through Terminal. I
authorize one narrowly bounded Lane G CHART-0002 scale-and-throughput amendment proposal while
CHART-0002 remains Proposed. The amendment must determine the largest safe coherent processing unit
supported by the actual Terminal-based workflow, with the goal of materially reducing the number of
batches required for the 220-chart governed library without compromising privacy, factual accuracy,
fact/observation/inference/uncertainty separation, provenance, source and retained-file hashes,
failure isolation, independent exact-head review, repository health, or rollback. The proposal must
evaluate a two-layer design in which all 220 charts may undergo one deterministic mechanical
preflight and inventory pass, while interpretive Chart Evidence Records are produced in larger but
bounded human/model-reviewed batches. It must evaluate at least 20-chart, 25-chart, and full-55-chart
single-timeframe batch options, and may recommend another ceiling if supported by evidence. It must
also evaluate whether image pixels should remain in the primary Portfolio-HQ repository, use Git
LFS, use a separately governed evidence repository or artifact store, or follow another durable
hash-verifiable storage model. This authorization permits read-only capacity testing, governance
design, and one amendment draft PR only. It does not authorize chart interpretation, chart-derived
conclusions, image retention, Stage 1 or Stage 2 records, processing a live batch, automatic batch
continuation, dashboard or Intelligence coupling, allocation changes, trading signals, or execution.
The amendment PR must remain Proposed and draft, receive independent exact-head review, and require
my explicit acceptance before any acceptance-recording or implementation PR proceeds."

This authorization is narrow in the same way both prior authorizations in this lineage were: it
authorizes *evaluating and drafting* a scale/throughput/storage amendment, not *accepting* it, not
*implementing* it, and not chart interpretation of any kind. Nothing in this amendment constitutes
principal acceptance of its own recommendations — `status: Proposed` above is unchanged by this
filing, and this amendment's own effectiveness requires its own later, separate independent review
and explicit principal acceptance, identical in kind to §29's original gating, restated for this
amendment specifically in §Q below.

### B. Preflight reconciliation (this session, independently verified, not assumed)

Repository confirmed `Mast3rkey/Portfolio-HQ`; branch `claude/chart-0002-scale-throughput-amendment`;
working tree clean at session start; `origin` fetched and pruned; local `HEAD` and `origin/main`
both confirmed identical at `6b503b835cb9db71b958e700113614a1c49bc8c8` (PR #222's merge commit),
zero divergence in either direction. **Zero open pull requests** (`gh pr list --state open` returns
`[]`). A full remote branch enumeration found no branch naming or concerning chart scale, throughput,
storage, acceptance-recording, or implementation for this decision. **PR #222** independently
reconfirmed: `state: MERGED`, `headRefOid: 1594fd6d6f19b54631336b9f5181781da0edd915`,
`mergeCommit: 6b503b835cb9db71b958e700113614a1c49bc8c8`; both retained reviews (`4837275237`,
`state: COMMENTED`, anchored `279c0783e43ca17597d89cb8de70503386927521`; `4837356725`,
`state: COMMENTED`, anchored `1594fd6d6f19b54631336b9f5181781da0edd915`) and the retained principal
acceptance comment (`issuecomment-5155704682`) independently refetched and confirmed present,
unedited. **PR #223** independently reconfirmed: `state: CLOSED`, `merged: false`,
`isDraft: true` at closure, `headRefOid: 11000da46081788c74fa3fee08ed32942721bb29`; its remote
branch confirmed deleted (`git ls-remote --heads origin` returns no match); the controlling
supersession comment (`issuecomment-5158074244`) independently refetched and confirmed present,
stating the PR was "superseded and paused before any independent review, readiness marking,
principal acceptance, or merge." `governance/decisions/CHART-0002-...md` frontmatter and
`governance/decisions.yaml`'s `CHART-0002` entry both independently confirmed `status: Proposed`.
`operations/WORKSTREAMS.yaml`'s `WS-0012` entry independently confirmed `status: proposed`,
`authorized_by: null`. No image, evidence package, Stage 1 record, or Stage 2 record exists anywhere
under `governance/evidence/CHART-0002/` (directory absent). No other acceptance-recording or
implementation PR is open. All eighteen Phase-1 preflight facts the authorizing task specified are
therefore confirmed exactly as stated, with no material difference found — this amendment proceeds.

### C. Methodology: read-only capacity testing performed this session

All testing below was performed against `~/Projects/Chart-Automation` (confirmed, independently
reconfirmed this session, **not a git repository**) in strictly read-only mode — no file under that
path or under `~/Downloads` was created, renamed, moved, deleted, cropped, redacted, converted, or
re-encoded. A single temporary Python script and its JSON output lived in a scratch directory outside
both repositories for the duration of this session and were removed before this filing (§ Phase 4/17
below); no copied image byte, extracted chart fact, or chart interpretation was written to that
scratch directory or to this repository. Where sampled images were viewed to evaluate the privacy-
review *workflow*, no price, date, indicator value, trend, or other chart-derived fact was recorded —
only structural privacy-relevant categories (watermark/username presence; presence/absence of
account, balance, or brokerage data; legibility) were logged, matching this authorization's explicit
prohibition on chart interpretation or chart-derived conclusions.

### D. External governed-library inventory (reconfirmed live, this session)

`~/Projects/Chart-Automation/library/governed/2026-08-01/` independently reconfirmed: **220 PNG
files**, **55 ticker subdirectories**, each holding **exactly 4 files** (`1D`/`1W`/`4H`/`1H`) — a
complete, gap-free 55×4 matrix (`find ... | wc -l` → 220; per-directory histogram → every directory
has exactly 4, zero directories with any other count). `output/governed_copy_manifest_2026-08-01.json`
independently reconfirmed: `run_status: "COMPLETED — 220 files copied, all post-copy checks passed"`,
`entry_count: 220`, `canonical_tickers` count 55, `excluded_duplicates` 6, `excluded_legacy_files` 14,
`excluded_manual_review_items` 10. `output/manual_review_queue.md`'s ten items independently
reconfirmed: none flags a content-level privacy or quality defect against any of the 220 governed
images; one (already-excluded, non-governed) item independently confirms the broader source material
this library was curated from **does** contain a brokerage positions/balances screenshot, correctly
excluded before it ever reached the governed 220 — direct evidence that the curation boundary between
"chart" and "brokerage-sensitive" material is being enforced upstream of this repository, though it
does not substitute for this repository's own required per-image privacy review of anything actually
retained. **Total governed-library bytes, independently recomputed this session**: **411,781,509
bytes (392.71 MB, `du -sh` independently confirms 393M)** across all 220 images — refining, not
contradicting, the original filing's rounded 393 MB figure. **Size distribution** (n=220, bytes):
min 1,312,883; p25 1,754,413; median 1,838,558; mean 1,871,734; p75 1,979,560; p90 2,234,904; max
2,436,875 — a narrow, well-behaved range (max is 1.86x min), no outliers. **By timeframe**: `1D`
total 93,552,664 bytes (mean 1,700,957/image); `1W` total 98,415,477 (mean 1,789,372); `4H` total
120,963,239 (mean 2,199,332, the largest — a wider intraday candle count per capture); `1H` total
98,850,129 (mean 1,797,275). **Image properties**: all 220 confirmed `format: PNG`; exactly three
distinct pixel-dimension pairs observed across the set — `(2750, 2252)`, `(3414, 2252)`, `(3624,
2336)` — consistent with ordinary window/display-size variance across capture sessions, not a defect.

### E. All-220 mechanical preflight: methodology and result

A deterministic, read-only Python script walked every file under `library/governed/2026-08-01/`
and, per file, without opening any image for visual/investment interpretation: resolved ticker and
timeframe from the directory/filename structure against the regex
`^([A-Z0-9\.\-]+)__(\d{4}-\d{2}-\d{2})__(1D|1W|4H|1H)\.png$`; confirmed the file is a regular file,
not a symlink; recorded byte size; confirmed the PNG magic-byte header; decoded the image via Pillow
(`Image.verify()` plus a second full open for dimensions/format, catching any truncation or
corruption); computed SHA-256; cross-referenced that hash and filename against the governed-copy
manifest's own `destination_filename`/`destination_sha256`/`source_sha256` fields; and flagged
duplicate hashes, missing manifest entries, and extra on-disk files not in the manifest.

**Result, this session, live**: **220/220 passed, 0 failed, 0 ambiguous flags, 0 duplicate-hash
groups, 0 files missing from disk vs. the manifest, 0 extra files on disk vs. the manifest, 220/220
manifest entries reconciled 1:1**. Elapsed wall-clock time: **2.18 seconds**; throughput **101.04
files/second**. All 220 filenames matched the naming convention exactly (0 mismatches); all 220
carried a valid PNG magic header; all 220 decoded cleanly via Pillow with no exception; all 220
`source_sha256`/`destination_sha256` pairs in the manifest were internally reconciled (not merely the
one `AAPL`/`1W` sample the original filing spot-checked). A follow-up filesystem-timestamp check
(`find ... -newer <script>`) confirmed **zero files were modified** after the preflight script was
written — the pass was genuinely read-only, not merely intended to be.

**Conclusion: one deterministic all-220 mechanical preflight is technically coherent, cheap (low
single-digit seconds), and safe to run repeatedly (idempotent, no repository-side effect of any
kind — it reads an external, non-version-controlled library and produces no committed artifact).**
This directly answers this amendment's requirement 1 (Objective) and confirms Layer A of the §G
architecture below. **Failure-isolation design a future implementation would require**, precisely
because this pass is so cheap it is expected to be re-run on demand rather than once: per-file
results are independent (one file's decode failure or hash mismatch does not block evaluation of the
other 219); the pass produces a structured summary plus a full per-file result list, so a future
implementation can diff two runs (e.g., before/after a library refresh) to detect exactly which files
changed, appeared, or disappeared; a retry of a single ambiguous file never needs to re-run the whole
220-file pass. No mechanical-preflight result is retained anywhere in this repository by this filing
— it is capacity evidence only, not a committed inventory artifact, matching this amendment's own
prohibition on creating any Stage 1/Stage 2 content or committed chart-derived data.

### F. Privacy-process capacity dry run: methodology and result

**Sample-selection rule (deterministic, neutral, disclosed)**: of the 55 alphabetically-sorted
ticker directories, the **first, middle, and last** (`AAPL`, `JNJ`, `XOM` — indices 0, 27, 54 of 55)
were selected, each contributing all 4 governed timeframes, for **12 sampled images total**. This
rule is purely positional — it references no conviction rating, tier weight, portfolio priority, or
chart appearance — and by construction spans the alphabet (early/mid/late), all four timeframes
evenly (3 images per timeframe), and a representative slice of the file-size distribution (sampled
bytes ranged 1,339,201–2,144,342, covering roughly the 5th–85th percentile of the full 220-image
range without deliberately targeting either extreme). None of the three sampled tickers appears in
the manual-review queue's content-flagged items (only `MU`'s already-superseded original capture and
`CEG`'s administrative folder-naming note appear there, and CEG was not in this sample) — this sample
therefore specifically tests the **ordinary, unflagged-file** case the authorization requires. **12
was deliberately chosen smaller than the 20-image default**: each governed image is a real,
uncompressed 1.3–2.4 MB high-resolution capture, and this is a capacity *estimate* to inform a batch-
size decision, not a completeness census — the future actual implementation batch will still review
every one of its own images individually regardless of what this dry run measures, per §G/§I below.

**Result**: all 12 images retrieved and rendered successfully (0 decode failures, 0 unreadable
files). Structural privacy-relevant observation, aggregated and disclosed at the category level
only, per this authorization's explicit prohibition on recording chart-derived facts: **12 of 12
sampled images show a small, consistently-positioned platform watermark/username string in the
image's top-left corner** (the same category of element CHART-0001 §5 already named and bounded with
its one narrow, principal-approved exception) **and 0 of 12 show any account balance, position list,
order history, buying-power/margin figure, or other brokerage-account identifier** — each of the 12
is, structurally, an ordinary price-chart capture with no brokerage-sensitive content requiring
escalation. **0 of 12 required escalation; 0 of 12 were ambiguous or illegible; 0 of 12 became
privacy-approved by this dry run** — this section is capacity-workflow evidence only; per CHART-0001
§5 and CHART-0002 §6, unchanged, every image actually proposed for retention in a future batch still
requires its own independent, per-image privacy review recorded in that image's own package
manifest, with no batch-wide shortcut. The 12-image retrieval-and-render pass completed within
roughly 22 seconds of aggregate tool round-trip time for the full parallel batch; because rendering
was parallelized, this figure is not a reliable per-image serial-review time and is reported only as
an aggregate retrieval-cost data point, not a throughput estimate for the analytical (fact/
observation/inference/uncertainty-separating) review step itself, which is a human/model judgment
task this dry run does not attempt to time in isolation.

**Whether privacy review can be safely sharded**: yes, structurally — each image's privacy
determination is fully independent of every other image's (no cross-image state), so per-image
review work can be distributed across parallel authoring/review shards (§I) without coordination
overhead beyond the final completeness check. **What remains necessarily human/model-reviewed**: the
actual privacy determination itself (is a watermark present; is anything account-identifying visible;
is the image otherwise safe to retain) is exactly the kind of visual judgment this authorization
reserves for human/model review, never mechanical automation — §E's mechanical preflight (hash,
decode, filename, dimensions) is a categorically different, safely automatable layer, and this
session's results do not blur that boundary. **Why bulk mechanical validation cannot substitute for
per-image privacy review**: §E's 220/220 mechanical pass proves every file is a structurally valid,
uncorrupted, correctly-named, hash-reconciled PNG — it says nothing about what is visually depicted in
any of them. A corrupted-file check and a "does this image contain a visible account balance" check
are unrelated questions; passing one implies nothing about the other, which is exactly why this
amendment defines two structurally separate layers (§G) rather than one.

### G. Two-layer architecture (Layer A / Layer B / Layer C), as authorized and evaluated

**Layer A — mechanical preflight.** Deterministic, read-only, safely automatable per §F's own
boundary discussion and CHART-0002 §12's existing "safe factual automation" boundary, unmodified.
**Recommended: authorized to run against all 220 governed images**, per §E's clean result. Produces
no committed artifact, no privacy approval, no interpretation, no Stage 1/Stage 2 content, and no
automatic retention of anything — it is inventory/integrity evidence only, re-runnable on demand, and
this amendment's own governance package (§L) does not itself commit any preflight output.

**Layer B — interpretive Stage 1 batch(es).** Human/model-reviewed, privacy-reviewed per image,
individually authored and reviewed. **Recommended maximum for a single implementation PR: 25 images,
single timeframe** — reasoned in full in §H. This is a general architectural ceiling for *future*
batches; the specific first batch recommended by this amendment (§H) uses exactly 19 images, the
entire currently-eligible universe under CHART-0002 §13's own unmodified selection rule, which fits
comfortably under the 25-image ceiling with headroom rather than requiring the ceiling to be reached.

**Layer C — future Stage 2 (cross-timeframe synthesis).** Unchanged from the original filing:
**remains entirely unauthorized by this amendment.** Nothing in this amendment evaluates,
recommends, or moves toward Stage 2 — it only re-scopes Layer A/B throughput and storage. A future
batch that includes more than one timeframe per ticker, or any Stage 2 record, requires its own
further, separate, later governance decision, exactly as CHART-0002 §3/§14/§25/§28/§31 already
require, unamended.

### H. Batch-size comparison and recommendation

**Comparison matrix** (Layer B, single-timeframe, Stage 1 only; "universe" rows use the 19-name
currently-eligible set per CHART-0002 §13, unmodified; "future full-library" rows are a hypothetical
upper bound if Company Intelligence coverage eventually reached all 55 governed-library tickers,
provided for context only — not authorized or assumed by this amendment):

| | 5 (original) | 20 | 25 (recommended) | 55 |
|---|---|---|---|---|
| Implementation PRs to cover current 19-name universe | 4 | 1 | 1 | 1 (oversized) |
| Implementation PRs to cover a hypothetical future 55-name universe | 11 | 3 | 3 | 1 |
| Retained binary files (current-universe batch) | 5×4=20 across 4 PRs | 19 in 1 PR | 19 in 1 PR | 19 in 1 PR (36 slots unused) |
| Stage 1 records | 1 per image | 1 per image | 1 per image | 1 per image |
| Package dirs / manifests / READMEs | 5/5/5 ×4 batches | 19/19/19 | 19/19/19 | 19/19/19 |
| Est. retained bytes (unredacted, current universe) | ~8.5 MB ×4 batches | ~32.2 MB | ~32.2 MB (≤40.5 MB at full 25-ceiling) | ~32.2 MB |
| Diff file count per PR | 20 | 76 | 76 | 76 |
| Privacy-review units per PR | 5 | 19 | 19 | 19 |
| Independent-review diffs to inspect | 4 bounded diffs | 1 diff, ~76 files | 1 diff, ~76 files, headroom to 100 | 1 diff, ~76 files |
| Correction blast radius on 1 bad image | 1/5 of one PR | 1/19 of one PR | 1/19–25 of one PR | 1/19 of one PR |
| Rollback granularity | per-package (unchanged across all options) | per-package | per-package | per-package |
| Governance lifecycles (Lane G filings) to reach current universe | 4 | 1 | 1 | 1 |
| Silent-omission/duplication risk | low (small batches) | needs shard discipline (§I) | needs shard discipline (§I) | needs shard discipline (§I), largest surface |
| CI/package-shape test burden | smallest, ×4 | moderate, once | moderate, once | moderate, once, most headroom unused |

**Why not 5 (status quo)**: quadruples the number of governance-and-implementation lifecycles needed
to cover even the small, already-known 19-name eligible universe (4 batches instead of 1) — directly
contrary to this amendment's own stated goal of materially reducing batch count, and the goal exists
specifically because the constraint that justified 5 (a web-upload interface limit) no longer applies
to this Terminal-based workflow, per §A.

**Why not 20**: technically sufficient for the current 19-name universe (barely — one spare slot),
but offers no headroom for near-term eligible-universe growth (e.g., the next WS-0005 Milestone-3
batch adding one or two more names whose tickers already have chart-library coverage), which would
immediately force a second batch at the same size this amendment was written to avoid. 25 costs
nothing extra in review/storage terms that 20 does not already cost (§H matrix — both fit the current
batch in one PR, one diff, one governance lifecycle) while providing that headroom.

**Why 25 (recommended)**: the smallest ceiling above 20 that (a) fits the entire current 19-name
eligible universe in one PR with real headroom, not by a single slot; (b) keeps a single
implementation PR's diff to roughly 100 files and ~40 MB at the ceiling — proportionate to, not
qualitatively different from, CHART-0001's own one-image precedent scaled up, and still small enough
for one eligible independent reviewer to complete an `OPS-0007` §1 exact-head review of the whole PR
in a single pass, or via the bounded shard model in §I; (c) keeps per-batch repository growth (§J) in
the tens-of-MB range rather than the ~89 MB a 55-image ceiling would add even before any second batch;
and (d) leaves meaningful margin before the batch size starts to resemble the "conflate two new
architectural axes at once" failure mode the original filing's own §14 already reasoned about for the
tickers-vs-timeframes case, applied here to tickers-per-PR instead.

**Why not 55**: the current eligible universe is 19, not 55 — a 55-image ceiling would retain 36
package slots' worth of unused headroom for a universe that does not exist under any currently
accepted selection rule (CHART-0002 §13, unmodified by this amendment — see §Phase 9/§K below), and
would, if the universe did eventually grow to 55, add ~89 MB in one PR (§J) — nearly 5x the recommended
25-ceiling's footprint, in one governance/implementation lifecycle, with a correspondingly larger
single-PR diff (220 files) for one independent reviewer's exact-head pass, worse failure isolation (a
systemic defect surfaces after more work is exposed to it), and no evidence yet — from either this
session's 12-image privacy dry run or CHART-0001's own single-image precedent — that the review
process has actually been exercised at anywhere near that scale. 55 is not rejected as unsafe in
principle; it is rejected as **unsupported by current evidence and unmatched to the current eligible
universe**, and nothing here forecloses raising the ceiling again later if a future batch's own
results justify it (§P).

**Recommended maximum: 25 images, single timeframe, per Layer-B implementation PR** — this is a
general architectural ceiling for future batches, not itself a batch authorization. See §Q for what
remains unauthorized.

### I. Review-shard and failure-isolation architecture

For a Layer-B batch up to the 25-image ceiling, a future implementation PR — not opened, drafted, or
begun by this amendment — is authorized, if this amendment is later separately accepted, to structure
its own required review as follows:

- **One immutable cohort manifest**, fixed before any authoring begins, listing every ticker in the
  batch by name, frozen and never silently altered mid-implementation.
- **Deterministic shard assignment**: the cohort is split into shards of exactly 5 tickers each
  (matching the original filing's own proven per-batch unit — CHART-0002 §14's five-image batch —
  reused here as an internal authoring/review chunk rather than a separate governance lifecycle), e.g.
  a 19-ticker cohort yields 4 shards of 5/5/5/4.
- **No duplicate ticker across shards; no missing ticker** — mechanically verified: the union of every
  shard's ticker list must equal the cohort manifest exactly, with zero overlap and zero omission,
  matching `test_chart_evidence_pilot.py`'s existing package-shape-test pattern extended to
  cohort-level completeness.
- **One package per image**, unchanged from CHART-0001/CHART-0002.
- **Per-shard authoring-session and privacy-review provenance**, recorded per image (already required
  by CHART-0001 §5/§6, unchanged), with a shard-level rollup for reviewer legibility only — the
  per-image record remains authoritative.
- **Per-shard content review**: an eligible independent reviewer (`OPS-0007` §1) may review one
  shard's bounded diff explicitly, rather than only ever facing one undifferentiated 25-image diff —
  this is an optional convenience for the reviewer, not a substitute for the final gate below.
- **One final, exact-head integration review** covering the complete PR — every shard, every package,
  completeness (cohort manifest count == retained package count, no extra, no missing), and any
  unresolved shard-level findings — is mandatory before merge, satisfying `OPS-0007` §1.2's "review
  the exact commit head that will be relied upon" requirement; a shard-level review is never by itself
  sufficient to satisfy the merge gate.
- **Correction ownership**: a MATERIAL finding in one shard triggers a bounded correction to that
  shard's affected package(s) only (matching CHART-0002 §23's existing rollback convention), followed
  by re-review of the corrected shard **and** a fresh final integration review at the PR's new exact
  head — never a merge based on a stale final-review head.
- **No partial silent acceptance**: unchanged from CHART-0002 §21 — a batch that cannot complete at
  least a majority of its cohort must stop and return for principal amendment rather than merge a
  materially shrunken batch silently; a batch that completes all but a small, individually-disclosed
  minority (one or two images failing §6 privacy review, say) may proceed with those specific tickers
  abstained per §22, disclosed by name and reason, never silently dropped.
- **Proof of full, not sampled, review**: satisfied structurally, not by assertion — the mechanical
  completeness test above (cohort-manifest count == retained-package count, exact ticker-set match)
  proves every cohort member has exactly one package, and every package's own manifest carries its own
  privacy-review and content-review attestation fields (already required by CHART-0001 §6/§7,
  unchanged) — a reviewer or later auditor can mechanically confirm full coverage without relying on a
  reviewer's unverified claim to have "covered everything."
- **Final principal acceptance** names the exact whole-PR head, unchanged discipline from CHART-0001
  §14/CHART-0002 §20, applied to the larger batch — never inferred from a shard-level approval alone.

This design directly satisfies this amendment's own requirement that "every image and record can
still receive attributable review" at the recommended 25-image ceiling, without requiring a return to
5-image batches to preserve that property.

### Phase 9 resolution — universe scope (addressed explicitly, not assumed)

This amendment is authorized to evaluate throughput, batch size, and storage — **it is not authorized
to, and does not, change CHART-0002 §13's selection-rule substance** (which names, expands, or
restricts *which* tickers are eligible is a different kind of governance question than *how many at
once* and *where the pixels live*). Re-run live this session (§ preflight above): the eligible set
under §13's unmodified rule — canonical `targets.yaml` destination entry **and** existing Company
Intelligence record **and** governed chart-library coverage **and** not actionable-gated — is
independently reconfirmed **identical to the original filing's own result, 19 names, zero drift**:
`AMZN, ASML, AVGO, CEG, COST, ETN, GEV, GOOGL, ISRG, KLAC, LLY, META, MSFT, NVDA, PANW, PWR, TMO, TSM,
V`. The governed 55-ticker library therefore contains 36 tickers with no current interpretive
eligibility under the unmodified rule — most lack a canonical destination entry or a Company
Intelligence record (§18 of the original filing already enumerates the gap categories in full,
unedited by this amendment). **This amendment does not authorize interpretive coverage of any of
those 36**, and does not recommend broadening §13's criteria — that would be a substantive eligibility
change, outside this amendment's own scope (§A), requiring its own separate future governance
decision if ever proposed. Layer A's all-220 mechanical preflight is unaffected by this scoping — it
is inventory/integrity evidence only, carries no eligibility judgment, and may run against the full
governed library regardless of which tickers are interpretively eligible.

### J. Storage architecture evaluation

**Current repository size, measured live this session**: local `.git` common directory **19 MB**
(`git count-objects -vH`: 2.18 MiB loose + 15.12 MiB packed across 3,351 objects); GitHub's own
server-reported size **16,321 KB (≈15.9 MB)**. **Git LFS is not installed in this local execution
environment** (`git-lfs not found`; `git lfs` is not a recognized git subcommand) — a directly
observed platform fact, not an assumption. No `.gitattributes` file exists in this repository — no
LFS tracking is configured anywhere, confirming this repository has never used LFS for anything,
including CHART-0001's own retained image.

**Projected repository growth, using live-measured, unredacted governed-library byte counts** (actual
retained sizes may be smaller after any privacy redaction/recompression a future implementation
applies, per CHART-0001 §5's disclosure-of-transformation requirement — these are conservative,
upper-bound estimates):

| Scope | Images | Projected bytes (unredacted) | Approx. repo growth vs. current ~19 MB |
|---|---|---|---|
| Current 19-name eligible universe, `1D` only | 19 | 33,729,566 (32.17 MB) | ~2.7x |
| Recommended 25-image ceiling, `1D` only | 25 | ~40.55 MB | ~3.1x |
| Hypothetical full 55-ticker library, `1D` only | 55 | ~89.22 MB | ~5.7x |
| Full 220-image library, all 4 timeframes | 220 | 411,781,509 (392.71 MB) | ~21.7x |

The last row is why this amendment does **not** recommend pixel-retention of the full 220-image
library under any storage model, ever, as a single unit — it is presented only to make the Layer-A
(mechanical-only, no retention) versus Layer-B (interpretive, bounded retention) distinction concrete
in size terms, reinforcing why the two layers must stay architecturally separate.

**Options evaluated**:

- **A. Raw image pixels committed directly to Portfolio-HQ Git history.** This is this repository's
  existing, already-used model — CHART-0001's own retained NVDA image is committed exactly this way,
  no LFS, no external reference. Confirmed compatible with `gh`/`git` tooling actually available in
  this environment; confirmed zero new tooling, zero new configuration, and zero new authorization
  (beyond what CHART-0001 §4/§9 already established) required to continue it. Cost: the projected
  growth above lands in the repository's own history permanently (PNG is already compressed, so git's
  own delta/zlib compression on top yields little further reduction — most of the projected bytes
  really do land in the repo). At the recommended 25-image ceiling (~40 MB), this triples the current
  repository size in one PR; that is a real, disclosed cost, not a hidden one. **Recommended: primary
  storage model**, unchanged from CHART-0001 §4/§9's own reasoning, now explicitly re-verified against
  live size data rather than assumed.
- **B. Git LFS within Portfolio-HQ.** Would reduce main-repository clone size by moving large binaries
  to LFS storage, but: **the LFS client is not installed in this environment** (directly confirmed,
  not inferred) — enabling it would require installing tooling and writing a new `.gitattributes` file,
  neither of which this session is authorized to do (explicitly prohibited: "Do not... enable Git
  LFS"); **GitHub LFS storage/bandwidth quota and billing behavior for this specific repository were
  not confirmed this session** (no live authenticated LFS-quota API call was made, and none is
  authorized) — a genuine, disclosed platform uncertainty, not a claimed fact; LFS also weakens
  in-diff exact-head reviewability (a reviewer viewing a GitHub PR diff sees an LFS pointer file, not
  the image inline, unless they separately pull LFS objects) which cuts against `OPS-0007` §1.3's
  "sufficient repository access to inspect the complete diff" requirement without extra reviewer
  tooling. **Not recommended as primary; not ruled out permanently** — flagged as the first
  reconsideration candidate if cumulative chart-evidence footprint grows large enough that Option A's
  repository-size cost becomes a genuine constraint (see stopping condition, §M).
- **C. A separate governed evidence repository.** Would keep Portfolio-HQ's own history smaller, but
  introduces cross-repository atomicity and governance complexity this repository's own doctrine
  already leans against — the filesystem-as-index principle (`PI-0001`, reaffirmed for Theme
  Intelligence by `PI-0006`, reused by CHART-0001 §4/§8) treats *this* repository as the authoritative,
  auditable evidence index; splitting evidence into a second repository would mean a governance
  decision's cited evidence lives outside the repository that governs it, undermining exact-head
  reviewability (`OPS-0007` §1.2/§1.3) unless that second repository is itself brought under the same
  review discipline — effectively duplicating this repository's own governance machinery. No such
  repository exists, none is authorized by this filing (explicitly prohibited: "Do not... create
  another repository"), and creating one is a materially larger structural decision than this
  amendment's own scope. **Not recommended**, primary or fallback, absent a much stronger future case.
- **D. GitHub release assets or another durable artifact store, with manifests/hashes retained in
  Portfolio-HQ.** Reduces repository history growth similarly to LFS, and this repository already has
  `gh` CLI access confirmed working in this session (used throughout for PR/review verification) —
  but release-asset lifecycle and retention are not naturally tied to a specific commit or PR the way
  a repo-tracked file is (an asset can be edited or removed independently of any commit), weakening the
  hash-verifiable, exact-head-anchored evidentiary guarantee this repository's entire evidence-package
  convention (`PHQ-2026-01` through `PHQ-2026-06`, CHART-0001) is built on, unless a future
  implementation separately re-verifies asset hashes against the manifest at every access — added
  complexity with no demonstrated benefit at the current, modest (tens-of-MB) batch scale. No release
  or artifact-store action of any kind is taken or authorized by this filing (explicitly prohibited:
  "Do not... upload release assets"). **Recommended: documented fallback only**, to be reconsidered,
  with its own future platform-capability confirmation (`gh release` permissions, retention behavior,
  quota), if repository-size growth crosses the stopping-condition threshold in §M and Option B (LFS)
  is also found insufficient or unavailable at that time.
- **E. Another durable, hash-verifiable model.** No alternative meeting this bar was identified this
  session beyond A-D above; none is recommended.

**Recommendation: primary storage model = Option A** (continue the existing CHART-0001 repository-
native, LFS-free, hash-manifested evidence-package pattern, unchanged), **fallback = Option D**
(GitHub release assets with in-repo manifests/hashes), reconsidered only if the stopping condition in
§M is reached. Option B (LFS) is the next candidate after D if this repository ever adopts LFS for
other reasons independent of this decision; it is not preferred over D today given the disclosed
tooling and reviewability gaps above.

### K. Supersession table — exactly what this amendment changes in the original filing

Nothing above (Context through Consequences, §§1-31) is deleted or silently contradicted; the
following operative provisions are **prospectively superseded for future operative purposes** by this
amendment, effective only on this amendment's own separate future acceptance and merge (§Q) — the
original text remains as historical record of what the original proposal said and why:

| Original provision | Original operative content | Superseded by |
|---|---|---|
| §8 (storage size bound) | "at most five images, an estimated ~5-9 MB" | §J above: primary model unchanged (Option A), but the bound is now the 25-image ceiling (§H), ~40.5 MB projected |
| §13 (selection rule) | Unchanged in substance | Reaffirmed unmodified — this amendment does not alter eligibility criteria (Phase-9 resolution above) |
| §14 (first batch: exact tickers/scope) | Five tickers (`AMZN, ASML, AVGO, CEG, COST`), five images | §H/§Q: the first batch, if separately authorized later, is the full current 19-name eligible set, `1D` only, Stage 1 only — still zero Stage 2, still one timeframe |
| §16 (tests) | Package-shape tests for a five-package batch | §I: extended to cohort-level completeness tests (union-of-shards == cohort manifest) for up to a 19-25-package batch |
| §21 (failure isolation) | "does not by itself invalidate the other four" (of five) | §I: same principle, restated for a 19-25-ticker cohort with shard-level correction scoping |
| §26/`WS-0012` register text | References a five-image batch and `governance-pr-drafted` milestone only | §L below: `WS-0012` gains one additional milestone recording this amendment; batch-size language updated to match §H |
| §27 (governance package scope, this filing) | Five files including `governance/decisions.yaml` and a test-count bump | §L below: this amendment's own scope is three files — `decisions.yaml` and the test file are unaffected (reasoned in §L) |

Unchanged, in full, by this amendment: §1 (purpose/status), §2 (explicit non-authority — restated,
not loosened, in §N below), §3-§7 (two-stage architecture, fact/observation/inference/uncertainty
separation, cross-timeframe conflict handling, privacy, provenance), §9 (pixels-retained-not-
referenced rationale — reaffirmed by §J's Option A recommendation), §10-§12 (Intelligence
non-coupling, freshness/supersession, human-review/automation boundary — §12's boundary is exactly
what §E/§F's own layer separation relies on), §15/§17/§19/§20/§22-§25/§28-§31 (acceptance criteria
extended only in scale per §H/§I, review weight, separate-implementation-PR requirement, principal-
acceptance/merge/post-merge-verification discipline, abstention, rollback, completion criteria,
stopping conditions extended per §M, prohibited scope restated per §N, effectiveness gates restated
per §Q, no-chart-analyzed disclosure — this amendment performed none either, per §C, and the
first-batch-only authorization scope of §31 is restated, resized, in §Q).

### L. This amendment's own governance package scope

This amendment touches exactly three repository files, narrower than the original filing's five-file
§27 scope:

1. `governance/decisions/CHART-0002-bounded-multi-chart-evidence-framework-proposal.md` (this file —
   this appended section).
2. `operations/WORKSTREAMS.yaml` (`WS-0012` entry only: one additional milestone recording this
   amendment's filing; `authorized_scope`/`next_action`/batch-size language updated to match §H/§Q;
   `status` remains `proposed`, `priority` remains `secondary`, `authorized_by` remains `null`).
3. `CLAUDE.md` (the single existing `CHART-0002` Decisions Log pointer, updated in place — no
   duplicate competing pointer added).

**`governance/decisions.yaml` is deliberately not touched**: it already carries the correct
`CHART-0002` entry at `status: Proposed` (independently reconfirmed, §B above) — this amendment does
not add a new decision, it amends the existing `Proposed` one, so no new index row and no status
change are needed. **No test file is touched**: the original filing's §27 item 5 bumped a hardcoded
decision-*count* assertion from 59→60 because it *added* the 60th decision entry; this amendment adds
no new entry to `governance/decisions.yaml` (the count stays 60, independently reconfirmed unchanged,
§Q below), so no count assertion needs to move. No chart image, Chart Evidence Record, Stage 1/Stage 2
content, or any file under `~/Projects/Chart-Automation` or `~/Downloads` is touched, matching the
original filing's own boundary, unweakened.

### M. Revised acceptance, completion, and stopping conditions

**Batch acceptance criteria (§15's original list, extended to a 19-25-image cohort)**: every original
bullet applies unchanged, with "the five" read as "every ticker in the frozen cohort manifest" and
"the five named tickers, one `1D` image each, and zero Stage 2 records" read as "every cohort-manifest
ticker named in the authorizing decision, one `1D` image each, and zero Stage 2 records" — any
deviation still requires stopping and returning for principal amendment, not silent substitution,
unchanged from §21-22.

**Stopping conditions (§25's original list, restated, plus one new condition specific to scale)**:
every original bullet applies unchanged (unidentifiable source image; metadata that can't be
established without invention; unredactable sensitive content; inability to separate fact from
interpretation; any attempt to introduce scoring/prediction/allocator coupling; any attempt to add a
sixth-plus ticker beyond the cohort manifest, a second timeframe, or Stage 2; any weakening of an
existing safeguard; inability to implement as a small, reversible unit; utility not justifying
resulting size/review/maintenance cost) — **plus, new**: **a future batch must stop and reconsider its
storage model (§J) before proceeding if implementing it would push this repository's own measured
`.git` size, or GitHub's own reported repository size, past roughly 250 MB** (a level chosen as
meaningfully below the ~393 MB the full 220-image library would add if ever retained in full — itself
already rejected, §J — while leaving headroom above the ~40 MB the recommended 25-image ceiling adds
per batch for several such batches before the threshold is reached); crossing that threshold requires
re-evaluating Option A vs. the Option D fallback (or a future Option B if LFS becomes available and
authorized) **before**, not after, the next batch's pixels are committed.

**Completion criteria for this amendment itself** (distinct from any future batch's own completion,
per §24's original distinction, unchanged in kind): met when independently reviewed under `OPS-0007`
§1, any required bounded correction made and re-reviewed, explicitly principal-accepted at the exact
final head, and merged to `main`. **This alone does not authorize any first batch** — see §Q.

### N. Explicit non-authority, restated for this amendment specifically

This amendment authorizes **none** of the following, now or as an implied consequence of anything
above, without its own separate, later, explicitly accepted governance decision — every item in the
original filing's §2/§28 remains in force, unweakened, and this amendment adds:

- any chart interpretation, chart-derived conclusion, trend/support/resistance/pattern/momentum/
  indicator/price/date/market observation of any kind, from any of the 220 governed images, sampled or
  not — §F's dry run recorded structural privacy categories only, never chart content;
- creation of any Stage 1 or Stage 2 record;
- copying, cropping, transforming, redacting, retaining, committing, uploading, or versioning any
  image — this amendment retained none;
- marking any image privacy-approved — §F explicitly disclaims this for all 12 sampled images;
- processing an implementation batch of any size;
- beginning an implementation branch or PR;
- enabling Git LFS, creating another repository, uploading release assets, or creating/altering any
  GitHub Actions artifact — §J evaluates these as options, none is activated;
- any modification to `~/Projects/Chart-Automation` or access to `~/Downloads`;
- changing `CHART-0002`'s `status` from `Proposed` to `Accepted`, or changing its decision-index
  status in `governance/decisions.yaml`;
- automatic batch continuation of any kind — every future batch, at any size up to the 25-image
  ceiling, requires its own separate implementation PR, review, and principal acceptance (§Q);
- any Intelligence, tier, target, holdings, gate, allocation, margin, allocator, dashboard, brokerage,
  signal, or trading-behavior change.

### O. Alternatives considered (amendment-specific)

- **Leave the five-image ceiling in place and simply run four sequential batches.** Rejected — this
  is exactly the outcome the principal's own authorization (§A) directs away from ("materially
  reducing the number of batches"), and §H's comparison shows no evidence-based reason the ceiling
  needs to stay that low once the web-upload constraint that originally motivated it no longer applies
  to a Terminal-based workflow.
- **Recommend 20 images as the ceiling**, matching the authorization's own "reasonable default."
  Considered and set aside in favor of 25 — §H reasons that 25 costs nothing extra in review/storage
  terms over 20 for the current 19-name universe (both fit in one PR) while providing real headroom
  for near-term eligible-universe growth that 20 would not.
- **Recommend the full 55-ticker library as the general ceiling**, since the authorization explicitly
  required evaluating it. Considered in full (§H, §J) and rejected — unsupported by current evidence
  (only 12 of 220 images have ever been inspected by any privacy-review-workflow test, and no image
  has received CHART-0001/CHART-0002 §6's full per-image review) and unmatched to the current 19-name
  eligible universe under the unmodified §13 selection rule; not foreclosed permanently (§P).
- **Broaden CHART-0002 §13's selection rule to include all 55 library tickers**, so a 55-image ceiling
  would have a matching universe. Rejected — explicitly out of this amendment's own authorized scope
  (§A: throughput/storage, not eligibility criteria), addressed directly in the Phase-9 resolution
  above; a future eligibility-broadening proposal, if ever made, is its own separate governance
  decision.
- **Adopt Git LFS or a separate evidence repository as primary storage now**, to pre-empt future
  repository-size growth. Rejected for now (§J) — both are explicitly prohibited to this session,
  neither has a demonstrated need at the recommended 25-image batch's ~40 MB footprint, and both carry
  real reviewability/tooling costs not yet justified by current scale; documented as reconsideration
  candidates instead (§J, §M's stopping condition).
- **Set no general ceiling at all, and let each future batch's own governance filing pick a size ad
  hoc.** Rejected — inconsistent with this repository's own preference for reusable, evidence-derived
  general standards over one-off numbers (matching `NUM-0001`'s provenance-classification discipline
  and this repository's own repeated "backtest once, cite the result, don't re-litigate" pattern); a
  standing 25-image ceiling gives every future batch proposal a pre-reasoned default it can cite or
  explicitly deviate from with its own justification.

### P. Consequences

**Authorized, effective only on this amendment's own separate future merge, and only to the extent
stated**: the two-layer Layer A/Layer B/Layer C architecture (§G); Layer A's all-220 mechanical-
preflight authorization (re-runnable, no retained artifact); the 25-image single-timeframe general
ceiling for future Layer-B batches (§H); the review-shard and failure-isolation architecture for a
19-25-image batch (§I); the Phase-9 universe-scope resolution (unmodified §13 eligibility, 19 names
currently); the storage recommendation (§J: primary Option A, fallback Option D, with the §M
repository-size stopping condition); the supersession table (§K); this amendment's own three-file
governance package scope (§L); the extended acceptance/stopping conditions (§M); and the restated,
unweakened non-authority list (§N). **`WS-0012` remains `proposed`, `priority: secondary`, with no
implementation authority** — this amendment being accepted, by itself, still authorizes no batch;
see §Q.

**Not authorized by this amendment, now or ever without a further separate decision**: any first or
later batch actually processing any image (§Q names the exact gate); any Stage 2 record, ever, under
any batch size; any broadening of §13's selection-rule eligibility criteria; any change to the
25-image ceiling itself (raising or lowering it) without its own future evidence-based proposal; any
Git LFS activation, second repository, or release-asset upload; any Company/Theme Intelligence,
dashboard, allocator, margin, tier, target, holdings, or brokerage change of any kind.

**Unchanged by this amendment**: everything the original filing's own Consequences section already
listed as unchanged (the Investment Constitution, every other accepted governance decision, `docs/
PORTFOLIO_INTELLIGENCE_SPEC.md` and every Company/Theme Intelligence record, `targets.yaml`/
`holdings.yaml`/`gates.yaml`/`issuer_lookthrough.yaml`, `allocate.py`/`margin_state.py`/`levels.py`,
`LADDER-0001`, `OPS-0011`/`OPS-0012`/`OPS-0013`, the 1.8x leverage cap and 30% buffer floor, every
`PHQ-####` decision, `~/Projects/Chart-Automation` itself) — plus, newly confirmed unchanged by this
amendment specifically: `CHART-0001`'s own file and its `WS-0011` register entry (neither read nor
touched this session beyond the read-only reconciliation in §B); `governance/decisions.yaml`'s
`CHART-0002` entry and overall 60-decision count (§L); every test file in this repository.

### Q. Effectiveness, review, and merge gates for this amendment

Identical in kind to the original filing's own §29, restated for this amendment specifically. This
governance PR must remain in **draft** state. Before it may even be considered for independent review
as a candidate for merge, it requires, in this order: (a) independent, exact-head review by an
eligible reviewer per `OPS-0007` §1; (b) any required bounded correction and exact-head re-review; and
(c) **explicit principal acceptance of this amendment's own content** — a distinct, later step from
the principal's authorization to *prepare* it (§A), which this filing does not claim to have
received. **This amendment does not mark itself ready, does not authorize its own merge, and does not
authorize beginning any batch of any size.** Nothing in §§A-P above becomes effective until this PR
merges to `main`, and even then: (1) Layer A's mechanical-preflight description becomes usable
capacity-testing methodology, but running it again produces no committed artifact and requires no
further authorization, since it was already run, live, this session, with no repository-side effect;
(2) Layer B's 25-image ceiling and the 19-name first-batch scope become the **governing architecture
for a future batch proposal** — they do not themselves retain any image, create any record, or begin
any implementation; **a first Layer-B batch still requires its own further, separate, later
implementation PR, under its own full `OPS-0007` §1 review cycle and explicit principal acceptance at
its own exact final head, before it may merge** — identical in kind to every gate the original filing
already imposed on its own five-image batch, simply resized. This amendment authorizes no chart
interpretation, no image retention, no Stage 1 or Stage 2 record, no live batch processing, no
automatic batch continuation, and no dashboard/Intelligence/allocation coupling, now or as a
consequence of its own future acceptance alone.

---

## Acceptance recording (2026-08-02, same governance layer, new PR)

**Principal authorization (verbatim, this session):** "I authorize one narrowly bounded CHART-0002
acceptance-recording PR based on the amendment now merged through PR #224 at merge commit
`3d8ad7896236148e57e9bef3dd8fc003ef55b07a` and my retained principal-acceptance comment `5158527253`.
The PR may record CHART-0002 as Accepted and synchronize only the controlling decision file,
`governance/decisions.yaml`, `WS-0012`, `CLAUDE.md`, and directly necessary tests or validators. It
must contain no chart image, chart interpretation, Chart Evidence Record, Stage 1 or Stage 2
implementation, live mechanical preflight, target or tier change, dashboard or Intelligence coupling,
margin or allocator change, trading signal, brokerage access, or execution. The PR must remain draft,
receive independent exact-head review, require my explicit exact-head approval before merge, and
undergo complete post-merge verification. This authorization does not yet authorize the 19-chart
implementation batch."

**Provenance chain, independently reconfirmed this session, not assumed.** `PR #224` ("CHART-0002:
amend chart scale and throughput design") independently reconfirmed `state: MERGED`,
`mergeCommit.oid: 3d8ad7896236148e57e9bef3dd8fc003ef55b07a`, `headRefOid`
(the amendment's own exact accepted head) `ab9fb6b49b55f8cf575c2e8d4267e8e15bce52d3`. Independent
exact-head review `4838752317`, anchored to that head, independently refetched this session and
confirmed verdict **APPROVED FOR PRINCIPAL ACCEPTANCE**, zero BLOCKING/MAJOR/MINOR findings (two
NOTEs only — a trivial local loose-object-size variance, and disclosed model/account overlap with the
authoring session — neither requiring correction). Retained principal-acceptance comment
`issuecomment-5158527253`, independently refetched this session and confirmed posted on `PR #224`,
explicitly naming exact head `ab9fb6b49b55f8cf575c2e8d4267e8e15bce52d3` and bounding its own scope to
exactly: deterministic mechanical-preflight capacity for the full 220-image governed library; a
25-image, single-timeframe Stage 1 implementation-PR ceiling; the recommended 19-name first cohort;
five-ticker review shards with one final exact-head integration review; and repository-native,
LFS-free evidence storage with the disclosed ~250 MB stopping condition and GitHub release-asset
fallback — while explicitly not authorizing a live preflight, image retention, chart interpretation,
Stage 1, Stage 2, processing of the cohort, automatic continuation, portfolio-policy changes, trading,
or execution. This session independently re-verified `origin/main` and local `HEAD` both at
`3d8ad7896236148e57e9bef3dd8fc003ef55b07a` before drafting this section, zero open pull requests, and
`CHART-0002`'s frontmatter and `governance/decisions.yaml` entry both still reading `status: Proposed`
immediately prior to this commit.

**Why this sequencing is not the same defect `CHART-0001`'s own review (`4835983890`) found, and does
not require the same corrected multi-commit sequence.** `CHART-0001`'s premature-status finding turned
on a specific fact: at the moment that filing's own first commit set `status: Accepted`, no
separately retained, PR-specific principal-acceptance comment existed anywhere for that content — the
acceptance-recording note itself was the only thing asserting acceptance, which is exactly the
self-certifying pattern that finding rejected. Here, the content being recorded (the scale-and-
throughput amendment, §§A-Q above) was independently reviewed, explicitly principal-accepted at its
exact head, and merged to `main` **entirely within a prior, separate, already-closed pull request
(`PR #224`)** before this acceptance-recording PR was even branched. `issuecomment-5158527253` is not
this filing's own assertion of acceptance — it is a pre-existing, independently verifiable historical
artifact this filing merely cites and reconfirms. Setting `status: Accepted` in this commit therefore
transcribes an acceptance that already, separately, fully closed; it does not assert a new one. This
distinction does not exempt this filing's own pull request from its own independent exact-head review
and explicit principal approval before merge (required immediately below) — it means the *content*
change is not premature the way `CHART-0001`'s was, while this *PR's own lifecycle gate* remains fully
intact and unweakened.

**Effect — exactly what becomes Accepted, and what does not.** This activates exactly what the
amendment's own §§A-Q already, conditionally, defined — no authority beyond what was already stated,
pending acceptance:

- The two-layer Layer A/Layer B/Layer C architecture (§G) is now the accepted, controlling
  architecture for any future chart-evidence work under `CHART-0002`.
- Layer A's all-220 deterministic mechanical-preflight methodology (§E) is confirmed capacity-testing
  methodology; re-running it produces no committed artifact and requires no further authorization —
  it was already run, live, read-only, with no repository-side effect, in the amendment's own session.
- The 25-image, single-timeframe general ceiling for future Layer-B implementation PRs (§H), and the
  five-ticker review-shard/failure-isolation architecture for a batch up to that ceiling (§I), are now
  the accepted, controlling architecture for a future batch proposal.
- The recommended first cohort — the full current 19-name eligible universe under §13's unmodified
  selection rule (`AMZN, ASML, AVGO, CEG, COST, ETN, GEV, GOOGL, ISRG, KLAC, LLY, META, MSFT, NVDA,
  PANW, PWR, TMO, TSM, V`) — is now the accepted basis a future implementation PR may propose to
  process, at `1D` only, Stage 1 only, zero Stage 2 records.
- The storage recommendation (§J: primary Option A — repository-native, LFS-free, hash-manifested
  evidence packages, unchanged from `CHART-0001`; fallback Option D — GitHub release assets with
  in-repo manifests/hashes; Git LFS confirmed not installed and not adopted) and its ~250 MB
  repository-size stopping condition (§M) are now the accepted, controlling storage architecture.
- The supersession table (§K) is now controlling: the original five-image §8/§14/§16/§21/§26 terms are
  superseded for future operative purposes exactly as that table states: the original text remains
  intact as historical record of the superseded five-image proposal.

**Not authorized by this note, now or as a consequence of it alone:** a live Layer A run against any
image; retention, copying, cropping, or redaction of any image; any chart interpretation or
chart-derived fact; any Stage 1 or Stage 2 record; processing of the 19-name cohort or any subset of
it; automatic continuation to an implementation PR; any second acceptance-recording action; any
tier/target/holdings/gate/cluster/cap change; any dashboard or Company/Theme Intelligence coupling;
any margin or allocator change; any trading signal, brokerage access, or execution; enabling Git LFS,
creating another repository, or uploading release assets; opening the future 19-chart implementation
branch or PR (none exists as of this note, and none is created by this filing). A first Layer-B batch
still requires its own further, separate, later, explicit principal authorization and implementation
PR, under its own full `OPS-0007` §1 review cycle and explicit principal acceptance at its own exact
final head, before it may merge — unchanged from §Q, resized by nothing in this note.

**This session performed no chart analysis and retained no chart image.** No path under
`~/Projects/Chart-Automation` or `~/Downloads` was read, written, or modified. This note performs no
repository mutation beyond this file, `governance/decisions.yaml`'s status field,
`operations/WORKSTREAMS.yaml`'s `WS-0012` entry, and one `CLAUDE.md` Decisions Log pointer — the same
four-file core scope the controlling authorization above bounds this filing to.

**Effectiveness of this note and this PR.** Per `governance/decisions/README.md`'s convention and
identical in kind to §Q's own three-gate discipline: this note, the frontmatter `status` change above,
and every downstream file this session touches take effect only when this recording pull request is
itself independently reviewed under `OPS-0007` §1, any required bounded correction is made and
re-reviewed, and the principal explicitly approves it at its own exact final head before merge,
followed by complete post-merge verification per `OPS-0009` §4(a). This note does not mark its own PR
ready and does not merge it. This authorization does not yet authorize the 19-chart implementation
batch — that remains gated on its own further, separate, later, explicit principal authorization and
implementation PR, exactly as stated above and in §Q.
