---
decision_id: PHQ-2026-05
date: 2026-07-31
status: Accepted
category: portfolio_construction_governance
related_decisions: [GOV-0001, GOV-0002, OPS-0001, OPS-0009, PHQ-2026-01, PHQ-2026-02, PHQ-2026-04]
supporting_artifact: governance/evidence/PHQ-2026-05/v1_37/Portfolio_HQ_Final_Confirmed_Account_State_v1_37.json
---

## Context

`PHQ-2026-02` reconciled `holdings.yaml` from the v1.35 evidence package.
Separately, `PHQ-2026-04` (this repository's other currently-open governance
PR, #205) records the principal's manual SKHY/SPCX exit, evidenced by
execution-fill facts (submitted 2026-07-31 15:10:57–15:11:27 ET, both filled,
both confirmed absent from the post-trade Positions screenshot, resulting
cash $2,675.05).

The principal has now supplied a further, later "Final Confirmed Account
State v1.37" package — a `MANIFEST.json` (with per-file SHA-256), a JSON
account-state export, a CSV holdings export, and a README — described as
"the final post-buy quantities shown in the principal-supplied mobile
holdings screenshots" after "all seven buy fills," with an `effective_time`
of "2026-07-31 approximately 16:13 ET." All three data files' SHA-256 hashes
were independently recomputed this session and matched the manifest exactly.

**Direct comparison against `holdings.yaml` as reconciled through
`PHQ-2026-04`** (i.e., after SKHY/SPCX removal) found exactly seven changed
or added `shares:` quantities and zero other equity/fund/crypto changes:

| Ticker | Pre-v1.37 | v1.37 confirmed | Change |
|---|---|---|---|
| AMZN | 0.423377 | 1.146551 | increased |
| NVDA | 0.986492 | 1.858992 | increased |
| TMO | 0.2038 | 0.325606 | increased |
| SPY | 0.25105 | 1.250856 | increased |
| PWR | (none) | 0.116807 | new |
| VEA | (none) | 6.186296 | new |
| VWO | (none) | 0.476555 | new |

All other tracked equities/funds (ASML, AVGO, CEG, COST, ETN, GEV, GLD,
GNRC, GOOGL, ISRG, KLAC, LLY, META, MSFT, PANW, RTX, TSM, V) and all crypto
(BTC, ETH, SOL) are identical between the pre-v1.37 state and the v1.37
package — independently confirmed by a full field-by-field diff, not
assumed. PWR, VEA, and VWO each already carry an existing canonical
`targets.yaml` destination row (1.25%, 7.00%, and 1.00% respectively) — this
filing introduces no new ticker, target, cap, or gate; it only updates share
counts for names the canonical architecture already governs.

**A material, unresolved conflict was found and escalated to the principal
before any file was edited**: the v1.37 package's own `positions` list still
includes SKHY (0.278473 sh) and SPCX (0.502727 sh) at their exact pre-exit
quantities, and its README/JSON both instruct to "preserve SPCX hold/no-add"
and "leave SKHY unresolved" — i.e., treats them as continuing holdings, not
exited. This directly contradicts `PHQ-2026-04`'s independently-evidenced
sale-fill facts. The v1.37 package's reported cash ($845.84) also does not
reconcile against `PHQ-2026-04`'s post-sale-only cash ($2,675.05), even after
accounting for the cost of the seven buy fills above. The principal was
asked directly and confirmed: **`PHQ-2026-04`'s SKHY/SPCX exit facts control;
v1.37's SKHY/SPCX rows and cash figure are treated as stale for those two
data points specifically.**

## Decision

**Accepted, bounded to exactly the seven-quantity reconciliation above:**

1. Updates `holdings.yaml`'s `shares:` block: AMZN, NVDA, TMO, SPY quantities
   updated to their v1.37-confirmed values; PWR, VEA, VWO added at their
   v1.37-confirmed quantities (new share-tracked positions, not new
   tickers to the canonical architecture — see table above).
2. Makes **no** change to SKHY or SPCX. Both remain exactly as `PHQ-2026-04`
   left them (removed from `holdings.yaml`/`targets.yaml`/`gates.yaml`, zero
   position, not restored). This filing does not reopen, edit, or
   second-guess `PHQ-2026-04`.
3. Makes **no** change to `targets.yaml`, `gates.yaml`, or
   `issuer_lookthrough.yaml` — every changed/added ticker already has an
   existing canonical row; no target, cap, or gate is added, removed, or
   resized.
4. **Resolves** the cash discrepancy between v1.37 ($845.84) and
   `PHQ-2026-04`'s post-sale cash ($2,675.05) — see "Bounded correction"
   below. `holdings.yaml` has no persisted cash field (unchanged since
   `PHQ-2026-02`), so this filing still has nothing to mutate in
   `holdings.yaml`'s data; the resolved figure is recorded as evidence and
   in `holdings.yaml`'s own comment block only.
5. Retains the full v1.37 evidence package verbatim under
   `governance/evidence/PHQ-2026-05/v1_37/` (`MANIFEST.json`, the JSON
   account-state export, the CSV holdings export, `README.md`) — SHA-256
   independently reconfirmed against the manifest at filing time.

## Bounded correction (same day, this PR)

After this decision was first filed with the cash discrepancy disclosed as
unresolved, the principal supplied a further "Final Account Summary
Correction v1.38" package (`MANIFEST.json`, a JSON account-summary export,
`README.md`, and three Robinhood screenshots — `account_home_1613.png`,
`buying_power_cash_1613.png`, `margin_state_1613.png`, all timestamped
~16:13 ET 2026-07-31). The original v1.38 transfer ZIP was verified before
extraction with SHA-256
`d423827f470576feb382772b8abdd66b27caea28b78a8a867c02b5e504c57a60`. The ZIP
itself is not retained in this repository, so that transfer-package hash is
recorded provenance rather than a repository-recomputable aggregate.
Integrity of the retained extracted evidence is controlled by the
manifest's per-file hashes, all of which were independently recomputed and
matched (internal-file hashes below under Evidence).

