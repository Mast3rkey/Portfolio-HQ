# Portfolio Validation Governance Review

> **⚠️ Governance review only — grants no implementation authorization.** Per `docs/PORTFOLIO_DATA_WORKSTREAM_CHARTER.md`. This document determines, for each of the 14 candidates `docs/PORTFOLIO_INPUT_VALIDATION_ASSESSMENT.md` classified **Potentially in scope**, whether the repository's evidence is mature enough to justify a *future* implementation proposal. It does not write, authorize, schedule, or rank any implementation. `docs/PORTFOLIO_DATA_WORKSTREAM_CHARTER.md`, `docs/PORTFOLIO_INPUT_INVENTORY.md`, `docs/PORTFOLIO_INPUT_INVARIANTS.md`, and `docs/PORTFOLIO_INPUT_VALIDATION_ASSESSMENT.md` are frozen and unmodified by this document.

_Written 2026-07-17. Inputs used: the repository (`allocate.py`, `margin_state.py`, `targets.yaml`, `holdings.yaml`, `alpaca_client.py`, re-checked directly where a claim required it), the four Portfolio Data Workstream documents, `CLAUDE.md` (Decisions Log and Guardrails), and `docs/PHASE5B_GOVERNANCE_DECISION.md` (as the structural precedent for what a governance document in this project looks like — not as a subject being reopened). No outside reasoning, general software-engineering convention, or claim not traceable to one of these sources appears below._

---

## Decision rule (restated, applied strictly)

An item is classified **Ready for future proposal** only if **all six** hold:

1. Verifies an existing factual invariant (not a newly-invented one).
2. Cannot influence investment judgment.
3. Does not alter allocation logic (which BUY/TRIM/BLOCKED decisions occur, or their dollar amounts).
4. Does not alter governance (doctrine, `targets.yaml` policy values, margin rules).
5. Requires no unresolved evidence.
6. Has a clearly defined scope (the fact to verify is unambiguous, even though *how* to enforce it is deliberately left unspecified per the Assessment's own "do not propose implementation details" constraint).

If any criterion is unmet, the item is **Needs additional evidence** (the gap is specific and potentially closeable) or **No further action recommended** (the gap is not closeable by more evidence, or the underlying invariant itself is not actually established). The default is not Ready — each item below states explicitly why it does or does not clear all six.

**Distinction used throughout:** an enforcement that *detects and surfaces* a violation (a warning, an error string, an abort-pending-confirmation prompt — the same shape as the already-approved `BOOK_CHANGE_WARN_PCT`/`STALE_MARGIN_DAYS` precedents already live in `allocate.py`) is treated as compatible with criterion 3; an enforcement that would *auto-correct* a violation (silently resolve a duplicate ticker, silently exclude a stale-priced ticker from buy candidacy) would change allocation logic and is explicitly out of scope for every candidate below — this boundary is restated per-item where the risk of drifting into auto-correction is non-obvious.

---

## Candidate reviews

### 1. Tier uniqueness (a ticker should not appear in more than one tier's `tickers` list)

1. **Existing invariant:** each roster ticker belongs to exactly one tier.
2. **Current evidence:** `docs/PORTFOLIO_INPUT_INVARIANTS.md` item 1b/4 — confirmed via direct trace of `build_roster()`'s dict-overwrite behavior (allocate.py:63) and YAML key order (T1, T2, ETF, band, spec).
3. **Existing enforcement:** none. Violation handling classified Silent in the invariants document.
4. **Why Assessment classified it Potentially in scope:** a uniqueness check verifies a structural fact about `targets.yaml`'s own internal consistency; it makes no claim about which tier a ticker *should* be in.
5. **Enforcing it would:** verify an existing invariant only. Would not change allocator behavior for any non-violating config (the overwhelming majority case). Would not change allocator outputs beyond a detection message. Introduces no judgment. Requires no new external data.
6. **Operational impact if implemented:** none for a correctly-specified roster (the current live `targets.yaml`, read directly for this review, contains no duplicate ticker across tiers — confirmed by scanning all five tier lists). Impact is limited to catching a future data-entry error at the moment it's introduced rather than after an unknown delay.
7. **Maintenance impact:** minimal — a single structural check against config already loaded into memory every run; no new data source, no new dependency.
8. **Failure mode if implemented incorrectly:** a check that silently reassigns the ticker to a "resolved" tier (rather than only detecting and reporting) would cross into altering allocation logic — this is the auto-correction risk named in the decision-rule preamble, not a risk inherent to the invariant itself.
9. **Governance recommendation: Ready for future proposal.** All six criteria hold on direct evidence; no unresolved question remains.

### 2. Crypto sleeve price-source completeness

1. **Existing invariant:** every `crypto.coins` entry resolves to a price via Alpaca or `coingecko_ids`.
2. **Current evidence:** `docs/PORTFOLIO_INPUT_INVARIANTS.md` item 2 and `docs/PORTFOLIO_INPUT_VALIDATION_ASSESSMENT.md` item 2 — confirmed via `resolve_holdings()`'s silent-drop filter (allocate.py:140) and `fetch_crypto()`'s routing logic (crypto.py:59-85).
3. **Existing enforcement:** partial — a per-coin fetch failure is Detected (shown as `n/a (error)` in `render()`); the aggregate sleeve-total consequence is Silent.
4. **Why Assessment classified it Potentially in scope:** a completeness check verifies a config-vs-coverage fact, not a market view.
5. **Enforcing it would:** verify an existing invariant only, in principle. However, direct re-reading of `targets.yaml`'s current `crypto` block shows `coingecko_ids: {}` (empty) while `coins: [BTC, ETH, SOL]` — all three currently rely on Alpaca coverage, and an *empty* `coingecko_ids` is today's entirely correct, working configuration, not a violation. This means "every coin resolves to a source" is not, on its own, a crisp binary fact to check at config-load time — a coin's absence from `coingecko_ids` is only meaningful in combination with an *actual, observed* Alpaca fetch failure, which is a runtime condition, not a static config fact. The candidate as described conflates a static completeness check with a runtime aggregate-flagging behavior.
6. **Operational impact if implemented:** currently unknowable precisely because the exact fact being verified is underspecified — see point 5.
7. **Maintenance impact:** unknown until the specific fact is defined.
8. **Failure mode if implemented incorrectly:** a check that flags today's correct, working `coingecko_ids: {}` configuration as an error would be a false positive against a currently-valid state — direct evidence this ambiguity is real, not hypothetical.
9. **Governance recommendation: Needs additional evidence.** Criterion 6 (clearly defined scope) is not met — the repository does not currently make clear whether the invariant is "every coin has a *configured* source" (which today's valid config violates) or "every coin resolves to a price *at runtime*" (already partially Detected). This distinction needs to be resolved before a proposal could define what it's actually verifying.

### 3. `coingecko_ids` routing completeness (distinguish "not configured" from "fetch failed")

1. **Existing invariant:** a coin's routing outcome should be distinguishable from an unrelated API outage in the displayed error.
2. **Current evidence:** `docs/PORTFOLIO_INPUT_INVARIANTS.md` item 3 — confirmed via `fetch_crypto()`'s routing logic (crypto.py:67).
3. **Existing enforcement:** none — both failure modes currently render as the same generic error shape.
4. **Why Assessment classified it Potentially in scope:** distinguishing two failure causes in an error message verifies a fact (which code path failed), not a market view.
5. **Enforcing it would:** verify an existing invariant only — but this candidate shares item 2's underlying ambiguity: since an empty/absent `coingecko_ids` entry is today's valid, intentional state for Alpaca-covered coins, "distinguishing" the two cases requires first defining what "not configured" is even supposed to mean as a distinct, flaggable condition, versus simply "this coin uses Alpaca, as intended."
6. **Operational impact if implemented:** unknown until the underlying scope question (shared with item 2) is resolved.
7. **Maintenance impact:** unknown until scope is resolved.
8. **Failure mode if implemented incorrectly:** same false-positive risk as item 2 — could mislabel a coin's intentional Alpaca routing as a "missing configuration."
9. **Governance recommendation: Needs additional evidence.** Same underlying gap as item 2 (criterion 6 not met) — this candidate should not be evaluated independently of item 2's resolution, since both rest on the same unresolved definitional question.

### 4. `weight_pct` non-negativity

1. **Existing invariant:** tier weight percentages should be within a sane numeric range (non-negative, at minimum).
2. **Current evidence:** `docs/PORTFOLIO_INPUT_INVARIANTS.md` item 5 — confirmed via `float(tier.get("weight_pct", 0))` (allocate.py:59) accepting any float with no bound.
3. **Existing enforcement:** none.
4. **Why Assessment classified it Potentially in scope:** a sign/range check on a numeric config value verifies a fact about the value's plausibility, not its "correctness" as an investment choice — the Assessment separately and explicitly rejected a "sum to 100%" version of this invariant (item 5b) as unsupported by evidence; this narrower non-negativity version was preserved specifically because it does not carry that same unsupported premise.
5. **Enforcing it would:** verify an existing invariant only (a percentage representing an allocation weight cannot be meaningfully negative under this system's design — no short-selling or negative-weight mechanic exists anywhere in `allocate.py`, `targets.yaml`, or `CLAUDE.md`'s doctrine). No allocation-logic change for any currently-valid config (every `weight_pct` in the live `targets.yaml`, re-read for this review, is positive). No judgment, no external data.
6. **Operational impact if implemented:** none for the current config; catches a future typo (e.g., a missing decimal point turning `3.35` into `-3.35` via some future edit) at config-load time.
7. **Maintenance impact:** minimal — a single numeric-range check.
8. **Failure mode if implemented incorrectly:** a check that also tried to enforce an upper bound or a sum constraint would reintroduce item 5b's already-rejected unsupported premise — the scope must stay limited to non-negativity specifically.
9. **Governance recommendation: Ready for future proposal.** All six criteria hold; the scope is narrower than, and does not reintroduce, the already-rejected item 5b premise.

### 5. `cap_multiple >= 1.0` (band tier)

1. **Existing invariant:** a tier's overweight ceiling multiplier should not sit below 1.0 (a ceiling below the target it caps is self-contradictory).
2. **Current evidence:** `docs/PORTFOLIO_INPUT_INVARIANTS.md` item 6 — confirmed via `plan()`'s use of `cap_multiple` in both the overweight-trim check and the buy-ceiling computation (allocate.py:214-215, 267-268).
3. **Existing enforcement:** partial — `max(0.0, name_ceiling - current)` (allocate.py:271) prevents a *negative allocation* but not the underlying misconfiguration.
4. **Why Assessment classified it Potentially in scope:** the relationship "a ceiling multiplier should be >= 1.0" follows directly and unambiguously from the multiplier's own stated purpose (a ceiling *above* target) in `targets.yaml`'s own comment ("band positions may run up to 1.25x target").
5. **Enforcing it would:** verify an existing invariant only, directly supported by the config file's own documentation of what this field means. No allocation-logic change for the current, valid value (1.25). No judgment, no external data.
6. **Operational impact if implemented:** none for the current config; would catch a future misconfiguration at config-load time rather than allowing it to silently produce a below-target ceiling.
7. **Maintenance impact:** minimal.
8. **Failure mode if implemented incorrectly:** none identified beyond the general auto-correction risk in the decision-rule preamble.
9. **Governance recommendation: Ready for future proposal.** All six criteria hold, directly supported by the field's own documented purpose.

### 6. `fixed`/`cap_multiple` self-consistency (spec tier)

1. **Existing invariant (candidate):** a tier marked `fixed: true` should also have `cap_multiple` unset or equal to 1.0.
2. **Current evidence:** `docs/PORTFOLIO_INPUT_INVARIANTS.md` item 7 states this relationship directly: "this relationship is nowhere stated" as a rule — it is an *observed coincidence* in the current `spec` tier's configuration (both fields independently happen to produce the same ceiling behavior today), not a documented design requirement.
3. **Existing enforcement:** none.
4. **Why Assessment classified it Potentially in scope:** the Assessment treated this as a config self-consistency check; on closer review for this governance pass, the premise itself does not meet criterion 1.
5. **Enforcing it would:** not clearly verify an *existing* invariant, because no such invariant is established anywhere in this repository — `targets.yaml`, `allocate.py`, and `CLAUDE.md` are all silent on whether `fixed` and `cap_multiple` are intended to be linked at all, versus two independently meaningful fields that merely happen to coincide for `spec` today.
6. **Operational impact if implemented:** unknown — enforcing an unestablished rule risks flagging a future, intentional reconfiguration (e.g., a deliberate decision to give a `fixed` tier a distinct `cap_multiple` for some purpose not yet used anywhere) as an error, when no evidence shows that combination is actually disallowed.
7. **Maintenance impact:** N/A pending resolution of point 5.
8. **Failure mode if implemented incorrectly:** would encode a rule that isn't actually part of this system's design, function as an unapproved doctrine addition through the back door of a "validation" check.
9. **Governance recommendation: No further action recommended.** Criterion 1 is not met — this is not a case of insufficient evidence about a fact; it's a case where re-review shows the candidate rests on a relationship this repository has never actually established as an invariant at all. Pursuing it further would not be resolved by gathering more evidence about the *current* config (already fully known) — it would require a *new doctrine decision* about whether such a rule should exist, which is out of this workstream's charter (a judgment/doctrine question, not an input-fidelity one).

### 7. `crypto.sleeve_pct` sane numeric range

1. **Existing invariant:** the crypto sleeve percentage should be within a sane range (non-negative, at minimum).
2. **Current evidence:** `docs/PORTFOLIO_INPUT_INVARIANTS.md` item 8 — same structure as item 5 (weight_pct), confirmed via `float(crypto_cfg.get("sleeve_pct", 0))` (allocate.py:326) accepting any float.
3. **Existing enforcement:** none.
4. **Why Assessment classified it Potentially in scope:** same reasoning as item 4 — a narrow sign/range check, not a value judgment about the "correct" sleeve size.
5. **Enforcing it would:** verify an existing invariant only. No allocation-logic change for the current, valid value (10.0, re-confirmed by direct read of `targets.yaml`). No judgment, no external data.
6. **Operational impact if implemented:** none for the current config.
7. **Maintenance impact:** minimal.
8. **Failure mode if implemented incorrectly:** none beyond the general auto-correction risk.
9. **Governance recommendation: Ready for future proposal.** Same evidentiary basis and reasoning as item 4; all six criteria hold.

### 8. Cluster ticker ⊆ roster consistency

1. **Existing invariant:** every ticker in a cluster's `tickers` list also appears in some tier's roster list.
2. **Current evidence:** `docs/PORTFOLIO_INPUT_INVARIANTS.md` item 10 — confirmed via direct trace: `plan()` computes `tk_clusters` from the roster loop's own view (allocate.py:208), with no reverse check.
3. **Existing enforcement:** none.
4. **Why Assessment classified it Potentially in scope:** a purely structural cross-reference between two already-existing, already-loaded config lists (`caps.clusters[].tickers` and the five tier lists) — no new data, no judgment about cluster membership correctness.
5. **Enforcing it would:** verify an existing invariant only. Direct re-check of the live `targets.yaml` confirms every ticker in every cluster (`semis`, `power_infra`, `oil`) does currently appear in some tier list — the check would not change any current output. No judgment, no external data.
6. **Operational impact if implemented:** none for the current config; would catch a future edit that removes a ticker from its tier list without also updating cluster membership (or vice versa).
7. **Maintenance impact:** minimal — a single set-membership check across already-loaded config.
8. **Failure mode if implemented incorrectly:** none identified beyond the general auto-correction risk (e.g., silently removing a ticker from a cluster's list rather than only flagging it).
9. **Governance recommendation: Ready for future proposal.** All six criteria hold, directly re-verified against the current live config.

### 9. Share/coin-count book-swing guard parity

1. **Existing invariant:** a large, unexplained book-value swing from a data-entry paste usually indicates a partial-paste error and should receive the same confirm-before-write treatment `update_holdings()` already applies.
2. **Current evidence:** `docs/PORTFOLIO_INPUT_INVARIANTS.md` item 12b/13b — confirmed via direct line-by-line comparison: `update_holdings()` has `BOOK_CHANGE_WARN_PCT` (allocate.py:602-613); `update_shares()`/`update_crypto_shares()` (allocate.py:622-659) have no equivalent.
3. **Existing enforcement:** already fully implemented and already-approved for one of the three sibling functions (`update_holdings()`), specifically *not* present for the other two.
4. **Why Assessment classified it Potentially in scope:** this candidate proposes applying an *already-approved, already-implemented* mechanism to sibling functions where the identical underlying assumption is stated (per `docs/PORTFOLIO_INPUT_INVARIANTS.md` item 12: "large changes are intentional") but left unguarded — not a new check design.
5. **Enforcing it would:** verify an existing invariant only, using an existing, already-governance-approved threshold (30%) and an already-existing code pattern. No new allocation logic (this only affects the `update-shares`/`update-crypto-shares` CLI write path, entirely separate from `plan()`'s allocation computation). No judgment. No external data — the check operates entirely on values already being written to `holdings.yaml`.
6. **Operational impact if implemented:** would make an unusually large share/coin-count paste require `--confirm`, exactly as an unusually large manual-dollar-value paste already does today — a direct behavioral parity, not a new behavior category.
7. **Maintenance impact:** minimal — the check pattern already exists in the codebase and would be applied a second and third time.
8. **Failure mode if implemented incorrectly:** a threshold value diverging from the existing 30% figure without justification would introduce an unexplained inconsistency between three functions meant to behave alike — the specific threshold value itself is not re-litigated by this recommendation, only the parity of applying *some* already-approved-shape check.
9. **Governance recommendation: Ready for future proposal.** All six criteria hold; this is the strongest-evidenced candidate in this set, since the enforcement pattern is not new — it already exists, already-approved, in a sibling function.

### 10. Share/coin quantity non-negativity

1. **Existing invariant:** entered share/coin quantities should not be negative — no short position is modeled anywhere in this system.
2. **Current evidence:** `docs/PORTFOLIO_INPUT_INVARIANTS.md` item 12c/13c — confirmed via `_parse_ticker_value_pairs()` (allocate.py:562-583) accepting any float including negative, with no downstream type check.
3. **Existing enforcement:** none.
4. **Why Assessment classified it Potentially in scope:** a sign check on a physical quantity (shares/coins held), not a market view — no code path anywhere in this project models or discusses a short position (confirmed by a search of `allocate.py`, `margin_state.py`, `CLAUDE.md`'s Portfolio Doctrine section, none of which reference shorting).
5. **Enforcing it would:** verify an existing invariant only. No allocation-logic change for the current, valid `holdings.yaml` (every entry re-checked is positive). No judgment, no external data.
6. **Operational impact if implemented:** none for current holdings; would catch a sign-flip data-entry error at the point of entry.
7. **Maintenance impact:** minimal.
8. **Failure mode if implemented incorrectly:** none identified.
9. **Governance recommendation: Ready for future proposal.** All six criteria hold; the "no shorting" premise is directly supported by the absence of any shorting mechanic anywhere in the codebase or doctrine.

### 11. `holdings` manual-value freshness signal

1. **Existing invariant (candidate):** a manually-pasted fallback dollar value should carry a freshness signal, the way `margin.synced_at`/`STALE_MARGIN_DAYS` already does.
2. **Current evidence:** `docs/PORTFOLIO_INPUT_INVARIANTS.md` item 14b — confirmed via direct read of `write_state()` (allocate.py:662-712) and `holdings.yaml`'s current schema: no `synced_at`-equivalent field exists for the `holdings:` block.
3. **Existing enforcement:** none for `holdings`; an equivalent, already-approved mechanism exists for `margin` specifically.
4. **Why Assessment classified it Potentially in scope:** this candidate proposes extending an already-approved pattern (age-based staleness signaling) to a second input, structurally identical to item 9's reasoning for the book-swing guard.
5. **Enforcing it would:** verify an existing invariant only (does this value have an age, and is that age within a sane bound), using an already-approved *pattern* (though not necessarily the same 2-day *threshold*, which is margin-specific per `STALE_MARGIN_DAYS`'s own naming — the Assessment's "do not propose implementation details" scope means this review does not attempt to fix a number here). No allocation-logic change (informational only, mirroring how the margin staleness warning is informational only, per `render()`'s existing structure). No judgment, no external data.
6. **Operational impact if implemented:** currently minimal in practice, since `holdings.yaml`'s `holdings:` block is presently empty (re-confirmed by direct read) — no ticker relies on this path today; the invariant remains real and evidenced regardless of the block's current emptiness, since the mechanism (SKHY historically, per `CLAUDE.md`'s Decisions Log) exists specifically for this fallback path when it *is* used.
7. **Maintenance impact:** minimal — would add one field and reuse an already-existing check pattern.
8. **Failure mode if implemented incorrectly:** none identified beyond needing its own threshold decision (a parameter, not a scope-defining fact) in the eventual proposal.
9. **Governance recommendation: Ready for future proposal.** All six criteria hold; the pattern is a direct structural analog to an already-approved sibling mechanism.

### 12. `min_lot_dollars` vs. the documented $25,000 book-size trigger

1. **Existing invariant:** `min_lot_dollars` should be revisited once the book crosses approximately $25,000.
2. **Current evidence:** `CLAUDE.md`'s Open Items section — states the exact trigger condition directly and explicitly: "revisit once the book crosses roughly $25,000... One-line bump in `targets.yaml` when that trigger hits; not needed now." This is the single most directly and explicitly documented invariant among all 14 candidates.
3. **Existing enforcement:** none — nothing in `allocate.py` checks the book's current size against this documented threshold.
4. **Why Assessment classified it Potentially in scope:** the fact to verify (current book size vs. an already-approved, already-quantified threshold) is fully specified in an existing doctrine document; enforcement would surface, not decide, the comparison.
5. **Enforcing it would:** verify an existing invariant only, using a threshold this workstream did not invent (`CLAUDE.md` did, separately, already). Would not itself change `min_lot_dollars` or any allocation decision — only surface a notice that the documented trigger condition has been met, leaving the actual revisit decision to the account holder, exactly as `CLAUDE.md`'s own phrasing ("revisit... when that trigger hits") frames it. No judgment, no external data (book size is already computed every run).
6. **Operational impact if implemented:** none today — the book (per `holdings.yaml`, re-read for this review: gross well under $10,000) is far below the $25,000 trigger; the check would be dormant until the account grows substantially.
7. **Maintenance impact:** minimal — a single comparison against an already-computed value (`book`) and an already-documented constant.
8. **Failure mode if implemented incorrectly:** a check that *automatically* adjusted `min_lot_dollars` upon crossing the threshold, rather than only notifying, would cross into altering governance (changing a `targets.yaml` policy value without an explicit human edit) — the candidate's scope must remain notification-only.
9. **Governance recommendation: Ready for future proposal.** All six criteria hold, with the strongest possible documentary support (a verbatim, pre-existing trigger condition in `CLAUDE.md` itself) of any candidate reviewed.

### 13. Market-open status at report-generation time

1. **Existing invariant:** the Alpaca price feed reflects only the regular 9:30am–4:00pm ET session and is frozen outside those hours — already documented doctrine (`CLAUDE.md`'s "Live-priced book" guardrail), not currently surfaced by the running code.
2. **Current evidence:** `docs/PORTFOLIO_INPUT_INVARIANTS.md` item 23 and `docs/PORTFOLIO_INPUT_VALIDATION_ASSESSMENT.md` item 23 — confirmed via direct read of `alpaca_client.py`: `get_clock()` (alpaca_client.py:87-88) already exists, already returns live market-open/closed status, and is confirmed **not called anywhere in `allocate.py`'s live workflow** (only in `alpaca_client.py`'s own `__main__` diagnostic block, re-verified by a direct grep of `allocate.py` for `get_clock` — zero matches).
3. **Existing enforcement:** none in the live workflow, despite the data source already existing and already being wired into the same client class every other call in this project already uses.
4. **Why Assessment classified it Potentially in scope:** surfacing an already-available, already-fetchable fact (is the market open right now) verifies a known limitation already documented elsewhere; it does not predict a price or recommend a trade.
5. **Enforcing it would:** verify an existing invariant only, using data this project's own client already provides. Would not change allocation logic (the buy/trim/block decisions themselves are unaffected — the Assessment already explicitly rejected, as Out of scope, the adjacent idea of *automatically excluding* a stale-priced ticker from buy candidacy; this candidate is narrower and stops at *displaying* the market-status fact). No judgment. No new external data — `get_clock()` is a zero-new-dependency call on the exact same authenticated client every other market-data call in this file already uses.
6. **Operational impact if implemented:** would add a single informational line/flag to the report (e.g., "market currently closed — prices as of last close") in the pre/post-market case; no impact during regular session hours.
7. **Maintenance impact:** minimal — one additional API call already supported by the existing client class, reusing an existing method rather than adding a new one.
8. **Failure mode if implemented incorrectly:** using this signal to *change* which tickers are eligible for a buy (rather than only labeling the report) would re-introduce the Assessment's already-rejected auto-exclusion idea — the scope must remain informational-only.
9. **Governance recommendation: Ready for future proposal.** All six criteria hold; notably, the data source already exists in the codebase and is simply unused, the strongest possible "no new external data" evidence of any candidate reviewed.

### 14. CLI argument non-negativity (`--cash`, `--margin`)

1. **Existing invariant:** deployable cash/margin request amounts represent real dollar figures and should not be negative.
2. **Current evidence:** `docs/PORTFOLIO_INPUT_INVARIANTS.md` item 34 — confirmed via direct read of `main()`'s `argparse` block (allocate.py:855-858): `type=float` performs no bounds check.
3. **Existing enforcement:** none.
4. **Why Assessment classified it Potentially in scope:** a sign check on a per-run numeric input, not a market view; the value is never persisted (confirmed: `args.cash`/`args.margin` flow only into `plan()`'s parameters for that single run, never written to `holdings.yaml` or `targets.yaml`).
5. **Enforcing it would:** verify an existing invariant only. No allocation-logic change for any sane invocation. No judgment, no external data.
6. **Operational impact if implemented:** minimal — would reject an obviously malformed command-line invocation (e.g., `--cash -500`) before it silently flows into `plan()`'s buying-power computation.
7. **Maintenance impact:** minimal — a single bounds check in `argparse` or immediately after.
8. **Failure mode if implemented incorrectly:** none identified — this is the lowest-blast-radius candidate reviewed, since a bad value here affects only the single run it was typed for, never persisted state.
9. **Governance recommendation: Ready for future proposal.** All six criteria hold.

---

## Repository-wide summary

| Governance recommendation | Count | Items |
|---|---:|---|
| Ready for future proposal | 11 | 1, 4, 5, 7, 8, 9, 10, 11, 12, 13, 14 |
| Needs additional evidence | 2 | 2, 3 |
| No further action recommended | 1 | 6 |

**Does the repository currently contain sufficient justification to begin any implementation work? No.** Eleven candidates clear all six decision-rule criteria on the evidence available today, which means they are appropriately positioned to become the *subject* of a future, separately-approved implementation proposal — it does not mean any of them may be implemented on the strength of this document. Per the charter's own decision boundaries (`docs/PORTFOLIO_DATA_WORKSTREAM_CHARTER.md` §11) and this document's own explicit scope, **a "Ready" classification is not an authorization** — it is a statement that the invariant is well-evidenced, narrowly scoped, and structurally incapable (as scoped) of introducing judgment or altering allocation logic or governance. A future proposal for any Ready item would still need to specify its own enforcement mechanics (warn vs. abort, exact threshold values where applicable) and pass its own review before any code is written.

Two candidates (2, 3) share a single underlying definitional gap — what "complete" means for a coin's price-source configuration, given that today's valid configuration includes coins with no `coingecko_ids` entry by design — and should not be pursued independently of resolving that shared question.

One candidate (6) is reclassified from the Assessment's "Potentially in scope" to this review's "No further action recommended" — not because new evidence contradicts the Assessment, but because closer review under the strict six-criterion test finds the candidate's premise (a `fixed`/`cap_multiple` consistency rule) was never actually established as an invariant anywhere in this repository; it was an *observed coincidence* in one tier's current config, and enforcing an unestablished rule would risk introducing a doctrine position through validation rather than verifying one that already exists.

---

## What this document deliberately does not do

- Does not authorize implementation of any candidate, including the 11 classified "Ready for future proposal."
- Does not write, sketch, or specify any validation code.
- Does not modify `allocate.py`, `targets.yaml`, `holdings.yaml`, `margin_state.py`, or any other production file.
- Does not modify any test.
- Does not modify `docs/PORTFOLIO_DATA_WORKSTREAM_CHARTER.md`, `docs/PORTFOLIO_INPUT_INVENTORY.md`, `docs/PORTFOLIO_INPUT_INVARIANTS.md`, or `docs/PORTFOLIO_INPUT_VALIDATION_ASSESSMENT.md`.
- Does not create a backlog, rank the 11 Ready items, or estimate engineering effort for any of them.
- Does not recommend a sequence or order in which candidates should be pursued — the table above lists items in their original candidate-set order, not by priority.
- Does not reopen `docs/PHASE5B_GOVERNANCE_DECISION.md` or any other closed governance decision, and does not reinterpret the band-overlay NO-GO verdict (`CLAUDE.md`'s Decisions Log, June 2026) — neither is referenced as a subject of re-examination anywhere above; `docs/PHASE5B_GOVERNANCE_DECISION.md` is cited only as a structural precedent for this document's own format.

Stopping here. This document's existence does not start an implementation phase — any next step requires its own separate, explicit approval, per the charter's decision boundaries.
