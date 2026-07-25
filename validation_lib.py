"""
validation_lib.py — MARGIN-0005 research-only isolation-guard and
statistical-validation library (S2, third and final authorized S2 PR under
the charter's <=3 ceiling; scope per `research/margin_target_study/
S2_G2_SCOPE_DETERMINATION.md` §5, item 2).

Authorized by `governance/decisions/MARGIN-0005-margin-target-research-charter.md`
(charter §4, "Research package" row) and `PROTOCOL_V2.md` §13. Closes the
literal G2-gate obligations for **T-D4** (structural TR bar), **T-U1**
(untouched-mode legality), and **T-U2** (candidate-freeze append-only /
hash-membership) identified in the scope determination §3, and bundles the
protocol §11 / T-7 statistical-validation machinery (bootstrap, DSR,
walk-forward fold boundaries) the determination groups here as "needed
regardless of when Study A/B actually run... both are 'validation'
concerns per the protocol's own module naming."

## Scope and isolation

Zero import relationship with `allocate.py`/`margin_state.py` in either
direction. No network I/O anywhere. The only file I/O in this module is:
(a) read-only access to the quarantined TR namespace
(`research/margin_target_study/data/quarantine_yahoo/`) — this module is
the ONE place in the research package licensed to touch it (protocol §14
T-D4: "simulation runners and `dividend_ledger.py` cannot reference the TR
namespace; only `validation_lib.py` may"); (b) the candidate-freeze
guard functions below, which operate ONLY against a caller-supplied path —
tests exercise them exclusively against `tmp_path` fixtures, never the real
`research/margin_target_study/candidate_freeze.yaml` (which this PR does
not create; that artifact is a G3 act, out of scope here).

This module never calls `margin_simulation.simulate()`, never touches
`trial_ledger.jsonl`, and consumes zero of the 300-run trial ceiling. It
performs no statistical work that itself constitutes a registered trial —
`bootstrap`/`dsr`/`walk_forward_folds` below are pure, deterministic
functions over caller-supplied numeric series, exercised only against
small synthetic fixtures in this PR's own tests.

## Statistical-machinery disclosure

`deflated_sharpe_ratio()` implements the standard Bailey & López de Prado
("The Deflated Sharpe Ratio," 2014) probabilistic-Sharpe-ratio-at-the-
expected-maximum-of-N-trials construction, using a closed-form rational
approximation of the inverse standard normal CDF (Peter Acklam's
algorithm — no `scipy`/`numpy` dependency). It is exercised here only
against internally hand-computed, self-consistent worked examples (this
PR introduces no external published reference table to validate against);
the pre-registered "DSR <= 0 at 95%" acceptance rule (`pre_registration.yaml`
`dsr.fail_below: 0_at_95pct`) is applied by a future study-run caller, not
by this module — this library computes the statistic, it does not itself
gate anything, consistent with S2's additive-library-only scope.
"""

from __future__ import annotations

import ast
import json
import math
import random
from datetime import date
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_RESEARCH = _HERE / "research" / "margin_target_study"
_TR_DIR = _RESEARCH / "data" / "quarantine_yahoo" / "tr"
_TRACK3_DIR = _RESEARCH / "data" / "quarantine_yahoo" / "track3"


# ═════════════════════════════════════════════════════════════════════════
# TR-namespace + import-graph isolation (T-D4 / T-8 extension)
# ═════════════════════════════════════════════════════════════════════════

# Literal tokens that only ever appear in this repository in connection with
# the quarantined total-return namespace (directory names, field names, and
# variable names data_acquisition.py itself uses for TR-only data). A plain
# substring scan of a module's full source text — not merely its AST Name
# nodes — deliberately catches string-literal references (dict keys, path
# fragments) as readily as identifier references.
TR_NAMESPACE_MARKERS = frozenset({
    "quarantine_yahoo", "TR_DIR", "TRACK3_DIR", "adjclose",
    "dividends_split_adjusted_yahoo", "close_raw", "adjclose_quarantined_tr",
})


