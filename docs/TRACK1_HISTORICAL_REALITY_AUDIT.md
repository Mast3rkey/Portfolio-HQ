# Track 1 — Historical Reality Audit

_2026-07-17, Rev 2 · Documentation only, no code. Companion to `docs/TRACK2_HYPOTHETICAL_MARGIN_SIMULATION.md` and `docs/MARGIN_DATA_INVENTORY.md`. This track has no simulation, no assumptions, and no hypothetical results — it is a factual inventory of what this account's real margin history actually shows, and, just as importantly, what it doesn't. Every figure below is sourced directly from git history, `performance_log.csv`, or `CLAUDE.md` prose (marked as such), checked at the time of writing. Rev 2 adds gross exposure / net equity / leverage ratio at each known point (not just debt/buffer) and restructures around eight specific questions._

**Question this track answers:** What do we actually know about the margin that existed?

**Question this track does NOT answer:** whether margin helped. That requires a counterfactual (what would have happened without it), and a counterfactual is definitionally not observable — it's Track 2's job entirely, and Track 2's results are labeled hypothetical throughout for exactly this reason.

---

## The eight questions, answered directly

### 1. When did margin debt first appear in records?

**2026-07-13**, commit `466fbce` ("Sync margin after $50 withdrawal") — the **first commit in this repository's entire git history** to touch `holdings.yaml`'s margin block, and in fact one of the earliest commits in the repo at all. Margin debt did not "appear" on this date in reality — `CLAUDE.md`'s Decisions Log states it was "discovered" already existing, at a recollected figure of ~$4,423, sometime before this date. What actually happened on 2026-07-13 is: **margin debt first entered this system's records**, mid-existence, not at origin. That distinction matters and is treated as its own finding in Question 8.

### 2. What is the earliest reliable debt snapshot?

**$3,449.50**, 2026-07-13, commit `466fbce` — the earliest **git-committed** figure. This is "reliable" in the specific sense of being a structured, dated, version-controlled data point. The ~$4,423 figure that came before it is a real fact (referenced consistently in `CLAUDE.md` prose) but is **not** a reliable snapshot in this same sense — it has no commit, no exact date, and no corroborating file. Treat $3,449.50 as the first point on any timeline; treat ~$4,423 as a caveat about what preceded that timeline, not as its starting point.

### 3. What portfolio value existed at each known point?

Real, computed values — not estimates — for every point where the source data supports an exact figure:

| Point | Source | Gross | Net equity |
|---|---|---:|---:|
| 2026-07-13, intraday #1 (`466fbce`) | Static `holdings:` dict, summed directly from the committed file (pre-share-tracking era — this file genuinely stored full per-ticker dollar values at this point, so the sum is exact, not estimated) | $8,994.32 | $5,544.82 |
| 2026-07-13, intraday #2 (`49c1ffe`, post-VMC-exit) | Same method | $8,878.67 | $5,543.29 |
| 2026-07-13, EOD (`performance_log.csv`) | Live-priced snapshot, logged same day | $8,817.47 | $5,518.09 |
| 2026-07-14, EOD | `performance_log.csv` | $8,648.93 | $5,969.53 |
| 2026-07-15, EOD | `performance_log.csv` | $7,596.07 | $5,967.43 |

**Why some of the 7 margin-sync commits (Table in Question 6) don't get their own row here:** `holdings.yaml` switched from storing full per-ticker dollar values to a share-count-based system at commit `c54be71` (2026-07-13, same day) — after that point, the `holdings:` block became a residual manual-fallback (nearly empty), and the real gross value requires live-priced shares at that exact historical moment, which isn't preserved. Where a margin sync commit doesn't land on exactly one of the 5 rows above, its portfolio value at that precise moment is not independently recoverable — only its debt/buffer (Question 6) is.

### 4. What was gross exposure vs. net equity?

Answered by the same table as Question 3 — gross and net equity are both directly computed there, not estimated. Net equity ranged from $5,518.09 (07-13 EOD, the low point) to $5,969.53 (07-14 EOD, the high point) across the 3-day observable window.

### 5. What leverage ratio was actually present?

Computed directly (`leverage = gross / net_equity`) from Question 3's table:

| Point | Leverage |
|---|---:|
| 2026-07-13, intraday #1 | **1.622x** |
| 2026-07-13, intraday #2 | 1.602x |
| 2026-07-13, EOD | 1.598x |
| 2026-07-14, EOD | 1.449x |
| 2026-07-15, EOD | **1.273x** |

**Directly observable: leverage fell monotonically across every recorded point**, from 1.622x down to 1.273x — a real, computed fact, not modeled. It never approached the current 1.8x structural cap at any recorded point; the highest observed leverage (1.622x) was already 90% of the way to the cap in relative terms but never breached it or came within a forced-response distance of it.

### 6. What margin buffer readings were recorded?

The complete set — 7 discrete syncs, the full historical record this system has ever captured:

| # | Date | Debt | Buffer % | Trigger |
|---|---|---:|---:|---|
| 1 | 2026-07-13 | $3,449.50 | 56.08% | Post-$50-withdrawal sync (earliest record) |
| 2 | 2026-07-13 | $3,335.38 | 56.61% | VMC exit + paydown |
| 3 | 2026-07-13 | $3,299.38 | 56.75% | NOW trim + paydown |
| 4 | 2026-07-14 | $2,898.22 | 59.76% | Deposit clearing |
| 5 | 2026-07-14 | $2,679.40 | 61.08% | Trim proceeds paydown |
| 6 | 2026-07-15 | $2,671.85 | 61.96% | Robinhood screen resync (price/position drift, not a real paydown) |
| 7 | 2026-07-15 | $1,628.64 | 61.77% | 9-name T1/T2 concentration-ceiling trim batch |

Buffer rose from 56.08% to a peak of 61.96% (row 6) before settling at 61.77% (row 7) — consistently well above the 30% floor throughout the entire observed record.

### 7. Are there any signs of forced deleveraging risk?

**No — not in the observed record.** Every one of the 7 buffer readings sits between 56.08% and 61.96%, roughly double the 30% floor at every single point. Nothing in this system's history shows a buffer reading anywhere near the floor. **This is not the same claim as "the floor was never approached in reality"** — Question 8 names the real gap: buffer is only captured at manual sync moments (7 of them, clustered in a 3-day window), and nothing is recorded about what happened *between* syncs, including any period before 2026-07-13 entirely. The honest statement is: **no forced-deleveraging risk is visible in what was recorded**, which is a narrower and weaker claim than "no forced-deleveraging risk ever existed."

### 8. What data is permanently unavailable?

Consolidated from `MARGIN_DATA_INVENTORY.md`'s Category C, restated here because it's a direct answer to this specific question:
- **True historical margin utilization before 2026-07-13** — the debt already existed when found; the draw history behind it is gone.
- **Exact historical interest paid** — zero records exist, anywhere, at any point, in this or any file.
- **Exact borrowing timeline** — individual draw events, beyond the 7 net debt-level snapshots above.
- **Actual buffer changes or margin calls between syncs** — the 3-day observed window has 7 syncs; every gap between them (and the entire period before 07-13) is a blind spot, not a zero.
- **Anything about the ~$4,423 pre-history figure** beyond the bare number itself — no date, no corroborating snapshot, no connection to a specific holdings state.

---

## Conclusion

**The system cannot evaluate whether historical margin usage created alpha, because the historical borrowing path does not exist.** It can only evaluate the current state, and future policy, from the point of logging forward. Everything in Questions 1-7 above is real and precisely computed — but it spans three days, starts mid-existence of the debt it's describing, and contains no counterfactual (there is no "what if this account hadn't used margin" data point, because there was never a parallel unlevered account to compare against). A counterfactual is exactly what Track 2 constructs — as a labeled hypothetical, over a simulated account, precisely because no real one exists to ask the question of directly.

This conclusion does not get weaker or stronger as more analysis is applied to the 3-day window — it is a structural fact about what data exists, not a statistical-power problem more data-massaging could fix. The correct response is what `MARGIN_DATA_INVENTORY.md`'s collection plan already proposes: start logging the data that would make this question answerable *from now forward*, and treat everything before 2026-07-13 as permanently outside this system's evidence base.
