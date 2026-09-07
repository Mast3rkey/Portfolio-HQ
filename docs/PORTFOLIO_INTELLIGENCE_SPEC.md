# Portfolio Intelligence Specification (Version 2, Frozen)

Status: **canonical, frozen**. This document captures the Version 2
architecture as reviewed and approved across three design-review passes
(architecture proposal, formal review against Portfolio HQ's engineering
principles, and a final index-necessity review). It is a specification
capture only — see §20 and §24 for what freezing this document does and
does not authorize.

## 1. Purpose and scope

The Portfolio Intelligence Engine is a structured, per-company record of
investment reasoning — thesis, risks, catalysts, conviction, review
history — that sits **above** the existing production allocator
(`allocate.py`) without being read by it. Its purpose is to give the
existing mechanical system higher-quality human judgment to sit alongside,
over time, without increasing the allocator's own complexity or altering
its determinism.

Scope, this specification only: the data model, file formats, directory
layout, and non-coupling rules for capturing and reviewing per-company
investment intelligence. It does not scope any specific company's content
— that is future, separate, opt-in work (§16).

A related, separately-governed record type, Theme Intelligence, is
documented in §25. It follows the same non-coupling and advisory-only
rules as Company Intelligence; §25 exists as a trailing addendum rather
than being interleaved throughout §1-§24, to avoid renumbering this
document's existing internal cross-references.

## 2. Non-goals

- Not a trading system, signal generator, or automated research pipeline.
- Not a replacement for `holdings.yaml`, `targets.yaml`, or
  `decision_log.yaml` — each remains sole authority for its own domain.
- Not per-archetype or per-security margin policy — that direction was
  evaluated and rejected in the roadmap reconciliation audit (see
  `docs/RESEARCH_BACKLOG_AND_PRIORITIZATION.md`'s closed item on
  portfolio-level-only margin risk) and stays rejected here (§20).
- Not a dashboard, UI, or reporting product beyond the single generated
  staleness report described in §18.
- Not an authorization to implement anything beyond this document (§20).

## 3. Governing principles

Carried forward from the formal architecture review, unchanged:

1. Elegance over complexity.
2. One responsibility per component.
3. Git-native workflows (conflict-free by construction wherever possible).
4. Human-in-the-loop decision making.
5. Deterministic production allocator, preserved absolutely.
6. Research and production remain clearly separated.
7. Every future integration point must be individually testable and
   reversible.
8. No hidden coupling.

## 4. One-way data flow

```
Capture  →  Track  →  Surface
```

The Intelligence Engine may read `holdings.yaml` and `targets.yaml`
(e.g., to cross-reference a stored tier reference). Production code
(`allocate.py`, `margin_state.py`, and all currently-passing tests) never
reads anything the Intelligence Engine writes. This is enforced by there
being no import of `intelligence/` anywhere in production code — not by
convention, but by the simple fact that no such import exists or is
authorized (§20).

## 5. Directory structure

```
intelligence/
  companies/
    <TICKER>.yaml      # structured profile, risks, catalysts, conviction,
                        # review metadata and history
    <TICKER>.md         # thesis narrative, conviction rationale,
                        # valuation notes — dated prose sections
  themes/
    <THEME_ID>.yaml      # structured theme record — see §25
    <THEME_ID>.md         # theme narrative
  reports/
    staleness_report.md # generated, overwritten in place (§18)
```

No top-level directories beyond `companies/`, `themes/`, and `reports/`.
Earlier drafts (Version 1) proposed separate `risks/`, `catalysts/`, and a
shared `reviews/` log — all three were rejected in review (self-contradicted
"company-first" framing, reintroduced shared-file merge-conflict risk) and
do not appear here.

## 6. Filesystem-as-index decision

**The directory listing is the index. No `intelligence/index.yaml` may be
introduced under this specification.** This is frozen current doctrine,
not a placeholder pending a better idea — it was evaluated explicitly
against an alternative (an explicit index file) across seven criteria —
single source of truth, git merge behavior, discoverability, reporting,
validation, future scalability, implementation complexity — and the
explicit-index alternative lost on every one. Like every other frozen
decision in this repository, it may only be reconsidered through a new,
separately documented architectural decision supported by materially
changed evidence (e.g. a real scaling ceiling actually reached, not a
hypothetical one) — not silently reopened inside a future implementation
pass:

- It would duplicate data already authoritative inside each company file
  (breaks single source of truth).
- It would be a shared file every company addition/removal touches,
  reintroducing the exact merge-conflict class already rejected once for
  the shared review log.