def scan_tr_namespace_references(path: str) -> frozenset[str]:
    """Return the subset of `TR_NAMESPACE_MARKERS` present anywhere in the
    given module's source text. An empty result means the module is clean
    of TR-namespace references (T-D4)."""
    src = open(path).read()
    return frozenset(m for m in TR_NAMESPACE_MARKERS if m in src)


def assert_module_does_not_reference_tr_namespace(path: str) -> None:
    """T-D4 structural bar: raises if the given module references the TR
    namespace anywhere. Simulation runners and `dividend_ledger.py` must
    pass this; this module (`validation_lib.py`) is deliberately exempt
    from ever being checked by this function against itself, since its own
    constants and docstring above necessarily name these markers."""
    hits = scan_tr_namespace_references(path)
    if hits:
        raise AssertionError(f"{path} references TR-namespace marker(s): {sorted(hits)}")


def imported_module_names(path: str) -> set[str]:
    """Top-level import target names (module or `from`-source), by full
    dotted path — the same AST-walk pattern already used by
    `test_margin_simulation.py`'s and `test_repayment_lib.py`'s own
    isolation tests, exposed here as a reusable helper rather than
    reimplemented ad hoc in every new test file."""
    tree = ast.parse(open(path).read())
    names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            names.add(node.module)
    return names


def assert_no_forbidden_imports(path: str, forbidden: frozenset[str]) -> None:
    """T-8 isolation: raises naming every forbidden module the given source
    file imports (by exact matched name — matching the existing
    `test_module_source_never_imports_allocate_or_margin_state()` /
    `test_module_source_imports_only_approved_dependencies()` pattern)."""
    hit = imported_module_names(path) & set(forbidden)
    if hit:
        raise AssertionError(f"{path} imports forbidden module(s): {sorted(hit)}")


_WRITE_MODES = {"w", "wb", "a", "ab", "x", "xb", "w+", "r+", "a+"}


def assert_module_never_opens_files_for_write(path: str) -> None:
    """T-8 write-path isolation: raises if the given module contains any
    `open(...)` call whose literal mode argument requests write access.
    Catches every write-capable literal mode string; a call with a
    non-literal (computed) mode would not be caught by this static scan —
    none of the modules checked with this function do that."""
    tree = ast.parse(open(path).read())
    offenders = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "open":
            mode = None
            if len(node.args) >= 2 and isinstance(node.args[1], ast.Constant):
                mode = node.args[1].value
            for kw in node.keywords:
                if kw.arg == "mode" and isinstance(kw.value, ast.Constant):
                    mode = kw.value.value
            if isinstance(mode, str) and mode in _WRITE_MODES:
                offenders.append((getattr(node, "lineno", None), mode))
    if offenders:
        raise AssertionError(f"{path} opens file(s) for write: {offenders}")


# ═════════════════════════════════════════════════════════════════════════
# Untouched-mode isolation guard (T-U1)
# ═════════════════════════════════════════════════════════════════════════
#
# No real research data loader or G4 runner exists yet (both are S4 scope,
# not authorized by this PR). The scope determination's own §3 table is
# explicit that T-U1's LEGALITY-CHECK half is "buildable now, without
# building the real G4 runner — the test exercises the guard's legality
# check, not an actual future runner." This is that guard: the one context
# marker a future G4 runner would supply, and nothing else, is legal.

G4_RUNNER_CONTEXT = "g4_runner_authorized_untouched_evaluation"


def guard_untouched_mode_access(context: str) -> None:
    """Raises `PermissionError` unless invoked with the exact G4-runner
    context marker (protocol §14 T-U1: "untouched-mode flag is rejected
    outside the G4 runner"). A future real loader/runner calls this before
    honoring an untouched-mode request; every other caller is illegal by
    construction."""
    if context != G4_RUNNER_CONTEXT:
        raise PermissionError(
            f"untouched-mode access is illegal outside the G4 runner context "
            f"(got {context!r}) — see PROTOCOL_V2.md §11/§14 T-U1")


