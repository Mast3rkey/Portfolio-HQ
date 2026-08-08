---
decision_id: VALUATION-0001
date: 2026-08-08
status: Proposed
category: research_charter
related_decisions: [GOV-0001, GOV-0002, OPS-0001, OPS-0006, OPS-0007, OPS-0008, OPS-0009, NUM-0001, ONTO-0001, TIER-0002, TIER-0003, TIER-0009, MARGIN-0005, LADDER-0001, XASSET-0001, XASSET-0005, PHQ-2026-01, PHQ-2026-02]
supporting_artifact: research/equity_valuation_study/PROTOCOL_V1.md
file: governance/decisions/VALUATION-0001-equity-valuation-research-charter.md
---

## Context

### Authority for this unit

`TIER-0009` (WS-0005 Milestone 8 policy-recommendation-framework authorization, accepted and merged
via PR #262) §K forces `target_and_range` and `maximum_position_size` to `primary_status:
valuation_required` on all 27 canonical equities, stating explicitly: "no such framework currently
exists anywhere in this repository," and that a future valuation architecture "is not created,
authorized, or implied by this filing in any way — it is a distinct, unscoped, future workstream this
filing identifies as a prerequisite... without beginning it," naming `MARGIN-0005`/`LADDER-0001`'s
bounded-charter discipline as the model a future filing should follow to close it. This filing is that
future filing, scoped to equities only.

### Preflight performed this session, independently verified, not assumed

- **Repository identity** confirmed `Mast3rkey/Portfolio-HQ`. `origin/main` fetched; local branch
  `claude/valuation-0001-research-charter-xg2jz8` confirmed created from, and identical to,
  `origin/main` at `1921864326f2cc75609b1c91037c24e333c4e3d0` (PR #273's merge commit), zero
  divergence in either direction, working tree clean throughout.
- **Zero open pull requests** confirmed via the GitHub API (`list_pull_requests`, `state: open`) —
  empty result. No competing mutation lane exists.
- **PR #273 (`XASSET-0005`) independently re-confirmed merged**, including its full multi-round
  review lifecycle: accepted head `8415c82ec82bbd4a99a1c0961184200290945350`; three independent
  reviews (`pullrequestreview-4887790034` CHANGES REQUIRED 0/1/0/1; `pullrequestreview-4887859729`
  CHANGES REQUIRED 0/0/2/1; `pullrequestreview-4887894742` **APPROVED FOR PRINCIPAL EXACT-HEAD
  ACCEPTANCE**, 0 BLOCKING / 0 MAJOR / 0 MINOR / 1 non-actionable NOTE, at exact head `8415c82e...` —
  this is the correct, real final review; a previously-circulated identifier,
  `pullrequestreview-4887997383`, does **not** exist anywhere in this PR's review history and must
  not be propagated); principal acceptance `issuecomment-5224205559`; merge commit
  `1921864326f2cc75609b1c91037c24e333c4e3d0` (parents `e5446cd5c4bfce744691fd1914ec8ef098286839` and
  `8415c82ec82bbd4a99a1c0961184200290945350`, both independently re-confirmed via `git show`,
  merge-tree confirmed byte-identical to the accepted head's own tree — zero drift at merge);
  merge-commit CI run `31236387352`/job `93049536968`, `status: completed`/`conclusion: success`.
  Full Lane M synchronization recorded in §7 below.
- **Decision catalog independently rebuilt: 94 decisions, `issues == ()`** — matching the expected
  post-merge state exactly.
- **`operations/WORKSTREAMS.yaml` independently re-read in full** — 14 workstreams, `WS-0005` the
  sole `status: complete` entry with `priority: secondary` (per `TIER-0013`), zero
  `priority: primary` workstreams remaining. `WS-0014` (`status: proposed`, `priority: secondary`,
  title "Contender Normalization and Cross-Asset Synthesis") independently re-read in full — its
  fourteen-item scope list, transcribed verbatim from `XASSET-0001` §I, does not include equity
  valuation methodology design or research anywhere in its enumeration.
- **Full repository `pytest` independently re-run this session: 3341 passed, 0 failed**, matching the
  expected post-`XASSET-0005` baseline exactly.

### Identifier determination — `VALUATION-####`, not `XASSET-####`

Independently re-derived from repository state, not assumed. `governance/decisions/README.md`'s own
rule: "a new prefix is chosen only when a genuinely new decision domain needs one — not pre-declared
in advance." Three lines of evidence, read together, resolve this as a genuinely new domain:

1. **`TIER-0009` §K's own words.** Having `XASSET-0001` and `WS-0014` already available to cite (both
   are named elsewhere in the same filing's `related_decisions`), `TIER-0009` §K deliberately did
   *not* point the future valuation architecture at either — it called it "a distinct, unscoped,
   future workstream," language this repository consistently uses to mean a literal `WS-####`
   register entity, and explicitly named `MARGIN-0005`/`LADDER-0001` as the structural template, not
   `XASSET-0002`/`XASSET-0005` (the XASSET series' own prior "framework design" filings).
2. **Domain mismatch with `XASSET-####`'s established identity.** Every `XASSET-####` filing to date
   (`XASSET-0001` cross-asset architecture; `XASSET-0002` ETF+crypto classification framework design;
   `XASSET-0003`/`XASSET-0004` ETF/crypto classification authorization; `XASSET-0005` functional
   doctrine + overlap-model architecture) is either explicitly cross-asset in scope or asset-class-
   specific to ETF/crypto/functional-capital-use. This filing's own authorized scope is the opposite
   shape — **equity-only**, with ETF/crypto/GLD/cash/debt valuation methodology explicitly and
   repeatedly excluded (protocol §12, this file's §2). Filing an equity-only charter under a prefix
   whose established identity is "cross-asset" would misstate this filing's actual scope, the same
   reasoning `LADDER-0001`'s own Rationale used to reject filing under `MARGIN-####` ("would blur two
   genuinely distinct research domains").
3. **Direct structural precedent: `LADDER-0001` itself.** `LADDER-0001` faced the identical question —
   a bounded, equity/roster-adjacent research charter that could plausibly have been folded into an
   existing series (`WS-0005`, `MARGIN-####`) but was instead independently re-derived as "a
   genuinely distinct research domain" and given its own prefix and its own workstream (`WS-0010`),
   explicitly reusing `MARGIN-0005`'s charter *mechanics* while keeping the domain separate. Equity
   valuation/economic-assessment methodology research is, by the same test, distinct in kind from
   every existing domain: not tier/company classification (`TIER-####`), not cross-asset architecture
   (`XASSET-####`), not margin/leverage sizing (`MARGIN-####`), not buy-ladder/execution timing
   (`LADDER-####`), not company narrative research (`PI-####`), not relationship mapping (`REL-####`),
   not chart evidence (`CHART-####`).

`VALUATION-####` is confirmed, by full-repository search this session (`decision_log.yaml`,
`governance/decisions/`, `governance/decisions.yaml`, and a full-text grep), to be a genuinely unused
prefix. Category `research_charter`, matching `MARGIN-0005`/`LADDER-0001` exactly — this is the same
kind of decision (a bounded, pre-registered charter authorizing a later, separate research
implementation), for a third distinct domain.

### Workstream determination — new `WS-0015`, not `WS-0014`

Following directly from the identifier determination above and the same `MARGIN-0005`→`WS-0001`/
`LADDER-0001`→`WS-0010`/`CHART-0001`→`WS-0011` pattern (every genuinely new research-charter domain
in this repository's history has been assigned its own dedicated workstream, never folded into an
existing one merely because the subject matter is thematically adjacent), this filing establishes
`WS-0015`. `WS-0014`'s own scope (§ above) does not include this work, and `WS-0014`'s own title
("Contender Normalization and Cross-Asset Synthesis") does not describe an equity-only valuation
charter. No existing `WS-0014` field is touched by this filing.

## Decision

**`VALUATION-0001` authorizes exactly one thing: the research protocol frozen in `research/
equity_valuation_study/PROTOCOL_V1.md`, pinned by SHA-256 below.** This filing itself performs no
methodology-family comparison, no archetype-fit evaluation, computes no valuation of any company, and
touches no production file. It authorizes a later, separate implementation PR — gated on this
decision's own independent review and principal acceptance, and required to stay in draft state until
that review lands — to execute exactly the protocol's bounded, pre-registered study: four research
questions (archetype differentiation; methodology defensibility; false-precision protection;
evidence sufficiency), evaluated via a closed 7×7 methodology-family-by-archetype-category matrix
against a four-value closed disposition vocabulary, producing one methodology-evaluation report —
nothing more.

### 1. Exact research authority granted

This charter authorizes only:

1. Execution of the study defined in `research/equity_valuation_study/PROTOCOL_V1.md` — strictly as
   that document's §§1–19 freeze it, including its research questions (§2), governing boundaries
   (§3), seven methodology families (§4), seven archetype categories (§5), evidence-source boundary
   (§6), 49-cell evaluation matrix and closed disposition vocabulary (§7), falsification/abstention
   rules (§8/§9), false-precision protections (§10), required output shape (§11), and prohibited-
   activities list (§12).
2. One future, separate implementation PR limited to the approved files in §4 below, carrying its own
   full independent-review, correction-if-needed, re-review, principal-acceptance, merge, and
   post-merge-verification cycle under `OPS-0007` §1 and `OPS-0009` Lane G (this filing is itself
   Lane G — a new governance authorization, full weight, never reduced).

Everything not listed is not authorized. This charter is not an adoption decision, not a `TIER-0009`
Milestone 8 amendment, not a `targets.yaml` change, and not an allocator change. It grants no
brokerage, Alpaca-account, Robinhood, or live-market-data access of any kind — this study consumes no
market data or company-specific financial data (protocol §6/§13).

### 2. Prohibited production and research effects (absolute for this charter's entire life)

- No valuation, fair value, price target, or expected return for any real company, at any point, for
  any purpose — including an "illustrative" or "worked-example" application of a methodology family
  to a real ticker.
- No archetype-category (protocol §5) assignment of any real, named canonical-roster company.
- No historical backtest of a valuation methodology's output against subsequent stock-price
  performance, under any framing — this is predictive research, permanently prohibited by CLAUDE.md's
  Guardrails, and is not what this charter authorizes (protocol §1).
- No chart, technical-indicator, or screenshot-derived input to any part of this study (protocol §3).
- No modification of `holdings.yaml`, `targets.yaml`, `gates.yaml`, `issuer_lookthrough.yaml`,
  `allocate.py`, `levels.py`, `margin_state.py`, any existing Company/Theme/relationship/
  classification/reconciliation/recommendation Intelligence record, dashboard code, `CLAUDE.md`
  doctrine text, or the Constitution by research code or by virtue of any research result.
- No claim that `TIER-0009`'s `target_and_range`/`maximum_position_size` `valuation_required` status
  is resolved, closed, or ready to be revisited by this charter's own output — that determination
  requires its own later, separate governance decision (protocol §15).
- No ETF, cryptocurrency, GLD, cash/reserve, or debt-reduction valuation or economic-assessment
  methodology content of any kind — equity only, per `XASSET-0001` §C/§D's own asset-appropriate-
  framework requirement, unaffected here.
- No consumption of `MARGIN-0005`'s trial budget or any change to its charter; no relationship to
  `LADDER-0001`'s charter or trial scope.
- Operator discretion is unaffected by this charter in every respect — it grants no new authorization
  of any kind over live account state.

### 3. Hash pinning (same-PR chronology)

`research/equity_valuation_study/PROTOCOL_V1.md` was finalized first, its SHA-256 computed, and the
exact hash inserted here — both this decision and the protocol are filed together in this single
governance PR:

- `research/equity_valuation_study/PROTOCOL_V1.md`
  SHA-256: `2948e4a852330fdbb649dc67a0cf317ef91119af21e053659fcd5a3709a10980`

After merge, the hash is verified from the committed blob (`git show <merge>:research/
equity_valuation_study/PROTOCOL_V1.md | sha256sum`). **No methodology-comparison research,
archetype-fit evaluation, or any other work under this charter may begin before this PR is merged and
the pinned hash verifies.** Any later change to the pinned protocol is a charter amendment: its own
governance decision with a newly pinned hash, per the protocol's own §17/§18.

### 4. Approved files for future implementation

A future implementation PR under this charter may create or modify only:

| Area | Files | Constraint |
|---|---|---|
| Output report | `research/equity_valuation_study/METHODOLOGY_EVALUATION_REPORT.md` or `reports/equity_valuation_methodology.md` (implementation PR's choice, matching this repository's existing `reports/*.md` convention) | Read-only findings document; no code; no company-specific content (protocol §12) |
| Research package | `research/equity_valuation_study/` — any supporting notes or an `assumptions_ledger.yaml`-style provenance file, if the implementation PR's own scope requires one | No live network calls; no market-data or financial-statement acquisition of any kind (protocol §6/§13 — this study has no data-acquisition step) |

No production file (`allocate.py`, `levels.py`, `margin_state.py`, `targets.yaml`, `holdings.yaml`,
`gates.yaml`, `issuer_lookthrough.yaml`, dashboard code, Intelligence content, freshness modules, or
the Constitution) may be created or modified by that future PR. No test file is anticipated as
required by this charter's own scope (no code is produced), but the implementation PR may add a
focused test file if its own scope introduces any parseable artifact (e.g., an assumptions ledger)
warranting one, matching this repository's existing convention.

### 5. Stopping, adoption, and non-adoption rules

Reused unedited from `research/equity_valuation_study/PROTOCOL_V1.md` §§11/14/15/17 and restated here
for visibility: no result produced under this charter — however well-supported — automatically
changes any target, tier, cap, gate, cluster, allocator, margin, ladder, or Intelligence-record field,
and does not itself resolve `TIER-0009`'s `valuation_required` status on any of the 27 canonical
equities. A completed methodology-evaluation report is a **research input only**, requiring its own
separate, later, independently reviewed and principal-accepted governance decision before any
methodology is selected, adopted, or applied to a real company. The program stops and reports what it
has, without adoption, upon: completion of the 49-cell matrix with any cell honestly resolved
`insufficient_evidence_to_determine` where the literature does not support a firmer conclusion
(protocol §9); a principal stop order at any time, for any reason, effective immediately; or a
discovered material conflict with a higher-authority source per `GOV-0002` (affected work halts until
reconciled).

### 6. Workstream

This filing establishes `WS-0015` in `operations/WORKSTREAMS.yaml` (`status: proposed`, `priority:
secondary` — zero `priority: primary` workstreams exist in the repository per `TIER-0013`, unaffected
by this filing) recording: equity valuation research charter authorized; study not yet run;
implementation not begun; no current policy change; no company valuation of any kind; independent
review and principal acceptance required before this authorization is effective. The workstream is
not marked `authorized`/effective until this governance PR merges.

### 7. Lane M — PR #273 (`XASSET-0005`) lifecycle, independently re-verified and recorded

Per `OPS-0009`'s additive historical convention, recorded here without editing any prior filing's own
text:

- Accepted head: `8415c82ec82bbd4a99a1c0961184200290945350`.
- Final independent review: `pullrequestreview-4887894742` — **APPROVED FOR PRINCIPAL EXACT-HEAD
  ACCEPTANCE**, 0 BLOCKING / 0 MAJOR / 0 MINOR / 1 non-actionable NOTE, at exact head `8415c82e...`.
  Two earlier review rounds on the same PR (`pullrequestreview-4887790034`, CHANGES REQUIRED — 1
  MAJOR overlap-model coverage-gap finding; `pullrequestreview-4887859729`, CHANGES REQUIRED — 2
  MINOR findings) were both fully resolved by bounded corrections before this final review, per
  `XASSET-0005`'s own correction-history text (unedited by this filing).
- **Correction of a previously-circulated identifier**: `pullrequestreview-4887997383` was reported
  in an earlier task handoff as PR #273's final review. Independently re-verified this session via
  the GitHub API — the PR's actual review list contains exactly three reviews
  (`pullrequestreview-4887790034`, `pullrequestreview-4887859729`, `pullrequestreview-4887894742`);
  `4887997383` does not exist anywhere in PR #273's history. This filing records the correction so
  the erroneous identifier is not propagated further; it does not indicate any defect in `XASSET-0005`
  itself.
- Principal acceptance: `issuecomment-5224205559`.
- Merge: `1921864326f2cc75609b1c91037c24e333c4e3d0`, parents `e5446cd5c4bfce744691fd1914ec8ef098286839`
  and `8415c82ec82bbd4a99a1c0961184200290945350` (both independently re-confirmed via `git show`;
  merge-tree confirmed byte-identical to the accepted head's own tree — zero drift at merge).
- Merge-commit CI: run `31236387352`, job `93049536968`, `status: completed`/`conclusion: success`.

`XASSET-0005`'s own historical gate text in `operations/WORKSTREAMS.yaml` (`xasset0005-...`) is left
exactly as filed — this section adds one additive post-merge-verification gate (§8) rather than
rewriting any existing entry.

### 8. Register updates performed by this filing

`operations/WORKSTREAMS.yaml` receives exactly two changes:

1. **A new `WS-0015` entry** (full text in the accompanying commit), `status: proposed`, `priority:
   secondary`, `dependencies: []` (this charter is equity-only and self-contained — it does not
   depend on `WS-0005`'s or `WS-0014`'s own execution to begin its own authorized research), scope
   matching §1/§2/§4 above exactly.
2. **One additive `xasset0005-implementation-post-merge-verification` gate on the existing `WS-0014`
   entry**, recording — without editing any existing `WS-0014` field — the §7 Lane M facts above
   (PR #273's accepted head, corrected final-review identifier, principal acceptance, merge, and
   merge-commit CI), matching this repository's established Lane M convention (`xasset0004-
   implementation-post-merge-verification`, `xasset0003-post-merge-verification`, and similar prior
   entries) of folding a prior PR's post-merge synchronization into the next filing that substantively
   touches the register, rather than opening a dedicated reconciliation PR for a routine, no-finding
   verification.

No `WS-0005` field is touched by this filing.

### 9. Governance package scope (this filing)

This filing touches exactly:

1. `governance/decisions/VALUATION-0001-equity-valuation-research-charter.md` (this file).
2. `research/equity_valuation_study/PROTOCOL_V1.md` (the pinned protocol).
3. `governance/decisions.yaml` (index regeneration: one new entry for `VALUATION-0001`).
4. `operations/WORKSTREAMS.yaml` (one new `WS-0015` entry, plus one additive `WS-0014` Lane M gate,
   per §8 above).
5. `CLAUDE.md` (one concise Decisions Log pointer entry, including the §7 Lane M record).
6. `test_portfolio_hq_dashboard_decisions.py` (decision-catalog count assertions, 94 → 95).

**No other file is touched.** No production code, no `backtest_*.py` script, no dashboard code, no
`holdings.yaml`/`targets.yaml`/`gates.yaml`/`issuer_lookthrough.yaml`, no Intelligence or freshness
content, no Constitution text.

### 10. Effectiveness, review, and merge gates

This governance PR must remain in draft state, gain its own independent eligible review anchored to
its exact head per `OPS-0007` §1 (this is `OPS-0009` Lane G — a new governance authorization, always
full weight, never reduced), complete any required bounded correction and exact-head re-review, and
receive explicit principal acceptance before it may be marked ready or merged. **This decision does
not mark itself ready and does not authorize its own merge.** Nothing in §§1–9 above, or in the
pinned protocol, becomes effective, and no research may begin, until this PR merges to `main` and the
pinned hash verifies from the committed blob.

## Rationale

**Why a new `VALUATION-####` prefix, not `XASSET-####`.** See the Context section's Identifier
determination above — restated briefly: `TIER-0009` §K's own text deliberately declined to name
`XASSET-0001`/`WS-0014` as the future home for this gap despite having both available to cite; every
existing `XASSET-####` filing is either cross-asset or ETF/crypto/functional-capital-use in scope,
while this filing is equity-only by explicit, repeated design; and this repository's own established
pattern (`MARGIN-0005`, `LADDER-0001`, `CHART-0001`) is to mint a new prefix, and typically a new
workstream, for every genuinely new research-charter domain, never to fold one into an existing series
merely because the subject matter is thematically adjacent.

**Why `MARGIN-0005`/`LADDER-0001` are the structural template for charter *mechanics*, while the
research *content* is closer to `TIER-0001`/`TIER-0002`'s design-then-authorize pattern.** `TIER-0009`
§K explicitly names `MARGIN-0005`/`LADDER-0001`'s discipline as the model to follow — hash-pinned
protocol freeze, bounded approved-file list, explicit non-adoption rule, dedicated workstream. But
neither of those two charters computes a valuation; both test a mechanical timing/deployment rule
against historical price data. This charter's actual research — comparing methodology families
against archetype categories on theoretical-defensibility grounds — has no analogous historical-data
input and would misapply the numeric-threshold/data-acquisition machinery those two charters use for
a genuinely different kind of question (see protocol §§1/13/14 for the full reasoning). Reusing the
proven charter *mechanics* while adapting the *content* design to this study's own closed-matrix
shape is lower-risk than either inventing a wholly new charter mechanism or forcing a numeric-backtest
shape onto a qualitative comparison.

**Why this charter must never become predictive research.** CLAUDE.md's Guardrails state "No
predictive research, price targets, or 'opportunity maps'" without qualification, and the Decisions
Log has rejected every prior attempt at anything resembling forecasting-based research (the band-
overlay backtest, chart-pattern reading, market-view-driven margin timing). A study that tested
"would methodology X's output have predicted subsequent returns" would be exactly that — this charter
is deliberately designed to never ask that question, evaluating methodology defensibility on
theoretical/data-availability grounds only (protocol §1/§3), never on predictive accuracy.

**Why archetype differentiation is preserved as an open research question (RQ1), not resolved here.**
The task's own instruction — "explicitly address whether equity archetypes require differentiated
methodology... do not silently force one method across structurally different companies" — matches
this repository's own repeated discipline of not forcing a uniform mechanism where the evidence does
not support one (the cluster-cap system's own per-cluster, not portfolio-wide, calibration; `TIER-
0002`'s abstention path). Pre-deciding RQ1 in this charter, rather than leaving it as the first thing
the future implementation must answer with cited reasoning, would be exactly the kind of premature
methodology selection this filing is authorized not to perform.

**Why a 49-cell closed matrix instead of a numeric backtest.** See protocol §14 in full — a numeric
materiality threshold requires a numeric outcome to threshold against; this study produces none.
Inventing one merely for consistency with `MARGIN-0005`/`LADDER-0001`'s shape would be false
precision, which this charter's own §10/protocol §10 exists specifically to prevent.

## Alternatives Considered

- **File under `XASSET-0006`, continuing the existing cross-asset series.** Rejected — see the
  Context section's Identifier determination in full; the domain mismatch (equity-only vs. `XASSET`'s
  established cross-asset identity) and `TIER-0009` §K's own explicit "distinct... workstream"
  language both argue against this, and the repeated `MARGIN-0005`/`LADDER-0001`/`CHART-0001`
  precedent of minting a new prefix for a genuinely new domain is directly on point.
- **File as a `WS-0014` item, reusing that workstream rather than creating `WS-0015`.** Rejected for
  the same reasons — `WS-0014`'s own fourteen-item scope list (`XASSET-0001` §I), independently
  re-read in full this session, does not include equity valuation methodology anywhere, and its own
  title ("Contender Normalization and Cross-Asset Synthesis") does not describe this filing's scope.
- **Design a numeric backtest comparing valuation-methodology outputs against subsequent stock
  returns, matching `MARGIN-0005`/`LADDER-0001`'s empirical shape exactly.** Rejected outright — this
  would be predictive research, permanently prohibited by CLAUDE.md's Guardrails and the Decisions
  Log's repeated rejection of forecasting-shaped studies (see Rationale above). Not a close call.
- **Pre-select a single "winner" methodology now, to save a future research round.** Rejected — the
  task's own explicit instruction against pre-selecting a winner, and this repository's own zero-based
  discipline (`OPS-0006` §2/§3) applied by analogy: a methodology selection made without the
  archetype-fit research this charter authorizes would be exactly the kind of premature conclusion
  this repository has repeatedly guarded against.
- **Fold the archetype taxonomy (protocol §5) into `docs/INVESTMENT_ONTOLOGY.md` (`ONTO-0001`)'s
  existing vocabulary rather than defining a new, narrower one.** Rejected — `ONTO-0001`'s economic-
  systems/company-roles/capital-types vocabulary serves a different analytical purpose (thematic,
  qualitative committee-review discussion) and is explicitly frozen, amendable only through its own
  separate governance decision; forcing a valuation-methodology-fit taxonomy into it would conflate
  two genuinely distinct classification purposes, the same reasoning `XASSET-0001` §C already applied
  to reject forcing ETF/crypto evidence into `TIER-0002`'s equity-shaped schema.
- **Include a numeric materiality threshold anyway, for consistency with every other closed backtest
  in this repository.** Rejected — protocol §14 explains in full why this would be false precision
  for a study with no empirical numeric outcome; consistency with a template's *shape* does not
  justify manufacturing a number this study's own design does not produce or need.

## Consequences

**Authorized, effective only on this decision's merge:** the frozen research protocol in `research/
equity_valuation_study/PROTOCOL_V1.md`; one later, separate, bounded implementation PR limited to §4's
approved files, itself gated on its own independent review, correction if needed, re-review, principal
acceptance, merge, and post-merge verification; `WS-0015` as a `proposed` workstream tracking this
authorization; the §7 Lane M record of PR #273's confirmed lifecycle.

**Not authorized by this filing, now or ever without a further separate decision:** any valuation,
fair value, price target, or expected return for any real company; any archetype-category assignment
of any real company; any `allocate.py`/`levels.py`/`margin_state.py` change; any `targets.yaml`/
`holdings.yaml`/`gates.yaml`/`issuer_lookthrough.yaml` change; any dashboard integration; any
Company/Theme/relationship/classification/reconciliation/recommendation Intelligence record creation
or edit; any resolution of `TIER-0009`'s `valuation_required` status; any ETF/crypto/GLD/cash/debt
valuation methodology content; any chart-evidence use; any Constitution change; any Intelligence-to-
allocator coupling; any automated scoring or ranking; any change to `MARGIN-0005`'s or `LADDER-0001`'s
own charter, trial ceiling, or research lane.

**Unchanged by this decision:** the canonical `targets.yaml` `destination:` list, `gates.yaml`, and
`issuer_lookthrough.yaml` exactly as `PHQ-2026-02` through `PHQ-2026-06` left them; `allocate.py`,
`levels.py`, and `margin_state.py`; every existing Company/Theme/relationship/classification/
reconciliation/recommendation Intelligence record, including all 27 sealed Milestone 6 classifications
and the Milestone 7/8 artifacts; `docs/INVESTMENT_ONTOLOGY.md` (`ONTO-0001`); `TIER-0009`'s own
`valuation_required` forcing on `target_and_range`/`maximum_position_size`; `XASSET-0001` through
`XASSET-0005`'s own text and authority, unedited; `MARGIN-0005`'s and `LADDER-0001`'s own research
charters and trial ceilings (this filing consumes neither); `OPS-0007`'s twelve-point review standard
and `OPS-0009`'s lane discipline (this filing is reviewed under both, in full, as Lane G). No
valuation has been computed, no methodology has been selected, no company has been assessed, and no
production behavior has changed by this filing.

This decision becomes effective only when its implementing pull request merges to `main`.

### Correction history (this filing, same PR)

**Bounded correction, independent exact-head review `pullrequestreview-4888034268` of head
`be2ca335435a750c5f2359a8c7035274826ea203`, one finding, 0 BLOCKING / 0 MAJOR / 1 MINOR / 1
non-actionable NOTE:** the review independently re-read `research/equity_valuation_study/PROTOCOL_V1.md`
§6 in full and found an internal cross-reference error — the clause barring `targets.yaml`,
`holdings.yaml`, `gates.yaml`, and `issuer_lookthrough.yaml` field values as evidence carried a
parenthetical, "(structure may be read for the RQ4 evidence-category question only, per above)," whose
"per above" back-reference actually points to the immediately preceding Company Intelligence schema
sentence, not to anything said about these four files — RQ4 (§2) is defined solely in terms of the
Company Intelligence schema and makes zero mention of these four files anywhere. As written, a future
implementer could misread the parenthetical as authorizing a structural read of four live production
config files for a purpose RQ4 never asks about. **Resolved** by removing the ambiguous parenthetical
and replacing it with an explicit statement that these four files are barred outright, structure
included, with the sole structural-read permission in §6 confirmed to apply only to the Company
Intelligence schema. This is a narrow, bounded wording correction inside §6 only — it does not touch
§2/§4/§5/§7/§14 or any other prohibition list, all of which the review independently confirmed were
already unambiguous. Because the corrected protocol's bytes differ from the originally filed version,
its SHA-256 changes and is re-pinned in full above (§3): **old hash**
`80aee45dbdc766d96625ce65887a85b7579658d5cf5b3d39dc7a1a0f1e35c995` → **new hash**
`2948e4a852330fdbb649dc67a0cf317ef91119af21e053659fcd5a3709a10980`, independently reproducible via
`sha256sum research/equity_valuation_study/PROTOCOL_V1.md` at the corrected head. No research question,
methodology family, archetype category, matrix cell, closed vocabulary, absolute prohibition, or
`VALUATION-0001`/`WS-0015` authority is changed by this correction. The review's own non-actionable
NOTE (directional methodology-fit framing embedded in §5's archetype descriptions) is carried forward
unresolved and non-actionable, per the review's own explicit finding that it is not a defect. Requires
its own fresh independent exact-head delta review before this PR may be considered ready.
