"""
verify_rungs.py — audit charts for the rung backtest. NO new analysis.

Replays the exact mechanics (same cached bars, same rungs_current / rungs_sr /
fill_price functions) per ticker, then renders what happened so the report can
be eyeballed against reality:
  * daily close over the sim window
  * every deposit date
  * Arm A rung levels drawn across their active window (deposit → expiry)
  * actual fills (A and B) vs Arm C's market-buy price
Outputs: reports/verification/{SYM}.png + {SYM}_table.md + console summary.

Ticker selection is computable, not curated: per-ticker mini-sim of A vs C
(shares acquired per dollar); pick where rungs helped most, hurt most, median.

Run:  python3 verify_rungs.py
"""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import yaml

from backtest_rungs import (CACHE, MIN_HISTORY, MIN_TICKERS_TO_START,
                            rungs_current, rungs_sr, fill_price, roster_tickers)

HERE = Path(__file__).resolve().parent
OUT = HERE / "reports" / "verification"


def load_cached() -> dict[str, list[dict]]:
    data = {}
    for sym in roster_tickers():
        f = CACHE / f"{sym.replace('/', '_')}.json"
        if f.exists():
            data[sym] = json.loads(f.read_text())
    return data


def build_deposit_days(data: dict) -> tuple[list[str], list[str]]:
    """Identical derivation to backtest_rungs.main()."""
    calendar = [b["t"][:10] for b in data["SPY"]]
    dep_all, seen = [], set()
    for d in calendar:
        if d[:7] not in seen:
            seen.add(d[:7])
            dep_all.append(d)
    tix = {s: {b["t"][:10] for b in bars[MIN_HISTORY:]} for s, bars in data.items()}
    deposit_days = [d for d in dep_all
                    if sum(1 for s in tix if d in tix[s]) >= MIN_TICKERS_TO_START]
    calendar = [d for d in calendar if d >= deposit_days[0]]
    return calendar, deposit_days


def replay_ticker(sym: str, bars: list[dict], deposit_days: list[str],
                  cfg: dict) -> dict:
    """Instrumented single-ticker replay of the exact mechanics. $1 per rung
    (scale-free): returns events + shares-per-dollar for A and C."""
    ix = {b["t"][:10]: j for j, b in enumerate(bars)}
    next_dep = {d: (deposit_days[k + 1] if k + 1 < len(deposit_days) else None)
                for k, d in enumerate(deposit_days)}
    events = []
    spent = {"A": 0.0, "C": 0.0}
    shares = {"A": 0.0, "C": 0.0}

    for d in deposit_days:
        j = ix.get(d)
        if j is None or j + 1 < MIN_HISTORY:
            continue
        close = float(bars[j]["c"])
        expiry = next_dep[d]
        upto = bars[:j + 1]
        ra = rungs_current(upto, cfg)
        rb = rungs_sr(upto)

        # Arm C: $1 at close
        shares["C"] += 1.0 / close
        spent["C"] += 1.0

        ev = {"deposit": d, "close_c": close, "rungs_a": ra, "rungs_b": rb,
              "fills_a": [], "fills_b": [], "expired_a": 0, "expired_b": 0}

        for arm, rungs in (("A", ra), ("B", rb)):
            per = (1.0 / len(rungs)) if rungs else 0.0
            for lv in rungs:
                fp_found = None
                fdate = None
                k = j + 1
                while k < len(bars) and (expiry is None or bars[k]["t"][:10] < expiry):
                    fp = fill_price(lv, float(bars[k]["o"]), float(bars[k]["l"]))
                    if fp:
                        fp_found, fdate = fp, bars[k]["t"][:10]
                        break
                    k += 1
                if fp_found:
                    ev[f"fills_{arm.lower()}"].append((fdate, lv, fp_found))
                    if arm == "A":
                        shares["A"] += per / fp_found
                        spent["A"] += per
                else:
                    ev[f"expired_{arm.lower()}"] += 1
                    if arm == "A" and expiry and expiry in ix:   # expiry market-buy
                        px = float(bars[ix[expiry]]["c"])
                        shares["A"] += per / px
                        spent["A"] += per
        if not ra:                                   # no rungs → A buys now (as in sim)
            shares["A"] += 1.0 / close
            spent["A"] += 1.0
        events.append(ev)

    spd_a = shares["A"] / spent["A"] if spent["A"] else 0.0
    spd_c = shares["C"] / spent["C"] if spent["C"] else 0.0
    return {"events": events, "edge_pct": (spd_a / spd_c - 1.0) * 100 if spd_c else 0.0}


