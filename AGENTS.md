# HackEM-_- agent rules
Read BRIEF.md first, then docs/PAPER_METHOD.md for the paper's method.
## Always
- Show a plan and wait for OK before editing more than one file.
- Never overwrite originals. Write new files or a new run folder. `~/Downloads/MachineLearningCVE/` is read-only.
- Cite the evidence behind every claim: paper table/section, file path, or results file.
- Label every number as `paper-reported`, `measured (results/...)`, or `unverified`. Flag assumptions.
- Log any ambiguity or deviation from the paper in docs/DEVIATIONS.md before acting on it.
- Fix seeds. Save config, package versions and runtime with every run. Select features by column name.

## Ask first
- Installing packages; git commit, push, or PR; any GitHub action (comment, vote, assign, close).
- Moving, renaming, or deleting files. Full-dataset runs expected to take over 10 minutes.

## Never
- Commit raw or processed data, or anything under data/.
- Fill a "Reproduction" value without a saved, re-runnable run.
- Tune settings toward the paper's numbers (99.86% / 0.999 / 0.003).
- Silently choose an interpretation of an unclear step in the paper.
- Vote, claim issues, or commit as or for a teammate.

## Stop and report
Counts differ from saved results · paper is ambiguous · results look too good (check leakage and duplicate rows) · memory errors · run over 30 min.
Before any PR: run the method-reviewer agent and include its report.