def assert_no_untouched_period_timestamps(dates_: list[str], boundary: str) -> None:
    """Protocol §14 T-U1's second half: "G3 report generators fail on any
    untouched-period timestamp in their inputs." No G3 report generator
    exists yet (out of scope for this PR); this is the reusable guard a
    future one calls on its own input dates. Raises naming every date past
    `boundary`."""
    bad = [d for d in dates_ if d > boundary]
    if bad:
        raise AssertionError(
            f"untouched-period timestamp(s) present in a development/G3-report "
            f"input (boundary {boundary}): {sorted(bad)[:10]}")


# ═════════════════════════════════════════════════════════════════════════
# Candidate freeze — append-only, hash-membership (T-U2)
# ═════════════════════════════════════════════════════════════════════════
#
# Operated ONLY against a caller-supplied path. This module never creates,
# reads, or writes the real `research/margin_target_study/candidate_freeze.yaml`
# — that artifact is authorized only at the real G3 freeze (protocol §11
# item 3), which this PR does not perform. Tests exercise these functions
# exclusively against `tmp_path` fixtures.

def canonical_config_hash(config: dict) -> str:
    """SHA-256 of the config's canonical JSON form (sorted keys, no
    incidental whitespace) — the "full configuration hash" the freeze
    records (protocol §11 item 3; `pre_registration.yaml`
    `candidate_freeze.contents`)."""
    import hashlib
    blob = json.dumps(config, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(blob).hexdigest()


def load_frozen_candidates(path: str) -> list[dict]:
    p = Path(path)
    if not p.exists():
        return []
    with open(p) as f:
        return json.load(f)


def append_candidate_freeze(path: str, new_entries: list[dict]) -> list[dict]:
    """Append-only write: each entry requires `finalist_id`, `config`, and
    `config_hash` (must equal `canonical_config_hash(config)`). Raises
    (writes nothing) if:
      * `config_hash` does not match a fresh hash of `config`;
      * `finalist_id` is already frozen (in this file or earlier in this
        same call) — a modified candidate requires a NEW finalist_id; per
        protocol §11 item 5, "any change to a frozen candidate's
        configuration after the freeze voids its untouched result," so
        reusing an id for a changed config is refused outright rather than
        silently accepted;
      * `config_hash` is already frozen under a different id (duplicate
        candidate).
    On success, returns the combined (existing + new) list, having written
    it to `path` — existing entries are always carried forward unchanged,
    never dropped or reordered."""
    existing = load_frozen_candidates(path)
    existing_ids = {e["finalist_id"] for e in existing}
    existing_hashes = {e["config_hash"] for e in existing}
    seen_ids: set = set()
    seen_hashes: set = set()
    for e in new_entries:
        for key in ("finalist_id", "config", "config_hash"):
            if key not in e:
                raise ValueError(f"candidate-freeze entry missing required field {key!r}")
        if e["config_hash"] != canonical_config_hash(e["config"]):
            raise ValueError(f"config_hash mismatch for finalist_id {e['finalist_id']!r}")
        if e["finalist_id"] in existing_ids or e["finalist_id"] in seen_ids:
            raise ValueError(
                f"finalist_id {e['finalist_id']!r} is already frozen — append-only "
                "(a modified candidate requires a new finalist_id; a "
                "configuration change voids the old candidate, protocol §11 item 5)")
        if e["config_hash"] in existing_hashes or e["config_hash"] in seen_hashes:
            raise ValueError(f"config_hash {e['config_hash']} is already frozen")
        seen_ids.add(e["finalist_id"])
        seen_hashes.add(e["config_hash"])
    combined = existing + list(new_entries)
    with open(path, "w") as f:
        json.dump(combined, f, indent=2, sort_keys=True)
    return combined


def is_frozen(path: str, config_hash: str) -> bool:
    return any(e["config_hash"] == config_hash for e in load_frozen_candidates(path))


def assert_frozen(path: str, config_hash: str) -> None:
    """Untouched-runner guard (T-U2): raises unless `config_hash` is
    present in the freeze at `path`. No G4 runner exists yet; this is the
    reusable legality check a future one calls before evaluating any
    configuration against the untouched period."""
    if not is_frozen(path, config_hash):
        raise PermissionError(
            f"config_hash {config_hash} is not in the candidate freeze at {path} "
            "— untouched-period evaluation is illegal for an unfrozen "
            "configuration (T-U2)")


def verify_candidate_freeze_integrity(path: str) -> bool:
    """True iff every entry's stored `config_hash` matches a fresh hash of
    its stored `config` — detects direct file tampering (an entry's
    `config` edited without updating `config_hash`, bypassing the
    `append_candidate_freeze()` API entirely)."""
    return all(e["config_hash"] == canonical_config_hash(e["config"])
              for e in load_frozen_candidates(path))


# ═════════════════════════════════════════════════════════════════════════
# Statistical-validation machinery (T-7 / protocol §11)
# ═════════════════════════════════════════════════════════════════════════

# ── stationary block bootstrap (seeded, reproducible) ───────────────────────

def stationary_block_bootstrap(series: list[float], *, mean_block_days: int = 21,
                               resamples: int = 1000, seed: int) -> list[float]:
    """Stationary block bootstrap (Politis & Romano) over a daily
    differential series (protocol §11; `pre_registration.yaml`
    `bootstrap: {method: stationary_block, mean_block_days: 21,
    resamples: 1000}`). Returns `resamples` bootstrap-replicate MEANS of
    `series`, each computed from a resampled path of the same length as
    `series`, built by concatenating randomly-placed blocks whose lengths
    are drawn from a geometric distribution with mean `mean_block_days`
    (wrapping around the series — standard stationary-bootstrap
    construction, preserves short-range dependence unlike an iid bootstrap).

    `seed` is REQUIRED (T-7: "seeded bootstrap reproducibility") — identical
    `series`/`mean_block_days`/`resamples`/`seed` always produce byte-
    identical output; this module bakes in no default seed of its own."""
    n = len(series)
    if n == 0:
        raise ValueError("series must be non-empty")
    if mean_block_days <= 0:
        raise ValueError(f"mean_block_days must be > 0, got {mean_block_days}")
    if resamples <= 0:
        raise ValueError(f"resamples must be > 0, got {resamples}")
    rng = random.Random(seed)
    p = 1.0 / mean_block_days   # geometric-block continuation probability
    out: list[float] = []
    for _ in range(resamples):
        path: list[float] = []
        while len(path) < n:
            start = rng.randrange(n)
            block_len = 1
            while rng.random() > p and len(path) + block_len < n + mean_block_days * 4:
                block_len += 1
            for k in range(block_len):
                path.append(series[(start + k) % n])
                if len(path) >= n:
                    break
        out.append(sum(path[:n]) / n)
    return out


# ── inverse standard normal CDF (Acklam's rational approximation) ──────────
# No scipy/numpy dependency; ~1.15e-9 relative-error accuracy, a standard,
# widely-published closed-form approximation (Peter Acklam, 2003).

_ACKLAM_A = (-3.969683028665376e+01, 2.209460984245205e+02, -2.759285104469687e+02,
            1.383577518672690e+02, -3.066479806614716e+01, 2.506628277459239e+00)
_ACKLAM_B = (-5.447609879822406e+01, 1.615858368580409e+02, -1.556989798598866e+02,
            6.680131188771972e+01, -1.328068155288572e+01)
_ACKLAM_C = (-7.784894002430293e-03, -3.223964580411365e-01, -2.400758277161838e+00,
            -2.549732539343734e+00, 4.374664141464968e+00, 2.938163982698783e+00)
_ACKLAM_D = (7.784695709041462e-03, 3.224671290700398e-01, 2.445134137142996e+00,
            3.754408661907416e+00)
_ACKLAM_PLOW = 0.02425


def norm_cdf(x: float) -> float:
    """Standard normal CDF via the exact `math.erf` closed form."""
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def norm_ppf(p: float) -> float:
    """Inverse standard normal CDF (probit) via Acklam's rational
    approximation. `p` must be in the open interval (0, 1)."""
    if not (0.0 < p < 1.0):
        raise ValueError(f"p must be in (0, 1), got {p}")
    phigh = 1.0 - _ACKLAM_PLOW
    if p < _ACKLAM_PLOW:
        q = math.sqrt(-2.0 * math.log(p))
        return (((((_ACKLAM_C[0]*q+_ACKLAM_C[1])*q+_ACKLAM_C[2])*q+_ACKLAM_C[3])*q+_ACKLAM_C[4])*q+_ACKLAM_C[5]) / \
              ((((_ACKLAM_D[0]*q+_ACKLAM_D[1])*q+_ACKLAM_D[2])*q+_ACKLAM_D[3])*q+1.0)
    if p > phigh:
        q = math.sqrt(-2.0 * math.log(1.0 - p))
        return -(((((_ACKLAM_C[0]*q+_ACKLAM_C[1])*q+_ACKLAM_C[2])*q+_ACKLAM_C[3])*q+_ACKLAM_C[4])*q+_ACKLAM_C[5]) / \
               ((((_ACKLAM_D[0]*q+_ACKLAM_D[1])*q+_ACKLAM_D[2])*q+_ACKLAM_D[3])*q+1.0)
    q = p - 0.5
    r = q * q
    return (((((_ACKLAM_A[0]*r+_ACKLAM_A[1])*r+_ACKLAM_A[2])*r+_ACKLAM_A[3])*r+_ACKLAM_A[4])*r+_ACKLAM_A[5]) * q / \
          (((((_ACKLAM_B[0]*r+_ACKLAM_B[1])*r+_ACKLAM_B[2])*r+_ACKLAM_B[3])*r+_ACKLAM_B[4])*r+1.0)


# ── deflated Sharpe ratio ────────────────────────────────────────────────────

EULER_MASCHERONI = 0.5772156649015329


def expected_max_sharpe(n_trials: int, *, sharpe_std: float = 1.0) -> float:
    """Expected maximum Sharpe ratio achievable by chance across `n_trials`
    independent trials under the null (Bailey & López de Prado 2014),
    scaled by `sharpe_std` (the cross-trial standard deviation of the
    Sharpe estimates; the default 1.0 returns the pure standard-normal
    order-statistic quantity). `n_trials=1` returns 0.0 — a single trial
    carries no multiple-testing inflation to deflate."""
    if not isinstance(n_trials, int) or isinstance(n_trials, bool) or n_trials < 1:
        raise ValueError(f"n_trials must be a positive int, got {n_trials!r}")
    if n_trials == 1:
        return 0.0
    term = ((1.0 - EULER_MASCHERONI) * norm_ppf(1.0 - 1.0 / n_trials)
           + EULER_MASCHERONI * norm_ppf(1.0 - 1.0 / (n_trials * math.e)))
    return sharpe_std * term


def probabilistic_sharpe_ratio(sr_hat: float, sr_benchmark: float, n_obs: int, *,
                               skew: float = 0.0, kurtosis: float = 3.0) -> float:
    """PSR(SR*): the probability the true Sharpe ratio exceeds
    `sr_benchmark`, given `n_obs` observations and the sample skew/
    (non-excess) kurtosis of the underlying return series (Bailey & López
    de Prado 2014). `kurtosis` uses the normal convention (normal = 3.0,
    not excess kurtosis = 0.0). Returns a probability in [0, 1]."""
    if n_obs < 2:
        raise ValueError(f"n_obs must be >= 2, got {n_obs}")
    denom = math.sqrt(1.0 - skew * sr_hat + ((kurtosis - 1.0) / 4.0) * sr_hat ** 2)
    if not (denom > 0):
        raise ValueError("degenerate PSR denominator — check skew/kurtosis/sr_hat inputs")
    z = (sr_hat - sr_benchmark) * math.sqrt(n_obs - 1) / denom
    return norm_cdf(z)


def deflated_sharpe_ratio(sr_hat: float, n_obs: int, n_trials: int, *,
                         skew: float = 0.0, kurtosis: float = 3.0,
                         sharpe_std: float = 1.0) -> float:
    """DSR (protocol §11; `pre_registration.yaml` `dsr: {trial_count:
    actual_disclosed, fail_below: 0_at_95pct}`): the probabilistic Sharpe
    ratio evaluated at the benchmark = the expected maximum Sharpe ratio
    achievable by chance across `n_trials` independent trials — i.e. the
    probability the observed edge is real net of the actual, disclosed
    multiple-testing burden. Returns a probability in [0, 1]. This module
    computes the statistic only; the pre-registered acceptance threshold is
    applied by the future study-run caller, not here."""
    benchmark = expected_max_sharpe(n_trials, sharpe_std=sharpe_std)
    return probabilistic_sharpe_ratio(sr_hat, benchmark, n_obs, skew=skew, kurtosis=kurtosis)


# ── walk-forward fold boundaries (exact calendar-month arithmetic) ─────────

def _add_months(d: date, months: int) -> date:
    total = d.month - 1 + months
    year = d.year + total // 12
    month = total % 12 + 1
    day = d.day
    while True:
        try:
            return date(year, month, day)
        except ValueError:
            day -= 1   # clip to the last valid day of the target month


def walk_forward_folds(train_start: str, dev_boundary: str, *,
                       initial_train_months: int, step_months: int = 6) -> list[dict]:
    """Expanding-window walk-forward folds (protocol §11: "expanding-window
    walk-forward (6-month steps)"). Returns a list of exact
    `{"train_start", "train_end", "test_start", "test_end"}` date-string
    dicts — pure calendar-month arithmetic, no data touched, no simulation
    run. The final fold's `test_end` is clipped to `dev_boundary`; a fold
    whose `test_start` would fall on or after `dev_boundary` is never
    generated (folds are development-period-only, per protocol §11 item 2 —
    "walk-forward folds are evaluation windows over stored
    DEVELOPMENT-period paths only")."""
    if step_months <= 0 or initial_train_months <= 0:
        raise ValueError("initial_train_months and step_months must be > 0")
    start = date.fromisoformat(train_start)
    boundary = date.fromisoformat(dev_boundary)
    folds: list[dict] = []
    train_end = _add_months(start, initial_train_months)
    while train_end < boundary:
        test_start = train_end
        test_end = min(_add_months(train_end, step_months), boundary)
        folds.append({
            "train_start": start.isoformat(),
            "train_end": train_end.isoformat(),
            "test_start": test_start.isoformat(),
            "test_end": test_end.isoformat(),
        })
        train_end = test_end
    return folds


# ── licensed TR-namespace access (this module only, per T-D4) ──────────────

def load_quarantined_tr(symbol: str) -> dict:
    """Read-only access to a roster ticker's quarantined total-return
    validation data (`research/margin_target_study/data/quarantine_yahoo/
    tr/{symbol}.json`) — licensed to this module alone (protocol §14
    T-D4). Used by `test_validation_lib.py`'s T-D2 purity check to prove
    the primary (split-adjusted, non-TR) price series genuinely diverges
    from the quarantined TR series for a known dividend payer; never
    merged into any primary-path dataset by this or any other function."""
    with open(_TR_DIR / f"{symbol}.json") as f:
        return json.load(f)


def load_track3_book(symbol: str) -> dict:
    """Read-only access to a Track 3 quarantined book (SPY/QQQ), same
    licensing as `load_quarantined_tr()` above."""
    with open(_TRACK3_DIR / f"{symbol}.json") as f:
        return json.load(f)
