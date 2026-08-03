# PHQ-2026-07 evidence

Two retained, unedited Robinhood screenshots supporting the `PHQ-2026-07`
factual cash synchronization (a $238 deposit reconciling the repository's
prior resolved cash of $1,041.23, per `PHQ-2026-06`, to a new displayed cash
figure of $1,279.23).

- `robinhood_investing_home_20260803.png` — Investing tab home screen.
  SHA-256 `3724e4d2b3d1a20047dca3837cf78535667b911801c4d173de1b0b5263737d84`,
  741690 bytes, `image/png`.
- `robinhood_buying_power_detail_20260803.png` — Buying power detail screen.
  SHA-256 `8f5f264f979bea803686505be80239fafb21cec8d4cc5c3e2fb7540563a4bc0f`,
  358939 bytes, `image/png`.
- `MANIFEST.json` — full displayed-figure record and provenance.

## Provenance

Unlike `PHQ-2026-06`, both images were supplied as filesystem-accessible
uploads at a real, readable path in this execution container — no
transcript-extraction workaround was required. Both files were copied
byte-for-byte into this directory and independently hashed from the copies
on disk.

## Scope

This evidence package supports a **cash-only** factual synchronization. It
does not evidence, and is not used to justify, any share-count change. The
buying-power screen's qualitative "Margin buffer: Ready to use" status is
recorded as context but does **not** update `holdings.yaml`'s
`margin.buffer_pct` — that field still requires a real Robinhood-displayed
numeric buffer % before any future margin-funded decision, unchanged
standing guidance. Margin debt ($0.00) and the confirmation that the prior
allocation check's recommended AVGO/ETN buys did not execute were both
obtained via explicit principal confirmation in-session (not derived from
either screenshot), and are recorded in `MANIFEST.json`. See
`governance/decisions/PHQ-2026-07-cash-synchronization-238-deposit.md` for
the governing decision record.
