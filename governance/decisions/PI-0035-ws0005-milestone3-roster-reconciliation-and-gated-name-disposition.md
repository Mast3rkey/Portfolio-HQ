---
decision_id: PI-0035
date: 2026-07-31
status: Proposed
category: portfolio_intelligence
related_decisions: [GOV-0001, GOV-0002, OPS-0001, OPS-0006, OPS-0007, OPS-0008, OPS-0009, PI-0005, PI-0011, PI-0013, PI-0014, PI-0016, PI-0027, PI-0031, PI-0032, PI-0033, PHQ-2026-01, PHQ-2026-02]
supporting_artifact: null
---

## Context

### Preflight (independently verified this session, not assumed)

- **Repository identity** confirmed `Mast3rkey/Portfolio-HQ`.
- **`origin/main` fetched.** `git fetch origin main` returned `d5400e998d71fa45ff8235b46d6d473f4d0640d8` as
  `origin/main`'s tip, matching this session's designated branch's own starting `HEAD` exactly
  (`git rev-parse HEAD` = `git rev-parse origin/main` before any commit). Working tree confirmed clean
  before any edit. `d5400e998d71fa45ff8235b46d6d473f4d0640d8` is PR #207's merge commit — WS-0007
  post-merge factual synchronization after PR #199 (repository-native dashboard). **Zero open pull
  requests** confirmed live via the GitHub API at this filing's preflight; no branch or in-flight work
  overlapping this filing's scope.
- **`CLAUDE.md`, `constitution/INVESTMENT_CONSTITUTION.md`, `governance/decisions/README.md`,
  `governance/decisions.yaml`, `OPS-0006`, `OPS-0007`, `OPS-0008`, `OPS-0009`, `PI-0031`, `PI-0032`,
  `PI-0033`, and `PHQ-2026-01` through `PHQ-2026-05` read in full this session** (not relied on from
  memory), together with `targets.yaml`, `gates.yaml`, `operations/WORKSTREAMS.yaml`, and
  `intelligence/companies/` — independently, directly, not inferred from any prior summary.
- **`governance/decisions.yaml` and `governance/decisions/` independently reconciled**: 52 files under
  `governance/decisions/` (excluding `README.md`) = 52 entries in `governance/decisions.yaml`, no
  orphans, highest filed `PI-####` is `PI-0034`. **`PI-0035` confirmed the next unused decision number**
  in its series, checked live against both the directory and the index, not assumed.
- **`intelligence/companies/` independently confirmed to hold 45 files** (`.yaml`/`.md` pairs): AAPL,
  ABBV, AMAT, AMD, AMZN, ASML, AVGO, BRK.B, CEG, COST, CRM, CRWD, CVX, ETN, GEV, GILD, GOOGL, IBM, INTC,
  ISRG, JNJ, JPM, KLAC, LLY, LRCX, MA, META, MLM, MRK, MRVL, MSFT, MU, NOW, NVDA, ORCL, PANW, PWR, SKHY,
  TMO, TSM, V, VRT, WDC, WMT, XOM.
- **`targets.yaml` independently re-parsed in full — this is the central finding this decision acts
  on.** `PHQ-2026-02` (merged 2026-07-31, same day as `PHQ-2026-01`, `PHQ-2026-03`, `PHQ-2026-04`, and
  `PHQ-2026-05`, all after `PI-0031`/`PI-0032`/`PI-0033` were filed and merged 2026-07-28) retired the
  T1/T2/ETF/band/spec tier structure entirely and replaced it with `targets.yaml`'s flat `destination:`
  list — 34 rows across `equity`/`fund`/`reserve`/`cash`/`crypto` asset classes, no tier labels of any
  kind. **`destination:` currently carries exactly 27 rows with `asset_class: equity`**: NVDA, TSM,
  ASML, AVGO, SNPS, KLAC, MSFT, GOOGL, AMZN, META, PANW, LLY, ISRG, TMO, ICE, SPGI, V, COST, WM, CEG,
  ETN, GEV, GNRC, PWR, RTX, RKLB, TSLA. `PI-0031` §K's completion criteria 1-3 are stated entirely in
  terms of the retired T1 (10 tickers)/T2 (14 tickers)/cluster-membership structure — a roster anchor
  `PHQ-2026-02` has since made obsolete. This is not a new fact requiring research; it is a direct,
  independently-verified reading of `targets.yaml` as currently committed to `main`.
