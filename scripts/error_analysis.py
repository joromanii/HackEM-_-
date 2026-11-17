"""Where do the stacking model's false alarms come from? (gap analysis, Issue #9)

Fits the headline stacking pipeline (config seed) on the training file,
predicts the test file, and breaks down the normal test records that are
flagged as attack (false positives) by `service` and by `sttl`. Also
compares how normal traffic is distributed in the training vs test files.

Outputs: fp_by_service.csv, fp_by_sttl.csv, normal_shift_service.csv,
normal_shift_sttl.csv, run_meta.json. No per-row predictions are saved.

Usage:
  .venv/bin/python scripts/error_analysis.py
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import DEFAULT_CONFIG, RunRecord, data_paths, load_config, load_train_test, new_run_dir  # noqa: E402
from models import stacking_pipeline  # noqa: E402


def breakdown(df: pd.DataFrame, col: str) -> pd.DataFrame:
    g = df.groupby(col).agg(normal_test_rows=("fp", "size"), false_positives=("fp", "sum")).reset_index()
    g["fp_rate"] = (g["false_positives"] / g["normal_test_rows"]).round(4)
    g["share_of_all_fp"] = (g["false_positives"] / g["false_positives"].sum()).round(4)
    return g.sort_values("false_positives", ascending=False)


def shift(tr: pd.DataFrame, te: pd.DataFrame, col: str) -> pd.DataFrame:
    a = tr[col].value_counts(normalize=True).rename("normal_train_share")
    b = te[col].value_counts(normalize=True).rename("normal_test_share")
    s = pd.concat([a, b], axis=1).fillna(0).round(4)
    s["difference"] = (s["normal_test_share"] - s["normal_train_share"]).round(4)
    return s.rename_axis(col).reset_index().sort_values("normal_test_share", ascending=False)


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    p.add_argument("--out-dir", type=Path, default=None)
    a = p.parse_args()
    cfg = load_config(a.config)
    seed = cfg["seed"]
    out = new_run_dir(cfg, "runs", f"error_analysis_stacking_seed{seed}", a.out_dir)
    rec = RunRecord("scripts/error_analysis.py", cfg, a.config, out, list(data_paths(cfg)))

    tr, te = load_train_test(cfg)
    feats, y = cfg["features"]["names"], cfg["data"]["label_col"]
    model = stacking_pipeline(cfg, seed).fit(tr[feats], tr[y].to_numpy())
    pred = model.predict(te[feats])

    normal_te = te[te[y] == 0].copy()
    normal_te["fp"] = (pred[te[y].to_numpy() == 0] == 1).astype(int)
    breakdown(normal_te, "service").to_csv(out / "fp_by_service.csv", index=False)
    breakdown(normal_te, "sttl").to_csv(out / "fp_by_sttl.csv", index=False)
    normal_tr = tr[tr[y] == 0]
    shift(normal_tr, normal_te, "service").to_csv(out / "normal_shift_service.csv", index=False)
    shift(normal_tr, normal_te, "sttl").to_csv(out / "normal_shift_sttl.csv", index=False)

    rec.save(normal_test_rows=len(normal_te), false_positives=int(normal_te["fp"].sum()))
    print(f"false positives: {int(normal_te['fp'].sum())} of {len(normal_te)} normal test rows")
    print(f"Wrote {out} in {rec.meta['runtime_seconds']} s")
    return 0


if __name__ == "__main__":
    sys.exit(main())
