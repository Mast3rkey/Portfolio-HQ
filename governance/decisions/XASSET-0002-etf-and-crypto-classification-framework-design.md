---
decision_id: XASSET-0002
date: 2026-08-07
status: Proposed
category: cross_asset_allocation_architecture
related_decisions: [GOV-0001, GOV-0002, OPS-0001, OPS-0006, OPS-0007, OPS-0008, OPS-0009, PI-0016, PI-0031, PI-0035, PI-0037, TIER-0001, TIER-0002, TIER-0003, TIER-0004, TIER-0005, TIER-0006, TIER-0007, TIER-0009, REL-0001, REL-0004, REL-0006, REL-0007, CHART-0001, CHART-0002, LADDER-0001, PHQ-2026-01, PHQ-2026-02, CONTENDER-0001, CONTENDER-0002, XASSET-0001]
supporting_artifact: governance/audits/WS0014_ETF_CRYPTO_CLASSIFICATION_FRAMEWORK_DESIGN_20260807.md
file: governance/decisions/XASSET-0002-etf-and-crypto-classification-framework-design.md
---

## Context

### Authority for this unit

`XASSET-0001` §J names "structural ETF + crypto framework design (step 3)" as the next dependency-ordered
item in `WS-0014`'s roadmap, explicitly permitted to batch as one filing ("both are schema-design
exercises, not content research, and may reasonably batch as one architecture unit even though the two
frameworks differ in content") while requiring, with equal explicitness, that framework **design** never
combine with blind-classification **content** for either asset type, and that ETF content and crypto
content never share a filing (§J, "Separate lifecycle units are required, never batched"). `XASSET-0001`
§C independently states that neither asset type may be forced into `TIER-0002`'s company-shaped equity
schema and that ETF/crypto framework design is explicitly **not authorized by `XASSET-0001` itself** —
"not authorized or designed by this filing... a future implementation must design new, asset-appropriate
schemas." This filing is that future, separately authorized design unit. It designs; it does not classify.

### Preflight performed this session, independently verified, not assumed

- **Repository identity**: `Mast3rkey/Portfolio-HQ`, working directory `/home/user/Portfolio-HQ`, branch
  `claude/etf-crypto-framework-design-ihdf67`, working tree clean at session start.
- **`origin/main` fetched and reconciled**: local `HEAD` and `origin/main` both confirmed identical at
  `bb909532b9329e22d509180b2f308103f3594fa0` — `TIER-0013`'s own merge commit (PR #267).
- **Zero open pull requests** confirmed live via the GitHub API — no competing mutation lane.
- **`WS-0005`'s final state independently re-verified**: `status: complete`, `priority: secondary`, all
  nine `OPS-0006` §4 milestone gates `status: complete`, per `TIER-0013`. Zero `priority: primary`
  workstreams currently exist in the repository — confirmed by direct grep of every `priority:` field in
  `operations/WORKSTREAMS.yaml`.
- **`WS-0014`'s full live entry independently re-read** (`operations/WORKSTREAMS.yaml`, `- id: WS-0014`):
  `status: proposed`, `priority: secondary`, `dependencies: [WS-0005]`, `authorized_scope: "None —
  architecture and sequencing planning only... Items 2-14 of the fourteen-item scope list remain wholly
  unauthorized"`, exactly two milestone gates recorded (`contender0002-normalization-and-readiness-
  screening-authorization`, `status: complete`, `pr: 257`; `contender0002-normalization-and-readiness-
  screening-implementation`, `status: in_progress`, `pr: 258`).
- **`XASSET-0001` and `CONTENDER-0001`/`CONTENDER-0002` read in full.** `TIER-0002`/`TIER-0003`/`TIER-0004`/
  `TIER-0005` read as the equity framework-design precedent and non-reuse boundary — `XASSET-0001` §C
  explicitly prohibits forcing ETF or crypto evidence into that schema; this filing does not reuse it,
  and the supporting artifact (§1–§2) documents exactly what is carried forward as general classification
  hygiene versus what is deliberately not reused.
