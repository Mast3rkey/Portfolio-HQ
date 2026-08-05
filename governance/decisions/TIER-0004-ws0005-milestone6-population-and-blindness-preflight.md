---
decision_id: TIER-0004
date: 2026-08-05
status: Proposed
category: tier_classification_governance
related_decisions: [GOV-0001, GOV-0002, OPS-0001, OPS-0006, OPS-0007, OPS-0008, OPS-0009, ONTO-0001, PI-0004, PI-0016, PI-0038, PI-0039, TIER-0001, TIER-0002, TIER-0003, REL-0001, REL-0007, CHART-0001, CHART-0002]
supporting_artifact: governance/audits/WS0005_M6_POPULATION_AND_BLINDNESS_PREFLIGHT_20260805.md
---

## Context

### Authority for this unit

`PI-0038`'s pre-Milestone-6 roadmap (`operations/WORKSTREAMS.yaml`, `WS-0005`) records six ordered
prerequisites required before a fresh Milestone 6 (blind classification) implementation may be
authorized. Prerequisites 1-4 are complete in substance (Step 4's own register `status: complete`
transition is this filing's own responsibility, deferred by `TIER-0003`'s post-merge-verification
comment to "the next WS-0005 filing"). The principal has now explicitly authorized exactly one Step
5 filing (`milestone6-prereq5-population-reconciliation`): reconcile the final eligible
classification population and define the exact blind-drafting process the future Milestone 6
implementation must follow. This filing does not authorize classification of any ticker.

### Preflight performed this session, independently verified, not assumed

`origin` fetched; local `main` confirmed identical to `origin/main` at
`ecd1e89d1278432874dab0d5440a9a8eecbc57d1` — the exact SHA reported in the authorizing task,
independently re-derived rather than trusted. Working tree clean. Zero open pull requests
(`mcp__github__list_pull_requests`, `state: open`, returns `[]`) — no active mutation lane.

`PR #250` (`TIER-0003`) independently re-confirmed via the GitHub API, not taken on faith from the
task's own summary: `merged: true`, merge commit `ecd1e89d1278432874dab0d5440a9a8eecbc57d1`
(matching `origin/main`'s current tip exactly, parents `71dab2d218de5c4184d5f62bc29f0bc7b409c64f`
and `94ce0f930ecd44b32e09d20ed53c3d545aa2b96a`), independent exact-head review `4865299395`
(0 BLOCKING / 0 MAJOR / 0 MINOR / 2 NOTE — "APPROVED FOR PRINCIPAL EXACT-HEAD ACCEPTANCE"),
retained principal-acceptance comment `issuecomment-5193111879` (explicit acceptance quoted
verbatim at exact head `94ce0f930ecd44b32e09d20ed53c3d545aa2b96a`), retained post-merge-verification
comment `issuecomment-5193183437` (merge-tree identity, 5-file scope, 77 decisions/`issues == ()`,
2581/2581 full suite, merge-commit CI `31015769683` `success`), all independently re-confirmed this
session.

`governance/decisions.yaml` and `portfolio_hq.dashboard.decisions.build_catalog('.')` both
independently re-derived: **77 decisions, `issues == ()`**, before this filing's own new row.
`TIER-0004` independently confirmed the next unused identifier: zero `TIER-####` matches beyond
`TIER-0001`/`TIER-0002`/`TIER-0003`, confirming `TIER` remains the correct, already-established
governance prefix for Milestone 5/6 classification-architecture decisions — no new prefix minted.

`targets.yaml`'s `destination:` list independently re-derived: exactly 27 canonical equity rows
(`SPY`/`VEA`/`VWO`/`RESERVE`/`CASH`/`GLD`/`BTC`/`ETH`/`SOL` excluded as non-equity), matching the
authorizing task's expected 27-name list exactly, zero drift. All 27 confirmed to carry a governed
Company Intelligence record (`intelligence/companies/*.yaml`, 53 total records repository-wide, 0
missing among the 27). `relationship_validator.py` — OK (13 records), unaffected;
`intelligence_validator.py` — 53/53 valid, unaffected; `freshness_validator.py` — OK, unaffected.

