---
decision_id: PI-0011
date: 2026-07-19
status: Accepted
category: portfolio_intelligence
related_decisions: [GOV-0001, PI-0001, PI-0002, PI-0003, PI-0006, PI-0007, PI-0010, ONTO-0001]
supporting_artifact: null
---

## Context

A design-only architecture session (this repository, same day) produced a
proposed "Intelligence Operations V1": a reporting/checking layer over
`intelligence/companies/` and `intelligence/themes/` — a staleness report, a
portfolio-role drift check, surfaced theme-reference integrity, and a
filesystem coverage rollup. That session's first draft incorrectly implied
the frozen `docs/PORTFOLIO_INTELLIGENCE_SPEC.md` already authorized building
this. It does not. The specification:

- defines the intended staleness report's behavior (§18);
- records portfolio-role-drift as a requirement for "a future validator"
  (§14, §21);
- permits a report-time theme/company relationship view (§6, §25);
- describes an incremental implementation sequence (§22);

but §§20 and 24 state plainly and repeatedly that freezing the specification
"does not authorize implementation" — no company file, validator, report
generator, or integration is created by the document's own existence. This
is the identical posture `PI-0001` took toward Company Intelligence
(requiring `PI-0002`/`PI-0003` as separate implementation authorizations)
and `PI-0006` took toward Theme Intelligence (requiring `PI-0007`). A
reporting layer built directly from §18/§14/§6 language, without a decision
of its own, would repeat the exact gap `PI-0002` existed to close for the
validator itself.

This decision is that separate, required authorization for Intelligence
Operations V1. A second review pass narrowed and corrected the first draft
in eight respects before this final version: source-read-only terminology
(the module owns exactly one generated artifact, so plain "read-only" is
imprecise); public-validator-API-only reuse (no underscore-prefixed
function of `intelligence_validator.py` is ever imported or called);
explicit advisory-only role-drift semantics that preserve both
`targets.yaml`'s authority and `PI-0003`'s human-authorship boundary;
internal repository-key ticker matching with no symbol-normalization map;
a corrected three-stage scan/render/write architecture (the original
"pure builder" framing was self-contradictory once the builder needed to
read files); precise report-date language; a fully specified CLI
action-group/exit-code contract; and a corrected description of what makes
the initial tracked report reproducible.

## Decision

**Authorizes exactly five things, and nothing else:**

1. A new, independent, **source-read-only** reporting/checking module:
   `intelligence_report.py` (repository root, sibling to
   `intelligence_validator.py`). Source-read-only means: it is unable to
   rewrite any Company or Theme Intelligence record, unable to write
   `holdings.yaml` or `targets.yaml`, and is permitted to overwrite exactly
   one generated artifact — `intelligence/reports/staleness_report.md` —
   and no other file.
2. A dedicated test module: `test_intelligence_report.py`.
3. One generated report: `intelligence/reports/staleness_report.md`.
4. Read-only, stdout-only checks for: portfolio-role drift; existing
   theme-reference integrity (surfaced through `intelligence_validator.py`'s
   public API, not reimplemented); filesystem-derived company/theme
   coverage.
5. The governance-index, Decisions Log, and README discoverability updates
   listed in Consequences.

No other Intelligence operation or integration is authorized by this
decision.

### 1. Staleness scope — company-only, literal to §18

`intelligence_report.py` evaluates **only** `intelligence/companies/*.yaml`.
It does not read, evaluate, or report on any `intelligence/themes/*.yaml`
`review.next_due` value. `docs/PORTFOLIO_INTELLIGENCE_SPEC.md` §18's frozen
text names companies only; `PI-0010` reconciled the specification's
directory/schema sections for Theme Intelligence but deliberately did not
amend §18, and this decision does not either. **Theme Intelligence staleness
remains deferred and would require its own later, separately approved
decision.**

A company review is overdue if and only if:

```
review.next_due < as_of_date
```

A review due exactly on `as_of_date` is not yet overdue (strict inequality).

