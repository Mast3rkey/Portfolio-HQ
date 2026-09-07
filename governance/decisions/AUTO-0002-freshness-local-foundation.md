---
decision_id: AUTO-0002
date: 2026-07-19
status: Accepted
category: research_automation
related_decisions: [GOV-0001, AUTO-0001]
supporting_artifact: null
---

## Context

`AUTO-0001` accepted a reusable Research Freshness Framework, specified in full in
`docs/FRESHNESS_PLANNER_V1_SPEC.md`. Its own filing authorized only its governance record
and two seed data files, `intelligence/freshness_registry.yaml` and `intelligence/
freshness_checkpoints.yaml` — both fully populated for seven tickers (COST, XOM, NVDA, GEV,
ISRG, TMO, TSM) but entirely inert: every row `monitoring_enabled: false`, every checkpoint
`checkpoint_status: pending` with an empty `channels` map. No validator, evaluator, identity
helper, adapter, workflow, or executor exists for this framework anywhere in the repository,
and `AUTO-0001` explicitly does not authorize any of them.

This decision authorizes the smallest safe next increment: a local-only, deterministic,
non-operational foundation that implements exactly what `AUTO-0001`'s specification already
fixes — its registry/checkpoint schema (§3–§5), its freshness-state precedence rule (§9), and
enough of its fingerprint/task-instance-identity model (§7, §12, §13) to be fully
implementable without inventing content the specification leaves open. Two categories of
specification content are deliberately left unimplemented rather than guessed at: a filing-
derived fingerprint's field set (§6 states trigger *conditions* but never a field list, not
even as a floor) and the replacement-authorization record schema's exact key names and
filename grammar (§14 describes required *content* and a naming *pattern* but never fixes a
YAML key for the named fingerprint set, nor a parseable token grammar for the filename). Both
gaps are real properties of the accepted specification text, not disputes about its meaning,
and closing them here would add new `AUTO-0001` content under this decision's number rather
than implement what already exists.

## Decision

**This decision authorizes a later, separate implementation PR** to add exactly the three
modules and three test modules described below. **The governance filing itself implements no
code** — merging this ADR, the `governance/decisions.yaml` row, and the `CLAUDE.md` pointer
creates zero new Python files. **Implementation of any kind remains prohibited until this
governance filing is merged to `main`** — no implementation PR against this scope may open
beforehand, and none of the modules, functions, or contracts below exist as executable code
as a result of merging this ADR alone.

### 1. Schema and cross-file validation

Authorizes `freshness_validator.py`, validating **only** `intelligence/freshness_registry.
yaml`, `intelligence/freshness_checkpoints.yaml`, and the cross-file invariants between them.
Replacement-authorization validation is explicitly **not** part of this tranche.

**Top-level document schema — both files:**
- The parsed YAML document must be a mapping; any other top-level shape (list, scalar, null)
  is a malformed-type error.
- `schema_version`: required key; value must be the Python integer `1` exactly
  (`isinstance(x, int) and not isinstance(x, bool) and x == 1`) — a string `"1"`, a float
  `1.0`, or any other value is a malformed-value error, never coerced.
- `tickers`: required key; value must be a list; each element of that list must itself be a
  mapping — a non-mapping element is a malformed-type error at the row level.
- A missing `schema_version` or `tickers` key produces a distinct "missing required
  top-level key" error, separate from a present-but-wrong-type/value error — the two are
  never merged into one message class.
- Unexpected top-level keys are **permitted**, not rejected — the same required-key-
  presence-plus-known-key-value-correctness model used at every other level in this
  contract, never a closed/strict-schema model.

**`freshness_registry.yaml` row schema:** required keys, all always present: `ticker`
(non-empty string; case-sensitive exact-match uniqueness, no normalization); `company_
record_authority` (non-empty string; presence/type checked only — no cross-check against
`governance/decisions.yaml` for existence or status, since that is a human-review-time rule,
not one of this file's own validator requirements); `enrollment_authority` (non-empty
string, same presence/type-only treatment); `enrolled_at` (a date — see the ISO-date rule
below); `template_version` (non-empty string — the specification never closes this to an
enumerated set, so only presence and type are checked, not membership in any invented list);
`filing_trigger_profile` (closed: exactly `domestic_issuer_v1` or `foreign_private_
issuer_v1`); `refresh_policy` (non-empty string — also never closed by the specification;
presence/type only); `monitoring_enabled` (must be `bool` exactly, `isinstance(x, bool)` —
a plain `0`/`1` integer is rejected even though it is truthy-equivalent). Unrecognized-but-
present row keys are permitted; missing-key and wrong-type/value errors are always reported
as distinct classes.

