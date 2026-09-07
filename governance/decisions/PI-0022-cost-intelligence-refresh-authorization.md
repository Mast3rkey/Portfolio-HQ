---
decision_id: PI-0022
date: 2026-07-23
status: Accepted
category: portfolio_intelligence
related_decisions: [GOV-0001, PI-0003, PI-0004, PI-0016, PI-0018, PI-0020, PI-0021, TGT-0002, ONTO-0001]
supporting_artifact: null
---

## Context

`governance/decisions/PI-0021-cost-committee-review-authorization.md`
authorized bounded, research-only Investment Committee review activity on
COST under `PI-0016`'s standing methodology, naming WMT/AMZN/BRK.B/V as
the fixed comparator set. That review has now been conducted and produced
a review packet stating both of `PI-0016` §F's required, independent
recommendations: an **advisory policy recommendation of "Keep current
policy"** and an **Intelligence-maintenance recommendation of
"Intelligence refresh recommended."** Per `PI-0016`/`PI-0021`'s own
lifecycle (`PI-0016` §H, `PI-0021` §G), a review packet's findings are not
self-executing — acting on the Intelligence-maintenance recommendation
requires its own separate, later, filed governance authorization before
any implementation may begin. This decision is that separate
authorization.

**Provenance of the evidentiary basis, stated precisely.** The human
principal supplied exactly two external artifacts directly to this
session as local file attachments:

- `COST_committee_review_packet_20260723_principal_review_v5.md` — the
  canonical, final (v5) COST committee-review packet. SHA256
  `6ae2aa232cf6b891ae25135e4b6a5c88b90da6dfea3b70f44d28a328d7c8170a`,
  independently computed in full by this session and matching the
  principal-identified expected value exactly. Measurements independently
  taken by this session under `LC_ALL=C.UTF-8 wc -l -w -c`: **543 lines,
  13,830 words, 111,839 bytes**, matching the principal-identified
  expected values exactly. Encoding independently confirmed UTF-8.
- `COST_committee_review_packet_20260723_principal_review_v5.sha256` —
  the accompanying SHA256 manifest, whose single recorded hash matches
  both the expected value and this session's independent computation.

The packet's conclusion, quoted from its own §2 and restated in §4.14/
§4.15: **"Advisory policy recommendation: Keep current policy."** and
**"Intelligence-maintenance recommendation: Intelligence refresh
recommended."**, each stated as exactly one value from `PI-0016` §F's
two closed vocabularies, each explicitly marked **"Neither is
self-executing (§16)."** The packet's own status line correctly
describes itself as "not a governance filing, not self-executing, not
principal-approved" — principal approval is an event outside the
packet, and it has now occurred: **the human principal explicitly
approved the final v5 packet and accepted both recommendations**, and
explicitly authorized preparing and filing this separate governance
decision. That approval authorizes this filing only — it does not
authorize the refresh implementation itself, and it does not authorize
merging any future implementation PR.

Recorded for precision, per this repository's verify-before-acting
guardrail: the v5 packet contains no "READY FOR PRINCIPAL REVIEW" audit
verdict string (the form `PI-0018`'s and `PI-0020`'s separate audit
artifacts used). Its verification chain is instead internal and
disclosed in its own text: five versions (v1→v5), each correction pass
logged in §0/§0.1–§0.3, prior-version SHA256s pinned in §17, and an
independent external audit that directly inspected the load-bearing
primary documents (classified `PRIMARY — INDEPENDENTLY INSPECTED DURING
EXTERNAL AUDIT; AUTHORING ENVIRONMENT ACCESS-BLOCKED`), with the
authoring environment itself rendering no primary document (its §13/
U-09 disclosure). This decision records the packet's actual conclusion
language rather than an audit-verdict string the artifact does not
contain. The four superseded versions (v1–v4) were not supplied to this
session and are not relied on; the v5 artifact and its manifest, both
independently hash-verified here, are the entire evidentiary basis. No
copy of either artifact is added to this repository by this decision —
they remain external review material, consistent with `PI-0018`/
`PI-0020`'s convention that a review packet's narrative lives outside
`intelligence/` while its authorized recommendations are what a
downstream governance filing acts on.