**The correction resolves the cash discrepancy exactly, not approximately:**

| | Amount |
|---|---:|
| Post-sale cash recorded by `PHQ-2026-04` evidence | $2,675.05 |
| Confirmed buy total (the seven `PHQ-2026-05` fills) | $1,734.00 |
| Calculated final cash | $941.05 |
| Robinhood-displayed final cash (v1.38 evidence) | $941.05 |
| Difference | $0.00 |

v1.37's $845.84 cash figure is superseded for final-account-state purposes
by this reconciliation and must no longer be described as an unresolved
current-state discrepancy. v1.38 supersedes v1.37 **only** for
account-summary fields (cash $941.05, buying power $7,243.93, margin used
$0.00, margin available $6,302.88, maintenance requirement $1,558.09) — it
does **not** supersede v1.37's post-buy position quantities (the seven-ticker
table above), and it does **not** reopen, restore, or otherwise touch
SKHY/SPCX, which remain governed entirely by `PHQ-2026-04`. Portfolio value
is reported at two slightly different point-in-time figures across the three
screenshots ($6,226.90 home screen vs. $6,227.11 margin screen, taken moments
apart) — treated as ordinary live-market price movement between screenshots,
not a reconciliation target; no artificial account-value balancing entry is
introduced. `holdings.yaml` has no persisted cash field (unchanged since
`PHQ-2026-02`); this correction updates `holdings.yaml`'s comment block and
this decision's own text to state the resolved figure, and retains the full
v1.38 evidence package (including the three screenshots) verbatim under
`governance/evidence/PHQ-2026-05/v1_38/`, matching the existing
screenshot-retention convention `PHQ-2026-02`'s v1_35 evidence already used.

