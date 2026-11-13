# IDS Capstone Report

> Working reproduction plan for the team-selected paper. Values below are paper claims only. No paper-specific implementation or reproduced measurement is complete yet.

## 1. Overview and research question

- Research question: Can the Table 4 binary result of the stacking ensemble (RF, KNN and LR combined by an SVM, 11 features) be reproduced on the UNSW-NB15 test set, and what documented choices explain any gap?
- Objective: Reproduce one precisely identified IDS result and explain any gap.
- Status: Target changed to Rajagopal et al. 2020 on 2026-11-13. Team votes on the new paper are pending; each member's vote is tracked in [issue #2](https://github.com/joromanii/HackEM-_-/issues/2). See [open issues](https://github.com/joromanii/HackEM-_-/issues) and [project board](https://github.com/users/joromanii/projects/1).

## 2. Paper selection and feasibility

| Field | Decision / evidence |
|---|---|
| Paper | Rajagopal, Kundapur & Hareesha, “A Stacking Ensemble for Network Intrusion Detection Using Heterogeneous Datasets” |
| Venue and year | *Security and Communication Networks*, 2020, article 4586875 |
| DOI | [10.1155/2020/4586875](https://doi.org/10.1155/2020/4586875) |
| Exact claim | Table 4: binary (normal vs attack) stacking ensemble on the UNSW-NB15 test set |
| Paper-reported values | Accuracy 0.94; precision 0.96; recall 0.93; F1 0.95; AUC 0.99; FAR 5.2% |
| Dataset | UNSW-NB15 training (175,341) and testing (82,332) records, per paper Table 1 (`paper-reported`); that these are the official partition files is `unverified` until the data audit |
| Paper-described method | 11 features chosen by Information Gain and hashing; preprocessing and scaling; base models RF (100, gini), KNN (5, Minkowski), LR (L2); meta-model SVM (C=1.0, rbf) via cross-validated stacking |
| Known ambiguities | Preprocessing, `service` encoding and scaling methods not named; FAR formula unclear; reported metrics look truncated. See `docs/PAPER_METHOD.md` S1–S14 |
| Team decision | Target changed on 2026-11-13 from Kurniabudi et al. 2020 (CIC-IDS2017). Votes to be recorded in issue #2. |
| Scope | Proposed (S14, pending team decision): UNSW-NB15 only, leaving out the paper's UGR'16 results |
| Fallback | If the target proves infeasible or the instructor rejects it, record the fallback and reason in issue #1. |

Do not present paper-reported values as reproduced results. Compute our metrics from our own confusion matrix, state the positive class and FAR formula, and compare with the paper's (apparently truncated) values.

## 3. Dataset and access evidence

UNSW-NB15 training and testing files (Table 1 of the paper). To be added: source URL, download date, file checksums, row and class counts from the data audit, class balance, and access instructions. Keep raw data out of Git. The earlier CIC-IDS2017 audit (`docs/DATA_AUDIT.md`) belongs to the superseded target.

## 4. Methodology and reproducible settings

Record the team's decisions on the open questions S1–S14 in `docs/PAPER_METHOD.md` (data files, the 11 features, `service` encoding, missing values and outliers, scaling, stacking folds and inputs, unstated model settings, SVM runtime, positive class, FAR formula, rounding, the Table 6 evaluation set, duplicates, scope). Preserve our chosen protocol and deviations in versioned configuration. Document cleaning, non-finite values, duplicates, feature types, Python/library versions, OS/hardware/runtime, seeds, commands, and expected outputs. Where the paper is underspecified, label our decision as an assumption and explain its impact.

## 5. Deviations from the paper

| Paper specification | Reproduction choice | Reason/evidence | Expected effect |
|---|---|---|---|
| Missing values and outliers "compensated by making the distribution normal" | To be decided (S4) | Method not named | To be assessed |
| Feature scaling and `service` encoding not named | To be decided (S3, S5) | Methods not named | Can affect KNN, LR and SVM |
| Unstated model settings (SVM gamma, LR solver, stacking folds and inputs) | To be decided (S6, S7) | Only some settings in Table 3 | Can affect scores |
| FAR 5.2% matches no standard formula; metrics look truncated | Report standard definitions and both roundings (S10, S11) | Arithmetic in `docs/PAPER_METHOD.md` | Not directly comparable |
| UGR'16 results | Proposed out of scope (S14, pending team decision) | Time and dataset size | Only the UNSW-NB15 part would be reproduced |

Separate confirmed deviations from unresolved interpretation choices.

## 6. Quantitative results

| Metric | Paper value (Table 4, binary, UNSW-NB15 test set) | Reproduced value | Difference | Notes |
|---|---:|---:|---:|---|
| Accuracy | 0.94 | Pending | Pending | Counts give 0.946 (`derived`); paper likely truncated |
| Precision | 0.96 | Pending | Pending | Attack = positive (proposed, S9) |
| Recall | 0.93 | Pending | Pending | Counts give 0.938 (`derived`) |
| F1 | 0.95 | Pending | Pending | |
| AUC | 0.99 | Pending | Pending | State the scores used |
| FAR | 5.2% | Pending | Pending | Paper formula unknown |

Include class-aware precision/recall/F1 and a confusion matrix where compatible. State averaging method, split, and seed.

## 7. Gap analysis and limitations

Explain differences using evidence. Separate verified causes from hypotheses; discuss imbalance, rare labels, data version, preprocessing, split design, random variation, compute limits, and unavailable paper details as relevant.

## 8. Clean-checkout reproduction instructions

1. Install documented Python and dependencies.
2. Obtain the UNSW-NB15 training and testing files from the documented source; raw files are not expected in this repository.
3. Set the documented data path/configuration.
4. Run inventory, training, and evaluation commands.
5. Compare output with linked evidence and paper values.

Add verified commands once the pipeline exists. Do not present a baseline as paper reproduction.

## 9. Evidence index

| Evidence | Path/link | What it verifies |
|---|---|---|
| Dataset inventory/counts (UNSW-NB15) | To be added (Issue #4) | File access and class distribution |
| Superseded: CIC-IDS2017 audit | [`results/inventory/2026-11-02_audit/`](../results/inventory/2026-11-02_audit/), [DATA_AUDIT.md](DATA_AUDIT.md) | Record of the earlier target only |
| Config/environment | To be added | Reproducible settings |
| Run logs/metrics | To be added | Execution and measurements |
| Figures/tables | To be added | Results and comparison |
| Decisions/blockers | Issues #1–#3, #13 | Paper, votes, proposal, scope |

## 10. Contributions

Use the contribution table at the bottom of README. Base points and percentages on completed work and agreed team rules, with issue/PR/commit evidence.

## 11. References

- Rajagopal, S., Kundapur, P. P., & Hareesha, K. S. “A Stacking Ensemble for Network Intrusion Detection Using Heterogeneous Datasets.” *Security and Communication Networks*, 2020, 4586875. [DOI](https://doi.org/10.1155/2020/4586875)
- UNSW-NB15 dataset, Australian Centre for Cyber Security (paper §3). Official source URL to be confirmed.