**Repository facts, reconfirmed directly by this session immediately
before filing:** `origin/main` and local `HEAD` both at
`ac68e88e9fd91408da67d92c26658ecd33336b69` (0 ahead / 0 behind — the
PR #133 merge commit that accepted `PI-0021`), working tree clean, no
open pull requests on `Mast3rkey/Portfolio-HQ`, no `PI-0022` reference
anywhere in the repository (decision ID free), `PI-0016` and `PI-0021`
both `status: Accepted` in their own frontmatter and in
`governance/decisions.yaml`, and unsuperseded. The packet's own
repository-fact reconciliation (§3, RC-1–RC-15) was pinned to this same
commit; this session independently re-verified the load-bearing rows
against the live files: COST in `targets.yaml`'s T1 list at the 3.35%
per-name weight; `holdings.yaml` COST `0.227127` shares;
`intelligence/companies/COST.yaml` with `portfolio_role_ref: T1`,
`conviction.rating: High`, `review.last_reviewed: 2026-07-17`,
`review.next_due: 2026-10-15`; and the record containing no dividend
figure, no litigation reference, and no digital-comparable-sales figures
(RC-15). `intelligence/companies/COST.yaml` and `COST.md` remain exactly
as the `PI-0003`-created, `TGT-0002`-role-reconciled record left them —
unmodified by this decision.

## Decision

**PI-0022 authorizes exactly one thing: a later, separate, bounded
implementation refresh of `intelligence/companies/COST.yaml` and
`COST.md`, evidence-content only, on its own future branch and PR.**
This decision itself changes neither file. It does not authorize any
change to COST's tier, target, holdings, roster, cluster, cap,
allocator, or margin behavior, and it does not authorize a
conviction-rating change.

**"Keep current policy" is accepted as the principal's advisory-policy
decision.** It requires no change and none is made — COST remains T1 at
its 3.35% per-name target, exactly as `targets.yaml` already encodes
under `TGT-0002`. This decision acts on the second, independent
conclusion only.

### A. Why a refresh is authorized

The packet, reconciled against the existing record per `PI-0016` §C /
`PI-0013`'s gate at the same commit this filing verified live,
identifies specific, dated, material facts absent from
`COST.yaml`/`COST.md` — with the timing stated honestly by the packet
itself: these are evidence-scope gaps of the record's narrow original
research base (largely predating its 2026-07-17 review stamp), not
post-review developments, and the refresh case stands either way
(packet §4.15):

1. **No dividend information at all** — the record contains no dividend
   figure, while a regular-dividend increase from $1.30 to $1.47 per
   quarter (+13.1%, committee arithmetic on the two named rates) was
   announced 2026-04-15, with the next regular $1.47 dividend declared
   2026-07-08.
2. **The June 2026 sales release (2026-07-08) and the monthly-sales
   picture** — including the corrected decomposition of the May→June
   comp deceleration (headline −3.7pp, 12.5% → 8.8%; core ex-gas/FX a
   real but modest −1.0pp, 8.0% → 7.0%) and May 2026 sales evidence.
3. **The confirmed digital-comparable-sales series** — the Q1–Q3 FY2026
   e-commerce/digital comparable-sales figures the record explicitly
   excluded "pending confirmation of their exact reporting period"; the
   periods and figures are now confirmed across named sources and can be
   added with proper citations at refresh.
4. **The *Stockov v. Costco* tariff-refund litigation** (N.D. Ill. No.
   1:26-cv-02734, filed 2026-03-11; motion to dismiss filed May 2026;
   ripeness contested July 2026; no class certified) — absent from the
   record entirely, despite the record's own tariff-exposure risk entry.
5. **The 2024–25 labor-relations history** — unfair-labor-practice
   charges (2024-12-04), the national strike-authorization result
   (2025-01-20), the strike averted under a new national agreement
   (2025-02-01 through 2028-01-31, subsequently described by the
   Teamsters as ratified), and the narrower, still-open June 2025
   Local 174 wage-theft complaint (~150 drivers, retroactive pay) —
   directly relevant to the record's labor-cost risk entry, which
   currently carries no factual anchor.
6. **The Kirkland Signature scale figure**, now multi-source
   corroborated.
7. **The current warehouse count** — the record carries 914 (FY2025);
   the June 2026 release states 933 currently operated.

The packet's currency assessment also confirms what remains valid: the
thesis, the four competitive advantages with counterarguments, the
conviction rationale, the review-framework triggers, and the
renewal-rate narrative — nothing found contradicts them. A refresh is
recommended because real, dated, material developments exist that the
record does not reflect — the same category of gap that produced the
NVDA (`PI-0018`) and GEV (`PI-0020`) refresh authorizations — not
because the existing thesis is judged wrong.

### B. Distinguishing the stages (do not conflate)

Per the same lifecycle discipline as `PI-0018` §B / `PI-0020` §B:

1. **Committee review completion** — done: the v5 packet, with its
   internally-logged v1→v5 audit and correction chain.
2. **Recommendations made** — done: "Keep current policy" (§F.1) and
   "Intelligence refresh recommended" (§F.2), stated in the packet,
   neither self-executing.
3. **Principal acceptance of both recommendations** — done: explicit,
   conveyed with the authorization to prepare this filing.
4. **Governance authorization** — this decision (`PI-0022`), filed now.
   Authorizes the refresh scope below; performs no refresh itself.
5. **Later implementation** — not yet begun. Requires its own branch and
   PR per §G below.
6. **Validation** — not yet performed. Required before merge, per §F
   below.
7. **Merge and effectiveness** — not yet reached and **not authorized by
   this filing**. The future implementation PR requires its own
   independent review and its own separate merge authorization.

### C. Authorized refresh scope

A later, separate implementation PR may refresh, within
`intelligence/companies/COST.yaml` and `COST.md` only, evidence-based
content limited to:

- current financial and membership evidence (net sales, membership-fee
  income, renewal rates, paid-member counts, and the reporting periods
  now current);
- the confirmed Q1–Q3 FY2026 digital-comparable-sales series;
- May and June 2026 sales evidence, including the ex-gas/FX
  decomposition of the June deceleration;
- the April 2026 regular-dividend increase ($1.30 → $1.47/quarter,
  announced 2026-04-15) and subsequent regular declarations;
- current warehouse count and expansion evidence (including the
  933-warehouse June 2026 figure and the FY2026 expansion guidance the
  record already carries as a catalyst);
- labor-relations history (the 2024–25 ULP/strike-authorization/
  national-agreement sequence) and the unresolved Local 174 wage-theft
  complaint's factual status;
- the *Stockov v. Costco* tariff-refund litigation, with the
  complaint's allegations and the procedural facts (filing date, motion
  to dismiss, ripeness argument, certification status) clearly
  distinguished at all times — allegations must never be written as
  established conduct;