The authoritative allocation check (`python3 allocate.py --review --no-log`)
was re-run against the repository state as corrected by this bounded
correction. Because `--review` mode uses no new cash input, the resolved
$941.05 figure does not change the review's own inputs — the check was
re-run anyway, as a live re-verification rather than an assumption that nothing
changed, and produced the same result as before this correction: 0
underweight, 0 trim, 1 blocked (ISRG, downtrend), 6 gated no-add, no cluster
cap breached, 40% common-driver ceiling live-calculated at 47.08% (unchanged;
review mode buys/trims nothing, so the live book composition did not move).

## Rationale

**FACT** — the seven-ticker delta table above was derived by a direct,
field-by-field comparison between `holdings.yaml`'s state after `PHQ-2026-04`
and the v1.37 package's `positions` list (JSON), cross-checked against the
CSV export (identical quantities in both v1.37 files). All three v1.37 data
files' SHA-256 hashes were independently recomputed and matched
`MANIFEST.json` exactly before any repository file was edited.

**INFERENCE** — none of the seven quantity changes required inference; each
is a directly-stated `quantity` field in the v1.37 JSON/CSV, both internally
consistent with each other.

**JUDGMENT** — resolving the SKHY/SPCX conflict between v1.37 and
`PHQ-2026-04` is a judgment this repository's evidence alone cannot make
(this session was explicitly instructed not to query Robinhood or infer tax
lots). The principal was asked directly and made the call: `PHQ-2026-04`'s
independently-evidenced, timestamped sale-fill record controls over v1.37's
apparently-stale SKHY/SPCX rows. This filing implements that principal
judgment; it does not make the call itself.

**UNCERTAINTY** — the root cause of v1.37's stale SKHY/SPCX rows is not
established by this filing (e.g., whether v1.37's screenshots were captured
before the `PHQ-2026-04` sale despite a later-stamped `effective_time`, or
some other explanation). This filing does not speculate further and treats
the principal's direction as controlling without asserting a mechanism for
that specific discrepancy. The cash figure itself is no longer uncertain as
of the bounded correction above — v1.38's arithmetic reconciles exactly
($0.00 difference) — though the mechanism behind v1.37's own $845.84 figure
being wrong is likewise not established.

## Alternatives Considered

- **Apply v1.37 verbatim, including its SKHY/SPCX rows.** Rejected — would
  silently re-introduce two positions `PHQ-2026-04` independently evidenced
  as sold, and was explicitly rejected by the principal when the conflict
  was escalated.
- **Wait for `PHQ-2026-04` (PR #205) to merge before filing this
  reconciliation.** Rejected — `PHQ-2026-04`'s exact commits were adopted
  directly onto this filing's branch (a clean fast-forward from the same
  base) rather than duplicated or re-derived, so this filing's diff against
  `main` is self-consistent and correctly sequenced; no conflicting branch
  was created. This filing does not alter, and is not itself, `PHQ-2026-04`.
- **Resolve the cash discrepancy by picking one of the two originally
  reported figures ($845.84 or $2,675.05) as authoritative, without further
  evidence.** Rejected at the time this decision was first filed —
  `holdings.yaml` has no persisted cash field to update, and picking a
  number without principal-supplied reconciling evidence would have
  fabricated a fact this session could not verify. Superseded by the
  bounded correction above once the principal supplied v1.38's reconciling
  evidence, which resolves the figure with an exact ($0.00) arithmetic
  match rather than a guess between the two candidates.
- **Add new `targets.yaml` rows for PWR/VEA/VWO.** Rejected — unnecessary;
  all three already have canonical destination rows from `PHQ-2026-02`'s
  migration. This is a quantity update only.
- **Treat the $0.21 portfolio-value difference between the two v1.38
  screenshots as a reconciliation gap requiring an artificial balancing
  entry.** Rejected — both screenshots are timestamped moments apart at
  live market prices; a sub-dollar difference across live snapshots is
  ordinary price movement, not an accounting error, and forcing a balancing
  entry would fabricate a fact not in evidence.

