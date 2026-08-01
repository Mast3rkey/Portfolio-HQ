---
decision_id: PHQ-2026-06
date: 2026-08-01
status: Proposed
category: portfolio_construction_governance
related_decisions: [GOV-0001, GOV-0002, OPS-0001, OPS-0009, PHQ-2026-01, PHQ-2026-02, PHQ-2026-04, PHQ-2026-05]
supporting_artifact: governance/evidence/PHQ-2026-06/MANIFEST.json
---

## Context

`PHQ-2026-05`'s bounded correction resolved the repository's cash figure to
**$941.05** (v1.38 evidence, exact $0.00 reconciliation against
`PHQ-2026-04`'s post-sale cash minus the seven confirmed buy fills). The
principal has since reported a new $100 deposit and supplied a Robinhood
"Account Summary" screenshot as evidence.

Separately, the principal mentioned an earlier connected-account snapshot
showing cash of **$941.23** — $0.18 higher than this repository's own
`PHQ-2026-05`-resolved $941.05. That $0.18 difference is disclosed here as
unresolved; no cause is asserted for it (see Rationale, Uncertainty).

The new screenshot's displayed cash reconciles exactly from the connected
snapshot, not from the repository figure: **$941.23 + $100.00 = $1,041.23**,
matching the screenshot exactly.

**Evidence-access history for this specific screenshot, disclosed in full**:
this session was first told a screenshot supported different figures
($6,315.86 / $315.73 total/crypto, $7,441.11 buying power) than what any
actual accessible file showed. When the actual inline image was inspected,
those three figures did not match (it showed $6,315.34 / $315.18 / $7,444.11
instead) — cash, margin available, and margin used matched throughout. The
session then declined a further instruction to treat an unverified path
(`/mnt/data/image(256).png`, which does not exist in this execution
container) as a retained file, and instead extracted the actual attached
image bytes directly from this session's own conversation transcript
(base64 content, `image/webp`), independently hashed them, and re-inspected
the result. That final, independently-hashed capture displays **$6,315.28 /
$315.12** total/crypto — a further few cents of live-market drift from the
immediately prior capture. **cash ($1,041.23), buying_power ($7,444.11),
margin_available ($6,403.06), and margin_used ($0.00) were identical across
every capture inspected this session** — only total account value and
crypto market value moved, consistent with 24/7 crypto pricing continuing to
move while the equities market was closed. This decision synchronizes cash
only, and relies on the one screenshot that was actually hashed and
retained, not on any earlier verbal approximation. Full detail in
`governance/evidence/PHQ-2026-06/MANIFEST.json`.

## Decision

**Proposed, bounded to exactly the cash fact below — nothing else:**

1. Records the new, retained-screenshot-supported cash figure:
   **$1,041.23**, evidence date 2026-08-01.
2. Makes **no** change to any `shares:` quantity, `crypto_shares:` quantity,
   or the `margin:` block in `holdings.yaml` — none is evidenced by this
   screenshot as having changed, and this screenshot is not treated as a
   full holdings reconciliation (unlike `PHQ-2026-02`'s v1.35 package, which
   was principal-confirmed as a complete post-transition position list).
3. Makes **no** change to `targets.yaml`, `gates.yaml`, or
   `issuer_lookthrough.yaml`.
4. Discloses, without resolving or inventing an explanation for, the $0.18
   difference between the repository's prior resolved cash ($941.05) and the
   earlier connected-account snapshot cash the principal separately
   mentioned ($941.23) — see Rationale, Uncertainty.
5. Records `buying_power` ($7,444.11) and `margin_available` ($6,403.06) as
   evidence-only context, explicitly **not** cash and **not** deployment
   authority of any kind; records `margin_used` ($0.00), consistent with
   `holdings.yaml`'s existing `margin.debt: 0.0`.
6. `holdings.yaml` has no persisted cash schema field (unchanged since
   `PHQ-2026-02`) — this decision updates only `holdings.yaml`'s explanatory
   comment/header, recording the new figure as evidence to be supplied
   through `allocate.py`'s existing `--cash` runtime input at whatever
   future, separate, live-credentialed allocation-check session runs.
7. Retains the supporting screenshot verbatim, hashed, under
   `governance/evidence/PHQ-2026-06/`.

This decision does not run, and does not authorize running, `allocate.py` in
any mode. It recommends no buy, no trim, no margin deployment, and no policy
change.

## Rationale

**FACT** — the retained screenshot's displayed cash ($1,041.23), buying
power ($7,444.11), margin available ($6,403.06), and margin used ($0.00)
were read directly from the one image file this session independently
extracted, hashed, and re-inspected (SHA-256
`d602da67bee33644da8600691974ddd3098549c78c73292904320a16c0e2ffca`), not
from any earlier verbal description of a different, unverifiable capture.
The $100 deposit is a principal-reported fact, not independently observable
from the screenshot alone (a screenshot shows a balance, not a transaction
history), but it is corroborated by the arithmetic: the earlier connected
snapshot cash plus exactly $100.00 equals the new screenshot's cash to the
penny.

**INFERENCE** — none required for the cash figure itself, which is read
directly off the retained image. The characterization of total-account-value
and crypto-market-value drift as "ordinary point-in-time market movement" is
a labeled inference, not a directly observed fact — it is supported by the
figures moving in a small, continuous way consistent with live crypto
pricing (24/7 market) while every other figure held constant across
captures, and by explicit principal instruction to treat that drift as
non-authoritative.

**JUDGMENT** — treating this screenshot as sufficient evidence for a
cash-only synchronization, rather than requiring a full holdings
reconciliation, follows `PHQ-2026-04`'s and `PHQ-2026-05`'s own precedent:
a screenshot that shows only aggregate positions-by-category (Equities Mkt
val, Crypto Mkt val) and account-level figures, with no per-ticker share
list, does not support a share-by-share reconciliation the way `PHQ-2026-02`'s
v1.35 package did, and this filing does not attempt one. The decision to
retain the actual transcript-extracted image rather than accept an
unverifiable claimed path is this session's own judgment, applying this
repository's standing "verify before acting on external review — assume an
outside inference is wrong until verified" guardrail (CLAUDE.md Guardrails)
to a claimed evidence path in exactly the same way that guardrail already
applies to a claimed code behavior or price.

**UNCERTAINTY** — the $0.18 difference between the repository's
`PHQ-2026-05`-resolved cash ($941.05) and the earlier connected-account
snapshot ($941.23) is **not resolved by this filing**. No cause is asserted;
it is disclosed as-is, consistent with `PHQ-2026-05`'s own precedent of
disclosing an unresolved discrepancy rather than fabricating an explanation
for one. Separately, the small drift in total-account-value and
crypto-market-value across the three screenshots inspected this session
means those two figures are non-reproducible past their capture moment —
this filing relies only on the one screenshot it actually retained and
hashed, and does not assert any of the three captures' total/crypto figures
as more "correct" than another; they are simply different, valid,
point-in-time reads of a continuously-moving market value.

## Alternatives Considered

- **Use the figures from an earlier, unverifiable screenshot description
  ($6,315.86 / $315.73 / $7,441.11) rather than the actual retained file.**
  Rejected — those figures were never confirmed against any file this
  session could open, hash, or independently verify; using them would have
  recorded evidence this session could not actually stand behind, contrary
  to this repository's "never hallucinate prices... verify before acting"
  guardrail.
- **Treat the claimed path `/mnt/data/image(256).png` as sufficient and
  fabricate a plausible hash for it.** Rejected outright — this repository's
  evidence discipline explicitly forbids inventing a screenshot hash, and
  doing so would have put a false provenance record into
  `governance/evidence/`.
- **Wait for a filesystem-accessible upload before filing anything.**
  Rejected once a legitimate alternative was found — this session's own
  conversation transcript retains the actual attached image bytes exactly
  as received, extractable and independently hashable without depending on
  a client-side path convention this container does not support. Using that
  path is not a lower evidentiary standard than a direct file upload; it
  recovers the identical bytes the model actually received.
- **Treat this screenshot as a full holdings reconciliation, matching
  `PHQ-2026-02`'s v1.35 precedent.** Rejected — this screenshot shows only
  category-level market values (Equities, Crypto) and account-level
  figures, not a per-ticker share list; it does not support verifying any
  individual position, and this filing does not claim it does.
- **Resolve or explain the $0.18 discrepancy with an inferred cause
  (rounding, interest, timing).** Rejected — no evidence in this session
  establishes a specific cause; asserting one would fabricate a fact not in
  evidence, the same discipline `PHQ-2026-05` applied to its own then-open
  discrepancy before v1.38 resolved it with an exact arithmetic match. This
  discrepancy remains open pending future evidence.
- **Run a live `python allocate.py --review` (or cash-funded) check as part
  of this filing.** Rejected — no live Alpaca credentials are available in
  this session, matching the disclosed limitation in `PHQ-2026-02` through
  `PHQ-2026-05`; this filing performs no allocation run of any kind and
  authorizes none.

## Consequences

- `holdings.yaml`'s explanatory comment/header is updated to record the new
  cash figure, evidence date, deposit amount, and the disclosed $0.18
  discrepancy — no `shares:`, `crypto_shares:`, or `margin:` data field is
  changed. `governance/decisions/PHQ-2026-06-cash-synchronization-100-deposit.md`
  (this file), `governance/decisions.yaml` (one new entry),
  `governance/evidence/PHQ-2026-06/` (new, screenshot retained verbatim plus
  `MANIFEST.json` and `README.md`), `operations/WORKSTREAMS.yaml` (the one
  stale $941.05 reference in `WS-0009`'s `next_action` updated to point to
  this decision's newer figure — no other field of that entry touched, and
  no new workstream created), and `CLAUDE.md` (one concise Decisions Log
  pointer) are the only other files this decision changes.
- No trade, order, margin draw, or brokerage mutation of any kind is
  authorized or performed. No buy or trim recommendation is produced. No
  `allocate.py` run of any kind occurs.
- `buying_power` and `margin_available` are recorded as evidence-only
  context; neither is treated as cash, and neither authorizes any
  deployment. `margin_used` remains $0.00, consistent with
  `holdings.yaml`'s existing `margin.debt: 0.0`.
- No allocator behavior, tier, target, cluster, cap, gate, or
  `issuer_lookthrough.yaml` weight is changed.
- Per this repository's Lean Delivery and Review Lifecycle (`OPS-0009`),
  this filing is classified **Lane M** (mechanical/factual synchronization)
  — it records an already-true, screenshot-evidenced cash figure and
  introduces no new tier/target/cluster/cap/gate/allocator authority. Per
  `OPS-0009` §2, Lane M may omit a separate independent-review round of the
  recording itself, but every other control still applies in full,
  including explicit principal acceptance of the underlying facts before
  merge, protected-path verification, and applicable test/validator
  re-confirmation. This decision does not mark itself ready and does not
  authorize its own merge.
- Effective only on merge; this draft PR is not itself approval, merge, or
  completion.

## Evidence

`governance/evidence/PHQ-2026-06/` — this decision's own retained evidence:

- `robinhood_account_summary_20260801.webp` — the screenshot, retained
  byte-for-byte, not cropped/annotated/recompressed. SHA-256
  `d602da67bee33644da8600691974ddd3098549c78c73292904320a16c0e2ffca`,
  49254 bytes, `image/webp`.
- `MANIFEST.json` — full displayed-figure record, provenance disclosure
  (including the rejected `/mnt/data/` path claim), prior repository and
  connected-snapshot cash figures, the deposit reconciliation, the disclosed
  $0.18 discrepancy, and the point-in-time note on total/crypto drift.
- `README.md` — evidence-directory summary and provenance pointer.

## Limitations

- The $0.18 discrepancy between the repository's `PHQ-2026-05`-resolved cash
  ($941.05) and the earlier connected-account snapshot ($941.23) is
  unresolved. It is not evidence of a trade or quantity change, and no cause
  is asserted; a future filing may resolve it if further evidence is
  supplied, exactly as `PHQ-2026-05`'s v1.37 cash discrepancy was later
  resolved by v1.38.
- This screenshot supports a cash-only synchronization. It does not support,
  and this decision does not attempt, a full share-by-share holdings
  reconciliation.
- No live, credentialed `python allocate.py --review` (or cash-funded) run
  was performed — the same disclosed limitation carried since `PHQ-2026-02`.
  A future, separate, live-credentialed allocation check remains the next
  action once this synchronization merges.
- `holdings.yaml`'s `margin.buffer_pct` (currently `100.0`, representing zero
  margin drawn rather than a Robinhood-displayed screen) is unchanged by
  this decision — this screenshot does not display a maintenance-buffer
  percentage. A real Robinhood-displayed buffer % should still be synced
  before any future margin-funded decision, unchanged standing guidance.

