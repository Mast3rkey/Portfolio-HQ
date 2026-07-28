---
decision_id: PI-0033
date: 2026-07-28
status: Proposed
category: portfolio_intelligence
related_decisions: [GOV-0001, GOV-0002, OPS-0001, OPS-0006, OPS-0007, OPS-0008, OPS-0009, PI-0011, PI-0013, PI-0014, PI-0016, PI-0027, PI-0029, PI-0031, PI-0032]
supporting_artifact: null
---

## Context

`PI-0031` §K defined the Milestone 3 completion standard and, as part of stating it, named the
governed roster's then-remaining gaps precisely: five non-deferred T2 names (CEG, BRK.B, WMT, MLM,
AAPL) and one `semis`-cluster name (WDC) with no deferral rationale on record (addressed by `PI-0032`,
filed alongside this decision in the same governance PR), and three names already explicitly deferred
by accepted authority (DHR, SYK per `PI-0014`; EQIX per `PI-0027`). `PI-0031` §K did not, however,
enumerate or individually reason through every remaining `band`- and `spec`-tier holding that has
never been named in any batch authorization, deferral, or exclusion decision. This decision performs
that enumeration and assigns each remaining name an individually reasoned disposition, so that a
future reader evaluating `PI-0031` §K criterion 4 — "every remaining uncovered company is covered,
explicitly deferred by accepted authority with rationale, or assigned to an approved alternative
research architecture" — has a complete, auditable record rather than an implicit gap.

### Preflight (independently verified this session, not assumed — shared with `PI-0032`)

This decision shares `PI-0032`'s preflight in full (repository identity, `origin/main` at
`db43d8b0e71dcf8915f74d81703e5fe260ecd6ce`, zero open PRs, 39 covered companies, `governance/
decisions.yaml` reconciliation at 43=43 before this filing, `PI-0033` confirmed the next unused
number after `PI-0032`) — not restated in full here. The fact specific to this decision: **independent
re-derivation of every `band`- and `spec`-tier ticker against the full `intelligence/companies/`
inventory** confirms exactly fourteen names carry no Company Intelligence record, no batch
authorization, and no deferral decision of any kind: **CAT, GNRC, NFLX, SHOP, UBER, HOOD, RTX, DELL,
PLTR, SPCX, RKLB, TSLA, BABA, UNH.** Cross-checked against `targets.yaml`: CAT, GNRC, UBER, HOOD, RTX,
DELL, BABA, UNH are `band` tier (0.75% target, 1.25x cap, RSI-gated opportunistic trim above cap);
NFLX, SHOP are also `band` tier; PLTR, SPCX, RKLB, TSLA are `spec` tier (1.0% fixed target, no RSI
gate on trims). None of the fourteen is a member of any `caps.clusters` correlated-cluster cap
(`semis`, `power_infra`, `oil`) and none is referenced by either existing Theme Intelligence record
(`ai_infrastructure`, `life_sciences_tools_medtech`).

## Decision

**PI-0033 authorizes no research of any kind.** It records fourteen new, individually reasoned
Company Intelligence coverage dispositions and restates, without altering, three already-accepted
deferrals — closing the roster-completeness accounting `PI-0031` §K criterion 4 requires, without
performing, commissioning, or scheduling any research itself. **This filing is Lane G (Governance
authorization) under `OPS-0009` §1** — full weight, no reduction, filed together with `PI-0032` in the
same governance PR as its own separate file, per this repository's established
two-decisions-in-one-PR convention (`OPS-0008`/`PI-0027` precedent).

**Arithmetic, stated precisely and controlling over any contrary reading: this decision newly
dispositions fourteen (14) names — CAT, GNRC, NFLX, SHOP, UBER, HOOD, RTX, DELL, PLTR, SPCX, RKLB,
TSLA, BABA, and UNH — and separately restates, without editing or reopening, three (3) already-accepted
deferrals — DHR, SYK, and EQIX. Fourteen plus three is seventeen (17) names represented in this
decision in total. UNH is one of the fourteen newly dispositioned names, not a fifteenth name added
to the fourteen — any description of this decision's scope as "14 names plus UNH" is incorrect and is
not this decision's own characterization of itself.**

