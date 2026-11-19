# Project proposal: reproducing a stacking-ensemble intrusion detector on UNSW-NB15

**Team HackEM-_- · CIS 3370 Intrusion Detection Systems · Instructor: Dr. Gonzalo D Parra**
**Issue #3 · Draft 2026-11-17**

> This proposal was written after the first results were measured (2026-11-15), so it reports status as well as plans. Number labels: `paper-reported` (from the paper), `derived` (arithmetic on paper numbers), `measured (results/...)` (our saved runs), `unverified`.

## 1. The claim we are reproducing

Rajagopal et al. (2020) report that a stacking ensemble (random forest, K-nearest neighbours and logistic regression, combined by a support vector machine) using 11 UNSW-NB15 features reaches **0.94 accuracy** (precision 0.96, recall 0.93, F1 0.95, AUC 0.99, false alarm rate 5.2%) when classifying normal vs attack traffic on the 82,332-record UNSW-NB15 test set (Table 4, `paper-reported`).

**Paper:** Smitha Rajagopal, Poornima Panduranga Kundapur, Katiganere Siddaramappa Hareesha, “A Stacking Ensemble for Network Intrusion Detection Using Heterogeneous Datasets,” *Security and Communication Networks*, 2020, article 4586875. DOI [10.1155/2020/4586875](https://doi.org/10.1155/2020/4586875). Open access.

## 2. Motivation

- **Why this question matters to us:** the paper argues that combining several classifiers (stacking) gives better intrusion detection than any one of them (§1). Rebuilding the method from its description lets us check whether its reported result holds up, and learn what a paper must state for others to reproduce it.
- **Why this paper:**
  - it uses public data (UNSW-NB15) with fixed official training and testing files;
  - it uses standard models available in scikit-learn;
  - it lists its model settings (Table 3) and the 11 features (§3.1);
  - Table 4 gives exact confusion counts, so we can check the paper's own arithmetic.
- **Why we changed paper:** the team first chose Kurniabudi et al. 2020 (CIC-IDS2017, Table 9). On 2026-11-13 the repo owner moved the target to this paper. The team's reason is to be written in Issue #1. The earlier work (CIC-IDS2017 audit, split spec) is kept in the repo as a record (story M1-10).

## 3. Data

| Item | Detail | Evidence |
|---|---|---|
| Dataset | UNSW-NB15, Australian Centre for Cyber Security | Paper §3 |
| Files | `UNSW_NB15_training-set.csv` (175,341 records), `UNSW_NB15_testing-set.csv` (82,332 records), 45 columns each | `measured (results/unsw_audit/2026-11-15_audit/files.csv)` |
| Source | Official page https://research.unsw.edu.au/projects/unsw-nb15-dataset → SharePoint → *CSV Files / Training and Testing Sets*; downloaded 2026-11-15 | `docs/wiki/Runbook.md` §3 |
| Match to the paper | All 10 class counts in both files equal the paper's Table 1 | `measured (results/unsw_audit/2026-11-15_audit/class_counts_vs_table1.csv)` |
| Class balance | Training 68.1% attack, testing 55.1% attack | `measured (results/unsw_audit/2026-11-15_audit/binary_balance.csv)` |
| Licence | Free for academic research; the official page lists five papers to cite (`unverified`: read from the page on 2026-11-15, not saved) | Official page |
| Handling | Raw files stay outside the repo; never committed | `.gitignore`, `CLAUDE.md` |

## 4. Method

1. **Features:** the paper's 11 features (§3.1), selected by column name.
2. **Preprocessing, fitted on training data only:** a transform and scaling for the 10 numeric features, and one-hot encoding of `service`. The paper doesn't name these methods, so they are proposed choices (D3–D5).
3. **Base models (paper Table 3):** random forest (100 trees, gini), KNN (5 neighbours, Minkowski), logistic regression (L2).
4. **Meta-model (paper Table 3):** SVM (C = 1.0, RBF kernel), trained on cross-validated base-model predictions as in the paper's Algorithm 1. The fold count (10) and the use of class probabilities are our proposed choices (D10).
5. **Evaluation:** train on the full training file, score once on the full test file. Report accuracy, precision, recall, F1, AUC and false alarm rate, a confusion matrix, and the paper / ours / difference table.
6. **Baseline first:** a majority-class predictor and each base model alone, on the same split.
7. **Gap analysis:** seed variation, alternative preprocessing, duplicate rows, cross-validation on the training file, and where the errors fall.

Every choice the paper doesn't state is logged in `docs/DEVIATIONS.md` (D1–D19, covering the open questions S1–S14 in `docs/PAPER_METHOD.md`) and kept in `configs/run.toml`, so changing one is a config edit and a re-run.

## 5. Feasibility

| Factor | Assessment | Evidence |
|---|---|---|
| Data size | About 48 MB (47,673,818 bytes for the two files); fits easily in memory | `measured (results/unsw_audit/2026-11-15_audit/files.csv)` |
| Compute | Headline stacking run: 130 s on a laptop with 10 CPUs | `measured (results/runs/2026-11-15_stacking_binary_seed42/run_meta.json)` |
| | Gap-analysis runs: about 53 minutes of summed runtime (3,208 s); they overlapped, taking about 27 minutes of clock time | `measured` from `runtime_seconds` and `started` in each `results/runs/2026-11-15_*/run_meta.json` (CV, seeds 1–5, three variants, multiclass, error analysis) |
| Software | Python 3.11 and scikit-learn 1.6.1, pinned | `requirements-lock.txt` |
| Skills | Standard scikit-learn pipeline; no deep learning | `scripts/models.py` |
| Time | About three weeks from 2026-11-13; the pipeline and first results were done in the first week | Timeline below |

## 6. Timeline

The presentation date is **to be confirmed**; the weeks below count from the paper switch on 2026-11-13.

| Week | Dates | Work | Status |
|---|---|---|---|
| 1 | Nov 13–19 | Paper spec; data download and audit; baseline; stacking model; comparison and gap analysis; report and runbook drafts; issues assigned | Mostly done. Still open: votes, second-member check of paper numbers (M1-2), superseded-plan cleanup (M1-6), course's data questions (M2-4) |
| 2 | Nov 20–26 | Team votes and decisions on D1–D19; a second member reproduces the results on their machine; wiki runbook tested; report sections rewritten by each member; data described the course's way | Not started |
| 3 | Nov 27–Dec 3 | Contribution table; board cleanup; slides; offline demo; timed dry run; final fresh-clone review | Not started |

## 7. Status so far

| Metric (binary, UNSW-NB15 test set) | Paper (Table 4) | Ours | Difference |
|---|---:|---:|---:|
| Accuracy | 0.94 | 0.8648 | −0.0752 |
| False alarm rate | 5.2% | 27.90% | +22.70 points |

Attack = positive class (D14); false alarm rate = FP/(FP+TN) (D15); AUC from the SVM decision function (D17); ours to 4 decimals, while the paper's values look truncated (D16). Paper values `paper-reported`; ours `measured (results/comparison/2026-11-15_table4/comparison.csv)`. Full table: `README.md` and `docs/REPORT.md` §6.

Under our proposed (not yet team-approved) choices D1–D19, the result is **not reproduced**:
- **Seeds:** six seeds give 0.8647–0.8662 (`measured (results/comparison/2026-11-15_table4/seed_spread.csv)`).
- **Preprocessing:** three alternatives give 0.8640–0.8652 (`measured (results/comparison/2026-11-15_table4/variants.csv)`).
- **Duplicate rows:** on the test rows not copied from training, accuracy is 0.8603 (`measured (results/comparison/2026-11-15_table4/comparison.csv, ours_test_unseen)`).
- **Cross-validation on the training file:** 0.9619 against the paper's 0.9285 (`measured (results/runs/2026-11-15_cv_train_stacking_seed42/summary_vs_table5.csv)` vs `paper-reported`, Table 5). Ours is optimistic because the training file has many duplicate rows.
- **Where the false alarms are:** 87.4% are normal test records with `sttl` = 254 (`measured (results/runs/2026-11-15_error_analysis_stacking_seed42/fp_by_sttl.csv)`). This is a concentration, not a tested cause.

How the paper reached its test result is not determined (`docs/REPORT.md` §7).

## 8. Risks and how we handle them

| Risk | Effect | Handling | Status |
|---|---|---|---|
| The paper leaves steps unstated (open questions S1–S14: preprocessing, encoding, scaling, stacking details, unstated settings) | Our pipeline may differ from theirs | Each choice logged as D1–D19; preprocessing choices D3–D5 tested for sensitivity | D3–D5 alternatives change accuracy little (0.8640–0.8652, `measured (results/comparison/2026-11-15_table4/variants.csv)`); D9, D10 and D17 not varied |
| The paper's own numbers are inconsistent: positive class (N1), truncated metrics (N2), unexplained 5.2% false alarm rate (N3), Table 6 on a 51,535-row subset (N4, `derived`) | Comparison isn't exactly like for like | Report our metrics with standard definitions; each inconsistency logged in `docs/DEVIATIONS.md` | Documented |
| RBF SVM may be slow on 175,341 rows | Schedule | Timed on samples first (`unverified`: scratch dry run, not saved) | Full run took 130 s; no subsampling needed |
| Results differ from the paper | Could be read as a failed project | The goal is an honest comparison; every gap gets a tested reason or "not determined" | Gap analysis done |
| Contribution evidence for each member not yet recorded | Checklist items 3, 6, 9, 11 and 15 need each member's own work | Issues assigned to each member with checkable tasks | Assigned 2026-11-17; all three members have voted (Issue #2) |
| Presentation date unknown | Late deliverables aren't accepted | Get the date this week and plan backwards | Open |

## 9. Scope and fallback

- **In scope:** the UNSW-NB15 binary result (Table 4), with the 10-class result (Table 6) as a secondary comparison.
- **Out of scope (proposed, D19):** the paper's UGR'16 results. That dataset is far larger (1,048,576 flows per attack type used, `paper-reported`, Table 2), and three weeks isn't enough. The report will say plainly that only the UNSW-NB15 part is reproduced.
- **Fallback:** if Dr. Parra rejects the target or the scope, the team records the reason and the alternative in Issue #1. The pipeline is config-driven, so a different metric or subset of this paper needs little new code.

## 10. Team and roles

Assignments were made on 2026-11-17 by the repo owner; members are to confirm or swap them on the issues.

| Member | Issues | Main responsibility |
|---|---|---|
| joromanii | #1, #3, #7, #8, #9 | Paper, proposal, environment, stacking model, comparison |
| elijahmart42 | #4, #5, #6, #12, #20 | Reproduce on own machine, lead team decisions, review baseline, test runbook, final review |
| Aponce0003 | #2, #10, #11, #13, #21, #22 | Votes and roster, report lead, evidence and contribution table, board cleanup, presentation, offline demo |

**Paper vote:** unanimous. All three members voted YES in [Issue #2](https://github.com/joromanii/HackEM-_-/issues/2) (Aponce0003 and joromanii on 2026-11-17, elijahmart42 on 2026-11-18) (checked on GitHub, 2026-11-19).

## 11. Readiness-checklist crosswalk

How each item on the CIS 3370 *Capstone Readiness Checklist* is met. Stories and statuses match `docs/USER_STORIES.md`.

| # | Checklist item | Where it's met | Issue | Stories | Status (2026-11-17) |
|---|---|---|---|---|---|
| 1 | Claim in one sentence | Top of `README.md`; §1 here | #1 | M1-1, M1-7 | Done |
| 2 | Paper's numbers recorded with citations | `docs/PAPER_METHOD.md` (Tables 1, 3, 4, 5, 6) | #1 | M1-2, M1-7, M5-10 | In progress: recorded; second-member check pending |
| 3 | A teammate gets the same row and column counts on a clean machine | `scripts/audit_unsw.py`; checksums in `results/unsw_audit/2026-11-15_audit/files.csv` | #4 | M1-9, M2-1 to M2-3, M2-5, M2-9, M5-6 | Script done; teammate run pending |
| 4 | Data described the course's way, with class balance | `docs/REPORT.md` §3 | #4, #10 | M2-2, M2-4, M5-1 | Blocked: class balance done; need the course's four questions |
| 5 | Baseline scored before the paper's method | `results/runs/2026-11-15_baseline_binary_seed42/`; `docs/REPORT.md` §6 | #6 | M2-7, M4-3 | Done |
| 6 | One documented command reproduces the headline on another machine | `scripts/run_models.py --task stacking`; `docs/wiki/Runbook.md` | #8, #12, #20 | M1-9, M2-5, M2-6, M2-8, M3-1 to M3-7, M5-6 | Command done; teammate run pending |
| 7 | Paper / ours / difference table, no empty cells | `README.md`; `results/comparison/2026-11-15_table4/` | #9 | M4-1 to M4-3, M5-1, M5-10 | Done |
| 8 | Every gap has a stated reason | `docs/REPORT.md` §7; `docs/DEVIATIONS.md` | #5, #9 | M2-6, M3-1, M4-2, M4-4 to M4-9, M5-1, M5-10 | Done; D1–D19 need team approval |
| 9 | Wiki runbook tested by a non-author | `docs/wiki/Runbook.md` (to copy to the wiki) | #20 | M5-2, M5-6 | Draft; not in wiki or tested yet |
| 10 | README is the front door | `README.md` (claim, result table, links) | #11, #13 | M1-6, M5-3 | README done; superseded-plan cleanup in progress (M1-6) |
| 11 | Contribution table supported by named records | Bottom of `README.md` | #11 | M1-4, M1-10, M1-12, M1-13, M5-4 | Partly done: assignments and story log in place; member rows not started |
| 12 | Project board clean | GitHub project board | #11, #13 | M1-6, M1-11, M1-13, M5-5 | Issues and milestones updated; board not checked |
| 13 | Dry run within the time limit | `docs/PRESENTATION.md` | #21 | M5-7 | Outline drafted; dry run not started |
| 14 | Offline demo fallback | Recording on the presentation machine | #22 | M5-8 | Not started |
| 15 | Each member knows their section and number | `docs/PRESENTATION.md` (presenter column) | #21 | M1-8, M1-12, M5-9 | Partly done: meeting held (reported), issues assigned; sections not chosen |

## 12. Instructor feedback

*To be filled in when Dr. Parra responds.* Record each comment, the date, and what changed as a result.

| Date | Feedback | Change made | Issue |
|---|---|---|---|
| | | | |

## References

- Rajagopal, S., Kundapur, P. P., & Hareesha, K. S. (2020). A Stacking Ensemble for Network Intrusion Detection Using Heterogeneous Datasets. *Security and Communication Networks*, 2020, 4586875. https://doi.org/10.1155/2020/4586875
- Moustafa, N., & Slay, J. (2015). UNSW-NB15: a comprehensive data set for network intrusion detection systems. *MilCIS 2015*, IEEE. (The dataset page lists four more papers to cite.)