def chart(sym: str, bars: list[dict], rep: dict, deposit_days: list[str],
          window_start: str) -> Path:
    seq = [(b["t"][:10], float(b["c"])) for b in bars if b["t"][:10] >= window_start]
    dates = [d for d, _ in seq]
    dpos = {d: i for i, d in enumerate(dates)}
    closes = [c for _, c in seq]

    fig, ax = plt.subplots(figsize=(15, 7))
    ax.plot(range(len(dates)), closes, lw=1.0, color="#333", label="close")
    for d in deposit_days:
        if d in dpos:
            ax.axvline(dpos[d], color="#bbb", lw=0.5, zorder=0)

    next_dep = {d: (deposit_days[k + 1] if k + 1 < len(deposit_days) else dates[-1])
                for k, d in enumerate(deposit_days)}
    for ev in rep["events"]:
        d0, d1 = ev["deposit"], next_dep.get(ev["deposit"], dates[-1])
        if d0 not in dpos:
            continue
        x0 = dpos[d0]
        x1 = dpos.get(d1, len(dates) - 1)
        for lv in ev["rungs_a"]:
            ax.hlines(lv, x0, x1, color="#1f77b4", lw=0.8, alpha=0.6)
        for fdate, lv, fp in ev["fills_a"]:
            if fdate in dpos:
                ax.plot(dpos[fdate], fp, "v", color="#1f77b4", ms=7,
                        label="A fill" if "A fill" not in ax.get_legend_handles_labels()[1] else "")
        for fdate, lv, fp in ev["fills_b"]:
            if fdate in dpos:
                ax.plot(dpos[fdate], fp, "^", color="#2ca02c", ms=6,
                        label="B fill" if "B fill" not in ax.get_legend_handles_labels()[1] else "")
        ax.plot(x0, ev["close_c"], "o", color="#d62728", ms=4,
                label="C market-buy" if "C market-buy" not in ax.get_legend_handles_labels()[1] else "")

    step = max(1, len(dates) // 12)
    ax.set_xticks(range(0, len(dates), step))
    ax.set_xticklabels([dates[i] for i in range(0, len(dates), step)], rotation=45,
                       fontsize=8)
    ax.set_title(f"{sym} — rung mechanics audit (blue lines = Arm A rungs active "
                 f"deposit→expiry; A edge vs C: {rep['edge_pct']:+.2f}% shares/$)")
    ax.legend(loc="upper left")
    fig.tight_layout()
    out = OUT / f"{sym}.png"
    fig.savefig(out, dpi=110)
    plt.close(fig)
    return out


def table(sym: str, rep: dict) -> Path:
    lines = [f"# {sym} — per-deposit mechanics",
             "", "| Deposit | A rungs | A outcome | B outcome | C price |",
             "|---------|---------|-----------|-----------|--------:|"]
    for ev in rep["events"]:
        ra = ", ".join(f"{r:.2f}" for r in ev["rungs_a"]) or "none → mkt-buy"
        fa = "; ".join(f"{lv:.2f}→{fp:.2f} ({fd})" for fd, lv, fp in ev["fills_a"])
        if ev["expired_a"]:
            fa += ("; " if fa else "") + f"{ev['expired_a']} expired→mkt"
        fb = "; ".join(f"{fp:.2f}" for _, _, fp in ev["fills_b"])
        if ev["expired_b"]:
            fb += ("; " if fb else "") + f"{ev['expired_b']} expired"
        lines.append(f"| {ev['deposit']} | {ra} | {fa or '—'} | {fb or '—'} | "
                     f"{ev['close_c']:.2f} |")
    out = OUT / f"{sym}_table.md"
    out.write_text("\n".join(lines) + "\n")
    return out


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    cfg = yaml.safe_load(open(HERE / "targets.yaml")).get("levels", {})
    data = load_cached()
    if "SPY" not in data:
        raise SystemExit("no cached bars — run backtest_rungs.py first")
    calendar, deposit_days = build_deposit_days(data)

    reps = {s: replay_ticker(s, b, deposit_days, cfg) for s, b in data.items()}
    ranked = sorted(reps.items(), key=lambda kv: kv[1]["edge_pct"])
    hurt, median, helped = ranked[0], ranked[len(ranked) // 2], ranked[-1]

    print(f"ticker selection (A shares/$ edge vs C): "
          f"helped={helped[0]} {helped[1]['edge_pct']:+.2f}%  "
          f"median={median[0]} {median[1]['edge_pct']:+.2f}%  "
          f"hurt={hurt[0]} {hurt[1]['edge_pct']:+.2f}%")

    for sym, rep in (helped, median, hurt):
        png = chart(sym, data[sym], rep, deposit_days, calendar[0])
        tbl = table(sym, rep)
        n_fill = sum(len(e["fills_a"]) for e in rep["events"])
        n_exp = sum(e["expired_a"] for e in rep["events"])
        print(f"  {sym}: chart→{png.name} table→{tbl.name}  "
              f"(A: {n_fill} fills, {n_exp} expiries over {len(rep['events'])} deposits)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
