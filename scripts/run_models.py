"""Train and score the baseline models or the stacking ensemble on UNSW-NB15.

  --task baseline : majority class, then RF, KNN and LR alone (Issue #6)
  --task stacking : RF + KNN + LR -> SVM stacking ensemble (Issue #8)

Binary target (attack = 1 positive, D14). Fitted on the training file only;
scored once on the full test file, and on the test rows that are not exact
copies of a training row (D6 sensitivity check).

Writes a new run folder with metrics.csv, confusion_matrices.csv,
run_meta.json. Per-row predictions are not saved.

Usage:
  .venv/bin/python scripts/run_models.py --task baseline
  .venv/bin/python scripts/run_models.py --task stacking [--seed N] [--sample-n N]
  .venv/bin/python scripts/run_models.py --task stacking --target multiclass
"""
from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.dummy import DummyClassifier
from sklearn.metrics import classification_report, confusion_matrix

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import (DEFAULT_CONFIG, RunRecord, binary_metrics, check_features,  # noqa: E402
                    data_paths, load_config, load_train_test, new_run_dir)
from models import base_models, single_pipeline, stacking_pipeline  # noqa: E402


def score_of(model, X) -> np.ndarray | None:
    if hasattr(model, "decision_function"):
        try:
            return model.decision_function(X)
        except Exception:
            pass
    if hasattr(model, "predict_proba"):
        return model.predict_proba(X)[:, 1]
    return None


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--task", choices=["baseline", "stacking"], required=True)
    p.add_argument("--target", choices=["binary", "multiclass"], default="binary")
    p.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    p.add_argument("--seed", type=int, default=None, help="overrides config seed")
    p.add_argument("--sample-n", type=int, default=None,
                   help="train on a stratified sample of N training rows (timing/dry runs only)")
    p.add_argument("--tag", default=None, help="extra label for the run folder name (e.g. a config variant)")
    p.add_argument("--out-dir", type=Path, default=None)
    a = p.parse_args()

    cfg = load_config(a.config)
    seed = a.seed if a.seed is not None else cfg["seed"]
    name = f"{a.task}_{a.target}_seed{seed}" + (f"_sample{a.sample_n}" if a.sample_n else "") + (f"_{a.tag}" if a.tag else "")
    out = new_run_dir(cfg, "runs", name, a.out_dir)
    tr_path, te_path = data_paths(cfg)
    rec = RunRecord("scripts/run_models.py", cfg, a.config, out, [tr_path, te_path])
    rec.meta["args"] = {"task": a.task, "target": a.target, "seed": seed, "sample_n": a.sample_n, "tag": a.tag}

    tr, te = load_train_test(cfg)
    feats = cfg["features"]["names"]
    check_features(tr, feats)
    check_features(te, feats)
    ycol = cfg["data"]["label_col"] if a.target == "binary" else cfg["data"]["category_col"]
    if a.target == "multiclass":
        tr[ycol] = tr[ycol].astype(str).str.strip()
        te[ycol] = te[ycol].astype(str).str.strip()

    if a.sample_n:
        tr = tr.groupby(ycol, group_keys=False).apply(
            lambda g: g.sample(frac=a.sample_n / len(tr), random_state=seed))
    X_tr, y_tr = tr[feats], tr[ycol].to_numpy()
    X_te, y_te = te[feats], te[ycol].to_numpy()

    # D6: test rows that are exact copies (all columns but id) of some training row
    keep = [c for c in te.columns if c != cfg["data"]["id_col"]]
    tr_full = load_train_test(cfg)[0]
    tr_hash = set(pd.util.hash_pandas_object(tr_full[keep], index=False).to_numpy())
    te_hash = pd.util.hash_pandas_object(te[keep], index=False).to_numpy()
    unseen = np.array([h not in tr_hash for h in te_hash])

    if a.task == "baseline":
        models = [("majority", single_pipeline(cfg, DummyClassifier(strategy="most_frequent")))]
        models += [(n, single_pipeline(cfg, m)) for n, m in base_models(cfg, seed)]
    else:
        models = [("stacking", stacking_pipeline(cfg, seed))]

    metric_rows, cm_rows, reports = [], [], {}
    for mname, model in models:
        t = time.time()
        model.fit(X_tr, y_tr)
        fit_s = time.time() - t
        t = time.time()
        pred = model.predict(X_te)
        pred_s = time.time() - t
        print(f"{mname}: fit {fit_s:.1f} s, predict {pred_s:.1f} s", flush=True)
        if a.target == "binary":
            score = score_of(model, X_te)
            for subset, mask in [("test_all", np.ones(len(y_te), bool)), ("test_unseen", unseen)]:
                mtr = binary_metrics(y_te[mask], pred[mask], None if score is None else score[mask])
                metric_rows.append({"model": mname, "subset": subset, "rows": int(mask.sum()),
                                    **{k: (round(v, 6) if isinstance(v, float) else v) for k, v in mtr.items()},
                                    "fit_seconds": round(fit_s, 1), "predict_seconds": round(pred_s, 1)})
        else:
            labels = sorted(set(y_tr) | set(y_te))
            cm = confusion_matrix(y_te, pred, labels=labels)
            cm_df = pd.DataFrame(cm, index=labels, columns=labels)
            cm_df.index.name = "true\\pred"
            cm_df.to_csv(out / f"confusion_{mname}.csv")
            rep = classification_report(y_te, pred, labels=labels, output_dict=True, zero_division=0)
            reports[mname] = rep
            pd.DataFrame(rep).T.round(6).to_csv(out / f"per_class_{mname}.csv")
            metric_rows.append({"model": mname, "subset": "test_all", "rows": len(y_te),
                                "accuracy": round(float((pred == y_te).mean()), 6),
                                "macro_f1": round(rep["macro avg"]["f1-score"], 6),
                                "weighted_f1": round(rep["weighted avg"]["f1-score"], 6),
                                "fit_seconds": round(fit_s, 1), "predict_seconds": round(pred_s, 1)})

    pd.DataFrame(metric_rows).to_csv(out / "metrics.csv", index=False)
    if a.target == "binary":
        for r in metric_rows:
            cm_rows.append({k: r[k] for k in ["model", "subset", "rows", "TP", "TN", "FN", "FP"]})
        pd.DataFrame(cm_rows).to_csv(out / "confusion_matrices.csv", index=False)

    rec.save(train_rows=len(X_tr), test_rows=len(X_te), test_unseen_rows=int(unseen.sum()),
             positive_class="attack (label 1)" if a.target == "binary" else None,
             far_formula="FP / (FP + TN)" if a.target == "binary" else None,
             auc_score="SVM decision_function (stacking); decision_function or predict_proba[:,1] (baseline)")
    print(pd.DataFrame(metric_rows).to_string(index=False))
    print(f"Wrote {out} in {rec.meta['runtime_seconds']} s")
    return 0


if __name__ == "__main__":
    sys.exit(main())