No condition met a Stop bar. This unit proceeded.

## Decision

**This filing reconciles the final eligible Milestone 6 classification population and specifies the
complete blind-drafting process** — the blindness boundary, redacted-evidence mechanics, drafting
sequencing, sealing and contamination controls, abstention mechanics, and future validator
requirements — for a later, separately authorized Milestone 6 implementation to follow. It does not
authorize Milestone 6, classify any ticker, create any sanitized evidence package, or implement any
validator. Full detail is retained at
`governance/audits/WS0005_M6_POPULATION_AND_BLINDNESS_PREFLIGHT_20260805.md`; summarized below.

### A. Final eligible population — 27 of 27 canonical equities

Derived live from `targets.yaml`: `NVDA, TSM, ASML, AVGO, SNPS, KLAC, MSFT, GOOGL, AMZN, META, PANW,
LLY, ISRG, TMO, ICE, SPGI, V, COST, WM, CEG, ETN, GEV, GNRC, PWR, RTX, RKLB, TSLA`. **Zero
exclusions.** A canonical equity is eligible if it carries governed Company Intelligence, regardless
of `PROVISIONAL` status, partial or blocked primary-source access, a bounded unresolved factual gap,
or current gate status — none of those conditions removes a ticker from the population; each is
instead represented inside that ticker's own future `evidence_quality` axis or, where the permitted
evidence genuinely cannot support a judgment, via the new narrow abstention path (§F). LLY and RKLB
(supporting artifact §3) and the six formerly-gated names — SNPS, ICE, SPGI, WM, RKLB, TSLA
(supporting artifact §4) — are explicitly confirmed included, on the same terms as every other
canonical name; this resolves `TIER-0001`'s own open question #5 (whether the gated set needs
classification at all) directly: yes, on identical terms.

### B. Permitted and forbidden drafting inputs

Permitted (restates `TIER-0003` §A): governed Company Intelligence business/financial/risk/catalyst
content; Theme Intelligence where relevant; `docs/INVESTMENT_ONTOLOGY.md` vocabulary; accepted
comparison artifacts' evidence content only; governed relationship records where permitted by
sequencing (§D). Forbidden — the answer-key list (supporting artifact §6.2, full text): `targets.yaml`/
`target_pct`; `holdings.yaml` weights; `portfolio_role_ref`; `conviction.rating`; `gates.yaml`/gate
membership; any prior tier label; any prior promotion/demotion/retain/remove/target conclusion;
`caps.clusters` and `issuer_lookthrough.yaml` membership **during `economic_role`/`capital_priority`
drafting specifically** (permitted afterward, computationally, for `risk_concentration` only); any
current `risk_concentration` output before the judgment axes are sealed; all chart-domain content
(images, filenames, manifests, coverage status, indicators, interpretations, price-action
conclusions); the CLAUDE.md Decisions Log's prior placement conclusions; any output of a stopped or
prior classification-drafting session.

### C. Redacted evidence-input mechanics (specified, not implemented)

One deterministic redaction procedure, reused identically across all 27 tickers, applied to **both**
each ticker's `.yaml` and its paired `.md` thesis narrative (supporting artifact §7, corrected in
this filing's own bounded correction pass — see Rationale): on the `.yaml`, strip `portfolio_role_ref`
and the entire `conviction` block wholesale, and strip `review.log`'s free-text notes wholesale
(retaining only `cadence_days`/`last_reviewed`/`next_due`); on the `.md`, strip any paragraph or
sentence containing a defined marker (`portfolio_role_ref`, a tier label used as this ticker's own
placement, `conviction.rating`/rating-level discussion, "keep current policy," "committee review,"
"promoted to/from," and similar), **then mandatorily re-scan the redacted output against the same
marker list and treat any surviving match as a hard failure** — the `.md` file is not exempt from
redaction and is not assumed safe by construction (an earlier draft of this filing made that false
claim; direct inspection found `portfolio_role_ref`/tier/conviction/committee-conclusion prose,
unredacted, in 8 of 27 current `.md` files, including TSM, AVGO, and NVDA); on both files, scan-and-
strip any chart-domain reference (a defensive pass; zero found live in any of the 27 records today);
retain `sector`, `industry`, `themes`, `competitive_advantages`, `risks[]`, `sources[]`, and redacted
`.md` thesis prose. Deterministic and re-runnable — the same procedure against the same source commit
produces byte-identical output, auditable by diffing. **No sanitized package is created and no script
is implemented by this filing.**