### A. Fourteen new dispositions

Each entry below states, individually: current materiality assessment; reason research is deferred;
a company-specific reopening trigger; and whether that trigger includes tier promotion, materially
increased position size, cluster/cap reconsideration, a company-specific disclosure event, or a future
coherent research wave. **No entry below is a substitute for any other — a generic trigger is not used
in place of company-specific reasoning anywhere in this section.**

1. **CAT** (`band`, 0.75% target). *Materiality*: small, capped position (0.75% target, 1.25x ceiling);
   already named once in this repository's own history — the `power_infra` correlation scan found CAT
   correlated with GEV/ETN/VRT/PWR but explicitly excluded it from that cap on fundamental-fit grounds
   (CLAUDE.md: "more likely riding bull-market beta than the specific power-buildout mechanism").
   *Deferral reason*: no coherent economic-mechanism wave currently exists for CAT — it does not share
   a genuine driver with any currently uncovered band/spec name, and forcing it into an artificial
   pairing would violate `OPS-0008` §1's coherence requirement. *Reopening trigger*: (a) a future
   correlation re-scan finding CAT's fundamental fit to `power_infra` has strengthened rather than
   weakened; (b) promotion to a higher tier; (c) a materially increased position size; (d) a future
   coherent industrials-sector research wave naming CAT alongside genuinely related machinery/heavy-
   equipment holdings, none of which currently exist in this roster.
2. **GNRC** (`band`, 0.75% target). *Materiality*: small, capped position; backup-power/generator
   manufacturer with plausible but unexamined adjacency to the `power_infra` theme (data-center and
   grid-resilience demand) that has never been formally scanned. *Deferral reason*: no correlation scan
   or coherent wave has ever examined GNRC specifically — unlike CAT, GNRC was never even included in
   the original `power_infra` correlation scan, so there is no existing evidence to act on either way.
   *Reopening trigger*: (a) a future correlation scan formally testing GNRC against `power_infra`
   member returns or against a power-resilience/backup-generation economic thesis; (b) tier promotion;
   (c) materially increased position size; (d) a future coherent power/energy-infrastructure-adjacent
   research wave.
3. **NFLX** (`band`, 0.75% target). *Materiality*: small, capped position; standalone
   streaming-media/content economics with no genuine shared driver among any currently covered or
   uncovered holding — `PI-0030`'s enterprise-software/cybersecurity batch explicitly did not include
   NFLX, and no theme references it. *Deferral reason*: no coherent economic-mechanism wave exists;
   media/streaming/content is a distinct sub-industry from every existing batch's mechanism (semis,
   memory, compute/networking, power infrastructure, hyperscaler AI infrastructure, financial
   infrastructure, biopharmaceuticals, enterprise software/cybersecurity). *Reopening trigger*: (a)
   tier promotion; (b) materially increased position size; (c) a future coherent media/consumer-
   internet/streaming research wave, which would require at least one other currently-uncovered
   comparably-themed holding to reach `OPS-0008` §1's default wave size (none currently exists on this
   roster) or its own smaller-wave justification.
