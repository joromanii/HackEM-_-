# Deviations and decisions log

Every place where the paper (Rajagopal et al. 2020) is unclear, or where we do something different, is logged here **before** code acts on it. Background and options: [docs/PAPER_METHOD.md](PAPER_METHOD.md) (open questions S1–S14).

**Status:**
- **Proposed**: written down and used by the code, but **the team has not approved it yet**. Approve or change each one in Issue #5, then mark it **Decided** with a link and date.
- **Decided**: approved by the team (link, date).
- **Note**: a paper inconsistency; no choice needed.

All choices live in [`configs/run.toml`](../configs/run.toml), so changing one is a config edit and a re-run, not a code change.

Number labels: `paper-reported`, `derived` (arithmetic on paper numbers), `measured (results/...)`, `unverified`.

## Data and features

| ID | Spec | Topic | Paper | Proposed choice | Why | Status |
|---|---|---|---|---|---|---|
| D1 | S1 | Data files | Table 1 counts only | Official partition files `UNSW_NB15_training-set.csv` / `UNSW_NB15_testing-set.csv`, from the UNSW research page's SharePoint folder, downloaded 2026-11-15 | All 10 class counts in both files equal Table 1 exactly: `measured (results/unsw_audit/2026-11-15_audit/class_counts_vs_table1.csv)` | Proposed |
| D2 | S2 | Feature selection | "IG and hashing" → 11 named features (§3.1) | Use the 11 listed features as given; don't re-run the paper's selection | The method that picked them is not described well enough to repeat; all 11 exist in both files (`measured`, `columns.csv`) | Proposed |
| D3 | S3 | Encoding of `service` | Not stated | One-hot encoding, fitted on training data; unseen values ignored | `service` has 13 values in train and none new in test (`measured`, `feature_summary.csv`); one-hot is exact, hashing would merge values | Proposed |
| D4 | S4 | Missing values and outliers ("making the distribution normal") | No method named | No imputation (none needed). Yeo-Johnson power transform on the 10 numeric features, fitted on training data | No NaN or Inf in any column (`measured`, `missing_values.csv`); Yeo-Johnson pushes skewed features toward a normal shape and handles zeros, matching the paper's wording most directly | Proposed |
| D5 | S5 | Feature scaling | "Feature scaling was applied" | Standardize (mean 0, sd 1) after the power transform | Needed by KNN, LR and the RBF SVM; done by a `StandardScaler` after the power transform | Proposed |
| D6 | S13 | Duplicate rows | Not mentioned | **Keep** all rows (use the files as published). Also score the test rows that are **not** copies of a training row, as a sensitivity check | Table 1 counts include duplicates, so the paper kept them. 67,601 extra copies in train, 4,247 test rows identical to a train row (`measured`, `duplicates.csv`) | Proposed |
| D7 | — | `service = "-"` | Not mentioned | Treat "-" as its own category | It's the most common value (94,168 train rows) and means "no identified service" (`measured`, `values_service.csv`), not missing data | Proposed |

## Model and stacking

| ID | Spec | Topic | Paper | Proposed choice | Why | Status |
|---|---|---|---|---|---|---|
| D8 | S7 | Software | Not named | Python 3.11, scikit-learn 1.6.1 (pinned in `requirements-lock.txt`) | Table 3 setting names (gini, Minkowski, L2, rbf) match scikit-learn (`unverified` that the authors used it) | Proposed |
| D9 | S7 | Unstated model settings | Only Table 3 values | scikit-learn 1.6.1 defaults for everything not in Table 3, except logistic regression `max_iter = 1000` | `max_iter` raised only so the solver converges; SVM `gamma = "scale"` is the default | Proposed |
| D10 | S6 | Stacking details | Algorithm 1: cross-validated base predictions | `StackingClassifier`: 10-fold stratified CV (shuffled, project seed), base models give class probabilities, SVM sees base outputs only | 10 folds as in Table 5; probabilities carry more information than labels; Algorithm 1 shows base outputs only | Proposed |
| D11 | S8 | SVM runtime | Implied full training set | Train on all 175,341 rows; time it first on a sample | Timed on 5,000 and 20,000-row samples in a scratch dry run (not saved); the full run took 130 s, so no subsampling was needed (`measured (results/runs/2026-11-15_stacking_binary_seed42/run_meta.json)`) | Proposed |
| D12 | — | Fitting order | Not stated | Preprocessing is fitted on the full training set, then the stacking CV runs on the transformed training data. The test set is never used for fitting | Keeps the test set clean. Within the CV, folds share the preprocessing fit; a small, standard simplification | Proposed |
| D13 | — | Seeds | Not stated | One seed (42) from config for every random step; the final comparison also reruns with seeds 1–5 to measure variation | Readiness item 8 needs variation measured before calling a gap real | Proposed |

## Metrics and comparison

| ID | Spec | Topic | Paper | Proposed choice | Why | Status |
|---|---|---|---|---|---|---|
| D14 | S9 | Positive class | Text: normal; Table 4 counts: attack | Attack (label 1) is positive | Table 4's counts only add up that way (`derived`, `PAPER_METHOD.md`); the dataset's `label` column uses 1 = attack | Proposed |
| D15 | S10 | FAR formula | 5.2%, formula not shown | FAR = FP / (FP + TN): normal traffic wrongly flagged | Standard definition; gives 4.42% on the paper's own counts (`derived`), so the paper's 5.2% stays unexplained | Proposed |
| D16 | S11 | Rounding | Values look truncated | Report ours to 4 decimals, and compare with the paper's printed value | The paper's accuracy and recall look truncated (`derived`) | Proposed |
| D17 | — | AUC | 0.99, score not stated | ROC AUC from the SVM's decision function on the test set | SVM decision scores are the natural ranking score | Proposed |
| D18 | S12 | Multiclass (Table 6) | 51,535 unexplained rows | Secondary: 10-class run on the full test set, compared per class only | Table 6's subset can't be rebuilt | Proposed |
| D19 | S14 | Scope | Two datasets | UNSW-NB15 only; UGR'16 not reproduced | Time (about three weeks) and dataset size | Proposed |

## Paper inconsistencies (notes)

| ID | Note |
|---|---|
| N1 | §4 says true positives are correctly classified **normal** records, but Table 4's counts only add up with **attack** as positive (`derived`). |
| N2 | Table 4 accuracy 0.94 and recall 0.93 look truncated: the counts give 0.9462 and 0.9383 (`derived`). |
| N3 | Table 4 FAR 5.2% matches no standard formula from its own counts (`derived`). |
| N4 | Table 6 covers 51,535 records, not the 82,332-record test set (`derived`). |

## Environment notes

| ID | Note |
|---|---|
| E1 | Logistic regression prints many `RuntimeWarning: overflow / divide by zero / invalid value encountered in matmul` lines on this Mac (numpy 2.0.2 with Apple's Accelerate BLAS). Checked on 2026-11-15: inputs after preprocessing are all finite and between −5 and 4; the lbfgs fit converges in 45 iterations with finite coefficients; it agrees with the liblinear solver on 99.98% of test predictions. Treated as a false alarm (session check, not saved as a results file: `unverified` until rerun). |
