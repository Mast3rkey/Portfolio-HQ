# Margin Doctrine

_2026-07-17 · The constitutional document for margin in this system. Every margin-related design, backtest, or code change is checked against this page before it's built. If a future proposal doesn't fit here, the proposal changes — not this page, and not without a new Decisions Log entry explaining why the doctrine itself is being revised._

---

## The one-sentence version

**Margin only amplifies whatever edge the underlying portfolio already has. It is not itself a source of edge, and its job in this system is risk governance, not return generation.**

## What margin is

Margin is borrowed buying power collateralized against the whole account. It lets the portfolio hold more gross exposure than net equity alone would allow. That's the entire mechanism — there is no sense in which margin *picks* better positions, *times* the market better, or *knows* something the unlevered portfolio didn't already know. Every dollar of return margin produces is a multiple of a return the portfolio was already going to earn (or lose) on its own. Every dollar of loss margin produces is the same multiple, in the same direction, on the way down.

## What margin is not

- **Not an alpha source.** It cannot turn a mediocre portfolio into a good one. If the underlying holdings don't have edge, margin just loses money faster, with interest added on top.
- **Not a timing tool.** There is no "right time to borrow more" and no "right time to borrow less" that this system will ever compute from a market read, a valuation judgment, a volatility level, or a drawdown. This line is absolute and has been tested against directly: a 2026-07-13 Decisions Log entry explicitly rejected any margin-timing model ("borrow more when conditions look good") as "not backtestable" — because the premise itself (leverage as a source of edge to time) is false, not because the backtest came back unfavorable. There is no version of this system, present or future, where margin usage moves because "now looks like a good time."
- **Not free.** Margin interest (~5% APR, first $1,000 free, per the Robinhood terms this account uses) is a guaranteed, certain cost — a hurdle rate the levered portion of the portfolio must clear just to break even, before any consideration of the extra risk taken on. It is never treated as a rounding error.
- **Not a discretionary lever.** Every existing margin rule in this system (the 1.8x leverage cap, the 30% buffer floor) is a fixed, mechanical ceiling/floor with no exception path — the same posture as the crypto sleeve's fixed conviction-sizing and the cluster caps' fixed concentration limits. Margin Intelligence extends this posture; it does not introduce a new one.

## The system's job, precisely

1. **Measure whether leverage has historically helped**, honestly, on a risk-adjusted basis, before assuming it should continue. This has never actually been tested — the current 1.8x cap was set at "the level in place when the debt was discovered" (2026-07-13), not derived from evidence that leverage at that level, or any level, improves outcomes. Phase 1 of the Margin Intelligence research program exists specifically to close this gap.
2. **Prevent leverage from exceeding survivable limits.** "Survivable" means: the account can hold through a realistic historical stress period without a forced, capital-destroying liquidation — not "survivable" in the sense of maximizing return across some backtested window. This is a materially different optimization target than return-maximization, and every leverage-level test this system runs must be evaluated against survivability first, return second.
3. **Identify when repayment improves risk-adjusted outcomes**, using the same evidence-based standard as everything else — a repayment rule earns its way into production by beating a clearly stated baseline on a pre-committed threshold, exactly like every trim rule, cap, and gate this system has ever adopted.

## What "risk governance" means operationally

- Margin availability is a **ceiling that responds to the account's own state** (leverage ratio, buffer %, concentration) — never to the market's state.
- Margin state (Normal / Elevated / Forced Deleveraging, per the Margin Intelligence Engine design) exists to **describe risk that already exists**, not to **forecast risk that might arrive.**
- Repayment logic exists to **reduce standing risk when it's elevated**, using cash flows that are already happening for other, already-approved reasons (trims) — never to **react to a market forecast.**
- Every number this system produces about margin must be explainable in one sentence without reference to where the market is headed. "Leverage is at 74% of the cap" is explainable. "We're paying down debt because a correction looks likely" is not, and will never appear in this system's output.

## How this doctrine gets tested, and how it can change

This page is not exempt from the same evidence standard it imposes on everything else — but the standard for *testing this page* is different from the standard for testing a specific rule. The core claim ("margin is not itself a source of edge") is a mathematical identity, not an empirical claim — leverage is definitionally a multiplier on existing returns, so no backtest is needed or possible to "prove" it, the same way no backtest is needed to prove that trimming a position reduces its dollar exposure. What *is* empirical, and what Phase 1 exists to test, is narrower and different: **given that identity, does carrying margin at this account's actual cost of capital, at some specific leverage level, produce a better risk-adjusted outcome than not carrying it — net of interest, net of the extra drawdown risk.** That's a real question with a real answer this system doesn't yet have. This doctrine page will be updated with a dated entry once Phase 1 produces that answer, the same way every other closed backtest question gets logged in `CLAUDE.md`'s Decisions Log — not before.
