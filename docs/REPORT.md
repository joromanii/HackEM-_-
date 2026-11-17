# IDS Capstone Report: reproducing a stacking ensemble on UNSW-NB15

> **Draft, 2026-11-15.** All measured numbers come from saved, re-runnable runs under `results/`. Method choices marked *proposed* still need team approval (`docs/DEVIATIONS.md`, Issue #5); changing one is a config edit and a re-run. Sections are to be split among members and rewritten in their own words before submission.

Number labels: `paper-reported` · `derived` (arithmetic on paper numbers) · `measured (results/...)` · `unverified`.

## 1. Overview and research question

**Claim:** Rajagopal et al. (2020) report that a stacking ensemble (random forest, K-nearest neighbours and logistic regression, combined by a support vector machine) using 11 UNSW-NB15 features reaches 0.94 accuracy (precision 0.96, recall 0.93, F1 0.95, AUC 0.99, false alarm rate 5.2%) when classifying normal vs attack traffic on the 82,332-record UNSW-NB15 test set (Table 4, `paper-reported`).

**Research question:** Can that Table 4 result be reproduced, and what explains any gap?

**Answer in one paragraph:** No. Built as the paper describes, our stacking ensemble reaches **0.8648 accuracy** on the same test set, with a false alarm rate of **27.9%** instead of 5.2% (`measured (results/comparison/2026-11-15_table4/comparison.csv)`). The gap is not random (six seeds span 0.8647–0.8662) and not explained by the three alternative preprocessing choices we tested (0.864–0.865). On the training file, the same model is not weaker than the paper reports (10-fold CV accuracy 0.9619 against the paper's 0.9285; ours is optimistic because the training file has many duplicate rows). Our false alarms concentrate in one place: 87.4% are normal test records with `sttl` = 254, a value that is about 90% attack traffic in training (`derived`) while its share of normal traffic rises from 20% in training to 41% in testing. The paper used the same files, so this shift doesn't by itself explain the difference between the paper and us; how the paper reached its test result is not determined.

## 2. Paper selection and feasibility

| Field | Decision / evidence |
|---|---|
| Paper | Rajagopal, Kundapur & Hareesha, “A Stacking Ensemble for Network Intrusion Detection Using Heterogeneous Datasets” |
| Venue and year | *Security and Communication Networks*, 2020, article 4586875 |
| DOI | [10.1155/2020/4586875](https://doi.org/10.1155/2020/4586875) |
| Exact claim | Table 4: binary (normal vs attack) stacking ensemble on the UNSW-NB15 test set |
| Paper-reported values | Accuracy 0.94; precision 0.96; recall 0.93; F1 0.95; AUC 0.99; FAR 5.2% |
| Why this paper | Public data, standard scikit-learn-style models, exact confusion counts we can check, and a laptop-sized dataset; feasible in about three weeks (stories M1-7, M1-8) |
| Previous target | Kurniabudi et al. 2020 (CIC-IDS2017, Table 9), dropped 2026-11-13; reason to be recorded by the team in Issue #1 |
| Team meeting | Thursday 2026-11-12, going over the paper (reported by the repo owner; notes in `docs/MEETINGS.md`) |
| Scope | UNSW-NB15 only; the paper's UGR'16 results are not reproduced (D19, proposed) |

**Checks on the paper's own numbers** (`derived`, `docs/PAPER_METHOD.md`): Table 4's counts sum to the test set and imply attack = positive, although §4 says normal is positive. Accuracy and recall look truncated (counts give 0.9462 and 0.9383). FAR 5.2% matches no standard formula (FP/(FP+TN) = 4.42%).

## 3. Dataset

**Source:** official UNSW-NB15 page, https://research.unsw.edu.au/projects/unsw-nb15-dataset → SharePoint folder → *CSV Files / Training and Testing Sets*. Downloaded 2026-11-15. Free for academic research; the five papers listed on that page must be cited.

**Files** (`measured (results/unsw_audit/2026-11-15_audit/files.csv)`):

| File | Rows | Columns | SHA-256 (first 12) |
|---|---:|---:|---|
| `UNSW_NB15_training-set.csv` | 175,341 | 45 | `bec7dd5ec88d` |
| `UNSW_NB15_testing-set.csv` | 82,332 | 45 | `734fe6642edf` |

**Class counts match the paper's Table 1 exactly** in all 10 classes of both files (`measured (results/unsw_audit/2026-11-15_audit/class_counts_vs_table1.csv)`).

**Class balance** (`measured (results/unsw_audit/2026-11-15_audit/binary_balance.csv)`):

| Split | Normal | Attack | Attack share |
|---|---:|---:|---:|
| Training | 56,000 | 119,341 | 68.1% |
| Testing | 37,000 | 45,332 | 55.1% |

Attack classes, rarest first, in training: Worms 130, Shellcode 1,133, Backdoor 1,746, Analysis 2,000 … Generic 40,000 (`class_counts_vs_table1.csv`).

**Data quality** (`measured (results/unsw_audit/2026-11-15_audit/)`):
- No missing or infinite values in any column (`missing_values.csv`).
- `service` is "-" (no identified service) in 94,168 training and 47,153 test rows; treated as its own category (D7).
- Duplicates: 67,601 extra copies of identical rows in training, 26,387 in testing, and 4,247 test rows identical to a training row (`duplicates.csv`). Kept, as the paper's counts include them (D6).

> **TODO (team):** answer the course's "first four questions" for describing data here (readiness checklist item 4), citing the files above.

## 4. Method

Pipeline (`scripts/models.py`, settings in `configs/run.toml`):

1. **Features:** the paper's 11 (§3.1), selected by name: `sbytes, sttl, sload, tcprtt, smean, ct_srv_src, ct_state_ttl, ct_src_dport_ltm, ct_dst_src_ltm, ct_srv_dst, service` (D2).
2. **Preprocessing, fitted on training data only:** Yeo-Johnson power transform and standard scaling of the 10 numeric features (D4, D5); one-hot encoding of `service` (D3).
3. **Base models (paper Table 3):** random forest (100 trees, gini), KNN (5 neighbours, Minkowski), logistic regression (L2).
4. **Meta-model (paper Table 3):** SVM (C = 1.0, RBF kernel), trained on the base models' class probabilities from 10-fold stratified cross-validation (D10).
5. **Evaluation:** fit once on all 175,341 training rows, score once on all 82,332 test rows. Attack = positive (D14); FAR = FP/(FP+TN) (D15); AUC from the SVM's decision function (D17).

**Reproducibility check:** re-running the headline with the final code gives identical metrics (`measured (results/runs/2026-11-15_stacking_binary_seed42_rerun_current_code/metrics.csv)`); that run records checksums of every script.

**Environment:** Python 3.11.18, scikit-learn 1.6.1, pandas 2.2.3, numpy 2.0.2 (`requirements-lock.txt`); macOS on Apple silicon, 10 CPUs. Seed 42 (D13). Runtime of the headline run: 130 s (`measured (results/runs/2026-11-15_stacking_binary_seed42/run_meta.json)`).

## 5. Deviations from the paper

Full log with reasons: [docs/DEVIATIONS.md](DEVIATIONS.md). All are **proposed**, pending team approval.

| Paper | Our choice | ID |
|---|---|---|
| Features chosen by "IG and hashing" | Use the 11 listed features as given | D2 |
| `service` encoding not stated | One-hot | D3 |
| "Making the distribution normal" | Yeo-Johnson (no missing values to impute) | D4 |
| Scaling not named | Standard scaling | D5 |
| Duplicates not mentioned | Keep; also score test rows not copied from training | D6 |
| Unstated settings | scikit-learn 1.6.1 defaults; LR `max_iter` = 1000 | D9 |
| Stacking details beyond Algorithm 1 | 10-fold stratified CV, probabilities, no passthrough | D10 |
| Positive class ambiguous | Attack | D14 |
| FAR formula unknown | FP/(FP+TN) | D15 |
| Two datasets | UNSW-NB15 only | D19 |

## 6. Results

### Baseline first (readiness item 5)

Same files, features and preprocessing (`measured (results/runs/2026-11-15_baseline_binary_seed42/metrics.csv)`):

| Model | Accuracy | Precision | Recall | F1 | AUC | FAR |
|---|---:|---:|---:|---:|---:|---:|
| Majority class (always "attack") | 0.5506 | 0.5506 | 1.0000 | 0.7102 | 0.5000 | 1.0000 |
| Random forest alone | 0.8675 | 0.8154 | 0.9815 | 0.8908 | 0.9676 | 0.2723 |
| KNN alone | 0.8667 | 0.8220 | 0.9673 | 0.8888 | 0.9342 | 0.2566 |
| Logistic regression alone | 0.7720 | 0.7258 | 0.9418 | 0.8198 | 0.8695 | 0.4359 |

### Stacking ensemble vs the paper (readiness item 7)

`measured (results/comparison/2026-11-15_table4/comparison.csv)`; paper values `paper-reported` (Table 4):

Attack = positive (D14); FAR = FP/(FP+TN) (D15); AUC from the SVM decision function (D17); ours to 4 decimals, the paper's values look truncated (D16).

| Metric | Paper | Ours | Difference |
|---|---:|---:|---:|
| Accuracy | 0.94 | 0.8648 | −0.0752 |
| Precision | 0.96 | 0.8118 | −0.1482 |
| Recall | 0.93 | 0.9821 | +0.0521 |
| F1 | 0.95 | 0.8889 | −0.0611 |
| AUC | 0.99 | 0.9248 | −0.0652 |
| FAR | 5.2% | 27.90% | +22.70 points |

Confusion counts (`measured (results/comparison/2026-11-15_table4/counts.csv)`):

| | Paper | Ours |
|---|---:|---:|
| TP (attack caught) | 42,535 | 44,522 |
| TN (normal passed) | 35,365 | 26,678 |
| FN (attack missed) | 2,797 | 810 |
| FP (normal flagged) | 1,635 | 10,322 |

Our model catches more attacks than the paper's but flags far more normal traffic.

### Multiclass (secondary)

10-class stacking on the full test set: accuracy **0.7533**, macro F1 0.4699 (`measured (results/runs/2026-11-15_stacking_multiclass_seed42/metrics.csv)`). Random forest alone: 0.7547 (`measured (results/runs/2026-11-15_baseline_multiclass_seed42/metrics.csv)`). The paper's Table 6 used an unexplained 51,535-record subset (N4), so we compare per-class recall only:

| Class | Paper recall (Table 6) | Our recall | Test rows |
|---|---:|---:|---:|
| Generic | 98.32% | 96.70% | 18,871 |
| Exploits | 85% | 86.11% | 11,132 |
| Reconnaissance | 74.8% | 78.86% | 3,496 |
| Shellcode | 58.22% | 78.57% | 378 |
| Fuzzers | 60.97% | 57.09% | 6,062 |
| Normal | 91.82% | 74.19% | 37,000 |
| Worms | 37.5% | 29.55% | 44 |
| DoS | 25% | 4.38% | 4,089 |
| Analysis | 11% | 0.89% | 677 |
| Backdoor | 10.79% | 3.77% | 583 |

Paper values `paper-reported`; ours `measured (results/runs/2026-11-15_stacking_multiclass_seed42/per_class_stacking.csv)`. The same classes are easy (Generic, Exploits, Reconnaissance) and hard (Analysis, Backdoor, DoS) in both. Normal recall is much lower for us, matching the binary false-alarm problem.

## 7. Gap analysis (readiness item 8)

| Possible cause | Test | Result | Verdict |
|---|---|---|---|
| Random variation | Stacking with seeds 1–5 and 42 | Accuracy 0.8647–0.8662, SD 0.0006 (`measured (results/comparison/2026-11-15_table4/seed_spread.csv)`) | **Ruled out**: far smaller than the 0.075 gap |
| Unstated preprocessing (D3–D5) | log1p instead of Yeo-Johnson; no transform with min-max; hashing for `service` | Accuracy 0.8640–0.8652, FAR 27.8–28.2% (`measured (results/comparison/2026-11-15_table4/variants.csv)`) | **Ruled out** for these alternatives |
| Duplicate rows leaking train into test (D6) | Score only the 78,085 test rows not identical to a training row | Accuracy 0.8603 (`measured (comparison.csv, ours_test_unseen)`) | **Ruled out**: duplicates don't inflate or explain the gap |
| A weaker model than the paper's | 10-fold CV on the training file, as the paper's Table 5 | Ours 0.9619 ± 0.0011 vs paper 0.9285 (`measured (results/runs/2026-11-15_cv_train_stacking_seed42/summary_vs_table5.csv)`) | **Not weaker** in-distribution. Caveat: the training file has 67,601 exact duplicate rows (78,679 on the 11 features), so CV folds share identical rows and 0.9619 is optimistic (`measured (results/unsw_audit/2026-11-15_audit/duplicates.csv)`) |
| Shift between the training and test files | Where false alarms fall; `sttl` by split and label | 87.4% of false alarms are normal test records with `sttl` = 254 (`measured (results/runs/2026-11-15_error_analysis_stacking_seed42/fp_by_sttl.csv)`). In training, `sttl` = 254 is 103,513 attack vs 11,230 normal rows; in testing, 39,000 attack vs 15,049 normal (`measured (results/runs/2026-11-15_sttl_profile/sttl_by_split_label.csv)`) | **Where our false alarms concentrate.** Not tested as a cause (no run removes or reweights `sttl`); the paper had the same files |
| How the paper reached 0.94 (0.946 `derived` from its counts) | — | The paper doesn't give enough detail. Its own Table 5 (0.9285 on training) is lower than its Table 4 test accuracy, the reverse of what we see (0.9619 CV vs 0.8648 test) | **Not determined** |

**Other observations**
- Stacking adds nothing over random forest alone on this split (0.8648 vs 0.8675).
- The paper's FAR of 5.2% can't be checked: its own counts give 4.42% (N3).

**Limitations:** one dataset only (UGR'16 not reproduced); every unstated setting is our proposal, not the paper's; the paper's 11 features were taken as given, not re-derived.

## 8. Reproduction instructions

See the runbook: [docs/wiki/Runbook.md](wiki/Runbook.md) (to be copied into the GitHub wiki, Issue #20). Headline result in two commands after setup:

```bash
.venv/bin/python scripts/audit_unsw.py
.venv/bin/python scripts/run_models.py --task stacking
```

## 9. Evidence index

| Evidence | Path | What it verifies |
|---|---|---|
| Data audit | [`results/unsw_audit/2026-11-15_audit/`](../results/unsw_audit/2026-11-15_audit/) | Files, checksums, Table 1 match, balance, quality, duplicates |
| Baseline | [`results/runs/2026-11-15_baseline_binary_seed42/`](../results/runs/2026-11-15_baseline_binary_seed42/) | Majority class and each base model |
| Headline stacking run | [`results/runs/2026-11-15_stacking_binary_seed42/`](../results/runs/2026-11-15_stacking_binary_seed42/) | Table 4 reproduction attempt |
| Re-run with final code | [`results/runs/2026-11-15_stacking_binary_seed42_rerun_current_code/`](../results/runs/2026-11-15_stacking_binary_seed42_rerun_current_code/) | Same metrics; checksums of every script |
| Seed runs | `results/runs/2026-11-15_stacking_binary_seed{1..5}/` | Run-to-run variation |
| Preprocessing variants | `results/runs/2026-11-15_stacking_binary_seed42_{log1p,minmax_notransform,hashing}/` | Sensitivity to unstated steps |
| CV on training | [`results/runs/2026-11-15_cv_train_stacking_seed42/`](../results/runs/2026-11-15_cv_train_stacking_seed42/) | Comparison with paper Table 5 |
| False-alarm analysis | [`results/runs/2026-11-15_error_analysis_stacking_seed42/`](../results/runs/2026-11-15_error_analysis_stacking_seed42/), [`results/runs/2026-11-15_sttl_profile/`](../results/runs/2026-11-15_sttl_profile/) | Cause of the gap |
| Comparison table | [`results/comparison/2026-11-15_table4/`](../results/comparison/2026-11-15_table4/) | Paper / ours / difference |
| Config and environment | `configs/run.toml`, `configs/variants/`, `requirements-lock.txt` | Settings and versions |
| Decisions | `docs/DEVIATIONS.md`, Issue #5 | Every unstated choice |
| Superseded: CIC-IDS2017 audit | [`results/inventory/2026-11-02_audit/`](../results/inventory/2026-11-02_audit/) | Record of the earlier target only |

## 10. Contributions

Use the Individual Contribution Summary Table at the bottom of the README. Each member fills in their own row from issue, PR, commit and document evidence.

## 11. References

- Rajagopal, S., Kundapur, P. P., & Hareesha, K. S. “A Stacking Ensemble for Network Intrusion Detection Using Heterogeneous Datasets.” *Security and Communication Networks*, 2020, 4586875. [DOI](https://doi.org/10.1155/2020/4586875)
- Moustafa, N., & Slay, J. “UNSW-NB15: a comprehensive data set for network intrusion detection systems.” MilCIS 2015, IEEE. (Required citation for the dataset; the other four are listed on the official page.)
- UNSW-NB15 dataset page: https://research.unsw.edu.au/projects/unsw-nb15-dataset