- Kirkland Signature / private-label evidence only where independently
  supportable at implementation time;
- risks and observable thesis-break-condition factual status (updated
  factual status only, not a redefinition of the existing qualitative
  framework);
- the source ledger, disclosed access limitations, review dates, and
  provenance (`review.last_reviewed`, `review.next_due`, `review.log`,
  consistent with the existing Company Intelligence schema);
- any subsequent reporting period current at implementation time (e.g.
  Q4 FY2026 if reported by then), provided it is independently verified
  at the §D standard and remains within this same bounded refresh
  purpose.

No other section of the schema, and no other file, is in scope.

### D. Evidence-standard requirement for implementation

The later implementation must **independently inspect current primary
sources wherever accessible**. The v5 packet's prior external audit
inspection of selected primary documents is provenance for the packet —
**it is not a substitute for implementation-time verification**: any
fact actually entering the repository through the refresh must be
independently checked by the implementation session itself against
current primary sources, exactly as the packet's own §4.15 requires.

Priority sources, in order of preference:

- Costco Investor Relations materials;
- Costco SEC filings and exhibits (10-K/10-Q/8-K);
- official earnings materials and transcripts;
- official Teamsters or relevant government/labor-agency documents (e.g.
  Washington State L&I) for the labor-relations facts;
- the court docket and filings for *Stockov v. Costco* (N.D. Ill. No.
  1:26-cv-02734) for the litigation facts;
