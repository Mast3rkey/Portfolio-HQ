# INTC — Intel Corporation

Last updated: 2026-07-26 — created through AI-assisted research, pending
independent PR review and human approval under `PI-0025` (WS-0005 Milestone 3,
Batch 3).

## Source-access disclosure

WebFetch (direct primary-document retrieval) was attempted fresh this session
against SEC EDGAR and intc.com URLs identified during research, plus a
non-target control domain — **all attempts returned HTTP 403**, consistent
with the tool/proxy-level block independently confirmed once for this entire
batch's research session (see `AVGO.md`'s Source-access disclosure for the
control-domain test). **No primary document was directly opened and
inspected by this session at any point.** Every fact below is
WebSearch-sourced: either a primary document identified but not opened
(PRIMARY, NOT OPENED) or secondary journalism/analyst commentary (SECONDARY).

**PI-0014 note:** this repository's prior bounded, conversation-only
evidence review (`governance/decisions/PI-0014-intc-syk-dhr-bounded-evidence-review.md`)
examined INTC's own committed TSM/INTC overlap question but produced no
repository artifact and no filed Company Intelligence record. Per `PI-0025`
§B's explicit instruction, that prior review is treated strictly as context
for this session — no fact from it is repeated or relied upon here, and it
is not treated as, or as a substitute for, a filed record.

## Business summary

Intel is an integrated device manufacturer (IDM) — it designs and
manufactures its own client and server CPUs, and is separately pursuing a
strategy to sell manufacturing capacity to external foundry customers
through Intel Foundry [S1, S3]. Q2 2026 (reported ~2026-07-23) revenue was
$16.1B, reported +25% year-over-year — characterized in secondary coverage
as the fastest growth rate since 2011 — and $1.8B above the midpoint of
prior guidance [S1]. Non-GAAP gross margin was 41.8% (~280 basis points
above guidance) and non-GAAP EPS was $0.42 (more than double the guided
$0.20) [S1]. Data Center and AI segment revenue was $6.3B (+59% YoY); Client
Computing Group revenue was $8.9B (+13% YoY) [S1]. Management raised
full-year 2026 capital-spending guidance to more than $20B [S1] —
characterized in secondary coverage as signaling growing confidence in
customer commitments for the 18A and 14A foundry nodes.

## Client and server CPU position

Both of Intel's core CPU businesses grew in Q2 2026: Client Computing Group
+13% YoY to $8.9B, and Data Center and AI +59% YoY to $6.3B [S1]. This
record's own AMD record (`AMD.md`) documents AMD as an active competitor in
both markets — Intel's Q2 2026 growth does not by itself establish market-
share gain against AMD specifically, since both companies reported growth in
the same period; a direct, reconciled market-share comparison was not
constructed in this research pass.

## Competitive pressure from AMD, ARM-based architectures, and TSMC-manufactured products

AMD (this batch, see `AMD.md`) competes directly with Intel in server and
client CPUs. ARM-based architectures and TSMC-manufactured competitor
products (including designs from AMD, NVIDIA, and others fabricated at
TSMC rather than Intel) represent a structural competitive pressure on
Intel's own manufacturing value proposition — if a chip can be designed for
ARM's instruction set or manufactured competitively at TSMC, Intel's
integrated design-and-manufacture model faces competition on both the
design side (x86 versus ARM) and the manufacturing side (Intel fabs versus
TSMC) simultaneously. No quantified Intel-specific market-share-loss figure
attributable to ARM competition was located in this research pass.

## Intel Foundry strategy and external-customer credibility

Intel Foundry segment revenue was $5.8B in Q2 2026, up 31% YoY (+6%
sequentially), of which **external (non-Intel) revenue was $293M** [S1] — a
small but nonzero and reportedly growing contribution.