### 2. Catalyst-expiry semantics — a reporting heuristic, not a schema rule

`catalyst.status` has no closed vocabulary anywhere in the frozen spec or
the validator (unlike `conviction.rating`, closed by `PI-0004`, and
`lifecycle`, closed by `PI-0006`). This decision authorizes exactly one
narrow, explicitly non-binding reporting heuristic: a catalyst is reported
as **lapsed** only when its `expected` date is strictly earlier than
`as_of_date` **and** its `status` is exactly the string `"pending"`. Any
other string status is treated as evidence the catalyst already received
some update and is not classified as lapsed. This heuristic is a
report-generation convenience only; it creates no new schema rule, is never
enforced by `intelligence_validator.py`, and grants no authority to reject
or rewrite any other status value.

Non-string status values, and unparseable or missing
`expected`/`next_due` dates on an otherwise validator-accepted record, are
surfaced as **"unable to evaluate"** — never silently ignored, and never
described as a new schema violation unless `intelligence_validator.py`
independently already reports the record as invalid.

### 3. Invalid records versus unable-to-evaluate records — kept separate

- **Schema-invalid**: `intelligence_validator.py`'s own
  `validate_company_file()` reports errors for the file. `intelligence_report.py`
  skips all date/status computation for that file and lists it, with the
  validator's own error text, under "Schema-invalid company records."
- **Unable to evaluate**: the record is validator-accepted, but a field this
  reporting layer needs for its own narrower purpose (a date or a catalyst
  status) can't be safely interpreted. Listed under "Unable to evaluate,"
  identifying ticker, field, raw value, and reason — without declaring a new
  schema rule.

This decision does not modify `intelligence_validator.py`'s schema, and adds
no check to it.

### 4. Role-drift — advisory only, internal ticker keys, no persistent file

Preserves two frozen requirements at once, not just one: `targets.yaml`
remains authoritative for current allocator tier policy (§14/§20), **and**
`PI-0003`'s rule that `portfolio_role_ref` is a human-authored Intelligence
value whose meaning is not silently rewritten by an allocator configuration
change. A mismatch is therefore:

- an advisory human-review finding;
- not proof that the Intelligence record is invalid;
- not authority to rewrite the Intelligence record;
- not authority to rewrite `targets.yaml`;
- not an automatic promotion or demotion.

> targets.yaml controls current allocator tier policy. The company record
> remains unchanged until a human separately reviews it. A mismatch reports
> that the two sources currently differ; it does not decide which
> historical or research statement should be edited.

For each schema-valid company record, the ticker is derived from the YAML
filename stem and compared against `targets.yaml`'s `tiers.*.tickers`
membership — **an internal repository-key comparison, not an
external-market-data lookup.** Both sides already use the same canonical
brokerage-convention key (including the dotted form, e.g. `BRK.B`), so no
symbol-normalization map is created, and `earnings.py`'s `_YAHOO_SYMBOL`
mapping (built for an external Yahoo Finance lookup, a different problem) is
neither imported nor extended. A ticker whose ownership can't be resolved
this way is reported as `NOT_IN_TARGETS`, never guessed or remapped.

Results are one of exactly four states — `MATCH`, `MISMATCH`,
`NOT_IN_TARGETS`, `AMBIGUOUS_TARGET_MEMBERSHIP` (a ticker present in more
than one `tiers.*` list) — with summary counts reported for all four and
only non-`MATCH` findings listed individually. **Role-drift output is
stdout-only; the persistent staleness report never contains role-drift
results.**

### 5. Theme-reference validation — reused, not reimplemented

`intelligence_report.py` calls only `intelligence_validator.py`'s **public**
functions — `validate_company_file`, `validate_directory`,
`validate_theme_file`, `validate_themes_directory` — never an
underscore-prefixed private function (e.g. `_validate_theme_references`,
`_validate_themes_field`). `validate_company_file` already performs
company→theme reference resolution as part of its own existing, tested
behavior; `validate_theme_file`/`validate_themes_directory` already enforce
the theme schema and reject reverse-membership keys
(`companies`/`members`/`company_count`). This decision authorizes surfacing
those existing public results through a CLI — it does not duplicate,
reinterpret, or independently reimplement them.