## Bounded correction (same day, this PR) — evidence-provenance precision

An independent review of this PR accepted file scope, the cash
reconciliation, the retained hash, the manifest, the decision text, tests,
validators, and protected-path review, with exactly one MATERIAL finding
remaining: **an independent reviewer cannot prove that the retained WebP is
the exact original principal screenshot, because only the authoring session
had access to the original inline chat bytes.**

**This is not a repository defect — it is an inherent limitation of
independent review of any chat-mediated screenshot evidence, present
identically in every prior `PHQ-####` decision that relies on a
principal-supplied screenshot** (`PHQ-2026-02`'s v1.35 package,
`PHQ-2026-04`'s unretained screenshots, `PHQ-2026-05`'s v1.37/v1.38
packages). No decision in this repository has ever had a mechanism for a
third party to cryptographically prove that a retained artifact is
bit-for-bit identical to what a principal's own device originally rendered
and sent — that link has always rested on principal representation and,
where retained, on principal acceptance of the retained artifact as a
faithful copy. `PHQ-2026-06` does not weaken that standard; if anything it
exceeds `PHQ-2026-04`'s (which retained no image at all) by giving any
reviewer, including the principal, a hash-verifiable artifact to check
against their own original screenshot directly.

To resolve the finding as precisely as possible without altering the
evidence itself, this correction makes the provenance chain's verifiability
boundary explicit — distinguishing exactly which layer each claim belongs
to (also reflected in the same day's corresponding update to
`governance/evidence/PHQ-2026-06/MANIFEST.json` and `README.md`):

