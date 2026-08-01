---
decision_id: LADDER-0001
date: 2026-08-01
status: Accepted
category: research_charter
related_decisions: [GOV-0001, GOV-0002, OPS-0001, OPS-0007, OPS-0008, OPS-0009, NUM-0001, MARGIN-0005, PHQ-2026-01, PHQ-2026-02]
supporting_artifact: research/buy_ladder_backtest/PROTOCOL_V1.md
---

## Context

A completed, read-only Buy-Ladder and Trim-Level Evidence Design Audit (conversation-only, no
repository artifact of its own) found: `reports/rung_backtest.md` (2026-07-12) tested the current
ATR-based buy-ladder methodology against a retired 65-ticker tier universe; `PHQ-2026-02`
(2026-07-31) migrated `targets.yaml` from that tiered structure to the canonical 27-name
`destination:` architecture; the ladder calibration has never been re-tested against the current
roster; ladder spacing, rung count, sizing, reset rules, ETF treatment, and crypto treatment remain
unresolved for that roster; and the audit recommended one narrowly scoped, pre-registered ladder
backtest as the smallest reversible next step. This filing treats those as leads, independently
verified below, not as pre-established fact.

**Preflight performed this session, independently verified, not assumed:** repository confirmed
`Mast3rkey/Portfolio-HQ`; `origin/main` fetched; local branch
`claude/buy-ladder-backtest-governance-74svzu` confirmed identical to `origin/main` at
`6db533338d3958233a23a09c375b91a5df9b00a9` (the merge commit of PR #211, `OPS-0012`), zero
divergence in either direction, working tree clean, no upstream configured (first push this
session). Exactly two open PRs exist in the repository: `#212` ("Dashboard 2.0: modern responsive
visual redesign", `OPS-0012` implementation, draft) and `#213` ("`OPS-0013`: authorize Governance
Decision Explorer", draft) — both based on the same `origin/main` head this filing is also based
on, neither touching `levels.py`, `allocate.py`, `targets.yaml`, `gates.yaml`, any `backtest_*.py`
script, `reports/`, or `research/`; no overlap with this filing's scope, and neither is modified,
reviewed, or merged by this filing. No other branch in the repository (96 branches enumerated via
the GitHub API) names or evidently concerns a ladder backtest, trim-policy change, or
capital-deployment study in flight. `governance/decisions/` and `governance/decisions.yaml` both
carry 55 entries (54 decision files plus `README.md`, versus 55 index rows — `governance/
decisions.yaml` reconciles 1:1 against every non-`README` file); highest filed `PHQ-####` is
`PHQ-2026-05`, highest `OPS-####` is `OPS-0012` (`#213`'s claimed `OPS-0013` is not yet merged and
does not reserve the number against a conflicting series), no `LADDER-####` series exists anywhere
in the repository (`decision_log.yaml`, `governance/decisions/`, `governance/decisions.yaml`, and a
full-repository grep for the string all return zero hits) — confirming `LADDER-0001` as a genuinely
new decision domain, chosen per `governance/decisions/README.md`'s own rule ("a new prefix is
chosen only when a genuinely new decision domain needs one — not pre-declared in advance"), not the
domain this task's own drafting prompt assumed. `PHQ-####` was considered and rejected for this
filing: every existing `PHQ-####` decision (`PHQ-2026-01` through `PHQ-2026-05`) records the
principal's approval of architecture, holdings, or gated-name disposition reached through a
**separate, out-of-repository "Portfolio-HQ committee" process** (`PHQ-2026-01`'s own text: "an
independent track from, and not a component of, WS-0005's in-repository zero-based tier review") —
this filing is the opposite shape: an in-repository, pre-registered, hash-pinned, retrospective
empirical study, with no out-of-repository committee evidence package behind it. `MARGIN-0005`
("research_charter" category) is the closest structural precedent — a bounded, pre-registered,
retrospective backtest charter under this repository's post-`GOV-0001` governance architecture —
but its `MARGIN-####` prefix is domain-specific to margin/target-sizing research and is not reused
for a different research domain, matching this repository's own narrow-prefix discipline. A new
`LADDER-####` series, category `research_charter` (matching `MARGIN-0005`'s category exactly, since
this is the same kind of decision — a bounded, pre-registered, retrospective backtest charter — for
a different domain), is therefore the correct family, independently re-derived from repository
state rather than assumed.

`levels.py`, `allocate.py`'s `build_roster()`, `targets.yaml`, `gates.yaml`, `reports/
rung_backtest.md`, and `backtest_rungs.py` were each independently re-read this session (not
summarized from the audit lead alone). `backtest_rungs.py`'s `roster_tickers()` reads
`targets.yaml["tiers"]` — that key no longer exists in `targets.yaml`, confirming the audit's first
lead directly: the existing rung backtest cannot run against, and was never re-run against, the
current canonical roster. The current production ladder mechanism (`levels.py`) was independently
verified against its actual source, not restated from the audit summary — see
`research/buy_ladder_backtest/PROTOCOL_V1.md` §3 for the verified specification.

## Decision

**`LADDER-0001` authorizes exactly one thing: the research protocol frozen in
`research/buy_ladder_backtest/PROTOCOL_V1.md`, pinned by SHA-256 below.** This filing itself
performs no data acquisition, writes no simulation code, runs no simulation, computes no live or
historical price, generates no buy list, and touches no production file. It authorizes a later,
separate implementation PR — gated on this decision's own independent review and principal
acceptance, and required to stay in draft state until that review lands — to execute exactly the
protocol's bounded, pre-registered study: three arms (current ATR ladder; a fixed-percentage
pullback ladder; immediate/scheduled deployment), on the current canonical non-gated equity/fund/
GLD roster, over the 2021-06-01-to-present window, against a pre-committed 1.0pp TWR / 1.0pp MaxDD
materiality threshold, producing a protocol, a deterministic script, a data manifest, an output
report, a limitations section, and a governance recommendation — nothing more.

### 1. Exact research authority granted

This charter authorizes only:

1. Execution of the study defined in `research/buy_ladder_backtest/PROTOCOL_V1.md` — Arms A
   (current production ATR ladder), B (fixed-percentage pullback ladder), and C (immediate/
   scheduled deployment baseline) — strictly as that document's §§1-23 freeze them, including its
   universe (§5), gated-name exclusion (§6), data period (§9), deposit/sizing/cash/reset rules
   (§10), corporate-action handling (§11), gate and cluster/issuer treatment (§12/§13), metrics
   (§14), segmented and sub-period reporting (§15/§16), success threshold and adoption rule (§17),
   and crypto exclusion (§19).
2. The data-acquisition step named in the protocol §21 — split-adjusted daily bars for the frozen
   universe, cached read-only under `research/buy_ladder_backtest/data/` (git-ignored, matching
   `research/margin_target_study/data/.gitignore`'s existing convention) and recorded in a future
   `research/buy_ladder_backtest/data_manifest.yaml` (source, acquisition timestamp, per-ticker
   coverage, minimum-history exclusions, known limitations).
3. One future, separate implementation PR limited to the approved files in §4 below, carrying its
   own full independent-review, correction-if-needed, re-review, principal-acceptance, merge, and
   post-merge-verification cycle under `OPS-0007` §1 and `OPS-0009` Lane G (this filing is itself
   Lane G — a new governance authorization — and is not reduced by any `OPS-0009` lane).

Everything not listed is not authorized. This charter is not an adoption decision, not a
`levels.py` change, not a `targets.yaml` change, and not an allocator change. It grants no
brokerage, Alpaca-account, Robinhood, or live-data access beyond the same read-only historical-bar
client every existing `backtest_*.py` script in this repository already uses.

### 2. Prohibited production effects (absolute for this charter's entire life)

- No order placement, ever (order methods remain absent from `alpaca_client.py`).
- No modification of `holdings.yaml`, `targets.yaml`, `gates.yaml`, `issuer_lookthrough.yaml`,
  `allocate.py`, `levels.py`, `margin_state.py`, Intelligence records, dashboard code, `CLAUDE.md`
  doctrine text, or the Constitution by research code or by virtue of any research result.
- No current ticker recommendation, buy list, price target, or live signal of any kind. This study
  computes historical, retrospective figures only.
- No implication that any of SNPS, ICE, SPGI, WM, RKLB, or TSLA is presently buy-eligible — all six
  remain excluded from the study's simulated universe entirely (protocol §6), and this charter does
  not authorize activating any of them.
- No cash or margin deployment of any kind; no change to the 1.8x leverage cap or 30% buffer floor;
  no margin-relevance claim of any kind (this study is unrelated to `MARGIN-0005`'s research lane
  and does not consume any of its trial budget).
- No re-running of the closed `rung_backtest.md`/`t1t2_trim_backtest.md`/`trend_backtest.md`
  questions as variants — this is a new question (current canonical roster, not the retired tier
  universe) under its own protocol, not a rerun of a closed one.
- No Intelligence-to-allocator coupling, no conviction/thesis/moat/sentiment/valuation/freshness
  input to any arm (protocol §7).
- No chart-pattern or screenshot-derived input to any arm (protocol §8).
- Operator discretion is unaffected by this charter in every respect — it grants no new
  authorization of any kind over live account state.

### 3. Hash pinning (same-PR chronology)

`research/buy_ladder_backtest/PROTOCOL_V1.md` was finalized first, its SHA-256 computed, and the
exact hash inserted here — both this decision and the protocol are filed together in this single
governance PR:

- `research/buy_ladder_backtest/PROTOCOL_V1.md`
  SHA-256: `a61f55e600e6f334de7fd0c00d8a78f181dbabd4f7e8997f7f6db5a3208f59d8`

After merge, the hash is verified from the committed blob (`git show <merge>:research/
buy_ladder_backtest/PROTOCOL_V1.md | sha256sum`). **No simulation may run before this PR is merged
and the pinned hash verifies.** Any later change to the pinned protocol is a charter amendment: its
own governance decision with a newly pinned hash, per the protocol's own §20/§22.

### 4. Approved files for future implementation

A future implementation PR under this charter may create or modify only:

| Area | Files | Constraint |
|---|---|---|
| Research package | `research/buy_ladder_backtest/` — `data_manifest.yaml`, `assumptions_ledger.yaml` (if needed), a deterministic simulation script (e.g. `run_ladder_backtest.py`), `data/**` (git-ignored cache), `results/**` | Zero import relationship with `allocate.py`/`levels.py`/`margin_state.py` in either direction (read the production modules for reference only, or reimplement the frozen §3 specification locally — either way, the study must not become a hidden second entry point into production code); writes only under its own directory |
| Output report | `research/buy_ladder_backtest/REPORT.md` or `reports/ladder_backtest_canonical.md` (implementation PR's choice, matching this repository's existing `reports/*.md` convention) | Read-only findings document; no code |
| Tests | A focused, deterministic test file for the simulation script, if the implementation PR's own scope requires one | No live network in CI, matching every existing `backtest_*.py`/`test_*.py` convention in this repository |

No production file (`allocate.py`, `levels.py`, `margin_state.py`, `targets.yaml`, `holdings.yaml`,
`gates.yaml`, `issuer_lookthrough.yaml`, dashboard code, Intelligence content, freshness modules, or
the Constitution) may be created or modified by that future PR.

### 5. Stopping, adoption, and non-adoption rules

Reused unedited from `research/buy_ladder_backtest/PROTOCOL_V1.md` §§17-18 and restated here for
visibility: no result produced under this charter — however strong, on any segment — automatically
changes `levels.py`, `targets.yaml`, or any production behavior. A result meeting the pre-committed
threshold is a **recommendation only** (retain / simplify / adopt / no change / insufficient
evidence), requiring its own separate, later, independently reviewed and principal-accepted
governance decision before any production file is touched. A null or inside-threshold result closes
the question under the same "no re-runs without a new regime in the data" discipline this
repository's Decisions Log already applies to every other closed backtest. The program stops and
reports what it has, without adoption, upon: an inside-threshold result on a segment; an unresolved
minimum-history data gap that removes too much of a segment to draw a conclusion (protocol §5, §18);
a principal stop order at any time, for any reason, effective immediately; or a discovered material
conflict with a higher-authority source per `GOV-0002` (affected work halts until reconciled).

### 6. Workstream

This filing establishes `WS-0010` in `operations/WORKSTREAMS.yaml` (`status: proposed`,
`priority: secondary` — `WS-0005` remains the repository's sole `priority: primary` workstream,
unaffected by this filing) recording: ladder backtest authorization proposed; study not yet run;
implementation not begun; no current policy change; no trade recommendation; independent review and
principal acceptance required before this authorization is effective. The workstream is not marked
`authorized`/effective until this governance PR merges.

### 7. Governance package scope (this filing)

This filing touches exactly:

1. `governance/decisions/LADDER-0001-canonical-buy-ladder-backtest-authorization.md` (this file).
2. `research/buy_ladder_backtest/PROTOCOL_V1.md` (the pinned protocol).
3. `governance/decisions.yaml` (index regeneration: one new entry for `LADDER-0001`).
4. `operations/WORKSTREAMS.yaml` (one new entry, `WS-0010`, per §6 above).
5. `CLAUDE.md` (one concise Decisions Log pointer entry).

**No other file is touched.** No production code, no `backtest_*.py` script, no dashboard code, no
`holdings.yaml`/`targets.yaml`/`gates.yaml`/`issuer_lookthrough.yaml`, no Intelligence or freshness
content, no Constitution text, and neither PR `#212` nor PR `#213` is touched by this filing.

### 8. Effectiveness, review, and merge gates

This governance PR must remain in draft state, gain its own independent eligible review anchored to
its exact head per `OPS-0007` §1 (this is `OPS-0009` Lane G — a new governance authorization, always
full weight, never reduced), complete any required bounded correction and exact-head re-review, and
receive explicit principal acceptance before it may be marked ready or merged. **This decision does
not mark itself ready and does not authorize its own merge.** Nothing in §§1-7 above, or in the
pinned protocol, becomes effective, and no simulation may begin, until this PR merges to `main` and
the pinned hash verifies from the committed blob.

## Rationale

**Why a new `LADDER-####` prefix, not `PHQ-####` or `MARGIN-####`.** `PHQ-####` is reserved, by
every existing filing in that series, for decisions ratifying the separate out-of-repository
Portfolio-HQ committee's own architecture/holdings/gated-name work — this filing has no such
committee package behind it and is not that kind of decision. `MARGIN-####` is domain-specific to
margin/target-sizing research (`MARGIN-0005`'s own charter). This filing is structurally identical
to `MARGIN-0005` — a bounded, pre-registered, hash-pinned, retrospective backtest charter under
post-`GOV-0001` governance — but for buy-ladder/execution methodology, a genuinely distinct research
domain from margin. `governance/decisions/README.md`'s own rule is that a new prefix is chosen only
when a genuinely new domain needs one, not pre-declared — that is exactly this case, independently
re-derived from repository state rather than assumed from this task's own drafting prompt (which
explicitly instructed against assuming the ID).

**Why `MARGIN-0005` is the structural template, not a fresh design.** This repository already has a
working, principal-approved shape for "bounded, pre-registered, retrospective, hash-pinned research
charter that authorizes a protocol and a later separate implementation, never an immediate result."
Reusing that shape (hash pinning, approved-file table, stopping/adoption/non-adoption rules, hard
prohibitions) for a different research domain is lower-risk than inventing new charter mechanics,
and keeps this filing's own review surface bounded to what actually differs (the protocol's
technical content), not the charter mechanism itself.

**Why the study is scoped to the canonical non-gated equity/fund/GLD roster, with crypto and gated
names excluded.** The audit's own findings — ETF treatment, crypto treatment, and gated-name
treatment are all unresolved — are addressed directly, not glossed over: gated names are excluded
because they are not currently buy-eligible in production and simulating a purchase would misstate
current authorization (protocol §6); crypto is excluded because no retained evidence supports
transferring an equity-calibrated ladder finding to BTC/ETH/SOL, and crypto already carries
materially different production doctrine (no trend/RSI/earnings gate) (protocol §19); ETFs and GLD
are included but reported as their own segments, not pooled with equities, because their
return/volatility profiles differ materially and pooling would obscure asset-class-specific effects
(protocol §15).

**Why three arms, not more.** The task's own instruction — "keep the study bounded," "avoid
optimization fishing" — and this repository's own `trim_backtest.md` precedent (per-ticker tailored
parameters explicitly rejected as overfitting) both argue against a wide arm or parameter set. Three
arms with one fixed parameterization each, isolating "how are levels computed" (A vs. B) and
"is waiting for any level worth it at all" (A/B vs. C) as the only two questions, is the smallest
design that still answers the research question. Reopening the previously-rejected
support/resistance arm was explicitly considered and declined (protocol §4) — no new hypothesis or
evidence regime is documented, and TradingView screenshots are not a reproducible numerical input
this charter permits as a study variable (protocol §8).

## Alternatives Considered

- **File under `PHQ-####`, since the current canonical roster is a `PHQ-2026-02` artifact.**
  Rejected — `PHQ-####` names the out-of-repository committee process itself, not any research
  question that happens to reference the canonical roster it approved; using it here would misstate
  this filing's actual provenance (an in-repository, self-contained, hash-pinned protocol, with no
  external committee package).
- **File under `MARGIN-####`, reusing `MARGIN-0005`'s series since it is the closest structural
  precedent.** Rejected — `MARGIN-####` is margin/target-sizing-domain-specific by this repository's
  own established convention (`governance/decisions/README.md`'s prefix-scoping rule); reusing it
  for an unrelated execution-methodology question would blur two genuinely distinct research
  domains and complicate any future margin-specific search or audit of that series.
- **Combine the protocol's content directly into this decision file, with no separate
  `PROTOCOL_V1.md`.** Rejected — the pre-registration content (23 required elements) is
  substantial enough that `MARGIN-0005` itself used a separate, hash-pinned protocol document
  rather than inlining it; following that precedent keeps the governance file focused on
  authorization scope and keeps the frozen technical specification independently hash-verifiable,
  exactly `MARGIN-0005`'s own design.
- **Include a fourth arm (support/resistance pivots, or an ATR-multiplier sweep).** Rejected —
  reopening the already-closed support/resistance question requires a new hypothesis and evidence
  regime this filing does not have (the task's own instruction warns against this specifically); a
  parameter sweep is optimization fishing this repository has already rejected once
  (`trim_backtest.md`).
- **Include a labeled gated-name counterfactual arm.** Rejected for this first study — even a
  clearly labeled counterfactual risks being misread as implying near-term eligibility for SNPS,
  ICE, SPGI, WM, RKLB, or TSLA; deferred to a future, separately authorized study if ever pursued,
  keeping this filing's own scope unambiguous.
- **Build a full point-in-time dividend ledger, matching `MARGIN-0005`'s standard.** Rejected as
  disproportionate to this study's "smallest reversible next step" framing — every existing closed
  backtest in this repository (rung/regime/trend/weight/trim/t1t2) already uses price-return only,
  disclosed as a limitation; matching that existing standard, not `MARGIN-0005`'s heavier one built
  for a much larger research program, is the proportionate choice here.

## Consequences

**Authorized, effective only on this decision's merge:** the frozen research protocol in
`research/buy_ladder_backtest/PROTOCOL_V1.md`; one later, separate, bounded implementation PR
limited to §4's approved files, itself gated on its own independent review, correction if needed,
re-review, principal acceptance, merge, and post-merge verification; `WS-0010` as a `proposed`
workstream tracking this authorization.

**Not authorized by this filing, now or ever without a further separate decision:** any
`allocate.py`/`levels.py`/`margin_state.py` change; any `targets.yaml`/`holdings.yaml`/`gates.yaml`/
`issuer_lookthrough.yaml` change; any dashboard integration; any trim rule; any buy list or current
ticker recommendation; any SOL reduction; any ICE (or any other gated name) purchase; any cash or
margin deployment; any Constitution change; any Intelligence-to-allocator coupling; any automated
scoring or ranking; any change to `MARGIN-0005`'s charter, trial ceiling, or research lane; any
touch to PR `#212` or PR `#213`.

**Unchanged by this decision:** the canonical `targets.yaml`
`destination:` list, `gates.yaml`, and `issuer_lookthrough.yaml` exactly as `PHQ-2026-02` through
`PHQ-2026-05` left them; `allocate.py`, `levels.py`, and `margin_state.py`; every existing Company/
Theme Intelligence record; the 1.8x leverage cap and 30% buffer floor; `MARGIN-0005`'s research
charter and trial ceiling (this filing consumes none of it); `OPS-0007`'s twelve-point review
standard and `OPS-0009`'s lane discipline (this filing is reviewed under both, in full, as Lane G).
No trade has been recommended, no backtest has been run, and no production behavior has changed by
this filing.

This decision becomes effective only when its implementing pull request merges to `main`.