**Fortinet is Intel Foundry's one actually-named, publicly confirmed
external customer** [S7], disclosed 2026-07-21: Intel will co-develop and
manufacture Fortinet's next-generation Security Processor 6 custom silicon
(powering the FortiGate firewall lineup) at Intel's Fab 34 facility in
Leixlip, Ireland, on the **Intel 4 process node** — a mature node that
debuted in 2022, not 18A or 14A. Multiple independent, concordant outlets
(SiliconANGLE, Tom's Hardware, The Register, TechTimes) report this as
Intel's first willingness to publicly name an external Intel 4 customer,
roughly three years after that node entered high-volume production
exclusively for Intel's own chips [S7]. This is a real, confirmed customer
relationship on a mature node — it is not evidence of 18A or 14A external
traction specifically.

Separately, design wins/commitments for **18A specifically** are reported
across AMD, NVIDIA, Marvell, Microsoft, Micron, and OpenAI, with a US
aerospace-and-defense customer bringing external-customer commitments on
Intel 18A to six by one secondary count [S4]. Specific reported programs
include a Microsoft Maia 2 AI-processor contract and an AI-fabric-chip
agreement with Amazon [S4]. **These 18A-specific names remain hedged/
secondary-sourced and unconfirmed by any primary disclosure this session
opened — in contrast to Fortinet's Intel-4 relationship, which is
independently and concordantly reported across multiple outlets as an
actual named, announced customer relationship, not a rumored design win.
This record does not conflate the two categories: one confirmed mature-node
customer (Fortinet) versus six hedged/rumored leading-edge-node design wins
(the 18A list).**

**Critically, this credibility is explicitly conditional going forward, not
established:** Intel has disclosed that it may pause or discontinue pursuit
of the 14A node (and further leading-edge nodes beyond it) if it cannot
secure sufficient committed demand through product design wins with
significant external customers [S5]. Secondary analysis frames 14A, not
18A, as the "real contest" and "decisive battle" for Intel Foundry's
viability as an external foundry business, expected to play out around
2027, on the stated reasoning that 18A is "not the ideal process for most
external foundry customers" [S5].

## Manufacturing roadmap and process-node execution; yield and execution risk

Q2 2026 output on the 18A node reportedly exceeded internal targets by
roughly 25%, with total output more than 50% higher quarter-over-quarter;
management is reported to have highlighted "strong execution" on 18A and
18A-P with yields "tracking ahead of expectations" [S1]. This is real,
verified-against-management's-own-statements positive data. **This record
deliberately does not extrapolate sustained future execution from this
result alone**: Intel has a multi-year public history of missed
leading-edge-node targets predating the current 18A/14A roadmap (well
established in public reporting and implicit in the "inflection point" and
"last chance" framing used in secondary coverage of Intel Foundry in 2026),
and the current positive data represents a small number of consecutive
positive data points against that longer history.

## Capital intensity; subsidies and government support; restructuring

Total planned US manufacturing investment is reported at more than $100B
across Arizona, New Mexico, Ohio, and Oregon, including up to $7.86B in
direct CHIPS Act funding for commercial manufacturing projects at those
sites [S6]. The Ohio "Silicon Heartland" project (>$28B, reported as the
largest private-sector investment in Ohio's history) is reported delayed
until 2030 [S6]. 2026 capital-spending guidance was raised to more than
$20B [S1].

Cumulative layoffs are reported at 23,000 across three phases: Phase One
(August 2024, ~15,000 positions), Phase Two (March 2025, ~4,200 positions,
primarily foundry-focused), and Phase Three (January 2026, ~3,800 positions,
sales/customer-support focused) [S4]. Secondary reporting indicates further
cuts are signaled as possible if the foundry business does not hit
external-customer commitments and if 18A external-ramp targets continue
slipping [S4] — meaning the positive Q2 2026 results and 18A execution news
coexist with an explicit, management-signaled threat of further
restructuring, not a completed turnaround.

## Liquidity, debt, and funding requirements

The US Department of Commerce converted $8.9B of previously-awarded but
undisbursed CHIPS Act grant/Secure Enclave funding into a US government
equity stake in August 2025, alongside accelerated direct-funding-agreement
disbursements of $5.695B and issuance of 274,583,000 shares plus a warrant
for up to 240,516,150 additional shares to the DOC [S2]. **The exact
resulting government ownership percentage is reported inconsistently across
sources — 8.4% (as of 2026-03-20, per one primary-filing-adjacent secondary
source), 9%, 9.9%, and 10% all appear across different sources/dates; this
record does not resolve the discrepancy**, which may partly reflect
different measurement dates given subsequent share issuances [S2, S6].
Separately, NVIDIA is reported to have finalized a $5B equity stake
(approximately 4% ownership) via private placement after FTC approval, and
SoftBank is reported to have invested/agreed to invest $2B (approximately 2%
stake, reported to make SoftBank Intel's fifth-largest shareholder) [S6].
Remaining CHIPS Act/DFA funding terms are reported to prohibit dividends and
stock buybacks, limit certain foreign expansions/collaborations, and
preserve US government remedies (including potential award repayment) in
the event of a breach [S6].

## Geopolitical and domestic-manufacturing relevance

Intel's domestic US fab buildout (Arizona, New Mexico, Ohio, Oregon) and its
new US government equity stake place Intel's foundry strategy more directly
within US industrial policy and national-security framing than any other
company in this batch — this is a structural characteristic of Intel's
current position, not a hypothetical risk. The national-security framing
cuts in Intel's favor for domestic-manufacturing-policy support, but also
means CHIPS-Act-funding and foundry-strategy decisions are subject to
political considerations (dividend/buyback restrictions, foreign-
collaboration limits, breach-remedy provisions) that a purely commercially-
governed company would not carry [S6].

## Margin-relevant turnaround, execution, refinancing, gap-risk, and prolonged-recovery evidence

*(Factual, advisory only — no leverage, deployment-timing, or margin-ceiling
recommendation.)* Intel's liquidity position has been materially strengthened
by the government/NVIDIA/SoftBank capital infusions [S2, S6] ahead of a very
large, multi-year, geographically-concentrated domestic capital-spending
program (>$100B total, >$20B guided for 2026 alone) [S1, S6] — a
**capital-intensity and gap-risk profile structurally different from every
other company in this batch**, whose expansions (per this batch's own AVGO,
AMD, and MRVL records, and this repository's Batch 1/Batch 2 records) are
more geographically diversified. A large, long-duration, single-project
delay (the Ohio project, reported delayed to 2030) [S6] illustrates
**prolonged-recovery risk**: capital committed to a fixed, large project
that slips does not become available for redeployment elsewhere in the near
term. The explicit 14A pause/discontinuation contingency [S5] is itself a
disclosed **thesis-deterioration-detectability** mechanism — Intel has told
the market what evidence (insufficient committed external demand) would
cause it to abandon its own foundry-turnaround strategy, which is a more
observable trigger than most companies disclose for their own strategic
pivots. Restructuring costs (23,000 cumulative layoffs, more signaled as
possible) [S4] represent an ongoing cash and execution drag layered on top
of the capital-spending program, not a one-time, already-absorbed cost.

## What exposure would be lost if INTC were absent from the portfolio

*(Research analysis only — this section does not recommend any allocation
action.)* Intel is currently the portfolio's only holding providing direct
exposure to a US-headquartered, US-manufacturing-concentrated integrated
device manufacturer pursuing an external-foundry strategy — a structurally
distinct position from TSM (also held; dedicated pure-play foundry, no
in-house chip design) and from every fabless company in this batch (AVGO,
AMD, MRVL). This record's own TSM Company Intelligence record separately
notes that "TSM is not the portfolio's only holding with some semiconductor-
manufacturing or foundry-related exposure" via INTC, without establishing
the degree of overlap — this record does not resolve that overlap question
either; it is deferred to any future, separately-authorized relationship-
mapping work (WS-0005 Milestone 4, not yet authorized).

## Current governed tier and target (existing policy, not research evidence)

`targets.yaml` currently places INTC in the **spec tier** (1.00% fixed
target, sized at exactly target, never above — no RSI-gated trim rule
applies) and in the `semis` correlated-cluster cap (≤25% of book). **This is
preserved here as historical, currently-governed policy only, per
`OPS-0006` §2/§3's zero-based research discipline — it is not evidence
supporting, and was not used to derive, this record's conviction rating,
role, or any other research conclusion above.**

## Review framework

- Cadence: 90 days, matching every other Batch 1/2/3 first-coverage record
  in this repository.
- Unscheduled-review triggers: any disclosed update on the 14A external-
  demand contingency (a design win, a pause, or a discontinuation
  announcement); a material change in Intel Foundry external revenue or
  external-customer count; a further restructuring/layoff phase; a material
  change in the reported government/NVIDIA/SoftBank ownership percentages or
  terms; a material Data Center/AI or Client Computing Group guidance
  change; a material domestic-fab-project delay or acceleration (Arizona,
  Ohio, New Mexico, Oregon).
- Metrics worth monitoring each review: quarterly revenue/margin versus
  guidance, Intel Foundry external revenue specifically, 18A/14A yield and
  output commentary, cumulative layoff count, and capital-spending guidance.

## Conviction

**Rating: Medium**

**Rationale:** see the YAML `conviction.rationale` field — reproduced there
in full to avoid duplication drift between the two files.

This rating and rationale reflect AI-assisted research pending the
independent PR review and human approval this repository's first-coverage
discipline requires before this record is treated as finalized.

## Portfolio role reference

`portfolio_role_ref: spec` reflects `targets.yaml`'s current tier placement,
recorded here descriptively per PI-0003's unchanged doctrine — this field is
a human-authored reference fixed at authoring time, not an allocator input,
and does not itself authorize or derive any allocation behavior. Recording
it here does not modify or reaffirm allocator policy; `targets.yaml` remains
the sole authority for actual tier weights and allocation.

## Theme membership

None. This record does not assign INTC to any Theme Intelligence theme.
`PI-0025` does not authorize a theme-membership determination for any
company in this batch, and no such determination is made here — consistent
with Batch 1 (ASML/AMAT/KLAC/LRCX) and Batch 2 (MU/SKHY), neither of which
received a theme assignment either.

## Sources

- [S1] Intel Corporation, Second-Quarter 2026 Financial Results press release (PRIMARY, NOT OPENED — WebFetch returned HTTP 403), https://www.intc.com/news-events/press-releases/detail/1776/intel-reports-second-quarter-2026-financial-results, 2026-07-23
- [S2] Intel Corporation Form 8-K / related SEC filing on the US Department of Commerce equity-stake transaction (PRIMARY, NOT OPENED — WebFetch returned HTTP 403), https://www.stocktitan.net/sec-filings/INTC/8-k-intel-corp-reports-material-event-6d9724241f00.html, 2026-03-20
- [S3] SECONDARY, Intel Foundry strategy overview coverage, 2026-07-26
- [S4] SECONDARY, restructuring/layoff coverage (TechPowerUp, KORE1, circuit-chip.com), 2026-07-26
- [S5] SECONDARY, 14A external-demand-contingency analysis (Forbes, Electronics Weekly, Manufacturing Dive), 2026-07-26
- [S6] SECONDARY, capital-investment and government/NVIDIA/SoftBank stake coverage (TechRepublic, Data Center Dynamics, ts2.tech, NIST CHIPS program pages), 2026-07-26
- [S7] SECONDARY, Intel Foundry's Fortinet customer disclosure (SiliconANGLE, Tom's Hardware, The Register, TechTimes — independently located in this bounded correction pass), 2026-07-21