**`freshness_checkpoints.yaml` row schema:** required keys are exactly `ticker`, `checkpoint_
status`, `channels`, `established_by` — all four keys must always be present. `ticker`:
non-empty string, must match a `freshness_registry.yaml` row's `ticker` exactly. `checkpoint_
status`: closed, exactly `pending` or `verified`. `channels`: required key; value must be a
mapping (see channel schema below); no rule requires it to be empty specifically because
`checkpoint_status` is `pending`, since neither this file's schema nor the cross-file
invariants below constrain a `pending` row's channel content — they constrain only a
`verified` row's channel completeness. `established_by`: **required key**; its **value**
must be either `null` or a non-empty string — no biconditional is enforced between `established_
by`'s null/non-null state and `channels`'s emptiness or population, since no such rule is
stated anywhere in the specification; the two fields are validated entirely independently.

**Channel object schema:** `channels` is a mapping whose keys are channel names drawn from a
profile-closed set — domestic: `annual_filing`, `quarterly_filing`, `event_filing_watermark`,
`earnings_release`; foreign private issuer (FPI): `annual_20f`, `earnings_6k_watermark`,
`earnings_release`. **Every non-null channel value is itself an object with exactly six
required keys, all always present when the value is non-null** — the parent mapping key
identifying the channel does not make the nested `channel_name` field optional or removable
from the governed data model:

- `channel_name` (required key; non-empty string; **must exactly equal the parent mapping
  key it appears under** — a channel keyed `annual_filing` whose object states `channel_
  name: quarterly_filing` is a validation error, never silently corrected or ignored).
- `official_form_type` (required key; non-empty string; validated for consistency with
  `channel_name`/profile. The specification states no exact literal string values beyond its
  own parenthetical labels, so this decision fixes them as new precision: `annual_filing` →
  `"10-K"`, `quarterly_filing` → `"10-Q"`, `event_filing_watermark` → `"8-K"`, `annual_20f` →
  `"20-F"`, `earnings_6k_watermark` → `"6-K"`, `earnings_release` → `"earnings_release"`, since
  it is a company release under either profile, not an SEC form).
- `stable_source_id` (required key; non-empty string; no format regex invented — a rigid
  accession-number pattern would wrongly reject `earnings_release`'s non-SEC "or equivalent"
  identifier, which the specification explicitly permits).
- `official_source_date` (required key; a date — see the ISO-date rule below).
- `fiscal_period` (**required key**; its **value** may be `null` **or** a string — never
  described as optional or "validated only when present." No format or closed vocabulary is
  invented for the string case, since none is specified.)
- `incorporation_reference` (required key; non-empty string; no format regex invented, same
  treatment as `stable_source_id`).

**Foreign-private-issuer `earnings_release` — exact representation.** The specification's
channel table lists `annual_20f`, `earnings_6k_watermark`, and `earnings_release` together as
the complete `foreign_private_issuer_v1` minimum key-set — `earnings_release` is a member of
that set, not exempt from it. What may be `null` is its *value* specifically, per the same
table's own annotation that it applies "only where a company issues one [a release] separately
from the 6-K itself." The mechanically testable rule:
- A `checkpoint_status: verified` row's `channels` key set **equals exactly** the closed
  channel-name universe for its `filing_trigger_profile` — domestic: all 4 names present;
  FPI: all 3 names present. (This closed universe equals each profile's minimum required set;
  no channel name exists beyond it.)
- For every required channel key **except** FPI's `earnings_release`: the value must be
  non-null and satisfy the complete six-key channel-object schema above.
- For FPI's `earnings_release` specifically: the value may be `null`, **or** a complete
  channel object satisfying the schema above.
- For domestic's `earnings_release`: no nullability is stated for it, so it follows the same
  non-null, complete-object rule as the domestic profile's other three channels.
- A present-but-`null` value for any channel other than FPI's `earnings_release` is invalid.

**All six cross-file invariants**, enforced by `validate_registry_and_checkpoints`:
1. Exactly one checkpoint row per enrolled registry ticker (bijective — no orphan on either
   side).
2. A checkpoint row's `ticker` matches its registry row's `ticker`.
3. `monitoring_enabled: true` together with `checkpoint_status: pending` on the same ticker
   is a hard validation failure.
4. Every populated channel's `official_form_type` is valid for that ticker's `filing_
   trigger_profile`.
5. No duplicate ticker rows in either file; no single filing/source identifier claimed as
   the "latest incorporated" value under two different tickers' channels.
6. A `checkpoint_status: verified` row's populated channel set matches the minimum required
   set for its profile, exactly as restated above, including the FPI `earnings_release`
   nullable-value case.

**ISO-date rule (`enrolled_at`, `official_source_date`):** authorizes a local, private
parser inside `freshness_validator.py` — never an import of `intelligence_report.py` or any
of its private symbols, which this module does not import in either direction. Documented
semantics, proven by parametrized tests: accepts a PyYAML-native `date` object; accepts a
strict `YYYY-MM-DD` string; rejects a `datetime` value outright, never silently truncating
it to a date; rejects any malformed string or any other type. This is an independently
implemented parser with equivalent semantics to `intelligence_report.py`'s own internal
date-parsing behavior — not a reuse of it. `AUTO-0001` specification §2's requirement that a
future monitor either call `intelligence_report.py`'s overdue comparison directly or prove
byte-for-byte equivalence against it applies specifically to the `review.next_due <
as_of_date` comparison, not to generic ISO-date parsing, and is not engaged by this helper.

**Isolation, definitive:** `freshness_validator.py` imports neither `intelligence_validator.
py` nor `intelligence_report.py`. No listed cross-file invariant requires either import.

**Deferred, not authorized — replacement-authorization validation.** `intelligence/
freshness_replacements/` does not exist and this decision does not create it or validate
anything against a future schema for it. The specification never fixes a YAML key name for
the named fingerprint set a replacement-authorization record must carry, and never defines a
fully parseable filename token grammar for `<ticker>-<episode>-<authorization-id>.yaml` (its
example authorization-id — "a digest of the exact named fingerprint set" — is stated as one
option among unstated others, not a fixed rule). Defining either now would add new content to
`AUTO-0001` under this decision's number. This validation belongs with whatever future
tranche implements the reassignment/rejection machinery that actually consumes these
records, once that tranche's own review can resolve these gaps on its own authority.

### 2. Pure freshness-state evaluator

Authorizes `freshness_state.py`, implementing this exact precedence rule over explicit,
already-computed, typed inputs only — no YAML read, no file I/O, no import of `intelligence_
report.py`, no cadence-fingerprint computation of any kind.

**States:** `current`, `unverified`, `review_due`, `pending_human_review`. No fifth state.

**Precedence — evaluated top to bottom, first match wins:**
1. `pending_human_review` if at least one fingerprint is `awaiting_human_incorporation`.
2. else `review_due` if no fingerprint awaits incorporation but at least one fingerprint is
   `outstanding` or `assigned`.
3. else `unverified` if neither of the above applies, and **any** of the following is true:
   `monitoring_enabled` is `false`; `checkpoint_status` is `pending`; no durable monitor-
   status record exists yet for this ticker (the monitor has never run); the durable
   monitor-status record's latest `monitor_state` is `degraded` or `failed`.
4. else `current` — reachable **only** if **all** of the following are true simultaneously:
   `monitoring_enabled` is `true`; `checkpoint_status` is `verified`; a durable monitor-
   status record exists for this ticker; that record's latest `monitor_state` is `healthy`;
   no fingerprint is `outstanding`, `assigned`, or `awaiting_human_incorporation`.

**Input shape:**

```
evaluate_freshness_state(
    *,
    monitoring_enabled: bool,
    checkpoint_status: str,                         # "pending" | "verified"
    monitor_record_exists: bool,
    latest_monitor_state: str | None,                # "healthy" | "degraded" | "failed" | None
    outstanding: collections.abc.Set[str],
    assigned: collections.abc.Set[str],
    awaiting_human_incorporation: collections.abc.Set[str],
    incorporated: collections.abc.Set[str],
) -> str
```

**All validation runs to completion before any precedence rank is evaluated** — this
ordering is the structural guarantee that an invalid input can never fall through to
`current`. `ValueError` is raised, and nothing further evaluated, on any of:
- `monitoring_enabled` is not exactly `bool` (`isinstance(x, bool)`).
- `monitor_record_exists` is not exactly `bool`.
- `checkpoint_status` is not exactly `"pending"` or `"verified"`.
- `monitor_record_exists is False` and `latest_monitor_state is not None` (contradiction).
- `monitor_record_exists is True` and `latest_monitor_state is None` (contradiction — a
  monitor run always records a state).
- `monitor_record_exists is True` and `latest_monitor_state` is not one of `"healthy"`,
  `"degraded"`, `"failed"`.
- Any of the four fingerprint arguments is not an instance of `collections.abc.Set` — a
  `str`, `list`, `dict`, or arbitrary scalar is rejected outright. **Both `set` and
  `frozenset` satisfy `collections.abc.Set` and are both accepted**; each accepted collection
  is internally snapshotted to a `frozenset` immediately after this check, before any further
  use, so a caller mutating a passed-in mutable `set` after the call cannot retroactively
  change an already-computed result.
- Any member of any of the four sets fails the pattern `^[0-9a-f]{64}$` (case-sensitive,
  lowercase hex only — the exact shape `freshness_identity.py` produces).
- The same fingerprint digest string is present in more than one of the four sets (a
  fingerprint occupies exactly one state at a time; membership in two sets simultaneously is
  a contradiction, not a valid input).

All four sets being empty simultaneously is explicitly **valid**, not an error — it
represents a ticker with no fingerprints in any active state, and correctly falls through
ranks 1–2 to whichever of rank 3 or rank 4 the remaining inputs determine.

This tranche does not discharge, and does not attempt to discharge, `AUTO-0001`
specification §2's requirement that a future monitor either call `intelligence_report.py`'s
overdue comparison directly or prove byte-for-byte semantic equivalence against it — that
obligation remains fully open, owed entirely by whichever future decision authorizes the
monitor/adapters tranche.

### 3. Deterministic fingerprint and task-instance identity helpers

Authorizes `freshness_identity.py` with **exactly two** public functions:

```
compute_cadence_fingerprint(
    *,
    ticker: str,
    next_due: date | str,
    template_version: str,
) -> str

