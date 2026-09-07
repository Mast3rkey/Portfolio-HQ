---
decision_id: PI-0013
date: 2026-07-19
status: Accepted
category: portfolio_intelligence
related_decisions: [GOV-0001, PI-0001, PI-0002, PI-0003, PI-0004, PI-0005, PI-0006, PI-0007, PI-0009, PI-0010, PI-0011, PI-0012, ONTO-0001]
supporting_artifact: null
---

## Context

`governance/decisions/PI-0012-ai-compute-committee-review-pilot.md` authorized
a bounded, one-company committee-review pilot for TSM. PR #97 implemented
exactly `intelligence/companies/TSM.yaml` and `TSM.md` and merged to `main`.
PI-0012 itself requires that any second company "follow the same review-gate
discipline PI-0004 applied to close the COST pilot before PI-0005 authorized
XOM" — meaning a closure decision applying `decision_log.yaml` PI-0004's
five-part "pilot reviewed" test (implementation merged to main; validator
passing; full test suite passing; an architectural retrospective completed;
any governance ambiguities the retrospective identifies explicitly resolved
by governance) is required before any second-company selection or
authorization proceeds. No such closure decision exists yet. This decision
is that closure — nothing more.

A same-session, read-only architectural retrospective (conversational
analysis; `supporting_artifact: null` above, same disclosure convention
PI-0004/PI-0005/PI-0009 already used) independently re-verified the
validator (`valid: True, errors: []`) and the full test suite (`498 passed`)
against the actual repository state rather than trusting PR #97's own
narrative, and reviewed `TSM.yaml`, `TSM.md`, `ai_infrastructure.yaml`/`.md`,
`intelligence_validator.py`, and `intelligence_report.py` directly. It found
the frozen Company Intelligence schema held without modification, the
eleven-question method produced narrative without creating any unauthorized
YAML field, the conditional TSM→`ai_infrastructure` theme reference was
evaluated against that theme's own committed "Non-membership" standard and
documented as a transparent, evidenced "MEETS STANDARD" conclusion with no
reverse membership stored, and Intelligence Operations (staleness,
role-drift, coverage) scanned TSM cleanly with zero findings.