- It solves no real discoverability problem (`ls`/glob already does this
  for free) and no real performance problem (65–500 YAML files parse in
  sub-second time; this repository already does full-roster scans of
  comparable size in `allocate.py`'s `fetch_market()`).
- It creates a new validation obligation — keeping the index consistent
  with the filesystem — that would not otherwise exist.

Any future report or tool that wants a fast rollup should scan
`intelligence/companies/*.yaml` directly, exactly as `reports/
staleness_report.md` is specified to do (§18).

## 7. Per-company file model

Each covered company has **at most two files**, no more:

- one structured YAML file (`intelligence/companies/<TICKER>.yaml`)
- one thesis Markdown file (`intelligence/companies/<TICKER>.md`)

Risks, catalysts, conviction, review cadence, and review history all live
**inside** the company YAML — not in separate topic-keyed files or
directories (§11, §12, §13).

## 8. Authored versus generated content

| Content | Origin | Location |
|---|---|---|
| Business/profile facts, risks, catalysts, conviction rating + rationale, portfolio-role reference, review dates, review log entries, sources | Hand-authored | Company YAML |
| Investment thesis, conviction narrative, valuation notes | Hand-authored | Company Markdown |
| Staleness/review-due flags, catalyst-expiry flags | **Generated** | `reports/staleness_report.md` |

Generated content is never hand-edited. This mirrors the existing
repository convention already used for `logs/allocation-*.md` and
`performance_log.csv`'s computed rows — a generated file is always fully
reproducible from source and carries no information that isn't already
recoverable by re-running the generator.

## 9. Company YAML schema

```yaml
sector: <string>
industry: <string>
portfolio_role_ref: <tier label only — see §14>
themes: [<theme_id>, ...]   # optional; zero or more references to
                             # intelligence/themes/<theme_id>.yaml — see §25.
                             # This is the only direction the reference runs;
                             # a theme file never lists its companies.
competitive_advantages: [<string>, ...]
risks:
  - risk: <string>
    severity: <string>
    identified: <ISO date>
    status: <string>
catalysts:
  - catalyst: <string>
    expected: <ISO date>
    status: <string>
conviction:
  rating: <ordinal scale, e.g. 1-5 or High/Medium/Low>
  rationale: <one-line string, required alongside any rating>
review:
  cadence_days: <int>
  last_reviewed: <ISO date>
  next_due: <ISO date>
  log:
    - date: <ISO date>
      note: <string>
sources:
  - note: <string>
    url: <string, optional>
    date: <ISO date>
```

No field in this schema stores a numeric target weight, tier percentage,
or any value `targets.yaml` already owns (§14).

## 10. Thesis Markdown structure

Freeform prose, dated sections, no fixed schema beyond a convention of
dating each substantive edit (consistent with how `CLAUDE.md`'s own
Decisions Log is dated). Recommended informal structure — not enforced by
any validator — is a business summary, an investment thesis narrative,
and a valuation-concerns section, in that order, each with an update date.
Markdown is used here specifically because forcing thesis narrative into
YAML fields either produces an unstructured wall of text in a single
string value (no structural benefit over Markdown) or artificial
atomization that breaks the argument's flow.

## 11. Risks and catalysts

Both live as list fields inside the company YAML (§9), not as separate
files or directories. A risk or catalyst is not independently meaningful
outside the context of the company it belongs to, so it does not get its
own top-level organizational unit.

## 12. Conviction framework

A minimal ordinal rating (§9's `conviction.rating`) with a required
one-line rationale — not a formula, not a derived score, not something a
script computes. It is exactly as advisory as the thesis narrative and
subject to the same "never manually overridden by generated output" rule
in reverse: nothing *computes* this value, a human always sets it
directly. A computed/derived conviction score is explicitly out of scope
for this specification and is not designed here; if ever pursued, it
would be a separate, future, separately-justified addition (§19), not an
extension silently folded into this one.

## 13. Review cadence and embedded review log

`review.cadence_days`, `review.last_reviewed`, and `review.next_due` are
hand-set fields (last_reviewed/next_due may be updated by a human after a
review; cadence_days is a policy choice). `review.log` is an append-only
list embedded in the same company YAML — not a shared cross-company file.
This keeps two sessions reviewing different tickers from ever touching the
same file, which is the specific failure mode a shared review log (rejected
in Version 1) would have reintroduced.

## 14. Portfolio role reference and single-source-of-truth rules

`portfolio_role_ref` stores **only** the tier/category label (e.g. `T1`,
`T2`, `band`, `spec`) — never the tier's numeric weight or dollar target.
`targets.yaml` remains the sole authority for tier weights and all
allocation policy, full stop. A future validator (§21) may check that a
company's `portfolio_role_ref` still matches the ticker's actual tier in
`targets.yaml` and flag drift — but the check only ever flags, it never
writes back to either file, and `targets.yaml` always wins in case of
disagreement.

## 15. Symbol resolution requirements

Ticker-keyed filenames must resolve symbols through the repository's
**existing** symbol-normalization pattern — the `_YAHOO_SYMBOL`-style
mapping already established in `earnings.py` for exactly this class of
problem (e.g. `BRK.B` brokerage convention vs. `BRK-B` elsewhere). A
second, independent symbol-mapping system must not be created; any future
implementation reuses or extends the existing pattern.

## 16. Opt-in coverage policy

Coverage is opt-in. A company file is created only when there is an
actual thesis worth recording — not mandated for the full ~65-name
roster, and not mandated to track pace with `holdings.yaml`. **Absence of
a company file is not an error, not a gap to fill, and not something any
future validator or report may flag as missing.** The staleness report
(§18) only ever evaluates companies that already have a file.

## 17. Evidence and citation rules

Evidence stays attached to the claim it supports — the `sources` list
lives inside the same company YAML as the risks/catalysts/thesis it
substantiates (§9), not in a separate evidence tree keyed by ticker or
topic. A citation only has meaning next to the claim it backs.

## 18. Staleness-report behavior

`intelligence/reports/staleness_report.md` is **generated** by scanning
`intelligence/companies/*.yaml` for companies whose `review.next_due` has
passed or whose catalysts have passed their `expected` date without a
status update. It is:

- never hand-edited (§8),
- **overwritten in place on each regeneration, not timestamped** — this
  differs deliberately from `logs/allocation-*.md`'s timestamped
  historical-record pattern, because a staleness report has no standing
  historical value once regenerated (it reflects "as of now," not "what
  was recommended on a given day"). This mirrors `performance_log.csv`'s
  overwrite-in-place precedent for its own computed rows, not the `logs/`
  append-forever pattern.

## 19. Future advisory integration points

Ranked loosest-coupled first; none of these are authorized for
implementation by this specification (§20):

1. **Report-adjacent, zero coupling** — the staleness report sits next to
   the allocator's own `--review` output; a human reads both and decides.
   Requires nothing from `allocate.py`.
2. **Suggested target, human-applied** — a conviction rating could
   *suggest* a tier-weight review is warranted, but any actual change is
   still a human hand-editing `targets.yaml`, exactly as today. No new
   `allocate.py` code path.
3. **Watchlist flag, informational only** — the only tier that would ever
   touch `allocate.py`'s output at all: an echoed footnote (e.g. "NVDA
   thesis last reviewed N days ago") appended after `plan()` has already
   decided every trade, using the exact same "computed after plan(),
   provably unable to alter a dollar amount" guarantee `margin_state.py`'s
   risk classifier already demonstrates in production. Any such addition
   requires its own separate research, justification, testing, and
   approval (§20) — it is not pre-approved by this document.

## 20. Explicit prohibitions

This specification is advisory-only and permanently non-coupled to
production behavior. Specifically, and without exception absent a future,
separately-justified, separately-approved change:

- The subsystem is **advisory only**.
- It **cannot modify** `holdings.yaml`, `targets.yaml`, or any allocator
  recommendation.
- **The allocator remains deterministic.**
- **No conviction value automatically changes a tier or weight** — any
  change to a tier or weight remains a manual `targets.yaml` edit.
- **No production code reads `intelligence/` files in the initial
  implementation.**
- **Coverage is opt-in.** Absence of a company file is not an error.
- **The filesystem is the index.** No `intelligence/index.yaml` may be
  introduced under this specification — frozen doctrine, reconsiderable
  only via a new documented architectural decision supported by
  materially changed evidence (§6), not by silent reintroduction during
  a future implementation pass.
- Each covered company has **at most one structured YAML file and one
  thesis Markdown file** — no additional per-company files or
  topic-keyed directories.
- Risks, catalysts, conviction, review cadence, and review history live
  **in the company YAML**, not elsewhere.
- Evidence **stays attached to the claim it supports**.
- **`targets.yaml` remains the sole authority** for tier weights and
  allocation policy.
- **`portfolio_role_ref` stores only the tier/category reference**, never
  its numeric weight.
- **Generated reports are never manually edited.**
- **The staleness report is overwritten in place**, not timestamped.
- **Symbol resolution must reuse** the repository's existing
  symbol-normalization pattern (`earnings.py`'s `_YAHOO_SYMBOL` approach)
  rather than create an independent mapping system.
- **Any future allocator-visible integration must be display-only**
  unless separately researched, justified, tested, and approved — the
  same discipline every existing gate in `allocate.py` was held to.
- **Per-security margin policy is not part of this subsystem** and
  remains a previously rejected direction (see
  `docs/RESEARCH_BACKLOG_AND_PRIORITIZATION.md`'s closed item).
- **This specification does not authorize implementation** beyond the
  document itself — no company files, validators, reports, or
  integrations are created by freezing this document (§24).

## 21. Validation requirements for future implementation

Not built by this document — requirements for whenever implementation is
separately authorized:

- Each company YAML must parse and conform to §9's schema.
- `portfolio_role_ref`, if present, should be checked against
  `targets.yaml`'s actual tier for that ticker and any drift flagged
  (never auto-corrected, never written back).
- Ticker filenames must resolve through the shared symbol-normalization
  pattern (§15) before any file lookup.
- The staleness-report generator must be idempotent and side-effect-free
  on every file except its own output file.
- No validator may treat a missing company file as an error (§16).

## 22. Incremental implementation sequence

Not authorized by this document (§20); recorded here only as the sequence
a future, separately-approved implementation should follow, smallest and
most reversible first:

1. One company file (YAML + Markdown) for a single ticker, by hand, no
   tooling — proves the schema is usable before any automation exists.
2. A schema validator for the company YAML only.
3. The staleness-report generator, read-only, scanning existing files.
4. Only after all of the above are in place and stable: consideration
   (not commitment) of a §19 tier-1 report-adjacent integration.

## 23. Open watch-items that are non-blocking

- `review.log` inside a company YAML grows unbounded over years of
  reviews. Not a defect worth blocking this freeze — trivially
  addressable later (e.g. archiving older entries) if it ever becomes
  material.

## 24. Freeze declaration

Version 2, as captured in this document, is **frozen** as the canonical
Portfolio Intelligence specification. Future work proceeds as incremental
implementation against this fixed specification (§22), not further
redesign, in the same manner this repository already treats a closed
backtest verdict — state it, build against it, don't relitigate without
new evidence.

**Freezing this document is a specification capture only. It is not
authorization to create any company file, validator, report generator, or
integration.** Each of those remains its own separate, future decision,
to be made and recorded on its own terms.

## 25. Theme Intelligence (addendum — PI-0006 / PI-0007 / PI-0009)

Frozen by `decision_log.yaml` PI-0006; implemented per PI-0007
(`ai_infrastructure`, referencing NVDA and GEV) and PI-0009
(`life_sciences_tools_medtech`, referencing ISRG and TMO). This section
faithfully codifies the schema and governing rules PI-0006 froze, without
changing their substance — it makes no new design decision and reopens
none.

A theme is identified by one stable `theme_id`. Each theme has exactly two
files: `intelligence/themes/<THEME_ID>.yaml` (structured) and
`intelligence/themes/<THEME_ID>.md` (narrative). A company references zero
or more themes via its own `themes:` field (§9); **authority runs one way
only, company → theme** — a theme file never stores, lists, or implies its
member companies. Any graph-like presentation of theme/company
relationships is a generated reporting view computed at report time, never
a stored data structure (PI-0006).

Theme YAML schema (PI-0006):

```yaml
theme_id: <string, must match filename>
description: <string>
evidence: [<string>, ...]
risks: [<string>, ...]      # theme-level, distinct in kind from a
                              # company's own risks[] (§9)
catalysts: [<string>, ...]
lifecycle: <one of: Emerging, Established, Mature, Declining, Archived>
review:
  cadence_days: <int>
  last_reviewed: <ISO date>
  next_due: <ISO date>
  log:
    - date: <ISO date>
      note: <string>
```

Themes carry **no conviction rating and no numeric score of any kind** — a
company has conviction (§12), a theme has evidence; PI-0006 treats these as
distinct concepts and declined to conflate them. `lifecycle` describes the
maturity of the shared narrative itself, is never read by anything that
gates a trade, and an Archived theme is not deleted and remains a valid
reference target for any company that once pointed at it (PI-0006).

§4's and §20's non-coupling rules are written in terms of `intelligence/` and
"the Intelligence Engine" generally, not `companies/` specifically, and
already cover Theme Intelligence without amendment now that §5 lists
`intelligence/themes/` as part of that directory. Portfolio Intelligence
aggregation across companies and themes remains fully deferred (PI-0006's
own roadmap statement) and no allocator integration of any kind is
authorized (PI-0007).
