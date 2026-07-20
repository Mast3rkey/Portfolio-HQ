---
decision_id: AUTO-0003
date: 2026-07-20
status: Accepted
category: research_automation
related_decisions: [GOV-0001, AUTO-0001, AUTO-0002, PI-0011]
supporting_artifact: null
---

## Context

`AUTO-0001` accepted the Research Freshness Framework and adopted, as its own
governing rule, `PI-0011`'s strict cadence-overdue test (specification §2:
`review.next_due < as_of_date`, never "reached or passed") — requiring any
future consumer of that rule to either reuse `PI-0011`'s own comparison
directly or demonstrate equivalence against it, since no reusable `PI-0011`
comparison helper exists to reuse directly (confirmed below). `AUTO-0001`
also fixed a cadence-fingerprint field floor (specification §7: `ticker`,
`next_due`, `template_version`). `AUTO-0002` implemented that fingerprint
floor as `freshness_identity.compute_cadence_fingerprint`, implemented the
framework's four-state precedence rule as `freshness_state.
evaluate_freshness_state`, and implemented the registry/checkpoint schema
as `freshness_validator.py` — three pure, local, non-operational modules,
nothing more. `AUTO-0002`'s own Consequences section states plainly that it
"does not discharge `AUTO-0001` specification §2's `PI-0011` overdue-rule
reuse-or-equivalence obligation; that remains open and is owed by whatever
future decision authorizes the monitor/adapters tranche."

That obligation remains open today, confirmed by direct inspection rather
than assumed: `intelligence_report.py`'s `collect_staleness_findings`
performs the strict comparison inline (`elif next_due < as_of_date:`) and
exposes no dedicated, importable comparison helper — there is currently no
`PI-0011`-owned function a future consumer could call directly. Given that,
this tranche selects `AUTO-0001` specification §2's equivalence path: an
independently implemented comparison, demonstrated to agree with
`intelligence_report.py`'s classification at the strict overdue boundary,
via a shared parametrized test fixture (scope defined precisely in §4
below). This is not offered as the only path conceivable in the abstract —
it is the path consistent with this tranche's own explicit prohibition on
modifying `intelligence_report.py` (§1), and, within this tranche's bounded
scope, it is sufficient to discharge the strict overdue-boundary portion of
that obligation.

A second, narrower gap sits directly next to the first: nothing in the
repository yet turns "this ticker's cadence is overdue" into "here is its
deterministic cadence fingerprint, or nothing if the ticker isn't eligible
to trigger at all." `freshness_state.py` consumes fingerprint sets it is
handed; `freshness_identity.py` hashes a fingerprint it is handed `next_due`
for; neither one decides *whether* a given ticker, in its current
enrollment/checkpoint state, as of a given date, actually has a due cadence
fingerprint to hand over in the first place. That decision — small,
local, and fully specified by what `AUTO-0001`/`AUTO-0002` already fixed —
is the gap this decision closes.

Verified directly against the current repository state before drafting
this decision: `AUTO-0003` is unused anywhere in the repository (no
governance file, index row, or code reference cites it); all seven rows in
`intelligence/freshness_registry.yaml` remain `monitoring_enabled: false`;
all seven rows in `intelligence/freshness_checkpoints.yaml` remain
`checkpoint_status: pending` with empty `channels` maps; and `AUTO-0002`'s
own authorized scope is exactly three implementation modules plus their
three test modules — it does not authorize a fourth module of any kind.

## Decision

**This decision authorizes a later, separate implementation PR** to add
exactly two new files, `freshness_cadence.py` and `test_freshness_cadence.
py`, once this governance filing itself is merged to `main`. **The
governance filing itself adds no executable code.** Merging this ADR, its
`governance/decisions.yaml` row, and its `CLAUDE.md` Decisions Log pointer
changes exactly three tracked files:

1. `governance/decisions/AUTO-0003-cadence-trigger-core.md` (this file)
2. `governance/decisions.yaml`
3. `CLAUDE.md`

No executable code, no registry/checkpoint data, and no other documentation
file changes as a result of the governance filing alone. No implementation
PR against this scope may open before this filing is merged, and none of
the functions, modules, or contracts below exist as executable code as a
result of merging this ADR by itself.

### 1. Exact later implementation scope — two files, nothing else

The future implementation PR is authorized to add exactly:

- `freshness_cadence.py`
- `test_freshness_cadence.py`

It is **not** authorized to modify: `intelligence_report.py`,
`test_intelligence_report.py`, `freshness_identity.py`, `freshness_state.py`,
`freshness_validator.py`, any existing test file, any governance or
documentation file (including this ADR, `governance/decisions.yaml`, or
`CLAUDE.md` — those are the governance filing's own scope, already closed
by the time an implementation PR can exist), `requirements.txt`,
`intelligence/freshness_registry.yaml`, `intelligence/
freshness_checkpoints.yaml`, any Company or Theme Intelligence file,
`allocate.py`, `margin_state.py`, `targets.yaml`, `holdings.yaml`, or any
`.github` path. `freshness_cadence.py` is permitted exactly one
cross-module import — the existing public function `freshness_identity.
compute_cadence_fingerprint` — and no other project-internal import.

### 2. Exact public API — one function

`freshness_cadence.py`'s only public surface is:

```
compute_due_cadence_fingerprint(
    *,
    ticker: str,
    monitoring_enabled: bool,
    checkpoint_status: str,
    next_due: date | str,
    as_of_date: date | str,
    template_version: str,
) -> str | None
```

No additional public function or class is authorized. The drafting analysis
behind this decision found no case requiring a second public entry point:
every intermediate step (string normalization, date parsing, the overdue
comparison itself) is an implementation detail of this one decision, never
independently useful outside it, and belongs behind a leading underscore.
Any private helper the implementation PR needs — a string-normalization
helper and a strict local date parser are anticipated, not more — carries
no stability guarantee and is not part of this authorization's public
contract.

### 3. Complete function contract — validation first, gating, overdue, delegation

All behavior below is fixed mechanically; no discretion is left to the
implementation PR beyond ordinary code-review-level implementation choices
(variable names, exact error-message text) that do not change observable
behavior.

**Step order, fixed:**

1. Validate `ticker`: must be `str`; apply Unicode NFC normalization
   (`unicodedata.normalize("NFC", value)`); reject (`ValueError`) if the
   normalized result is empty; reject (`ValueError`) if any character `ch`
   in the normalized result satisfies `ord(ch) < 0x20 or 0x7F <= ord(ch) <=
   0x9F` — the identical C0/C1 control-character rule `AUTO-0002` fixed for
   `freshness_identity.py`'s `ticker`/`episode_id`/`template_version`
   fields. Produces `normalized_ticker`.
2. Validate `template_version` identically to step 1. Produces
   `normalized_template_version`.
3. Validate `monitoring_enabled`: must be exactly `bool`
   (`isinstance(x, bool)`) — a truthy/falsy non-bool (e.g. `1`, `"true"`)
   is rejected, never coerced. `ValueError` otherwise.
4. Validate `checkpoint_status`: must be a `str` (checked before set
   membership, so an unhashable value such as a `list` or `dict` raises
   this function's own documented `ValueError` rather than an uncaught
   `TypeError` from `in`), and must be exactly `"pending"` or `"verified"`.
   `ValueError` otherwise.
5. Validate `next_due`: accepts a `datetime.date` object or a strict
   `YYYY-MM-DD` string; rejects a `datetime.datetime` outright (checked
   before `date`, since `datetime` is itself a `date` subclass — never
   silently truncated to its calendar date); rejects any malformed string
   or any other type. `ValueError` otherwise. Produces canonical
   `next_due_date: date`.
6. Validate `as_of_date` identically to step 5. Produces canonical
   `as_of_date_date: date`.
7. **Cross-field invariant**: if `monitoring_enabled is True` and
   `checkpoint_status == "pending"`, raise `ValueError` — the same invalid
   combination `freshness_validator.py`'s cross-file invariant #3 already
   rejects at the registry/checkpoint-file level, restated here at the
   single-call level so this function can never be asked to reason about a
   contradictory input.
8. **All validation is now complete — no precedence rank, gate, or
   overdue evaluation below is ever reached while validation could still
   fail.** This ordering is the structural guarantee (identical in kind to
   `freshness_state.evaluate_freshness_state`'s own "all validation runs to
   completion before any precedence rank is evaluated") that an invalid
   input can never fall through to a `None` result that looks like a valid
   "not due" answer.
9. **Gate:** if `monitoring_enabled is False` or `checkpoint_status ==
   "pending"`, return `None`. (By step 7's invariant, the only way
   `checkpoint_status == "pending"` reaches this line is with
   `monitoring_enabled is False` already — the two conditions are stated
   together, disjunctively, to mirror `freshness_state.py`'s own rank-3
   gating style, not because both branches are independently reachable.)
10. **Strict overdue rule**, applied only once every gate above has passed
    (i.e. `monitoring_enabled is True` and `checkpoint_status ==
    "verified"`): `next_due_date < as_of_date_date` is overdue;
    `next_due_date == as_of_date_date` is **not** overdue; `next_due_date >
    as_of_date_date` is not overdue. If not overdue, return `None`.
11. **If overdue**, delegate fingerprint production, unchanged, to:
    `freshness_identity.compute_cadence_fingerprint(ticker=normalized_ticker,
    next_due=next_due_date, template_version=normalized_template_version)`.
    Return that function's lowercase 64-character hex digest exactly as
    received — this decision does not authorize a second implementation of
    the canonical-JSON/SHA-256 cadence-hashing algorithm `AUTO-0002` already
    fixed once.

The function is pure and deterministic: every value is supplied by the
caller; no file I/O, no YAML loading, no implicit system-clock access
(`datetime.today`/`date.today`/`time.time` or equivalent), no network
access, no randomness.

### 4. PI-0011 equivalence resolution — the selected path and its governed scope

This decision resolves `AUTO-0001` specification §2's open reuse-or-
equivalence question for the cadence dimension by selecting, for this
bounded tranche, the equivalence path described below — the path consistent
with this tranche's own explicit prohibition on modifying `intelligence_
report.py` (§1), and sufficient to discharge the strict overdue-boundary
portion of that obligation within this tranche's scope:

- `freshness_cadence.py` does not import, modify, or otherwise couple to
  `intelligence_report.py` in any way.
- It implements its own private, strict date comparison (step 10 above),
  independent of `intelligence_report.py`'s inline comparison inside
  `collect_staleness_findings` — the same "independently implemented,
  equivalent semantics" pattern `AUTO-0002` already established for its own
  local ISO-date parser relative to `intelligence_report.py`'s.
- `test_freshness_cadence.py` proves **strict overdue-boundary
  equivalence** — precisely scoped, not full byte-for-byte or
  whole-function equivalence — against the real, imported
  `intelligence_report.collect_staleness_findings`. The governed scope is
  exactly this: **for a schema-valid synthetic company record with a
  valid, parseable `next_due` and an explicit valid `as_of_date`, both
  paths must classify the strict date ordering identically** —
  `next_due < as_of_date` → overdue; `next_due == as_of_date` → not
  overdue; `next_due > as_of_date` → not overdue. This is called **strict
  overdue-boundary equivalence** (equivalently, **cadence
  overdue-classification equivalence**) throughout this decision. The test
  calls the real, unmodified `collect_staleness_findings` — never a copy
  or paraphrase of its logic — using one shared parametrized synthetic
  fixture covering at minimum: `next_due` one day before `as_of_date`;
  `next_due` equal to `as_of_date`; `next_due` one day after `as_of_date`;
  both `date` objects and strict date strings where applicable.
- **This equivalence claim is deliberately narrow and does not extend
  to**: directory scanning; schema validation; missing or malformed
  `review` data; `UnableToEvaluate` reporting; catalysts; report
  construction; or any other `intelligence_report.py` behavior.
  `collect_staleness_findings` scans a directory of files and produces
  reporting findings, including `UnableToEvaluate` outcomes for malformed
  or missing `next_due` values; `compute_due_cadence_fingerprint` is a
  pure function over direct arguments that raises `ValueError` for the
  equivalent malformed-input case. These are not globally equivalent
  functions — only their strict-boundary date classification, under the
  governed valid-input scope stated above, is asserted to agree.
- No change of any kind to `intelligence_report.py` — a `PI-0011`-owned
  module — is authorized by this decision. `test_freshness_cadence.py` is
  permitted to import `intelligence_report.py` solely to exercise its
  real, existing public function for the equivalence assertions;
  `freshness_cadence.py` itself never imports it.

This choice is deliberate, not a default: `AUTO-0001` specification §2
anticipates exactly this fallback — an independently implemented
comparison, rigorously demonstrated to agree with `intelligence_report.py`'s
actual behavior via a shared parametrized test fixture — as one of its two
permitted paths. It is selected here not because it is the only path
conceivable in the abstract, but because it is: the only path consistent
with this tranche's own explicit prohibition on modifying
`intelligence_report.py`; and sufficient, within this tranche's governed
scope, to discharge the strict overdue-boundary obligation.

### 5. Inertness and authority boundary

`freshness_cadence.py` is required to have, and is verified at
implementation-PR review to have, none of the following: filesystem reads
or writes; YAML loading; implicit system-clock access of any kind; network
access; GitHub API access; issue creation or modification; GitHub Actions
or scheduling of any kind; Claude or Anthropic invocation; authentication
or secrets; source adapters; filing-derived fingerprint computation
(`compute_filing_fingerprint` remains unauthorized, exactly as `AUTO-0002`
left it); replacement-authorization validation of any kind; monitor-status
persistence; task-instance or episode-fingerprint lifecycle machinery;
checkpoint bootstrap; registry or checkpoint mutation of any kind;
`monitoring_enabled` changes of any kind; any `PI-0014` activation; any
Company or Theme Intelligence modification; and no allocator, margin, tier,
target, weight, cluster, conviction, trading, or recommendation authority
of any kind. Every value the function reasons about is supplied explicitly
by its caller — it never inspects `intelligence/freshness_registry.yaml`,
`intelligence/freshness_checkpoints.yaml`, or any Company Intelligence file
directly, and this remains true even though every real enrolled ticker
today would in fact gate to `None` if such values were read from the real
files. **Inertness here comes from the total absence of orchestration,
file loading, scheduling, network access, and operational writes — not
from the current, incidental fact that all seven real registry rows happen
to be disabled.** A future orchestration layer that reads the real files
and calls this function is explicitly out of scope for this decision and
would require its own future, separate authorization.

### 6. Test contract

`test_freshness_cadence.py` is authorized to contain comprehensive coverage
of: the three PI-0011 strict overdue-boundary equivalence cases (and their
date-object/date-string variants) — calling the real, unmodified
`intelligence_report.collect_staleness_findings` and comparing **only its
overdue/not-overdue classification** against `compute_due_cadence_
fingerprint`'s classification, for schema-valid synthetic company records
carrying a valid, parseable `next_due` and an explicit valid `as_of_date`
(never a claim of whole-function equivalence — see §4); `monitoring_
enabled: false` gating to `None`; `checkpoint_status: "pending"` gating to
`None`; the `monitoring_enabled: true` + `checkpoint_status: "pending"`
contradiction raising `ValueError`; exact-`bool` rejection for
`monitoring_enabled` (a truthy non-bool must raise, never coerce);
`checkpoint_status`'s closed two-value vocabulary; strict `YYYY-MM-DD`
string acceptance for `next_due`/`as_of_date`; `date`-object acceptance for
both; `datetime` rejection for both (never silently truncated); malformed
or wrong-type date rejection for both (retained separately from the
equivalence cases above — these are `freshness_cadence`'s own direct-input
validation tests, requiring `ValueError`, not a comparison against
`intelligence_report.py`, which handles malformed input as an
`UnableToEvaluate` reporting outcome rather than an exception);
`ticker`/`template_version` NFC normalization and non-empty-after-
normalization rejection; the exact `ord(ch) < 0x20 or 0x7F <= ord(ch) <=
0x9F` control-character boundary for both string fields; deterministic,
repeatable results across repeated calls with identical input; delegation
equivalence — the overdue path's returned digest must equal a direct call
to `freshness_identity.compute_cadence_fingerprint` with the same
normalized `ticker`/`next_due`/`template_version`; the returned digest's
lowercase-64-character-hex shape; and that every invalid-input `ValueError`
case fires even when the same call's `monitoring_enabled`/`checkpoint_
status`/overdue-vs-not-overdue combination would otherwise have produced a
`None` result — proving invalid input can never be masked by a "not due" or
"disabled" outcome.

AST/source-level architectural tests, in the same style `AUTO-0002` already
established for its own three modules, are required to prove: no file I/O
anywhere in `freshness_cadence.py`; no `yaml` import; no top-level
side-effecting statement; no implicit system-clock access
(`datetime.today`/`date.today`/`time.time`/equivalent); no import of
`requests`, `urllib`, `socket`, `http.client`, `subprocess`, or any
GitHub-API- or Claude/Anthropic-related name; no import of, or by,
`allocate.py`/`margin_state.py` in either direction; no import of
`intelligence_report.py` by `freshness_cadence.py` (the reverse — this test
file importing it for equivalence assertions only — is explicitly
permitted, and is the one place in this authorization where that import is
allowed); a check that none of the existing modules (`freshness_identity.
py`, `freshness_state.py`, `freshness_validator.py`, `intelligence_report.
py`) imports `freshness_cadence.py` (a one-way dependency only); and no
operational entry point or `__main__` execution block in `freshness_
cadence.py`. Both this targeted test file and the complete existing
repository test suite must pass, in a correctly provisioned environment,
before the implementation PR may merge — establishing and recording that
this is met is that PR's own responsibility, identical to the standard
`AUTO-0002` already set.

### Prohibited — explicit authority boundary

This decision prohibits — restated for clarity, matching §5 above and
`AUTO-0002`'s own precedent — the implementation having: any network
access; any GitHub API access; any issue creation or modification; any
GitHub Actions workflow or scheduling; any Claude invocation; any
authentication or secrets; any writer of any tracked file; any implicit
system clock; any allocator or margin integration; any runtime activation
of any kind; any source adapters; any checkpoint bootstrap; any monitoring
enablement (`monitoring_enabled` stays `false` for all seven tickers); any
`PI-0014` Path-B implementation of any kind; any filing-derived fingerprint
computation; any replacement-authorization validation or fixture schema of
any kind; any creation of `intelligence/freshness_replacements/`; any
modification of `intelligence_report.py` or any other file listed in §1
above.

## Rationale

This tranche applies the identical discipline `AUTO-0002` already applied
one level down: it closes exactly the one obligation `AUTO-0002` explicitly
left open and named — the `PI-0011` overdue-rule reuse-or-equivalence
requirement — without inventing any specification content that `AUTO-0001`
did not already fix. The cadence-fingerprint field floor (§7) and the
four-state precedence rule (§9) are already implemented and merged
(`freshness_identity.py`, `freshness_state.py`); what remains missing is the
one small, local decision procedure that sits between "a ticker's raw
enrollment/checkpoint/date state" and "a fingerprint (or nothing) ready to
hand to those already-accepted functions." Confirmed directly against the
current repository, not assumed: `intelligence_report.py` still inlines its
overdue comparison rather than exposing a reusable helper, so the
equivalence path is the path this tranche selects — not the only one
conceivable in the abstract, but the only one consistent with this
tranche's own prohibition on modifying `intelligence_report.py`, and
sufficient, within this tranche's scope, to discharge the strict
overdue-boundary obligation.

Choosing the equivalence path over touching `intelligence_report.py`
follows the same ownership discipline `AUTO-0001` itself established for
`PI-0011`'s fields: this decision has no standing to modify a module a
different, already-Accepted decision (`PI-0011`) owns, and inventing a
narrow "just extract one helper" carve-out would itself be new content
requiring `PI-0011`'s own review, not this decision's. Fixing the
implementation to exactly two new files, with exactly one public function
and exactly one permitted cross-module import (`freshness_identity.
compute_cadence_fingerprint`), mirrors `AUTO-0002`'s own "smallest safe next
increment" framing and keeps this tranche strictly smaller than a full
monitor: it decides whether a fingerprint is due; it does not read real
enrollment data, call an adapter, open an issue, or schedule anything.

## Alternatives Considered

- **Name the implementation `freshness_monitor.py`.** Rejected: this
  tranche does not implement the filing monitor, adapters, monitor state,
  operational issues, scheduling, or any orchestration layer — naming it
  "monitor" would misstate its scope as something considerably larger and
  more operational than a single pure gating function.
- **Extract a new overdue-comparison helper from `intelligence_report.py`
  and import it directly.** Rejected: this would satisfy `AUTO-0001` §2's
  direct-reuse path, but modifying a `PI-0011`-owned module is outside this
  decision's standing — `PI-0011` enumerated exactly five things it
  authorized and none of them is "expose a new public comparison helper for
  a different framework's future consumption." The equivalence path is the
  one this decision selects as consistent with its own scope — not the
  only path conceivable, but the only one available without exceeding this
  decision's standing to modify a `PI-0011`-owned module.
- **Import and reuse `collect_staleness_findings` directly in
  production.** Rejected: that function scans an entire companies
  directory and reports on catalysts and schema-invalid records alongside
  overdue reviews — broader reporting concerns this narrow cadence core has
  no need for and no authority to depend on. This core needs exactly one
  explicit, single-ticker overdue decision, not a directory-wide report.
- **Implement registry/checkpoint or Company Intelligence file loading now**,
  so the function could be called against real data directly. Rejected as
  orchestration beyond a pure core — every value must come from the caller,
  exactly as `freshness_state.evaluate_freshness_state` already established
  for the precedence rule this fingerprint eventually feeds.
- **Add filing-derived fingerprint computation in the same tranche.**
  Rejected for the same reason `AUTO-0002` rejected it: specification §6
  states trigger conditions, never a field list, so there is nothing to
  close without inventing new `AUTO-0001` content under a decision number
  that has no standing to do so.
- **Add adapters, checkpoint bootstrap, or replacement-authorization
  validation in the same tranche.** Rejected: each depends on
  specification content `AUTO-0001` never fixed (adapters, replacement
  schema) or on real per-company evidence-gathering work (bootstrap) that
  is content-authoring, not infrastructure, and belongs to its own future,
  separately reviewed tranche.
- **Combine the governance filing and the implementation into a single
  PR.** Rejected for the same reason `AUTO-0002` rejected it: the
  governance filing is inert declarative text; the implementation is real
  executable Python, materially higher review risk, and reviewing it
  against an already-settled, unambiguous contract is cleaner than
  co-mingling authorization with code.
- **Enable monitoring for any real ticker as part of this tranche.**
  Rejected: this tranche authorizes a pure function, not an operational
  capability; flipping any `monitoring_enabled` row remains its own,
  separately reviewed act regardless of what code exists to eventually
  consume it.

## Consequences

This decision, by itself, creates zero code — only its own ADR file, one
new row in `governance/decisions.yaml`, and one short pointer entry in
`CLAUDE.md`'s Decisions Log. It authorizes, but does not itself create, a
later, separate implementation PR containing exactly two files:
`freshness_cadence.py` and `test_freshness_cadence.py`. That implementation
PR is permitted only after this governance filing is merged to `main`, and
must itself establish, in a correctly provisioned environment, that both
its own targeted tests and the complete existing repository test suite
pass, before it may merge.

Merging that future implementation would still create **no operational
monitor**: it would add exactly one pure, local, deterministic function
that a future, separately authorized orchestration layer — the monitor and
adapters tranche `AUTO-0002` already named as the framework's next major,
still-fully-deferred piece — may eventually call. No change to
`freshness_registry.yaml` or `freshness_checkpoints.yaml` content, no
checkpoint bootstrap, no `monitoring_enabled` flip, no adapter, no GitHub
Actions workflow, no GitHub API usage, no Claude invocation, and no
`PI-0014` artifact of any kind results from this decision or from anything
it authorizes — all remain exactly as `AUTO-0001`/`AUTO-0002` left them.
`freshness_identity.py`'s authorized public surface remains exactly
`compute_cadence_fingerprint` and `compute_task_instance_id`; a
`compute_filing_fingerprint` function and any replacement-authorization
validation function would each still require their own future, separate
authorization. This decision does not discharge every remaining
`AUTO-0001` operational layer — filing-derived fingerprints, adapters,
checkpoint bootstrap, durable monitor-status/issue lifecycle, and the
bounded research executor all remain exactly as open as `AUTO-0002` left
them, each owed to its own future, separately authorized tranche.