### D. Sequencing — judgment axes before risk-concentration

Per ticker: (1) generate sanitized evidence; (2) draft `economic_role`; (3) draft `capital_priority`;
(4) seal both judgment axes; (5) only then compute `risk_concentration` mechanically from
`caps.clusters`/`issuer_lookthrough.yaml`/`intelligence/relationships/`; (6) complete
`evidence_quality`; (7) seal the full record; (8) record its hash in the cohort manifest; (9) stop —
Milestone 7 reconciliation does not begin in the same PR. Computing `risk_concentration` only after
both judgment axes are sealed prevents policy-adjacent structural signals from anchoring the
independent judgment the blind-classification exercise exists to protect.

### E. Sealing and contamination controls

Every sealed record carries `lifecycle_status`, `sealed_at`, `governing_decision`,
`drafting_session_or_shard_id`, `schema_version`, `content_sha256` (excluding the seal block itself),
and a `cohort_manifest_entry` pointer (supporting artifact §9.1) — a content-hash-and-timestamp audit
trail, not a claim of cryptographic immutability beyond what a hash-diff can actually prove.
Contamination controls: redaction-first (structural, not behavioral) evidence exclusion; ~5-ticker
shard isolation bounding any single contamination event's blast radius; no cross-ticker peeking
during judgment-axis drafting; a hard sealed-before-comparison stop preventing any "double check
against current weight" reconciliation before Milestone 7. One retained cohort manifest per future
implementation batch records every ticker's `content_sha256` for later audit. **Not created by this
filing.**

### F. Economic-role abstention — narrow schema amendment

`TIER-0002` §3.4 (`capital_priority`) already has a `no_assessment` default; §3.6
(`evidence_quality`) already expresses `blocked`. §3.3 (`economic_role`) has no abstention path at
all. This filing adds exactly one new allowed value to `economic_role.economic_system_ref`'s existing
enum — `unable_to_determine` — requiring, only when selected, two new conditional sub-fields:
`abstention_reason` (one sentence, why the permitted evidence cannot support a determination) and
`evidence_gap_statement` (one sentence, what specific evidence is missing or blocked). `company_role`/
`role_basis` remain independently attempted on a best-effort basis even when `economic_system_ref`
abstains. **Abstention does not cascade** to `capital_priority` or `evidence_quality` — each axis is
sealed on its own evidence sufficiency; a bounded unresolved evidence item on one axis is never
automatic grounds for `no_assessment` or abstention on another. This is the smallest compatible
amendment: one new enum value, two conditional sub-fields, zero new axes, zero new top-level
structure, no numeric score.

### G. Future validator requirement (design only)

A future Milestone 6 implementation PR requires a fresh `classification_validator.py` and dedicated
test file, authored from current `main` at implementation time, enforcing at minimum: the required
four-axis structure; each axis's closed vocabulary including the §F amendment; the §F abstention
field requirements; the absence of any numeric score/target field; the absence of every §B forbidden
answer-key field inside `economic_role`/`capital_priority` specifically; valid sealing metadata;
manifest/hash consistency; and permitted `lifecycle_status` values only. **Not implemented by this
filing** — matching this repository's design-then-implement precedent (`TIER-0002` designed a full
schema with zero files of the new type created).

### H. Prior stopped session — no contamination

The two untracked local files reportedly left by a prior, separate, unpushed session
(`classification_validator.py`, `test_classification_validator.py`) were independently confirmed
absent from this session's working tree (`git status --porcelain` clean; zero filesystem matches).
They were never committed, pushed, or opened in a PR, and remain outside any session's ability to
read, copy, adapt, move, stage, delete, clean, or reuse from this repository's own tracked state. No
cleanup PR is warranted. The future validator (§G) must be authored fresh, independently, and
independently reviewed.