1. **Principal-supplied inline image** — what the principal's Robinhood
   client rendered and attached in this Claude Code chat session. This
   layer exists only as what the principal saw and sent; it is not
   independently reconstructable by anyone outside that original exchange,
   including this correction.
2. **Authoring-session extraction** — the authoring session decoded the
   base64 `image/webp` content stored in its own conversation transcript
   (the same bytes the model received as the inline image content block)
   and wrote them to disk. This action required access to that session's
   own transcript state, which a third-party reviewer does not have and
   cannot independently re-execute.
3. **Retained repository artifact** —
   `governance/evidence/PHQ-2026-06/robinhood_account_summary_20260801.webp`
   as committed. This is the one artifact every downstream party, including
   any independent reviewer and the principal, actually has direct access
   to.
4. **Independently verifiable, by anyone with repository access, without
   trusting the authoring session's narrative**: the retained file's
   SHA-256 (`d602da67bee33644da8600691974ddd3098549c78c73292904320a16c0e2ffca`)
   recomputes and matches `MANIFEST.json` exactly; its byte size (49254)
   and media type (`image/webp`) are directly inspectable; and every
   displayed figure this decision relies on (cash $1,041.23, buying power
   $7,444.11, margin available $6,403.06, margin used $0.00, equities
   $4,958.55, crypto $315.12, total $6,315.28) is directly legible by
   opening the retained file and reading it — exactly as the authoring
   session did, and independently reproducible by anyone else who opens it.
5. **Necessarily reliant on principal acceptance, not independently
   provable by any reviewer, including this correction**: that the retained
   artifact (layer 3) is bit-for-bit identical to what the principal's
   client actually rendered and transmitted (layer 1) — i.e., that nothing
   was substituted, corrupted, or altered between the principal's screen
   and the authoring session's extraction — and that the underlying
   Robinhood screen itself was authentic and current when captured. Every
   prior `PHQ-####` screenshot-evidenced decision in this repository carries
   this identical, unavoidable trust boundary; it is resolved the same way
   here as there — by the principal's own review and acceptance of the
   retained artifact as a faithful copy of what they sent, not by any
   technical mechanism this filing could add.

**No change is made to the retained screenshot, its SHA-256, its byte size,
its media type, or any displayed figure.** No governance authority is
broadened or narrowed by this correction — it clarifies wording only. This
correction requires its own exact-head re-review before this decision may
be considered ready, per this repository's standing review discipline for
bounded corrections on an open, unmerged PR.