- repository-authoritative files (`targets.yaml`, `holdings.yaml`,
  `governance/decisions.yaml`, other Company/Theme Intelligence records)
  for any governed portfolio fact restated in the refreshed record.

Secondary sources may be retained only when clearly and explicitly
classified as secondary and only when primary access remains unavailable
at implementation time — the same access limitation both the existing
record and the packet disclose. If primary access is available at
implementation time where it was not during research, the implementation
must prefer it. Every material claim carried into the refreshed record
must retain (or newly assign) an explicit classification — established
fact, management claim, third-party claim, committee inference, or
unresolved uncertainty — per `PI-0016` §D and the packet's own §18
ledger discipline. Packet-specific obligations bind the implementation:

1. **The flagged CEO tariff-refund pledge [packet C-15] must not enter
   the record without primary confirmation** — it is a single-source,
   headline-level secondary report of a Q2 FY2026 earnings-call
   statement, and the packet requires primary verification against the
   Q2 transcript before it may enter any record.
2. **The free-cash-flow and buyback detail [packet U-03, U-04] remain
   unresolved unless confirmed from primary financial statements** — no
   reproducible FY2026 FCF or buyback figure was found from an
   identifiable source during the review, and the refreshed record must
   not assert either, in either direction, without primary
   cash-flow-statement (or proxy) confirmation.
3. **Complaint allegations must never be written as established
   conduct** — the *Stockov* complaint's assertions remain allegations;
   the record must preserve that distinction in every reference.
4. **Unresolved items must not be silently resolved or omitted** — the
   packet's disclosed unresolved uncertainties (its §12, U-01 through
   U-09, as applicable to content actually carried into the record) must
   either be confirmed against a primary source or retained with their
   unresolved status stated; and the single-source items the packet's
   own audit passes removed (its §0.3 list) must not enter the record
   without the independent verification those passes found lacking.

### E. Explicit prohibitions

The later implementation must not, under any interpretation:

- change COST's T1 tier or its 3.35% per-name target in `targets.yaml`;
- change `holdings.yaml`, the portfolio roster, any cluster membership,
  or any cluster cap;
- execute, propose, imply, or instruct any trade, order, buy, trim, or
  execution action;
- change `allocate.py`, `margin_state.py`, or any margin or allocator
  behavior;
- change any other company's or theme's Company/Theme Intelligence
  record, or create any new comparator Intelligence record (none exists
  for WMT/AMZN/BRK.B/V and none is authorized);
- change `intelligence_validator.py`, `intelligence_report.py`, any
  report generator, any test file, or any other production module beyond
  the two named content files;
- amend `constitution/INVESTMENT_CONSTITUTION.md`,
  `docs/INVESTMENT_ONTOLOGY.md`, or
  `docs/PORTFOLIO_INTELLIGENCE_SPEC.md`;
- introduce any computed or derived conviction value, numeric score,
  ranking, league table, portfolio aggregation, or allocator coupling of
  any kind, consistent with `PI-0016` §E/§I and `ONTO-0001`'s unchanged
  boundary;
- treat this authorization as automatic implementation, or treat the
  future implementation PR as pre-authorized to merge.

