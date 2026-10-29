# IDS Capstone Report

> Planning template. The reproduction paper, target result, implementation, and reproduction measurements have not yet been selected or completed. Replace placeholders only when supported by evidence.

## 1. Overview and research question

- Research question: To be defined after paper selection.
- Objective: Reproduce one precisely identified IDS result and explain any gap.
- Current status: [open issues](https://github.com/joromanii/HackEM-_-/issues), [project board](https://github.com/users/joromanii/projects/1).

## 2. Paper selection and feasibility

| Field | Decision / evidence |
|---|---|
| Paper title and authors | To be selected |
| Venue and year | To be selected |
| DOI or stable URL | To be selected |
| Exact claim and table/figure/row | To be selected |
| Metric and published value | To be selected |
| Dataset/subset and label mapping | To be verified |
| Method and compute feasibility | To be assessed |
| Blockers and assumptions | To be recorded |
| Fallback paper/claim | To be recorded |
| Team vote | Record each explicit vote in issue #2 |

Do not mark the paper approved until the required unanimous vote is recorded.

## 3. Dataset and access evidence

The initial state reported by the project owner is CIC-IDS2017 MachineLearningCSV, 2,830,743 records, 15 labels, and 79 columns, with about 80.3% benign and 19.7% attack traffic. These are preliminary until re-counted from source files. Record source/version, retrieval date, file inventory, headers, row counts, label normalization, access instructions, and redistribution constraints. Keep raw data out of Git unless its terms and course requirements permit it.

## 4. Methodology and reproducible settings

Document the task and label mapping; input files and features; cleaning, missing/non-finite values, duplicates, encoding, and scaling; split unit, proportions, grouping/stratification, and leakage controls; algorithm, hyperparameters, training and evaluation protocol; Python/library versions, OS/hardware/runtime; fixed seeds, config paths, exact commands, and expected outputs.

## 5. Deviations from the paper

| Paper specification | Reproduction choice | Reason/evidence | Expected effect |
|---|---|---|---|
| To be completed after paper selection | — | — | — |

Separate confirmed deviations from unresolved interpretation choices.

## 6. Quantitative results

| Metric / target | Paper value | Reproduced value | Difference | Source page/table/row and notes |
|---|---:|---:|---:|---|
| To be completed after paper selection | — | — | — | — |

State rounding, averaging method, split, seed, and whether metrics are per-class or aggregate. Include confusion matrix and precision/recall/F1 where compatible with the target claim.

## 7. Gap analysis and limitations

Explain differences using recorded evidence. Distinguish verified causes from hypotheses; discuss imbalance, rare labels, data version, preprocessing, split design, random variation, compute limits, and unavailable paper details as relevant.

## 8. Clean-checkout reproduction instructions

1. Install the documented Python version and dependencies.
2. Obtain the dataset from its documented source; raw files are not expected in this repository.
3. Set the documented data path/configuration.
4. Run the inventory, training, and evaluation commands.
5. Compare generated output with linked evidence and reported values.

Add verified commands and outputs once the pipeline exists. Do not present a baseline as paper reproduction.

## 9. Evidence index

| Evidence | Path or link | What it verifies |
|---|---|---|
| Dataset inventory and label counts | To be added | File access and class distribution |
| Configuration and environment manifest | To be added | Reproducible settings |
| Run logs and saved metrics | To be added | Execution and measurements |
| Figures/tables | To be added | Results and comparison |
| Decisions and blockers | Issues #1–#3, #13 | Paper choice, vote, proposal, and scope reconciliation |

## 10. Contributions

Use the contribution table at the bottom of the repository README. Base points and percentages on completed work and agreed team rules, with issue/PR/commit evidence. Do not infer assignments or contributions.

## 11. References

Add the selected paper, dataset source, software documentation, and supplementary materials with stable links and access dates.
