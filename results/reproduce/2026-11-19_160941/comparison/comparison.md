# Table 4 comparison (binary, UNSW-NB15 test set, 82,332 records)

Headline run: `results/reproduce/2026-11-19_160941/stacking` (seed 42). Attack = positive (D14); FAR = FP/(FP+TN) (D15); AUC from the SVM decision function (D17). Paper values `paper-reported` (Table 4); ours `measured` from the run's `metrics.csv`.

| Metric | Paper | Ours | Difference | Ours, test rows not copied from train |
|---|---:|---:|---:|---:|
| accuracy | 0.94 | 0.8648 | -0.0752 | 0.8603 |
| precision | 0.96 | 0.8118 | -0.1482 | 0.8041 |
| recall | 0.93 | 0.9821 | +0.0521 | 0.9809 |
| f1 | 0.95 | 0.8889 | -0.0611 | 0.8837 |
| auc | 0.99 | 0.9248 | -0.0652 | 0.9224 |
| far | 0.052 | 0.2790 | +0.2270 | 0.2822 |

| Count | Paper | Ours | Difference |
|---|---:|---:|---:|
| TP | 42,535 | 44,522 | +1,987 |
| TN | 35,365 | 26,678 | -8,687 |
| FN | 2,797 | 810 | -1,987 |
| FP | 1,635 | 10,322 | +8,687 |

Seed variation over 1 runs (seeds 42):

| Metric | Mean | SD | Min | Max |
|---|---:|---:|---:|---:|
| accuracy | 0.8648 | nan | 0.8648 | 0.8648 |
| precision | 0.8118 | nan | 0.8118 | 0.8118 |
| recall | 0.9821 | nan | 0.9821 | 0.9821 |
| f1 | 0.8889 | nan | 0.8889 | 0.8889 |
| auc | 0.9248 | nan | 0.9248 | 0.9248 |
| far | 0.2790 | nan | 0.2790 | 0.2790 |

Baseline (same split and features):

| Model | accuracy | precision | recall | f1 | auc | far |
|---|---:|---:|---:|---:|---:|---:|
| majority | 0.5506 | 0.5506 | 1.0000 | 0.7102 | 0.5000 | 1.0000 |
| rf | 0.8675 | 0.8154 | 0.9815 | 0.8908 | 0.9676 | 0.2723 |
| knn | 0.8667 | 0.8220 | 0.9673 | 0.8888 | 0.9342 | 0.2566 |
| lr | 0.7720 | 0.7258 | 0.9418 | 0.8198 | 0.8695 | 0.4359 |