- **`issuer_lookthrough.yaml` and `targets.yaml` independently re-read**: `targets.yaml` carries 36
  `destination:` rows — 27 equities, `asset_class: fund` for SPY/VEA/VWO/GLD (4 rows, GLD included),
  `asset_class: crypto` for BTC/ETH/SOL, plus RESERVE (`reserve`) and CASH (`cash`).
  `issuer_lookthrough.yaml`'s `funds:` list, independently greped across every issuer row, names only
  `SPY`, `VEA`, and `VWO` — GLD never appears as a constituent-bearing fund anywhere in that file. Both
  facts are load-bearing for §5's GLD determination below.
- **Decision catalog** independently rebuilt: **90 decisions, `issues == ()`** at the starting head, 90
  `.md` files in `governance/decisions/` (excluding `README.md`) reconciling 1:1. `XASSET-0002` confirmed
  unused: zero matches in `governance/decisions.yaml`, zero matches via full-repository grep;
  `governance/decisions/README.md`'s own rule ("a new prefix is chosen only when a genuinely new decision
  domain needs one") is satisfied by continuing the existing `XASSET-####` series rather than minting a
  new one — this filing is the direct continuation of `XASSET-0001`'s own roadmap step 3, not a
  genuinely new decision domain (mirroring `CONTENDER-0001`→`CONTENDER-0002`'s identical continuation
  pattern for that series' own item 1).

### Stale `WS-0014` item-1 register state — independently verified, synchronized here (Lane M)

The preflight found `operations/WORKSTREAMS.yaml`'s `contender0002-normalization-and-readiness-screening-
implementation` gate reading `status: in_progress`, `pr: 258` — but PR #258 is, in fact, fully merged.
Independently re-verified via the GitHub API, not assumed: PR #258 (`merged: true`, `merged_at:
2026-08-06T14:22:49Z`, merge commit `1d5d93f94bbc39a0b9d99178a7b477e6f0f27928`, confirmed an ancestor of
current `HEAD`), five correction rounds, a final independent exact-head delta review
(`pullrequestreview-4875587500`, **APPROVED FOR PRINCIPAL EXACT-HEAD ACCEPTANCE**, zero
BLOCKING/MAJOR/MINOR), principal acceptance (`issuecomment-5205949519`), and post-merge verification
(`issuecomment-5206063709`, confirming the 8-file scope, all validators clean, full suite 2875/0, decision
catalog 84/`issues == ()`, zero protected-path diff) — all independently re-fetched and re-read this
session, not inferred from any prior summary. `intelligence/contenders/registry.yaml` is confirmed present
in the current working tree.

**Governing basis for including this synchronization in this filing (rather than deferring it to its own
follow-up unit)**: this is the exact `OPS-0009` Lane M pattern this repository has applied on every
directly comparable occasion — `TIER-0002` folded in `TIER-0001`'s identical stale-gate correction
("`TIER-0001`... reads `status: in_progress`, `pr: null`... This filing performs that synchronization...
as an `OPS-0009` Lane M unit folded into this governance filing, per `OPS-0008` §4(a)'s read-only-by-
default convention"); the `REL-0002`→`REL-0006` chain and `PI-0039`/`REL-0007`/`TIER-0007`/`TIER-0009`/
`TIER-0011` each did the same for their own immediately-preceding merged PR. The pattern is: **leave the
original gate's own historical text unedited** (it was accurate as filed) and **add one new, additive,
separately-named gate** recording the confirmed post-merge state — never a direct edit of the stale
`status` field in place. §I below performs exactly that addition. This is option **A** from the task
brief: the tiny factual synchronization is safely included in this filing under established, repeatedly-
applied precedent, without expanding this filing's own substantive scope beyond design.

## Decision

This filing does four things, in one bounded PR:

1. **Reconfirms (Lane M) that `CONTENDER-0002`'s own implementation PR (#258) is fully merged, reviewed,
   corrected, principal-accepted, and post-merge verified**, and synchronizes `operations/WORKSTREAMS.yaml`
   accordingly via one additive gate entry — no edit to the original gate's own historical text (§I).
2. **Designs, as text only — not an authorization, not an adoption, not applied to any fund or coin — an
   ETF-appropriate blind-classification framework**: six substantive axes (`structural_role`,
   `constituent_exposure`, `overlap_and_concentration`, `cost_and_tracking_quality`, `liquidity`,
   `structure_and_methodology`) plus `evidence_quality`, none of them equity-shaped, each with a closed
   vocabulary, evidence-input list, abstention discipline, prohibited-inference statement, and downstream
   use. Full field-by-field detail in the supporting artifact §3.
3. **Designs, as text only, a crypto-appropriate blind-classification framework**: six substantive axes
   (`network_fundamentals`, `economic_model`, `liquidity_and_market_structure`,
   `custody_and_counterparty_risk`, `correlation_and_volatility`, `regulatory_and_structural_uncertainty`)
   plus `evidence_quality`, explicitly rejecting every company-shaped equity field (no `economic_role`/
   `capital_priority` in `TIER-0002`'s sense, no financial-statement-derived fields, no cluster/issuer-
   look-through-shaped concentration field). Full field-by-field detail in the supporting artifact §4.
4. **Resolves the GLD structural-versus-functional placement question as Option C** — GLD receives both
   structural fund-mechanics evaluation under the ETF framework (its `constituent_exposure` and
   `overlap_and_concentration` axes are expected to resolve `not_applicable`, a genuine structural fact,
   not a schema failure) and a fully separate, future, functional defensive-asset-role determination
   under `XASSET-0001` §D — neither this design nor any future ETF classification built from it may
   itself assign GLD's portfolio role. Full reasoning, citing `targets.yaml`'s own `asset_class: fund`
   tag and `issuer_lookthrough.yaml`'s own confirmed non-inclusion of GLD as a constituent-bearing fund,
   in the supporting artifact §5.

Both frameworks share one common envelope (`instrument_id`, `asset_type`, `schema_version`, `provenance`,
`evidence_quality_status`, `uncertainty_summary`, `structural_risk_flags`, `record_status`,
`valuation_and_economic_assessment_readiness`, `cross_asset_handoff`, `abstention_index` — supporting
artifact §6), with **no numeric score, rank, or target field anywhere** except real, disclosed, inherited
financial facts (an ETF's own expense ratio), matching how every prior Milestone 6/7/8 equity record
already carries inherited percentages without those being scores. `valuation_and_economic_assessment_
readiness` forces exactly one value, `valuation_required`, today — the direct ETF/crypto analogue of
`TIER-0009` §G.4/§G.5's forced equity `valuation_required` state — preserving the boundary: framework/
classification → later asset-specific valuation/economic assessment → later cross-asset synthesis → later
sizing (supporting artifact §6.3, §10).

This filing also specifies, for a later, separate implementing PR: a validator specification (thirteen
requirements — supporting artifact §8) and a focused test inventory (supporting artifact §9), both
drawing explicit lessons from this repository's own prior validator-review history (closed-schema
extra-key gaps, independent-mechanism verification, self-declared-flag-without-independent-scan gaps —
§9.1) so a future implementation does not rediscover them the expensive way.

This decision explicitly does **not**: classify any ETF or cryptocurrency (SPY, VEA, VWO, GLD, BTC, ETH,
and SOL are named nowhere in this filing except as structural examples in the supporting artifact's own
reasoning, never assigned a value on any axis); create `intelligence/etf_classification/`,
`intelligence/crypto_classification/`, or any file inside either; modify `targets.yaml`, `holdings.yaml`,
`gates.yaml`, `issuer_lookthrough.yaml`, `allocate.py`, `levels.py`, or `margin_state.py`; compute a
mechanical score of any kind; perform any valuation, cross-asset synthesis, or sizing; define cash/
reserve/GLD/debt functional doctrine (`XASSET-0001` §D remains wholly undesigned by this filing beyond
the GLD structural/functional boundary determination in point 4 above); or authorize any of `WS-0014`'s
remaining items (4–14, per `XASSET-0001` §I/§J) — ETF classification (item 5) and crypto classification
(item 7) each require their own separate, future, explicit principal authorization and independent-review
lifecycle, and this filing does not combine, foreshadow, or pre-stage either.

## Rationale

**Why one filing for both frameworks.** `XASSET-0001` §J states plainly that structural design for both
asset types "may reasonably batch as one architecture unit" — the two frameworks are schema-design
exercises sharing a method (derive axes from decision usefulness, keep judgment separate from mechanical
computation, per-axis abstention rather than a bolted-on uncertainty axis), even though their content
differs entirely. Filing them separately would duplicate the shared-envelope design (§6) and the
validator/test specification (§8/§9) across two documents for no review benefit — matching the same
economy-of-filing reasoning `CHART-0002`'s own multi-ticker batching decisions applied.

**Why neither framework reuses `TIER-0002`'s schema.** `XASSET-0001` §C is explicit and was independently
re-verified this session, not merely cited: an ETF has no issuer or competitive position to assign an
"economic role" to in the company sense, and a cryptocurrency has no capital-allocation decision-maker
whose "priority" can be compared to a peer company's. Forcing either into the company-shaped schema was
independently rejected, not merely declined by omission — the supporting artifact §4.2 lists each
equity-shaped concept explicitly excluded and why, so a future implementation cannot silently reintroduce
one by analogy.

**Why `overlap_and_concentration`/`correlation_and_volatility` are mechanical, not narrative.** This
mirrors `TIER-0002`'s own separation of `risk_concentration` (computed) from `economic_role`/
`capital_priority` (narrative judgment) — a general classification-hygiene principle, not equity-specific
content, and one this design deliberately keeps rather than discards, because it is what makes the
judgment-before-computation sequencing (supporting artifact §6) meaningful for either asset type.

**Why GLD resolves to Option C without a principal stop.** Three independently sufficient lines of
existing authority converge on the same answer: `targets.yaml`'s own config schema already tags GLD
`asset_class: fund`; `issuer_lookthrough.yaml`'s own live data already excludes GLD from constituent
look-through, confirming its structural distinctness from SPY/VEA/VWO within the same fund category;
and `XASSET-0001` §D already assigns GLD's *role* question to a separate functional-doctrine track without
foreclosing structural fund-mechanics evaluation. No genuine ambiguity requiring principal judgment
remained once all three were read together — see supporting artifact §5 for the full citation-backed
argument.

**Why contamination controls are re-derived, not copied from `TIER-0004`.** `TIER-0004`'s redaction-and-
reseal apparatus exists because Company Intelligence records literally embed policy content
(`portfolio_role_ref`, `conviction`) inside the same file a blind drafter must read for factual evidence.
No ETF or crypto Intelligence record exists today, and neither framework's evidence sources (fund
prospectuses, protocol documentation, on-chain data) embed portfolio-policy text — so the file-level
redaction-and-reseal pipeline `TIER-0004` needed does not transfer. What does transfer, because it is a
bias-avoidance principle independent of file shape, is judgment-before-mechanical-rollup sequencing; what
is explicitly determined unnecessary at today's population scale (ETF ≤4, crypto = 3) is `TIER-0004`'s
multi-shard isolation apparatus, sized for 27 equities split across five shards. The supporting artifact
documents this determination directly rather than assuming either "reuse everything" or "reuse nothing."

## Alternatives Considered

**Design ETF and crypto frameworks as two separate filings rather than one.** Rejected — `XASSET-0001` §J
explicitly authorizes batching the design step, and the two frameworks share enough method (not content)
that one filing avoids duplicating the shared envelope, validator, and test specifications without
violating the rule against combining design with content or combining ETF and crypto *content*, which
this filing does not do.

**Reuse `TIER-0002`'s four-axis equity schema for both ETFs and crypto, adapting field meanings per asset
type.** Rejected outright — `XASSET-0001` §C prohibits this explicitly, and the supporting artifact §4.2
documents concretely why no company-shaped field (economic role, capital priority, financial-statement
metrics) has a coherent analogue for either asset type.

**Treat GLD exclusively under a future functional-doctrine unit, excluding it from the ETF framework
entirely.** Rejected — `targets.yaml`'s own schema already places GLD inside the `fund` asset class, and
GLD genuinely has real, disclosed fund-structural facts (expense ratio, replication method, tracking
versus spot gold) that are ETF-framework-shaped regardless of its eventual functional role; excluding it
from structural evaluation would leave a real fund's real structural risk (e.g., physical-custody
mechanics) permanently unrepresented in any framework.

**Treat GLD exclusively under the ETF framework, deciding its portfolio role as part of `structural_role`
now.** Rejected — `XASSET-0001` §D explicitly reserves GLD's role (ballast versus broad-market-beta) to a
separate, future, functional cash/reserve/GLD/debt doctrine unit; deciding it here would exceed this
filing's own design-only, architecture-and-sequencing-only authorization and would pre-empt a decision
`XASSET-0001` already assigned elsewhere.

**Design the ETF and crypto frameworks' full validator and test code as part of this filing, rather than
a specification for a future implementing PR.** Rejected, matching `TIER-0002`'s own explicit precedent
("designing a full framework... is substantive content work requiring its own dedicated authorization")
and `XASSET-0001` §J's own rule that framework design must never combine with content — a working
validator applied against real fund/coin data would itself constitute the beginning of classification
content, not design.

**Include a numeric or weighted scoring model on any axis of either framework.** Rejected outright,
matching `TIER-0002`'s identical prohibition and `docs/PORTFOLIO_INTELLIGENCE_SPEC.md` §12's standing rule
that conviction/priority "is not a formula, not a derived score." No field in either recommended design is
numeric or orderable by weight, except the two real, disclosed cost/tracking financial facts explicitly
carved out and bounded by the validator specification (supporting artifact §8 point 6).

## Consequences

**Changes as a direct result of this decision**: the existence of two retained, structural classification-
framework designs (ETF: six axes plus evidence quality; crypto: six axes plus evidence quality), one
shared cross-asset-handoff envelope design, one resolved GLD structural/functional placement
determination, one validator specification, and one test specification — all recorded in the supporting
artifact for a future, separately authorized implementing PR to draw on; one rejected major alternative
(equity-schema reuse) and five smaller rejected alternatives recorded for the same future reference;
confirmation, via one additive `operations/WORKSTREAMS.yaml` gate entry, that `CONTENDER-0002`'s own
implementation PR (#258) is fully merged, reviewed, corrected, accepted, and post-merge verified.

**Does not change**: any tier, target, cap, cluster, gate, or holding; any allocator or margin behavior;
any Company, Theme, relationship, or sealed classification record's content; `docs/INVESTMENT_
ONTOLOGY.md`'s or `docs/PORTFOLIO_INTELLIGENCE_SPEC.md`'s frozen text; `CONTENDER-0002`'s own historical
gate entry or decision-file text; `WS-0005`'s completed, `status: complete` state; `WS-0014`'s own
`status: proposed`/`priority: secondary` (this filing adds a design gate, it does not begin execution or
change the workstream's own status/priority); or any brokerage, trading, or order-related capability.
Completing this unit does not itself authorize ETF blind classification (`WS-0014` item 5), crypto blind
classification (item 7), cash/reserve/GLD/debt functional doctrine (item 8), overlap/concentration
modeling (item 9), cross-asset synthesis (item 10), sleeve- or instrument-level targets (items 11–12),
chart-informed deployment (item 13), or the final independent audit (item 14) — each requires its own
separate, explicit, future principal authorization, per `XASSET-0001` §J's own dependency-ordered roadmap
and `OPS-0006` §16.4's standing rule that the register never originates authority.
