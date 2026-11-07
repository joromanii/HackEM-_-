# Deviations and ambiguities log

Every place where the paper (Kurniabudi et al. 2020) is unclear, or where we do something different, is logged here **before** we act on it. Details, evidence and options: [docs/SPLIT_SPEC.md](SPLIT_SPEC.md).

Numbers below are labeled as in the spec: `paper-reported`, `measured`, `derived`, `inference`, `unverified`. Sources for measured numbers: `results/inventory/2026-11-02_audit/` (audit) and `results/spec/2026-11-07_evidence/` (spec evidence).

Status values: **Open** (team decision needed) · **Decided** (rule fixed, with who/when/where) · **Note** (a paper inconsistency, no choice needed).

| ID | Topic | Paper says | Our situation | Status | Spec section |
|---|---|---|---|---|---|
| D1 | 20% sample method | "Only 20% … are used" (§III.B); method not given | Must pick a reproducible rule. Evidence points to a fixed-size, non-stratified random sample | Open | §1 |
| D2 | Duplicate rows | Not mentioned | 308,381 exact repeats, 10.89% (`measured`, audit `duplicates.csv`); `inference`: paper's counts fit duplicates **kept** (spec `table3_compare.csv`) | Open | §2 |
| D3 | Same features, different labels | Not mentioned | 698 groups, 7,020 rows (`measured`, audit `conflicting_labels*.csv`) | Open | §2 |
| D4 | NaN / Inf values | "no data transformation is required" (§IV.A) | 2,867 rows with NaN/Inf in 2 columns (`measured`, spec `nan_inf_rows.csv`); scikit-learn rejects Inf (`unverified`, session test not saved) | Open | §3 |
| D5 | Which `Fwd Header Length` to drop | "one of those columns must be removed" (§IV.A) | Columns identical; choice has no effect on values | Open (low stakes) | §4 |
| D6 | Web Attack label strings | Table 3 shows "Web Attack–…" | Raw files contain U+FFFD; keep or rename | Open (low stakes) | §5 |
| D7 | Table 3 vs Table 4, Normal count | Table 3: 454,396; Table 4 sum: 454,306 (`paper-reported` / `derived`) | 90-row gap; Table 4 total matches 20% of our rows. Likely a Table 3 typo (`unverified`) | Note | §5 |
| D8 | 70/30 split vs 10-fold CV | Both described (§III.B, §IV.A, §IV.C); relation not stated | `inference`: Table 9 Infiltration TPRs 0.6/0.4/0.8 (`paper-reported`) fit CV on the 70% training set | Open | §6 |
| D9 | Split stratification | Not stated | `inference`: Table 4 per-class train shares 0.685–0.722 (`derived`, spec `table4_ratios.csv`) mean not stratified | Open | §6 |
| D10 | IG implementation | Weka 3.9; settings not given | Python/scikit-learn has no identical evaluator; discretization choice affects ranking | Open | §7 |
| D11 | Random Forest settings | Weka 3.9; parameters not given | Must choose Weka-equivalent or scikit-learn defaults, or run Weka | Open | §8 |
| D12 | Metric averaging | Not stated | Single Table 9 values likely Weka weighted averages (`unverified`) | Open | §9 |
| D13 | Tool | Weka 3.9 (§III.E) | Project uses Python and scikit-learn 1.6.1 (Python 3.11 pin pending on branch `m2/env`) unless the team chooses Weka for D10/D11 | Open | §7, §8 |
| D14 | IG threshold wording | Table 6 ">0.4"; Algorithm 2 "≥ 0.4" | No effect: weights 0.415 (22nd) and 0.390 (23rd) (`paper-reported`, Table 5) | Note | §7 |
| D15 | Using Table 9 results as protocol evidence | — | §6 and §9 reason from Table 9 TPR values; `PAPER_METHOD.md` says not to infer settings from reported scores | Open | §6 |
| D16 | Reporting rules | Not stated | Proposal: report confusion matrix, per-class and macro/weighted metrics; never-predicted class precision = undefined, not 0 | Open | §9 |

When a row is decided, change its status to **Decided** and add: the choice, who agreed (issue/PR link), date, and the expected effect on results.
