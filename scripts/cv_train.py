"""10-fold cross-validation of the stacking ensemble on the training file only.

Compares with the paper's Table 5 (mean training accuracy 0.9285, recall
0.9115, precision 0.9497). The test file is not read.

Each fold fits the whole pipeline (preprocessing + stacking) on 9/10 of the
training rows and scores the held-out tenth. Attack = positive (D14).

Usage:
  .venv/bin/python scripts/cv_train.py [--seed N] [--folds 10]
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd
from sklearn.model_selection import StratifiedKFold, cross_validate

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import DEFAULT_CONFIG, RunRecord, check_features, data_paths, load_config, load_split, new_run_dir  # noqa: E402
from models import stacking_pipeline  # noqa: E402

PAPER_TABLE5 = {"accuracy": 0.9285, "recall": 0.9115, "precision": 0.9497}  # paper-reported means


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    p.add_argument("--seed", type=int, default=None)
    p.add_argument("--folds", type=int, default=10)
    p.add_argument("--out-dir", type=Path, default=None)
    a = p.parse_args()
    cfg = load_config(a.config)
    seed = a.seed if a.seed is not None else cfg["seed"]
    out = new_run_dir(cfg, "runs", f"cv_train_stacking_seed{seed}", a.out_dir)
    tr_path, _ = data_paths(cfg)
    rec = RunRecord("scripts/cv_train.py", cfg, a.config, out, [tr_path])
    rec.meta["args"] = {"seed": seed, "folds": a.folds}

    tr = load_split(tr_path)
    feats = cfg["features"]["names"]
    check_features(tr, feats)
    X, y = tr[feats], tr[cfg["data"]["label_col"]].to_numpy()
    cv = StratifiedKFold(n_splits=a.folds, shuffle=True, random_state=seed)
    res = cross_validate(stacking_pipeline(cfg, seed), X, y, cv=cv,
                         scoring=["accuracy", "recall", "precision", "f1"], return_train_score=False)
    folds = pd.DataFrame({"fold": range(1, a.folds + 1),
                          "accuracy": res["test_accuracy"], "recall": res["test_recall"],
                          "precision": res["test_precision"], "f1": res["test_f1"],
                          "fit_seconds": res["fit_time"]}).round(6)
    folds.to_csv(out / "folds.csv", index=False)
    summ = pd.DataFrame([{"metric": m, "ours_mean": round(float(folds[m].mean()), 6),
                          "ours_sd": round(float(folds[m].std()), 6), "paper_table5": PAPER_TABLE5[m],
                          "difference": round(float(folds[m].mean()) - PAPER_TABLE5[m], 6)}
                         for m in PAPER_TABLE5])
    summ.to_csv(out / "summary_vs_table5.csv", index=False)
    rec.save(train_rows=len(y))
    print(summ.to_string(index=False))
    print(f"Wrote {out} in {rec.meta['runtime_seconds']} s")
    return 0


if __name__ == "__main__":
    sys.exit(main())
