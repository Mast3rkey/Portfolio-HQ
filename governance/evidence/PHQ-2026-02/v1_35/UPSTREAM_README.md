# Portfolio-HQ post-execution reconciliation package v1.35

## Purpose

This package captures principal-supplied account and holdings evidence received
at approximately 2026-07-31 09:40 ET after the manual transition orders.

## Controlling use

- Position quantities are the primary evidence for a future `holdings.yaml`
  reconciliation.
- The later screenshot supplies the account summary and complete equity list.
- The earlier screenshot supplies expanded crypto quantities.
- Values are point-in-time references only and differ slightly because the
  screenshots were captured seconds apart during live markets.
- Do not force the values to reconcile exactly.
- Do not infer tax lots, holding periods, unshown fills, or current prices.
- Do not query Robinhood.
- Do not place or submit orders.

## Account state shown

- Account value: $6,223.16
- Cash: $2,579.84
- Margin used: $0.00
- Buying power: $8,841.78
- Equities displayed: $3,325.86
- Crypto displayed: $317.90

The displayed components differ from the displayed account value by
$0.44, consistent with live timing and displayed rounding.

## Repository treatment

A future Claude Code session must:

1. inspect the live `holdings.yaml` schema and controlling decisions;
2. compare every screenshot quantity with existing repository state;
3. present any symbol-mapping ambiguity explicitly;
4. update holdings only in a narrow reviewed PR;
5. preserve SPCX as hold/no-add and SKHY as unresolved;
6. keep all order execution external and manual;
7. run repository validators and tests;
8. generate a post-reconciliation allocation check only after the holdings and
   PHQ-2026-02 implementation are both authoritative in GitHub.
