---
decision_id: OPS-0007
date: 2026-07-26
status: Accepted
category: operations_coordination
related_decisions: [OPS-0001, OPS-0002, OPS-0003, OPS-0004, OPS-0005, OPS-0006, GOV-0001, GOV-0002, GOV-0003, PI-0011, PI-0013, PI-0016, PI-0023, PI-0024, PI-0025, NUM-0001]
supporting_artifact: null
---

## Context

Every independent-review gate this repository has used since `OPS-0004` established the
retained-artifact convention — `PI-0023` §I, `PI-0024` §I, `PI-0025` §I, and `OPS-0006` §4's
Milestone 9 — names the reviewer as "Fable" specifically. That naming was never itself a
deliberate doctrine choice about *why* Fable and not another sufficiently capable independent
model; it was simply the reviewer available at the time each of those decisions was filed. The
principal directs that this repository's research and allocation-readiness work must not depend
on one specific model's usage availability as a single point of failure — if Fable access is
unavailable when a review is due, the correct response is a capability-based reviewer standard
any sufficiently capable independent model can satisfy, not a stall.

At the same time, `OPS-0006` §2/§3's zero-based-research discipline and every accepted `PI-####`
batch authorization (`PI-0023`, `PI-0024`, `PI-0025`) require independent review, exact-head
anchoring, retained attribution, bounded correction on material findings, and explicit principal
acceptance before any research output is treated as final. None of that is being waived here. The
principal is explicit: "Independent review remains mandatory. I am not waiving factual
verification, exact-head review, retained attribution, principal acceptance, or later deeper
review." This decision exists to decouple the reviewer's identity (which model) from the
substance of the review gate (what the review must do) — nothing more.

