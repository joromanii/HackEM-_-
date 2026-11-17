"""Read-only audit of the UNSW-NB15 training and testing files (Issue #4).

Reports, never fixes: file checksums, rows and columns, class counts
compared with the paper's Table 1, binary label balance, missing and
non-finite values, duplicate rows (within each file and shared between
train and test), the 11 paper features, and the `service` categories.

Usage:
    .venv/bin/python scripts/audit_unsw.py [--config configs/run.toml] [--out-dir DIR]
Exit code 2 if any class count differs from Table 1 (stop and report).
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import (DEFAULT_CONFIG, RunRecord, check_features, data_paths,  # noqa: E402
                    load_config, load_split, new_run_dir)

# paper-reported, Table 1 (Rajagopal et al. 2020)
TABLE1 = {
    "Normal": (56000, 37000), "Generic": (40000, 18871), "Exploits": (33393, 11132),
    "Fuzzers": (18184, 6062), "DoS": (12264, 4089), "Reconnaissance": (10491, 3496),
    "Analysis": (2000, 677), "Backdoor": (1746, 583), "Shellcode": (1133, 378), "Worms": (130, 44),
}


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    p.add_argument("--out-dir", type=Path, default=None)
    a = p.parse_args()
    cfg = load_config(a.config)
    tr_path, te_path = data_paths(cfg)
    out = new_run_dir(cfg, "unsw_audit", "audit", a.out_dir)
    rec = RunRecord("scripts/audit_unsw.py", cfg, a.config, out, [tr_path, te_path])

    tr, te = load_split(tr_path), load_split(te_path)
    lab, cat, idc = cfg["data"]["label_col"], cfg["data"]["category_col"], cfg["data"]["id_col"]
    feats = cfg["features"]["names"]

    # files
    files = pd.DataFrame([
        {"split": "train", "file": tr_path.name, "rows": len(tr), "columns": tr.shape[1],
         "sha256": rec.meta["inputs"][tr_path.name]["sha256"], "bytes": tr_path.stat().st_size},
        {"split": "test", "file": te_path.name, "rows": len(te), "columns": te.shape[1],
         "sha256": rec.meta["inputs"][te_path.name]["sha256"], "bytes": te_path.stat().st_size},
    ])
    files.to_csv(out / "files.csv", index=False)

    # columns
    cols = pd.DataFrame({"column": tr.columns, "dtype_train": [str(t) for t in tr.dtypes],
                         "in_test": [c in te.columns for c in tr.columns],
                         "paper_feature": [c in feats for c in tr.columns]})
    cols.to_csv(out / "columns.csv", index=False)
    check_features(tr, feats)
    check_features(te, feats)

    # class counts vs Table 1 (attack_cat values stripped of spaces)
    rows, differ = [], False
    trc = tr[cat].astype(str).str.strip().value_counts()
    tec = te[cat].astype(str).str.strip().value_counts()
    for c, (ptr, pte) in TABLE1.items():
        r = {"class": c, "train": int(trc.get(c, 0)), "paper_train": ptr,
             "test": int(tec.get(c, 0)), "paper_test": pte}
        r["match"] = r["train"] == ptr and r["test"] == pte
        differ |= not r["match"]
        rows.append(r)
    extra = (set(trc.index) | set(tec.index)) - set(TABLE1)
    for c in sorted(extra):
        rows.append({"class": c, "train": int(trc.get(c, 0)), "paper_train": 0,
                     "test": int(tec.get(c, 0)), "paper_test": 0, "match": False})
        differ = True
    cc = pd.DataFrame(rows)
    tot = {"class": "TOTAL", "train": int(cc["train"].sum()), "paper_train": 175341,
           "test": int(cc["test"].sum()), "paper_test": 82332}
    tot["match"] = tot["train"] == 175341 and tot["test"] == 82332
    pd.concat([cc, pd.DataFrame([tot])]).to_csv(out / "class_counts_vs_table1.csv", index=False)

    # binary label, and its agreement with attack_cat
    bl = []
    for name, df in [("train", tr), ("test", te)]:
        normal_cat = df[cat].astype(str).str.strip() == "Normal"
        bl.append({"split": name, "label_0_normal": int((df[lab] == 0).sum()),
                   "label_1_attack": int((df[lab] == 1).sum()),
                   "attack_share": round(float((df[lab] == 1).mean()), 5),
                   "label_disagrees_with_attack_cat": int(((df[lab] == 0) != normal_cat).sum())})
    pd.DataFrame(bl).to_csv(out / "binary_balance.csv", index=False)

    # missing / non-finite values
    mv = []
    for name, df in [("train", tr), ("test", te)]:
        for c in df.columns:
            col = df[c]
            num = pd.api.types.is_numeric_dtype(col)
            vals = col.to_numpy(dtype="float64") if num else None
            mv.append({"split": name, "column": c, "nan": int(col.isna().sum()),
                       "pos_inf": int(np.isposinf(vals).sum()) if num else 0,
                       "neg_inf": int(np.isneginf(vals).sum()) if num else 0,
                       "negative": int((vals < 0).sum()) if num else 0,
                       "dash_placeholder": 0 if num else int((col.astype(str).str.strip() == "-").sum())})
    pd.DataFrame(mv).to_csv(out / "missing_values.csv", index=False)

    # duplicates (all columns except id)
    keep = [c for c in tr.columns if c != idc]
    h_tr = pd.util.hash_pandas_object(tr[keep], index=False).to_numpy()
    h_te = pd.util.hash_pandas_object(te[keep], index=False).to_numpy()
    fkeep = feats
    f_tr = pd.util.hash_pandas_object(tr[fkeep], index=False).to_numpy()
    f_te = pd.util.hash_pandas_object(te[fkeep], index=False).to_numpy()
    tr_set, f_tr_set = set(h_tr), set(f_tr)
    dups = pd.DataFrame([
        {"check": "train exact duplicates (extra copies, all columns but id)", "rows": int(len(h_tr) - len(set(h_tr)))},
        {"check": "test exact duplicates (extra copies, all columns but id)", "rows": int(len(h_te) - len(set(h_te)))},
        {"check": "test rows identical to some train row (all columns but id)", "rows": int(sum(h in tr_set for h in h_te))},
        {"check": "train duplicates on the 11 features only", "rows": int(len(f_tr) - len(set(f_tr)))},
        {"check": "test rows whose 11 features appear in train", "rows": int(sum(h in f_tr_set for h in f_te))},
    ])
    dups.to_csv(out / "duplicates.csv", index=False)

    # 11 features: summary
    desc = []
    for f in feats:
        s_tr, s_te = tr[f], te[f]
        if pd.api.types.is_numeric_dtype(s_tr):
            desc.append({"feature": f, "type": "numeric", "train_min": s_tr.min(), "train_median": s_tr.median(),
                         "train_max": s_tr.max(), "test_min": s_te.min(), "test_max": s_te.max(),
                         "distinct_train": s_tr.nunique()})
        else:
            desc.append({"feature": f, "type": "categorical", "distinct_train": s_tr.nunique(),
                         "distinct_test": s_te.nunique(),
                         "test_values_not_in_train": len(set(s_te.unique()) - set(s_tr.unique()))})
    pd.DataFrame(desc).to_csv(out / "feature_summary.csv", index=False)

    for f in cfg["features"]["categorical"]:
        vc = pd.concat([tr[f].value_counts().rename("train"), te[f].value_counts().rename("test")], axis=1)
        vc.fillna(0).astype(int).rename_axis(f).reset_index().to_csv(out / f"values_{f}.csv", index=False)

    rec.save(train_rows=len(tr), test_rows=len(te), class_counts_match_table1=not differ)
    print(f"Wrote {out} in {rec.meta['runtime_seconds']} s")
    if differ:
        print("STOP: class counts differ from paper Table 1. See class_counts_vs_table1.csv", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