compute_task_instance_id(
    *,
    ticker: str,
    episode_id: str,
    fingerprint_assignments: collections.abc.Sequence,
    template_version: str,
) -> str
```

`compute_cadence_fingerprint` closes specification §7's stated floor exactly, adding nothing
beyond `ticker`, `next_due`, and `template_version` — the three fields the specification
names as the required minimum for this fingerprint type. `compute_task_instance_id`
implements specification §13's field list, which the specification states as an exact,
unhedged enumeration (unlike §7's "at least" floor). A third function, computing a filing-
derived fingerprint, is explicitly **not authorized** by this decision: specification §6
states trigger *conditions* for filing-derived fingerprints but never states any field list
for them, not even as a floor, so there is nothing to close without inventing new content.

**Canonicalization and hashing contract — complete, stated here:**

1. **Domain separation.** A fixed literal `fingerprint_type` tag is always the first
   canonical field: `"cadence_v1"` for the cadence fingerprint, `"task_instance_v1"` for the
   task-instance ID (a future `"filing_v1"` is reserved, not implemented). This tag
   guarantees the two types' canonical JSON payloads can never be byte-identical, since they
   differ at the first serialized field regardless of every other value — it prevents
   **cross-domain payload ambiguity** only. Whether two genuinely different canonical
   payloads could ever hash to the same SHA-256 digest is a question of SHA-256's own
   collision resistance, a property of the hash function, not a guarantee this contract adds
   independently.
2. **Field order — fixed, never alphabetized:** cadence fingerprint: `fingerprint_type`,
   `ticker`, `next_due`, `template_version`. Task-instance ID: `fingerprint_type`, `ticker`,
   `episode_id`, `fingerprint_assignments` (the sorted, validated pairs — see step 5 below),
   `template_version`.
3. **String-field normalization (`ticker`, `episode_id`, `template_version` only):**
   - Require the value to be a `str`.
   - Apply Unicode NFC normalization: `unicodedata.normalize("NFC", value)`.
   - Reject (`ValueError`) if the normalized result is empty.
   - Reject (`ValueError`) if any character `ch` in the normalized result satisfies
     `ord(ch) < 0x20 or 0x7F <= ord(ch) <= 0x9F` (the C0 control range below space, and the
     C1 control range from DEL through the C1 block).
4. **Date normalization (`next_due` only):** via the same local ISO-date rule as §1 above —
   a `date` object or a strict `YYYY-MM-DD` string is accepted and canonicalized to
   `YYYY-MM-DD`; a `datetime` value is rejected outright, never truncated; any other type or
   malformed string is rejected.
5. **`compute_task_instance_id` container and pair validation — exact order:**
   1. If `fingerprint_assignments` is an instance of `str`, `bytes`, or `bytearray`, raise
      `ValueError` — these satisfy `collections.abc.Sequence` but are explicitly rejected as
      the outer container.
   2. If `fingerprint_assignments` is not an instance of `collections.abc.Sequence`, raise
      `ValueError` — this rejects `set`, `frozenset`, any mapping, any generator, any other
      arbitrary iterable, and any scalar.
   3. Snapshot the accepted sequence to a tuple **exactly once**: `snapshot =
      tuple(fingerprint_assignments)`.
   4. If `len(snapshot) == 0`, raise `ValueError` — a task instance always covers at least
      one fingerprint.
   5. For each `item` in `snapshot`, in order: if `item` is an instance of `str`, `bytes`, or
      `bytearray`, raise `ValueError` (invalid pair object, even though these satisfy
      `Sequence`); else if `item` is not an instance of `collections.abc.Sequence`, raise
      `ValueError`; else if `len(item) != 2`, raise `ValueError`. Otherwise interpret
      `item[0]` as the fingerprint and `item[1]` as the assignment ordinal.
   6. For the fingerprint element: if it is not a `str` matching `^[0-9a-f]{64}$` exactly
      (lowercase ASCII hex, no Unicode normalization applied — a fingerprint digest is
      already constrained to `[0-9a-f]`), raise `ValueError` (malformed digest).
   7. For the ordinal element: if it is a `bool`, raise `ValueError` (bool ordinals
      explicitly rejected, since `isinstance(True, int)` is `True` in Python and would
      otherwise silently alias to ordinal `1`); else if it is not an `int`, raise
      `ValueError`; else if it is `< 1`, raise `ValueError`.
   8. Every item in `snapshot` must pass steps 5–7 completely, producing a fully validated,
      canonicalized list of `(fingerprint: str, ordinal: int)` tuples, **before** any
      duplicate or conflict detection begins.
   9. Detect duplicate pairs: if the same exact `(fingerprint, ordinal)` tuple appears more
      than once in the validated list, raise `ValueError`.
   10. Detect conflicting ordinals: if the same `fingerprint` string appears with two
       different `ordinal` values anywhere in the validated list, raise `ValueError`.
   11. Sort the validated, canonicalized tuples ascending by `(fingerprint, ordinal)` —
       ordinary string then integer comparison. Only validated values are ever sorted; a
       malformed entry is always rejected before sorting is attempted.
6. **Serialization.** Build the fixed-order field list from step 2 as a JSON array of
   `[field_name, canonical_value]` pairs — never a JSON object, which would not by itself
   guarantee key order. `fingerprint_assignments`'s canonical value is a JSON array of
   `[fingerprint, ordinal]` pairs in the sorted order from step 5.11. Serialize with
   `json.dumps(pairs, ensure_ascii=True, separators=(",", ":"))`.
7. **Hashing.** UTF-8-encode the resulting JSON text; compute `hashlib.sha256(<bytes>).
   hexdigest()`; the lowercase 64-character hex digest is the fingerprint or task-instance
   ID.

Both functions are pure: no file I/O, no network access, no implicit read of the system
clock, no randomness — every value is supplied by the caller. All invalid input raises
`ValueError`, consistently with the fail-closed contract used throughout this decision.

### 4. Tests and architectural enforcement

Authorizes `test_freshness_validator.py`, `test_freshness_state.py`, `test_freshness_
identity.py` — no replacement-authorization fixture tests. Following this repository's
existing pytest conventions: plain `def test_*()` functions, `tmp_path`-based fixtures,
fictional/synthetic tickers only, and `@pytest.mark.parametrize` over every closed
vocabulary and boundary condition in this Decision, explicitly including: the local
ISO-date parser's four documented behaviors; the `established_by`/`fiscal_period` required-
key-nullable-value contract; the FPI `earnings_release` null-vs-complete-object case; the
exact `ord(ch) < 0x20 or 0x7F <= ord(ch) <= 0x9F` control-character boundary for `ticker`/
`episode_id`/`template_version`; every rejection case listed in §3's container/pair
validation algorithm (non-`Sequence` outer container, `str`/`bytes`/`bytearray` as outer
container, empty outer container, non-`Sequence` pair, `str`/`bytes`/`bytearray` as a pair,
wrong pair length, malformed digest, bool ordinal, non-int ordinal, ordinal `< 1`, duplicate
pair, conflicting ordinal); and every rejection case in the state evaluator's contract
(non-`bool` typing, contradictory monitor-record/state combinations, non-`Set` fingerprint
arguments, malformed digest members, cross-set duplicate fingerprints). AST-based
architectural-invariant tests must prove: zero writes to disk anywhere in any of the three
modules; zero top-level side-effecting statements; zero import of `requests`, `urllib`,
`socket`, `http.client`, `subprocess`, or any GitHub-API-related name; and zero import of, or
by, `allocate.py`/`margin_state.py` in either direction. The three targeted test files and
the complete existing repository test suite must both pass, in a correctly provisioned
environment, before the implementation PR may merge — establishing and recording that this
is met is that PR's own responsibility.

### Prohibited — explicit authority boundary

The implementation authorized by this decision must have, and must be verified at
implementation-PR review to have: no network access; no GitHub API access; no issue creation
or modification; no GitHub Actions workflow; no Claude invocation; no authentication or
secrets; no writer of any tracked file; no implicit system clock; no allocator or margin
integration; no runtime activation of any kind; no source adapters; no checkpoint bootstrap;
no monitoring enablement (`monitoring_enabled` stays `false` for all seven tickers); no
`PI-0014` Path-B implementation of any kind; no filing-derived fingerprint computation; no
replacement-authorization validation or fixture schema of any kind; no creation of
`intelligence/freshness_replacements/`. The three modules must remain isolated from
`allocate.py`, `margin_state.py`, `targets.yaml`, `holdings.yaml`, and every tier, weight,
cap, role, conviction, trading, and allocation concept those files carry — none of it is
read, written, computed, or implied by anything authorized here.

## Rationale

This tranche applies the same single-owner, no-duplication discipline `AUTO-0001` already
established for `PI-0011`'s fields, one level down: it implements exactly the rules the
accepted specification fixes, reproducing rather than reinterpreting them, and explicitly
declines to discharge the one obligation (the `PI-0011` overdue-rule reuse-or-equivalence
requirement) that belongs to a different, later tranche — doing so here would risk a second,
independently-drifting implementation of that comparison appearing before the monitor that
actually needs it exists. Choosing a purely local, deterministic, non-operational first
increment mirrors this repository's own precedent for exactly this situation: an earlier
Portfolio Intelligence decision authorized a schema validator in complete isolation, before
any real content or higher-risk capability existed under that governance line — proving a
foundation correct on its own terms before building anything on top of it. Fixing a precise
canonical-JSON/SHA-256 hashing contract now, rather than leaving it to be invented ad hoc by
a future implementation PR, closes a real risk: two independently-written implementations of
the same rule could otherwise produce different fingerprint or task-instance IDs from
identical logical inputs, silently breaking the framework's own identity model before it is
ever operational. Declining to implement filing-derived fingerprints or replacement-
authorization validation is not a loss of scope but a correction of it: both would require
inventing specification content that does not yet exist, which this decision has no standing
to do under its own number — each belongs with the future tranche whose own review can
resolve those gaps (the adapters that would supply a filing fingerprint's inputs; the
reassignment/rejection machinery that would consume a replacement-authorization record).

## Alternatives Considered

- **Authorize the full monitor/adapter/executor stack in one filing.** Rejected: `AUTO-0001`
  specification §21 requires each later capability to pass its own separate review before
  merge; a single filing pre-clearing that entire sequence would functionally violate that
  requirement regardless of how the resulting PRs were split, and would depart from this
  repository's own convention of authorizing each bounded increment through its own numbered
  decision, filed only when that increment is ready.
- **Combine the governance filing and the implementation into a single PR.** Rejected:
  `AUTO-0001`'s own two seed data files are inert declarative YAML carrying zero operational
  risk by construction, reasonably bundled with their own authorizing filing; this decision
  authorizes real executable Python, materially higher risk. Separating the authorization
  text from the code it authorizes lets the code be reviewed against an already-settled,
  unambiguous contract rather than co-mingled with it.
- **Write a new supporting specification document rather than a self-contained ADR.**
  Rejected: this tranche's job is to reproduce rules the specification already froze, not to
  invent comparable new mechanism; the one genuinely new element — the hashing/
  canonicalization contract — is short and precise enough to state completely inside this
  ADR's Decision section, and a separate artifact would be ceremony without a corresponding
  increase in precision.
- **Include `PI-0011` in `related_decisions`, since `AUTO-0001` itself cites it.** Rejected:
  this tranche never imports `intelligence_report.py`, never implements or reuses the
  overdue rule, and explicitly does not discharge `AUTO-0001`'s own future obligation to
  reconcile with it — citing `PI-0011` here would claim a functional relationship that does
  not exist at this tranche's scope.
- **Include `PI-0014` in `related_decisions`.** Rejected for the same reason, more clearly —
  this tranche has no relationship to the Path-B pilot; the seven-ticker roster appears only
  as already-committed fixture/test data, never acted on.
- **Invent a filing-derived fingerprint field list so all three identity functions could ship
  in one tranche.** Rejected: unlike the cadence fingerprint, specification §6 never states
  any field list for a filing-derived fingerprint, not even as a floor — there is nothing to
  close without adding new specification content under this decision's number. Deferring it
  to the tranche that also defines the official-source adapters — the actual data source such
  a fingerprint would hash — is the smaller, more honest scope.
- **Keep replacement-authorization validation in this tranche, accepting an invented filename
  grammar and body-field key name as reasonable defaults.** Rejected: an invented default
  filed inside a validator PR is still new specification content authorized under a decision
  number that has no standing to extend `AUTO-0001` — the same objection that disqualifies
  inventing filing-fingerprint fields applies identically here.
- **Treat the foreign-private-issuer `earnings_release` channel as exempt from the minimum
  required set, since its value may be `null`.** Rejected on direct re-reading of the
  specification's channel table: `earnings_release` is listed as a member of the three-item
  `foreign_private_issuer_v1` minimum set, with only its value — not its presence as a key —
  annotated nullable. Treating it as exempt would make a verified FPI checkpoint's required
  key-set looser than the specification actually states.

## Consequences

This decision, by itself, creates zero code — only its own ADR file, one new row in
`governance/decisions.yaml`, and one short pointer entry in `CLAUDE.md`'s Decisions Log. It
authorizes, but does not itself create, a later, separate implementation PR containing
exactly six files: `freshness_validator.py`, `freshness_state.py`, `freshness_identity.py`,
`test_freshness_validator.py`, `test_freshness_state.py`, `test_freshness_identity.py` — no
`README.md`, no governance-file changes bundled into that PR, no replacement-authorization
record or validator, and no other path. That implementation PR is permitted only after this
governance filing is merged to `main`, and must itself establish, in a correctly provisioned
environment, that both its own targeted tests and the complete existing repository test suite
pass, before it may merge. No change to `freshness_registry.yaml` or `freshness_checkpoints.
yaml` content, no checkpoint bootstrap, no `monitoring_enabled` flip, no adapter, no GitHub
Actions workflow, no GitHub API usage, no Claude invocation, and no `PI-0014` artifact of any
kind results from this decision or from anything it authorizes — all remain exactly as
`AUTO-0001` left them. `freshness_identity.py`'s authorized public surface remains exactly
`compute_cadence_fingerprint` and `compute_task_instance_id`; a `compute_filing_fingerprint`
function and any replacement-authorization validation function each require their own
future, separate authorization, once the specification content they would depend on is
itself fixed by a decision with standing to fix it. This decision does not discharge
`AUTO-0001` specification §2's `PI-0011` overdue-rule reuse-or-equivalence obligation; that
remains open and is owed by whatever future decision authorizes the monitor/adapters
tranche.
