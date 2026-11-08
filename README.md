# HACKEM-_- — IDS Capstone

## Project status

The team has agreed to use the following working paper and reproduction target. The repository owner reports teammate agreement; record each teammate’s explicit vote in [issue #2](https://github.com/joromanii/HackEM-_-/issues/2) before marking the rubric's unanimous-commit condition complete. The implementation and reproduction measurements are not complete.

**Paper:** Kurniabudi et al., “CICIDS-2017 Dataset Feature Analysis With Information Gain for Anomaly Detection,” *IEEE Access*, vol. 8 (2020), pp. 132911–132921. [DOI: 10.1109/ACCESS.2020.3009843](https://doi.org/10.1109/ACCESS.2020.3009843).

**Target:** Table 9, Random Forest with the 22-feature Information Gain subset (>=0.4): reported accuracy 99.86%, recall 0.999, false-positive rate 0.003, and precision NaN. The paper says it uses 20% of MachineLearningCSV, removes one duplicated Fwd Header Length feature, relabels attack classes, and describes both a 70/30 split and 10-fold evaluation. It does not clearly explain how those two evaluation descriptions compose. The paper attributes NaN values to rare classes missing from folds and reports that RF does not detect Infiltration for this feature subset. These are paper-reported values, not our results. See the [paper-method specification](docs/PAPER_METHOD.md) for the 22-feature list and open protocol questions.

Start with [open Issues](https://github.com/joromanii/HackEM-_-/issues), the [IDS_Capstone project board](https://github.com/users/joromanii/projects/1), the [report](docs/REPORT.md), the [paper-method specification](docs/PAPER_METHOD.md), and [paper-selection issue #1](https://github.com/joromanii/HackEM-_-/issues/1).

## Dataset starting point

The project owner reports CIC-IDS2017 MachineLearningCSV locally available and an initial count of 2,830,743 records, 15 labels, and 79 columns, with about 80.3% benign and 19.7% attack traffic. The Issue #4 audit reran these counts from the source files and they match: measured (`results/inventory/2026-11-02_audit/`). See [docs/DATA_AUDIT.md](docs/DATA_AUDIT.md) for the full inventory, including duplicate rows and NaN/Inf values. Do not commit raw dataset files, virtual environments, credentials, or machine-specific paths.

## Setup and run

Tested on macOS (Apple silicon) with Homebrew only; no Linux or Windows steps yet. Pinned versions: [requirements.txt](requirements.txt) (direct) and [requirements-lock.txt](requirements-lock.txt) (full `pip freeze`).

1. Install Python 3.11 (we used 3.11.18 from Homebrew; other 3.11.x versions are untested):

   ```bash
   brew install python@3.11
   ```

2. From the repo root, create the project venv and install the pinned packages:

   ```bash
   python3.11 -m venv .venv
   .venv/bin/pip install -r requirements-lock.txt
   ```

3. Put the CIC-IDS2017 MachineLearningCSV files in `~/Downloads/MachineLearningCVE/`, or change `data_dir` in [configs/run.toml](configs/run.toml). The raw files are never copied into the repo.

4. Run the data audit (14.6 s and 16.8 s on our machine: measured, `run_meta.json` in each run folder). It writes a new folder `results/inventory/<today>_audit/` and refuses to overwrite one that exists:

   ```bash
   .venv/bin/python scripts/audit_inventory.py
   ```

5. Check your download matches ours: the `sha256` column of your `files.csv` should equal [results/inventory/2026-11-02_audit/files.csv](results/inventory/2026-11-02_audit/files.csv). The comparison with the old label counts needs `~/ids-capstone/results/dataset_label_counts.csv`, which only the repo owner has. Without it the audit skips `label_count_comparison.csv`, so your run folder won't match ours file for file.

**Config:** [configs/run.toml](configs/run.toml) holds the one project seed (`42`, not yet used: the audit has no randomness) and the data and results paths. It is TOML rather than the YAML suggested in `PROMPTS.md`, because Python 3.11 reads TOML with no extra package.

**Not pinned:** the macOS version, the Homebrew Python build, and CPU type. Each run records them in its `run_meta.json`. The Python 3.11 setup reproduced every CSV of the first audit (Python 3.9.6) byte for byte: measured ([`results/inventory/2026-11-04_audit/compare_to_2026-11-02_audit.csv`](results/inventory/2026-11-04_audit/compare_to_2026-11-02_audit.csv)). Both runs used the same pandas, numpy and scikit-learn versions, so this tests the Python change only.

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
