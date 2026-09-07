# Live-state boundary

This package synchronizes architecture research, evidence, and approved policy.

It must not be used to reconstruct current holdings.

After the frozen snapshot:

- Robinhood orders were entered;
- some orders filled;
- some orders were queued for the next market open;
- therefore the frozen snapshot, provisional transition map, and simplified
  allocation output are stale as live-state evidence.

Required repository treatment:

- retain historical artifacts only when clearly labeled;
- do not update `holdings.yaml`;
- do not claim current account state;
- do not treat any allocation output as current execution authority;
- preserve SPCX as HOLD / NO ADD in current narrative;
- leave SKHY unresolved pending later policy or holdings reconciliation.
