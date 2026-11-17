# Project Brief: HackEM-_- — UNSW-NB15 stacking-ensemble reproduction

## What this is
A CIS 3370 capstone project that reproduces and evaluates one published intrusion-detection result.
Target: Rajagopal, Kundapur & Hareesha, "A Stacking Ensemble for Network Intrusion Detection Using Heterogeneous Datasets," *Security and Communication Networks* 2020 (DOI 10.1155/2020/4586875), **Table 4: binary stacking ensemble on the UNSW-NB15 test set, accuracy 0.94**.
We implement the paper's preprocessing, 11 features and stacking model (random forest, KNN and logistic regression combined by an SVM) as closely as the paper allows, measure our own results with fixed settings, and explain any gap. Ambiguities become documented deviations, not silent choices. Full spec: `docs/PAPER_METHOD.md`.

## Target change (2026-11-13)
The team dropped the earlier target (Kurniabudi et al. 2020, CIC-IDS2017, Table 9) for this paper. Earlier CIC-IDS2017 work stays in the repo as a record: `docs/DATA_AUDIT.md`, `scripts/audit_inventory.py`, `results/inventory/`. The old spec is in git (`git show 33c47b5:docs/PAPER_METHOD.md`). The reason and votes go in Issues #1 and #2.

## Current state (as of 2026-11-15)
| Item | Status |
|---|---|
| New paper chosen | Owner's choice; team meeting Thursday 2026-11-12 (reported). **Team votes pending** (Issue #2). |
| Paper spec | `docs/PAPER_METHOD.md` |
| UNSW-NB15 data | Downloaded 2026-11-15 to `~/Downloads/UNSW-NB15/`; every class count matches Table 1: measured (`results/unsw_audit/2026-11-15_audit/`) |
| Method choices | 19 **proposed** choices in `docs/DEVIATIONS.md`; **team approval pending** (Issue #5) |
| Baseline | Done: measured (`results/runs/2026-11-15_baseline_binary_seed42/`) |
| Stacking ensemble | Done: accuracy 0.8648 vs paper 0.94: measured (`results/comparison/2026-11-15_table4/`) |
| Gap analysis | Done: seed variation, three preprocessing alternatives and duplicates don't account for the gap; 87.4% of false alarms are normal test records with `sttl` = 254; the paper's result is not explained (`docs/REPORT.md` §7) |
| Report, runbook | Drafts: `docs/REPORT.md`, `docs/wiki/Runbook.md` |
| Presentation | Outline: `docs/PRESENTATION.md` (Issue #21) |
| Deadline | About 3 weeks from 2026-11-13 (`unverified`; exact presentation date needed) |

## Next steps
1. Team votes (Issue #2) and approves or changes the proposed choices (Issue #5). Any change: edit `configs/run.toml`, re-run, re-run `scripts/compare.py`.
2. A member who didn't write the code follows the runbook on their own machine (Issues #4, #20).
3. Each member rewrites their report section and fills in `docs/MEETINGS.md` and the contribution table.
4. Presentation dry run and offline demo (Issues #21, #22).

## Key components and where they live
- Repo: `github.com/joromanii/HackEM-_-`.
- Paper spec: `docs/PAPER_METHOD.md`. User stories: `docs/USER_STORIES.md`. Deviations log: `docs/DEVIATIONS.md` (D1–D19 proposed).
- Raw data: outside the repo, **read-only, never committed**. Location set in `configs/run.toml` (`~/Downloads/UNSW-NB15`).
- Grading: CIS 3370 *Capstone Readiness Checklist* (15 items); final deliverables (wiki, repo, board, presentation) are not accepted late.

## Open questions
- The 14 method questions S1–S14 in `docs/PAPER_METHOD.md`.
- Presentation date and time limit.
- The course's "first four questions" for describing data (checklist item 4).
- Team roster and GitHub usernames, confirmed by each member.
