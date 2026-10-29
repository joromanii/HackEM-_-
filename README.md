# HACKEM-_- — IDS Capstone

## Project status

The team has agreed to use the following working paper and reproduction target. The repository owner reports teammate agreement; record each teammate’s explicit vote in [issue #2](https://github.com/joromanii/HackEM-_-/issues/2) before marking the rubric's unanimous-commit condition complete. The implementation and reproduction measurements are not complete.

**Paper:** Kurniabudi et al., “CICIDS-2017 Dataset Feature Analysis With Information Gain for Anomaly Detection,” *IEEE Access*, vol. 8 (2020), pp. 132911–132921. [DOI: 10.1109/ACCESS.2020.3009843](https://doi.org/10.1109/ACCESS.2020.3009843).

**Target:** Table 9, Random Forest with the 22-feature Information Gain subset (>=0.4): reported accuracy 99.86%, recall 0.999, false-positive rate 0.003, and precision NaN. The paper says it uses 20% of MachineLearningCSV, removes one duplicated Fwd Header Length feature, relabels attack classes, and describes both a 70/30 split and 10-fold evaluation. It does not clearly explain how those two evaluation descriptions compose. The paper attributes NaN values to rare classes missing from folds and reports that RF does not detect Infiltration for this feature subset. These are paper-reported values, not our results. See the [paper-method specification](docs/PAPER_METHOD.md) for the 22-feature list and open protocol questions.

Start with [open Issues](https://github.com/joromanii/HackEM-_-/issues), the [IDS_Capstone project board](https://github.com/users/joromanii/projects/1), the [report](docs/REPORT.md), the [paper-method specification](docs/PAPER_METHOD.md), and [paper-selection issue #1](https://github.com/joromanii/HackEM-_-/issues/1).

## Dataset starting point

The project owner reports CIC-IDS2017 MachineLearningCSV locally available and an initial count of 2,830,743 records, 15 labels, and 79 columns, with about 80.3% benign and 19.7% attack traffic. These are preliminary reported values; recheck them from the source files and preserve the counting script and inventory as evidence. Do not commit raw dataset files, virtual environments, credentials, or machine-specific paths.

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
