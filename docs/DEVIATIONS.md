# Deviations and ambiguities log

Every place where the paper (Kurniabudi et al. 2020) is unclear, or where we do something different, is logged here **before** we act on it. Details, evidence and options: [docs/SPLIT_SPEC.md](SPLIT_SPEC.md).

Status values: **Open** (team decision needed) · **Decided** (rule fixed, with who/when/where) · **Note** (a paper inconsistency, no choice needed).

| ID | Topic | Paper says | Our situation | Status | Spec section |
|---|---|---|---|---|---|
| D1 | 20% sample method | "Only 20% … are used" (§III.B); method not given | Must pick a reproducible rule. Evidence points to a fixed-size, non-stratified random sample | Open | §1 |
| D2 | Duplicate rows | Not mentioned | 308,381 exact repeats (10.89%); paper's Table 3 counts fit duplicates **kept** | Open | §2 |
| D3 | Same features, different labels | Not mentioned | 698 groups, 7,020 rows | Open | §2 |
| D4 | NaN / Inf values | "no data transformation is required" (§IV.A) | 2,867 rows with NaN/Inf in 2 columns; scikit-learn needs finite values | Open | §3 |
| D5 | Which `Fwd Header Length` to drop | "one of those columns must be removed" (§IV.A) | Columns identical; choice has no effect on values | Open (low stakes) | §4 |
| D6 | Web Attack label strings | Table 3 shows "Web Attack–…" | Raw files contain U+FFFD; keep or rename | Open (low stakes) | §5 |
| D7 | Table 3 vs Table 4, Normal count | Table 3: 454,396; Table 4 sum: 454,306 | 90-row gap; Table 4 total is the exact 20%. Likely a Table 3 typo (`unverified`) | Note | §5 |
| D8 | 70/30 split vs 10-fold CV | Both described (§III.B, §IV.A, §IV.C); relation not stated | Table 9 Infiltration TPRs (0.6/0.4/0.8) fit CV on the 70% training set | Open | §6 |
| D9 | Split stratification | Not stated | Table 4 per-class train shares 0.685–0.833: not stratified | Open | §6 |
| D10 | IG implementation | Weka 3.9; settings not given | Python/scikit-learn has no identical evaluator; discretization choice affects ranking | Open | §7 |
| D11 | Random Forest settings | Weka 3.9; parameters not given | Must choose Weka-equivalent or scikit-learn defaults, or run Weka | Open | §8 |
| D12 | Metric averaging | Not stated | Single Table 9 values likely Weka weighted averages (`unverified`) | Open | §9 |
| D13 | Tool | Weka 3.9 (§III.E) | Project is Python 3.11 / scikit-learn 1.6.1 unless the team chooses Weka for D10/D11 | Open | §7, §8 |
| D14 | IG threshold wording | Table 6 ">0.4"; Algorithm 2 "≥ 0.4" | No effect: weights 0.415 (22nd) and 0.390 (23rd) | Note | §7 |

When a row is decided, change its status to **Decided** and add: the choice, who agreed (issue/PR link), date, and the expected effect on results.
