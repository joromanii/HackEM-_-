# Presentation outline (Issue #21)

**Monday 1 December 2026 · 10-minute limit.** Each member presents one part and states the **one number** they explain (readiness checklist item 15). Presenter names are filled in by the members themselves.

## 10-minute version (proposed, for Aponce0003 and the team to adjust)

10 slides, **9:00 of talking** plus 1:00 of buffer for slide changes and the hand-offs between speakers. Three parts of about 3 minutes, one per member. Every number is from `docs/REPORT.md` and its results files.

| # | Slide | Say this (one line) | Key number | Figure / source | Time | Part |
|---|---|---|---|---|---:|---|
| 1 | Title and the claim | "Rajagopal et al. report a stacking ensemble hits 0.94 accuracy on UNSW-NB15. We rebuilt it to check." | 0.94 (`paper-reported`, Table 4) | `docs/PAPER_METHOD.md` | 0:45 | A |
| 2 | Why this paper, and the data | Public data, standard models, exact counts we can check; our files match the paper's Table 1 exactly | 175,341 / 82,332 rows | `results/unsw_audit/2026-11-15_audit/` | 0:45 | A |
| 3 | Method | 11 features → transform, scale, one-hot → RF, KNN, LR → 10-fold stacking → SVM. The paper left 19 choices unstated; we logged each one | 19 proposed choices | `scripts/models.py`, `docs/DEVIATIONS.md` | 0:45 | A |
| 4 | Baseline first | Always guessing "attack" scores 0.5506; random forest alone already scores 0.8675 | 0.8675 | `results/runs/2026-11-15_baseline_binary_seed42/` | 0:45 | A |
| 5 | Headline result | Paper / ours / difference: 0.8648 vs 0.94 | 0.8648 | fig1 (`results/figures/2026-11-19_figures/fig1_table4_metrics.png`) | 1:15 | B |
| 6 | Confusion counts | We catch more attacks but flag far more normal traffic | FP 10,322 vs 1,635 | fig2 | 0:45 | B |
| 7 | Ruling things out | Not random (six seeds 0.8647–0.8662), not our preprocessing (three variants 0.864–0.865), not duplicates (0.8603). On training data we score 0.9619 vs the paper's 0.9285 | SD 0.0006 | fig5; `summary_vs_table5.csv` | 1:15 | B |
| 8 | Where the false alarms are | 87.4% of false alarms are normal records with `sttl` = 254; that value is about 90% attacks in training, and its share of normal traffic doubles in testing. A concentration, not a tested cause | 87.4% | fig3 and fig4 | 1:15 | C |
| 9 | It reproduces | One command, raw data to this table, identical numbers every time | 147.6 s | 30-second recorded clip of `scripts/reproduce.py` ending in REPRODUCED (#22) | 0:45 | C |
| 10 | Limitations and takeaways | UNSW-NB15 only; unstated settings are our proposals; how the paper got 0.94 is not determined. What we learned about reproducing papers | — | `docs/REPORT.md` §7 | 0:45 | C |
| | | | | | **9:00** | |

**Part times:** A (slides 1–4) 3:00 · B (slides 5–7) 3:15 · C (slides 8–10) 2:45.

**Demo:** a live `reproduce.py` run takes about 2.5 minutes, which is too long for 10 minutes. Play the 30-second recorded clip instead (slide 9, Issue #22), and keep the live command ready only if there's time at the end.

**Backup slides (questions only):** 10-class recall (fig6), data quality (duplicates, `service` "-"), the full D1–D19 list, the leakage check (`results/checks/2026-11-19_no_leakage/`).

**Rules of thumb for the dry run:** one idea per slide; read the key number aloud; if a part runs long, cut words, not slide 5 (readiness item 13 says the results section must stay intact).

## Full outline (backup and Q&A)

The original 16-slide plan, kept so any slide can be pulled back in.

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

**Figures for the full outline:** [`results/figures/2026-11-19_figures/`](../results/figures/2026-11-19_figures/figures.md): slide 9 → fig1, slide 10 → fig2, slide 11 → fig5, slide 13 → fig3 and fig4, slide 14 → fig6.


## Dry run log (Issue #21)

Record every run-through. Readiness item 13 needs at least one inside 10:00 with the results section (slides 5–8) intact.

| Date | Duration | Within limit? | Results section intact? | Notes |
|---|---|---|---|---|
| | | | | |
