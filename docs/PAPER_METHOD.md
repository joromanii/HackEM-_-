# Paper method specification: CICIDS-2017 feature analysis

This file translates the selected paper into an auditable reproduction target. It is a specification, not evidence that the experiment has been run.

## Selected paper

Kurniabudi et al., “CICIDS-2017 Dataset Feature Analysis With Information Gain for Anomaly Detection,” *IEEE Access*, vol. 8, 2020, pp. 132911–132921. DOI: [10.1109/ACCESS.2020.3009843](https://doi.org/10.1109/ACCESS.2020.3009843).

The paper studies CICIDS2017 and feature selection with Information Gain. The team-selected target is its **Table 9 Random Forest row using 22 features**.

## Exact quantitative target

| Paper table / model | Feature count | Accuracy | Recall | False-positive rate | Precision |
|---|---:|---:|---:|---:|---|
| Table 9 / Random Forest | 22 | 99.86% | 0.999 | 0.003 | NaN (reported) |

These are values reported by the paper, not results from this repository. The paper explains that NaN can occur when a rare class is absent from some cross-validation folds; it specifically notes that Random Forest does not detect Infiltration with the 22-feature subset. Preserve NaN for the paper value and report our own metrics with explicit averaging and per-class definitions.

## Selected 22-feature set

After removing one of the duplicated Fwd Header Length columns, the paper analyzes 77 features and labels its feature IDs from 1 to 77. The list below records the Table 6 22-feature subset at the >=0.4 Information Gain threshold, with the corresponding CICIDS2017 names. These IDs are paper identifiers, not raw CSV offsets; keep each ID/name pair together and verify the exact header spelling before training.

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

**Verification gate:** Confirm which of the two Fwd Header Length columns is removed in the downloaded files, then verify every ID/name pair against the paper's feature tables and the CSV header. Select by verified column name, not raw numeric position.

## Method extraction and unresolved protocol

The paper's reported pipeline has two data-size/splitting stages: it uses only 20% of MachineLearningCSV, removes one duplicate Fwd Header Length column, relabels attack types (Table 3), and splits that 20% into 70% training and 30% test. It says Information Gain feature ranking is performed on training data. Its classifier-results section then describes 10-fold cross-validation (nine folds train, one fold test, rotating the test fold through all ten). The paper does not clearly state whether this cross-validation is run only inside the 70% training portion, across the 20% sample, or in another way after the holdout split. Resolve this protocol from the paper and tables; if it remains unclear, predeclare our interpretation as a deviation and do not describe it as an exact reproduction.

The paper defines seven feature subsets: weights >=0.6, >=0.5, >=0.4, >=0.3, >=0.2, >=0.1, and all features. The 22-feature target is the >=0.4 subset. It uses Weka 3.9; the Random Forest configuration and several implementation details are not specified in enough detail to assume defaults silently.

Before fitting:
- verify all CSV files, columns, label values, duplicate-header handling, and row counts; record excluded/invalid rows;
- document how the paper's 20% sample is selected, or mark this as an unrecoverable specification and predeclare a reproducible sampling rule;
- transcribe and verify Table 3's attack relabeling map; the task is multiclass (including normal traffic and grouped attack labels), not a binary benign-vs-attack task;
- determine whether 10-fold CV runs inside the 70% training partition or on another stated subset;
- verify the Table 6 feature ID/name pairs against the exact CSV headers;
- find the precise Random Forest parameters and metric averaging/reporting definitions;
- fix seeds, package versions, splits, preprocessing, and any class balancing;
- preserve confusion matrices and per-class metrics so FPR, TPR, recall, precision, and accuracy are computed consistently.

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
- [Full paper PDF, University of Sriwijaya repository](https://repository.unsri.ac.id/34942/1/CICIDS-2017%20Dataset%20Feature%20Analysis%20With.pdf)
- [Full paper PDF (University of Sriwijaya repository)](https://repository.unsri.ac.id/34942/1/CICIDS-2017%20Dataset%20Feature%20Analysis%20With.pdf)
- [Official CICIDS2017 dataset page](https://www.unb.ca/cic/datasets/ids-2017.html)
- Related feature-index cross-check: [Important Features of CICIDS-2017 Dataset for Anomaly Detection (2021 PDF)](https://repository.unsri.ac.id/59455/1/Important_Features_of_CICIDS_2017_Dataset_For_Anom.pdf). This is a secondary cross-check; the original paper remains authoritative.
