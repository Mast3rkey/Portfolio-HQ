---
decision_id: LEVEL2-0001
date: 2026-08-13
status: Proposed
category: level2_selection_governance
related_decisions: [GOV-0001, GOV-0002, OPS-0001, OPS-0007, OPS-0009, OPS-0014, CONTENDER-0001, CONTENDER-0002, CONTENDER-0003, TIER-0004, TIER-0005, TIER-0008, TIER-0010, TIER-0012, TIER-0013, VALUATION-0003, VALUATION-0005, VALUATION-0007, XASSET-0001, XASSET-0002, XASSET-0003, XASSET-0004, XASSET-0008, XASSET-0009, XASSET-0010, XASSET-0011, XASSET-0014, XASSET-0015, XASSET-0016, XASSET-0017, XASSET-0018]
supporting_artifact: governance/evidence/LEVEL2-0001/RESEARCH_COHORT_FREEZE.yaml
file: governance/decisions/LEVEL2-0001-selection-only-research-cohort-freeze.md
---

## Context

### Live preflight and prior-phase state

This filing began from verified `origin/main` and local base
`013c7ab5e10c8007af0d47822c6888771b594f2e`, the merge commit of PR #311. The connected GitHub
repository reported zero open pull requests. PR #311 was independently re-opened read-only and
confirmed merged from exact head `0cd8e88f560ff1115caded91158695bfe537046f` into main as
`013c7ab5e10c8007af0d47822c6888771b594f2e`; exact-head CI run `31701117009` completed successfully.
The primary checkout contained unrelated untracked `AGENTS.md` and `.worktrees/` paths, so this filing
uses the clean dedicated worktree and branch `codex/level2-0001-selection-cohort` and leaves those
paths untouched. No competing mutation lane existed when this branch was created.

The merged schema-2.0 Level 1 records remain provisional and not adopted. Their values, blocked
states, assigned subtotal, and unsized residual are not inputs to this decision, are not copied into
the structured freeze, and create no Level 2 selection or sizing authority. This filing does not
alter those records or authorize the separately contemplated Level 1 robustness study.

### Identifier determination

`LEVEL2-0001` is the correct live identifier. No `LEVEL2-####` decision exists in the decision
catalog or repository, and this is the first decision whose domain is specifically Level 2
instrument-selection governance. It does not continue the `XASSET-####` Level 1 architecture and
numeric-sizing sequence, and it does not consume the separately contemplated `XASSET-0019`
robustness-protocol unit. Per `governance/decisions/README.md`, a new prefix is used here because
selection-only Level 2 governance is a genuinely distinct decision domain, not because a session
label alone requested it.

### Evidence reconstructed from repository truth

The exact 34-instrument research cohort is reproduced independently from the live sealed corpora:

- 27 equities form the only closed equity population with sealed blind classification, valuation
  archetype, valuation evidence, and valuation-result manifests;
- SPY, VEA, and VWO have sealed ETF classification and instrument economic-assessment records;
- GLD has sealed ETF classification, functional-doctrine, and economic-assessment records; and
- BTC, ETH, and SOL have sealed crypto classification and instrument economic-assessment records.

The live contender registry was also reconciled. After the 34 core identities and the VRT/WMT pilot
are separated, it contributes 25 named abstentions and 23 current-freeze exclusions. Its unresolved
approximately 41-name pre-PHQ-2026-02 legacy gap remains a separate abstained population. The
governed ETF/GLD economic records additionally name nine same-category peer references: IAU, SGOL,
GLDM and six broad-market fund labels. The three gold peers have normalized identities in their
source record; the six broad-market peers remain exact source labels with no invented ticker
normalization.

## Decision

### A. Sole structured authority

`governance/evidence/LEVEL2-0001/RESEARCH_COHORT_FREEZE.yaml` is the sole authority-bearing cohort
record created by this filing. Its schema is recursively closed and enforced by
`research_cohort_freeze_validator.py`. This narrative explains the record but does not enlarge,
override, reinterpret, or supplement its dispositions, populations, source pins, or boundary states.