- **Cross-referenced the 27-company canonical equity list against `intelligence/companies/`'s 45
  records**, independently, name by name:
  - **19 canonical names already carry a Company Intelligence record**: NVDA, TSM, ASML, AVGO, KLAC,
    MSFT, GOOGL, AMZN, META, PANW, LLY, ISRG, TMO, V, COST, CEG, ETN, GEV, PWR.
  - **8 canonical names carry no record.** Of these, exactly **4 are actionable-gated**
    (`gates.yaml`, authority `PHQ-2026-01`): **SNPS, ICE, SPGI, WM** — none of the four appears in any
    prior Milestone 3 batch authorization, deferral, or disposition; they entered the canonical roster
    only with `PHQ-2026-02`'s migration and have never been individually addressed by Company
    Intelligence governance. The other **4 are already individually dispositioned by `PI-0033` §A**:
    **GNRC** (§A.2), **RTX** (§A.7), **RKLB** (§A.11), **TSLA** (§A.12) — each carries its own
    company-specific materiality assessment, deferral reason, and reopening trigger, filed under the
    old tier labels (`band`/`spec`) but naming the same tickers the canonical architecture still
    contains at the same rows.
  - **26 of the 45 existing Company Intelligence records cover tickers no longer present in
    `targets.yaml`'s canonical `destination:` list**: AAPL, ABBV, AMAT, AMD, BRK.B, CRM, CRWD, CVX,
    GILD, IBM, INTC, JNJ, JPM, LRCX, MA, MLM, MRK, MRVL, MU, NOW, ORCL, SKHY, VRT, WDC, WMT, XOM. These
    were governed holdings (T1/T2/band/spec, or cluster members) at the time their batches were
    authorized (`PI-0023`-`PI-0034`); `PHQ-2026-02`'s migration to the 37-row (now 34-row, post
    `PHQ-2026-04`) canonical architecture did not carry all of them forward — e.g. `oil`'s cluster
    membership (`XOM, CVX`) is now `tickers: []` in `targets.yaml`'s `caps.clusters`, meaning neither
    surviving canonical name backs that cap any longer; `semis` retained only 5 of its former 13
    members (WDC dropped); the T1/T2 roster (24 names) is gone as a concept entirely.
  - **`caps.clusters` independently re-parsed**: `semis` (ASML, TSM, NVDA, AVGO, KLAC, 25.0%) — all 5
    covered. `power_infra` (ETN, GEV, PWR, 20.0%) — all 3 covered. `oil` (`tickers: []`, 20.0%) — no
    current members, so no coverage question currently applies to it.
- **`gates.yaml` independently re-parsed**: 6 gated tickers total (SNPS, ICE, SPGI, WM, RKLB, TSLA),
  each `status: cash_pending_clearance`, `authority: PHQ-2026-01`, `allow_add: false`, each carrying its
  own `next_gate` text transcribed verbatim from the retained `PHQ-2026-01` evidence. RKLB and TSLA are
  simultaneously gated **and** already carry a `PI-0033` disposition (a name can be both); SNPS, ICE,
  SPGI, and WM are gated with **no** disposition of any kind on record — the gap this decision closes.
- **No repository truth conflicts with this filing's own scope.** The 27/19/4-gated/4-`PI-0033`/26-
  off-roster accounting above was independently re-derived from live `targets.yaml`, `gates.yaml`, and
  `intelligence/companies/` state, not copied from any prior session's summary.

`PI-0031` §K defined seven completion criteria for WS-0005 Milestone 3 against the roster as it stood on
2026-07-28. Criteria 1-3 name that roster explicitly (T1's 10 tickers, T2's 14 tickers, and the
then-current `caps.clusters` membership including WDC as an uncovered `semis` name). `PHQ-2026-02`
retired that entire tiered roster three days later. No accepted decision has yet reconciled `PI-0031`
§K's completion accounting against the roster that now actually governs the account. Separately, four
canonical equity names (SNPS, ICE, SPGI, WM) — all pre-existing actionable gates under `PHQ-2026-01` —
have never received any Company Intelligence disposition, because they were not part of the tiered
roster any prior Milestone 3 filing accounted for. This decision performs both reconciliations. It
performs no company research and changes no portfolio behavior.