### I. Future batch and shard structure (recommended, not authorized)

All 27 tickers in one coherent future implementation PR; approximately five internal blind-drafting
shards of five to six names each (matching `CHART-0002`'s own shard-review precedent); one
integration and sealing pass; one independent exact-head review of the complete batch; no separate
pilot unless that review finds a genuine architectural defect; no one-PR-per-ticker design. **Not
authorized by this filing** — recorded as the recommended shape for whatever future, separately
authorized implementation decides.

### J. Step 4 and Step 5 register synchronization

`operations/WORKSTREAMS.yaml`'s `milestone6-prereq4-chart-evidence-scope-decision` gate is updated
`status: in_progress` → `status: complete`, reflecting `TIER-0003` (PR #250)'s independently
re-confirmed merge, review, and principal acceptance (§ above) — matching this gate's own stated
completion condition. `milestone6-prereq5-population-reconciliation` is updated `status: proposed` →
`status: in_progress`, recording this filing's own branch and (once it exists) PR number — **not**
`status: complete`, since this filing's own governance PR is itself unmerged, unreviewed, and
unaccepted, matching every prior WS-0005 filing's identical discipline.
`milestone6-prereq6-fresh-authorization-required` and `milestone-6-blind-classification` are left
exactly as merged (`status: blocked` and `status: proposed` respectively) — both already, correctly,
unauthorized; neither is edited by this filing. **Disclosed discrepancy against the authorizing
task's own assumed state**: the task described `milestone6-prereq6` as `status: proposed`; live
`operations/WORKSTREAMS.yaml` instead reads `status: blocked`, a materially equivalent, already-correct
non-authorization state set by `PI-0038` and unedited since. Per this repository's "never trust copied
state over live truth" discipline, live state controls and is left unedited, not "corrected" to match
the task's assumption.

### K. Non-authority

This decision does not authorize: Milestone 6 itself; classification of any ticker; creation of
`intelligence/classification/` or any file inside it; any sanitized evidence package; any validator
implementation; any Step 6 (`milestone6-prereq6-fresh-authorization-required`) work; any edit to
`CHART-0001`, `CHART-0002`, `TIER-0001`, `TIER-0002`, or `TIER-0003`'s own text; any new
`intelligence/relationships/` record or external relationship research; any Company or Theme
Intelligence edit; any tier/target/holdings/gate/cap/cluster/allocator/margin/ladder/trade change; or
any brokerage action. The `milestone-6-blind-classification` gate's own `status: proposed`, "Not
authorized to execute," is unchanged.

### L. Governance package scope (this filing)

This filing touches exactly: (1) this decision file; (2) the supporting audit artifact
(`governance/audits/WS0005_M6_POPULATION_AND_BLINDNESS_PREFLIGHT_20260805.md`); (3)
`governance/decisions.yaml` (one new index row); (4) `operations/WORKSTREAMS.yaml` (`WS-0005` only —
the §J gate updates plus the `active_branch`/`active_pr`/`last_verified_main_sha`/`last_verified_date`
self-reference fields per `OPS-0001`'s existing convention); (5) `CLAUDE.md` (one concise Decisions
Log pointer entry); (6) `test_portfolio_hq_dashboard_decisions.py` (two hardcoded decision-catalog-
count assertions, 77→78, made stale by this filing's own new row). No chart file, no `intelligence/`
company/theme/relationship record, no `targets.yaml`/`holdings.yaml`/`gates.yaml`/
`issuer_lookthrough.yaml`, and no production allocator/margin code is touched.

### M. Effectiveness, review, and merge gates

This governance PR must remain in draft state, gain its own independent eligible review anchored to
its exact head per `OPS-0007` §1, complete any required bounded correction and exact-head re-review,
and receive explicit principal acceptance before it may be marked ready or merged. This session does
not review its own work, mark it ready, merge it, or post principal acceptance. Nothing in this
decision becomes effective until this governance PR merges to `main`.

## Rationale

**Why the population reconciliation reconfirms all 27 rather than assuming the task's own list.**
This repository's own established discipline (every prior filing in this chain independently
re-derives population/coverage facts rather than trusting a prior summary) applies with equal force
to a task's own expected-state text. The 27-name list matched exactly on independent re-derivation —
recorded as a confirmed match, not an assumption.

**Why LLY and RKLB are not excluded despite real, disclosed evidence gaps.** Excluding a ticker for
imperfect evidence would silently narrow Milestone 6's population based on how well an earlier,
separately-scoped research session's `WebFetch` access happened to work that day — a fact about
network conditions, not about the ticker's own economic role or capital-priority question. `TIER-0002`
§3.6's `evidence_quality` axis exists precisely to carry that distinction honestly (a `High`-conviction
thesis can carry `limited` primary-source coverage) rather than resolving it via population exclusion.

**Why the six formerly-gated names are included on identical terms.** Gate status
(`gates.yaml allow_add: false`) is a buy-eligibility fact, explicitly not a research- or
classification-eligibility fact — `gates.yaml`'s own text distinguishes "held, not force-exited"
existing positions from buy eligibility, and nothing in `PHQ-2026-01`/`PHQ-2026-02`/`PI-0038`
conditions Company Intelligence coverage on gate status. Treating "gated" as a classification
exclusion would conflate two independent concepts this repository has already kept separate
throughout its own governance history.

**Why `economic_role` needed an abstention path but the other three axes did not.** `capital_priority`
and `evidence_quality` were each designed with a natural "insufficient basis" value already built in
(`no_assessment`, `blocked`) because their own closed-enum shape made room for it. `economic_role`'s
three free-text/citation sub-fields had no equivalent — a drafting session facing genuinely
undeterminable evidence had no honest way to record that fact within the existing schema, which risks
either a forced low-confidence guess or an ad hoc undocumented workaround. Closing this gap with the
smallest possible amendment (one enum value, two conditional fields) avoids both.

**Why abstention must not cascade automatically across axes.** The authorizing instruction is explicit
that a bounded unresolved evidence item must not automatically produce `capital_priority:
no_assessment`. Automatic cascading would effectively let evidence-quality problems silently expand
into capital-priority judgments no one actually made — the same category of quiet scope creep
`TIER-0003`'s own rationale rejected for chart evidence "entering through an unstated gap." Each axis
must be sealed on its own merits.

**Why the redaction mechanics are specified, not implemented.** Every prior WS-0005 schema-design
filing in this series (`TIER-0002`, and before it `PI-0002`) designed a complete mechanism before any
code or content of the new type existed, deferring implementation to its own later, separately
authorized PR. A deterministic, fully-specified redaction procedure (§C) gives a future
implementation everything needed to build and independently review it, without this filing needing to
carry code review risk for a mechanism no Milestone 6 session has yet used.

**Why sealing is described as a hash-and-timestamp audit trail, not immutability.** Overclaiming what
a repository-native mechanism can guarantee would misrepresent the actual protection to a future
reviewer. `CHART-0002`'s own `verifiability_boundary` field already draws exactly this distinction for
image evidence; this filing applies the same honest framing to classification-record sealing.

## Alternatives Considered

- **Narrow the population to exclude LLY, RKLB, or the six gated names given their weaker evidence
  base.** Rejected — see Rationale; excluding on evidence-quality grounds contradicts the authorizing
  instruction's explicit eligibility standard and the very purpose of the `evidence_quality` axis.
- **Add a fifth "confidence" or "abstention" axis spanning all four existing axes, rather than a
  narrow per-axis amendment to `economic_role` alone.** Rejected — `capital_priority` and
  `evidence_quality` already have adequate abstention/degraded-state representation; a new
  cross-cutting axis would duplicate what those two already do and would violate the authorizing
  instruction's explicit "do not invent a fifth axis" constraint.
- **Implement the redaction script and/or the classification validator in this filing**, since the
  design is fully specified. Rejected — the authorizing instruction explicitly prefers design now,
  code in the later implementation PR, "unless current repository precedent proves that the schema
  amendment cannot be validated without it." No such proof exists: the §F schema amendment is
  reviewable as text (one enum value, two conditional fields) without any code needing to run first,
  matching `TIER-0002`'s own precedent exactly.
- **Fold Step 6 (fresh Milestone 6 authorization) into this same filing, since Steps 1-5 are now
  substantively complete.** Rejected — the authorizing instruction is explicit that this filing
  preserves the requirement for a separate future Step 6 authorization; completing prerequisites 1-5
  does not itself authorize Milestone 6, matching `milestone6-prereq6`'s own register text exactly.
- **"Correct" `milestone6-prereq6`'s live `status: blocked` to `status: proposed` to match the
  authorizing task's own described state.** Rejected — live repository truth controls over a task's
  copied assumption; `blocked` is already a correct, more specific non-authorization state, and
  rewriting another filing's (`PI-0038`'s) own historical gate text without a substantive reason
  would violate this repository's own convention against silently rewriting retained state.