4. **SHOP** (`band`, 0.75% target). *Materiality*: small, capped position; e-commerce-infrastructure/
   platform economics, plausibly adjacent to AMZN's marketplace business (covered, `PI-0027`) but a
   structurally different role (platform-as-a-service to merchants versus AMZN's own direct
   retail/marketplace/cloud operations) that has never been formally compared. *Deferral reason*: no
   coherent wave currently exists — a two-company SHOP/AMZN pairing would not meet `OPS-0008` §1's
   coherence bar given AMZN's business is dominated by AWS/retail economics far broader than e-commerce
   platform tooling, and AMZN's own record is not being reopened or expanded by this decision.
   *Reopening trigger*: (a) tier promotion; (b) materially increased position size; (c) a future
   coherent e-commerce-infrastructure/digital-commerce-platform research wave, naming SHOP alongside
   any future comparably-themed addition to the roster; (d) a company-specific disclosure event
   (e.g. a material change to SHOP's merchant-concentration or payments-attach economics).
5. **UBER** (`band`, 0.75% target). *Materiality*: small, capped position; ride-hailing/delivery
   platform economics, gig-labor-model exposure with regulatory sensitivity distinct from every
   currently covered holding. *Deferral reason*: no coherent economic-mechanism wave exists — no other
   currently uncovered holding shares UBER's specific gig-platform/mobility-and-delivery mechanism.
   *Reopening trigger*: (a) tier promotion; (b) materially increased position size; (c) a
   company-specific disclosure event (e.g. a material gig-worker-classification regulatory ruling or
   a material change to UBER's profitability trajectory); (d) a future coherent
   mobility/gig-platform research wave.
6. **HOOD** (`band`, 0.75% target). *Materiality*: small, capped position; notable because it is the
   brokerage this account itself is manually executed on (`CLAUDE.md` Identity & Role: "I execute
   manually on Robinhood") — a structural, non-investment-thesis fact worth flagging explicitly so a
   future reader does not read the absence of research as an oversight of that connection. *Deferral
   reason*: no coherent economic-mechanism wave exists for HOOD as a fintech/brokerage-platform
   holding; the operational fact that HOOD is also this account's execution venue is unrelated to and
   does not itself justify or accelerate any investment-thesis research priority. *Reopening trigger*:
   (a) tier promotion; (b) materially increased position size; (c) a future coherent
   fintech/consumer-brokerage-platform research wave; (d) a company-specific disclosure event material
   to HOOD's own thesis (distinct from, and never substituting for, its role as this account's
   brokerage).
7. **RTX** (`band`, 0.75% target). *Materiality*: small, capped position; aerospace/defense
   conglomerate economics (commercial aerospace plus defense-contracting revenue mix), a distinct
   government-counterparty and defense-budget-cycle risk profile not present in any currently covered
   holding. *Deferral reason*: no coherent wave exists — RTX shares no genuine economic mechanism with
   any other currently uncovered band/spec name; a standalone aerospace/defense wave would need at
   least one comparably-themed addition to reach `OPS-0008` §1's default size or its own explicit
   smaller-wave justification. *Reopening trigger*: (a) tier promotion; (b) materially increased
   position size; (c) a future coherent aerospace/defense research wave; (d) a material defense-budget,
   export-control, or program-specific (e.g. engine/platform) disclosure event.
8. **DELL** (`band`, 0.75% target). *Materiality*: small, capped position; enterprise hardware/
   infrastructure (servers, storage, PCs) with plausible but unexamined AI-server/data-center-hardware
   adjacency to already-covered hyperscaler and semis-cluster names. *Deferral reason*: no coherent
   wave currently exists — DELL's specific hardware-integrator economics differ enough from both the
   hyperscaler cloud-services mechanism (`PI-0027`) and the semis-equipment/compute mechanisms
   (`PI-0023`/`PI-0025`) that folding it into either would misstate the mechanism; a standalone
   enterprise-hardware wave has no other current candidate. *Reopening trigger*: (a) tier promotion;
   (b) materially increased position size; (c) a future coherent enterprise-hardware/server-integrator
   research wave; (d) a material AI-server backlog or margin-mix disclosure event.
9. **PLTR** (`spec`, 1.0% fixed target, no RSI gate on trims). *Materiality*: fixed spec-tier
   conviction sizing; data-analytics/software platform with government and commercial segments,
   distinct enough from `PI-0030`'s enterprise-software batch (workflow/CRM/database/cybersecurity
   mechanisms) to not have been folded into it. *Deferral reason*: no coherent wave currently exists
   for PLTR specifically — its government-contracting-plus-commercial-AI-platform mix does not cleanly
   match any already-covered enterprise-software mechanism, and spec-tier names have not yet been
   addressed as a group by any batch. *Reopening trigger*: (a) tier promotion out of spec; (b) a
   materially increased position size beyond the fixed 1.0% spec target (which would itself require a
   tier or target-structure change); (c) a future coherent spec-tier or government/commercial-AI-
   platform research wave; (d) a material government-contract-concentration disclosure event.
10. **SPCX** (`spec`, 1.0% fixed target, no RSI gate on trims). *Materiality*: fixed spec-tier
    conviction sizing; already trimmed once in this account's own history (`CLAUDE.md` Standing Queue:
    "SPCX trim to 1.0% spec target — done 2026-07-13"). *Deferral reason*: no coherent wave currently
    exists — SPCX's space-launch/satellite-services economics share no genuine mechanism with any other
    currently uncovered holding, and privately-held-company-adjacent disclosure limitations (SPCX being
    substantially privately held with limited public-filing depth relative to the roster's other
    holdings) make primary-source research for it structurally different from a typical public-company
    unit — a fact a future research wave authorization should account for explicitly rather than assume
    away. *Reopening trigger*: (a) tier promotion; (b) materially increased position size; (c) a future
    coherent spec-tier or space/launch-services research wave that explicitly addresses SPCX's
    disclosure-depth limitations; (d) a material public-disclosure event (e.g. an IPO or a material
    financing round with new public filings).
