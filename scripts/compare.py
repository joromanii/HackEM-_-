"""Build the paper / ours / difference table for Table 4 from saved run folders.

Reads only results/ files (never retrains). Writes a new folder with
comparison.csv (headline: config seed run), seeds.csv (seed variation),
variants.csv (preprocessing sensitivity), baseline.csv, and comparison.md.

Usage:
  .venv/bin/python scripts/compare.py --main RUN_DIR [--seeds RUN_DIR ...]
        [--variants RUN_DIR ...] [--baseline RUN_DIR] [--cv RUN_DIR]
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import DEFAULT_CONFIG, REPO_ROOT, git_info, load_config, new_run_dir, package_versions, sha256_file  # noqa: E402

# paper-reported, Table 4 (binary, UNSW-NB15 test set)
PAPER = {"accuracy": 0.94, "precision": 0.96, "recall": 0.93, "f1": 0.95, "auc": 0.99, "far": 0.052}
PAPER_COUNTS = {"TP": 42535, "TN": 35365, "FN": 2797, "FP": 1635}
METRICS = list(PAPER)


def read_metrics(run: Path, subset: str = "test_all") -> pd.DataFrame:
    m = pd.read_csv(run / "metrics.csv")
    return m[m["subset"] == subset]


def rel(p: Path) -> str:
    p = p.resolve()
    return str(p.relative_to(REPO_ROOT)) if p.is_relative_to(REPO_ROOT) else str(p)


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--main", type=Path, required=True)
    p.add_argument("--seeds", type=Path, nargs="*", default=[])
    p.add_argument("--variants", type=Path, nargs="*", default=[])
    p.add_argument("--baseline", type=Path, default=None)
    p.add_argument("--cv", type=Path, default=None)
    p.add_argument("--out-dir", type=Path, default=None)
    a = p.parse_args()
    cfg = load_config(DEFAULT_CONFIG)
    out = new_run_dir(cfg, "comparison", "table4", a.out_dir)

    main_all = read_metrics(a.main).iloc[0]
    main_unseen = read_metrics(a.main, "test_unseen").iloc[0]
    rows = []
    for m in METRICS:
        ours = float(main_all[m])
        rows.append({"metric": m, "paper_table4": PAPER[m], "ours": round(ours, 4),
                     "difference": round(ours - PAPER[m], 4),
                     "ours_test_unseen": round(float(main_unseen[m]), 4)})
    comp = pd.DataFrame(rows)
    comp.to_csv(out / "comparison.csv", index=False)
    counts = pd.DataFrame([{"count": k, "paper_table4": v, "ours": int(main_all[k]),
                            "difference": int(main_all[k]) - v} for k, v in PAPER_COUNTS.items()])
    counts.to_csv(out / "counts.csv", index=False)

    seed_rows = []
    for run in [a.main, *a.seeds]:
        r = read_metrics(run).iloc[0]
        seed = json.loads((run / "run_meta.json").read_text())["args"]["seed"]
        seed_rows.append({"seed": seed, **{m: round(float(r[m]), 6) for m in METRICS}, "run": rel(run)})
    seeds = pd.DataFrame(seed_rows).sort_values("seed")
    seeds.to_csv(out / "seeds.csv", index=False)
    spread = seeds[METRICS].agg(["mean", "std", "min", "max"]).round(6)
    spread.to_csv(out / "seed_spread.csv")

    var_rows = []
    for run in a.variants:
        r = read_metrics(run).iloc[0]
        meta = json.loads((run / "run_meta.json").read_text())
        var_rows.append({"variant": meta["args"].get("tag"), **{m: round(float(r[m]), 6) for m in METRICS},
                         "run": rel(run)})
    if var_rows:
        pd.DataFrame(var_rows).to_csv(out / "variants.csv", index=False)

    base = None
    if a.baseline:
        base = read_metrics(a.baseline)[["model", *METRICS]].round(6)
        base.to_csv(out / "baseline.csv", index=False)

    cv = None
    if a.cv:
        cv = pd.read_csv(a.cv / "summary_vs_table5.csv")

    md = ["# Table 4 comparison (binary, UNSW-NB15 test set, 82,332 records)", "",
          f"Headline run: `{rel(a.main)}` (seed {seed_rows[0]['seed']}). Attack = positive (D14); "
          "FAR = FP/(FP+TN) (D15); AUC from the SVM decision function (D17). "
          "Paper values `paper-reported` (Table 4); ours `measured` from the run's `metrics.csv`.", "",
          "| Metric | Paper | Ours | Difference | Ours, test rows not copied from train |",
          "|---|---:|---:|---:|---:|"]
    for r in rows:
        md.append(f"| {r['metric']} | {r['paper_table4']} | {r['ours']:.4f} | {r['difference']:+.4f} | {r['ours_test_unseen']:.4f} |")
    md += ["", "| Count | Paper | Ours | Difference |", "|---|---:|---:|---:|"]
    md += [f"| {k} | {v:,} | {int(main_all[k]):,} | {int(main_all[k]) - v:+,} |" for k, v in PAPER_COUNTS.items()]
    md += ["", f"Seed variation over {len(seeds)} runs (seeds {', '.join(str(s) for s in seeds['seed'])}):", "",
           "| Metric | Mean | SD | Min | Max |", "|---|---:|---:|---:|---:|"]
    md += [f"| {m} | {spread.loc['mean', m]:.4f} | {spread.loc['std', m]:.4f} | {spread.loc['min', m]:.4f} | {spread.loc['max', m]:.4f} |" for m in METRICS]
    if var_rows:
        md += ["", "Preprocessing sensitivity (seed 42; sensitivity checks only, not used to choose settings):", "", "| Variant | " + " | ".join(METRICS) + " |",
               "|---|" + "---:|" * len(METRICS)]
        md += [f"| {v['variant']} | " + " | ".join(f"{v[m]:.4f}" for m in METRICS) + " |" for v in var_rows]
    if base is not None:
        md += ["", "Baseline (same split and features):", "", "| Model | " + " | ".join(METRICS) + " |",
               "|---|" + "---:|" * len(METRICS)]
        md += [f"| {r['model']} | " + " | ".join(f"{r[m]:.4f}" for m in METRICS) + " |" for _, r in base.iterrows()]
    if cv is not None:
        md += ["", "10-fold CV on the training file vs paper Table 5:", "", "| Metric | Ours (mean ± SD) | Paper | Difference |",
               "|---|---:|---:|---:|"]
        md += [f"| {r['metric']} | {r['ours_mean']:.4f} ± {r['ours_sd']:.4f} | {r['paper_table5']} | {r['difference']:+.4f} |" for _, r in cv.iterrows()]
    (out / "comparison.md").write_text("\n".join(md) + "\n")

    inputs = [a.main, *a.seeds, *a.variants] + ([a.baseline] if a.baseline else []) + ([a.cv] if a.cv else [])
    meta = {"script": "scripts/compare.py", "script_sha256": sha256_file(Path(__file__)),
            "inputs": {rel(r): sha256_file(r / ("metrics.csv" if (r / "metrics.csv").exists() else "summary_vs_table5.csv"))
                       for r in inputs},
            "paper_values": {"table4": PAPER, "table4_counts": PAPER_COUNTS},
            "python": sys.version.split()[0], "packages": package_versions(), "git": git_info(),
            "note": "Reads saved results only; no training. Variants are sensitivity checks, not used to pick settings."}
    (out / "run_meta.json").write_text(json.dumps(meta, indent=2))
    print("\n".join(md))
    print(f"Wrote {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
