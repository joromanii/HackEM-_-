# HACKEM-_- — IDS Capstone

## Project status

**Claim we are reproducing:** Rajagopal et al. (2020) report that a stacking ensemble (random forest, K-nearest neighbours and logistic regression, combined by a support vector machine) using 11 UNSW-NB15 features reaches **0.94 accuracy** (precision 0.96, recall 0.93, F1 0.95, AUC 0.99, false alarm rate 5.2%) when classifying normal vs attack traffic on the 82,332-record UNSW-NB15 test set (Table 4). These are paper-reported values, not our results.

**Our result:** **not reproduced.** Built as the paper describes, our stacking ensemble reaches **0.8648 accuracy** on the same test set (paper 0.94), with a false alarm rate of **27.9%** (paper 5.2%): `measured (results/comparison/2026-11-15_table4/comparison.md)`. Seed variation, the three alternative preprocessing choices we tested, and duplicate rows don't account for the gap. In 10-fold cross-validation on the training file our model scores 0.9619 (`measured (results/runs/2026-11-15_cv_train_stacking_seed42/summary_vs_table5.csv)`; optimistic, as the file has many duplicate rows) against the paper's 0.9285 (`paper-reported`, Table 5). 87.4% of our false alarms are normal test records with `sttl` = 254, a value that is about 90% attack traffic in the training file (`derived` from `results/runs/2026-11-15_sttl_profile/`). How the paper reached its test result is not determined. Full analysis: [docs/REPORT.md](docs/REPORT.md) §7.

| Metric (binary, UNSW-NB15 test set) | Paper (Table 4) | Ours | Difference |
|---|---:|---:|---:|
| Accuracy | 0.94 | 0.8648 | −0.0752 |
| Precision | 0.96 | 0.8118 | −0.1482 |
| Recall | 0.93 | 0.9821 | +0.0521 |
| F1 | 0.95 | 0.8889 | −0.0611 |
| AUC | 0.99 | 0.9248 | −0.0652 |
| FAR | 5.2% | 27.90% | +22.70 points |

Attack = positive class (D14); FAR = FP/(FP+TN) (D15); AUC from the SVM decision function (D17); ours rounded to 4 decimals, while the paper's values look truncated (D16).

Reproduce it: [runbook](docs/wiki/Runbook.md). Method choices not stated in the paper are **proposed, pending team approval** in [docs/DEVIATIONS.md](docs/DEVIATIONS.md).

**Paper:** Smitha Rajagopal, Poornima Panduranga Kundapur, Katiganere Siddaramappa Hareesha, “A Stacking Ensemble for Network Intrusion Detection Using Heterogeneous Datasets,” *Security and Communication Networks*, 2020, article 4586875. [DOI: 10.1155/2020/4586875](https://doi.org/10.1155/2020/4586875). Proposal: [docs/PROPOSAL.md](docs/PROPOSAL.md). Spec, settings and open questions: [docs/PAPER_METHOD.md](docs/PAPER_METHOD.md). User stories: [docs/USER_STORIES.md](docs/USER_STORIES.md).

**Target changed on 2026-11-13.** The repo owner moved the target from Kurniabudi et al. 2020 (CIC-IDS2017, Table 9) to this paper. Each member's vote on the new paper goes in [issue #2](https://github.com/joromanii/HackEM-_-/issues/2), and the reason for the change in [issue #1](https://github.com/joromanii/HackEM-_-/issues/1). **The vote is unanimous:** all three members voted YES (Aponce0003 and joromanii on 2026-11-17, elijahmart42 on 2026-11-18).

Start with [open Issues](https://github.com/joromanii/HackEM-_-/issues), the [IDS_Capstone project board](https://github.com/users/joromanii/projects/1), the [report](docs/REPORT.md) and the [paper-method specification](docs/PAPER_METHOD.md).

## Dataset

**UNSW-NB15** official partition files `UNSW_NB15_training-set.csv` (175,341 records) and `UNSW_NB15_testing-set.csv` (82,332 records), from the [official UNSW-NB15 page](https://research.unsw.edu.au/projects/unsw-nb15-dataset). Every class count matches the paper's Table 1: `measured (results/unsw_audit/2026-11-15_audit/class_counts_vs_table1.csv)`. Download steps: [runbook](docs/wiki/Runbook.md) §3. Raw data is never committed. Do not commit raw dataset files, virtual environments, credentials, or machine-specific paths.

**Earlier work (superseded):** a read-only audit of CIC-IDS2017 from the previous target is kept as a record in [docs/DATA_AUDIT.md](docs/DATA_AUDIT.md) and `results/inventory/`.

## Setup and run

Full step-by-step instructions: [docs/wiki/Runbook.md](docs/wiki/Runbook.md). Short version, tested on macOS (Apple silicon) with Homebrew:

```bash
brew install python@3.11
python3.11 -m venv .venv
.venv/bin/pip install -r requirements-lock.txt
.venv/bin/python scripts/reproduce.py   # raw data -> audit -> baseline -> stacking -> comparison, about 2.5 minutes
```

`reproduce.py` writes everything to `results/reproduce/<date>_<time>/` and ends with **REPRODUCED** if your headline metrics are identical to ours. Figures for the report and slides: [`results/figures/2026-11-19_figures/figures.md`](results/figures/2026-11-19_figures/figures.md).

Put the UNSW-NB15 training and testing CSVs in `~/Downloads/UNSW-NB15/` first (runbook §3), or change `data_dir` in [configs/run.toml](configs/run.toml). Pinned versions: [requirements.txt](requirements.txt) (direct) and [requirements-lock.txt](requirements-lock.txt) (full `pip freeze`).

**Not pinned:** the macOS version, the Homebrew Python build and CPU type; each run records them in its `run_meta.json`. The Python 3.11 setup reproduced every CSV of the earlier (superseded) CIC-IDS2017 audit byte for byte: measured ([`results/inventory/2026-11-04_audit/compare_to_2026-11-02_audit.csv`](results/inventory/2026-11-04_audit/compare_to_2026-11-02_audit.csv)).

## Workflow

1. Verify the exact paper claim, citation, data match, feasibility, blockers, and fallback.
2. Record the reported team agreement and each member’s explicit vote in issue #2.
3. Audit the data, resolve label mapping/preprocessing, and document the paper's ambiguous split/CV protocol.
4. Pin environment versions, seeds, configuration, and clean-checkout commands.
5. Implement the approved paper method, log assumptions and deviations, then compare the target metrics quantitatively.
6. Explain differences using evidence, finish the report, and perform a clean-checkout review.

Five phase milestones are organized with dates intentionally unset until the course calendar is confirmed. Issue owners were assigned on 2026-11-17 (see each issue and `docs/USER_STORIES.md` M1-12); contributions are never inferred. Use issues to record accepted owners, blockers, decisions, and evidence. Move project cards through Backlog, Ready, In progress, In review, and Done as work changes. Plan iterations when actual semester dates are known.

## Results and evidence

Paper values are `paper-reported` (Table 4). Our values are `measured` from saved runs listed in the [report's evidence index](docs/REPORT.md#9-evidence-index). Explanations are separated into what was tested and what remains undetermined (report §7).

## Individual Contribution Summary Table

Fill from completed issues, pull requests, commits, and agreed point allocation. Do not estimate contributions in advance.

| Member | GitHub username | Story points completed | Contribution % | Issue/PR evidence |
|---|---|---:|---:|---|
| To be completed | To be completed | — | — | — |
| **Team total** |  | **—** | **100%** |  |
