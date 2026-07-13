# band-validation — manual-allocation advisor

A **recommendation-only** allocation tool. It reads your holdings and target
tiers, pulls read-only market data from Alpaca, applies your gates, and prints a
BUY / TRIM / BLOCKED table. **It never places, modifies, or cancels an order —
anywhere.** You execute manually on Robinhood.

> Safety by construction: `alpaca_client.py` has had all order-placement methods
> **removed**. The project contains no order code. Do not re-add it.

## Usage
```bash
python allocate.py --cash 2000     # deploy new cash → ranked buys
python allocate.py --review        # rebalance check, no new cash (underweights + trims)
python allocate.py update-holdings # paste "TICKER value" lines, Ctrl-D to save
```
Output is Markdown to the console **and** `logs/allocation-YYYY-MM-DD.md`.

## Config (YAML, all values editable)
- **`targets.yaml`** — tier structure. Per-name weights (% of book): T1 3.35%,
  T2 1.65%, ETF (SPY/QQQ/GLD) 2.3%, band 0.75%, spec (INTC/SPCX/RKLB/TSLA/PLTR)
  1.0% fixed, crypto sleeve 10%. Plus caps (semis ≤25%, band ×1.25), gates
  (min lot $25, trend RSI override 30, earnings blackout 7d, trim RSI 60).
  **Paste your final roster into the tier `tickers:` lists.**
- **`holdings.yaml`** — `{ticker: market_value}`; rewritten by `update-holdings`.

## How a run works
1. Book = holdings + new cash; per-ticker target dollars from tier weights.
2. Pull last price, 200-SMA, 50-SMA, RSI(14), ATR(14) per roster ticker; QQQ
   daily bars for the regime signal.
3. Rank underweight names by gap, then gate in order:
   **regime** (QQQ below 200-EMA → hold cash, list would-buys) →
   **trend** (skip below-200-SMA adds unless RSI<30) →
   **earnings** (skip within 7 days; flagged if date unavailable) →
   **caps** (semis ≤25% of book, band ≤1.25× target, spec fixed at target).
4. Greedy-allocate cash to the largest passing gaps, $25 minimum lot.
5. Trim candidates: band/spec > 1.25× target with RSI > 60.

## Harvested modules
- **`alpaca_client.py`** — read-only paper connection (account/clock/positions/
  bars), `PAPER_ONLY` guard, **order methods stripped**.
- **`market_hours.py`** — Alpaca-clock market gate + local ET fallback.
- **`regime_gate.py`** — 200-day-EMA regime layer on QQQ daily bars.
- **`indicators.py`** / **`earnings.py`** — SMA/RSI/ATR; yfinance earnings lookup
  with graceful "unavailable" flagging.

## Known limitation
Live bars use the **IEX free feed** → volume figures are IEX-only. The advisor
relies on **price-based** indicators (SMA/RSI/ATR), so this does not affect it.
