# Project Brief: HackEM-_- — CIC-IDS2017 paper reproduction

## What this is
A capstone project that reproduces and evaluates one published intrusion-detection result on CIC-IDS2017 (MachineLearningCSV).
Target: Kurniabudi et al., "CICIDS-2017 Dataset Feature Analysis With Information Gain for Anomaly Detection," IEEE Access 2020 (DOI 10.1109/ACCESS.2020.3009843), **Table 9, Random Forest, 22 features**.
We implement the paper's preprocessing and Information Gain feature selection as closely as the paper allows, measure our own results with fixed settings, and explain any gap. Ambiguities become documented deviations, not silent choices.

## Current state (as of 2026-11-02)
| Item | Status |
|---|---|
| Paper selected; owner's vote recorded in Issue #2 | Done. Teammate votes **pending**. |
| Paper method spec: `docs/PAPER_METHOD.md` | Written, on branch `docs/select-cicids-paper` (PR #14, open) |
| Paper numbers: 99.86% acc, 0.999 recall, 0.003 FPR, precision NaN | **Paper-reported only. Not reproduced.** |
| Dataset CSVs at `~/Downloads/MachineLearningCVE/` | Present. Header check: 8 files, 79 columns, two `Fwd Header Length` columns |
| Label counts `~/ids-capstone/results/dataset_label_counts.csv` | Exists: 2,830,743 rows, 15 labels. Rerun and matched exactly by the Issue #4 audit: measured (`results/inventory/2026-11-02_audit/label_count_comparison.csv`). |
| Label names | The three Web Attack labels contain U+FFFD (bytes `ef bf bd`) in the raw files: measured (`results/inventory/2026-11-02_audit/label_encoding.csv`). See `docs/DATA_AUDIT.md`. |
| Local env `~/ids-capstone/.venv` | Python 3.9.6 (system), pandas 2.2.3, scikit-learn 1.6.1, numpy 2.0.2. Not pinned in the repo. |
| Data audit (#4): `scripts/audit_inventory.py`, `docs/DATA_AUDIT.md` | Done on branch `m2/setup` (not yet in a PR) |
| Split spec, baseline, model, evaluation | Not started |

## Next milestone: M2 — Data audit and reproducible baseline (Issues #4–#7)
Done means:
- A clean checkout reproduces the dataset inventory (files, rows, labels, duplicates, Inf/NaN) from a committed script (#4).
- Preprocessing and a leakage-safe split are written down **before** training (#5).
- A baseline pipeline runs end to end with a fixed seed and saved outputs (#6).
- Python version, packages, seeds and run steps are pinned (#7).

## Key components and where they live
- Repo: `github.com/joromanii/HackEM-_-` (work in a local clone; kit files at repo root).
- Paper spec: `docs/PAPER_METHOD.md`. Deviations log: `docs/DEVIATIONS.md` (TODO: create).
- Raw data: `~/Downloads/MachineLearningCVE/` — **read-only, never committed**.
- Earlier local work: `~/ids-capstone/` (`scripts/inspect_data.py`, `results/dataset_label_counts.csv`).
- Issues: #1–#3 and #13 (M1), #4–#7 (M2), #8 (M3), #9 (M4), #10–#12 (M5).

## Open questions
- How did the paper draw its 20% sample? (Unspecified so far.)
- Does 10-fold CV run inside the 70% train split, or on the whole 20% sample?
- Weka 3.9 Random Forest settings, and how metrics were averaged (multiclass).
- Which duplicate `Fwd Header Length` column was dropped? The two are identical in every row: measured (`results/inventory/2026-11-02_audit/fwd_header_check.csv`), so the choice doesn't change values, but the rule still needs writing down.
- Do we remove duplicate rows? (Not stated in the paper; affects accuracy.) 308,381 rows (10.89%) are extra copies of an earlier identical row: measured (`results/inventory/2026-11-02_audit/duplicates.csv`).
- Machine RAM: unknown. Load data in chunks or by column until confirmed.
- Team roster and GitHub usernames: TODO. Issue assignments: TODO (team decision).