### 6. Coverage rollup — filesystem-derived, stdout-only, no index

Computed fresh from the filesystem on every invocation via the public
validator API and plain directory globs. May report: company YAML count;
company Markdown count; theme YAML count; theme Markdown count;
company→theme references derived at runtime; and validation results. Must
not create `intelligence/index.yaml` or any other stored index; cache
relationship edges between runs; store a reverse theme→company list on
disk; compare coverage against the full holdings roster; flag an uncovered
holding as missing research; or imply any count is a target. Stdout-only.

### 7. Module architecture — three separated stages, not two

A corrected architecture, replacing the first draft's self-contradictory
"pure builder" framing:

1. **Read-only scan/collection** (e.g. `collect_staleness_findings(companies_dir, as_of_date)`)
   — may read Company YAML files and call the validator's public API;
   performs no writes.
2. **Pure rendering** (e.g. `render_staleness_report(findings, as_of_date) -> str`)
   — accepts already-collected data; performs no filesystem I/O of any
   kind.
3. **Single fixed-path writer** (e.g. `write_staleness_report(report_text, repo_root) -> Path`)
   — computes exactly `repo_root / "intelligence/reports/staleness_report.md"`;
   accepts no caller-supplied output destination, through the CLI or
   otherwise; opens no other path in write/append/update mode; does not
   create the `intelligence/reports/` directory if it's missing — a missing
   approved directory is a genuine I/O failure, raised clearly rather than
   silently written elsewhere.

Role-drift and coverage functions are pure in the same sense as stage 2:
they read via stage-1-style scans and return data/text for the CLI to
print; neither ever writes a file.

### 8. CLI contract

A required, mutually exclusive action group — `--staleness`, `--role-drift`,
`--coverage`, `--all` — contained entirely inside `intelligence_report.py`,
independent of `allocate.py`'s own CLI. No arguments prints argparse usage
and exits `2`. `--as-of YYYY-MM-DD` affects only the staleness component: it
is valid with `--staleness` or `--all`, and invalid (exit `2`) with
`--role-drift` alone or `--coverage` alone. Exit codes: `0` — the requested
operation completed, regardless of findings; `1` — a genuine I/O or
unexpected execution failure; `2` — invalid command usage or an invalid
date. `--staleness`/`--all` overwrite the one tracked report and echo the
same text to stdout; `--role-drift`/`--coverage` are stdout-only and never
write anything. No arbitrary directory is created at runtime — the
implementation PR creates and tracks `intelligence/reports/` and its report;
a missing or unwritable approved directory during later execution is exit
`1`, not a silent mkdir.

### 9. Generated-report tracking

`intelligence/reports/staleness_report.md` is a **tracked generated
artifact** — committed to git, overwritten in place only when
`intelligence_report.py --staleness`/`--all` is explicitly run, never
regenerated by `allocate.py`, `margin_state.py`, `run_portfolio_check.sh`,
any test, any import, or ordinary `intelligence_validator.py` validation,
and never hand-edited. **The initial implementation PR includes a
deterministically generated report using an explicit as-of date recorded in
the report and PR validation** — `2026-07-19` for this PR. This does not
make the report a source of truth: every value in it is mechanically
re-derivable at any time from `intelligence/companies/*.yaml` alone, exactly
as `docs/PORTFOLIO_INTELLIGENCE_SPEC.md` §8 already requires for generated
content. Company YAML files remain sole authority for `review.next_due` and
catalyst data.

### 10. Report schema

Fixed section order: Header and as-of date; Overdue company reviews; Lapsed
pending catalysts; Unable to evaluate; Schema-invalid company records;
Coverage note. No "unrecognized status vocabulary" section exists. "Unable
to evaluate" identifies ticker, field, raw value, and reason without
declaring a new schema rule. Every findings section has explicit, stated
empty-state text.

