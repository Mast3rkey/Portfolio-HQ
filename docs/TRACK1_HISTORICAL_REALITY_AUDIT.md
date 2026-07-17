# Track 1 — Historical Reality Audit

_2026-07-17 · Documentation only, no code. Companion to `docs/TRACK2_HYPOTHETICAL_MARGIN_SIMULATION.md` and `docs/MARGIN_DATA_INVENTORY.md`. This track has no simulation, no assumptions, and no hypothetical results — it is a factual inventory of what this account's real margin history actually shows, and, just as importantly, what it doesn't. Every figure below is sourced directly from git history, `performance_log.csv`, or `CLAUDE.md` prose (marked as such), checked at the time of writing._

**Question this track answers:** What do we actually know about the margin that existed?

**Question this track does NOT answer:** whether margin helped. That requires a counterfactual (what would have happened without it), and a counterfactual is definitionally not observable — it's Track 2's job entirely, and Track 2's results are labeled hypothetical throughout for exactly this reason.

---

## 1. The observable margin timeline

Reconstructed from `git log --follow -- holdings.yaml`, cross-referenced against commit messages for the triggering event. This is the complete set of margin snapshots this repository has ever recorded — not a sample, the full set.

| # | Date | Debt | Buffer % | Change vs. prior | Trigger |
|---|---|---:|---:|---:|---|
| 1 | 2026-07-13 | $3,449.50 | 56.08% | — (earliest recorded) | Post-$50-withdrawal sync |
| 2 | 2026-07-13 | $3,335.38 | 56.61% | −$114.12 | VMC exit + paydown |
| 3 | 2026-07-13 | $3,299.38 | 56.75% | −$36.00 | NOW trim + paydown |
| 4 | 2026-07-14 | $2,898.22 | 59.76% | −$401.16 | Deposit clearing |
| 5 | 2026-07-14 | $2,679.40 | 61.08% | −$218.82 | Trim proceeds paydown |
| 6 | 2026-07-15 | $2,671.85 | 61.96% | −$7.55 | Robinhood screen resync (price/position drift, not a real paydown) |
| 7 | 2026-07-15 | $1,628.64 | 61.77% | −$1,043.21 | 9-name T1/T2 concentration-ceiling trim batch |

**Directly observable pattern:** across all 7 recorded points, debt only ever *decreased* — from $3,449.50 to $1,628.64, a $1,820.86 reduction (53% of the starting recorded balance) over 3 calendar days. Buffer correspondingly rose from 56.08% to 61.77%. **This is a real, fully verifiable fact, not an estimate**: every dollar of paydown in this window came from trims and a deposit, not from a deliberate "let's delever" decision — consistent with the standing doctrine that margin paydown here has always been a side effect of other mechanical rules firing (trims, deposits), never a standalone timing call.

**What this timeline cannot show:** whether this 3-day window is representative of anything. It's the entire observable history — there is no earlier or later data to compare it against, and no way to know from this alone whether debt was rising, flat, or being paid down in the weeks or months before 2026-07-13.

## 2. What predates the observable window

`CLAUDE.md`'s Decisions Log states the debt was originally "discovered" at **~$4,423** before the 2026-07-13 revision. Comparing this to the earliest git-committed snapshot ($3,449.50, also 2026-07-13, already post-$50-withdrawal): the gap between ~$4,423 and $3,449.50 (~$973.50) is larger than the $50 withdrawal alone accounts for, meaning some further paydown or correction happened between the "discovery" moment and this repo's first commit — **and that intermediate history is not recorded anywhere.** The ~$4,423 figure itself is prose, not a committed data point (see `MARGIN_DATA_INVENTORY.md`, Category A) — it's a real fact about what was once true, but it is the *only* fact this system has about the period before 2026-07-13, and it cannot be placed on a timeline, dated precisely, or connected to any specific holdings/price snapshot.

## 3. Deposits and withdrawals