## Consequences

- `holdings.yaml` changed exactly as described (seven `shares:` quantities,
  plus its own comment block updated by the bounded correction to record
  the resolved cash figure — no data field added);
  `governance/decisions/PHQ-2026-05-post-buy-quantity-reconciliation-v1-37.md`
  (this file), `governance/decisions.yaml` (one new entry),
  `governance/evidence/PHQ-2026-05/v1_37/` and
  `governance/evidence/PHQ-2026-05/v1_38/` (both new, retained verbatim),
  and `CLAUDE.md` (Decisions Log pointer, updated by the bounded correction)
  are the only other files this decision changes. No `targets.yaml`,
  `gates.yaml`, `issuer_lookthrough.yaml`, `allocate.py`, `margin_state.py`,
  or `operations/WORKSTREAMS.yaml` change.
- No trade, order, margin draw, or brokerage mutation of any kind is
  authorized or performed by this decision — it records buy fills the
  principal already executed manually.
- No allocator behavior, tier, target, cluster, cap, or gate is changed.
  SKHY and SPCX remain exactly as `PHQ-2026-04` left them.
- Per this repository's Lean Delivery and Review Lifecycle (`OPS-0009`),
  this filing is classified **Lane M** (mechanical/factual synchronization)
  — it records already-true, principal-confirmed post-buy quantities and
  introduces no new tier/target/cluster/cap/gate/allocator authority. Per
  `OPS-0009` §2, Lane M may omit a separate independent-review round of the
  recording itself, but every other control still applies in full,
  including explicit principal acceptance of the underlying facts before
  merge, protected-path verification, and applicable test/validator
  re-confirmation. This decision does not mark itself ready and does not
  authorize its own merge.
- Effective only on merge; this draft PR is not itself approval, merge, or
  completion.

## Evidence

`governance/evidence/PHQ-2026-05/v1_37/` — the principal-supplied v1.37
package retained verbatim (`MANIFEST.json`, `Portfolio_HQ_Final_Confirmed_Account_State_v1_37.json`,
`Portfolio_HQ_Final_Confirmed_Holdings_v1_37.csv`, `README.md`). SHA-256 of
each file independently recomputed and matched against `MANIFEST.json` at
filing time:

- `Portfolio_HQ_Final_Confirmed_Account_State_v1_37.json`:
  `782f68284b92377ed396584a63c112f7835900ac18a2d117d85f62239da85ebd`
- `Portfolio_HQ_Final_Confirmed_Holdings_v1_37.csv`:
  `c091ef39994829a2ebfd71baa419983a820cd43fbcd23d13ba18e845a6a4636b`
- `README.md`: `ab17dfe6314c549d74bd8edf4a2b4ad2a9d43f104e1940115038106d4b1bf38c`

`governance/evidence/PHQ-2026-05/v1_38/` — the principal-supplied v1.38
"Final Account Summary Correction" package retained verbatim
(`MANIFEST.json`, `Portfolio_HQ_Final_Account_Summary_Correction_v1_38.json`,
`README.md`, `evidence/account_home_1613.png`,
`evidence/buying_power_cash_1613.png`, `evidence/margin_state_1613.png`).
The original v1.38 transfer ZIP was verified before extraction with SHA-256
`d423827f470576feb382772b8abdd66b27caea28b78a8a867c02b5e504c57a60`. The ZIP
itself is not retained in this repository, so that transfer-package hash is
recorded provenance rather than a repository-recomputable aggregate.
Integrity of the retained extracted evidence is controlled by the
manifest's per-file hashes, all of which were independently recomputed and
matched against `MANIFEST.json` exactly at filing time:

- `Portfolio_HQ_Final_Account_Summary_Correction_v1_38.json`:
  `506f8b8d33b4dd247fd2ebff4583032065bf85f919c638380aa1b50d8bf84012`
