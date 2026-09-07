---
decision_id: PI-0018
date: 2026-07-22
status: Accepted
category: portfolio_intelligence
related_decisions: [GOV-0001, PI-0003, PI-0004, PI-0006, PI-0007, PI-0009, PI-0016, PI-0017, ONTO-0001]
supporting_artifact: null
---

## Context

`governance/decisions/PI-0017-nvda-committee-review-authorization.md`
authorized bounded, research-only Investment Committee review activity on
NVDA under `PI-0016`'s standing methodology, naming TSM/ASML/AVGO/MSFT as
the fixed comparator set. That review has now been conducted and produced
a review packet stating both of `PI-0016` §F's required, independent
recommendations: an **advisory policy recommendation of "Keep current
policy"** and an **Intelligence-maintenance recommendation of
"Intelligence refresh recommended."** Per `PI-0016`/`PI-0017`'s own
lifecycle (`PI-0016` §H, `PI-0017` §G), a review packet's findings are not
self-executing — acting on the Intelligence-maintenance recommendation
requires its own separate, later, filed governance authorization before any
implementation may begin. This decision is that separate authorization.

**Provenance of the evidentiary basis, stated precisely.** The human
principal supplied four external artifacts directly to this session as
local file attachments (not fetched from any network location, and not the
same-named archive path referenced in an earlier, unrelated session that
this session found inaccessible and did not rely on):

1. `01_original_packet_20260721_superseded.md` — the first-drafted review
   packet, explicitly marked `SUPERSEDED — DO NOT USE` in its own text,
   preserved for provenance only.
2. `02_independent_audit_report.md` — an independent audit of artifact 1,
   concluding **`REVISE BEFORE PRINCIPAL REVIEW`** on evidentiary-rigor and
   internal-consistency grounds (no fabricated or reversed conclusion, no
   scope/authority violation found).
3. `03_revised_packet_20260722.md` — the canonical, revised review packet,
   dated 2026-07-22, addressing every finding in artifact 2 and adding a
   37-entry claim-level evidence ledger (§16: NVDA `[N1]`–`[N13]`, MSFT
   `[M1]`–`[M6]`, ASML `[A1]`–`[A6]`, AVGO `[B1]`–`[B5]`, repository
   `[R1]`–`[R7]`) satisfying `PI-0016` §D's per-claim sourcing requirement.
4. `04_final_independent_verification_corrected1.md` — a final independent
   verification of artifact 3 against every finding in artifact 2,
   concluding **`READY FOR PRINCIPAL REVIEW`**, with one clerical
   self-correction (the evidence ledger contains 37 entries, not the 31
   originally miscounted — verified directly against artifact 3's own
   §16 by this session, not merely cited from artifact 4).

This session independently opened all four files, computed each one's
SHA256 in full, and confirms:

| Artifact | SHA256 (independently computed this session) |
|---|---|
| 01 (superseded original) | `275cd85ee3cbf13650cba8fc5c2c34f3a49d9b1bbdf97eba64881eb24a73e432` |
| 02 (independent audit) | `f7c60644982e3f2c8b1140a3060bc3473820889ce8572e4be32a8227dd7f3827` |
| 03 (canonical revised packet) | `1dc750a5d2f22f260b1170f687a1b441705a7bae9798c2bc7d842d99a21134e9` |
| 04 (final independent verification) | `6cc19df032d83a31da704eb654f35b9ed91b0662175602a29b00c489f609c15d` |

Artifact 3's independently-computed hash matches the canonical value the
principal identified for it exactly. **This session did not inspect, rely
on, or claim access to any archive path from a different, prior session —
the four artifacts above, supplied directly to this session, are the
entire evidentiary basis for this decision.** No copy of any artifact is
added to this repository by this decision; they remain external review
material, consistent with `PI-0016` §H's convention that a review packet's
narrative may live outside `intelligence/` while its authorized
recommendations are what a downstream governance filing acts on.

**Repository facts, reconfirmed directly by this session immediately
before filing:** `origin/main` and local `HEAD` both at `af85827` (0 ahead
/ 0 behind), working tree clean, no open pull requests on
`Mast3rkey/Portfolio-HQ`, `governance/decisions/PI-0016-...md` and
`PI-0017-...md` both `status: Accepted` in their own frontmatter and in
`governance/decisions.yaml`. `intelligence/companies/NVDA.yaml` and
`NVDA.md` remain exactly as `PI-0007` left them (`conviction.rating: High`,
`review.next_due: 2026-10-16`) — unread for content changes and unmodified
by this decision.