### Prohibited — explicit authority boundary

This decision explicitly prohibits, and none of the following is authorized
by it under any interpretation:

- any import of, or read path from, `allocate.py`;
- any import of, or read path from, `margin_state.py`;
- any change to any allocation recommendation, buy/trim/block decision, or
  cash/margin computation;
- any change to `holdings.yaml` or `targets.yaml`;
- any automatic tier promotion or demotion;
- any numeric scoring or ranking of any company or theme;
- any next-dollar or "what to buy" recommendation;
- any classification of a company or theme, and no ontology field,
  integration, or read path of `docs/INVESTMENT_ONTOLOGY.md` of any kind
  (`ONTO-0001` already prohibits this; this decision restates, not
  reopens, that boundary);
- any Theme Intelligence staleness evaluation (item 1);
- any persistent (file-written) role-drift or coverage report — both stay
  stdout-only;
- any new Intelligence index, cache, or duplicate source of truth;
- any rewrite of any `intelligence/companies/*` or `intelligence/themes/*`
  source record;
- any enforcement of a closed `catalyst.status` vocabulary, in
  `intelligence_validator.py` or anywhere else;
- any order placement of any kind;
- any automatic invocation of `intelligence_report.py` from
  `run_portfolio_check.sh`, `allocate.py`, or any other phone/session
  bootstrap path.

## Rationale

Same discipline `PI-0002`/`PI-0003` applied to Company Intelligence and
`PI-0007` applied to Theme Intelligence: a frozen specification describing
intended behavior is not itself authorization to build that behavior. This
decision supplies exactly that missing authorization for Intelligence
Operations V1.

Scoping staleness to companies only (item 1) follows directly from
`PI-0010`'s own choice not to touch §18 when it reconciled every other
Theme-Intelligence-adjacent section of the spec. The catalyst-status
heuristic (item 2) stays deliberately narrow because `PI-0004` and `PI-0006`
each required their own dedicated decision to close a vocabulary — a third
closed vocabulary must not appear as a side effect of a reporting tool.

Reusing `intelligence_validator.py`'s **public** API only (items 3, 5) is a
correction from the first draft, which referenced private
underscore-prefixed functions by name as "reuse." Calling a private function
directly from another module is not the one-responsibility separation the
spec's §3 governing principles require — it is a second, undeclared
coupling to implementation detail that could change without notice. The
public functions (`validate_company_file`, `validate_directory`,
`validate_theme_file`, `validate_themes_directory`) already expose
everything this decision needs; nothing here required touching
`intelligence_validator.py`'s private surface.

The role-drift advisory-only wording (item 4) is not new invention — it is
the direct, explicit preservation of two already-frozen rules operating
together: `targets.yaml`'s authority (§14/§20) and `PI-0003`'s human-
authorship boundary (a Company Intelligence value is fixed at authoring
time and is not silently reinterpreted by a later allocator-side change).
Treating a mismatch as advisory-only, never as invalidating or rewriting
either source, is what makes both rules true simultaneously rather than one
silently overriding the other. The internal-ticker-matching correction (also
item 4) follows because this is a repository-key comparison, not an
external-data lookup — `earnings.py`'s `_YAHOO_SYMBOL` solves a categorically
different problem (bridging to Yahoo Finance's own external convention) and
reusing it here would be solving a problem that does not exist in this
comparison.

The three-stage architecture (item 7) corrects a genuine contradiction in
the first draft: a function that reads company YAML files to produce
findings cannot also be called a "pure builder" with no I/O. Splitting scan
(reads files) from render (pure) from write (the one writer) removes the
contradiction while preserving the original single-writer guarantee.

`related_decisions` is the smallest set that directly establishes this
decision's own authority boundary: `GOV-0001` (the governance-decision-
record layer this file is filed under, and its "freeze generalizes to
implementation, not automatically" reasoning, extended here into a third
domain); `PI-0001` (the Company Intelligence spec freeze and the
"freeze ≠ authorization" precedent this decision follows); `PI-0002` (the
first bounded-implementation-after-a-freeze precedent — same shape this
decision repeats: exactly one narrow experiment, not the broader
subsystem); `PI-0003` (the human-authorship boundary that item 4's
advisory-only role-drift wording directly preserves — load-bearing, not
background); `PI-0006` and `PI-0007` (the Theme Intelligence data model and
its implementation — the direct source of the theme-reference checks this
decision surfaces rather than reimplements); `PI-0010` (the specific
reconciliation decision whose choice not to touch §18 is what makes item
1's scope boundary a real, established one); and `ONTO-0001` (the decision
whose non-integration boundary this decision restates rather than reopens).

