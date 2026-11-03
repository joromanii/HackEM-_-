"""Read-only inventory of the CIC-IDS2017 MachineLearningCSV files (Issue #4).

Reports, never fixes: file checksums, row/column counts, column names,
label counts and label encoding, NaN/Inf counts, whether the two
"Fwd Header Length" columns are identical, and duplicate rows.

The raw CSVs are only read. All outputs go to a new run folder; the script
refuses to write into a folder that already exists.

Usage:
    python scripts/audit_inventory.py                      # full run
    python scripts/audit_inventory.py --nrows 50000 --out-dir /tmp/x  # test run
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import hashlib
import json
import platform
import subprocess
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATA_DIR = Path.home() / "Downloads" / "MachineLearningCVE"
DEFAULT_OLD_COUNTS = Path.home() / "ids-capstone" / "results" / "dataset_label_counts.csv"
LABEL = "Label"  # matched after stripping spaces from the raw header
FWD_HEADER = "Fwd Header Length"
CHUNK_ROWS = 200_000


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def raw_header(path: Path) -> list[str]:
    with path.open(newline="", encoding="utf-8") as f:
        return next(csv.reader(f))


def git_info() -> dict:
    def run(*args: str) -> str:
        try:
            return subprocess.run(["git", *args], cwd=REPO_ROOT, capture_output=True,
                                  text=True, check=True).stdout.strip()
        except Exception as exc:  # git missing or not a repo
            return f"unavailable ({exc.__class__.__name__})"
    return {"commit": run("rev-parse", "HEAD"), "branch": run("rev-parse", "--abbrev-ref", "HEAD"),
            "dirty_files": run("status", "--porcelain")}


def describe_label(label: str) -> dict:
    non_ascii = [f"U+{ord(c):04X}" for c in label if ord(c) > 127]
    return {"label_repr": repr(label), "non_ascii_codepoints": " ".join(non_ascii),
            "utf8_bytes_hex": label.encode("utf-8").hex(" ")}


def audit(data_dir: Path, out_dir: Path, nrows: int | None, old_counts: Path) -> int:
    t0 = time.time()
    started = dt.datetime.now().astimezone().isoformat(timespec="seconds")
    files = sorted(data_dir.glob("*.csv"))
    if not files:
        print(f"No CSV files in {data_dir}", file=sys.stderr)
        return 1

    file_rows, column_rows, inf_nan_rows, fwd_rows = [], [], [], []
    label_counts: dict[tuple[str, str], int] = {}
    full_hashes, feat_hashes, labels_all, file_idx_all = [], [], [], []
    reference_header = None

    for fi, path in enumerate(files):
        print(f"[{fi + 1}/{len(files)}] {path.name}", flush=True)
        header = raw_header(path)
        stripped = [c.strip() for c in header]
        if reference_header is None:
            reference_header = header
        label_pos = stripped.index(LABEL)
        fwd_pos = [i for i, c in enumerate(stripped) if c == FWD_HEADER]
        feat_pos = [i for i in range(len(header)) if i != label_pos]

        n_rows, n_all_nan_rows, fwd_mismatch, fwd_both_nan = 0, 0, 0, 0
        nan_c = np.zeros(len(header), dtype=np.int64)
        pinf_c = np.zeros(len(header), dtype=np.int64)
        ninf_c = np.zeros(len(header), dtype=np.int64)
        dtypes_seen: list[set[str]] = [set() for _ in header]

        # header=0 + names=positions keeps duplicate names apart without pandas renaming them
        reader = pd.read_csv(path, header=0, names=list(range(len(header))), chunksize=CHUNK_ROWS,
                             nrows=nrows, encoding="utf-8", low_memory=False)
        for chunk in reader:
            n_rows += len(chunk)
            for i in range(len(header)):
                col = chunk[i]
                dtypes_seen[i].add(str(col.dtype))
                nan_c[i] += int(col.isna().sum())
                if i != label_pos:
                    vals = pd.to_numeric(col, errors="coerce").to_numpy(dtype="float64")
                    pinf_c[i] += int(np.isposinf(vals).sum())
                    ninf_c[i] += int(np.isneginf(vals).sum())
            feats = chunk[feat_pos].apply(pd.to_numeric, errors="coerce").astype("float64")
            n_all_nan_rows += int(feats.isna().all(axis=1).sum())

            if len(fwd_pos) == 2:
                a = chunk[fwd_pos[0]].to_numpy(dtype="float64")
                b = chunk[fwd_pos[1]].to_numpy(dtype="float64")
                both_nan = np.isnan(a) & np.isnan(b)
                fwd_both_nan += int(both_nan.sum())
                fwd_mismatch += int(((a != b) & ~both_nan).sum())

            labels = chunk[label_pos].astype("string").fillna("<NA>")
            for lab, cnt in labels.value_counts().items():
                label_counts[(path.name, lab)] = label_counts.get((path.name, lab), 0) + int(cnt)

            # Hash rows: features as float64 so int/float dtype differences between
            # chunks/files don't change the hash; label as string.
            feats.columns = [str(c) for c in feats.columns]
            fh = pd.util.hash_pandas_object(feats, index=False).to_numpy()
            with_label = feats.assign(_label=labels.to_numpy())
            full_hashes.append(pd.util.hash_pandas_object(with_label, index=False).to_numpy())
            feat_hashes.append(fh)
            labels_all.append(labels.to_numpy(dtype=object))
            file_idx_all.append(np.full(len(chunk), fi, dtype=np.int16))

        file_rows.append({"file": path.name, "size_bytes": path.stat().st_size,
                          "sha256": sha256_file(path), "rows": n_rows, "columns": len(header),
                          "header_same_as_first_file": header == reference_header,
                          "rows_all_features_nan": n_all_nan_rows})
        for i, name in enumerate(header):
            column_rows.append({"file": path.name, "position": i, "raw_name": name,
                                "stripped_name": stripped[i], "has_outer_spaces": name != stripped[i],
                                "dtypes_seen": "|".join(sorted(dtypes_seen[i]))})
            inf_nan_rows.append({"file": path.name, "position": i, "column": stripped[i],
                                 "nan": int(nan_c[i]), "pos_inf": int(pinf_c[i]),
                                 "neg_inf": int(ninf_c[i])})
        fwd_rows.append({"file": path.name, "positions": " ".join(map(str, fwd_pos)),
                         "rows": n_rows, "rows_differing": fwd_mismatch if len(fwd_pos) == 2 else "",
                         "rows_both_nan": fwd_both_nan if len(fwd_pos) == 2 else "",
                         "identical": (fwd_mismatch == 0) if len(fwd_pos) == 2 else ""})

    out_dir.mkdir(parents=True, exist_ok=False)
    pd.DataFrame(file_rows).to_csv(out_dir / "files.csv", index=False)
    pd.DataFrame(column_rows).to_csv(out_dir / "columns.csv", index=False)
    pd.DataFrame(inf_nan_rows).to_csv(out_dir / "inf_nan.csv", index=False)
    pd.DataFrame(fwd_rows).to_csv(out_dir / "fwd_header_check.csv", index=False)

    # Label counts per file plus a TOTAL block
    lc = pd.DataFrame([{"file": f, "label": l, "count": c} for (f, l), c in label_counts.items()])
    totals = lc.groupby("label", as_index=False)["count"].sum().sort_values("count", ascending=False)
    grand = int(totals["count"].sum())
    totals["percentage"] = (totals["count"] / grand * 100).round(4)
    totals.insert(0, "file", "TOTAL")
    pd.concat([lc.sort_values(["file", "count"], ascending=[True, False]), totals]) \
        .to_csv(out_dir / "label_counts.csv", index=False)
    pd.DataFrame([{"label": l, **describe_label(l)} for l in totals["label"]]) \
        .to_csv(out_dir / "label_encoding.csv", index=False)

    # Compare with the earlier saved counts (exact label string match)
    counts_differ = None
    if old_counts.exists():
        old = pd.read_csv(old_counts, encoding="utf-8")[["label", "count"]].rename(columns={"count": "old_count"})
        cmp = totals[["label", "count"]].rename(columns={"count": "new_count"}) \
            .merge(old, on="label", how="outer")
        cmp["match"] = cmp["new_count"] == cmp["old_count"]
        cmp.to_csv(out_dir / "label_count_comparison.csv", index=False)
        counts_differ = not bool(cmp["match"].all())

    # Duplicates (64-bit row hashes; keep-first marks later copies as duplicates)
    full = np.concatenate(full_hashes)
    feat = np.concatenate(feat_hashes)
    labs = np.concatenate(labels_all)
    fidx = np.concatenate(file_idx_all)
    n = len(full)
    _, first_idx = np.unique(full, return_index=True)
    is_dup = np.ones(n, dtype=bool)
    is_dup[first_idx] = False
    within_dup = 0
    for fi in range(len(files)):
        m = fidx == fi
        within_dup += int(m.sum() - len(np.unique(full[m])))
    dup_rows = [{"scope": "all_files", "label": "ALL", "rows": n, "duplicate_rows_extra_copies": int(is_dup.sum())},
                {"scope": "sum_within_each_file", "label": "ALL", "rows": n,
                 "duplicate_rows_extra_copies": within_dup}]
    for lab in sorted(set(labs)):
        m = labs == lab
        dup_rows.append({"scope": "all_files", "label": lab, "rows": int(m.sum()),
                         "duplicate_rows_extra_copies": int((is_dup & m).sum())})
    pd.DataFrame(dup_rows).to_csv(out_dir / "duplicates.csv", index=False)

    # Same features, different labels
    fl = pd.DataFrame({"fh": feat, "label": labs})
    nlab = fl.drop_duplicates().groupby("fh")["label"].nunique()
    conflict_keys = nlab[nlab > 1].index
    conflict = fl[fl["fh"].isin(conflict_keys)]
    pairs = conflict.drop_duplicates().groupby("fh")["label"].apply(lambda s: " | ".join(sorted(s)))
    conf_summary = pairs.value_counts().rename_axis("label_set").reset_index(name="feature_groups")
    conf_rows = conflict.groupby("label").size().rename("rows_in_conflicting_groups").reset_index()
    conf_summary.to_csv(out_dir / "conflicting_labels.csv", index=False)
    conf_rows.to_csv(out_dir / "conflicting_labels_by_label.csv", index=False)

    import sklearn  # version only
    meta = {
        "script": "scripts/audit_inventory.py",
        "script_sha256": sha256_file(Path(__file__)),
        "args": {"data_dir": str(data_dir), "out_dir": str(out_dir), "nrows_per_file": nrows,
                 "old_counts": str(old_counts), "chunk_rows": CHUNK_ROWS},
        "started": started, "runtime_seconds": round(time.time() - t0, 1),
        "python": sys.version, "platform": platform.platform(),
        "packages": {"pandas": pd.__version__, "numpy": np.__version__, "scikit-learn": sklearn.__version__},
        "git": git_info(),
        "randomness": "none (deterministic; no seed needed)",
        "duplicate_method": "pandas.util.hash_pandas_object 64-bit row hashes; features cast to float64, label as string",
        "total_rows": n, "files": len(files),
        "label_counts_differ_from_old": counts_differ,
    }
    (out_dir / "run_meta.json").write_text(json.dumps(meta, indent=2))
    print(f"Wrote {out_dir} in {meta['runtime_seconds']} s")
    if counts_differ:
        print("STOP: label counts differ from the earlier saved counts. See label_count_comparison.csv",
              file=sys.stderr)
        return 2
    return 0


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--data-dir", type=Path, default=DEFAULT_DATA_DIR)
    p.add_argument("--out-dir", type=Path,
                   default=REPO_ROOT / "results" / "inventory" / f"{dt.date.today().isoformat()}_audit")
    p.add_argument("--nrows", type=int, default=None, help="rows per file (test runs only)")
    p.add_argument("--old-counts", type=Path, default=DEFAULT_OLD_COUNTS)
    a = p.parse_args()
    if a.out_dir.exists():
        print(f"Refusing to overwrite existing run folder: {a.out_dir}", file=sys.stderr)
        return 1
    return audit(a.data_dir, a.out_dir, a.nrows, a.old_counts)


if __name__ == "__main__":
    sys.exit(main())