## Decision

**PI-0018 authorizes exactly one thing: a later, separate, bounded
implementation refresh of `intelligence/companies/NVDA.yaml` and
`NVDA.md`, evidence-content only, on its own future branch and PR.** This
decision itself changes neither file. It does not authorize any change to
NVDA's tier, target, holdings, roster, cluster, cap, allocator, or margin
behavior, and it does not authorize a conviction-rating change.

### A. Why a refresh is authorized

The canonical review packet (artifact 3), reconciled against the existing
record per `PI-0016` §C / `PI-0013`'s gate, identifies specific, dated
gaps between `NVDA.yaml`/`.md` (last dated 2026-07-18) and the company's
current disclosed state:

1. **One full reporting cycle is absent.** The existing record cites only
   FY2026 (Q4, reported 2026-02-25). NVIDIA has since reported Q1 FY2027
   (~2026-05-20) — record revenue, accelerating Data Center growth (+92%
   YoY vs. FY2026's +68% YoY), with a second cycle (Q2 FY2027) due
   2026-08-26.
2. **Dividend and buyback developments are absent.** A quarterly dividend
   increase (from $0.01 to $0.25/share) and an additional $80.0B buyback
   authorization (approved 2026-05-18) post-date the existing record and
   are not reflected in it.
3. **Export-control/geopolitical conditions are more active** than the
   existing record's static framing — a January 2026 licensing-policy
   change, continued Blackwell-class restricted status, and a May/June
   2026 extraterritorial-scope guidance change are all more granular and
   more recent than what the existing record captures.
4. **Customer-concentration and several financial details need stronger
   primary-source confirmation.** The review found the current quarter's
   customer-concentration figures, R&D expense detail, and a cash-balance
   figure only via secondary aggregation, with an unreconciled
   operating-income/net-income relationship — precisely the kind of gap a
   refresh with primary-source access should close, per the review's own
   Intelligence-maintenance rationale (artifact 3, §15).

### B. Distinguishing the stages (do not conflate)

This decision exists specifically to keep the following six events
separate and sequential, per `PI-0016`/`PI-0017`'s own lifecycle
discipline:

1. **Committee review completion** — done: artifact 3 is the completed,
   audited, independently re-verified review packet.
2. **Refresh recommendation** — done: artifact 3 §15 states "Intelligence
   refresh recommended," one of `PI-0016` §F's two required, independent
   conclusions.
3. **Governance authorization** — this decision (`PI-0018`), filed now.
   Authorizes the refresh scope below; performs no refresh itself.
4. **Later implementation** — not yet begun. Requires its own branch and
   PR per §E below.
5. **Validation** — not yet performed. Required before merge, per §D
   below.
6. **Merge and effectiveness** — not yet reached. Requires its own
   separate merge decision; this filing does not itself authorize merging
   that future PR.

### C. Authorized refresh scope

A later, separate implementation PR may refresh, within
`intelligence/companies/NVDA.yaml` and `NVDA.md` only, evidence-based
content limited to:

- the newly reported financial period (Q1 FY2027 and any subsequent
  reporting cycle current at implementation time);
- financial-quality and capital-allocation evidence (revenue, margin,
  earnings, dividend, buyback, R&D detail — reconciled to primary sources
  where accessible, per §D);
- export-control and geopolitical-risk evidence;
- customer-concentration evidence;
- competition and supply-chain evidence;
- observable thesis-break conditions (updated factual status only, not a
  redefinition of the existing qualitative framework);
- the source ledger and disclosed access limitations;
- review dates and provenance (`review.last_reviewed`, `review.next_due`,
  `review.log`, consistent with the existing Company Intelligence schema).

No other section of the schema, and no other file, is in scope.

### D. Evidence-standard requirement for implementation

The later implementation must use **current primary sources wherever
accessible**, specifically:

- NVIDIA investor-relations materials;
- SEC filings (10-Q/10-K/8-K and exhibits);
- BIS or other official government sources (export-control actions);
- official earnings materials or transcripts;
- repository-authoritative files (`targets.yaml`, `holdings.yaml`,
  `governance/decisions.yaml`, other Company/Theme Intelligence records)
  for any governed portfolio fact restated in the refreshed record.

**Secondary sources may be retained only when clearly classified as
secondary and only when primary access remains unavailable** at
implementation time — the same access limitation the canonical packet
(artifact 3, §0/§16) discloses for this research environment. If primary
access is available at implementation time where it was not during
research, the implementation must prefer it. Every material claim carried
into the refreshed record must retain (or newly assign) an explicit
classification: established fact, management claim, third-party claim,
committee inference, or unresolved uncertainty — consistent with
`PI-0016` §D and the evidentiary discipline already demonstrated in
artifact 3's §16 ledger. Unresolved items disclosed in artifact 3 (the
cash/operating-cash-flow pairing, exact R&D figures, the
operating-income/net-income relationship) must not be silently resolved
or silently dropped by implementation — either confirm them against a
primary source or retain their unresolved status.

