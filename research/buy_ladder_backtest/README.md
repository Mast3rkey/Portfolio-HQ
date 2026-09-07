# Buy-ladder backtest

`PROTOCOL_V2.md` and its foreign-dividend amendment govern the one registered
canonical-roster comparison. `inputs/` is the accepted result-blind LADDER-0003
evidence disposition.

Run the integrity gate before the registered execution:

```bash
python -m research.buy_ladder_backtest.ladder_v2 validate
python -m research.buy_ladder_backtest.ladder_v2 execute
```

Validation checks frozen hashes, selected OHLC identity, action uniqueness, market
calendar coverage, and context-only indicators. It emits no holdout result. Execution
requires the matching receipt and refuses to overwrite an existing `execution/`
directory. The committed execution is the only authorized run; another run or any
changed input requires separate governance authority.

See `RESULTS.md` for the plain-language disposition. Nothing in this directory is
connected to account state, brokerage access, orders, production allocation, margin,
or Stage 1.
