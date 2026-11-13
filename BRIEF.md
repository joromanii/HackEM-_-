# Project Brief: HackEM-_- — UNSW-NB15 stacking-ensemble reproduction

## What this is
A CIS 3370 capstone project that reproduces and evaluates one published intrusion-detection result.
Target: Rajagopal, Kundapur & Hareesha, "A Stacking Ensemble for Network Intrusion Detection Using Heterogeneous Datasets," *Security and Communication Networks* 2020 (DOI 10.1155/2020/4586875), **Table 4: binary stacking ensemble on the UNSW-NB15 test set, accuracy 0.94**.
We implement the paper's preprocessing, 11 features and stacking model (random forest, KNN and logistic regression combined by an SVM) as closely as the paper allows, measure our own results with fixed settings, and explain any gap. Ambiguities become documented deviations, not silent choices. Full spec: `docs/PAPER_METHOD.md`.

## Target change (2026-11-13)
The team dropped the earlier target (Kurniabudi et al. 2020, CIC-IDS2017, Table 9) for this paper. Earlier CIC-IDS2017 work stays in the repo as a record: `docs/DATA_AUDIT.md`, `scripts/audit_inventory.py`, `results/inventory/`. The old spec is in git (`git show 33c47b5:docs/PAPER_METHOD.md`). The reason and votes go in Issues #1 and #2.

## Current state (as of 2026-11-13)
| Item | Status |
|---|---|
| New paper chosen | Owner's choice. **Team votes pending** (Issue #2). |
| Paper spec `docs/PAPER_METHOD.md` | Written on branch `docs/stacking-paper` |
| Paper numbers: accuracy 0.94, precision 0.96, recall 0.93, F1 0.95, AUC 0.99, FAR 5.2% | **Paper-reported only. Not reproduced.** Arithmetic checks in the spec show truncation and an unexplained FAR. |
| UNSW-NB15 data | **Not downloaded.** Official source to be confirmed; ask before downloading. |
| Environment | Python 3.11 pin in PR #16 (open; dataset-independent, still valid). See that PR's `run_meta.json` evidence. |
| Data audit, preprocessing spec, baseline, model, evaluation | Not started for UNSW-NB15 |
| Deadline | About 3 weeks from 2026-11-13 (`unverified`; exact presentation date needed) |

## Next steps
1. Team votes on the paper and target (Issue #2).
2. Confirm the UNSW-NB15 source and download the training and testing CSVs.
3. Data audit: rows, columns, class counts vs Table 1, missing values, duplicates.
4. Team decides the open questions S1–S14 in `docs/PAPER_METHOD.md`; log them in `docs/DEVIATIONS.md`.
5. Baseline (majority class, each base model alone), then the stacking ensemble, then the Table 4 comparison.

## Key components and where they live
- Repo: `github.com/joromanii/HackEM-_-`.
- Paper spec: `docs/PAPER_METHOD.md`. User stories: `docs/USER_STORIES.md`. Deviations log: `docs/DEVIATIONS.md` (to be created for this paper).
- Raw data: outside the repo, **read-only, never committed**. Location to be set in `configs/run.toml`.
- Grading: CIS 3370 *Capstone Readiness Checklist* (15 items); final deliverables (wiki, repo, board, presentation) are not accepted late.

## Open questions
- The 14 method questions S1–S14 in `docs/PAPER_METHOD.md`.
- Presentation date and time limit.
- The course's "first four questions" for describing data (checklist item 4).
- Team roster and GitHub usernames, confirmed by each member.
