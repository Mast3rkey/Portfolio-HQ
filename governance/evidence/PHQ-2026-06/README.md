# PHQ-2026-06 evidence

Retained, unedited Robinhood "Account Summary" screenshot supporting the
`PHQ-2026-06` factual cash synchronization (a $100 deposit reconciling the
repository's prior resolved cash of $941.05, via an earlier connected-account
snapshot of $941.23, to a new displayed cash figure of $1,041.23).

- `robinhood_account_summary_20260801.webp` — the screenshot, copied
  byte-for-byte. Not cropped, annotated, recompressed, or otherwise
  transformed. SHA-256 `d602da67bee33644da8600691974ddd3098549c78c73292904320a16c0e2ffca`,
  49254 bytes.
- `MANIFEST.json` — displayed figures, hash, provenance, and the disclosed
  $0.18 discrepancy note.

## Provenance

This screenshot was supplied as an inline chat image attachment in the
Claude Code session, not as a named file at a filesystem path. An earlier
turn in the same session asserted the file existed at `/mnt/data/image(256).png`;
that path does not exist in this execution container and nothing was found
there. The bytes retained here were instead extracted directly from this
session's own conversation transcript (where an attached image is stored as
base64 content exactly as received by the model), independently hashed, and
visually re-inspected side-by-side against what had been rendered inline in
chat before being copied into this directory. See `MANIFEST.json`'s
`provenance_note` for the full disclosure.

**Verifiability boundary** (see `MANIFEST.json`'s `provenance_chain` for the
full breakdown): anyone with repository access can independently verify the
retained file's SHA-256, byte size, media type, and every displayed figure
by opening `robinhood_account_summary_20260801.webp` directly — no trust in
the authoring session is required for those checks. What cannot be
independently proven by any third-party reviewer is that this retained file
is bit-for-bit identical to what the principal's own Robinhood client
originally rendered and sent — that link rests on principal review and
acceptance of this artifact as a faithful copy, the same unavoidable trust
boundary every prior screenshot-evidenced `PHQ-####` decision in this
repository carries (`PHQ-2026-02`, `PHQ-2026-04`, `PHQ-2026-05`).

## Scope

This evidence package supports a **cash-only** factual synchronization. It
does not evidence, and is not used to justify, any share-count change,
margin change, trade, allocator run, or policy change. See
`governance/decisions/PHQ-2026-06-cash-synchronization-100-deposit.md` for
the governing decision record.