Separately, WS-0005's roadmap (`OPS-0006` §4) currently authorizes only Milestones 1-2 to execute;
Milestone 3 (Intelligence completion) proceeds batch-by-batch under its own `PI-####`
authorizations (`PI-0023` merged and complete, `PI-0024` merged, `PI-0025` filed and gating PR
#161); Milestones 4 through 9 (relationship mapping, zero-based classification, blind
classification, baseline reconciliation, the policy recommendation package, and final adoption)
remain entirely unauthorized roadmap items. The principal separately directs that currently
available, independently reviewed Intelligence should be usable now, under an explicit provisional
label, to support preliminary — not final — organizational and scenario work: a preliminary
portfolio-role/tier organization, preliminary target-range scenarios, and a scenario-only,
cash-only, zero-margin allocation comparison. This is not a claim that Milestone 3 is complete
roster-wide or that Milestones 4 through 9 have been performed. It is a new, separate, explicitly
bounded authorization — filed under this decision, naming its own scope precisely, exactly as
`OPS-0006` §5 itself contemplates for any post-Milestone-2 work ("each requires its own separate,
later, explicit principal authorization").

### Preflight (independently verified this session, not assumed)

- **Repository identity** confirmed `Mast3rkey/Portfolio-HQ` (remote origin path).
- **`origin/main` fetched and pruned** successfully; local `main` matches `origin/main` exactly.
- **Authoritative `main` includes PR #160** at its merge commit
  `b20922bc51e1040081505f236065cb4fe5b23a33` — confirmed both by `git log` and
  `git merge-base --is-ancestor`.
- **`PI-0025`** confirmed `status: Accepted` and effective in both
  `governance/decisions/PI-0025-ws0005-milestone3-batch3-compute-networking.md` and
  `governance/decisions.yaml`.
- **PR #161** confirmed open, `draft: true`, `merged: false`, head exactly
  `e37392b075e26d55f2996bcd86487c93b453623a`, base `main` at `b20922bc...` (PI-0025's own merge
  commit) — matching PI-0025 §I's own gating requirement. Untouched by this filing.
- **CI run `30187314320`** (the `test` check run at PR #161's exact head) independently confirmed
  `status: completed`, `conclusion: success`.
- **No review satisfying PI-0025 §I's final merge gate has been retained** — PR #161 carries no
  GitHub review and no retained artifact under `governance/audits/` anchored to its head; its
  independent-review, correction, and principal-acceptance gates remain open.
- **Working tree confirmed clean** at this filing's base commit.
- **No conflicting open governance PR exists** — `PR #161` is the only open PR in the repository,
  and it is `PI-0025`'s own gated research-implementation PR, not a competing governance filing.
- **`OPS-0007` confirmed the next unused decision number** — checked live against both
  `governance/decisions/` (highest filed: `PI-0025`; highest `OPS-####`: `OPS-0006`) and
  `governance/decisions.yaml` (same), not assumed.
- **`allocate.py` independently inspected**: `plan(targets, holdings, roster, metrics, regime_ok,
  regime_known, cash, ...)` (line 236) and `build_roster(targets)` (line 88) both take a `targets`
  dict as an explicit parameter rather than reading `targets.yaml` from inside the function body —
  confirming that a scenario configuration can be loaded as a separate in-memory dict (via the
  same `load_yaml()` helper, line 83, pointed at a different file) and passed through the existing
  pure allocation functions without modifying `allocate.py` or `targets.yaml` — the basis for §5
  below.

## Decision

**OPS-0007 authorizes two things, both governance-only: (1) a capability-based independent-review
standard that replaces a reviewer requirement based solely on a named model, for WS-0005 work from
this decision forward; and (2) a bounded, safeguarded, explicitly provisional bridge permitting
currently available, independently reviewed Intelligence to support preliminary organizational and
scenario-only allocation work before Milestones 3-9 and any later, deeper review are complete.**
This filing itself creates no Company Intelligence record, no comparison artifact, no target
scenario, no allocation check, and touches no file beyond the governance package named in §9. It
does not review, modify, mark ready, or merge PR #161. It does not begin Milestone 3, 4, or any
later WS-0005 milestone's substantive execution.

### 1. Capability-based independent review

Effective on this decision's merge, every WS-0005 independent-review gate that previously named
"Fable" specifically (`OPS-0006` §4 Milestone 9; `PI-0023` §E; `PI-0024` §I; `PI-0025` §I; and any
future WS-0005 filing that would otherwise repeat that naming) is satisfied by **any eligible
independent reviewer**, defined by capability, not by brand. An eligible independent reviewer must:

1. Be a session and model that did not author or edit the reviewed work.
2. Review the exact commit head that will be relied upon (for a merge decision, the exact head
   that ultimately merges — an intermediate-commit review does not by itself satisfy a merge gate,
   unchanged from existing practice).
3. Have repository access sufficient to inspect the complete diff and the controlling authority
   (Constitution, governing decisions, `CLAUDE.md`, and any other document the reviewed work
   depends on).
4. Have web/research capability sufficient to verify external factual claims made in the reviewed
   work.
5. Attempt direct primary-source inspection for load-bearing claims, disclosing when a source is
   blocked rather than silently substituting a secondary source.
6. Distinguish primary, secondary, search-snippet, estimate, inference, and unresolved evidence
   throughout its findings — never presenting one as another.
7. Run, or independently verify the results of, all validators and tests the reviewed work's own
   authorization requires.
8. Classify findings by severity (e.g. Blocking / Major / Minor / Advisory, or an equivalent
   ordinal scheme it discloses) rather than presenting an undifferentiated list.
9. Retain an attributable review: either a GitHub review/comment thread, or a verbatim audit
   artifact filed under `governance/audits/` per that directory's existing convention — matching
   `OPS-0004`'s retained-artifact standard exactly. A claim of review that exists only as prose
   authored by the same identity as the reviewed work — the exact gap `OPS-0004`'s Finding FA-1
   identified and closed — does not satisfy this requirement.
10. Disclose, in the retained review itself: the reviewing model and session identifier, any
    evidence-access limitation encountered, the exact commit head reviewed, and an explicit
    verdict.
11. Require a bounded correction and an exact-head re-review for any material (Blocking or Major)
    finding before the work may be considered ready — the same single-bounded-correction-pass
    mechanism `PI-0024` §I already established, generalized here to any eligible reviewer.
12. Require explicit principal acceptance, at the exact head being merged or adopted, before
    merge or adoption — never inferred from silence or from an earlier round's acceptance of a
    different head.

**Fable remains eligible** — nothing in this standard excludes it, and every existing retained
Fable review on this repository's merged history remains valid exactly as recorded; this decision
changes no past review's status. **A capable independent ChatGPT session may satisfy this standard
when it meets every one of the twelve requirements above** — the same as any other sufficiently
capable independent reviewer. **A Sonnet session may not independently approve work that the same
Sonnet session authored** — requirement 1 (no self-review) applies regardless of which model
performs the review, and is restated here because it is the one requirement most likely to be
overlooked when a single conversational session both implements and would otherwise be asked to
"check its own work." No specific model name is elevated to a permanent requirement by this
decision — the standard is capability, disclosed and verifiable, not brand.

### 2. Effect on PI-0025 and PR #161

**OPS-0007 prospectively supersedes only `PI-0025` §I's model-name-specific requirement** — the
clause requiring "an independent Fable review... anchored to the exact implementation PR head."
Following this repository's own narrow-supersession convention (`OPS-0003` narrowing `OPS-0002`
items 2-3 only; `OPS-0005` narrowing `OPS-0003` item 1 and `OPS-0004` item 6 only — in neither
case was the superseded decision's `status` changed from `Accepted`), `PI-0025` remains `status:
Accepted` and its `.md` file is not edited: every other requirement in `PI-0025` §I — independent
review, exact-head anchoring, retained attribution, a bounded correction pass for material
findings, explicit principal acceptance before merge, and post-merge ancestry/scope/validator/test
re-verification with factual `operations/WORKSTREAMS.yaml` synchronization — remains unchanged and
fully in force. Only the word "Fable" in that one clause is read, from this decision's merge
forward, as "an eligible independent reviewer per `OPS-0007` §1."

**PR #161 may therefore be reviewed by an independent ChatGPT session (or any other eligible
reviewer under §1) after this decision merges**, satisfying `PI-0025` §I's review gate exactly as a
Fable review would have. **This decision does not itself declare PR #161 reviewed, approved,
corrected, ready, or mergeable** — those outcomes require the actual review, any resulting bounded
correction, exact-head re-review, and principal acceptance described in §8 below, none of which
this filing performs.

### 3. Provisional Intelligence status

A new advisory category, **PROVISIONAL**, is defined for Company or Theme Intelligence content
that has cleared an eligible independent review under §1 but has not yet been subjected to
WS-0005's later, deeper, portfolio-wide review (Milestones 4-9, and any future dedicated Fable
review of the completed workstream per `OPS-0006` §4 Milestone 9).

Provisional Intelligence:

- **May** inform preliminary research organization, candidate economic roles, classifications,
  tiers, target ranges, and scenario analysis, exactly as authorized in §4 and §5 below.
- **Must** display its provisional status and evidence cutoff wherever it is used outside its own
  Company/Theme Intelligence record (e.g., in any preliminary-architecture or scenario artifact
  produced under §4/§5).
- **Must** preserve unresolved claims, evidence-access limitations, and confidence limitations
  exactly as the underlying record discloses them — never silently smoothing over a labeled
  uncertainty when the content is reused downstream.
- **May not** silently be called final, verified, fully complete, or equivalent to a
  Milestone-9-reviewed conclusion.
- **May later** be confirmed, corrected, downgraded, or superseded once the deeper review occurs,
  without the provisional work being treated as wasted — per §6.

**This decision does not alter the frozen Company Intelligence schema** (`docs/
PORTFOLIO_INTELLIGENCE_SPEC.md` §9, frozen per that document's own §20/§24). No new schema field
is created. Provisional status is recorded through retained review/audit metadata, `operations/
WORKSTREAMS.yaml`, scenario artifacts, or review reports — the same "principle, not a schema
mandate" approach `OPS-0006` §10 already used for the broader Intelligence-lifecycle principle.

### 4. Preliminary portfolio architecture authority

Authorized: **one later, separate, bounded implementation PR** (not opened by this filing) may use:

- currently accepted Intelligence (the thirteen existing records plus any batch, including PR
  #161's AVGO/AMD/MRVL/INTC records, that has cleared an eligible independent review under §1);
- explicitly identified incomplete or uncovered holdings (every roster ticker without a Company
  Intelligence record, named as such, not silently omitted);
- current `targets.yaml` policy, preserved only as an unchanged comparison baseline, per `OPS-0006`
  §2/§3 — never treated as evidence for a preliminary conclusion;

to prepare:

- a preliminary portfolio-role organization;
- a preliminary classification/tier architecture;
- preliminary target or target-range scenarios;
- explicit confidence and evidence-quality labels for every element above;
- a coverage-gap register (which holdings have no record, or only a provisional one, and why);
- a current-policy-versus-provisional-scenario comparison table;
- **no claim of final portfolio-wide completion** — this PR may not describe Milestones 3 through
  8 as complete, in whole or in part, beyond what has actually and separately been completed and
  recorded in `operations/WORKSTREAMS.yaml`.

For any holding that is unresearched or insufficiently researched at the time of that future PR,
current policy is preserved as an unchanged temporary baseline and labeled **"not independently
re-derived"** — the future PR may not invent a new conclusion for a holding it has not
independently researched under an eligible-reviewed Intelligence record.

**This is an explicitly provisional bridge across incomplete coverage, not a completion claim.**
It does not authorize, and must not be read to authorize, Milestone 4 (relationship mapping)
beyond the structural-overlap evidence already required inside any merged Intelligence batch's own
comparison artifact, Milestone 5 (zero-based classification) as a final architecture, Milestone 6
(blind classification), Milestone 7 (baseline reconciliation), or Milestone 8 (the final policy
recommendation package) as WS-0005 itself defines them in `OPS-0006` §4 — the artifact this
section authorizes is explicitly preliminary and provisional, produced under this decision's own
separate authority, not a claim that any of those milestones has been performed or completed.

### 5. Monday allocation-readiness bridge

Authorized: **one later, separate, scenario-only allocation package** (not opened by this filing)
containing:

1. An official allocation check using authoritative `targets.yaml`, unchanged.
2. A provisional allocation check using a separate, clearly named scenario target configuration
   (e.g. a differently named YAML file, never `targets.yaml` itself).
3. A reconciliation table explaining every output difference between the two checks.
4. Live holdings and market data refreshed at run time, per the existing workflow (CLAUDE.md
   Workflow §2-3) — not a stale or hypothetical book.
5. Confidence/evidence-quality flags for every changed target in the provisional scenario.
6. **No mutation of authoritative `targets.yaml`.**
7. **No modification of `holdings.yaml`** except an independently authorized live factual sync,
   performed exactly as the existing workflow already requires (share-count or margin updates
   after a real, principal-executed trade) — never a sync manufactured to fit the scenario.
8. **No automatic order placement** — this tool places no orders under any authorization; that
   constraint is unaffected and restated, not created, by this section.

**The provisional scenario must initially be:**

- cash-only;
- margin requested = $0;
- no margin-policy change of any kind;
- no automatic trim or sale mandate based solely on provisional Intelligence;
- no removal of any current holding based solely on incomplete research;
- advisory, and principal-reviewed, before any manual execution — exactly as every allocator
  recommendation already is under this system's Identity & Role.

Because `allocate.py` currently accepts `targets` as an explicit parameter to its pure allocation
functions (confirmed by direct code inspection this session — `plan()` line 236, `build_roster()`
line 88), the later analysis is authorized to call those existing pure functions with a temporary,
in-memory scenario configuration loaded via the existing `load_yaml()` helper pointed at a
separate scenario file — or, alternatively, to run the existing, unmodified `allocate.py` unchanged
inside an isolated throwaway worktree or copy against a separate scenario `targets.yaml`-shaped
file. **This decision does not authorize changing `allocate.py` merely to build this bridge.** A
later preflight may propose a minimal, reversible change only if it demonstrates that neither the
in-memory-parameter approach nor the isolated-copy approach is sufficient — and any such change
requires its own separate authorization; it is not pre-approved here.

### 6. Temporary-use and sunset discipline

Every provisional scenario produced under §4 or §5 must record:

- creation date;
- evidence cutoff (the latest evidence date reflected in any Intelligence record it draws on);
- exact source Intelligence commit heads (which reviewed heads its inputs came from);
- exact `holdings.yaml` sync date used;
- exact market-data run time;
- assumptions made where evidence was incomplete;
- unresolved evidence, carried forward from the underlying records, not smoothed over;
- an expiration or next-review date;
- the rule by which it is superseded (a specific later artifact or decision, named once it exists).

**Mandatory re-review is required when:**

- Fable access returns and a deeper audit is requested;
- any underlying Company Intelligence record it draws on materially changes;
- research coverage materially expands (e.g. a new Milestone-3 batch merges);
- a material earnings, guidance, regulatory, customer, liquidity, or thesis-break event occurs
  affecting any holding the scenario touches;
- the provisional scenario reaches its own recorded expiration date.

The later, deeper review (Milestones 4-9, and any future dedicated Fable or eligible-reviewer audit
of the completed workstream) may confirm or replace a provisional conclusion **without treating the
provisional work as wasted** — a superseded provisional scenario remains a dated, disclosed
snapshot of what the evidence supported at the time, not an error to be erased.

### 7. Hard prohibitions

This decision, and any later PR authorized under it, must not:

- merge, modify, or mark ready PR #161;
- change `targets.yaml`;
- change any holding, tier, role, cluster, cap, or weight in production;
- modify `allocate.py` or `margin_state.py` (see §5's narrow exception process, which is not
  exercised by this filing);
- authorize margin deployment of any kind;
- change the 1.8x leverage cap or the 30% buffer floor;
- recommend or execute a trade;
- begin a fourth Milestone 3 research batch;
- declare Milestone 3 (in aggregate), Milestones 4 through 8, Milestone 9, or WS-0005 as a whole
  complete;
- waive independent review for any WS-0005 gate;
- allow an authoring session to self-review its own work under the §1 standard;
- make provisional Intelligence mathematically load-bearing in `allocate.py` or any production
  path;
- make any provisional scenario, or its output, the authoritative policy automatically — every
  provisional scenario remains advisory and requires explicit principal review before any manual
  execution, exactly as every other allocator output already does.

### 8. Later sequence authorized after merge

After this decision merges, the following sequence is authorized to proceed, each step gated on
the one before it:

A. Independent, exact-head review of PR #161 by an eligible reviewer under §1 (e.g. an independent
   ChatGPT session), satisfying `PI-0025` §I as modified by §2 above.
B. One consolidated, bounded correction pass, only if that review returns a supported (Blocking or
   Major) finding.
C. Exact-head re-review by an eligible reviewer and a retained artifact, per §1.11.
D. Explicit principal acceptance of PR #161 at its exact final head.
E. A provisional-use determination — whether and how PR #161's four new records, once merged,
   enter PROVISIONAL status per §3.
F. Creation of one preliminary architecture/target-scenario package, per §4.
G. The official-and-provisional Monday allocation-check package, per §5.
H. Later Fable (or other eligible reviewer) deeper review of WS-0005 as a whole, and supersession
   of any provisional conclusion, when that deeper review becomes available.

**PR #161 still may not merge until its exact-head independent review, any required correction,
exact-head re-review, and explicit principal acceptance are complete** — nothing in this decision
shortens, waives, or bypasses that sequence; it only widens which reviewers can perform step A/C.

### 9. Governance package scope (this filing)

This filing touches exactly:

1. `governance/decisions/OPS-0007-capability-based-review-provisional-allocation-bridge.md` (this
   file).
2. `governance/decisions.yaml` (index regeneration: one new entry for `OPS-0007`).
3. `operations/WORKSTREAMS.yaml` (WS-0005 entry: record this authorization's existence and
   effect, using only `OPS-0001`'s existing schema and status vocabulary — no new field, no new
   status value; `next_action` states plainly that the next step is independent review of this
   governance PR, not PR #161 work).
4. `CLAUDE.md` (one Decisions Log entry recording this acceptance).

**No other file is touched by this governance filing.** No Company Intelligence record, no
comparison artifact, no freshness-registry row, no target-scenario file, no allocation-check
output, and no test or validator file is created, modified, or authorized to be created by this
filing — those belong exclusively to the later, separate PRs authorized in §4, §5, and §8.

### 10. Effectiveness, review, and merge gates

This governance PR is itself subject to the same discipline it establishes: it must remain in
draft state, gain its own independent review from an eligible reviewer under §1 anchored to its
exact head, and receive explicit principal acceptance before it may be marked ready or merged. This
decision does not mark itself, or authorize marking itself, ready for merge. Nothing in §1 through
§8 becomes effective until this governance PR merges to `main`.

## Rationale

**Why capability-based, not model-specific.** `OPS-0004` already established that a review's value
lies in its independence, its anchoring to an exact head, and its retained attribution — not in
which vendor's model performed it. Naming "Fable" in `PI-0023`/`PI-0024`/`PI-0025`/`OPS-0006`
Milestone 9 reflected reviewer availability at filing time, not a considered judgment that only
Fable can meet this repository's evidentiary bar. Making the repository's research pipeline
dependent on one model's continued availability is an operational fragility with no doctrine
benefit — the twelve capability requirements in §1 are exactly the substance every retained Fable
review on this repository's history has actually satisfied; restating them as a capability standard
changes nothing about what a review must do, only who may perform it.

**Why a narrow prospective supersession, not an edit or a full supersession of `PI-0025`.**
`governance/decisions/README.md`'s own convention forbids editing a decision's substance after
`status: Accepted`; this repository's own precedent (`OPS-0003` narrowing two items of `OPS-0002`;
`OPS-0005` narrowing one item each of `OPS-0003`/`OPS-0004`) shows that a later decision may narrowly
supersede one clause of an earlier one while both remain `status: Accepted` and un-edited. Marking
`PI-0025` `Superseded` would misstate the fact that only its reviewer-identity clause changes — every
other requirement in `PI-0025` §I remains binding exactly as filed.

**Why a provisional bridge now, rather than waiting for Milestones 3-9.** The principal's directive
is explicit: currently available, independently reviewed Intelligence should be usable to prepare
preliminary organizational and scenario work while deeper research continues, provided the
provisional nature of that work is never obscured and no production policy or account state changes
as a result. `OPS-0006` §5 itself contemplates exactly this shape of authorization — "[each
milestone] requires its own separate, later, explicit principal authorization" — this decision is
that authorization for a narrow, explicitly provisional slice of preliminary work, not an
end-run around the Milestone 3-9 gate structure. The hard prohibitions in §7 and the sunset
discipline in §6 exist specifically so that this bridge cannot be mistaken for, or silently expand
into, Milestone 3-9 completion.

**Why the scenario-only allocation bridge does not touch `allocate.py`.** Direct code inspection
this session confirms `plan()` and `build_roster()` already accept `targets` as an explicit
parameter rather than reading `targets.yaml` internally — the existing pure-function design already
supports a scenario run without any code change. Authorizing a code change "merely for this bridge"
would be exactly the kind of unnecessary production-code coupling `OPS-0006` §6 already prohibits
("production coupling between Intelligence and the allocator"); the isolated-copy or in-memory-
parameter approaches are sufficient on the evidence available now.

## Alternatives Considered

- **Wait for Fable access to return before any further WS-0005 review.** Rejected — the principal's
  explicit directive is to remove this single point of failure, not to accept it as a standing
  constraint; independent review substance (§1) is unaffected either way.
- **Amend `PI-0023`/`PI-0024`/`PI-0025`'s files directly to remove "Fable."** Rejected — those
  decisions are `status: Accepted`; `governance/decisions/README.md` forbids editing accepted
  substance, and this repository's own narrow-supersession convention (§2's Rationale) is the
  correct instrument.
- **Let PR #161 be marked ready or merged by this filing, since a capability-based reviewer will
  eventually clear it.** Rejected — explicitly instructed against by the principal, and inconsistent
  with `PI-0025` §I's still-binding requirement that review, correction, and acceptance occur before
  merge.
- **Fold the provisional-Intelligence bridge into a schema change (e.g. a `provisional: true`
  field on Company Intelligence records).** Rejected — `docs/PORTFOLIO_INTELLIGENCE_SPEC.md`'s
  Company YAML schema is frozen (§20/§24); a schema change is its own separate, future governance
  decision, and provisional status is fully expressible through retained review metadata and
  scenario-artifact labeling without touching the frozen schema.
- **Authorize the preliminary architecture and allocation-scenario work to proceed immediately in
  this same filing.** Rejected — the principal's explicit instruction confines this filing to
  process authorization only; the actual preliminary-architecture and scenario PRs are separate,
  later, and still gated on PR #161's own independent review and principal acceptance where they
  depend on its content.
- **Authorize a minimal `allocate.py` change now to make scenario-running more convenient.**
  Rejected — code inspection shows no change is currently necessary; §5 leaves the door open only
  if a later preflight demonstrates genuine need, and even then requires its own separate
  authorization.

## Consequences

**Authorized, effective on this decision's merge:** a capability-based independent-review standard
(§1) replacing the model-specific "Fable" requirement across WS-0005's review gates from this point
forward; a narrow, disclosed prospective supersession of `PI-0025` §I's reviewer-identity clause
only (§2); a PROVISIONAL Intelligence category (§3); one later, separate, bounded preliminary
portfolio-architecture PR (§4); one later, separate, bounded scenario-only, cash-only, zero-margin
Monday allocation-check package (§5); and the sunset/re-review discipline every provisional
artifact must carry (§6).

**Unchanged by this decision:** every existing tier, target, role, cluster, cap, and holding in
`targets.yaml`/`holdings.yaml`; `allocate.py`, `margin_state.py`, `intelligence_validator.py`,
`intelligence_report.py`, every freshness module, and every existing test; every existing Company/
Theme Intelligence record; the frozen Company Intelligence schema (`docs/
PORTFOLIO_INTELLIGENCE_SPEC.md` §9/§20/§24); the 1.8x leverage cap and 30% buffer floor; `PI-0025`'s
every requirement other than the one reviewer-identity clause named in §2; `OPS-0006`'s Milestone
3-9 authorization boundary (unchanged — this decision's §4/§5 bridge is its own separate, narrow
authorization, not a reinterpretation of `OPS-0006` §5); and `MARGIN-0005`'s research charter and
trial ceiling.

**PR #161 is untouched by this filing** — its state (open, draft, unmerged, head
`e37392b075e26d55f2996bcd86487c93b453623a`) is exactly as found at this decision's preflight, and
remains gated on its own independent review, correction if needed, exact-head re-review, and
principal acceptance (§8), now performable by any eligible reviewer under §1, not only Fable.

**No preliminary architecture, no target scenario, and no allocation check of any kind has been
performed by this filing** — §4 and §5 authorize a later, separate implementation only. **No
Milestone 3 batch beyond `PI-0023`/`PI-0024`/`PI-0025` (once merged), and no Milestone 4 through 9
work, is authorized or implied by this decision.** The next concrete step is this governance PR's
own independent review, per §10 — not PR #161 work, not the preliminary-architecture PR, and not
the allocation-check package.
