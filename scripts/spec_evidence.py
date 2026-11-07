"""Read-only evidence for the Issue #5 preprocessing and split spec.

Measures, on the full MachineLearningCSV data, the facts that each open
choice in docs/SPLIT_SPEC.md depends on, and sets them next to the
paper's Table 3 and Table 4 counts. It does not sample, split, clean or
train anything.

Outputs (new run folder; refuses to overwrite):
  table3_compare.csv   per paper class: full-data rows, 20% of them, the
                       same after removing exact duplicates, and the
                       paper's Table 3 / Table 4 counts
  nan_inf_rows.csv     rows with NaN or Inf in any feature, by original label
  table4_ratios.csv    paper Table 4 train share per class (paper numbers only)
  run_meta.json        versions, paths, runtime, script SHA-256

Usage:
  .venv/bin/python scripts/spec_evidence.py [--data-dir DIR] [--out-dir DIR]
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import platform
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATA_DIR = Path.home() / "Downloads" / "MachineLearningCVE"

# Paper Table 3 grouping (old label -> new label). Label strings are the exact
# raw strings, including U+FFFD in the Web Attack labels (docs/DATA_AUDIT.md).
WA = "Web Attack � "
TABLE3_MAP = {
    "BENIGN": "Normal",
    "Bot": "Bot",
    "FTP-Patator": "Brute Force", "SSH-Patator": "Brute Force",
    "DDoS": "DoS/DDoS", "DoS GoldenEye": "DoS/DDoS", "DoS Hulk": "DoS/DDoS",
    "DoS Slowhttptest": "DoS/DDoS", "DoS slowloris": "DoS/DDoS", "Heartbleed": "DoS/DDoS",
    "Infiltration": "Infiltration",
    "PortScan": "PortScan",
    WA + "Brute Force": "Web Attack", WA + "XSS": "Web Attack", WA + "Sql Injection": "Web Attack",
}

# paper-reported, transcribed from the IEEE Xplore table images on 2026-11-07
PAPER_T3 = {"Normal": 454396, "Bot": 367, "Brute Force": 2717, "DoS/DDoS": 76445,
            "Infiltration": 6, "PortScan": 31882, "Web Attack": 426}
PAPER_T4_TRAIN = {"Normal": 318087, "Bot": 265, "Brute Force": 1904, "DoS/DDoS": 53427,
                  "Infiltration": 5, "PortScan": 22324, "Web Attack": 292}
PAPER_T4_TEST = {"Normal": 136219, "Bot": 102, "Brute Force": 813, "DoS/DDoS": 23018,
                 "Infiltration": 1, "PortScan": 9558, "Web Attack": 134}


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def load(data_dir: Path) -> tuple[pd.DataFrame, pd.Series]:
    feats, labels = [], []
    for path in sorted(data_dir.glob("*.csv")):
        df = pd.read_csv(path, low_memory=False, encoding="utf-8")
        df.columns = [c.strip() for c in df.columns]
        # pandas renames the second "Fwd Header Length" to "Fwd Header Length.1"
        labels.append(df.pop("Label").astype(str))
        feats.append(df.astype("float64"))
    return pd.concat(feats, ignore_index=True), pd.concat(labels, ignore_index=True)


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--data-dir", type=Path, default=DEFAULT_DATA_DIR)
    p.add_argument("--out-dir", type=Path,
                   default=REPO_ROOT / "results" / "spec" / f"{dt.date.today().isoformat()}_evidence")
    a = p.parse_args()
    if a.out_dir.exists():
        print(f"Refusing to overwrite existing run folder: {a.out_dir}", file=sys.stderr)
        return 1
    t0 = time.time()

    X, y = load(a.data_dir)
    unknown = sorted(set(y) - set(TABLE3_MAP))
    if unknown:
        print(f"STOP: labels not in the Table 3 map: {unknown}", file=sys.stderr)
        return 2
    g = y.map(TABLE3_MAP)

    full = g.value_counts()
    dup = X.assign(_y=y.to_numpy()).duplicated()          # exact duplicates incl. label, keep first
    dedup = g[~dup].value_counts()
    vals = X.to_numpy()
    bad = np.isnan(vals).any(axis=1) | np.isinf(vals).any(axis=1)
    bad_after_dedup = bad & ~dup.to_numpy()

    rows = []
    for c in PAPER_T3:
        rows.append({
            "class": c,
            "full_rows": int(full.get(c, 0)),
            "full_x0.2": round(full.get(c, 0) * 0.2, 1),
            "dedup_rows": int(dedup.get(c, 0)),
            "dedup_x0.2": round(dedup.get(c, 0) * 0.2, 1),
            "paper_t3": PAPER_T3[c],
            "paper_t4_train_plus_test": PAPER_T4_TRAIN[c] + PAPER_T4_TEST[c],
            "paper_t3_over_full": round(PAPER_T3[c] / full.get(c, 1), 5),
        })
    t3 = pd.DataFrame(rows)
    tot = {"class": "TOTAL"}
    for col in ["full_rows", "full_x0.2", "dedup_rows", "dedup_x0.2", "paper_t3", "paper_t4_train_plus_test"]:
        tot[col] = round(t3[col].sum(), 1)
    tot["paper_t3_over_full"] = round(tot["paper_t3"] / tot["full_rows"], 5)
    t3 = pd.concat([t3, pd.DataFrame([tot])], ignore_index=True)

    a.out_dir.mkdir(parents=True, exist_ok=False)
    t3.to_csv(a.out_dir / "table3_compare.csv", index=False)

    ni = pd.DataFrame({"label": y, "class": g, "nan_or_inf": bad, "nan_or_inf_after_dedup": bad_after_dedup})
    ni.groupby(["label", "class"], as_index=False)[["nan_or_inf", "nan_or_inf_after_dedup"]].sum() \
        .assign(rows=ni.groupby(["label", "class"]).size().to_numpy()) \
        .to_csv(a.out_dir / "nan_inf_rows.csv", index=False)

    r = [{"class": c, "paper_train": PAPER_T4_TRAIN[c], "paper_test": PAPER_T4_TEST[c],
          "paper_train_share": round(PAPER_T4_TRAIN[c] / (PAPER_T4_TRAIN[c] + PAPER_T4_TEST[c]), 5)}
         for c in PAPER_T3]
    trn, tst = sum(PAPER_T4_TRAIN.values()), sum(PAPER_T4_TEST.values())
    r.append({"class": "TOTAL", "paper_train": trn, "paper_test": tst,
              "paper_train_share": round(trn / (trn + tst), 5)})
    pd.DataFrame(r).to_csv(a.out_dir / "table4_ratios.csv", index=False)

    import sklearn
    meta = {
        "script": "scripts/spec_evidence.py", "script_sha256": sha256_file(Path(__file__)),
        "args": {"data_dir": str(a.data_dir), "out_dir": str(a.out_dir)},
        "started": dt.datetime.now().astimezone().isoformat(timespec="seconds"),
        "runtime_seconds": round(time.time() - t0, 1),
        "python": sys.version, "platform": platform.platform(),
        "packages": {"pandas": pd.__version__, "numpy": np.__version__, "scikit-learn": sklearn.__version__},
        "randomness": "none (deterministic; no seed needed)",
        "paper_numbers": "Table 3 and Table 4 counts transcribed by hand from IEEE Xplore images, 2026-11-07",
        "total_rows": int(len(y)), "exact_duplicate_rows": int(dup.sum()),
        "rows_with_nan_or_inf": int(bad.sum()),
    }
    (a.out_dir / "run_meta.json").write_text(json.dumps(meta, indent=2))
    print(f"Wrote {a.out_dir} in {meta['runtime_seconds']} s")
    return 0


if __name__ == "__main__":
    sys.exit(main())
