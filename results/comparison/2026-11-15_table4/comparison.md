# Table 4 comparison (binary, UNSW-NB15 test set, 82,332 records)

Headline run: `results/runs/2026-11-15_stacking_binary_seed42` (seed 42). Attack = positive (D14); FAR = FP/(FP+TN) (D15); AUC from the SVM decision function (D17). Paper values `paper-reported` (Table 4); ours `measured` from the run's `metrics.csv`.

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

Seed variation over 6 runs (seeds 1, 2, 3, 4, 5, 42):

| Metric | Mean | SD | Min | Max |
|---|---:|---:|---:|---:|
| accuracy | 0.8651 | 0.0006 | 0.8647 | 0.8662 |
| precision | 0.8120 | 0.0007 | 0.8113 | 0.8132 |
| recall | 0.9827 | 0.0004 | 0.9821 | 0.9832 |
| f1 | 0.8892 | 0.0004 | 0.8888 | 0.8900 |
| auc | 0.9280 | 0.0022 | 0.9248 | 0.9317 |
| far | 0.2788 | 0.0012 | 0.2767 | 0.2802 |

Preprocessing sensitivity (seed as headline):

| Variant | accuracy | precision | recall | f1 | auc | far |
|---|---:|---:|---:|---:|---:|---:|
| log1p | 0.8640 | 0.8104 | 0.9830 | 0.8884 | 0.9152 | 0.2817 |
| minmax_notransform | 0.8640 | 0.8105 | 0.9828 | 0.8884 | 0.9278 | 0.2816 |
| hashing | 0.8652 | 0.8122 | 0.9822 | 0.8892 | 0.9243 | 0.2782 |

Baseline (same split and features):

| Model | accuracy | precision | recall | f1 | auc | far |
|---|---:|---:|---:|---:|---:|---:|
| majority | 0.5506 | 0.5506 | 1.0000 | 0.7102 | 0.5000 | 1.0000 |
| rf | 0.8675 | 0.8154 | 0.9815 | 0.8908 | 0.9676 | 0.2723 |
| knn | 0.8667 | 0.8220 | 0.9673 | 0.8888 | 0.9342 | 0.2566 |
| lr | 0.7720 | 0.7258 | 0.9418 | 0.8198 | 0.8695 | 0.4359 |

10-fold CV on the training file vs paper Table 5:

| Metric | Ours (mean ± SD) | Paper | Difference |
|---|---:|---:|---:|
| accuracy | 0.9619 ± 0.0011 | 0.9285 | +0.0334 |
| recall | 0.9802 ± 0.0016 | 0.9115 | +0.0687 |
| precision | 0.9644 ± 0.0013 | 0.9497 | +0.0147 |