The structured record carries only closed disposition, reason, caveat, sleeve, asset-type, boundary,
and refreeze vocabularies; exact identifiers; exact governed source labels for the six unnormalized
fund references; repository paths; booleans/nulls where structurally required; integer population
counts; and SHA-256 pins. It contains no unrestricted policy prose, percentage, instrument weight,
rank, score, Level 2 sizing field, current-holding authority, or current-configuration authority.

### B. Closed disposition vocabulary

Exactly four dispositions exist:

1. `RESEARCH_COHORT_INCLUDED`;
2. `CONDITIONAL`;
3. `ABSTAIN_INSUFFICIENT_EVIDENCE`; and
4. `EXCLUDED_FROM_CURRENT_RESEARCH_COHORT`.

These labels are selection-only research states. `RESEARCH_COHORT_INCLUDED` does not mean selected
for a portfolio, and `EXCLUDED_FROM_CURRENT_RESEARCH_COHORT` is expressly current-freeze scoped,
never a permanent exclusion.

### C. Exact included research cohort

The core cohort contains exactly 34 unique instruments in four sleeves:

- equity (27): AMZN, ASML, AVGO, CEG, COST, ETN, GEV, GNRC, GOOGL, ICE, ISRG, KLAC, LLY, META,
  MSFT, NVDA, PANW, PWR, RKLB, RTX, SNPS, SPGI, TMO, TSLA, TSM, V, WM;
- broad market (3): SPY, VEA, VWO;
- defensive (1): GLD; and
- crypto (3): BTC, ETH, SOL.

The validator enforces exact membership, ordering, sleeve classification, uniqueness, and count. It
also proves that QQQ, CASH, RESERVE, cash-reserve accounting, and debt-reduction accounting are absent
from the included instrument cohort.

### D. Equity boundary

The 27 equities enter only because they are the sole closed equity population with sufficiently
complete governed evidence and provenance for historical examination. Their current membership,
current holding state, current configuration, or incumbency is not evidence for future inclusion.

The freeze preserves rather than resolves partial valuation results, the universal discount-rate
gap, source-access and freshness limitations, SPGI's `no_policy_conclusion`, structural-measurement
gaps, the approximately 41-name legacy completeness gap, and the noncanonical contender population.
No included equity is declared a final member, and no absent equity is declared permanently excluded.

VRT and WMT remain conditional. Their sealed contender pilot establishes evidence-parity findings
only; it is not converted into a capital-priority, promotion, replacement, or final-membership
conclusion.

### E. Broad-market boundary

SPY, VEA, and VWO are included for research. SPY's domestic-beta duplication caveat, VEA's
developed-ex-US geographic distinction, and VWO's emerging-market geographic distinction remain
explicit. Individual vehicle selection is unresolved.

The six exact peer labels named in the governed economic-assessment evidence remain conditional
source references. Their ticker identities are deliberately null because the controlling records do
not normalize them. They are neither silently ignored nor silently promoted.

### F. GLD boundary

GLD is included as the sole currently governed defensive representation. Its defensive-role evidence,
mixed historical protection evidence, and elevated cost versus IAU/SGOL/GLDM are preserved. IAU,
SGOL, and GLDM remain conditional. This filing reaches no conclusion that GLD is the final vehicle or
that any Level 1 GLD percentage is appropriate.

### G. Crypto boundary

BTC, ETH, and SOL are included separately because their governed records describe distinct network
and economic roles. Cross-coin correlation remains unresolved; SOL's historical equity-drawdown
field remains an abstention; and no equal-weight, market-cap, conviction, or other internal weighting
method is adopted. Inclusion establishes neither final membership nor a weight for any coin.

### H. Abstained and excluded populations

The structured record enumerates 25 named abstentions from the live contender registry. Reason codes
distinguish freshness review, absence of governed parity with the closed cohort, and research not yet
authorized. The unidentified approximately 41-name legacy population is separately abstained; no
placeholder identities are invented.

The 23 current-freeze exclusions reproduce the live registry's governed deferment/exclusion,
benchmark-only, and non-investable-accounting-row findings. QQQ remains benchmark-only. CASH and
RESERVE remain non-investable structural rows. No exclusion is made permanent by this filing.

### I. Source and provenance pins