**`conviction.rating: High` is the authorized baseline and must be
preserved as-is by the refresh.** A conviction-rating change is not
authorized by this decision and must never be inferred merely from
refreshing evidence — the packet's own advisory policy recommendation,
accepted by the principal, is "Keep current policy," and `PI-0004`'s
closed four-value vocabulary governs any future rating regardless. If a
future human reviewer separately concludes that the rating itself should
change, that change requires its own separate, explicit human approval —
it may not be made silently inside the refresh this decision authorizes.

**This governance filing itself modifies no tier, target, conviction,
allocation, or Intelligence content** — it adds one decision file, one
index row, and one `CLAUDE.md` pointer entry, and nothing else.

### F. Required implementation validation (before merge)

The later implementation PR must pass, and its description must record
the exact results of:

1. **`intelligence_validator.py`** run against the refreshed `COST.yaml`
   — must pass with zero errors.
2. **Focused, relevant tests** covering Company-Intelligence validation
   paths in the existing test suite.
3. **The full applicable test suite** — must pass in full, not merely
   the focused subset.
4. **YAML parse validation** of the refreshed `COST.yaml` (a clean
   `yaml.safe_load` or equivalent, independent of the validator's own
   schema checks).
5. **`git diff --check`** against the implementation branch, confirming
   no whitespace errors.
6. **An exact protected-path and scope review** — a diff enumeration
   confirming the only files changed are
   `intelligence/companies/COST.yaml` and
   `intelligence/companies/COST.md`, and confirming, by name, that
   `targets.yaml`, `holdings.yaml`, `allocate.py`, `margin_state.py`,
   every other Company/Theme Intelligence record,
   `intelligence_validator.py`, and `intelligence_report.py` are
   unchanged.

The implementation PR additionally requires its own independent review
and its own separate merge authorization — passing this validation suite
is necessary, not sufficient, for merge.

### G. Branch and PR

The later implementation must occur on its **own narrow branch**,
separate from this governance decision's branch, and must open its
**own PR** — this decision's PR does not carry the refresh's
implementation.

### H. This decision performs no Intelligence refresh

Filing and accepting `PI-0022` changes no byte of
`intelligence/companies/COST.yaml` or `COST.md`. It authorizes scope,
sourcing standard, and validation requirements for a future, separate
implementation only. Implementation has not begun; validation has not
begun; merge of the future implementation PR is not authorized by this
filing.

### I. Append-only governance history

This decision adds one new file and one new `governance/decisions.yaml`
row. No existing decision file, index row, or `CLAUDE.md` Decisions Log
entry is edited or removed by this filing.

## Rationale

Same discipline `PI-0017`→`PI-0018` and `PI-0019`→`PI-0020`
established: a completed, verified review is one governance event, and
authority to implement what it recommends is a separate, later, filed
decision. `PI-0016`/`PI-0021` deliberately split "Keep current policy"
from "Intelligence refresh recommended" as two independent conclusions
precisely so a correct tier/target can coexist with a record that
independently needs newer evidence — this decision is the authorization
that lets the second conclusion be acted on without touching the first.

The packet-specific §D obligations (primary confirmation before C-15
enters, U-03/U-04 held unresolved absent primary confirmation,
allegations-versus-conduct discipline for the litigation, and the
no-silent-resolution rule) exist because they were the substance of the
packet's own five-version correction cycle — v2's audit removed
single-source and irreproducible claims, v3 upgraded load-bearing
figures to external-audit primary inspection, and v4/v5 corrected the
evidence-classification and provenance wording. An implementation that
copied the content while dropping those boundaries would undo the
correction the audit chain paid for.

Preserving `conviction.rating: High` as an explicit baseline follows
`PI-0018`/`PI-0020`'s precedent and `PI-0004`'s closed-vocabulary
discipline: refreshing evidence is not evidence of a conviction change,
and the accepted advisory recommendation is "Keep current policy," not a
rating change.

