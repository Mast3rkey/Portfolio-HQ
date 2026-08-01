---
decision_id: CHART-0001
date: 2026-08-01
status: Accepted
category: chart_evidence_governance
related_decisions: [GOV-0001, GOV-0002, OPS-0001, OPS-0007, OPS-0009, OPS-0011, PI-0001, PI-0011, LADDER-0001, PHQ-2026-06]
supporting_artifact: null
---

## Context

**Preflight performed this session, independently verified, not assumed.** Repository confirmed
`Mast3rkey/Portfolio-HQ`; `origin/main` fetched and pruned; local branch
`claude/lane-g-chart-0001-proposal-qbg54r` confirmed identical to `origin/main` at
`44c74473e8affed3e8aa6b1a2e5a684d65a2c1e9` (the merge commit of PR #217, `OPS-0013`'s Governance
Decision Explorer implementation), zero divergence in either direction, working tree clean.
**Zero open pull requests** exist in the repository (`mcp__github__list_pull_requests`, `state:
open`, confirmed empty). A repository-wide code search for `CHART-0001` returns zero hits, and a
targeted grep of `governance/decisions.yaml`, `decision_log.yaml`, and every file under
`governance/decisions/` finds no existing `CHART-####` series — confirming `CHART` as a genuinely
new, unclaimed decision-domain prefix, per `governance/decisions/README.md`'s rule that a new
prefix is chosen only when a genuinely new domain needs one, not pre-declared. `governance/
decisions.yaml` carries 58 entries, reconciling exactly 1:1 against the 58 non-`README.md` files
under `governance/decisions/` — highest filed `OPS-####` is `OPS-0013`, highest `PHQ-####` is
`PHQ-2026-06`, highest new-domain single-charter series is `LADDER-0001`. `operations/
WORKSTREAMS.yaml` carries ten workstream entries, `WS-0001` through `WS-0010` — confirming
`WS-0011` as the next unused identifier, checked live against the register rather than assumed.
No branch name or open PR anywhere in the repository concerns chart evidence, TradingView, or any
similarly-shaped record type. `intelligence/companies/NVDA.yaml` exists, `portfolio_role_ref: T1`,
`conviction.rating: High`, most recently corrected under `PI-0018`'s implementation — confirming a
live Company Intelligence record exists for the proposed pilot's default asset and could support a
fundamental cross-check, independently verified rather than assumed from the authorizing prompt.

**Principal authorization (verbatim, this session):** "I authorize preparation of a narrowly
bounded Lane G governance proposal, provisionally designated CHART-0001, for one chart-evidence
pilot. The proposal may define an advisory record type, privacy and provenance requirements, one
proposed workstream, and a one-asset/one-screenshot pilot. It must authorize no bulk ingestion,
dashboard implementation, scoring, trading signals, tier or target changes, margin changes,
allocator coupling, or brokerage action. Draft and review the governance proposal before any chart
evidence is committed." This authorization is narrow and explicit: it authorizes *preparing* this
proposal, not *accepting* its content. **Nothing in this filing constitutes principal acceptance of
CHART-0001 itself** — that is a separate, later, explicit step this filing does not take and cannot
take on the principal's behalf. Accordingly this decision's own `status` is `Proposed`, not
`Accepted` — the first decision filed under this governance layer to use that status value, since
every prior filing already carried explicit principal content-approval language before drafting
began. Filing this proposal on a branch and opening a draft PR does not change that.

**What gap this addresses.** Manual, conversational chart-reading (trendlines, moving averages,
support/resistance context read visually from a platform like TradingView) already happens
informally in some sessions but leaves no repository record — unlike Company Intelligence
(`docs/PORTFOLIO_INTELLIGENCE_SPEC.md`, fundamentals-only, frozen schema, advisory-only per its
own §20) or the buy-ladder research charter (`LADDER-0001`, which explicitly excludes chart-pattern
or screenshot-derived input from its own study, protocol §8). This proposal is not an extension of
either — Company Intelligence's frozen schema is not touched, and `LADDER-0001`'s numerical,
reproducible research protocol is unaffected and remains the sole authority on what feeds that
study. Chart evidence, if this proposal is later accepted and its pilot separately implemented, is
a third, independent, advisory-only evidence track with no coupling to either.

**Reconciling the repository's own differing screenshot-retention practice, explicitly.** Two
different patterns already exist for brokerage-adjacent screenshots: `PHQ-2026-02`/`PHQ-2026-04`/
`PHQ-2026-05` each disclosed a screenshot was reviewed in-session but deliberately *not* retained in
the repository (a narrower evidence-retention choice, stated as such); `PHQ-2026-06` *did* retain a
full Robinhood "Account Summary" screenshot (`governance/evidence/PHQ-2026-06/
robinhood_account_summary_20260801.webp`) showing total account value, cash, buying power, and
margin figures, alongside a `MANIFEST.json` recording its SHA-256, provenance chain, and
verifiability boundary. Neither practice is silently picked here. `PHQ-2026-06`'s retained image
carries live account-balance figures because the decision it evidences *is* a cash-balance
reconciliation — the balance is the fact being synchronized. A chart-evidence screenshot has no
comparable need to show account balances, positions, or brokerage identifiers at all — its entire
evidentiary value is the price chart itself. §5 below therefore sets a privacy standard for this
pilot that is **stricter than `PHQ-2026-06`'s own retained image**, not merely a restatement of it:
balances, account numbers, and brokerage-account identifiers are barred from a retained chart
screenshot outright, not merely disclosed. This does not revise or reopen `PHQ-2026-06`, which
remains valid for what it actually evidences.