The structured record pins the exact source commit and twelve controlling manifest/source files by
SHA-256 of repository file bytes. The pins cover equity classification and valuation, the SPGI-bearing
recommendation package, ETF and crypto classification, GLD and instrument economic assessments,
functional doctrine, VRT/WMT contender evaluation, and the complete contender registry. The validator
recomputes every pin, verifies the governed manifest populations, and reconciles the registry's 84
normalized identities exactly across the included, VRT/WMT conditional, named-abstained, and excluded
populations.

### J. Refreeze triggers

The cohort must be revisited before use when any closed trigger in the structured record occurs:

- material population change;
- a normalized same-role alternative reaches equivalent evidence;
- material freshness or access correction;
- a candidate reaches governed evidence parity;
- any pinned source hash changes in a way affecting the disposition basis; or
- a future final Level 2 membership decision is undertaken.

No recurring scanner or automation is created or authorized.

### K. Mandatory authority boundary

Research-cohort inclusion permits historical and evidentiary examination only. It does not establish
final portfolio membership, Level 2 selection policy, an instrument target or weight, rank, capital
priority, or portfolio adoption. It does not change current targets or any portfolio configuration.
It does not authorize buying, selling, an allocation check, backtesting, stress testing, Level 2
sizing, margin activity, or any brokerage action. Backtesting requires its own separate authorization.

### L. Register and catalog synchronization

This filing adds a factual PR #311 post-merge-verification gate and this current
`level2-0001-selection-only-research-cohort-freeze` gate to WS-0014. Historical gates remain
byte-unchanged. Active-lane fields move to this branch and, after the draft PR exists, its actual PR
number. The decision catalog gains exactly this one new row. The two mechanically hardcoded catalog
count assertions move from 115 to 116; no dashboard behavior or governance test is weakened.

### M. Explicit non-authorization and protected paths

This filing does not edit or authorize edits to `targets.yaml`, `holdings.yaml`, `gates.yaml`,
`issuer_lookthrough.yaml`, `allocate.py`, `margin_state.py`, `levels.py`, any numeric-sizing record or
numeric-sizing validator/test, XASSET-0014 through XASSET-0018, any sealed Intelligence record, or
any pre-existing decision's substance. It does not create XASSET-0019, run a robustness study or
backtest, collect market data, stress test, rank equities, determine capital priority, change a
contender disposition outside this research-freeze overlay, make a trade, or declare the portfolio
ready.

## Rationale

A research cohort must be stable before historical evidence is compared, or later availability and
selection decisions can leak into the study population. Freezing the narrow evidence-ready population
now controls that risk without pretending the freeze answers final membership. A closed structured
record is necessary because a prose-only cohort list cannot mechanically prove exact identities,
sidecar separation, source-hash reconciliation, or the absence of sizing and ranking authority.

## Alternatives Considered

**Use `XASSET-0019`.** Rejected. This is the first Level 2 selection-governance unit, while the
separately contemplated XASSET-0019 unit concerns future Level 1 robustness methodology. Reusing the
XASSET sequence would blur the Level 1/Level 2 authority boundary.

**Treat the 34 instruments as final membership.** Rejected. The evidence permits a bounded historical
research population, not a final portfolio conclusion.

**Promote all evaluation-ready contenders or named peer funds.** Rejected. The noncanonical equities
lack the closed cohort's complete governed parity, and the peer funds lack equivalent normalized and
classified evidence. VRT/WMT's pilot is explicitly non-prioritizing.

**Omit candidates with incomplete evidence.** Rejected. Conditional, abstained, excluded, and legacy
gap states preserve unresolved population truth and prevent silent survivorship or incumbency bias.

**Create only narrative authority.** Rejected. XASSET-0018 established the repository-native lesson:
unrestricted prose cannot be exhaustively policed as structured policy authority. The freeze therefore
uses closed structured authority plus a dedicated validator and adversarial tests.

## Consequences

After this decision's own independent exact-head review, principal acceptance, merge, and post-merge
verification, future separately authorized evidence work may use the exact 34-instrument core while
preserving the conditional, abstained, and excluded sidecars. Any refreeze trigger stops use pending a
new governed determination. Final selection, Level 2 sizing, robustness research, backtesting, policy
adoption, and deployment all remain separate and unauthorized.
