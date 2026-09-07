# Protocol V2 foreign-dividend tax amendment

Status: frozen result-blind amendment; no ladder result was inspected before this
text was fixed.

Authority: `LADDER-0003`. This document amends only the foreign-dividend tax and
reporting rules in `PROTOCOL_V2.md`. Every arm, selector, target, date, threshold,
cost cell, bootstrap rule, seed, event-order rule, and abstention rule in V2 remains
unchanged.

## Reason for the amendment

The retained action registry sometimes reports the cash rate after tax withheld by
the issuer's jurisdiction. Applying V2's 16.8% U.S. taxable-middle approximation to
that source-net rate would understate the gross dividend and then charge U.S. tax on
the wrong base. Applying the full U.S. rate to gross after also subtracting foreign
withholding would double count tax when a foreign-tax credit is available.

This correction was identified while reconciling actions, before any ladder arm was
implemented or evaluated.

## Amended calculation

For each foreign cash dividend, the accepted action row must carry:

- `gross_rate_usd`, the gross USD entitlement per source-date share;
- `source_net_rate_usd`, the USD cash amount after source withholding;
- `source_withholding_usd = gross_rate_usd - source_net_rate_usd`; and
- `rate_evidence`, which separates exact issuer facts from a stated withholding
  assumption or inference.

Negative withholding, a source-net amount above gross, missing evidence labels, or
an untraceable gross-rate derivation is fatal.

Let `q` be entitled shares after V2's split-unit conversion and let `u = 0.168` be
V2's unchanged U.S. taxable-middle rate. Compute:

```text
gross_entitlement       = q * gross_rate_usd
source_withholding      = q * source_withholding_usd
tentative_us_tax        = u * gross_entitlement
foreign_tax_credit      = min(source_withholding, tentative_us_tax)
residual_us_tax         = tentative_us_tax - foreign_tax_credit
total_dividend_tax      = source_withholding + residual_us_tax
net_dividend_receivable = gross_entitlement - total_dividend_tax
```

This is a research approximation. It assumes the modeled account can use a foreign
tax credit up to the modeled U.S. tax on the same dividend. It does not model ADR
fees, credit carryovers, jurisdiction-specific reclaim procedures, account-specific
limitations, or tax advice. Domestic dividends retain V2's original calculation:
source withholding is zero, residual U.S. tax is 16.8% of gross, and the net
receivable is 83.2% of gross.

## Required outputs and sensitivities

Each arm and window must report gross dividends, source withholding, tentative U.S.
tax, foreign-tax credit, residual U.S. tax, total dividend tax, net dividend
receivables, and settlements separately. The engine must also report a conservative
foreign-tax-credit sensitivity that sets the credit to zero. This sensitivity is
non-voting unless it causes the apparent winner to fail a V2 adoption gate, in which
case the disposition is `INSUFFICIENT_EVIDENCE`.

All payable-date, ex-date, split-basis, receivable, end-of-window, and price-only
diagnostic rules remain exactly as stated in V2. This amendment authorizes no target
change, production policy change, brokerage action, order, trade, or leverage. Stage
1 remains **UNARMED AND NOT EXECUTABLE**.
