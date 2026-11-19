"""Automated check that no test row is ever used for fitting (Issue #8, story M3-1).

Runs the real `scripts/run_models.py` code path (baseline and stacking) on a
stratified training sample, while recording every DataFrame passed to
`Pipeline.fit`. Then checks, by hashing the 11 feature values of each row:

  1. every fitted row comes from the training file;
  2. no fitted row is a "test-only" row (feature values that appear in the
     test file but nowhere in the training file);
  3. the number of fitted rows equals the training rows the script reports;
  4. negative control: the same test flags rows deliberately taken from the
     test file, so a pass is meaningful.

It also text-checks that `scripts/cv_train.py` references only the training
file (a static check: the script is not run).

Limits: only top-level `Pipeline.fit` calls on DataFrames can be traced to
rows; a test row whose 11 feature values also occur in training can't be told
apart from a training row (about a quarter of test rows); only the 5,000-row
binary path is executed.

Existing scripts are imported, not edited, so the code checksums recorded by
earlier runs stay valid. Writes a new folder results/checks/<date>_no_leakage/
with checks.csv and run_meta.json; exits 1 if any check fails.

Usage:
  .venv/bin/python scripts/check_no_leakage.py [--sample-n 5000]
"""
from __future__ import annotations

import argparse
import ast
import json
import sys
import tempfile
from pathlib import Path

import pandas as pd
from sklearn.pipeline import Pipeline

sys.path.insert(0, str(Path(__file__).resolve().parent))
import run_models  # noqa: E402
from common import (DEFAULT_CONFIG, REPO_ROOT, RunRecord, data_paths, load_config,  # noqa: E402
                    load_train_test, new_run_dir)


def row_hashes(df: pd.DataFrame) -> set:
    return set(pd.util.hash_pandas_object(df, index=False).to_numpy())


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--sample-n", type=int, default=5000)
    a = p.parse_args()
    cfg = load_config(DEFAULT_CONFIG)
    out = new_run_dir(cfg, "checks", "no_leakage")
    rec = RunRecord("scripts/check_no_leakage.py", cfg, DEFAULT_CONFIG, out, list(data_paths(cfg)))

    feats = cfg["features"]["names"]
    tr, te = load_train_test(cfg)
    train_h, test_h = row_hashes(tr[feats]), row_hashes(te[feats])
    test_only = test_h - train_h

    fitted: list[pd.DataFrame] = []
    other_fits: list = []
    original_fit = Pipeline.fit

    def recording_fit(self, X, y=None, **kw):
        # top-level pipelines receive the raw feature DataFrame; inner (numpy)
        # fits are counted but can't be traced back to rows
        if isinstance(X, pd.DataFrame):
            fitted.append(X.copy())
        else:
            other_fits.append(getattr(X, "shape", None))
        return original_fit(self, X, y, **kw)

    rows = []
    Pipeline.fit = recording_fit
    try:
        with tempfile.TemporaryDirectory() as tmp:
            for task in ["baseline", "stacking"]:
                fitted.clear()
                sys.argv = ["run_models.py", "--task", task, "--sample-n", str(a.sample_n),
                            "--out-dir", str(Path(tmp) / task)]
                run_models.main()
                fit_rows = pd.concat(fitted) if fitted else pd.DataFrame(columns=feats)
                h = pd.util.hash_pandas_object(fit_rows[feats], index=False).to_numpy() if len(fit_rows) else []
                n_not_train = int(sum(x not in train_h for x in h))
                n_test_only = int(sum(x in test_only for x in h))
                per_fit = sorted({len(f) for f in fitted})
                reported = json.loads((Path(tmp) / task / "run_meta.json").read_text())["train_rows"]
                rows += [
                    {"task": task, "check": "fit calls recorded", "value": len(fitted), "pass": len(fitted) > 0},
                    {"task": task, "check": "rows per fit call vs training rows the script reports",
                     "value": f"{'|'.join(map(str, per_fit))} vs {reported}",
                     "pass": per_fit == [reported]},
                    {"task": task, "check": "fitted rows not found in training file", "value": n_not_train,
                     "pass": n_not_train == 0},
                    {"task": task, "check": "fitted rows that exist only in test file", "value": n_test_only,
                     "pass": n_test_only == 0},
                ]
    finally:
        Pipeline.fit = original_fit

    # negative control, through the same recording hook: deliberately fit a
    # pipeline on 1,000 test rows and confirm the check flags them
    from models import single_pipeline
    from sklearn.dummy import DummyClassifier
    Pipeline.fit = recording_fit
    try:
        fitted.clear()
        single_pipeline(cfg, DummyClassifier()).fit(te[feats].head(1000), te[cfg["data"]["label_col"]].head(1000))
    finally:
        Pipeline.fit = original_fit
    ctrl = pd.util.hash_pandas_object(pd.concat(fitted)[feats], index=False).to_numpy()
    caught = int(sum(x in test_only for x in ctrl))
    rows.append({"task": "control", "check": "deliberate fit on 1000 test rows is flagged (through the hook)",
                 "value": f"{caught} of 1000 flagged; the rest duplicate a training row and are invisible",
                 "pass": caught > 0})

    cv_src = (REPO_ROOT / "scripts" / "cv_train.py").read_text()
    reads_test = "te_path" in cv_src.replace("_, te_path", "") or "load_train_test" in cv_src
    tree_ok = "test_file" not in cv_src
    rows.append({"task": "cv_train", "check": "cv_train.py source references only the training file (text check, not run)",
                 "value": "loads train only" if (not reads_test and tree_ok) else "test file referenced",
                 "pass": (not reads_test) and tree_ok})
    ast.parse(cv_src)  # make sure the file we inspected is valid Python

    res = pd.DataFrame(rows)
    res.to_csv(out / "checks.csv", index=False)
    ok = bool(res["pass"].all())
    rec.save(sample_n=a.sample_n, train_rows=len(tr), test_rows=len(te),
             test_only_feature_rows=len(test_only), all_checks_pass=ok)
    print(res.to_string(index=False))
    print(f"{'ALL CHECKS PASS' if ok else 'CHECK FAILED'} - wrote {out}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