## Decision

**CHART-0001 authorizes exactly the preparation, definition, and independent review of this
proposal.** It commits no chart evidence, creates no `chart_evidence/` directory or file, creates
no Company Intelligence record or edit, and creates no current chart-evidence record of any kind.
If, and only if, this proposal is later independently reviewed and explicitly accepted by the
principal — a status change this filing does not itself make — it would then authorize exactly one
future, separate, bounded implementation PR for one one-asset/one-screenshot pilot per §8 below,
itself gated on its own full review and merge cycle. No implementation begins in this session, and
none may begin before that future acceptance.

### 1. Purpose and status

This is an advisory chart-evidence *pilot proposal* only. If accepted and later piloted, chart
evidence would be supplementary, dated, non-authoritative, and subordinate to the Investment
Constitution, every accepted governance decision, `holdings.yaml`, `targets.yaml`, current Company/
Theme Intelligence, and executable allocator policy — squarely at or below level 7-8 of `GOV-0002`'s
precedence hierarchy (generated/derivative, non-authoritative synthesis), never able to move or
create authority at any higher level. This filing itself commits no evidence, creates no current
chart-evidence record, and does not itself become effective until independently reviewed and
merged — and even then, only §§1-13 of this governance text become effective; the pilot itself
requires its own further separate implementation PR under its own full review cycle (§8-§9).

### 2. Explicit non-authority

This decision authorizes **none** of the following, now or as an implied consequence of anything
below, without its own separate, later, explicitly accepted governance decision:

- bulk screenshot ingestion of any kind, in this filing or the future pilot;
- recurring or automatic ingestion, scheduled capture, or any standing monitoring process;
- automatic chart interpretation (OCR-driven or otherwise) as a substitute for human-reviewed
  analyst judgment;
- OCR-derived market-data authority of any kind — no chart-derived figure may be treated as a price,
  quantity, or market datum for any production purpose;
- chart-pattern systems (flags, head-and-shoulders, wave counts, or any comparable automated
  pattern classifier) — the Decisions Log already ruled chart-pattern reading "not computable, not
  backtestable" (July 2026, `reports/rung_backtest.md`-era entry), and nothing here reopens that;
- scoring, ranking, aggregation, or any technical-signal generation of any kind;
- price targets or opportunity maps of any kind;
- trading signals or recommendations represented, worded, or formatted as execution instructions;
- any change to tiers, targets, weights, holdings, buys, trims, sells, margin, allocator output,
  brokerage behavior, or trading behavior of any kind;
- use as `LADDER-0001` study or backtest input — `LADDER-0001` protocol §8 already independently
  excludes chart-pattern/screenshot-derived input from that charter, and this filing does not touch,
  narrow, or reinterpret that exclusion;
- use as a substitute for primary-source fundamental evidence in any Company or Theme Intelligence
  record;
- direct mutation of any existing Company or Theme Intelligence record — chart evidence, even once
  piloted, is never written into `intelligence/companies/*.yaml` or `*.md`;
- extension of the frozen Company Intelligence schema (`docs/PORTFOLIO_INTELLIGENCE_SPEC.md` §9,
  §20, §24, incorporated into the Constitution at level 1 per `GOV-0002`) in any respect — chart
  evidence is a wholly separate, independent record type, never a new field, section, or attachment
  on an existing company record;
- dashboard implementation, integration, or display of any kind (`OPS-0011`/`OPS-0012`/`OPS-0013`
  remain entirely unaffected and untouched);
- browser uploads, remote network calls, or repository writes originating from any UI;
- any order placement or brokerage action of any kind — order methods remain absent from
  `alpaca_client.py`, unchanged.

### 3. Advisory record type (logical schema, non-executable)

If this proposal is later accepted, a future implementation may define — but does not define here as
executable code, a YAML/JSON Schema file, or a validator — a single logical **Chart Evidence
Record**, distinguishing fact from interpretation throughout. No numeric technical score, composite
rating, automatic classification, or capital-priority ranking is part of this record type, now or
under any future pilot without its own separate authorization. The record's fields, grouped for
clarity only (no grouping is itself schema-binding):

