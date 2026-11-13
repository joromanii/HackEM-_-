# User stories by milestone

User stories for reproducing **Rajagopal et al. (2020), Table 4: a stacking ensemble on UNSW-NB15, binary accuracy 0.94** (spec: [docs/PAPER_METHOD.md](PAPER_METHOD.md)). Each story names its GitHub issue and the item it covers in the instructor's *Capstone Readiness Checklist* (CIS 3370), numbered 1–15 in the order the checklist lists them.

**Format:** *As a [role], I want [something], so that [benefit].* Each story has acceptance criteria that can be checked against a file, run or issue.

**Roles:** **researcher** (a member building or running the reproduction) · **reviewer** (a member checking someone else's work) · **instructor** (Dr. Parra, grading against the readiness checklist) · **newcomer** (someone opening the repo or wiki for the first time) · **presenter** (a member presenting on presentation day).

**Status** as of 2026-11-13: Done · In review · In progress · Not started · Blocked.

**Team** marks stories that need every member, or someone other than the author. Owners are chosen by the team and recorded on the issue, never filled in here.

> Issue numbers assume Issues #4–#9 are re-pointed from CIC-IDS2017 to this paper; #1–#3 and #10–#13 keep their current topics; #20–#22 cover the wiki runbook, presentation and offline demo.

---

## M1 — Paper selection and proposal

| ID | User story | Acceptance criteria | Issue | Checklist | Status |
|---|---|---|---|---|---|
| M1-1 | As the **instructor**, I want the claim in one sentence, so that I know exactly what number the team is chasing and on what data. | The sentence from `docs/PAPER_METHOD.md` is at the top of `README.md`: stacking ensemble, 11 features, UNSW-NB15 test set, binary accuracy 0.94 (Table 4). Someone outside the team can repeat it without a follow-up question. | #1 | 1 | In progress |
| M1-2 | As a **researcher**, I want every paper number we compare against recorded with its table, so that the comparison uses the right targets. | `docs/PAPER_METHOD.md` lists Table 4 (counts and six metrics), Table 1 (class counts) and Table 3 (settings) with citations. A second member checks them against the paper. | #1 | 2 | In progress (second check needed) |
| M1-3 | As a **team** member, I want my vote on the new paper recorded, so that the switch is unanimous and visible. | Each member posts their own vote in Issue #2. The reason for leaving the old paper is recorded in Issue #1. | #1, #2 | — | Not started (*Team*) |
| M1-4 | As the **team**, I want the roster, GitHub usernames, presentation date and deadlines in one place, so that work can be planned and credited. | Issue #2 lists each member's name and username (posted by that member), the presentation date and time limit, and the deliverable deadline. | #2 | 11 | Not started (*Team*) |
| M1-5 | As the **instructor**, I want a proposal that maps each checklist item to an issue or file, so that I can see how the team will meet it. | The proposal covers the citation, claim, data source, feasibility in three weeks, risks (SVM runtime, unstated settings) and scope (UNSW-NB15 only), plus a table mapping all 15 checklist items. | #3 | All | Not started |
| M1-6 | As a **newcomer**, I want the old CIC-IDS2017 and KDD plans clearly marked as superseded, so that the repo and board show one project. | Old milestones and PRs are closed or renamed with a note. Old CIC-IDS2017 files are labeled as superseded, not deleted. | #13 | 10, 12 | In progress |

## M2 — Data audit and reproducible baseline

| ID | User story | Acceptance criteria | Issue | Checklist | Status |
|---|---|---|---|---|---|
| M2-1 | As a **researcher**, I want the official UNSW-NB15 training and testing files, so that we use the same data as the paper. | Source URL, download date and file checksums are recorded. Raw files stay outside the repo. | #4 | 3 | Not started |
| M2-2 | As a **researcher**, I want a data audit, so that we know the files match the paper before any modelling. | A committed read-only script reports rows, columns, class counts vs Table 1, missing values, duplicates, and whether all 11 features exist. Any count that differs from Table 1 stops the work and is reported. | #4 | 3, 4 | Not started |
| M2-3 | As a **reviewer**, I want to run the audit on my own machine and get the same counts, so that loading is reproducible. | A member other than the author runs it from the README steps and posts matching checksums and counts in Issue #4. | #4 | 3 | Not started (*Team*) |
| M2-4 | As the **instructor**, I want the data described the course's way, so that the report answers the standard data questions. | The report answers the course's first four data questions and gives the class balance (binary and 10-class), each with the code or results file behind it. | #4, #10 | 4 | Blocked (need the course's four questions) |
| M2-5 | As a **future reviewer**, I want pinned Python, packages and one config file, so that the project runs the same on any machine. | `requirements.txt`, `requirements-lock.txt` and `configs/run.toml` (data paths updated for UNSW-NB15). | #7 | 3, 6 | In review (PR #16) |
| M2-6 | As the **team**, I want each open method question (S1–S14) decided before coding, so that no choice is made after seeing results. | `docs/DEVIATIONS.md` has a row per question with the choice, where the team agreed, and the date. | #5 | 6, 8 | Not started (*Team*) |
| M2-7 | As a **researcher**, I want a baseline scored before the stacking model, so that we know what stacking adds. | One command scores a majority-class predictor and each base model alone (RF, KNN, LR) on the same split and features. A run folder holds config, seed, versions, runtime, confusion matrices and metrics. Not called a reproduction. | #6 | 5 | Blocked by M2-2, M2-6 |

## M3 — Faithful paper method

| ID | User story | Acceptance criteria | Issue | Checklist | Status |
|---|---|---|---|---|---|
| M3-1 | As a **researcher**, I want preprocessing fitted on training data only, so that the test set can't leak into the model. | Scaling, encoding of `service` and any transform are fitted on the 175,341 training rows only. A check confirms the test rows aren't used. | #8 | 6, 8 | Not started |
| M3-2 | As a **researcher**, I want the 11 features selected by name, so that a column shift can't select the wrong feature. | The code selects the 11 features by name and stops if one is missing. Any change to the list is logged. | #8 | 6 | Not started |
| M3-3 | As a **researcher**, I want the stacking ensemble built as the paper describes, so that our result tests the paper's method. | RF (100, gini), KNN (5, Minkowski) and LR (L2) feed an SVM (C=1.0, rbf) through cross-validated predictions (Algorithm 1). Every unstated setting comes from `DEVIATIONS.md`. | #8 | 6 | Not started |
| M3-4 | As a **researcher**, I want the SVM's runtime checked on a sample first, so that a slow full run doesn't block the schedule. | Timing on a sample is saved. Any subsampling or setting change for speed is logged as a deviation before the full run. | #8 | 6 | Not started |
| M3-5 | As a **reviewer**, I want one command that goes from raw data to the headline number, so that I can rerun it on my machine. | One command in the README and wiki produces the Table 4 comparison. A member who didn't write the code runs it and gets the same numbers. | #8, #12 | 6 | Not started (*Team*) |
| M3-6 | As a **reviewer**, I want each method PR checked against the paper, so that mistakes are caught before results are reported. | Each PR includes the method-reviewer report and is approved by at least one member. | #8 | 6 | Not started (*Team*) |

## M4 — Evaluation and gap analysis

| ID | User story | Acceptance criteria | Issue | Checklist | Status |
|---|---|---|---|---|---|
| M4-1 | As the **instructor**, I want one table with the paper's numbers, ours and the difference, so that I can judge the reproduction at a glance. | Columns Paper, Ours and Difference for accuracy, precision, recall, F1, AUC and FAR on the 82,332-record test set. No empty cells. Each of our numbers links to its results file. | #9 | 7 | Not started |
| M4-2 | As a **reviewer**, I want metric definitions next to the numbers, so that paper and ours are compared like for like. | Positive class (proposed: attack, per S9), FAR formula, AUC scores used, and rounding are stated. The paper's apparent truncation and its unexplained 5.2% FAR are noted. | #9 | 7, 8 | Not started |
| M4-3 | As a **researcher**, I want confusion matrices for the baseline and the stacking model, so that we can see what stacking actually changes. | Binary confusion matrices next to Table 4's counts, and each base model's numbers alongside. | #9 | 5, 7 | Not started |
| M4-4 | As the **instructor**, I want every gap explained or plainly marked unexplained, so that conclusions don't outrun the evidence. | For each difference beyond seed-to-seed variation (measured over several seeds), the report names a cause (unstated preprocessing, settings, rounding) or says none was found. | #9 | 8 | Not started |
| M4-5 | As a **researcher**, I want a 10-class run on the full test set, so that we can discuss per-class detection like the paper's Table 6. | Per-class recall and precision on all 82,332 test rows, with a note that the paper's Table 6 used an unexplained 51,535-row subset. | #9 | 8 | Not started |

## M5 — Report, evidence, presentation and final review

| ID | User story | Acceptance criteria | Issue | Checklist | Status |
|---|---|---|---|---|---|
| M5-1 | As the **instructor**, I want a report that explains the method, deviations, results and gaps, so that I can grade from saved evidence. | `docs/REPORT.md` covers data, preprocessing, model settings, versions, seeds, the comparison table and the gap analysis. Every number links to a results file. Sections are split among members. | #10 | 4, 7, 8 | Not started (*Team*) |
| M5-2 | As a **newcomer**, I want a wiki runbook, so that I can set up and run the project without asking anyone. | The wiki covers setup, downloading the data, the audit, baseline and stacking runs, and where results go. A member who didn't write it follows it and records where they got stuck. | #20 | 9 | Not started (*Team*) |
| M5-3 | As a **newcomer**, I want the README to show the result within a minute, so that I know what the project found right away. | The README top has the claim, our headline number beside the paper's, status, and links to the report and wiki. | #11 | 10 | Not started |
| M5-4 | As the **team**, I want an accurate contribution table, so that each member is credited for real work. | Each row in the README's Individual Contribution Summary Table is backed by commits, issues, PRs or documents with that person's name. Points and percentages agreed by the team. | #11 | 11 | Not started (*Team*) |
| M5-5 | As the **instructor**, I want a clean project board, so that I can see what was done, in progress or dropped. | Every card is closed, in progress with a reason, or dropped with a note. | #11, #13 | 12 | Not started |
| M5-6 | As a **reviewer**, I want a final check from a fresh clone, so that we submit only what works. | Someone reruns the pipeline from a clean clone, checks each reported number against its file, checks links, and records what passed and what's unverified. | #12 | 3, 6, 9 | Not started (*Team*) |
| M5-7 | As the **team**, I want a timed dry run of the presentation, so that we finish within the limit without cutting results. | At least one full run-through inside the time limit with the results section intact; the time is recorded. | #21 | 13 | Not started (*Team*) |
| M5-8 | As a **presenter**, I want a demo fallback that works offline, so that a network or laptop problem doesn't stop the demo. | A recorded video or screenshots of the pipeline running play from the presentation machine with no network. | #22 | 14 | Not started |
| M5-9 | As each **team member**, I want to know my section and the one number I explain, so that everyone presents confidently. | A list maps each member to a section and a number, confirmed by each member in the dry run. | #21 | 15 | Not started (*Team*) |

---

## Checklist coverage

| Checklist item | Stories |
|---|---|
| 1 Claim in one sentence | M1-1 |
| 2 Paper's numbers recorded | M1-2 |
| 3 Same counts on a clean machine | M2-1, M2-2, M2-3, M2-5, M5-6 |
| 4 Data described the course's way | M2-2, M2-4, M5-1 |
| 5 Baseline before the paper's method | M2-7, M4-3 |
| 6 Method runs end to end, one command | M2-5, M2-6, M3-1 to M3-6, M5-6 |
| 7 Paper / ours / difference table | M4-1, M4-2, M4-3, M5-1 |
| 8 Every gap has a reason | M2-6, M3-1, M4-2, M4-4, M4-5, M5-1 |
| 9 Wiki runbook | M5-2, M5-6 |
| 10 README front door | M1-6, M5-3 |
| 11 Contribution table | M1-4, M5-4 |
| 12 Board clean | M1-6, M5-5 |
| 13 Dry run within time | M5-7 |
| 14 Offline demo fallback | M5-8 |
| 15 Each member knows their part | M5-9 |
