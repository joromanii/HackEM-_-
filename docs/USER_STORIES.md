# User stories by milestone

User stories for the current plan (milestones **M1–M5** on GitHub). Each story names its GitHub issue and the item it covers in the instructor's *Capstone Readiness Checklist* (CIS 3370), numbered 1–15 in the order the checklist lists them.

**Format:** *As a [role], I want [something], so that [benefit].* Each story has acceptance criteria that can be checked against a file, run or issue.

**Roles used**
- **Researcher**: a team member building or running the reproduction.
- **Reviewer**: a team member checking someone else's work.
- **Instructor**: Dr. Parra, grading against the readiness checklist.
- **Newcomer**: someone opening the repo or wiki for the first time.

**Status** is as of 2026-11-10: Done · In review (PR open) · In progress · Not started · Blocked.

**Who does what:** stories marked *Team* need every member, or must be done by someone other than the author (for example, testing a runbook you didn't write). Owners are chosen by the team and recorded on the issue, never filled in here.

> The four older milestones (*Proposal approved…*, *Environment built…*, *Defenses implemented…*, *Documentation and presentation*) describe the earlier KDD plan. Issue #13 is for deciding whether to close or rename them, so they have no stories here.

---

## M1 — Paper selection and proposal

**Goal:** the team agrees on one paper and one exact claim, and the proposal maps the rubric to evidence.

| ID | User story | Acceptance criteria | Issue | Checklist | Status |
|---|---|---|---|---|---|
| M1-1 | As the **instructor**, I want the claim stated in one sentence, so that I know exactly what number the team is chasing and on what data. | One sentence at the top of `README.md` naming the paper, Table 9, Random Forest with 22 features, accuracy 99.86%, and CIC-IDS2017 MachineLearningCSV. Someone outside the team can repeat it without asking a question. | #1 | 1 | In progress |
| M1-2 | As a **researcher**, I want the paper's own numbers recorded with citations, so that every comparison uses the right target. | `docs/PAPER_METHOD.md` lists every target number with its table and row. A second team member has checked the hand-copied table numbers against the paper. | #1 | 2 | In progress (second check needed) |
| M1-3 | As a **team** member, I want every member's vote on the paper recorded, so that our choice is unanimous and visible. | Each member posts their own vote in Issue #2. Nobody's vote is entered for them. | #2 | — | Not started (*Team*) |
| M1-4 | As the **team**, I want our roster, GitHub usernames, availability and deadlines in one place, so that work can be planned and credited. | Issue #2 lists each member's name and GitHub username (posted by that member), the presentation date and the deliverable deadline. | #2 | 11 | Not started (*Team*) |
| M1-5 | As the **instructor**, I want a proposal that maps each rubric line to an issue or report section, so that I can see how the team plans to meet it. | A proposal document covers the citation, claim, data access, feasibility, risks and fallback, plus a table mapping all 15 checklist items to issues or files. | #3 | All | Not started |
| M1-6 | As a **newcomer**, I want the old KDD milestones resolved, so that the board doesn't show two different projects. | The legacy milestones are closed or renamed with a note saying why. README and board links are consistent. | #13 | 12 | In progress |

## M2 — Data audit and reproducible baseline

**Goal:** the data is verified, the environment is pinned, the preprocessing and split are decided before training, and a simple baseline runs.

| ID | User story | Acceptance criteria | Issue | Checklist | Status |
|---|---|---|---|---|---|
| M2-1 | As a **researcher**, I want a verified inventory of the dataset, so that the paper's method can be matched to the data we actually have. | `scripts/audit_inventory.py` and `results/inventory/2026-11-02_audit/` record rows, columns, labels, duplicates and NaN/Inf. `docs/DATA_AUDIT.md` summarizes them. | #4 | 3, 4 | Done (PR #15) |
| M2-2 | As a **reviewer**, I want to run the data audit on my own machine and get the same counts, so that we know the data loading is reproducible. | A team member other than the author runs the audit following the README. Their `files.csv` checksums and row counts match the committed run, and they report the result in Issue #4. | #4 | 3 | Not started (*Team*) |
| M2-3 | As the **instructor**, I want the data described the way the course describes data, so that the report answers the course's standard questions. | The report answers the course's first four data questions and gives the class balance, each with the code or results file that produced it. | #4, #10 | 4 | Blocked (need the course's four questions) |
| M2-4 | As a **future reviewer**, I want pinned Python and package versions and one config file, so that the project runs the same on any machine. | `requirements.txt`, `requirements-lock.txt` and `configs/run.toml` exist. The audit re-run under the pinned environment matches the first run byte for byte. | #7 | 3, 6 | In review (PR #16) |
| M2-5 | As a **researcher**, I want the preprocessing and split written down before training, so that no choice is made after seeing results. | `docs/SPLIT_SPEC.md` gives options for every unclear step. `docs/DEVIATIONS.md` logs each one. | #5 | 8 | In review (PR #17) |
| M2-6 | As the **team**, I want each open decision (D1–D16) made and recorded, so that the baseline and method can be built. | Each row in `docs/DEVIATIONS.md` is marked Decided, with the choice, a link to where the team agreed, and the date. | #5 | 5–8 | Not started (*Team*) |
| M2-7 | As a **researcher**, I want a do-nothing baseline and a simple model scored on the same split as the paper's method, so that we know what the paper's method adds. | One command produces a majority-class score and a simple-model score on the agreed split. A run folder holds the config, seed, versions, runtime, confusion matrix and per-class metrics. The output is not called a reproduction. | #6 | 5 | Blocked by M2-6 |

## M3 — Faithful paper method

**Goal:** the paper's method (Information Gain feature selection plus a Random Forest on 22 features) runs end to end from raw data with one command.

| ID | User story | Acceptance criteria | Issue | Checklist | Status |
|---|---|---|---|---|---|
| M3-1 | As a **researcher**, I want the team's decisions turned into one config file, so that every run uses the same settings. | Sample, split, cleaning, label mapping, Information Gain and Random Forest settings live in versioned config. Each setting points to its row in `DEVIATIONS.md`. | #8 | 6 | Not started |
| M3-2 | As a **researcher**, I want Information Gain computed on the training data only, so that the test data can't leak into feature selection. | The code fits feature ranking on the training part only. A test or check confirms the test rows are never used. The ranking is saved and compared with paper Table 5. | #8 | 6, 8 | Not started |
| M3-3 | As a **researcher**, I want the 22 features selected by column name, so that a column shifting position can't select the wrong feature. | The code selects features by name and stops with an error if any name is missing. The choice of which `Fwd Header Length` column to keep is logged. | #8 | 6 | Not started |
| M3-4 | As a **reviewer**, I want one documented command that goes from raw data to the headline number, so that I can rerun it on my machine. | One command in the README and wiki produces the headline result. A team member who didn't write the code runs it on their own machine and gets the same numbers. | #8, #12 | 6 | Not started (*Team*) |
| M3-5 | As a **reviewer**, I want every method PR reviewed against the paper, so that mistakes are caught before results are reported. | The method-reviewer report is in each PR, and at least one team member approves each PR. | #8 | 6 | Not started (*Team*) |

## M4 — Evaluation and gap analysis

**Goal:** our numbers sit beside the paper's, and every gap has a stated reason.

| ID | User story | Acceptance criteria | Issue | Checklist | Status |
|---|---|---|---|---|---|
| M4-1 | As the **instructor**, I want one table showing what the paper reported, what we got, and the difference, so that I can judge the reproduction at a glance. | A table with the columns Paper, Ours and Difference covers accuracy, recall, precision and FPR, with no empty cells. Each of our numbers links to its results file. | #9 | 7 | Not started |
| M4-2 | As a **reviewer**, I want each metric's definition next to the number, so that the paper's values and ours are compared like for like. | The averaging method (weighted or macro) and the FPR definition are stated beside the table. The paper's precision "NaN" is explained, and our precision is computed from the confusion matrix. | #9 | 7 | Not started |
| M4-3 | As a **researcher**, I want per-class results and a confusion matrix, so that the rare classes aren't hidden behind a high overall accuracy. | Per-class TPR, FPR, precision and recall, plus the confusion matrix, for the baseline and the paper's method. | #9 | 7, 8 | Not started |
| M4-4 | As the **instructor**, I want every gap explained or plainly marked unexplained, so that the conclusions don't claim more than the evidence shows. | For each difference larger than random variation, the report names a cause (for example duplicates, split, tool or settings) or says no cause was found. Run-to-run variation is measured across seeds. | #9 | 8 | Not started |
| M4-5 | As a **researcher**, I want to check how much the open choices move the results, so that we know which deviations matter. | Sensitivity runs for the main choices the team flagged (for example duplicates kept vs removed, or cross-validation vs holdout), each saved as its own run. | #9 | 8 | Not started |

## M5 — Report, evidence, presentation and final review

**Goal:** a complete report, wiki runbook, clean README and board, an accurate contribution table, and a rehearsed presentation.

| ID | User story | Acceptance criteria | Issue | Checklist | Status |
|---|---|---|---|---|---|
| M5-1 | As the **instructor**, I want a report that explains the method, the deviations, the results and the gaps, so that I can grade the reproduction from saved evidence. | `docs/REPORT.md` covers data, preprocessing, split, training, versions, seeds, the comparison table and the gap analysis. Every number links to a results file. Sections are split among members. | #10 | 4, 7, 8 | Not started (*Team*) |
| M5-2 | As a **newcomer**, I want a wiki runbook, so that I can set up and run the project without asking anyone. | The wiki covers setup, getting the data, running the audit, baseline and method, and where the results go. A team member who didn't write it follows it start to finish and records where they got stuck. | #10, #12 | 9 | Not started (*Team*) |
| M5-3 | As a **newcomer**, I want the README to show the result within a minute, so that I know what the project found right away. | The top of the README has the claim, our headline number beside the paper's, status, and links to the report and wiki. | #11 | 10 | Not started |
| M5-4 | As the **team**, I want an accurate contribution table, so that each member is credited for their real work. | Every row in the README's Individual Contribution Summary Table is backed by commits, issues, PRs or documents carrying that person's name. Points and percentages are agreed by the team. | #11 | 11 | Not started (*Team*) |
| M5-5 | As the **instructor**, I want a clean project board, so that I can see what was done, what's in progress and what was dropped. | Every card is closed, in progress with a reason, or dropped with a note. | #11 | 12 | Not started |
| M5-6 | As a **reviewer**, I want a final check from a fresh copy of the repo, so that we submit only what actually works. | Someone reruns the pipeline from a clean clone, checks every reported number against its results file, checks the links, and records what passed and what is unverified. | #12 | 3, 6, 9 | Not started (*Team*) |
| M5-7 | As the **team**, I want a timed dry run of the presentation, so that we finish within the limit without cutting the results. | At least one full run-through finishes inside the time limit with the results section intact, and the time is recorded. | — (new issue) | 13 | Not started (*Team*) |
| M5-8 | As a **presenter**, I want a demo fallback that works offline, so that a network or laptop problem doesn't stop the demo. | A recorded video or screenshots of the pipeline running play from the presentation machine with no network. | — (new issue) | 14 | Not started |
| M5-9 | As each **team member**, I want to know my presentation section and the one number I explain, so that everyone presents confidently. | A list maps each member to a section and a number, confirmed by each member in the dry run. | — (new issue) | 15 | Not started (*Team*) |

---

## Checklist coverage

| Checklist item | Stories |
|---|---|
| 1 Claim in one sentence | M1-1 |
| 2 Paper's numbers recorded | M1-2 |
| 3 Same counts on a clean machine | M2-1, M2-2, M2-4, M5-6 |
| 4 Data described the course's way | M2-1, M2-3, M5-1 |
| 5 Baseline before the paper's method | M2-7 |
| 6 Method runs end to end, one command | M2-4, M3-1 to M3-5, M5-6 |
| 7 Paper / ours / difference table | M4-1, M4-2, M4-3 |
| 8 Every gap has a reason | M2-5, M3-2, M4-3, M4-4, M4-5 |
| 9 Wiki runbook | M5-2, M5-6 |
| 10 README front door | M5-3 |
| 11 Contribution table | M1-4, M5-4 |
| 12 Board clean | M1-6, M5-5 |
| 13 Dry run within time | M5-7 |
| 14 Offline demo fallback | M5-8 |
| 15 Each member knows their part | M5-9 |

Stories M5-7 to M5-9 have no GitHub issue yet. The presentation isn't covered by any current issue.
