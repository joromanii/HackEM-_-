"""How `sttl` (source time-to-live) splits between normal and attack records
in the training and testing files (gap analysis, Issue #9). Read-only.

Output: sttl_by_split_label.csv (rows per split, sttl value and label, with
the share of that split's normal or attack records), run_meta.json.

Usage:
  .venv/bin/python scripts/sttl_profile.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import DEFAULT_CONFIG, RunRecord, data_paths, load_config, load_train_test, new_run_dir  # noqa: E402


def main() -> int:
    cfg = load_config(DEFAULT_CONFIG)
    out = new_run_dir(cfg, "runs", "sttl_profile")
    rec = RunRecord("scripts/sttl_profile.py", cfg, DEFAULT_CONFIG, out, list(data_paths(cfg)))
    tr, te = load_train_test(cfg)
    y = cfg["data"]["label_col"]
    rows = []
    for split, df in [("train", tr), ("test", te)]:
        for lab, name in [(0, "normal"), (1, "attack")]:
            sub = df[df[y] == lab]
            for v, n in sub["sttl"].value_counts().items():
                rows.append({"split": split, "label": name, "sttl": int(v), "rows": int(n),
                             "share_of_label_in_split": round(n / len(sub), 4)})
    res = pd.DataFrame(rows).sort_values(["split", "label", "rows"], ascending=[False, False, False])
    res.to_csv(out / "sttl_by_split_label.csv", index=False)
    rec.save()
    print(res[res["sttl"].isin([254, 62, 31, 0])].to_string(index=False))
    print(f"Wrote {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