The retrospective also surfaced one demonstrated ambiguity: PR #97's own
body discloses that an initial draft's Portfolio-uniqueness and
Replacement-candidate sections were factually wrong about INTC's actual
held/spec/semis-cluster status until a manual "Gate 9" correction pass
caught it before merge. The eleven-question method, as authorized by
PI-0012, has no structural step requiring a reviewer to check draft claims
against `targets.yaml`/`holdings.yaml` before human approval — the catch in
this instance was manual, not built into the process. `constitution/
INVESTMENT_CONSTITUTION.md` Principle 6 ("verify before acting on external
review") supports direct verification of claims *about this repository*
generally, but the INTC error did not originate outside the repository —
it arose *inside the drafting workflow itself*, during authoring of a
record meant to already be repository-aware. Principle 6 alone therefore
does not fully resolve this; it justifies a more specific, narrower
future-adoption requirement, defined in Decision below, rather than being
cited as sufficient on its own. A second item — `TSM.md`'s own explicit,
honestly-disclosed statement that the degree of TSM/INTC economic overlap
and operational substitutability "remains unresolved" — is not a process
ambiguity requiring resolution; it is the shipped record correctly declining
to overclaim, and this decision leaves it exactly as recorded, not as a
defect requiring further TSM work.

## Decision

**Closes the PI-0012 TSM pilot review gate.** All five of `decision_log.yaml`
PI-0004's completion conditions are now satisfied: (1) implementation merged
to `main`, confirmed at HEAD `b10f9250af6cace13dea1c648e594ee866d15c0a`; (2)
validator passing, confirmed by direct re-execution of
`intelligence_validator.validate_company_file("intelligence/companies/TSM.yaml")`
in this session (`valid: True, errors: []`), not merely cited from PR #97's
own text; (3) full test suite passing, confirmed by direct re-execution of
`python3 -m pytest -q` in this session (`498 passed`); (4) the architectural
retrospective above is that retrospective, completed by this decision; (5)
the one ambiguity the retrospective identified is resolved as follows.

**Ambiguity resolution — future-adoption reconciliation gate, not a present
code change.** `TSM.yaml` and `TSM.md` need no change — their INTC-related
text was corrected before merge and is accurate as shipped. No schema,
validator, template, test, or code change is authorized by this decision.
Instead: **any future governance decision that explicitly adopts PI-0012's
eleven-question method for another company must also require, before final
human approval of that record's Portfolio Uniqueness gate, Replacement
Candidate gate, final YAML, and final Markdown, a repository-fact
reconciliation against (a) `targets.yaml`, (b) `holdings.yaml`, (c) the
current `intelligence/companies/` inventory, and (d) any existing
company-side `themes:` references relevant to the claims being made in that
record.** The reconciliation must verify the record's factual claims
concerning current holdings, tiers, targets, cluster membership, existing
Intelligence coverage, and current company-side theme references. It may
remain a manual, read-only review step — no new script, validator check, or
test is required or authorized — and may be documented in that future
pilot's review packet or implementation-PR narrative, the same disclosure
convention already used for every prior pilot's human-approval record. This
requirement binds only a future decision that explicitly adopts the
eleven-question method for a company beyond TSM; it imposes nothing on any
other Intelligence workflow and changes nothing about how TSM's own record
was produced or reviewed.

**The eleven-question method and TSM-specific evidence standard remain
TSM-only**, exactly as PI-0012 already stated. This decision does not extend
them to any other company. A future decision may adopt them by explicit
reference for a different company, subject to the reconciliation
requirement above; this decision itself grants no adoption authority.

**Tier, target weight, raw share count, ownership, and cluster membership
may be reported as repository context in any future review, but none of
them may be treated as evidence of company quality, conviction, theme
eligibility, or automatic entitlement to become the next pilot.** Beyond
that narrow guardrail, **PI-0013 does not define, rank, or freeze the
criteria for selecting the next company.** A future, separate
candidate-selection proposal must state and justify its own selection
criteria and its own evidentiary standard for any business-model or
economic-role characterization it performs — this decision neither supplies
those criteria nor prohibits that future proposal from characterizing a
company's business or economic role where it establishes its own sourcing
for doing so.

## Rationale

Same discipline `PI-0004` applied to close the COST pilot before `PI-0005`
authorized XOM, and the same discipline `PI-0012` itself requires be applied
here: a frozen specification or a completed implementation is not itself a
closed pilot-review gate; closure requires its own decision, applying the
reusable five-part test `PI-0004` established. This decision performs
exactly that test against `PI-0012`'s TSM pilot, re-verifies the two
independently-checkable conditions (validator, test suite) directly against
repository state rather than trusting a PR narrative, and resolves the one
ambiguity the retrospective actually surfaced — narrowly, as a gate on any
*future* adoption of the eleven-question method, not as a present change to
TSM or to any shared Intelligence code. Scoping the reconciliation
requirement to future adoption only (rather than, say, amending
`intelligence_validator.py` now) follows the same restraint `PI-0004`
applied to COST's own implementation-improvement findings — deferred as a
condition on future work, not folded into this closure. Declining to freeze
a standing candidate-selection doctrine here follows the same
smallest-reversible-step discipline this repository has applied to every
prior pilot: `PI-0004` closed COST's gate without pre-selecting XOM, and
this decision closes TSM's gate without pre-selecting, ranking, or
constraining whatever candidate a later proposal names. The narrow
quality/conviction/priority guardrail is retained because it restates
findings this session's own audit of the *prior* candidate-analysis attempt
already demonstrated concretely (tier weight and raw share count were
treated as if they carried materiality or selection significance without
governance authorization to do so) — recording that specific, demonstrated
guardrail is different from freezing a complete selection policy, which
this decision deliberately does not do.

## Alternatives Considered

- **Combine closure and second-company selection into one decision.**
  Rejected: this is exactly the blurring `PI-0004`'s own rationale describes
  avoiding ("preserve the established Governance -> Implementation ->
  Validation -> Retrospective -> Governance cadence rather than letting
  pilot closure and the next expansion phase blur together"), and `PI-0012`
  independently requires the `PI-0004`-before-`PI-0005` sequence be
  repeated here.
- **Treat PR #97's own validation narrative as sufficient without
  independent re-verification.** Rejected per `constitution/
  INVESTMENT_CONSTITUTION.md` Principle 6 — claims originating outside a
  live session with real file access are treated as unverified until
  confirmed directly; this decision only asserts conditions 2 and 3 as PASS
  because they were independently re-run, not because PR #97 said so.
- **Resolve the demonstrated ambiguity by citing Principle 6 alone, as
  already sufficient.** Rejected on reconsideration: Principle 6 addresses
  claims originating *outside* a session with repository access; the INTC
  error occurred *inside* the drafting workflow that already had repository
  access, so citing Principle 6 alone would overstate what it actually
  covers. A narrower, explicit reconciliation requirement, scoped to any
  future adoption of the eleven-question method, is the more accurate fix.
- **Add a structural repository-fact-check step to the eleven-question
  method, `intelligence_validator.py`, or a new script now.** Rejected:
  this would be a present schema/tooling/code change, out of scope for a
  closure decision, under the same restraint `PI-0004` applied to COST's
  own implementation-improvement findings (deferred as ordinary
  maintenance, not folded into the closure decision). The reconciliation
  requirement above binds a *future* decision's adoption, not any file in
  this repository today.
- **Freeze a complete, standing candidate-selection policy inside this
  closure decision.** Rejected: a closure decision's job is to close the
  gate PI-0012 opened, not to pre-write the next pilot's selection
  criteria. `PI-0004` itself closed COST's gate without pre-selecting or
  constraining XOM beyond what `PI-0005` later stated on its own terms;
  this decision follows the same pattern. Retaining only the narrow
  quality/conviction/priority guardrail — rather than either silence or a
  full policy — reflects a concretely demonstrated risk (this session's own
  finding that tier/weight/share-count were treated as selection-relevant
  without authorization) without overreaching into territory a future,
  separate proposal is better positioned to define.
- **Prohibit all future business-model or economic-role characterization of
  any company absent a committed artifact.** Rejected: that would freeze an
  evidentiary standard for research this decision has no basis to impose on
  a future proposal's own bounded scope. The evidentiary standard for any
  future characterization is left to that later, separate proposal to state
  and justify.
- **Leave the TSM/INTC overlap question formally "unresolved" in this
  decision's own terms, requiring further action.** Rejected: `TSM.md`
  already discloses this honestly as unresolved at the record level: that
  is the correct, intended state for a record that lacks evidence to
  support a stronger claim, not a defect this closure decision needs to fix
  or escalate.

## Consequences

`intelligence/companies/TSM.yaml`, `TSM.md`, `intelligence/themes/
ai_infrastructure.yaml`/`.md`, every other existing Company/Theme
Intelligence record, `intelligence_validator.py`, `intelligence_report.py`,
every test file, `docs/PORTFOLIO_INTELLIGENCE_SPEC.md`,
`docs/INVESTMENT_ONTOLOGY.md`, `constitution/INVESTMENT_CONSTITUTION.md`,
`allocate.py`, `margin_state.py`, `targets.yaml`, and `holdings.yaml` all
remain unchanged. `governance/decisions.yaml` gains one new row for this
entry. `CLAUDE.md`'s Decisions Log gains one short pointer entry. **This
decision does not select, name, rank, or imply a second Company Intelligence
pilot subject of any kind** — no candidate is chosen here. **No external
company research is authorized or was conducted under this decision.** The
repository-fact reconciliation requirement above binds only a future
decision that explicitly adopts the eleven-question method for a company
beyond TSM; it creates no obligation on any other Intelligence workflow and
requires no file change today. A future second-company authorization
remains its own separate, future governance decision, to be made only after
this closure and stating its own selection criteria — exactly the same
relationship `PI-0005` had to `PI-0004`.
