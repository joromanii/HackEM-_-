"""One command from raw data to the Table 4 comparison (Issue #8, readiness item 6).

Runs, in order, into one new folder results/reproduce/<date>_<time>/:
  1. audit/       scripts/audit_unsw.py   (stops if counts differ from Table 1)
  2. baseline/    scripts/run_models.py --task baseline
  3. stacking/    scripts/run_models.py --task stacking   (the headline)
  4. comparison/  scripts/compare.py      (paper / ours / difference)
Then checks the new headline metrics against the saved reference run and
writes summary.md. Exit code 0 only if every step succeeds and the metrics
match the reference exactly.

Takes about 2.5 minutes on a 10-CPU laptop (measured: see run_meta.json in the output folder). Needs the data in the folder set by configs/run.toml
(see docs/wiki/Runbook.md).

Usage:
  .venv/bin/python scripts/reproduce.py
"""
from __future__ import annotations

import argparse
import datetime as dt
import subprocess
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import DEFAULT_CONFIG, REPO_ROOT, RunRecord, data_paths, load_config  # noqa: E402

REFERENCE = REPO_ROOT / "results" / "runs" / "2026-11-15_stacking_binary_seed42" / "metrics.csv"
BASELINE_REF = REPO_ROOT / "results" / "runs" / "2026-11-15_baseline_binary_seed42" / "metrics.csv"
METRIC_COLS = ["model", "subset", "rows", "TP", "TN", "FN", "FP",
               "accuracy", "precision", "recall", "f1", "far", "auc"]
BASE_COLS = METRIC_COLS


def step(name: str, args: list[str], log) -> int:
    print(f"\n== {name}: {' '.join(args)}", flush=True)
    proc = subprocess.run([sys.executable, *args], cwd=REPO_ROOT, capture_output=True, text=True)
    log.write(f"== {name} (exit {proc.returncode})\n{proc.stdout}\n")
    tail = [line for line in proc.stdout.splitlines() if line.startswith(("Wrote", "STOP", "stacking", "rf ", "knn", "lr "))]
    print("\n".join(tail[-4:]) or "(no output)")
    if proc.returncode != 0:
        print(proc.stderr[-2000:], file=sys.stderr)
    return proc.returncode


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--reference", type=Path, default=REFERENCE,
                   help="metrics.csv of the saved headline run to compare against")
    a = p.parse_args()
    stamp = dt.datetime.now().strftime("%Y-%m-%d_%H%M%S")
    out = REPO_ROOT / "results" / "reproduce" / stamp
    out.mkdir(parents=True, exist_ok=False)
    cfg = load_config(DEFAULT_CONFIG)
    rec = RunRecord("scripts/reproduce.py", cfg, DEFAULT_CONFIG, out, list(data_paths(cfg)))
    rel = lambda d: str((out / d).relative_to(REPO_ROOT))  # noqa: E731

    with (out / "log.txt").open("w") as log:
        steps = [
            ("audit", ["scripts/audit_unsw.py", "--out-dir", rel("audit")]),
            ("baseline", ["scripts/run_models.py", "--task", "baseline", "--out-dir", rel("baseline")]),
            ("stacking", ["scripts/run_models.py", "--task", "stacking", "--out-dir", rel("stacking")]),
            ("comparison", ["scripts/compare.py", "--main", rel("stacking"), "--baseline", rel("baseline"),
                            "--out-dir", rel("comparison")]),
        ]
        codes = {}
        for name, args in steps:
            codes[name] = step(name, args, log)
            if codes[name] != 0:
                break

    lines = [f"# Reproduction run {stamp}", "", "| Step | Exit code |", "|---|---:|"]
    lines += [f"| {k} | {v} |" for k, v in codes.items()]
    ok = len(codes) == len(steps) and all(v == 0 for v in codes.values())
    match = base_match = False
    if ok:
        new = pd.read_csv(out / "stacking" / "metrics.csv")[METRIC_COLS]
        ref = pd.read_csv(a.reference)[METRIC_COLS]
        match = new.round(6).equals(ref.round(6))
        bnew = pd.read_csv(out / "baseline" / "metrics.csv")[BASE_COLS].round(6)
        bref = pd.read_csv(BASELINE_REF)[BASE_COLS].round(6)
        base_match = bnew.equals(bref)
        comp = (out / "comparison" / "comparison.md").read_text()
        lines += ["", f"**Headline metrics identical to the saved reference run "
                      f"(`{a.reference.relative_to(REPO_ROOT)}`): {'YES' if match else 'NO'}**",
                  f"Baseline metrics identical to `{BASELINE_REF.relative_to(REPO_ROOT)}`: {'YES' if base_match else 'NO'}", "",
                  comp.split("\n\n| Count")[0].split("\n", 2)[2]]
        if not match:
            diff = new.compare(ref, result_names=("this run", "reference"))
            lines += ["", "Differences:", "", "```", diff.to_string(), "```"]
    rec.save(steps=codes, headline_matches_reference=bool(match),
             baseline_matches_reference=bool(ok and base_match),
             reference=str(a.reference.relative_to(REPO_ROOT)))
    lines += ["", f"Total runtime: {rec.meta['runtime_seconds']} s (`run_meta.json`)."]
    (out / "summary.md").write_text("\n".join(lines) + "\n")
    print(f"\nSummary: {out.relative_to(REPO_ROOT)}/summary.md")
    print("RESULT:", "REPRODUCED (identical to the saved headline run)" if ok and match
          else "DID NOT MATCH - see summary.md" if ok else "A STEP FAILED - see log.txt")
    return 0 if ok and match else 1


if __name__ == "__main__":
    sys.exit(main())