### E. Explicit prohibitions

The later implementation must not, under any interpretation:

- change NVDA's T1 tier or its 3.35% per-name target in `targets.yaml`;
- change `holdings.yaml`, the portfolio roster, any cluster membership, or
  any cluster cap (including the `semis` cluster NVDA belongs to);
- change `allocate.py`, `margin_state.py`, or any margin or allocator
  behavior;
- change any other company's or theme's Company/Theme Intelligence record
  (including `TSM.yaml`/`.md`, cited only as read-only reconciliation
  context in the review);
- propose, imply, or execute any trade or execution instruction;
- change `intelligence_validator.py`, `intelligence_report.py`, or any
  other production module beyond the two named content files;
- amend `constitution/INVESTMENT_CONSTITUTION.md`,
  `docs/INVESTMENT_ONTOLOGY.md`, or `docs/PORTFOLIO_INTELLIGENCE_SPEC.md`.

**`conviction.rating: High` is the authorized baseline and must be
preserved as-is by the refresh.** A conviction-rating change is not
authorized by this decision and must never be inferred merely from
refreshing evidence — the canonical review's own advisory policy
recommendation is "Keep current policy," not a conviction change, and
`PI-0004`'s closed four-value vocabulary (`Low`/`Medium`/`High`/`Very
High`) governs any future rating regardless. If a future human
reviewer separately concludes, while implementing this refresh, that the
rating itself should change, that change requires its own separate,
explicit human approval, filed as its own governance decision or
explicitly folded into a revised implementation authorization — it may
not be made silently inside the refresh this decision authorizes.

No computed or derived conviction value, ranking, score, portfolio
aggregation, or allocator coupling of any kind is authorized by this
decision, consistent with `PI-0016` §E/§I and `ONTO-0001`'s unchanged
boundary.

### F. Required implementation validation (before merge)

The later implementation PR must pass, and its description must record
the exact results of:

1. **`intelligence_validator.py`** run against the refreshed
   `NVDA.yaml` — must pass with zero errors.
2. **Focused, relevant tests** covering NVDA/Company-Intelligence
   validation paths in the existing test suite.
3. **The full applicable test suite** (`pytest` across the repository's
   test files touching `intelligence/`, or the complete suite if that is
   the established convention at implementation time) — must pass in
   full, not merely the focused subset.
4. **YAML parse validation** of the refreshed `NVDA.yaml` (a clean
   `yaml.safe_load` or equivalent, independent of the validator's own
   schema checks).
5. **`git diff --check`** against the implementation branch, confirming
   no whitespace errors.
6. **An exact protected-path and scope review** — a diff enumeration
   confirming the only files changed are `intelligence/companies/
   NVDA.yaml` and `intelligence/companies/NVDA.md` (plus, if the
   implementation branch also carries this decision's own governance
   files forward, no unintended overlap with them) — and confirming, by
   name, that `targets.yaml`, `holdings.yaml`, `allocate.py`,
   `margin_state.py`, every other Company/Theme Intelligence record,
   `intelligence_validator.py`, and `intelligence_report.py` are
   unchanged.

### G. Branch and PR

The later implementation must occur on its **own narrow branch**, separate
from this governance decision's branch, and must open its **own PR** —
this decision's PR does not carry the refresh's implementation.

### H. This decision performs no Intelligence refresh

Filing and accepting `PI-0018` changes no byte of `intelligence/
companies/NVDA.yaml` or `NVDA.md`. It authorizes scope, sourcing
standard, and validation requirements for a future, separate
implementation only.

### I. Append-only governance history

This decision adds one new file and one new `governance/decisions.yaml`
row. No existing decision file, index row, or `CLAUDE.md` Decisions Log
entry is edited or removed by this filing.

## Rationale

Same discipline `PI-0002`→`PI-0003`, `PI-0006`→`PI-0007`, and
`PI-0012`→`PI-0013` already established for this repository's
Intelligence layer: a review or freeze is one governance event, and
authority to implement anything the review recommends is a separate,
later, filed decision. `PI-0016`/`PI-0017` deliberately split "Keep
current policy" from "Intelligence refresh recommended" as two
independent conclusions precisely so that a correct tier/target could
coexist with a record that independently needs newer evidence — this
decision is the missing authorization that lets the second, independent
conclusion actually be acted on, without touching the first.

Requiring current primary sources wherever accessible (§D), while
permitting clearly-classified secondary sources only where primary access
remains unavailable, directly answers the canonical review's own
strongest self-criticism (artifact 3 §0, §15 point 4: "this review's own
evidentiary basis remains weaker than a refresh with working primary-source
access would achieve") without inventing a new evidence standard — it
applies `PI-0016` §D's existing standard and simply insists implementation
try harder for primary access than research, in this instance, was able
to.

Preserving `conviction.rating: High` as an explicit baseline (§E), rather
than leaving it silently implied, follows `PI-0004`'s own closed-vocabulary
discipline and the review's own advisory recommendation ("Keep current
policy") — refreshing evidence is not evidence of a conviction change, and
the two must not be conflated inside a single implementation PR.

`related_decisions` lists `GOV-0001` (the governance-record layer this
file is filed under); `PI-0003`/`PI-0004` (the original Company
Intelligence implementation pattern and closed conviction vocabulary this
refresh must respect); `PI-0006`/`PI-0007` (the Theme Intelligence
authority behind NVDA's existing `ai_infrastructure` reference, unchanged
by this decision); `PI-0009` (the corpus precedent for reconciling
multiple records against the same theme, relevant background only);
`PI-0016` (the standing methodology and evidence standard this refresh's
sourcing requirement extends into implementation); `PI-0017` (the specific
NVDA research authorization whose recommendations this decision acts on);
`ONTO-0001` (the vocabulary boundary this decision's prohibitions
reaffirm, unchanged and unextended).

## Alternatives Considered

- **Treat the review packet's own recommendation as sufficient
  authorization to implement the refresh directly.** Rejected:
  `PI-0016` §H / `PI-0017` §G are explicit that a review's findings are
  not self-executing and that acting on them requires its own separate,
  filed authorization — exactly what this decision supplies.
- **Fold conviction-rating reconsideration into this authorization**,
  since the review touched NVDA's thesis in depth. Rejected: the review's
  own advisory recommendation is "Keep current policy," not a rating
  change, and `PI-0004`'s vocabulary discipline requires any rating
  change to rest on its own explicit human approval, not be inferred from
  an evidence refresh.
- **Authorize a broader refresh scope** (e.g., allowing the implementation
  to also revise the qualitative thesis narrative wholesale, not just
  evidence sections). Rejected: the canonical review's own findings are
  evidence-and-currency gaps, not a thesis reversal — scoping the
  authorization to evidence content keeps the refresh proportional to
  what was actually found, consistent with `PI-0003`'s original "no more
  than what was justified" discipline.
- **Skip independent SHA256 verification of the supplied artifacts and
  rely on the principal's stated values.** Rejected: this repository's
  own standing guardrail ("verify before acting on external review") and
  this decision's own evidentiary-integrity purpose both require this
  session to independently compute, not merely echo, the hash it cites as
  matching.
- **Cite the archive path referenced by an earlier, unrelated session as
  though it had been inspected here.** Rejected outright: that path was
  never accessible to this session, and this decision's provenance
  section states plainly that the four locally-supplied artifacts, not
  that path, are its evidentiary basis.

## Consequences

**Changes:** `governance/decisions.yaml` gains one new row for `PI-0018`.
`CLAUDE.md`'s Decisions Log gains one short pointer entry.

**Does not change:** `intelligence/companies/NVDA.yaml`, `NVDA.md`, any
other Company or Theme Intelligence record, `targets.yaml`,
`holdings.yaml`, any tier, target, roster, cluster, or cap,
`allocate.py`, `margin_state.py`, `intelligence_validator.py`,
`intelligence_report.py`, `constitution/INVESTMENT_CONSTITUTION.md`,
`docs/INVESTMENT_ONTOLOGY.md`, `docs/PORTFOLIO_INTELLIGENCE_SPEC.md`, any
existing governance decision file, or any trade/execution state.

**Enables:** a future, separate, narrowly-scoped implementation PR,
subject to the sourcing standard (§D), prohibitions (§E), and validation
requirements (§F) above, and its own separate merge decision.