| Group | Fields |
|---|---|
| **Identity & capture** | evidence ID; asset/ticker; asset type (equity, ETF, crypto); timeframe (e.g. daily, weekly); capture timestamp and timezone; source platform (e.g. TradingView); retained filename; retained-file SHA-256; file type; image dimensions; known or unknown indicator settings (disclosed as unknown, never invented, when not legible or not confirmed) |
| **Content — fact-to-interpretation gradient, kept strictly separate** | visible facts (what is literally legible in the image — price levels, dates, drawn lines already present, indicator values if shown); observations (a human or analyst noticing a pattern in the visible facts, still descriptive); inferences (an interpretive judgment drawn from the observations, labeled as inference, never presented as fact); uncertainty (what is not legible, not confirmed, or ambiguous, disclosed rather than silently resolved) |
| **Governance & advisory content** | portfolio relevance (why this asset/evidence matters to the current holding, if any); whether fundamental cross-checking against existing Company Intelligence is required before any advisory weight is given; advisory recommendation (worded as advisory, never as an execution instruction); governed consequence (normally `none` — the record changes no tier, target, holding, or allocator output unless a separate future governance decision says otherwise for that specific record); analyst/model/session provenance; principal acceptance state (distinct from, and recorded separately from, analyst authorship) |
| **Relationships** | related holdings (ticker cross-reference only); related Company/Theme Intelligence records (reference only, no mutation); related accepted governance decisions |
| **Lifecycle** | freshness/review date; supersedes / superseded-by relationship to any prior evidence record for the same asset |

This table is illustrative of the logical shape a future pilot record would need to preserve every
element the principal's authorization named — it is not itself a schema file, is not validated by
any code, and creates no record. A future implementation PR, if this proposal is accepted, defines
the actual file format (most likely YAML, matching this repository's existing structured-record
convention) as part of its own separately reviewed scope.

### 4. Storage model

If accepted, the future one-asset/one-screenshot pilot (§8) is authorized to use exactly a bounded
hybrid model, reusing this repository's existing evidence-package/manifest/hash pattern
(`governance/evidence/<decision-id>/...`, the pattern `PHQ-2026-01` through `PHQ-2026-06` already
established) rather than inventing a new subsystem or a new top-level directory:

- Exactly one selected, decision-relevant screenshot may eventually be retained, under
  `governance/evidence/CHART-0001/<pilot-slug>/`, as a byte-for-byte copy — not cropped, annotated,
  or recompressed beyond what §5's privacy redaction requires.