11. **RKLB** (`spec`, 1.0% fixed target, no RSI gate on trims). *Materiality*: fixed spec-tier
    conviction sizing; already the subject of this repository's own trim-backtest analysis
    (`CLAUDE.md` Decisions Log, `trim_backtest.md`: RKLB ballooned to 12.6% of the band/spec sleeve
    under the never-trim control arm, cited as the specific evidence for keeping the mechanical trim
    rule). *Deferral reason*: no coherent wave currently exists — RKLB's space-launch/satellite
    economics share the same absence of a comparably-themed sibling as SPCX, though RKLB, unlike SPCX,
    is a standard publicly-traded company with ordinary SEC disclosure depth. *Reopening trigger*: (a)
    tier promotion; (b) materially increased position size; (c) a future coherent spec-tier or
    space/launch-services research wave (which could reasonably pair RKLB and SPCX together once their
    differing disclosure-depth profiles are accounted for); (d) a material program, contract, or
    manifest-concentration disclosure event.
12. **TSLA** (`spec`, 1.0% fixed target, no RSI gate on trims). *Materiality*: fixed spec-tier
    conviction sizing; already named once in this repository's own history — the `power_infra`
    correlation scan found TSLA correlated with GEV/ETN/VRT/PWR but explicitly excluded it from that
    cap ("more likely riding bull-market beta than the specific power-buildout mechanism," same
    treatment as CAT). *Deferral reason*: no coherent wave currently exists — TSLA's
    EV/energy-storage/autonomy economics share no genuine mechanism with any other currently uncovered
    spec-tier name (PLTR/SPCX/RKLB/INTC — INTC already covered per `PI-0025`), and forcing a pairing
    would misstate the mechanism the same way it would for CAT. *Reopening trigger*: (a) tier
    promotion; (b) materially increased position size; (c) a future correlation re-scan or a future
    coherent EV/energy-storage/autonomous-vehicle research wave; (d) a material
    autonomy/robotaxi/energy-storage-segment disclosure event.
13. **BABA** (`band`, 0.75% target). *Materiality*: small, capped position; **treated with particular
    care per this decision's own governing instructions, distinct in kind from every other name in
    this section.** BABA is a US-listed foreign private issuer (Chinese e-commerce/cloud conglomerate)
    subject to a materially different evidence and disclosure regime than every other name in this
    decision or in this repository's entire existing Intelligence coverage: PCAOB audit-inspection
    access history and its own regulatory back-and-forth; VIE (variable interest entity) corporate
    structure rather than direct equity ownership of underlying Chinese operating businesses; PRC
    regulatory, delisting-risk (Holding Foreign Companies Accountable Act-adjacent), and cross-border
    data/antitrust exposure; and geopolitical risk (US-China trade, technology, and capital-markets
    policy) materially distinct from any domestic holding's regulatory exposure. `PI-0027`'s deferred
    EQIX is the closest existing precedent for "a structurally different disclosure regime deferred
    specifically because it is untested anywhere in this repository's Intelligence coverage" — BABA's
    case is more consequential than EQIX's REIT-structure difference, because it compounds a foreign-
    issuer disclosure gap with jurisdiction-level geopolitical and audit-access risk that no research
    wave in this repository's history has ever addressed. *Deferral reason*: no existing batch or
    research-wave design in this repository has ever established an evidence standard for a VIE-
    structured, PCAOB-audit-history-affected, foreign-private-issuer holding — applying the ordinary
    SEC 10-K/10-Q/8-K-first evidence protocol used throughout `PI-0023`-`PI-0032` without first
    addressing BABA's distinct filing regime (20-F annual reports, not 10-K; VIE structural disclosure
    requirements; audit-inspection-status disclosure) risks producing a record that misrepresents its
    own evidentiary confidence. *Reopening trigger*: (a) tier promotion; (b) materially increased
    position size; (c) **a company-specific disclosure event — specifically, a material change to
    BABA's PCAOB audit-inspection status, VIE structural disclosure, or PRC/US delisting-risk
    posture** — any of which would itself be a reason to research BABA promptly rather than wait for a
    wave; (d) a future, separately authorized research-wave design that explicitly states its
    foreign-issuer/VIE/audit-access evidence standard before naming BABA or any other foreign private
    issuer as a candidate — this decision does not design that standard and does not authorize research
    under the ordinary domestic-issuer evidence protocol used elsewhere in this repository.