## Bounded Correction (same day, this PR)

An independent exact-head review of PR #251 (anchored to head `5d76e08add4b531b8c29669c6facfa0fc95995aa`)
confirmed every structural/population/register-synchronization claim in this filing accurate, but
returned **CHANGES REQUIRED** on one BLOCKING and one MINOR finding, both now resolved:

**BLOCKING, resolved.** The originally filed §7.2 asserted the paired `.md` thesis narrative "is
evidence-only by construction... and passes through unredacted." The independent reviewer directly
inspected the current 27-ticker population and found `portfolio_role_ref` values, tier-placement
language, conviction restatements, or prior committee/policy-conclusion prose, unredacted, inside at
least 8 of 27 `.md` files — including `TSM.md` ("`portfolio_role_ref: T1` was explicitly approved by
the human principal..."), `AVGO.md` ("`portfolio_role_ref: T2` reflects `targets.yaml`'s current tier
placement..."), and `NVDA.md` (the PI-0017 committee review's "Keep current policy" recommendation),
plus `AMZN.md`, `ISRG.md`, `TMO.md`, `CEG.md`, and `GEV.md`. This finding was independently
re-verified in this correction pass via direct grep against the same 8 files before any text changed
— confirmed accurate, not taken on the reviewer's word alone. **Resolved** by rewriting supporting
artifact §6.1/§7 and this decision's own §C: the false "passes through unredacted" claim is retracted;
the redaction procedure now applies to both the `.yaml` and `.md` files, with a defined marker-based
strip pass for the `.md` file's tier/conviction/committee-conclusion prose, **plus a mandatory
post-redaction re-scan of the `.md` output that treats any surviving marker match as a hard failure**
(not a one-pass trust) — because free-form prose isn't a fixed key list, and this very finding proved
a plausible-sounding "safe by construction" claim can be wrong when actually checked against the
corpus. No population, sequencing, sealing, abstention, or non-authorization claim in this filing was
affected — the correction is confined to §6.1's evidence-source bullet and all of §7.

**MINOR, resolved.** §6.1 and §8 of the supporting artifact attributed a quoted "risk_concentration
computed after judgment axes" sequencing rule to `TIER-0002` §3.5 as already-existing design.
Independently re-verified this correction pass: `TIER-0002` §3.5 states `risk_concentration` is "a
pure cross-reference rollup" (a claim about its computational content) but contains no ordering
language of any kind — the quoted fragment does not appear in `TIER-0002`'s text. The
judgment-before-risk-concentration sequencing rule is legitimate, well-reasoned, and within this
filing's own authorized scope to establish — but it is new content this filing introduces for
Milestone 6, not a restatement of prior `TIER-0002` review. **Resolved** by rephrasing both references
to state the sequencing rule as this filing's own, consistent with (not quoting as already decided by)
`TIER-0002` §3.5's cross-reference-rollup description.

**NOTE, not corrected (reviewer's own assessment: not a defect requiring correction now).** The
reviewer flagged that a future ticker whose `economic_role` abstains (§F) but whose `capital_priority`
still seals independently selects a `comparator_set` under conditions `TIER-0002`'s own rationale
calls indefensible without a settled economic role. This is a real edge case for a future
implementation to address explicitly (e.g., a `capital_priority` rationale disclosing that it was
assessed without a settled `economic_role`) — left unaddressed in this filing per the reviewer's own
recommendation, since the authorizing instruction requires non-cascading abstention and a mechanical
fix here would risk re-introducing cascading behavior the authorizing instruction explicitly
prohibits.

This correction changes no population entry, no gate status transition, no register field beyond what
was already specified, and no non-authorization boundary. It requires its own exact-head re-review
before this filing may be considered ready.

## Delta Correction (same day, this PR, second round)

An independent exact-head delta review of the Bounded Correction above (anchored to head
`a9bef37f2fce5354418fc8a5a943edea9f8937a4`) confirmed the BLOCKING finding fully and correctly
resolved — independently re-verifying the `.md` marker list against all 8 previously-flagged files'
actual text and confirming fail-closed re-scan behavior is correctly specified — but found the
Bounded Correction's own claim to have "resolved by rephrasing both references" was **not accurate as
filed**: only the supporting artifact's §6.1 occurrence was corrected; §8's own opening sentence — the
actual sequencing specification, not a summary reference — still quoted "computed after" and framed
the rule as `TIER-0002` §3.5's "own existing design," the identical defect the original MINOR finding
described.

Independently re-verified before fixing: `grep`-confirmed the supporting artifact's §8 opening
sentence (governing the actual sequencing rule stated in the section that follows it) was unchanged
from its originally filed text, and re-confirmed `TIER-0002` §3.5 contains no ordering language of any
kind (same check as the first correction pass, re-run against current `main` at this filing's base).
**Resolved** by applying the identical rephrasing already used in §6.1 to §8's opening sentence:
removed the quoted "computed after" fragment and the "own existing design" framing, restated as this
filing's own new sequencing rule, consistent with (not quoting) `TIER-0002` §3.5's cross-reference-
rollup description. The one remaining "computed after" occurrence in the supporting artifact (§11,
"computed after sealing per §8") was independently checked and confirmed correctly attributes ordering
to this filing's own §8, not to `TIER-0002` — left unedited, not a defect.

This delta correction changes no population entry, no gate status transition, no redaction mechanics,
no register field, and no non-authorization boundary — confined to one sentence in the supporting
artifact's §8. It requires its own exact-head re-review before this filing may be considered ready.

## Consequences

**Authorized, effective only on this decision's merge:** the reconciled 27-name Milestone 6
population with zero exclusions; the specified permitted/forbidden evidence boundary; the specified
redaction mechanics, sequencing, sealing/contamination controls, and validator requirements (design
only, no implementation); the `economic_role` abstention schema amendment (text only, applies to no
existing record); the `milestone6-prereq4` gate transition to `status: complete`; the
`milestone6-prereq5` gate transition to `status: in_progress` recording Option-A-successor Step 5 as
substantively complete pending merge.

**Not authorized by this filing, now or ever without a further separate decision:** Milestone 6
itself; classification of any ticker; any sanitized evidence package; any validator implementation;
Step 6 (fresh authorization) of the pre-Milestone-6 roadmap; any edit to `CHART-0001`, `CHART-0002`,
`TIER-0001`, `TIER-0002`, or `TIER-0003`'s own text; any new `intelligence/relationships/` record or
external relationship research; any Company or Theme Intelligence edit; and any
tier/target/holdings/gate/cap/cluster/allocator/margin/ladder/trade/brokerage/order change.

**Unchanged by this decision:** every existing Company/Theme/relationship Intelligence record,
byte-for-byte; `CHART-0001`'s, `CHART-0002`'s, `TIER-0001`'s, `TIER-0002`'s, and `TIER-0003`'s own
accepted text and scope, in full, unedited; `targets.yaml`, `holdings.yaml`, `gates.yaml`,
`issuer_lookthrough.yaml`, `allocate.py`, `levels.py`, `margin_state.py`; the Constitution; `WS-0005`'s
top-level `status`, `priority`, `authorized_scope`, `prohibited_scope`, and `completion_criteria`;
Milestones 1-4's own `status: complete` (unedited, not reopened); the `milestone6-prereq6-fresh-
authorization-required` gate's own `status: blocked` and the `milestone-6-blind-classification` gate's
own `status: proposed` (both unedited, not reopened).

This decision becomes effective only when its implementing pull request merges to `main`.
