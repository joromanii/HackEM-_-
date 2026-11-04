# Data audit: CIC-IDS2017 MachineLearningCSV (Issue #4)

This audit reports what is in the raw files. It does not clean, drop or relabel anything. Choices about what to do with these findings belong in `docs/SPLIT_SPEC.md` (Issue #5).

- **Run folder:** [`results/inventory/2026-11-02_audit/`](../results/inventory/2026-11-02_audit/)
- **Script:** [`scripts/audit_inventory.py`](../scripts/audit_inventory.py), read-only on `~/Downloads/MachineLearningCVE/`
- **Environment:** Python 3.9.6, pandas 2.2.3, numpy 2.0.2, scikit-learn 1.6.1 (recorded in [`run_meta.json`](../results/inventory/2026-11-02_audit/run_meta.json)). Runtime 14.6 s. No randomness.
- **Re-run:** `.venv/bin/python scripts/audit_inventory.py --out-dir results/inventory/<new-folder>` (setup: README "Setup and run") (the script refuses to overwrite an existing folder).

All numbers below are `measured (results/inventory/2026-11-02_audit/...)` unless marked otherwise.

## Summary

| Check | Finding | Evidence |
|---|---|---|
| Files | 8 CSVs, 2,830,743 rows in total, 79 columns each, same header in all files | [`files.csv`](../results/inventory/2026-11-02_audit/files.csv) |
| Earlier label counts | All 15 labels match `~/ids-capstone/results/dataset_label_counts.csv` exactly | [`label_count_comparison.csv`](../results/inventory/2026-11-02_audit/label_count_comparison.csv) |
| Label encoding | The three Web Attack labels contain U+FFFD (bytes `ef bf bd`) in the raw file | [`label_encoding.csv`](../results/inventory/2026-11-02_audit/label_encoding.csv) |
| Column names | 65 of 79 raw names have a leading space (e.g. `" Destination Port"`) | [`columns.csv`](../results/inventory/2026-11-02_audit/columns.csv) |
| Duplicate `Fwd Header Length` | Columns at positions 34 and 55 (0-based) are identical in every row of every file | [`fwd_header_check.csv`](../results/inventory/2026-11-02_audit/fwd_header_check.csv) |
| NaN / Inf | Only in `Flow Bytes/s` (1,358 NaN, 1,509 +Inf) and `Flow Packets/s` (2,867 +Inf). No −Inf. | [`inf_nan.csv`](../results/inventory/2026-11-02_audit/inf_nan.csv) |
| Exact duplicate rows | 308,381 extra copies (10.89% of rows); 256,479 within files, 51,902 across files | [`duplicates.csv`](../results/inventory/2026-11-02_audit/duplicates.csv) |
| Same features, different label | 698 feature groups covering 7,020 rows | [`conflicting_labels.csv`](../results/inventory/2026-11-02_audit/conflicting_labels.csv) |

## Files and rows

| File | Rows |
|---|---:|
| Friday-WorkingHours-Afternoon-DDos | 225,745 |
| Friday-WorkingHours-Afternoon-PortScan | 286,467 |
| Friday-WorkingHours-Morning | 191,033 |
| Monday-WorkingHours | 529,918 |
| Thursday-WorkingHours-Afternoon-Infilteration | 288,602 |
| Thursday-WorkingHours-Morning-WebAttacks | 170,366 |
| Tuesday-WorkingHours | 445,909 |
| Wednesday-workingHours | 692,703 |
| **Total** | **2,830,743** |

SHA-256 checksums for each file are in `files.csv`, so teammates can confirm they have the same download. No row has all features missing.

## Labels

15 labels; BENIGN is 2,273,097 rows (80.30%). Full per-file and total counts: [`label_counts.csv`](../results/inventory/2026-11-02_audit/label_counts.csv). The smallest classes are Infiltration (36), Web Attack Sql Injection (21) and Heartbleed (11).

**Encoding:** `Web Attack � Brute Force`, `Web Attack � XSS` and `Web Attack � Sql Injection` contain the Unicode replacement character U+FFFD, stored as UTF-8 bytes `ef bf bd` in the raw CSV. So the problem is in the file itself, not in how it is read. `unverified`: the original character (likely a dash) was probably lost when the CSVs were created; the audit cannot show when or how. Any relabeling (paper Table 3) must match these exact strings or rename them deliberately and log it in `docs/DEVIATIONS.md` (to be created in Issue #5).

## Columns

- 78 feature columns plus `Label`. Integer columns read as `int64`, the rest as `float64`; only `Label` is text.
- 65 raw names start with a space. Code should select columns by **stripped** name and check that every expected name exists.
- `Fwd Header Length` appears twice (positions 34 and 55, 0-based). The two columns have 0 differing rows in all 8 files, so dropping either one gives the same data. The paper says one was removed but not which (see `docs/PAPER_METHOD.md`); since they are identical, the choice doesn't change values.

## NaN and Inf

| Column | NaN | +Inf | −Inf |
|---|---:|---:|---:|
| Flow Bytes/s | 1,358 | 1,509 | 0 |
| Flow Packets/s | 0 | 2,867 | 0 |

All other columns have no NaN or Inf. Per-file counts are in `inf_nan.csv`. `unverified`: these are probably flows with zero duration (rate = x/0); the audit did not check that. Neither column is in the paper's 22-feature set (Table 6, per `docs/PAPER_METHOD.md`), but both are among the 77 features ranked by Information Gain, so handling them is an Issue #5 decision.

## Duplicate rows

Exact duplicates compare all 79 columns, including `Label`. "Extra copies" counts every repeat after the first.

| Label | Rows | Extra copies |
|---|---:|---:|
| BENIGN | 2,273,097 | 176,613 |
| PortScan | 158,930 | 68,111 |
| DoS Hulk | 231,073 | 58,224 |
| SSH-Patator | 5,897 | 2,678 |
| FTP-Patator | 7,938 | 2,005 |
| DoS slowloris | 5,796 | 411 |
| DoS Slowhttptest | 5,499 | 271 |
| Web Attack � Brute Force | 1,507 | 37 |
| Bot | 1,966 | 13 |
| DDoS | 128,027 | 11 |
| DoS GoldenEye | 10,293 | 7 |
| Heartbleed, Infiltration, Web Attack � Sql Injection, Web Attack � XSS | — | 0 |
| **All** | **2,830,743** | **308,381** |

The highest shares of repeats are SSH-Patator (45.4%), PortScan (42.9%), FTP-Patator (25.3%) and DoS Hulk (25.2%). If duplicates are kept, identical rows can land in both training and test sets, which can inflate accuracy. Whether to remove them is not stated in the paper and is an open question in `BRIEF.md`.

**Same features, different label:** 698 groups of rows have identical features but more than one label: BENIGN/PortScan 564, BENIGN/DoS Hulk 130, BENIGN/DDoS 3, BENIGN/DoS slowloris 1. Rows involved by label: DoS Hulk 5,224, PortScan 1,053, BENIGN 736, DDoS 6, DoS slowloris 1 ([`conflicting_labels_by_label.csv`](../results/inventory/2026-11-02_audit/conflicting_labels_by_label.csv)). No model can separate these rows.

**Method:** the script uses 64-bit row hashes. A separate in-session check that compared full rows directly gave the same counts (308,381 / 256,479 / 698). That check was not saved as a results file, so treat it as `unverified` support only.

## Questions this hands to Issue #5

1. Remove exact duplicate rows, keep them, or test both? (Paper doesn't say.)
2. Handle the 698 conflicting-label groups?
3. Drop or impute rows with NaN/Inf in `Flow Bytes/s` and `Flow Packets/s`, or drop those columns?
4. Keep the U+FFFD label strings as-is or rename them, and how they map to Table 3 groups.
5. Which `Fwd Header Length` to drop (no effect on values, but the rule should be written down).