**One event is recorded**: a $50 withdrawal, 2026-07-13, referenced in the commit that produced snapshot #1 above and in `CLAUDE.md`'s "post-BTC-trim, post-withdrawal" line. **No other deposit or withdrawal is dated, amount-stamped, or logged anywhere** — the workflow handles them conversationally each cycle (`CLAUDE.md` step 1: "I deposit money and report buying power") without persisting the event. `performance_log.csv`'s net-equity column moves for reasons that include deposits, withdrawals, margin draws/paydowns, *and* market price changes, all mixed together with no way to separate them — this is `render_performance()`'s own standing, disclosed limitation, not a new finding, but it's directly relevant here: it means net-equity changes across the 3-day window in Table 1 cannot be cleanly attributed to "margin paydown effect" vs. "everything else that happened at the same time."

## 4. Interest actually paid

**Zero data points.** No interest-charge figure exists anywhere in this repository — not a total, not a single dated charge, not an estimate derived from a statement. `CLAUDE.md`'s "~5% APR, first $1,000 free" is a description of the account's rate *terms*, sourced from Robinhood's stated policy for this account type, not a record of what has actually been charged and paid. This is the single largest gap in this audit: the entire "was margin worth its cost" question has never had a real cost figure to weigh against, in either direction.

## 5. Net equity / gross / benchmark comparison over the observable window

From `performance_log.csv` directly (3 distinct calendar dates):

| Date | Net equity | Gross | Margin debt | QQQ | VOO |
|---|---:|---:|---:|---:|---:|
| 2026-07-13 | $5,518.09 | $8,817.47 | $3,299.38 | $711.85 | $688.60 |
| 2026-07-14 | $5,969.53 | $8,648.93 | $2,679.40 | $719.71 | $691.12 |
| 2026-07-15 | $5,967.43 | $7,596.07 | $1,628.64 | $716.11 | $692.58 |

**Directly observable:** net equity rose $451.44 (8.2%) from 07-13 to 07-14, then fell $2.10 (flat) from 07-14 to 07-15, while gross fell sharply on 07-15 (the T1/T2 trim batch converting equity positions to debt paydown, not a market loss) and QQQ/VOO moved less than 1% across the same 3 days. **This is too short a window, with too much simultaneous change (a large trim event, a deposit, price moves, and a withdrawal all inside 3 days) to attribute any of this movement to "margin's effect" specifically** — stated here explicitly so it isn't quietly used as evidence for anything in Track 2 or beyond. Three days of data with multiple simultaneous causes is not a basis for a causal claim about margin, positively or negatively.

## 6. Summary — what this account's real history actually establishes

1. **A margin doctrine revision happened on 2026-07-13**, formalizing a debt that already existed (~$4,423 by recollection, $3,449.50 by the earliest hard record) into a fixed 1.8x leverage cap / 30% buffer floor regime — a policy decision made when the debt was found, not derived from a performance record of that debt.
2. **In the only 3 days this repository has ever recorded**, debt fell 53% and buffer rose 5.7 points, entirely as a side effect of trims and a deposit — consistent with, but not proof of, the standing doctrine that paydown here is mechanical, not a timing decision.
3. **Every quantity needed to answer "has margin been worth it"** — interest actually paid, a clean before/after equity comparison isolated from deposits and price moves, and any data at all from before 2026-07-13 — **does not exist in this system.** This is not a gap Track 2's simulation can fill; it can only build a parallel, clearly-labeled hypothetical answer to a *related* question (what would a stated policy have done to a simulated portfolio through real historical prices), which is a different question from "what did this account's real margin actually do," honestly answered here: **we don't know, and can't, from the data that exists.**

This conclusion is itself the primary deliverable of Track 1 — not a disappointing non-result, but the honest ceiling on what evidence-based margin research can claim about this specific account's past, stated plainly instead of allowed to blur into Track 2's hypothetical findings.