## Decision

**PI-0035 authorizes exactly three things: (1) narrow supersession of `PI-0031` §K's completion criteria
1-3, restated against the current canonical 27-company equity list; (2) four new, individually reasoned
Company Intelligence coverage dispositions for SNPS, ICE, SPGI, and WM, each deferred to its own existing
`gates.yaml` reopening condition; and (3) an explicit reaffirmation that `PI-0033`'s existing GNRC, RTX,
RKLB, and TSLA dispositions remain controlling, unedited, and unreopened.** This is **accounting
reconciliation and disposition recording only** — no research has been performed, and this filing alone
authorizes no research finding, Company Intelligence record, comparison artifact, freshness-registry row,
policy change, tier/target/roster/cluster/cap/gate/allocator change, margin-policy recommendation, trade,
or order. **This filing touches only the governance-authorization package** — this decision file,
`governance/decisions.yaml`, the smallest directly related `operations/WORKSTREAMS.yaml` fields for the
WS-0005 Milestone 3 gate, and one `CLAUDE.md` Decisions Log entry.

**This filing is Lane G (Governance authorization) under `OPS-0009` §1** — full weight throughout: no
reduced preflight, no reduced review, no reduced principal-acceptance requirement.

### A. Old roster versus canonical roster

| | Old anchor (`PI-0031` §K, as filed 2026-07-28) | Canonical anchor (this decision, `targets.yaml` as of `PHQ-2026-02`/`PHQ-2026-04`) |
|---|---|---|
| Structure | T1 (10) / T2 (14) / ETF / band / spec tiers | Flat `destination:` list, `asset_class: equity` \| `fund` \| `reserve` \| `cash` \| `crypto` |
| Equity denominator | 24 T1+T2 names explicitly named in §K.1/§K.2; band/spec named elsewhere | 27 `asset_class: equity` rows |
| Cluster membership | `semis` included WDC (uncovered); `oil` included XOM, CVX (CVX authorized same filing) | `semis`: ASML, TSM, NVDA, AVGO, KLAC (WDC no longer a member); `oil`: no members (`tickers: []`); `power_infra`: ETN, GEV, PWR (unchanged) |
| Gated names | Not a `PI-0031`/`PI-0032`/`PI-0033` concept — gates postdate all three (`PHQ-2026-01`/`PHQ-2026-02`, 2026-07-31) | 6 gated tickers (`gates.yaml`): SNPS, ICE, SPGI, WM, RKLB, TSLA |

### B. Exact current completion-accounting denominator

**27 canonical equity names**, `target_pct` and Company Intelligence status as independently verified
above:

- **19 covered**: NVDA, TSM, ASML, AVGO, KLAC, MSFT, GOOGL, AMZN, META, PANW, LLY, ISRG, TMO, V, COST,
  CEG, ETN, GEV, PWR.
- **4 gated, newly dispositioned by this decision** (§D below): SNPS, ICE, SPGI, WM.
- **4 non-gated, already dispositioned by `PI-0033`, reaffirmed unedited by this decision** (§E below):
  GNRC, RTX, RKLB, TSLA (RKLB and TSLA are also gated — both facts hold simultaneously and neither
  supersedes the other).

**19 + 4 + 4 = 27. Every canonical equity name is now either covered, gated-and-deferred, or
`PI-0033`-deferred — accounted for, not researched.** Accounting for all 27 does not itself mean
Milestone 3 is complete; see §G.

### C. Narrow supersession of `PI-0031` §K criteria 1-3

