# Paper method specification: stacking ensemble on UNSW-NB15

This file turns the selected paper into a reproduction target we can check. It is a specification, not evidence that anything has been run.

> **Target changed on 2026-11-13.** The team moved from Kurniabudi et al. 2020 (CIC-IDS2017, Table 9) to the paper below. The previous spec is preserved in git: `git show 33c47b5:docs/PAPER_METHOD.md`. The reason for the change and each member's vote belong in Issue #1 and Issue #2. **Team votes on this paper are pending.**

Number labels used here: `paper-reported` (with table/section), `derived` (arithmetic on paper numbers, shown), `measured (file)`, or `unverified`.

## Selected paper

Smitha Rajagopal, Poornima Panduranga Kundapur, Katiganere Siddaramappa Hareesha, "A Stacking Ensemble for Network Intrusion Detection Using Heterogeneous Datasets," *Security and Communication Networks*, vol. 2020, article 4586875, published 24 January 2020. DOI: [10.1155/2020/4586875](https://doi.org/10.1155/2020/4586875). Open access.

Read from the [Wiley Online Library full text](https://onlinelibrary.wiley.com/doi/10.1155/2020/4586875) on 2026-11-13. All tables below were available as text on that page (no hand transcription from images).

## The claim in one sentence

Rajagopal et al. (2020) report that a stacking ensemble (random forest, K-nearest neighbours and logistic regression, combined by a support vector machine) using 11 UNSW-NB15 features reaches **0.94 accuracy** (precision 0.96, recall 0.93, F1 0.95, AUC 0.99, false alarm rate 5.2%) when classifying normal vs attack traffic on the 82,332-record UNSW-NB15 test set (Table 4).

## Exact quantitative target

**Table 4, binary classification on UNSW-NB15** (`paper-reported`):

| TP | TN | FN | FP | Accuracy | Precision | Recall | F1 | AUC | FAR |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 42,535 | 35,365 | 2,797 | 1,635 | 0.94 | 0.96 | 0.93 | 0.95 | 0.99 | 5.2% |

The abstract repeats "94% accuracy" for UNSW-NB15.

**Checks on Table 4** (`derived` from the four counts above):

| Quantity | From the counts | Paper | Note |
|---|---:|---:|---|
| Total | 82,332 | — | Equals the Table 1 test-set size |
| Attacks (TP + FN) | 45,332 | — | Equals Table 1 test attacks (82,332 − 37,000 normal) |
| Normal (TN + FP) | 37,000 | — | Equals Table 1 test Normal |
| Accuracy (TP+TN)/total | 0.94617 | 0.94 | Paper value looks **truncated** (rounding gives 0.95) |
| Precision TP/(TP+FP) | 0.96298 | 0.96 | Matches |
| Recall TP/(TP+FN) | 0.93830 | 0.93 | Paper value looks **truncated** (rounding gives 0.94) |
| F1 | 0.95048 | 0.95 | Matches |
| FP/(FP+TN) | 4.42% | 5.2% | **No standard formula gives 5.2%**: FN/(FN+TP) 6.17%, 1 − accuracy 5.38%, FP/(FP+TP) 3.70% |

So the counts treat **attack as the positive class**, even though §4 says "True positives denote the correct classifications of normal network instances." See S9–S11 below.

AUC 0.99 cannot be checked from the counts.

**Not the target (secondary only):**
- **Table 6, 10-class confusion matrix on UNSW-NB15.** Its per-class recall and precision agree with its own matrix to within truncation (`derived`). But it covers only **51,535** records, not the 82,332 test set: for example, Normal has 18,595 rows against 37,000 (assuming Table 6 rows are the true class, as its recall column implies) in the test set (`derived`). The paper doesn't say which records were used, and it reports no overall multiclass accuracy (from the matrix: 0.8221, `derived`). Use it only for per-class discussion.
- **Table 5, 10-fold cross-validation on training data:** mean training accuracy 0.9285, recall 0.9115, precision 0.9497 (`paper-reported`). Useful as a sanity check, not as the target.
- **UGR'16 results** (Tables 7–8, 97.19% accuracy): **out of scope** (proposed). The dataset is very large (1,048,576 flows per attack type used, per Table 2), and three weeks isn't enough. The report must say plainly that only the UNSW-NB15 part is reproduced.

## Data

**UNSW-NB15**, created by the Australian Centre for Cyber Security (§3). Table 1 (`paper-reported`):

| Class | Training | Testing |
|---|---:|---:|
| Normal | 56,000 | 37,000 |
| Generic | 40,000 | 18,871 |
| Exploits | 33,393 | 11,132 |
| Fuzzers | 18,184 | 6,062 |
| DoS | 12,264 | 4,089 |
| Reconnaissance | 10,491 | 3,496 |
| Analysis | 2,000 | 677 |
| Backdoor | 1,746 | 583 |
| Shellcode | 1,133 | 378 |
| Worms | 130 | 44 |
| **Total** | **175,341** | **82,332** |

`unverified`: these totals match the official UNSW-NB15 training and testing partition files (`UNSW_NB15_training-set.csv`, `UNSW_NB15_testing-set.csv`). Confirm by counting the downloaded files. The paper's own data link (Data Availability section) points to an old UNSW address; the current download location must be confirmed before downloading.

## Method as described

**Features (§3.1):** 11 features, selected using "a combination of information gain (IG) and hashing":

`sbytes`, `sttl`, `sload`, `tcprtt`, `smean`, `ct_srv_src`, `ct_state_ttl`, `ct_src_dport_ltm`, `ct_dst_src_ltm`, `ct_srv_dst`, `service`

`service` is a text (categorical) column. The other 10 are numeric (`unverified` until the audit).

**Preprocessing (§3.1):** missing values and outliers "were compensated by making the distribution normal"; feature scaling was applied so large-range features don't dominate. No method names are given.

**Models and settings (Table 3, UNSW-NB15 column):**

| Model | Role | Settings given |
|---|---|---|
| Random forest | Base (level 0) | 100 estimators, criterion gini |
| K-nearest neighbours | Base | 5 neighbours, Minkowski metric |
| Logistic regression | Base | L2 penalty |
| Support vector machine | Meta (level 1) | C = 1.0, RBF kernel |

**Stacking (Algorithm 1):** cross-validation is used to build the meta-classifier's training set. The training data is split into equal subsets, the base models are trained, and each base model's predictions on held-out data become the SVM's inputs.

**Evaluation (§4):** binary results on the test set (Table 4); 10-fold cross-validation results on training data (Table 5); multiclass confusion matrix (Table 6).

The paper does not name its software. `unverified`: the setting names in Table 3 (gini, Minkowski, L2, rbf) match scikit-learn's.

## Fixed rules for our reproduction

These come from the paper, the project rules (`CLAUDE.md`) or the course's readiness checklist, as noted on each; they are not open team choices.

1. **Fit every learned step on training data only** (project rules; standard leakage control): scaling, encoding, any imputation or transform, any feature ranking. The test set is used once, for the final score.
2. **Select features by column name** (project rules), and stop if any of the 11 names is missing.
3. **Compare against Table 4 on the 82,332-record test set** (paper Table 1; that it is the official testing file is `unverified`, S1), with the confusion matrix and the positive class stated.
4. **Fix seeds** (project rules) from the project config, and save config, package versions and runtime with every run.
5. **Run a baseline first** (course readiness checklist item 5, not the paper): a majority-class predictor and each base model on its own, on the same split. The paper reports no single-model numbers, so these have no paper value to compare against.
6. **Never tune toward the paper's numbers** (project rules; Table 4: 0.94 / 0.96 / 0.93 / 0.95 / 0.99 / 5.2%).

## Open questions (team decisions before coding)

Each one gets a row in `docs/DEVIATIONS.md` before we act on it.

| ID | Question | Paper | Options to consider |
|---|---|---|---|
| S1 | Which data files? | Table 1 counts only | Official partition CSVs (counts appear to match); confirm by audit |
| S2 | Feature selection | "IG and hashing" → 11 named features | A. use the 11 listed; B. recompute IG on training data and compare; C. both |
| S3 | Encoding of `service` | Not stated ("hashing" may refer to it) | Feature hashing, one-hot, or integer codes |
| S4 | Missing values and outliers | "making the distribution normal" | Log transform, power transform (Yeo-Johnson), quantile-to-normal, or none if no missing values exist |
| S5 | Feature scaling | "Feature scaling was applied" | Standard scaling or min-max scaling |
| S6 | Stacking details | Algorithm 1 | Number of folds (Table 5 uses 10); base outputs as class labels or probabilities; whether the SVM also sees the original features |
| S7 | SVM `gamma` and other unstated settings | Only C and kernel | Library defaults (state version); LR solver and C; RF/KNN other settings |
| S8 | Training on all 175,341 rows | Implied | An RBF SVM may be slow at this size; time on a sample first; any subsampling is a deviation |
| S9 | Positive class | Text: normal; counts: attack | Report attack-positive to match the counts; state both |
| S10 | FAR definition | 5.2%, formula not shown | Report FP/(FP+TN) and note the mismatch; don't chase 5.2% |
| S11 | Rounding | Values look truncated | Report ours to 4 decimals; compare with both truncated and rounded paper values |
| S12 | Table 6 evaluation set | 51,535 records, unexplained | Secondary only; run multiclass on the full test set and say so |
| S13 | Duplicates, missing values in UNSW-NB15 | Not stated | Measure in the data audit first |
| S14 | Scope | Two datasets | UNSW-NB15 only (UGR'16 out of scope); say so in the report |

Do not infer unstated settings from the paper's reported scores.

## Reproduction comparison table

Fill the "Ours" column only from saved, re-runnable runs (`results/...`).

| Metric (binary, UNSW-NB15 test set) | Paper (Table 4) | Ours | Difference | Notes |
|---|---:|---:|---:|---|
| Accuracy | 0.94 | Pending | Pending | Paper likely truncated (counts give 0.946) |
| Precision | 0.96 | Pending | Pending | Attack = positive (proposed, S9) |
| Recall | 0.93 | Pending | Pending | Paper likely truncated (counts give 0.938) |
| F1 | 0.95 | Pending | Pending | |
| AUC | 0.99 | Pending | Pending | State which scores the AUC uses |
| FAR | 5.2% | Pending | Pending | Paper formula unknown (S10) |

## Source links

- [Full text, Wiley Online Library](https://onlinelibrary.wiley.com/doi/10.1155/2020/4586875)
- [DOI 10.1155/2020/4586875](https://doi.org/10.1155/2020/4586875)
- UNSW-NB15 dataset: official page to be confirmed before download (the paper's link is outdated).
