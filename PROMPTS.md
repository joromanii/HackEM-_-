# Starter prompts: HackEM-_-

Each prompt has the four parts: **Goal · Inputs · Rules · Output**. Paste into Claude Code from the repo root. Replace anything in [brackets].

---

## 1. Read-only project review (start here)
```
Goal: Tell me the current state of this reproduction and what to do first for M2.
Inputs: BRIEF.md, docs/PAPER_METHOD.md, the repo tree, and open issues (gh issue list --state open).
Rules: Read-only. Don't create, edit, move, or run anything that writes files. Don't touch GitHub.
Mark every number as paper-reported, measured (with file), or unverified.
Output: In chat only: 1) what exists vs. what's missing, 2) open questions from BRIEF.md that block M2,
3) the top 3 next steps with the issue each one belongs to.
```

## 2. Dataset audit (Issue #4)
```
Goal: Build a reproducible inventory of the CIC-IDS2017 MachineLearningCSV files.
Inputs: ~/Downloads/MachineLearningCVE/*.csv (read-only); ~/ids-capstone/results/dataset_label_counts.csv
for comparison; ~/ids-capstone/scripts/inspect_data.py as a reference only.
Rules: Show me the plan first. Never modify or copy the raw CSVs into the repo. Read in chunks to limit memory.
Report, don't fix: encoding problems in labels, Inf/NaN counts, exact duplicate rows, and whether the two
"Fwd Header Length" columns are identical. If counts differ from the saved CSV, stop and tell me.
Output: scripts/audit_inventory.py, results/inventory/ (per-file rows/columns, label counts,
duplicate and Inf/NaN counts, run metadata with package versions), and docs/DATA_AUDIT.md
summarizing findings with a link to each results file.
```

## 3. Pin the environment (Issue #7)
```
Goal: Make the project run the same way on any teammate's clean checkout.
Inputs: ~/ids-capstone/.venv (current packages), the scripts in this repo.
Rules: Propose before installing anything. Target Python 3.11 in a project venv; don't change the system Python
or the old ~/ids-capstone venv. Pin exact versions. One seed value in one config file.
Output: requirements.txt, configs/run.yaml (seed, data path, output path), and a "Setup and run" section
in README.md with copy-paste steps. List anything you couldn't pin.
```

## 4. Preprocessing and split spec (Issue #5)
```
Goal: Write down the preprocessing and leakage-safe split BEFORE any training.
Inputs: docs/PAPER_METHOD.md, docs/DATA_AUDIT.md, the paper PDF linked in PAPER_METHOD.md.
Rules: Write only docs. For each unclear paper step (20% sample, 70/30 vs 10-fold CV, duplicate rows,
Inf/NaN handling, label grouping from Table 3, which Fwd Header Length to drop), quote or cite the paper section,
list 2–3 options with trade-offs, and leave the choice as "TEAM DECISION NEEDED". Don't pick for us.
Information Gain must be computed on training data only.
Output: docs/SPLIT_SPEC.md and new entries in docs/DEVIATIONS.md (create it if missing).
```

## 5. Baseline pipeline (Issue #6)
```
Goal: A first end-to-end Random Forest run on the 22 paper features, using the split the team approved.
Inputs: docs/SPLIT_SPEC.md (approved choices only), configs/run.yaml, the 22-feature list in docs/PAPER_METHOD.md.
Rules: Show the plan first. Select features by column name and stop if any name is missing.
Do a small dry run on a sample before the full data, and ask before a full run expected to exceed 10 minutes.
Don't tune toward the paper's numbers. If accuracy looks too good, check for leakage and duplicates and report.
Output: src/ or scripts/ code, results/runs/<date>_<short-name>/ with config, package versions, runtime,
confusion matrix, per-class precision/recall/FPR, and a short README.md for that run. Never overwrite a past run.
```

## 6. Independent method review (before any PR)
```
Goal: Get an independent check that our method and numbers match the paper and our saved results.
Inputs: The current branch's diff (git diff main...HEAD), docs/PAPER_METHOD.md, docs/DEVIATIONS.md, results/.
Rules: Use the method-reviewer agent. It reads only and does not fix anything.
Output: The reviewer's pass/fail report, pasted into the PR description draft. Don't open the PR; show me the draft.
```
