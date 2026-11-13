# HACKEM-_- — IDS Capstone

## Project status

**Claim we are reproducing:** Rajagopal et al. (2020) report that a stacking ensemble (random forest, K-nearest neighbours and logistic regression, combined by a support vector machine) using 11 UNSW-NB15 features reaches **0.94 accuracy** (precision 0.96, recall 0.93, F1 0.95, AUC 0.99, false alarm rate 5.2%) when classifying normal vs attack traffic on the 82,332-record UNSW-NB15 test set (Table 4). These are paper-reported values, not our results.

**Our result:** not yet measured.

**Paper:** Smitha Rajagopal, Poornima Panduranga Kundapur, Katiganere Siddaramappa Hareesha, “A Stacking Ensemble for Network Intrusion Detection Using Heterogeneous Datasets,” *Security and Communication Networks*, 2020, article 4586875. [DOI: 10.1155/2020/4586875](https://doi.org/10.1155/2020/4586875). Spec, settings and open questions: [docs/PAPER_METHOD.md](docs/PAPER_METHOD.md). User stories: [docs/USER_STORIES.md](docs/USER_STORIES.md).

**Target changed on 2026-11-13.** The team moved from Kurniabudi et al. 2020 (CIC-IDS2017, Table 9) to this paper. Each member's vote on the new paper goes in [issue #2](https://github.com/joromanii/HackEM-_-/issues/2), and the reason for the change in [issue #1](https://github.com/joromanii/HackEM-_-/issues/1). Votes are pending.

Start with [open Issues](https://github.com/joromanii/HackEM-_-/issues), the [IDS_Capstone project board](https://github.com/users/joromanii/projects/1), the [report](docs/REPORT.md) and the [paper-method specification](docs/PAPER_METHOD.md).

## Dataset

**UNSW-NB15** training (175,341 records) and testing (82,332 records), per the paper's Table 1 (`paper-reported`). That these are the official partition files is `unverified` until the data audit. Not downloaded yet; the official source must be confirmed first. Raw data is never committed. Do not commit raw dataset files, virtual environments, credentials, or machine-specific paths.

**Earlier work (superseded):** a read-only audit of CIC-IDS2017 from the previous target is kept as a record in [docs/DATA_AUDIT.md](docs/DATA_AUDIT.md) and `results/inventory/`.

## Workflow

1. Verify the exact paper claim, citation, data match, feasibility, blockers, and fallback.
2. Record the reported team agreement and each member’s explicit vote in issue #2.
3. Audit the data, resolve label mapping/preprocessing, and document the paper's ambiguous split/CV protocol.
4. Pin environment versions, seeds, configuration, and clean-checkout commands.
5. Implement the approved paper method, log assumptions and deviations, then compare the target metrics quantitatively.
6. Explain differences using evidence, finish the report, and perform a clean-checkout review.

Five phase milestones are organized with dates intentionally unset until the course calendar is confirmed. No individual assignments or contributions are inferred. Use issues to record accepted owners, blockers, decisions, and evidence. Move project cards through Backlog, Ready, In progress, In review, and Done as work changes. Plan iterations when actual semester dates are known.

## Results and evidence

The published target values are listed above as paper-reported values, not as results from this project. No implementation or reproduction result is available yet. Add reproduced values, their difference, exact source row, settings, and evidence links to [docs/REPORT.md](docs/REPORT.md). Separate verified explanations from hypotheses.

## Individual Contribution Summary Table

Fill from completed issues, pull requests, commits, and agreed point allocation. Do not estimate contributions in advance.

| Member | GitHub username | Story points completed | Contribution % | Issue/PR evidence |
|---|---|---:|---:|---|
| To be completed | To be completed | — | — | — |
| **Team total** |  | **—** | **100%** |  |
