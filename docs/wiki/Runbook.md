# Runbook: reproduce our results from scratch

Copy this page into the GitHub wiki (Issue #20). A team member who did **not** write it should follow it start to finish and record in Issue #20 where they got stuck (readiness checklist item 9).

Tested on macOS (Apple silicon) with Homebrew. Total time: about 10 minutes for setup and the headline result; about 45 minutes for every gap-analysis run.

## 1. Get the code

```bash
git clone https://github.com/joromanii/HackEM-_-.git
cd HackEM-_-
```

## 2. Install Python 3.11 and the pinned packages

```bash
brew install python@3.11
python3.11 -m venv .venv
.venv/bin/pip install -r requirements-lock.txt
```

`requirements-lock.txt` pins every package (scikit-learn 1.6.1, pandas 2.2.3, numpy 2.0.2).

## 3. Download the data (about 46 MB)

1. Open the official UNSW-NB15 page: https://research.unsw.edu.au/projects/unsw-nb15-dataset
2. Click **HERE** (the SharePoint folder) → **CSV Files** → **Training and Testing Sets**.
3. Download `UNSW_NB15_training-set.csv` (30.8 MB) and `UNSW_NB15_testing-set.csv` (14.7 MB).
4. Put both in `~/Downloads/UNSW-NB15/`. To use another folder, change `data_dir` in `configs/run.toml`.

Never copy the data into the repo.

## 4. Check your data matches ours (under 1 second)

```bash
.venv/bin/python scripts/audit_unsw.py
```

It writes `results/unsw_audit/<today>_audit/`. Check:
- `class_counts_vs_table1.csv`: every row says `True` (the counts match the paper's Table 1). The script stops with exit code 2 if not.
- `files.csv`: the `sha256` values match `results/unsw_audit/2026-11-15_audit/files.csv`.

## 5. Baseline (about 15 seconds)

```bash
.venv/bin/python scripts/run_models.py --task baseline
```

Majority class, then random forest, KNN and logistic regression alone. Results in `results/runs/<today>_baseline_binary_seed42/metrics.csv`.

## 6. Headline result in one command (about 2.5 minutes)

```bash
.venv/bin/python scripts/reproduce.py
```

This runs the audit, baseline, stacking model and comparison into one new folder, `results/reproduce/<date>_<time>/`, and ends with **REPRODUCED** if the headline metrics are identical to the saved run (it also checks the baseline). Total runtime is saved in that folder's `run_meta.json` (147.6 s on our 10-CPU laptop). Open `summary.md` in that folder. Post the result in Issue #20.

To run only the stacking model:

```bash
.venv/bin/python scripts/run_models.py --task stacking
```

Results in `results/runs/<today>_stacking_binary_seed42/metrics.csv`. The `test_all` row is the headline; compare it with `results/comparison/` (step 8).

You may see many `RuntimeWarning: ... encountered in matmul` lines from logistic regression. They are a known false alarm from numpy 2.0 with macOS's Accelerate library; the fit converges and agrees with another solver (see `docs/DEVIATIONS.md`, E1).

## 7. Gap analysis (optional, about 53 minutes of runtime: `derived` from each run's `run_meta.json`)

```bash
.venv/bin/python scripts/cv_train.py
for s in 1 2 3 4 5; do .venv/bin/python scripts/run_models.py --task stacking --seed $s; done
for v in log1p minmax_notransform hashing; do .venv/bin/python scripts/run_models.py --task stacking --config configs/variants/$v.toml --tag $v; done
.venv/bin/python scripts/run_models.py --task stacking --target multiclass
.venv/bin/python scripts/run_models.py --task baseline --target multiclass
.venv/bin/python scripts/error_analysis.py
.venv/bin/python scripts/sttl_profile.py
.venv/bin/python scripts/check_no_leakage.py   # checks no test row is used for fitting on a 5,000-row sample (about 7 seconds)
.venv/bin/python scripts/make_figures.py       # report and slide figures from saved results
```

## 8. Comparison table

```bash
.venv/bin/python scripts/compare.py --main results/runs/<date>_stacking_binary_seed42 \
  --seeds results/runs/<date>_stacking_binary_seed{1,2,3,4,5} \
  --variants results/runs/<date>_stacking_binary_seed42_{log1p,minmax_notransform,hashing} \
  --baseline results/runs/<date>_baseline_binary_seed42 \
  --cv results/runs/<date>_cv_train_stacking_seed42
```

Writes `results/comparison/<today>_table4/comparison.md`.

## Rules to remember

- Every script writes a **new** results folder and refuses to overwrite one.
- Every run saves `run_meta.json`: config, package versions, input checksums, git commit, runtime.
- Method choices live in `configs/run.toml` and are explained in `docs/DEVIATIONS.md`. Change a choice there, not in code.

## Where I got stuck (tester fills in)

| Step | Problem | How it was solved |
|---|---|---|
| | | |
