---
decision_id: GOV-0002
date: 2026-07-20
status: Accepted
category: constitutional_amendment
related_decisions: [GOV-0001]
supporting_artifact: null
---

## Context

GOV-0001 adopted a four-layer documentation architecture (Constitution →
governance decisions → Company/Theme Intelligence → Portfolio Policy) and
`governance/README.md` restated it as a flow ending in `targets.yaml` /
`allocate.py`. Neither document states a complete, general operational
precedence order across every source this repository actually treats as
authoritative. Three self-descriptions are currently partial or in tension:
the Constitution's own introduction resolves a Constitution/CLAUDE.md
conflict by deferring to "CLAUDE.md's Decisions Log" as "the more recent
and more specific record"; CLAUDE.md's own title calls itself the "single
source of truth"; and the Portfolio Policy Manual's document-status line
lists CLAUDE.md, `targets.yaml`, `decision_log.yaml`, `governance/decisions/`,
and `docs/PORTFOLIO_INTELLIGENCE_SPEC.md` as if they were five co-equal
authorities.

## Decision

Establishes the following complete operational precedence hierarchy,
highest authority first:

1. **The Investment Constitution** (`constitution/INVESTMENT_CONSTITUTION.md`),
   including only material it expressly incorporates by reference, and only
   within the exact scope it states that incorporation to cover:
   `docs/MARGIN_DOCTRINE.md` in full; `docs/PORTFOLIO_INTELLIGENCE_SPEC.md`
   §20 and §24 only. Incorporated material is part of level 1 — it is not
   ranked below accepted governance decisions.
2. **Accepted governance decisions** (`governance/decisions/`), operating
   within constitutional bounds. `decision_log.yaml` is included here only
   as authoritative evidence of the historical, pre-GOV-0001 `MARGIN-####`
   and `PI-####` decisions it actually records, within their original scope
   and subject to explicit governed supersession — it does not have its own
   separate, lowest-ranked level.
3. **Current accepted or frozen specifications and doctrine** not
   incorporated into the Constitution at level 1 — including the balance of
   any governing specification outside its constitutionally incorporated
   portion (e.g., the remainder of `docs/PORTFOLIO_INTELLIGENCE_SPEC.md`
   outside §20/§24).
4. **CLAUDE.md**, as operational synthesis, current-parameter record,
   workflow, agent entry point, and decision index.
5. **`targets.yaml`**, as authorized allocation-policy configuration.
6. **`holdings.yaml`**, as the repository's record of synchronized account
   and portfolio state.
7. **Executable code and tests**, as implementation and verification —
   never as policy originators.
8. **Generated or derivative outputs and non-authoritative syntheses**,
   including reports and `docs/PORTFOLIO_POLICY_MANUAL.md`.

Conflict resolution across this hierarchy is governed by the following
binding rules:

- A lower-authority source cannot amend, override, or silently supersede a
  higher-authority source.
- Where sources conflict, higher authority remains controlling.
- A material contradiction affecting the current action must be surfaced,
  not silently resolved.
- The affected implementation or policy mutation is blocked until the
  conflicting sources are reconciled.
- The lower-authority source is corrected to match, unless the
  higher-authority source is itself amended through its own governed
  procedure (Constitution §7 for level 1; a new governance decision for
  level 2/3).
- Unrelated work is not blocked by an immaterial or task-irrelevant wording
  difference.
- Recency and specificity may aid interpretation only *between sources at
  the same authority level* — never across levels.
- Recency or specificity alone never creates supersession of a
  higher-authority source by a lower one.
- Supersession must be explicit — through a status change, a stated
  amendment, a stated replacement, or a clearly identified later accepted
  record at the same or higher level.

Subject to explicit human approval, and executed only through a separate
implementation PR (this decision record does not itself edit any file),
this decision authorizes exactly five file edits:

1. `constitution/INVESTMENT_CONSTITUTION.md` — revise the introduction;
   add new §8 ("Operational precedence"), §7 unchanged.
2. `governance/decisions/GOV-0002-operational-precedence-hierarchy.md` —
   this file (new).
3. `governance/decisions.yaml` — new `GOV-0002` index entry.
4. `CLAUDE.md` — retitle; revise the governance paragraph in Identity & Role.
5. `docs/PORTFOLIO_POLICY_MANUAL.md` — revise the document-status header.

No allocator, `targets.yaml`, `holdings.yaml`, margin-rule, Company/Theme
Intelligence content, or code change is authorized by this decision.

## Rationale

GOV-0001 and `governance/README.md` established the documentation
architecture but did not state the complete operational precedence order
across it — the Constitution's introduction, CLAUDE.md's title, and the
Policy Manual's document-status line each made a partial, sometimes
conflicting claim instead. This decision clarifies that order and corrects
the contradictory self-description; it does not claim the hierarchy was
previously wholly undocumented, only that no single document stated it
completely and consistently, and that at least one existing statement (the
Constitution's recency/specificity conflict sentence) actively pointed the
wrong direction. This rests on Constitution §5 (fixed, mechanical,
no-exception limits — the same reasoning that rejects discretionary
override applies to rejecting discretionary *authority* override) and §6
(verify before acting on external or lower-confidence claims, the same
principle applied here to lower-ranked sources).

## Alternatives Considered

- **Leave the existing partial, scattered self-descriptions as-is.**
  Rejected — demonstrated to produce a regression this correction exists
  to fix.
- **Allow recency or specificity to operate across authority levels.**
  Rejected — it would let any lower-ranked source override a
  higher-ranked one by merely being newer or more specific, inverting the
  authority relationship GOV-0001 established.
- **Give `decision_log.yaml` a separate bottom-ranked tier**, apart from
  `governance/decisions/`. Rejected — it is evidence of historical,
  already-accepted decisions in the same domain that GOV-0001 explicitly
  left in place, unmigrated (`governance/decisions/README.md`), not a
  lesser category of decision.
- **Reproduce the full eight-level hierarchy inside the Constitution
  itself.** Rejected — the Constitution changes "rarely, and only through
  its own amendment process" (§7); a hierarchy that must accommodate new
  specification and decision types over time belongs in an amendable
  governance decision, not the document hardest to amend.
- **Treat the Portfolio Policy Manual or `decision_log.yaml` as independent
  authority tiers**, as the Manual's current header does. Rejected — both
  are folded into their correct existing levels (8 and 2, respectively);
  inventing separate tiers for them was never justified by anything in
  GOV-0001.

## Consequences

Going forward: any future conflict between two governed sources is
resolved by rank, not by which is newer or more specific, except between
sources at the same rank. CLAUDE.md, the Policy Manual, and the
Constitution's own introduction are brought into agreement with this
hierarchy (edits enumerated above, applied only via a future implementation
PR after explicit approval).

Explicitly unchanged: GOV-0001's text and status; `governance/README.md`;
Constitution §7; `allocate.py`, `targets.yaml`, `holdings.yaml`, margin
rules; any Company/Theme Intelligence record. Conversation approval
authorizes implementation of this exact decision; filing it on a branch and
opening a pull request does not make it effective. GOV-0002 and the
authorized synchronized edits become effective only when the reviewed
implementation pull request merges to `main`.