- `README.md`: `4718aa8bd38d269d7daadbfbce0be34b3579850f37ceaeaa2cb3fe346fccdfb6`
- `evidence/account_home_1613.png`:
  `afa879ecf996b49a53962f8c50213e2736a1d0ddd2b6ec42adf7688f1ab8447a`
- `evidence/buying_power_cash_1613.png`:
  `f843ae852aa268b12860843635fb43d413e2dd0bf6edcd3ff0e94a8eac1be4a1`
- `evidence/margin_state_1613.png`:
  `14647c2b2b69af1df079fd440f4118b0c0ee9e4be840d6982ed13a066893f928`

## Limitations

- The root cause of v1.37's stale SKHY/SPCX rows is not established (see
  Rationale, Uncertainty) — resolving the cash figure via v1.38 does not by
  itself explain why v1.37's SKHY/SPCX rows or its $845.84 cash figure were
  wrong.
- `holdings.yaml`'s `margin.buffer_pct` (currently `100.0`, representing
  zero margin drawn rather than a Robinhood-displayed screen) is unchanged
  by this correction — v1.38 supplies margin-available ($6,302.88) and
  maintenance-requirement ($1,558.09) figures, but not a Robinhood-displayed
  buffer percentage, and this repository's standing rule is to use only
  Robinhood's own displayed buffer %, never a derived one. A real displayed
  buffer % should still be synced before any future margin-funded decision.
- This filing does not evaluate, re-open, or resolve SPCX's or SKHY's
  reopening conditions (`PHQ-2026-03` §7) — unchanged.

---

_**2026-08-01 Lane M factual synchronization** (dated note, appended per
`governance/decisions/README.md`'s convention for a narrow factual/lifecycle
correction — no edit to this decision's substance): this decision (commits
`f56f7db`, `6a3afe7`, `0757a6a`) was merged to `main` via PR #206 at merge
commit `f700fca0abeb321196e015550d1439dfedb9d7b0` (two parents:
`7d9477b2a30180b6025452957eb3c866fed50387`, the shared `PHQ-2026-03`/PR #204
base, and `0757a6a604bd83876a4f21ca5cbfddce55a54f31`, this decision's own
reviewed head), independently confirmed this session via `git log
--pretty=%P -n1 f700fca...` and via `git merge-base --is-ancestor` showing
head `0757a6a...` is an ancestor of `origin/main`. **An independent review
is retained and was independently verified this session**: GitHub PR #206
review id `4832265448` (`state: COMMENTED` — GitHub's own
"Can not approve your own pull request" self-approval restriction on the
authenticated account is disclosed in the review text itself, per
`OPS-0007` §1's platform-identity caveat; the review states it was performed
by "a new, independent Claude Code session that did not author PR #206, PR
#205, commit `6a3afe7`, or correction commit `0757a6a`"), anchored to this
exact merged head (`0757a6a604bd83876a4f21ca5cbfddce55a54f31`), verdict
"APPROVE" with "No remaining findings." The GitHub API independently
confirms the PR itself as `merged: true` (`merged_by: Mast3rkey`, this
repository's own principal/owner identity). No separate, distinctly-labeled
"Principal acceptance:" comment was found retained on the PR via the GitHub
API as of this synchronization session; the merge action itself, taken by
the principal/owner identity after the retained review's APPROVE verdict, is
the lifecycle evidence this note relies on for that element — this note does
not assert a separate acceptance statement exists beyond what is shown
above. Frontmatter `status` is updated to `Accepted` accordingly. This note
records only the completed merge-lifecycle event confirmed by this session's
own independent verification; it does not alter, re-open, or re-evaluate any
substantive term of this decision, does not touch SKHY/SPCX's disposition
(governed entirely by `PHQ-2026-04`), and does not authorize any further
research, trade, target, gate, or margin change.