- That screenshot must be accompanied by exactly one structured advisory record (per §3's logical
  schema, materialized as one YAML file in the same package directory) and one `MANIFEST.json`
  recording displayed/visible figures, hash, byte size, media type, and provenance — mirroring
  `PHQ-2026-06`'s `MANIFEST.json` shape, including its `provenance_chain` and `verifiability_
  boundary` structure.
- One `README.md` in the same package directory, mirroring the existing `governance/evidence/*/
  README.md` convention, describing scope and explicitly stating what the package does and does not
  evidence.
- Routine screenshots viewed or discussed in ordinary conversation remain conversation context and
  are never committed to the repository.
- No batch of screenshots is ever ingested under this pilot — exactly one, for exactly one asset.
- Historical chart evidence, once retained, is dated archive evidence only — it never becomes live
  market-data authority, and no production code may read it as a price or quantity source.
- No `chart_evidence/index.yaml` or comparable index file is created — if a second or later record
  is ever separately authorized, this repository's existing filesystem-as-index doctrine (`PI-0001`,
  reaffirmed for Theme Intelligence by `PI-0006`) is the default starting point for any such future
  design question, not decided here.

This section authorizes a storage *model* for a future, separately gated pilot — it does not create
`governance/evidence/CHART-0001/` or any file inside it now.

### 5. Privacy

Every image considered for retention under a future pilot must receive an **explicit privacy
review** before retention, recorded in that package's `MANIFEST.json`. For this proposed pilot,
stricter than `PHQ-2026-06`'s own retained brokerage screenshot (§ Context above):

- Account balances, account numbers, brokerage-account identifiers, position lists, order history,
  buying-power/margin figures, or any other financial-account identifier must not enter the public
  repository via a chart-evidence screenshot, full stop — a chart screenshot's entire evidentiary
  value is the price chart itself, and it carries no legitimate need to also show account state.
- An image that cannot be made safe (cannot be cropped or redacted to remove the above while still
  preserving the chart's evidentiary content) must be rejected outright and not retained — the pilot
  proceeds with no evidence for that asset, or is deferred, rather than accepting an unsafe image.
- The retained file's SHA-256 must identify the actual retained copy, computed after any redaction
  or transformation, not before.
- Any redaction, cropping, or transformation applied must be recorded in the package's manifest —
  what was changed, and why — following the same disclosure discipline `PHQ-2026-06`'s manifest
  already applies to its own provenance chain.
- **Named, bounded exception, stated by the principal in this authorizing session**: a visible
  platform username that the principal has explicitly approved for the specific retained image,
  if it appears in a chart screenshot, is acceptable and does not by itself require redaction —
  the actual identifier is recorded only in that image's own pilot package manifest, not restated
  in general governance prose. This is a narrow, single-fact exception — it does not waive any
  other privacy requirement above, and it does not extend to any other personal or financial
  information that might also be visible (email, real name, brokerage account details, watchlist
  contents revealing other unrelated positions, private notes, or any other identifying data), all
  of which remain subject to the full redaction standard above.

### 6. Provenance and claim boundary

A future pilot record must carry, at minimum: source platform and capture time (with timezone);
retained filename (subject to §5's privacy rules — an original filename that itself leaks private
information is not retained verbatim); SHA-256 of the retained copy; analyst/model and session
attribution; a clear, structural separation of screenshot-visible facts from interpretation (§3);
explicit uncertainty disclosure wherever the image is ambiguous or a detail is not legible; an
explicit statement that a chart screenshot is **secondary observational evidence**, not inspected
issuer or regulatory primary evidence, and must never be presented or relied upon as if it were;
claim-level linkage to any related holding, Intelligence record, or governance decision where
practical; principal acceptance recorded as its own field, separate from and never conflated with
analyst authorship. No fabricated inspection, provenance, indicator setting, or market datum is
permitted at any point — an indicator setting that cannot be confirmed from the image itself is
recorded as unknown, never guessed.

### 7. Freshness and supersession

A chart-evidence screenshot is **point-in-time evidence**. A future pilot record must define an
explicit review/expiration schedule proportional to the asset and timeframe captured (a daily chart
goes stale faster than a weekly one) — staleness requires disclosure or analyst abstention from
relying on the record, never an automatic demotion, sale, target change, or policy change of any
kind, matching the discipline `OPS-0006` §14 already applies to Company/Theme Intelligence
freshness and `PI-0011`/`AUTO-0001` already apply to their own staleness reporting. A refresh
creates a **new** evidence record, never an overwrite of the prior one; the prior record is retained
as historical context and linked forward via an explicit `supersedes`/`superseded_by` relationship
(§3). This pilot creates no standing monitoring system, no scheduled recapture, and no automated
staleness scanner of any kind — matching `LADDER-0001`'s and `OPS-0006` §15's own explicit
prohibition on any such automation being implied by a bounded evidentiary or research authorization.

### 8. One-asset / one-screenshot pilot

**Not authorized by this filing.** If, and only if, this proposal (CHART-0001) is independently
reviewed and explicitly accepted by the principal in a later step, it would then authorize exactly
one future, separate, bounded implementation PR containing:

- one asset;
- one screenshot;
- one timeframe;
- one structured advisory record (§3);
- one evidence package (§4);
- itself gated on its own independent, exact-head review per `OPS-0007` §1 and `OPS-0009` Lane G
  (this filing, and any future implementation of it, is Lane G in full — a new governance
  authorization, never reduced), any required bounded correction and exact-head re-review, and
  explicit principal acceptance before that implementation PR may merge.

**Default proposed pilot asset: NVDA, daily timeframe**, from the manual chart-analysis work already
completed in prior conversation. NVDA is used as the default because it already carries an
established Company Intelligence record (`intelligence/companies/NVDA.yaml`, `portfolio_role_ref:
T1`, `conviction.rating: High`, independently confirmed present and current this session), which
permits a clear fundamental cross-check per §3's "whether fundamental cross-checking is required"
field — the same reason a future implementation session would not need to originate that
cross-check from nothing. **This governance PR does not contain, recreate, restate, or summarize
that screenshot or its analysis** — no chart image, no extracted chart fact, and no chart-derived
observation appears anywhere in this filing. If repository evidence, at the time a future
implementation is actually attempted, establishes that another pilot asset is materially safer
(e.g., a cleaner privacy profile) or better governed (e.g., a more current Intelligence record),
that future implementation session must explain the substitution reasoning in its own filing rather
than silently choosing a different asset.

### 9. Pilot acceptance criteria

A future one-asset/one-screenshot pilot implementation, if separately authorized and attempted, must
satisfy at minimum, before its own PR may merge:

- the exact source image is reliably identified (matching `PHQ-2026-06`'s own disclosed standard for
  what "identified" means when a claimed filesystem path does not exist);
- privacy review passed per §5, with any redaction disclosed;
- the retained copy's SHA-256 is independently verified against the manifest;
- the structured record cleanly distinguishes fact, observation, inference, and uncertainty per §3
  — no field blurs the boundary;
- no indicator setting, date, or price level is invented — unknowns are recorded as unknown;
- no numeric score, composite rating, or trading signal is produced;
- no allocator, margin, holdings, target, Company/Theme Intelligence schema, dashboard, or brokerage
  coupling is introduced anywhere in the implementation;
- every relationship link (related holding, related Intelligence record, related governance
  decision) resolves to something that actually exists;
- the freshness/review-date and supersession fields validate against §7;
- independent review is attributable (a retained GitHub review/comment thread or a `governance/
  audits/` artifact) and anchored to the exact final head, per `OPS-0007` §1;
- the principal explicitly accepts the pilot at that exact final head before merge.

### 10. Stopping and rejection conditions

A future pilot attempt must stop, or be rejected outright, if any of the following holds:

- the source image cannot be reliably identified;
- required metadata (capture time, source platform, asset, timeframe) cannot be established without
  invention;
- sensitive information in the image cannot be safely redacted consistent with §5;
- the analysis cannot cleanly separate visible fact from interpretation;
- the implementation attempts to introduce technical scoring, prediction, an automatic
  recommendation, or any allocator/trading coupling of any kind;
- satisfying the pilot would require weakening any existing paper-only, read-only, secrets-handling,
  or no-order safeguard anywhere in this repository;
- the change cannot be implemented as a small, reversible unit;
- the claimed utility does not justify the resulting ongoing repository size, review burden, or
  maintenance cost.

### 11. Future phases — not authorized by this filing

CHART-0001 does not authorize, now or as an implied consequence of any acceptance of this proposal
alone: scaling beyond the single pilot record; ingestion of any batch of screenshots (2, 4, or any
other number); a recurring or scheduled refresh process; a dashboard surface of any kind; automated
validation beyond what the one pilot implementation's own narrow scope needs; technical research or
backtesting use of chart evidence (including, explicitly, any use as `LADDER-0001` input); or any
linkage of chart evidence into portfolio recommendations, allocator output, or Company/Theme
Intelligence content. Every such expansion requires its own later, separately reviewed and
principal-accepted governance decision, grounded in evidence from how the single pilot actually
performed — not assumed in advance from this filing.

### 12. Workstream

This filing establishes `WS-0011` in `operations/WORKSTREAMS.yaml` (`status: proposed`, `priority:
secondary` — `WS-0005` remains the repository's sole `priority: primary` workstream, unaffected by
this filing) recording: CHART-0001 proposed, not accepted; no chart evidence committed; no pilot
implementation begun; independent review and explicit principal acceptance of CHART-0001's own
content required before this authorization is effective, and — even then — a further, separate,
bounded implementation PR (§8) is required before any pilot record exists. The workstream records
state; it originates no authority of its own, matching `OPS-0001`'s own founding constraint on the
register.

### 13. Governance package scope (this filing)

This filing touches exactly:

1. `governance/decisions/CHART-0001-chart-evidence-pilot-governance-proposal.md` (this file).
2. `governance/decisions.yaml` (index regeneration: one new entry for `CHART-0001`).
3. `operations/WORKSTREAMS.yaml` (one new entry, `WS-0011`, per §12 above).
4. `CLAUDE.md` (one concise Decisions Log pointer entry, matching this repository's unbroken
   convention of recording every filed governance decision there at filing time — worded to reflect
   `Proposed`, not `Accepted`, status).

**No other file is touched.** No chart image, no chart analysis, no `chart_evidence/` directory, no
Company/Theme Intelligence file, no dashboard code, no `holdings.yaml`/`targets.yaml`/`gates.yaml`/
`issuer_lookthrough.yaml`, no `allocate.py`/`margin_state.py`/`levels.py`, no Constitution text, and
no `research/buy_ladder_backtest/**` file is touched by this filing.

### 14. Effectiveness, review, and merge gates

This governance PR must remain in **draft** state. Before it may even be considered for
independent review as a candidate for merge, it requires, in this order: (a) independent, exact-head
review by an eligible reviewer per `OPS-0007` §1 (this is `OPS-0009` Lane G — a new governance
authorization, always full weight, never reduced); (b) any required bounded correction and exact-head
re-review; and (c) **explicit principal acceptance of CHART-0001's own content** — a distinct,
later step from the principal's authorization to prepare this proposal, and one this filing
explicitly does not claim to have received. **This decision does not mark itself ready, does not
authorize its own merge, and does not authorize beginning the §8 pilot implementation.** Nothing in
§§1-13 above becomes effective until this PR merges to `main`, and even then, only the governance
text itself takes effect — the pilot remains gated on its own further, separate implementation PR
and review cycle.

## Rationale

**Why a new `CHART-####` prefix, not `PI-####` or an extension of `docs/PORTFOLIO_INTELLIGENCE_
SPEC.md`.** Company Intelligence's own frozen schema (`PI-0001`, §20/§24 of the spec, incorporated
into the Constitution) is fundamentals-only, advisory-only, and permanently non-coupled to
production — chart evidence is a structurally different kind of record (visual, price-chart-derived,
carrying its own distinct privacy surface a fundamentals record never has) and forcing it into the
`PI-####` series or the existing spec would either dilute that frozen schema's own discipline or
require reopening a frozen document for an unrelated purpose. `governance/decisions/README.md`'s own
rule — a new prefix only when a genuinely new domain needs one — is independently satisfied here,
the same reasoning `LADDER-0001` already applied when it declined to reuse `PHQ-####` or
`MARGIN-####` for a genuinely different research domain.

**Why `LADDER-0001` is the closest structural template, not a fresh design.** Both are bounded,
new-domain charters that authorize a later, separate implementation PR rather than any immediate
result; both explicitly forbid extrapolation into production policy without a further governance
decision; both stay in draft, unmerged, pending independent review and principal acceptance. Reusing
that shape here — rather than inventing new charter mechanics for chart evidence specifically — keeps
this filing's own review surface bounded to what actually differs (an advisory record type and its
privacy standard), not the charter mechanism itself.

**Why `status: Proposed`, not `Accepted`, unlike every prior filing in this governance layer.** Every
decision from `GOV-0001` through `PHQ-2026-06` was filed only after the principal had already given
explicit content-approval language in the authorizing conversation — the open question in each case
was independent review and merge, not whether the principal had approved the substance. Here, the
principal's own authorization is explicit that only *preparation* is authorized and that
*acceptance* is a distinct, later, unperformed step. Marking this `Accepted` would misstate that
fact. `Proposed` is the first live use of that status value in `governance/decisions/`, exactly
matching `governance/templates/decision_template.md`'s own vocabulary (`Proposed | Accepted |
Superseded | Archived`), which every prior filing had simply never needed.

**Why the privacy standard is stricter than `PHQ-2026-06`'s own retained image, not a restatement of
it.** `PHQ-2026-06` retained a full account-summary screenshot because the fact it evidences *is* an
account balance. A chart-evidence screenshot's entire evidentiary value is the price chart; it has
no comparable reason to also disclose account balances, positions, or brokerage identifiers, so §5
bars them outright rather than merely disclosing them the way `PHQ-2026-06`'s manifest discloses its
own account figures. Reconciling this explicitly, rather than silently picking one of the
repository's two existing screenshot-retention patterns, follows the same "material contradiction
must be surfaced, not silently resolved" rule `GOV-0002` already establishes for conflicts between
governed sources.

**Why NVDA/daily is the default proposed pilot asset.** It is the only asset named in the
authorizing conversation's already-completed manual chart work, and it independently verifies
(§ Context) as carrying a current, high-conviction Company Intelligence record — the one factual
precondition §3's "fundamental cross-checking" field exists to support. Naming a default here, while
explicitly forbidding the screenshot or analysis itself from entering this filing, keeps the future
implementation session from having to re-derive which asset was intended, without smuggling any
chart content into a governance-only PR.

**Why storage reuses the existing evidence-package pattern rather than a new top-level directory.**
The principal's own authorization requires the retained artifact to "follow an existing
repository-native evidence package and manifest/hash pattern wherever possible rather than creating
a new subsystem." `governance/evidence/<decision-id>/` already exists, is already used for six prior
decisions (`PHQ-2026-01` through `PHQ-2026-06`), and already carries exactly the
screenshot-plus-manifest-plus-README shape a chart-evidence package needs. Inventing a parallel
`chart_evidence/` filesystem-as-index subsystem, modeled on `intelligence/`, was considered and
rejected for that reason (see Alternatives Considered) — it would be a second subsystem doing what
the first already does.

## Alternatives Considered

- **File under `PI-####`, treating chart evidence as a Company Intelligence extension.** Rejected —
  explicitly barred by the principal's own authorization (no extension of the frozen Company
  Intelligence schema) and, independently, because chart evidence's privacy surface and evidentiary
  shape are different enough from a fundamentals record to warrant a genuinely separate type, not a
  new field bolted onto an existing frozen one.
- **A new top-level `chart_evidence/` directory with its own filesystem-as-index, mirroring
  `intelligence/`.** Rejected for this pilot — the principal's authorization directs reuse of an
  existing evidence-package pattern "rather than creating a new subsystem," and `governance/
  evidence/CHART-0001/` already satisfies every structural need §3/§4 name without a second
  subsystem. Not foreclosed for a much later, separately authorized expansion phase if one is ever
  proposed and justified on its own evidence.
- **Mark this decision `status: Accepted`, since every prior filing in this series has been.**
  Rejected — would misstate the principal's own authorization, which is explicit that only
  preparation, not acceptance, is authorized here. `Proposed` is the accurate, template-defined
  value.
- **Include the actual NVDA chart screenshot or its extracted facts in this governance PR, to make
  the pilot definition concrete.** Rejected — explicitly barred by the principal's authorization
  ("Draft and review the governance proposal before any chart evidence is committed") and by the
  task's own objective statement ("The governance PR itself must contain no chart screenshot, no
  extracted chart facts... and no implementation code").
- **Skip the `CLAUDE.md` Decisions Log entry, since CHART-0001 is not yet accepted.** Rejected —
  every prior filing in this repository, including several still in draft/unreviewed state at
  filing time (`LADDER-0001`, `OPS-0012`, `OPS-0013`, `PHQ-2026-06`), received a `CLAUDE.md` pointer
  entry immediately upon filing; the live, unbroken convention is to record the filing itself, worded
  to match its actual status — here, `Proposed`, not `Accepted`.
- **Skip the workstream entry, since no implementation is authorized yet.** Rejected — `LADDER-0001`
  established the precedent of recording a `proposed`-status workstream for a not-yet-effective
  charter (`WS-0010`), and doing the same here keeps CHART-0001's status discoverable across
  sessions without asserting any authority the register itself does not have.

## Consequences

**Authorized, effective only on this decision's merge, and only to the extent stated:** the
definitions in §§1-11 above (purpose/status, explicit non-authority, the logical advisory-record
schema, the storage model, the privacy standard, the provenance/claim-boundary standard, the
freshness/supersession rule, the bounded one-asset/one-screenshot pilot description, its acceptance
criteria, its stopping/rejection conditions, and the explicit future-phase exclusions); `WS-0011` as
a `proposed` workstream tracking this authorization. **Even upon merge, no chart-evidence pilot
implementation is authorized to begin** — that requires its own further, separate, later
implementation PR under its own full independent-review and principal-acceptance cycle (§8, §14).

**Not authorized by this filing, now or ever without a further separate decision:** any chart
screenshot, chart analysis, or chart-derived fact committed to the repository; any `chart_evidence/`
directory, file, schema, or validator; any Company/Theme Intelligence record edit or schema
extension; any dashboard integration; any scoring, ranking, or trading-signal generation; any
tier/target/holdings/margin/allocator/brokerage change; any use as `LADDER-0001` or any other
research/backtest input; any bulk or recurring ingestion; any second pilot asset or record.

**Unchanged by this decision:** the Investment Constitution; every existing accepted governance
decision; `docs/PORTFOLIO_INTELLIGENCE_SPEC.md` and every existing Company/Theme Intelligence
record, including `intelligence/companies/NVDA.yaml`; `targets.yaml`, `holdings.yaml`, `gates.yaml`,
`issuer_lookthrough.yaml`; `allocate.py`, `margin_state.py`, `levels.py`; `LADDER-0001`'s research
charter and its own chart-pattern/screenshot exclusion (protocol §8); `OPS-0011`/`OPS-0012`/
`OPS-0013`'s dashboard capability and its own boundaries; the 1.8x leverage cap and 30% buffer floor;
`PHQ-2026-06` and every other prior `PHQ-####` decision, exactly as filed.

This decision — including its own acceptance, not only its merge — requires a further, explicit,
later principal step this filing does not take. This decision becomes effective, to the bounded
extent stated above, only when its implementing pull request is independently reviewed, explicitly
accepted by the principal, and merged to `main`.

---

## Principal acceptance and pilot-preparation authorization (2026-08-01)

_Dated note appended per `governance/decisions/README.md`'s convention for a narrow, additive
lifecycle correction — §§1-14, Rationale, Alternatives Considered, and Consequences above are
unedited and remain exactly as originally filed and merged. Frontmatter `status` is updated to
`Accepted` above, alongside this note, mirroring `PI-0034`'s own status-transition precedent._

**Live state, independently reverified before this note, not assumed.** PR #218
(`claude/lane-g-chart-0001-proposal-qbg54r`) is confirmed merged to `main` at merge commit
`9b85ee163ae978d2d8f4aa68c9b9b23dc66892cd`, carrying this file to parent head
`4f7c1f60e46c6b4f49a65dbb86be245250202b9c` — the exact head an independent delta review verdicted
**"DELTA APPROVED — APPROVED FOR PRINCIPAL ACCEPTANCE,"** finding zero surviving MATERIAL or MINOR
findings and naming "explicit principal acceptance of CHART-0001's own content" as the one remaining
gate before merge. That review did not itself accept the content, mark the PR ready, or merge it.
This note is that separate, later, explicit principal-acceptance step — distinct from, and later
than, both the original preparation authorization and PR #218's merge.

**Principal authorization (verbatim, this session):** "I accept the CHART-0001 chart-evidence
framework in principle and authorize a narrowly bounded governance update to record that acceptance
and authorize preparation of one isolated, read-only one-image pilot. The pilot may test ingestion,
provenance, structured observation, uncertainty disclosure, and report formatting only. It must not
create automatic scoring, rankings, trading signals, buy/sell recommendations, tier or target
changes, holdings changes, allocation changes, margin changes, allocator coupling, bulk chart
analysis, or brokerage actions. Implementation must occur in a separate future draft PR, receive
independent exact-head review, and return to me for approval before merge."

**Effect.** This activates exactly what §§1-13 above already, and only, defined — this note creates
no authority beyond what was already conditionally stated, pending acceptance:

- §§1-7 (purpose/status, explicit non-authority, the logical advisory-record schema, the storage
  model, the privacy standard including its named username exception, the provenance/claim-boundary
  standard, and the freshness/supersession rule) are now the accepted, controlling definition for any
  future chart-evidence work in this repository.
- §8's bounded one-asset/one-screenshot pilot description is now the accepted basis on which a
  future, separate implementation PR **may be prepared and opened** — preparation only. §8's own
  gating is unchanged and unweakened: that future PR must itself remain draft, be independently
  reviewed at its exact head per `OPS-0007` §1 (including that standard's disclosure of
  author/reviewer/session/model overlap), receive any required bounded correction and exact-head
  re-review, and receive explicit principal approval before it may be marked ready or merged — and,
  following this repository's standing Lane G post-merge convention (`OPS-0009` §4(a)), post-merge
  verification once it does merge. **This note does not open, draft, or begin that implementation
  PR** — no branch for it exists as of this note, and none is created by this filing.
- §9 (pilot acceptance criteria) and §10 (stopping/rejection conditions) remain the controlling
  standard that future implementation PR must satisfy or must stop against, unedited.
- §11's future-phase exclusions, §2's full non-authority list, and §5's privacy standard (including
  its named, bounded username exception) are unweakened. Restated here only as a cross-reference to
  already-controlling text, not as new authority:
  - **Permitted for the future pilot to test, per §§3-4/§6-7/§9-10 as already written**: (1)
    ingestion of exactly one explicitly selected image; (2) file and source provenance; (3)
    deterministic metadata capture; (4) structured visual observation, kept separate from
    interpretation; (5) separation of observation from inference; (6) uncertainty and
    unreadability disclosure; (7) the advisory record's schema and report formatting; (8) abstention
    when evidence is unclear or cannot be safely captured.
  - **Prohibited for the future pilot, per §2/§11 as already written, none of it loosened by this
    note**: (1) any technical signal; (2) any score or ranking of any security; (3) any transaction
    recommendation; (4) any change to investment policy; (5) any tier or target change; (6) any
    holdings or allocation change; (7) any margin eligibility or parameter change; (8) any coupling
    of chart observations to allocator output; (9) any bulk ingestion or bulk chart analysis; (10)
    any access to, or action through, a brokerage.

**Not authorized by this note:** opening the §8 implementation branch or PR; drafting, committing,
or retaining any chart image, extracted chart fact, or chart-derived observation; any Company/Theme
Intelligence edit; any dashboard change; any `holdings.yaml`/`targets.yaml`/`gates.yaml`/
`issuer_lookthrough.yaml`/`allocate.py`/`margin_state.py`/`levels.py` change; any margin action; any
brokerage action; any second pilot asset. This note performs no repository mutation beyond this
file, `governance/decisions.yaml`'s status field, `operations/WORKSTREAMS.yaml`'s `WS-0011` entry,
and one `CLAUDE.md` Decisions Log pointer entry — the same four-file scope §13 already bounded this
filing to.

**This session did not access, view, inspect, or analyze any chart image or file outside this
repository** — no path under `~/Downloads` or `~/Projects/Chart-Automation` was read. The NVDA
default named in §8 remains a name only, carried over unedited from the original filing; no image
sits behind it in this repository.

**Effectiveness of this note.** Identical discipline to the original filing's own §14: this note,
the frontmatter `status` change above, and every downstream file this session touches take
effect only when this recording pull request is itself independently reviewed under `OPS-0007` §1,
any required bounded correction is made and re-reviewed, and it is merged to `main`. This note does
not mark its own PR ready and does not merge it.

---

## Bounded correction — premature status transition reverted (2026-08-01, same PR)

An independent, exact-head review of this PR (PR #219, review ID `4835983890`, reviewed head
`c7bdc2bbd7ec0fb0671a21955f532fb3bf11e656`) returned **CHANGES REQUIRED**, finding (MATERIAL) that
the note above set frontmatter `status: Accepted` in its own first commit — before any independent
review had occurred and without a separately retained, PR-specific `Principal acceptance:` comment
distinct from both the review verdict and the merge action — contradicting §14's own three-gate
standard (independent review, explicit principal acceptance, merge) restated by this very note's
last paragraph, and inconsistent with `operations/WORKSTREAMS.yaml`'s `WS-0011` entry in the same
diff, which correctly treated acceptance as not yet effective.

**This correction does not edit or retract the note above.** The note's quoted principal
authorization, its description of what §§1-13 mean once accepted, and its description of what §8
would authorize once properly sequenced are accurate and are left exactly as filed — the review
found the prose "otherwise sound." What is corrected: frontmatter `status` (in this file and in
`governance/decisions.yaml`) is reverted from `Accepted` back to `Proposed`, matching this decision's
state as originally filed and merged via PR #218. The note above describes what acceptance *would*
mean; it does not, by itself, make acceptance effective — that requires the distinct, later steps
below, mirroring `PI-0034`'s actual (not merely labeled) commit sequence.

**Corrected effectiveness sequence, restated precisely:** (1) a correction commit,
`0db5bc80cd75ce08bca3b160c2e8a747e07a9bfc`, reverting `status` to `Proposed` and recording this
finding; (2) a separate, distinct PR issue comment on PR #219
(`issuecomment-5153866676`, "Principal acceptance retained for CHART-0001 lifecycle," posted
2026-08-01), quoting the principal's authorization verbatim and naming this PR's then-exact head
`0db5bc80cd75ce08bca3b160c2e8a747e07a9bfc` — never inferred from this note's prose, from authorship,
from timing, or from merge metadata; (3) only after that comment existed, this further, separate,
later commit, setting `status: Accepted` in this file and in `governance/decisions.yaml`,
referencing review `4835983890`, correction commit `0db5bc80cd75ce08bca3b160c2e8a747e07a9bfc`, and
retained comment `issuecomment-5153866676`; (4) independent exact-head re-review of the resulting
delta, still required, not yet performed as of this commit; (5) explicit principal mark-ready and
merge, still required, not yet performed as of this commit. No step in this sequence was skipped or
assumed. **`status: Accepted` above becomes effective, per §14 and this note, only when steps (4)
and (5) are also complete — this commit alone does not mark PR #219 ready or merge it.**
