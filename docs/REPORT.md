# IDS Capstone Report

> Working reproduction plan for the team-selected paper. Values below are paper claims only. No paper-specific implementation or reproduced measurement is complete yet.

## 1. Overview and research question

- Research question: Can the Table 9 Random Forest result be reproduced with the described CICIDS-2017 preprocessing and 22 Information Gain features, and what documented protocol choices explain any gap?
- Objective: Reproduce one precisely identified IDS result and explain any gap.
- Status: Repository owner reports teammate agreement. Individual explicit votes are tracked in [issue #2](https://github.com/joromanii/HackEM-_-/issues/2). See [open issues](https://github.com/joromanii/HackEM-_-/issues) and [project board](https://github.com/users/joromanii/projects/1).

## 2. Paper selection and feasibility

| Field | Decision / evidence |
|---|---|
| Paper | Kurniabudi et al., “CICIDS-2017 Dataset Feature Analysis With Information Gain for Anomaly Detection” |
| Venue and year | *IEEE Access*, vol. 8, 2020, pp. 132911–132921 |
| DOI | [10.1109/ACCESS.2020.3009843](https://doi.org/10.1109/ACCESS.2020.3009843) |
| Exact claim | Table 9, Random Forest, 22 selected features |
| Paper-reported values | Accuracy 99.86%; recall 0.999; false-positive rate 0.003; precision NaN |
| Dataset | CICIDS-2017 MachineLearningCSV; owner reports this collection is available locally |
| Paper-described method | 20% of MachineLearningCSV; redundant-feature removal; seven traffic categories; Information Gain ranking and 22 features above weight 0.4; Random Forest; 10-fold cross-validation is described |
| Protocol ambiguity | Paper also states 70/30 train/test. Exact subset selection and model/software settings need verification. Resolve before claiming a faithful comparison. |
| Team decision | Owner reports teammates agree. Individual explicit votes still need to be recorded in issue #2. |
| Feasibility and blockers | Dataset family is available to the team; large-data runtime and exact protocol remain to be checked. Clarify 20% sample selection and 70/30 vs 10-fold evaluation. |
| Fallback | If faithful implementation proves infeasible or the instructor rejects the target, record the fallback and reason in issue #1. |

Do not present paper-reported values as reproduced results. Table 9 precision of NaN is not a valid computed score; calculate precision from our predictions and report class-aware metrics.

## 3. Dataset and access evidence

The owner reports CIC-IDS2017 MachineLearningCSV, 2,830,743 records, 15 labels, and 79 columns, about 80.3% benign and 19.7% attack. Preliminary until re-counted from source files. Record source/version, retrieval date, inventory, headers, row counts, label normalization, access instructions, and redistribution constraints. Keep raw data out of Git unless permitted.

## 4. Methodology and reproducible settings

Record the seven-category label mapping, redundant-feature handling, exact 20% sample selection, Information Gain settings, mapping of published feature IDs to names, Random Forest parameters, and whether the reported number uses a 70/30 holdout or 10-fold evaluation. Preserve our chosen protocol and deviations in versioned configuration. Document cleaning, non-finite values, duplicates, feature types, Python/library versions, OS/hardware/runtime, seeds, commands, and expected outputs. Where the paper is underspecified, label our decision as an assumption and explain its impact.

## 5. Deviations from the paper

| Paper specification | Reproduction choice | Reason/evidence | Expected effect |
|---|---|---|---|
| 20% subset selection unclear | To be determined and fixed by seed | Record exact rule after source/data inspection | To be assessed |
| Both 70/30 split and 10-fold CV mentioned | Resolve before comparison | Record source text and interpretation | May limit comparability |
| RF/software parameters not fully pinned | Verify or explicitly assume | Record package version and parameters | Can affect scores |
| Table 9 precision is NaN | Recompute from predictions/confusion counts | NaN is not a valid numeric precision | Not directly comparable |

Separate confirmed deviations from unresolved interpretation choices.

## 6. Quantitative results

| Metric | Paper value (Table 9, RF, 22 features) | Reproduced value | Difference | Notes |
|---|---:|---:|---:|---|
| Accuracy | 99.86% | Pending | Pending | State split/fold and rounding |
| Recall | 0.999 | Pending | Pending | Verify averaging convention |
| False-positive rate | 0.003 | Pending | Pending | Verify class definition |
| Precision | NaN | Pending | Pending | Recompute; do not use NaN as score |

Include class-aware precision/recall/F1 and a confusion matrix where compatible. State averaging method, split, and seed.

## 7. Gap analysis and limitations

Explain differences using evidence. Separate verified causes from hypotheses; discuss imbalance, rare labels, data version, preprocessing, split design, random variation, compute limits, and unavailable paper details as relevant.

## 8. Clean-checkout reproduction instructions

1. Install documented Python and dependencies.
2. Obtain CICIDS-2017 from its documented source; raw files are not expected in this repository.
3. Set the documented data path/configuration.
4. Run inventory, training, and evaluation commands.
5. Compare output with linked evidence and paper values.

Add verified commands once the pipeline exists. Do not present a baseline as paper reproduction.

## 9. Evidence index

| Evidence | Path/link | What it verifies |
|---|---|---|
| Dataset inventory/counts | To be added | File access and class distribution |
| Config/environment | To be added | Reproducible settings |
| Run logs/metrics | To be added | Execution and measurements |
| Figures/tables | To be added | Results and comparison |
| Decisions/blockers | Issues #1–#3, #13 | Paper, votes, proposal, scope |

## 10. Contributions

Use the contribution table at the bottom of README. Base points and percentages on completed work and agreed team rules, with issue/PR/commit evidence.

## 11. References

- Kurniabudi et al. “CICIDS-2017 Dataset Feature Analysis With Information Gain for Anomaly Detection.” *IEEE Access*, 8 (2020), 132911–132921. [DOI](https://doi.org/10.1109/ACCESS.2020.3009843)
- Canadian Institute for Cybersecurity. [CIC-IDS2017 dataset](https://www.unb.ca/cic/datasets/ids-2017.html)
