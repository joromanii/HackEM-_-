# Reproduction run 2026-11-19_160941

| Step | Exit code |
|---|---:|
| audit | 0 |
| baseline | 0 |
| stacking | 0 |
| comparison | 0 |

**Headline metrics identical to the saved reference run (`results/runs/2026-11-15_stacking_binary_seed42/metrics.csv`): YES**
Baseline metrics identical to `results/runs/2026-11-15_baseline_binary_seed42/metrics.csv`: YES

Headline run: `results/reproduce/2026-11-19_160941/stacking` (seed 42). Attack = positive (D14); FAR = FP/(FP+TN) (D15); AUC from the SVM decision function (D17). Paper values `paper-reported` (Table 4); ours `measured` from the run's `metrics.csv`.

| Metric | Paper | Ours | Difference | Ours, test rows not copied from train |
|---|---:|---:|---:|---:|
| accuracy | 0.94 | 0.8648 | -0.0752 | 0.8603 |
| precision | 0.96 | 0.8118 | -0.1482 | 0.8041 |
| recall | 0.93 | 0.9821 | +0.0521 | 0.9809 |
| f1 | 0.95 | 0.8889 | -0.0611 | 0.8837 |
| auc | 0.99 | 0.9248 | -0.0652 | 0.9224 |
| far | 0.052 | 0.2790 | +0.2270 | 0.2822 |

Total runtime: 147.6 s (`run_meta.json`).
