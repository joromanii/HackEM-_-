# Paper method specification: CICIDS-2017 feature analysis

This file translates the selected paper into an auditable reproduction target. It is a specification, not evidence that the experiment has been run.

## Selected paper

Kurniabudi et al., “CICIDS-2017 Dataset Feature Analysis With Information Gain for Anomaly Detection,” *IEEE Access*, vol. 8, 2020, pp. 132911–132921. DOI: [10.1109/ACCESS.2020.3009843](https://doi.org/10.1109/ACCESS.2020.3009843).

The paper studies CICIDS2017 and feature selection with Information Gain. The team-selected target is its **Table 9 Random Forest row using 22 features**.

## Exact quantitative target

| Paper table / model | Feature count | Accuracy | Recall | False-positive rate | Precision |
|---|---:|---:|---:|---:|---|
| Table 9 / Random Forest | 22 | 99.86% | 0.999 | 0.003 | NaN (reported) |

These are values reported by the paper. They are not results from this repository. Preserve the paper’s reported NaN for precision in the comparison rather than silently replacing it.

## Selected 22-feature set

The paper numbers the feature columns in its feature-analysis tables. The names below are the corresponding CICIDS2017 fields. Keep IDs and names together when implementing, and verify them against the paper PDF and the exact downloaded CSV header before training.

| Paper feature ID | CICIDS2017 field |
|---:|---|
| 41 | Packet Length Std |
| 13 | Total Length of Bwd Packets |
| 65 | Subflow Bwd Bytes |
| 8 | Destination Port |
| 42 | Packet Length Variance |
| 20 | Bwd Packet Length Mean |
| 54 | Avg Bwd Segment Size |
| 18 | Bwd Packet Length Max |
| 67 | Init_Win_bytes_backward |
| 12 | Total Length of Fwd Packets |
| 63 | Subflow Fwd Bytes |
| 66 | Init_Win_bytes_forward |
| 52 | Average Packet Size |
| 40 | Packet Length Mean |
| 39 | Max Packet Length |
| 14 | Fwd Packet Length Max |
| 22 | Flow IAT Max |
| 36 | Bwd Header Length |
| 9 | Flow Duration |
| 26 | Fwd IAT Max |
| 55 | Fwd Header Length |
| 24 | Fwd IAT Total |

**Verification gate:** Confirm whether the paper's numbering is one-based and which original CSV column is excluded as redundant before using these numeric IDs. The names above are implementation keys; do not select columns by numeric position until the mapping has been checked against the paper's own tables and the CSV header.

## Method extraction and unresolved protocol

The paper describes feature grouping and Information Gain thresholding, identifies a 22-feature set at the stated threshold (>= 0.4), and reports a 70:30 train/test split. It also describes repeated 10-fold cross-validation (nine folds for training and one for testing, repeated ten times). The exact relationship between the 70:30 holdout and the repeated 10-fold procedure must be resolved from the full text before results are compared.

Record the authors' wording and the team's operational interpretation in the experiment configuration and final report. If the paper does not define how the procedures interact, label the chosen interpretation as a deviation/assumption, and include a sensitivity run only if time and compute allow.

Before fitting:
- verify all CSV files, columns, label values, and row counts; record excluded/invalid rows;
- confirm the 78 original predictors and which redundant feature is removed, leaving 77 ranked predictors;
- determine whether the 22-feature list is fixed from the paper or reselected using only each training fold;
- reproduce the paper's seven feature groups and Information Gain calculation/threshold from the full text;
- establish target label mapping and binary vs. multiclass task definition;
- find the precise Random Forest parameters, class/label handling, and metric averaging definitions in the paper;
- fix the split/CV protocol, random seeds, package versions, and any class balancing;
- preserve confusion matrix and metric definitions so the paper's FPR and recall can be computed consistently.

Do not infer unspecified settings from the paper's reported score. If a setting cannot be recovered, document the reason and the predeclared choice.

## Dataset and local progress

The team reports having CICIDS2017 MachineLearningCSV extracted locally at `~/Downloads/MachineLearningCVE/`. A prior local label-count run was reported as 2,830,743 rows, 15 labels, and 79 CSV columns (including label), with approximately 80.3% benign and 19.7% attack traffic. The summary file was reported at `~/ids-capstone/results/dataset_label_counts.csv`. These facts are user-reported prior work; the repository has not independently verified the files or rerun those counts.

Official dataset page: [CICIDS2017, Canadian Institute for Cybersecurity](https://www.unb.ca/cic/datasets/ids-2017.html).

## Reproduction comparison table

Fill the reproduction columns only from saved, reproducible runs.

| Metric | Paper Table 9 RF (22 features) | Reproduction | Absolute gap | Notes |
|---|---:|---:|---:|---|
| Accuracy | 99.86% | Pending | Pending | Same label/task definition required |
| Recall | 0.999 | Pending | Pending | Specify averaging and positive class |
| False-positive rate | 0.003 | Pending | Pending | Specify one-vs-rest or binary calculation |
| Precision | NaN (reported) | Pending | Pending | Explain the paper's NaN and local definition |

## Source links

- [IEEE Xplore paper record](https://ieeexplore.ieee.org/document/9142219/)
- [Full paper PDF (University of Sriwijaya repository)](https://repository.unsri.ac.id/34942/1/CICIDS-2017%20Dataset%20Feature%20Analysis%20With.pdf)
- [Official CICIDS2017 dataset page](https://www.unb.ca/cic/datasets/ids-2017.html)
- Related feature-index cross-check: [Important Features of CICIDS-2017 Dataset for Anomaly Detection (2021 PDF)](https://repository.unsri.ac.id/59455/1/Important_Features_of_CICIDS_2017_Dataset_For_Anom.pdf). This is a secondary cross-check; the original paper remains authoritative.