`related_decisions` lists `GOV-0001` (the governance-record layer this
file is filed under); `PI-0003` (the pilot authorization that created
COST's original record, whose disclosed source-access limitation frames
this refresh's evidence standard); `PI-0004` (the closed conviction
vocabulary and pilot-closure discipline this refresh must respect);
`PI-0016` (the standing methodology and two-vocabulary recommendation
structure this decision acts under); `PI-0018`/`PI-0020` (the two prior
refresh authorizations whose structure and lifecycle discipline this
decision follows); `PI-0021` (the specific COST research authorization
whose recommendations this decision acts on); `TGT-0002` (the separate
tier decision that governs COST's current T1/3.35% placement, reported
here as context and left untouched); `ONTO-0001` (the vocabulary
boundary this decision's prohibitions reaffirm, unchanged and
unextended). `PI-0006`/`PI-0007`/`PI-0009` are deliberately not listed:
COST's record carries no `themes:` reference, so the Theme Intelligence
lineage is not implicated by this refresh.

## Alternatives Considered

- **Treat the packet's recommendation plus the principal's approval as
  sufficient authorization to implement the refresh directly.**
  Rejected: `PI-0016` §H / `PI-0021` §G are explicit that review
  findings are not self-executing; the `PI-0018`/`PI-0020` pattern
  requires a filed, repository-auditable authorization, which is what
  this decision supplies — the principal's approval is its basis, this
  filing is its record.
- **Fold conviction-rating reconsideration into this authorization.**
  Rejected: the accepted advisory recommendation is "Keep current
  policy"; a rating change needs its own explicit human approval.
- **Authorize a broader refresh scope** (wholesale thesis-narrative
  revision). Rejected: the packet's findings are evidence-and-currency
  gaps, not a thesis reversal — its own §4.15 states the thesis, the
  competitive advantages, the conviction rationale, and the
  review-framework triggers all remain valid; the authorization stays
  proportional to what was actually found.
- **Commit the review packet or its manifest into the repository as a
  supporting artifact.** Rejected: `PI-0018`/`PI-0020` established the
  convention that review-packet narratives remain external, the
  principal's instruction for this filing states it explicitly, and the
  packet's identity is pinned here by its independently computed SHA256
  and exact measurements instead.
- **Record a "READY FOR PRINCIPAL REVIEW" audit verdict as the packet's
  conclusion.** Rejected on verify-before-acting grounds: this session
  searched the v5 artifact and that string does not appear in it — the
  packet's verification chain is its internal, hash-pinned v1→v5
  audit-and-correction log plus the external audit's primary
  inspections, and its actual conclusion is the two §F recommendations
  quoted in Context. This decision records what the artifact actually
  says.
- **Skip independent verification of the artifact's hash and
  measurements and rely on the principal's stated values.** Rejected:
  this repository's standing "verify before acting on external review"
  guardrail requires this session to independently compute, not merely
  echo, the identity values it cites as matching — which it did (SHA256,
  line/word/byte counts, UTF-8 check, recommendation text, and
  non-self-executing lifecycle language all independently confirmed).

## Consequences

**Changes:** `governance/decisions.yaml` gains one new row for
`PI-0022`. `CLAUDE.md`'s Decisions Log gains one short pointer entry.

**Does not change:** `intelligence/companies/COST.yaml`, `COST.md`, any
other Company or Theme Intelligence record, `targets.yaml`,
`holdings.yaml`, any tier, target, roster, cluster, or cap,
`allocate.py`, `margin_state.py`, `intelligence_validator.py`,
`intelligence_report.py`, any test file,
`constitution/INVESTMENT_CONSTITUTION.md`, `docs/INVESTMENT_ONTOLOGY.md`,
`docs/PORTFOLIO_INTELLIGENCE_SPEC.md`, any existing governance decision
file, or any trade/execution state. COST's conviction rating remains
`High`; COST remains T1 at 3.35%.

**Enables:** a future, separate, narrowly-scoped implementation PR,
subject to the sourcing standard and packet-specific obligations (§D),
prohibitions (§E), and validation requirements (§F) above, and its own
separate, independent review and merge authorization.