14. **UNH** (`band`, 0.75% target). *Materiality*: small, capped position; **formalizes the rationale
    already recorded in `PI-0029`'s biopharmaceuticals batch and CLAUDE.md's own Decisions Log, adding
    the explicit reopening trigger neither previously stated.** UNH is a managed-care/health-insurance
    company — payer economics (premiums, medical-loss ratios, risk-adjustment, PBM/Optum
    services-segment economics) — a structurally different economic mechanism from every currently
    covered healthcare-adjacent holding: distinct from `life_sciences_tools_medtech`'s device/tools/
    diagnostics economics (ISRG, TMO) and distinct from `PI-0029`'s biopharmaceutical
    franchise/pipeline economics (LLY, ABBV, MRK, JNJ, GILD). `PI-0029` itself considered and
    explicitly excluded UNH from that batch on exactly this basis ("UNH was considered and explicitly
    excluded from this batch, not covered — a structurally different economic mechanism (payer
    economics, not branded-franchise/pipeline economics)"). *Deferral reason*: no coherent
    payer/managed-care wave currently exists — UNH is this roster's only managed-care holding, so no
    genuine economic-mechanism sibling exists for a batch under `OPS-0008` §1's default sizing, and a
    single-company UNH wave under §1's smaller-wave exception has not yet been separately requested or
    authorized (unlike CVX's, which `PI-0031` explicitly authorized). *Reopening trigger*: (a) tier
    promotion; (b) materially increased position size; (c) a future coherent payer/managed-care/health-
    insurance research wave — plausible only if the roster ever adds a second managed-care holding, or
    via `OPS-0008` §1's smaller-wave exception exactly as `PI-0031` used it for CVX, requiring its own
    separate, later, explicit authorization naming UNH; (d) a material regulatory event (e.g. Medicare
    Advantage rate-setting or risk-adjustment-methodology change), litigation, or reimbursement-policy
    disclosure event specific to UNH's payer economics.

### B. Three existing deferrals — restated, not altered

**This section states, without editing, reopening, expanding, or in any way altering, the deferral
decisions already accepted for DHR, SYK, and EQIX.** No new fact, trigger, or rationale is added here
beyond what `PI-0014` and `PI-0027` already established; this section exists solely so this decision's
own accounting of "every remaining uncovered company" is complete without requiring a reader to
cross-reference two other files to see the full seventeen-name picture.

15. **DHR** — deferred per `PI-0014`. `PI-0014` authorized a bounded, conversation-based,
    read-only evidence-gathering step (not yet exercised as of this filing) into whether DHR's FY2025
    disclosed mixed segment picture (Biotechnology +7%, Life Sciences −4%, Diagnostics −1.5%) has
    changed in subsequent reporting periods — explicitly excluding any revisiting of the existing
    TMO-redundancy finding recorded in `life_sciences_tools_medtech.md`. This decision changes nothing
    about DHR's status, scope, or trigger — `PI-0014`'s own terms continue to govern exactly as filed.
16. **SYK** — deferred per `PI-0014`. `PI-0014` authorized the same bounded evidence-gathering step for
    SYK, addressing whether its disclosed "Ortho Tech" segment reorganization (effective Q1 2026, with
    2023–2025 financials recast) has now been observable across enough reporting periods under the new
    structure to support a durable record. This decision changes nothing about SYK's status, scope, or
    trigger — `PI-0014`'s own terms continue to govern exactly as filed.
17. **EQIX** — deferred per `PI-0027`. `PI-0027` deferred EQIX from Batch 5 specifically because its
    REIT legal and disclosure structure (a different SEC filing shape — funds from operations,
    tenant/lease concentration, dividend-distribution mechanics — than any operating company this
    repository has yet covered) is untested anywhere in this repository's Intelligence coverage, while
    preserving EQIX as a named, explicit candidate for its own future batch. This decision changes
    nothing about EQIX's status, scope, or trigger — `PI-0027`'s own terms continue to govern exactly
    as filed.

## Milestone 3 completion boundary

**Milestone 3 remains in progress after this governance filing.** This decision records dispositions;
it performs no research, and no research implementation or approval for any of the fourteen newly
dispositioned names is authorized by this filing under any circumstance — a "deferred, with a
reopening trigger" disposition is explicitly not a research authorization; it is the opposite, a
recorded reason research does not proceed now.

- **A later, separate completion-determination decision must evaluate all seven of `PI-0031` §K's
  accepted completion criteria** before Milestone 3 may be marked `complete`. This decision materially
  advances criterion 4 ("every remaining uncovered company is covered, explicitly deferred by accepted
  authority with rationale, or assigned to an approved alternative research architecture") by supplying
  the missing individual rationale for fourteen previously-unaddressed names, but does not itself
  perform that seven-criterion evaluation.
- **Sandisk cannot delay Milestone 3 completion because it is not a governed holding** — restated from
  `PI-0032`, applicable here because this decision's own completeness accounting is scoped to governed
  holdings only; Sandisk (addressed in `PI-0032`, not this decision) was never within `PI-0031` §K's
  criterion 4 scope.
- **Completion does not authorize Milestone 4.** Milestone 4 remains unauthorized until a later,
  separate decision determines `PI-0031` §K's criteria have been met and separately authorizes
  Milestone 4's own scope.
- **No portfolio mutation is authorized** by this decision. Every `holdings.yaml`/`targets.yaml` value,
  every tier, cluster, cap, and margin parameter remains exactly as currently governed throughout and
  after this filing.

## Rationale

**Why company-specific reasoning for every one of the fourteen, not one generic trigger.** A single
generic "revisit if the roster changes" trigger applied uniformly across fourteen structurally
different companies would state nothing a future reader could act on — it would not distinguish CAT's
already-scanned-and-excluded correlation history from GNRC's never-scanned adjacency, or BABA's
foreign-issuer disclosure-regime gap from UNH's payer-economics mechanism gap. `PI-0031` §K's own
completion criterion requires "explicitly deferred by accepted authority with rationale" — a rationale
that is identical for fourteen unrelated companies is not a rationale in the sense that criterion
requires; it is a placeholder. Individual reasoning, even where several entries share structural
features (four spec-tier names; a shared "no coherent wave exists" observation across most of the
fourteen), still ties each disposition to that specific company's own facts.

**Why BABA and UNH receive materially longer treatment.** The principal's own instructions single out
both as requiring particular care, and the underlying facts justify that: BABA is the roster's only
foreign private issuer with VIE/PCAOB/geopolitical exposure this repository has never built an evidence
standard for, and UNH is the roster's only managed-care/payer-economics holding, already the subject of
an explicit, on-the-record exclusion decision (`PI-0029`) that stopped short of stating a reopening
trigger. Formalizing UNH's rationale, rather than re-deriving it from scratch, follows this
repository's own reference-not-restate discipline (`OPS-0008` §7, `OPS-0009` §2) — citing and extending
the existing finding rather than duplicating it.

**Why the three existing deferrals are restated but not altered.** `PI-0031` §K's own completion
criterion 4 requires an accounting of every remaining uncovered company — DHR, SYK, and EQIX are
uncovered and already carry accepted deferral rationale, so a complete accounting must reference them,
but `governance/decisions/README.md`'s own convention forbids editing a decision's substance after
`status: Accepted`. Restating their existing terms verbatim-in-substance, without adding or changing
anything, closes the accounting gap without touching `PI-0014` or `PI-0027`'s own accepted text.

**Why `PI-####`, not a new `OPS-####`.** Same reasoning as every prior Milestone 3 filing and as
`PI-0032`: this is Company Intelligence coverage-disposition content (`category: portfolio_intelligence`),
filed in the `PI-####` series.

**Why filed as a companion to `PI-0032` rather than folded into one combined document.** Following the
same principal-directed separation `OPS-0008`/`PI-0027` already established — a research authorization
and a disposition/deferral record are different kinds of decisions with different future amendment
paths (a later decision may need to reopen one of the fourteen dispositions here without touching
`PI-0032`'s research authorization, or vice versa) — cleaner with `governance/decisions/README.md`'s
one-file-per-decision convention followed literally even when filed and reviewed together in one PR.

## Alternatives Considered

- **Use one generic reopening trigger for all fourteen names.** Rejected per the principal's explicit
  instruction and on the merits — see Rationale above; a uniform trigger would not satisfy `PI-0031`
  §K criterion 4's "with rationale" requirement in any meaningful sense.
- **Treat UNH as a fifteenth name, separate from "the 14."** Rejected per the principal's explicit
  instruction — UNH is one of the fourteen newly dispositioned names; the arithmetic in §A above states
  this precisely and is controlling.
- **Fold BABA's and UNH's treatment into the same brief format as the other twelve.** Rejected — both
  carry distinct, consequential facts (BABA's foreign-issuer/VIE/audit-access regime; UNH's
  already-recorded-but-incomplete exclusion rationale) that a brief entry would not adequately capture,
  and the principal's own instructions require particular care for both.
- **Edit `PI-0014` or `PI-0027` directly to add a cross-reference to this decision.** Rejected —
  `governance/decisions/README.md` forbids editing a decision's substance after `status: Accepted`;
  restating their terms here, in this new decision, is the correct instrument.
- **Combine this decision with `PI-0032` into one filing.** Rejected per the principal's explicit
  instruction and this repository's own `OPS-0008`/`PI-0027` precedent for filing two decisions
  together as separate files in one PR.
- **Omit the Milestone 3 completion boundary section, relying on `PI-0032`'s statement of it alone.**
  Rejected — this decision materially affects `PI-0031` §K criterion 4's evaluation and should state its
  own boundary explicitly rather than relying on a companion file a future reader might not open
  alongside this one.

## Consequences

**Authorized, effective on this decision's merge:** nothing beyond the recorded dispositions and
restatements themselves. This decision authorizes no research, no Company Intelligence record, no
comparison artifact, no freshness row, and no policy, tier, target, cluster, cap, holdings, margin, or
allocator change for CAT, GNRC, NFLX, SHOP, UBER, HOOD, RTX, DELL, PLTR, SPCX, RKLB, TSLA, BABA, UNH,
DHR, SYK, or EQIX.

**Unchanged by this decision:** every existing tier, target, role, cluster, cap, and holding in
`targets.yaml`/`holdings.yaml`; every existing Company/Theme Intelligence record; `allocate.py`,
`margin_state.py`, and every existing test; the 1.8x leverage cap and 30% buffer floor;
`MARGIN-0005`'s research charter and trial ceiling; `PI-0014`'s and `PI-0027`'s own accepted text and
scope, in full, unedited. Milestones 4-9 of WS-0005 remain entirely unauthorized.

**No research has been conducted, and no research finding, deferral reversal, ranking, score, or
automatic implementation is authorized or implied by this decision alone.** Any future research on any
of the seventeen names addressed here requires its own separate, later, explicit governance decision,
naming that company specifically and stating why its reopening trigger has occurred — exactly the
discipline `PI-0016`, `PI-0023`-`PI-0032`, `PI-0014`, and `PI-0027` already established.
