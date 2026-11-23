# Presentation outline (Issue #21)

Draft for the team to adapt. Each member takes sections and states the **one number** they explain (readiness checklist item 15). Presenter names are filled in by the members themselves. Time limit: **10 minutes**.

| # | Slide | Content | Key number | Source | Presenter |
|---|---|---|---|---|---|
| 1 | Title | Team, course (CIS 3370), paper title | — | — | |
| 2 | The claim | One sentence: stacking (RF, KNN, LR → SVM), 11 features, UNSW-NB15 test set, accuracy 0.94 | 0.94 (`paper-reported`, Table 4) | `docs/PAPER_METHOD.md` | |
| 3 | Why this paper | Public data, standard models, exact counts we could check; switched from the CIC-IDS2017 paper on 2026-11-13 | — | `docs/USER_STORIES.md` M1-7 | |
| 4 | The data | Official training/testing files; counts match Table 1 exactly; 68% attacks in training, 55% in testing | 175,341 / 82,332 rows | `results/unsw_audit/2026-11-15_audit/` | |
| 5 | Data quality | No missing values; many duplicates (67,601 in training); `service` "-" in about half the rows | 67,601 | `duplicates.csv`, `values_service.csv` | |
| 6 | Method | Pipeline diagram: 11 features → transform/scale/one-hot → RF, KNN, LR → 10-fold stacking → SVM | 10 folds | `scripts/models.py` | |
| 7 | Choices the paper left out | Proposed D-items, highlight D4 (transform), D14 (positive class), D15 (FAR) | 19 proposed choices | `docs/DEVIATIONS.md` | |
| 8 | Baseline | Majority class 0.5506; RF alone 0.8675 | 0.8675 | `results/runs/2026-11-15_baseline_binary_seed42/` | |
| 9 | Headline result | Paper / ours / difference table | 0.8648 vs 0.94 | `results/comparison/2026-11-15_table4/comparison.md` | |
| 10 | Confusion counts | We catch more attacks (FN 810 vs 2,797) but flag far more normal traffic (FP 10,322 vs 1,635) | FAR 27.9% vs 5.2% | `counts.csv` | |
| 11 | Is it random? Is it our preprocessing? | Seeds 0.8647–0.8662; three preprocessing variants 0.864–0.865 | SD 0.0006 | `seed_spread.csv`, `variants.csv` | |
| 12 | Is our model weaker? | 10-fold CV on training: ours 0.9619 vs paper 0.9285 (ours optimistic: duplicate rows) | 0.9619 | `results/runs/2026-11-15_cv_train_stacking_seed42/` | |
| 13 | Where the false alarms are: `sttl` shift | `sttl` = 254 is about 90% attacks in training (`derived`); its share of normal traffic doubles in testing (20% → 41%); 87% of false alarms are there. A concentration, not a tested cause | 87.4% | `fp_by_sttl.csv`, `sttl_by_split_label.csv` | |
| 14 | Multiclass | Same easy/hard classes as the paper's Table 6; 0.7533 accuracy | 0.7533 | `results/runs/2026-11-15_stacking_multiclass_seed42/` | |
| 15 | Limitations | UNSW-NB15 only; unstated settings are ours; paper's 0.94 (0.946 `derived` from its counts) not explained | — | `docs/REPORT.md` §7 | |
| 16 | Takeaways | What we learned about reproducing IDS papers | — | — | |

**Demo:** run `scripts/run_models.py --task stacking` live (about 2 minutes) or play the offline fallback (Issue #22).

**Dry run log** (Issue #21):

| Date | Duration | Within limit? | Results section intact? | Notes |
|---|---|---|---|---|
| | | | | |