## Alternatives Considered

- **Treat the frozen specification as sufficient authorization and skip a
  new decision.** Rejected — the exact error this decision exists to
  correct; §§20/24 foreclose it explicitly.
- **Fold Theme Intelligence staleness into V1's scope now.** Rejected:
  `PI-0010` deliberately left §18 company-only; extending it here would be a
  second, uncoordinated attempt at the same scope question `PI-0010`
  already answered narrowly.
- **Define a closed `catalyst.status` vocabulary as part of this decision.**
  Rejected: one company's worth of `pending`-status evidence is insufficient
  to freeze a vocabulary, the same "3-5 records" anti-overfitting bar
  `PI-0004` set for `risk.severity`/`risk.status`.
- **Reference `intelligence_validator.py`'s private helper functions
  directly**, as the first draft did. Rejected on review: a private,
  underscore-prefixed function carries no API stability guarantee even
  within the same repository; the public functions already provide
  everything needed, so there is no reason to couple to implementation
  detail.
- **Treat a role-drift mismatch as grounds to flag the Intelligence record
  itself as wrong.** Rejected: this would silently invert `PI-0003`'s
  human-authorship rule (a company record's own history and rationale don't
  become wrong merely because `targets.yaml` changed) while also overstating
  what a mechanical string comparison can conclude. Advisory-only, dual-
  preservation wording is the only framing consistent with both frozen
  rules at once.
- **Reuse or extend `earnings.py`'s `_YAHOO_SYMBOL` map for role-drift
  ticker matching.** Rejected: that mechanism exists to bridge to an
  external API's own symbol convention; this check is a same-repository,
  same-convention comparison with no such gap to bridge. Verified directly
  against real data that no current record needs any normalization.
- **Persist role-drift and coverage as generated files** for historical
  comparison over time. Rejected for V1: no stated need exists yet, and it
  would require its own §5 amendment — the same cost `PI-0010` already paid
  once for themes.

## Consequences

`intelligence_report.py` and `test_intelligence_report.py` are created;
`intelligence/reports/staleness_report.md` is created and tracked in git as
a generated artifact, initially produced with `--as-of 2026-07-19`.
`governance/decisions.yaml` gains one new row for this entry. `CLAUDE.md`'s
Decisions Log gains one short pointer entry, consistent with the pattern
`GOV-0001`/`PI-0010`/`ONTO-0001` already set. `README.md` gains a
repo-structure line for the three new paths and a short "Intelligence
Operations" subsection documenting the CLI. No other file changes as a
result of this decision: `intelligence_validator.py`,
`docs/PORTFOLIO_INTELLIGENCE_SPEC.md`, `docs/INVESTMENT_ONTOLOGY.md`,
`constitution/INVESTMENT_CONSTITUTION.md`, `decision_log.yaml`,
`allocate.py`, `margin_state.py`, `run_portfolio_check.sh`,
`holdings.yaml`, `targets.yaml`, and every existing
`intelligence/companies/*`/`intelligence/themes/*` source record are all
unchanged and unmodified by this decision or its implementation. This
decision authorizes nothing beyond the five items stated in Decision above
— Theme Intelligence staleness, persistent role-drift/coverage files,
ontology integration, and any allocator-visible behavior each remain
separately unauthorized and would each require their own future,
separately-approved decision.