**This decision narrowly supersedes `PI-0031` §K criteria 1 and 2 in full, and the roster-membership
clause of criterion 3, and nothing else in `PI-0031` or `PI-0033`.** `PI-0031` §K's own text is not
edited (per `governance/decisions/README.md`'s never-edit-after-Accepted convention) — this decision
restates the criteria going forward, controlling from this decision's own merge:

1. ~~Every T1 company has a current Company Intelligence record.~~ **Restated: every canonical equity
   name in `targets.yaml`'s `destination:` list that is not actionable-gated and not individually
   deferred by accepted authority has a current Company Intelligence record.** (As of this filing: 19 of
   19 such names are covered — see §B. The T1 concept no longer exists in `targets.yaml`; this criterion
   is restated against the flat canonical list, not against any tier.)
2. ~~Every non-deferred T2 company has a current Company Intelligence record.~~ **Retired as a separate
   criterion — the T1/T2 distinction no longer exists in `targets.yaml`.** Criterion 1 as restated above
   now covers what criteria 1 and 2 jointly covered under the old tiered structure; maintaining two
   criteria that differed only by a tier label that no longer exists would restate the same fact twice.
3. **Every member of every active correlated-cluster cap has a current Company Intelligence record —
   restated against current `caps.clusters` membership, not the membership in force when `PI-0031` was
   filed.** (As of this filing: `semis` — ASML, TSM, NVDA, AVGO, KLAC — fully covered; `power_infra` —
   ETN, GEV, PWR — fully covered; `oil` — `tickers: []`, no current members, so no coverage question
   currently applies. **WDC is no longer a `semis`-cluster member and its coverage status has no bearing
   on this criterion** — WDC's existing Company Intelligence record, produced under `PI-0032`, is
   unaffected and unedited by this decision; see §F.)

**Criteria 4-7 of `PI-0031` §K are restated below for completeness, unedited in substance, not
independently re-verified by this filing (out of this filing's authorized scope — see §H):**

4. Every remaining uncovered canonical equity company is covered, explicitly deferred by accepted
   authority with rationale, or assigned to an approved alternative research architecture. **As of this
   filing, this is satisfied for all 8 previously-uncovered canonical names** — 4 by this decision's own
   new dispositions (§D), 4 by `PI-0033`'s existing, reaffirmed dispositions (§E). This filing does not
   independently re-verify whether any *other*, non-canonical consideration bears on criterion 4 — none
   is known to.
5. No unresolved MATERIAL research-coverage finding remains. **Carried forward from `PI-0031` §K
   unchanged — CRM's and IBM's residual MINOR findings and the universal 90-day freshness-cadence NOTE
   remain recorded as open, non-blocking, and outside this filing's scope; this filing does not
   re-verify their current status.**
6. Coverage indexes, freshness records, and `operations/WORKSTREAMS.yaml` are synchronized. **Not
   independently re-verified in full by this filing** beyond the narrow WS-0005 Milestone 3 gate fields
   this filing itself touches (§I) — a broader synchronization pass is explicitly out of scope (§H).
7. Every completed record has passed the required independent review, merge, and post-merge verification
   lifecycle, per `OPS-0007` §3's PROVISIONAL definition, applied per record. **Not independently
   re-verified per record by this filing** — that is a Lane M synchronization task explicitly deferred
   (§H).

### D. Four new gated-name dispositions (SNPS, ICE, SPGI, WM)

Each entry states, individually: current canonical role and materiality; deferral reason; and the exact
reopening condition, transcribed verbatim from that ticker's own `gates.yaml` `next_gate` field — no
generic trigger substituted for company-specific reasoning, matching `PI-0033`'s own discipline for its
fourteen dispositions.

1. **SNPS** (canonical equity, `target_pct: 2.50`, gated). *Materiality*: the second-largest canonical
   target weight among the four newly dispositioned names — a name whose eventual coverage, once
   un-gated, would be a materially sized addition to the record. *Deferral reason*: SNPS is
   actionable-gated under `PHQ-2026-01` (`status: cash_pending_clearance`) — its destination weight is
   never bought while gated, and no Company Intelligence research is authorized ahead of the evidence the
   gate's own review condition calls for; committing research effort now would front-run exactly the
   September 2026 Investor Day and valuation-model evidence the gate itself is waiting on. *Reopening
   trigger*: exactly `gates.yaml`'s own SNPS `next_gate` text — **"Review after September 30, 2026
   Investor Day and a fresh normalized valuation model."** This decision does not change, activate, or
   advance that gate; it only defers Company Intelligence coverage to the same evidentiary trigger.
2. **ICE** (canonical equity, `target_pct: 1.25`, gated). *Materiality*: a mid-sized canonical target
   weight; a financial-exchange/market-infrastructure name with no existing Company Intelligence coverage
   or prior batch mention. *Deferral reason*: actionable-gated under `PHQ-2026-01`; the gate's own
   `next_gate` condition names a transaction financing/integration review that substantially overlaps
   what a Company Intelligence record's business-model and capital-allocation sections would need to
   establish — researching ahead of that review risks producing a record before the exact facts the gate
   itself is waiting on are known. *Reopening trigger*: exactly `gates.yaml`'s own ICE `next_gate` text —
   **"Review official Q2 package and transaction financing/integration assumptions before initiation."**
3. **SPGI** (canonical equity, `target_pct: 1.25`, gated). *Materiality*: a mid-sized canonical target
   weight; a ratings/index/analytics name with no existing Company Intelligence coverage. *Deferral
   reason*: actionable-gated under `PHQ-2026-01`; the gate's own `next_gate` condition names a post-spin
   valuation comparison that is itself a precondition for a defensible business-model assessment — a
   Company Intelligence record drafted before "one clean post-spin quarter" of financials exist would
   rest on an incomplete post-spin picture. *Reopening trigger*: exactly `gates.yaml`'s own SPGI
   `next_gate` text — **"Review one clean post-spin quarter and normalized SPGI-versus-MSCI valuation,
   leverage, and growth comparison."**
4. **WM** (canonical equity, `target_pct: 0.75`, gated). *Materiality*: the smallest canonical target
   weight among the four; a waste-management/environmental-services name with no existing Company
   Intelligence coverage. *Deferral reason*: actionable-gated under `PHQ-2026-01`; the gate's own
   `next_gate` condition requires the complete Q2 2026 earnings package, which has not yet been retrieved
   or modeled — drafting a Company Intelligence record ahead of that package would either omit the
   most-current financial evidence or duplicate the gate's own review work out of sequence. *Reopening
   trigger*: exactly `gates.yaml`'s own WM `next_gate` text — **"Retrieve and model the complete Q2 2026
   earnings package and update valuation."**

**Common note, all four**: none of these four dispositions changes, narrows, expands, or reinterprets
`gates.yaml` in any way — the gate entries, their `status`, `authority`, `allow_add`, and `next_gate`
text remain exactly as `PHQ-2026-01`/`PHQ-2026-02` left them. This decision only records that Company
Intelligence coverage for these four names is deferred, and states the same evidentiary condition the
gate itself already names as the reopening trigger — a company-specific reason for each, not a uniform
placeholder, per `PI-0033`'s own established discipline.

### E. Reaffirmation of PI-0033's existing dispositions (GNRC, RTX, RKLB, TSLA)

**This section reaffirms, without editing, reopening, or in any way altering, `PI-0033` §A's existing
dispositions for GNRC (§A.2), RTX (§A.7), RKLB (§A.11), and TSLA (§A.12).** Each of these four names is a
current canonical `destination:` equity row; each already carries its own company-specific materiality
assessment, deferral reason, and reopening trigger, filed under the retired `band`/`spec` tier labels but
naming the same tickers the canonical architecture still contains at the same target rows (GNRC 1.25%,
RTX 0.75%, RKLB 0.50% — gated, TSLA 0.50% — gated). **No new fact, trigger, or rationale is added here
beyond what `PI-0033` already established.** This section exists solely so this decision's own
27-name canonical accounting is complete without requiring a future reader to cross-reference `PI-0033`
separately to see why these four carry no new disposition here. `PI-0033`'s own text, `status: Accepted`,
and every reopening trigger it states for these four names remain fully controlling, exactly as filed.

### F. Treatment of the 26 off-roster Company Intelligence records

The 26 Company Intelligence records for tickers no longer present in `targets.yaml`'s canonical
`destination:` list — AAPL, ABBV, AMAT, AMD, BRK.B, CRM, CRWD, CVX, GILD, IBM, INTC, JNJ, JPM, LRCX, MA,
MLM, MRK, MRVL, MU, NOW, ORCL, SKHY, VRT, WDC, WMT, XOM — are classified, effective on this decision's
merge, as:

- **Retained** — no record is deleted, archived out of `intelligence/companies/`, or moved.
- **Historical/advisory** — each record continues to state whatever it already states about the company
  it covers; none is asserted to be stale, wrong, or superseded by this classification alone.
- **Non-current for Milestone 3 completion accounting** — none of the 26 counts toward, or is required
  by, `PI-0031` §K's completion criteria as restated in §C above, because none corresponds to a current
  canonical `destination:` equity row. Their prior relevance (T1/T2 membership, `semis`/`oil`-cluster
  membership under the pre-`PHQ-2026-02` structure) is historical fact, not a current governance
  requirement.

**This decision edits, deletes, relabels, or rewrites none of the 26 records.** Every one of their
`.yaml`/`.md` pairs, freshness-registry rows, and freshness-checkpoint rows remains exactly as it was
immediately before this filing. Nothing in this classification implies any of the 26 companies is no
longer worth holding, tracking, or eventually reconciling against a future roster change — it states only
that their coverage is not, and was never claimed to be, a requirement of `targets.yaml`'s current
canonical architecture, and records that fact so a future reader does not mistake their continued
presence in `intelligence/companies/` for an unmet current-roster gap.

### G. Milestone 3 completion boundary

**Milestone 3 remains in progress after this governance filing. This decision does not declare it
complete, evaluate it as complete, or advance it toward completion beyond materially closing criteria
1-4 as restated in §C.** Criteria 5, 6, and 7 are restated for completeness in §C but are explicitly
**not** independently re-verified by this filing — a future, separate completion-determination decision
must evaluate all seven criteria together, freshly verified against live state at that time, before
Milestone 3 may be marked `complete`. Accounting for all 27 canonical equity names (§B) is a necessary
input to that future evaluation, not a substitute for it.

### H. Scope authorized

This decision's own implementation — the governance PR itself — touches exactly:

1. `governance/decisions/PI-0035-ws0005-milestone3-roster-reconciliation-and-gated-name-disposition.md`
   (this file).
2. `governance/decisions.yaml` (index regeneration: one new entry, `PI-0035`).
3. `operations/WORKSTREAMS.yaml` — the smallest directly related WS-0005 Milestone 3 gate fields needed
   to record this decision's existence and its narrow effect (the four new gated-name dispositions, the
   `PI-0033` reaffirmation, and the restated criteria 1-3) — **not** a broader historical catch-up of the
   register's other stale fields.
4. One `CLAUDE.md` Decisions Log entry recording this decision.

### I. Scope explicitly not authorized

- **No research of any kind** for SNPS, ICE, SPGI, WM, or any other ticker.
- **No gate change** — `gates.yaml`'s six entries, their `status`, `authority`, `allow_add`, and
  `next_gate` text are unchanged; no gate is activated, narrowed, or reinterpreted.
- **No tier, target, role, cluster, cap, or portfolio-role change** — `targets.yaml` is unchanged.
- **No cash or margin handling change** — `holdings.yaml`, `margin_state.py`, and every margin parameter
  are unchanged.
- **No Company or Theme Intelligence record edit** — none of the 19 covered, 26 off-roster, or any other
  existing record is modified.
- **No freshness record or monitoring change** — `intelligence/freshness_registry.yaml` and
  `intelligence/freshness_checkpoints.yaml` are unchanged; no new row is added for SNPS, ICE, SPGI, or WM
  (a gated-and-deferred name does not enter monitoring infrastructure any more than an unresearched one
  does).
- **No Intelligence schema or validator change** — `docs/PORTFOLIO_INTELLIGENCE_SPEC.md`,
  `intelligence_validator.py`, and `freshness_validator.py` are unchanged.
- **No dashboard code change.**
- **No test change** beyond what governance-validation/decision-index consistency already requires (none
  is expected — this filing adds no new schema or field).
- **No broad `operations/WORKSTREAMS.yaml` historical catch-up** — every other stale field in the
  register (e.g. any residual `PHQ-2026-04`/`PHQ-2026-05` status language) is explicitly out of scope,
  deferred to its own future, separately authorized Lane M synchronization pass.
- **No activation of any gated name; no buy, trim, exit, target, tier, or margin recommendation; no
  brokerage query; no order placed or simulated.**
- **No declaration that Milestone 3 is complete, and no advancement of Milestone 4 or any later
  milestone.**
- **No merge, and no marking this PR ready for review, by this session.**

## Rationale

**Why this reconciliation is filed now, as its own decision.** `PHQ-2026-02` (2026-07-31) retired the
entire tiered roster structure `PI-0031` §K's completion criteria were written against, three days after
`PI-0031`/`PI-0032`/`PI-0033` were filed and merged. No accepted decision has yet reconciled WS-0005
Milestone 3's own completion accounting against the roster that now actually governs the account — a gap
a future reader evaluating Milestone 3 completion would otherwise have to silently paper over or
re-derive from scratch. Reconciling it now, narrowly, prevents that gap from compounding as further
Milestone 3 work proceeds.

**Why SNPS, ICE, SPGI, and WM specifically, and why now.** These four are the only canonical equity
names with neither a Company Intelligence record nor any disposition of any kind on record — a gap
created by `PHQ-2026-02`'s roster migration, since none of the four was part of the tiered roster any
prior Milestone 3 filing accounted for. Leaving them undispositioned would leave criterion 4 (as restated
in §C) genuinely unmet, unlike GNRC/RTX/RKLB/TSLA, which already carry `PI-0033` dispositions that simply
needed reaffirming against the new roster.

**Why each gated name's own `next_gate` text as the reopening trigger, not a generic one.** `PI-0033`
already established that a uniform trigger across structurally different companies states nothing a
future reader could act on. For a gated name, the gate's own `next_gate` condition is not merely
analogous to a company-specific trigger — it is the literal evidentiary condition the account's own
policy has already named for that ticker, making it the most defensible, least-invented choice of
reopening condition available. Using it also avoids inventing a second, parallel evidentiary standard for
the same four tickers.

**Why criteria 1 and 2 collapse into one restated criterion rather than two.** `PI-0031` §K's original
criteria 1 and 2 differed only by which tier (T1 vs. T2) a name belonged to. `targets.yaml`'s canonical
`destination:` list has no tier concept at all — every equity row carries its own explicit `target_pct`
and no tier label. Preserving two criteria that would now differ by nothing meaningful would restate the
same underlying requirement (a canonical equity name has coverage or an accepted deferral) twice under
a distinction that no longer exists.

**Why criteria 4-7 are restated but not re-verified.** The principal's own scope for this filing excludes
a broad `operations/WORKSTREAMS.yaml` historical catch-up and any correction to `PHQ-2026-04`/
`PHQ-2026-05` status fields — both are Lane M mechanical-synchronization work for a later, separately
authorized pass. Restating criteria 4-7 for completeness (so this decision's own §C is a complete
seven-criterion picture, not a silent partial one) is different from re-verifying their current truth,
which this filing does not claim to have done.

**Why `PI-####`, not a new `OPS-####`.** Same category and reasoning as every prior Milestone 3 filing:
this is Company Intelligence coverage-accounting and disposition content (`category: portfolio_intelligence`),
filed in the `PI-####` series per `governance/decisions/README.md`'s convention.

**Why the 26 off-roster records are classified, not touched.** `PI-0031`/`PI-0032`/`PI-0033`'s own
never-edit-after-`Accepted` convention, and this repository's general discipline of never modifying an
existing Company Intelligence record without its own separate, later, explicit authorization, both
counsel leaving all 26 exactly as they are. Classifying them (retained, historical/advisory, non-current
for Milestone 3 accounting) closes the accounting question — whether they count toward the current
denominator — without touching their content.

## Alternatives Considered

- **Edit `PI-0031` §K's text directly to reflect the new roster.** Rejected —
  `governance/decisions/README.md` forbids editing a decision's substance after `status: Accepted`;
  narrow supersession via a new decision, exactly as `OPS-0003`/`OPS-0005`/`OPS-0007` already did for
  their own narrow-supersession cases, is the correct instrument.
- **Fold this reconciliation into a future Milestone 3 completion-determination decision instead of
  filing it separately now.** Rejected — the roster/criteria mismatch is a standing, present-tense
  accuracy problem independent of when completion is ultimately evaluated; leaving it unreconciled would
  let every intervening filing keep citing an obsolete anchor.
- **Treat SNPS/ICE/SPGI/WM as requiring a `PI-0033`-style fourteen-name-style batch disposition filing of
  their own, separate from this reconciliation.** Rejected — bundling their disposition with the roster
  reconciliation that surfaced them in the first place is more legible than a third, freestanding filing
  for the same four names discovered by this same accounting exercise.
- **Perform the broad `operations/WORKSTREAMS.yaml` historical catch-up and the `PHQ-2026-04`/
  `PHQ-2026-05` status corrections in this same filing, since they were also noticed during preflight.**
  Rejected per the principal's explicit instruction — those are Lane M mechanical-synchronization items
  for a later, separately authorized pass, and bundling them here would expand this filing's authorized
  scope beyond the narrow reconciliation it is meant to perform.
- **Declare Milestone 3 complete now that all 27 canonical names are accounted for.** Rejected —
  criteria 5-7 have not been independently re-verified by this filing, and `PI-0031` §K itself requires
  all seven criteria evaluated together by a dedicated future decision, not inferred from criteria 1-4
  alone.

## Consequences

**Authorized, effective on this decision's merge:** narrow supersession of `PI-0031` §K's completion
criteria 1-3 (§C); four new Company Intelligence coverage dispositions for SNPS, ICE, SPGI, and WM, each
deferred to its own `gates.yaml` reopening condition (§D); explicit reaffirmation, unedited, of `PI-0033`'s
GNRC, RTX, RKLB, and TSLA dispositions (§E); and classification of the 26 off-roster Company Intelligence
records as retained/historical-advisory/non-current for Milestone 3 accounting (§F).

**Unchanged by this decision:** every existing tier, target, role, cluster, cap, gate, and holding in
`targets.yaml`/`gates.yaml`/`holdings.yaml`; every existing Company/Theme Intelligence record, all 45 of
them, including every one of the 19 covered canonical names and every one of the 26 off-roster names;
`allocate.py`, `margin_state.py`, `intelligence_validator.py`, `intelligence_report.py`, every freshness
module, and every existing test; the 1.8x leverage cap and 30% buffer floor; `PI-0031`'s and `PI-0033`'s
own accepted text and scope, in full, unedited, other than the narrow §C supersession stated above;
`docs/PORTFOLIO_INTELLIGENCE_SPEC.md`, `docs/INVESTMENT_ONTOLOGY.md`, and
`constitution/INVESTMENT_CONSTITUTION.md`. Milestones 4-9 of WS-0005 remain entirely unauthorized, and
`OPS-0007` §8 step I is neither begun nor advanced by this filing. **No tenth (or later-numbered)
Milestone 3 batch is authorized by this filing, and none is inferred from its acceptance.**

**No research has been conducted, and no research finding, ranking, score, gate activation, or automatic
implementation is authorized or implied by this decision alone.** No investment recommendation is made or
implied. Milestone 3 remains `in_progress`; this decision does not declare it complete and does not
itself evaluate `PI-0031` §K's criteria 5-7. Any future research on SNPS, ICE, SPGI, WM, GNRC, RTX, RKLB,
TSLA, or any of the 26 off-roster names requires its own separate, later, explicit governance decision,
naming that company specifically.

### Required independent review, principal-acceptance gate, and stopping condition

- **This governance PR must remain in draft state** and must not be marked ready for review or merged by
  this session.
- **An eligible independent review is required**, anchored to this PR's exact final head, per `OPS-0007`
  §1's twelve-point capability-based standard — no self-review by the authoring session.
- **Any material (Blocking or Major) finding from that review requires a bounded correction and an
  exact-head re-review** before the PR may be considered ready, per `OPS-0009` §6's four-condition
  delta-review test; any doubt defaults to a full re-review, per `OPS-0009` §10.
- **Explicit principal acceptance is required before merge**, at the exact head being merged.
- **This decision does not mark itself, or authorize marking itself, ready for merge.** It becomes
  effective — including the four gated-name dispositions in §D and the criteria restatement in §C — only
  on this governance PR's own merge to `main`.
- **Stopping condition, controlling over any contrary inference**: this session's own authorized scope
  ends at opening this draft PR and reporting its exact head. No independent review, no correction pass,
  no re-review, no merge, and no post-merge verification is performed by this session — each is a
  separate future step requiring a separate actor per `OPS-0009` §§7-9's KEEP/START NEW/SESSION DONE and
  role-bounded-mechanical-action discipline.

**No current portfolio policy or allocator behavior changes as a result of this decision, before or after
its merge.** `allocate.py`'s buy/trim/gap logic, every gate parameter, every cap, every target weight, and
every margin parameter remain exactly as `targets.yaml`/`gates.yaml`/`holdings.yaml` currently state them,
unaffected by this filing under any circumstance.
