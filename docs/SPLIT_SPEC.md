# Preprocessing and split specification (Issue #5)

Written **before** any training. It records what the paper says, what our data shows, and the options for each step. Where the paper is unclear, the choice is left as **TEAM DECISION NEEDED**. Nothing here has been chosen for the team.

**Sources**
- Paper: Kurniabudi et al., *IEEE Access* 8 (2020), read from the [IEEE Xplore full text](https://ieeexplore.ieee.org/document/9142219) on 2026-11-07 (open access, CC BY 4.0). Tables 3–6 and 9 are images there; their numbers were transcribed by hand and should be double-checked by a second person.
- Data audit: [docs/DATA_AUDIT.md](DATA_AUDIT.md), [`results/inventory/2026-11-02_audit/`](../results/inventory/2026-11-02_audit/)
- Spec evidence: [`scripts/spec_evidence.py`](../scripts/spec_evidence.py), run in [`results/spec/2026-11-07_evidence/`](../results/spec/2026-11-07_evidence/)
- Deviations and open choices: [docs/DEVIATIONS.md](DEVIATIONS.md)

Number labels: `paper-reported` (paper table/section), `measured (file)`, `derived` (arithmetic on paper-reported numbers, shown), or `unverified`.

## Fixed rules (not open)

These follow directly from the paper or from the project rules.

1. **Information Gain uses training data only.** Paper §III.B: "Feature selection is performed on the training data using Information Gain." The test portion is never seen by feature ranking, scaling or any fitted step.
2. **Features are selected by column name**, using the Table 5/6 ID-to-name pairs. Checked 2026-11-07: all 22 IDs in Table 6 (>0.4 group) map in Table 5 to the names listed in [docs/PAPER_METHOD.md](PAPER_METHOD.md), and all 22 names exist in the CSV header (`measured (results/inventory/2026-11-02_audit/columns.csv)`).
3. **Multiclass task with the paper's 7 classes** (Table 3). Exact mapping in §5 below.
4. **One seed** from [`configs/run.toml`](../configs/run.toml) (on branch `m2/env`, PR pending) for every random step.
5. **Raw files stay read-only**; every run writes a new folder with config, versions and runtime.

---

## 1. Drawing the 20% sample

**Paper:** §III.B: "Only 20% of MachineLearningCSV data … are used." §IV.A: the eight CSVs "are combined into one CSV file" and converted to ARFF for Weka. The paper does not say how the 20% was drawn (random or not, stratified or not, with or without replacement, seed).

**Evidence**
- Table 4 train + test = 396,304 + 169,845 = **566,149** (`derived` from paper-reported Table 4). 20% of our 2,830,743 rows is 566,148.6 (`measured (results/spec/2026-11-07_evidence/table3_compare.csv)`). So the sample is a fixed-size 20%, not a per-row coin flip.
- Per class, the paper's sample is not exactly 20%: Bot 367 of 1,966 (0.187), Infiltration 6 of 36 (0.167), DoS/DDoS 0.201 (`measured (table3_compare.csv, column paper_t3_over_full)`). That fits a random sample that is **not stratified** by class. `unverified`: it could also fit other schemes.
- `unverified`: Weka's `Resample` filter samples **with replacement** by default. If the authors used it, their sample contains extra repeated rows. The paper doesn't name the tool.

**Options**

| Option | What it means | Trade-off |
|---|---|---|
| A. Simple random 20%, without replacement, fixed seed | Closest to the evidence (fixed size, not stratified) | Rare classes vary run to run (Infiltration is ~7 rows); report per-class counts |
| B. Stratified random 20% by original label | Every class gets exactly its 20% share | Not what the paper's counts show; rare classes more stable |
| C. Option A or B, repeated with several seeds | Shows how much the sample alone moves the results | More runtime; needs a rule for how results are summarized |

**TEAM DECISION NEEDED.** Log the choice as a deviation (the paper's method is unrecoverable).

## 2. Duplicate rows

**Paper:** Not mentioned. The only removal described is the duplicate `Fwd Header Length` column (§IV.A).

**Evidence**
- 308,381 rows (10.89%) are extra copies of an identical row (`measured (results/inventory/2026-11-02_audit/duplicates.csv)`).
- The paper's Table 3 counts match 20% of the data **with** duplicates, not without: PortScan paper 31,882 vs 31,786 with duplicates vs 18,164 without; Normal 454,396 vs 454,619 vs 419,297 (`measured (results/spec/2026-11-07_evidence/table3_compare.csv)`). So the paper very likely kept duplicates.
- Keeping duplicates means identical rows can fall in both train and test, which can raise test scores (leakage).

**Options**

| Option | Trade-off |
|---|---|
| A. Keep duplicates (match the paper) | Faithful to the evidence; scores may be inflated by train/test overlap |
| B. Remove exact duplicates before sampling | Cleaner test; class sizes shrink (PortScan −43%, SSH-Patator −45%); a clear deviation |
| C. Run A as the reproduction and B as a sensitivity check | Shows how much duplicates move the numbers; twice the runs |

**TEAM DECISION NEEDED.** Also decide on the 698 groups (7,020 rows) with identical features but different labels (`measured (results/inventory/2026-11-02_audit/conflicting_labels.csv)`): keep, or drop the whole group.

## 3. NaN and Inf values

**Paper:** §IV.A says the 77 features "are already in numerical data type, so no data transformation is required." NaN/Inf handling is not mentioned. Table 5 ranks `Flow Bytes/s` (ID 2, weight 0.379) and `Flow Packets/s` (ID 3, 0.311), so the paper kept both columns.

**Evidence**
- NaN/Inf occur only in `Flow Bytes/s` and `Flow Packets/s` (`measured (results/inventory/2026-11-02_audit/inf_nan.csv)`).
- 2,867 rows (0.10%) have a NaN or Inf in some feature, mostly BENIGN (1,777), DoS Hulk (949) and PortScan (126) (`measured (results/spec/2026-11-07_evidence/nan_inf_rows.csv)`).
- Neither column is among the 22 selected features, but both are ranked by Information Gain.
- `unverified`: how Weka 3.9 read `Infinity` and empty values from this CSV (missing value or a number).

**Options**

| Option | Trade-off |
|---|---|
| A. Drop the 2,867 rows before sampling | Simple; removes 0.10% of rows, mostly BENIGN; small change to class counts |
| B. Keep rows; treat NaN/±Inf as missing and impute (e.g. training-set median) for IG and RF | Keeps all rows; imputation must be fitted on training data only |
| C. Keep rows; replace +Inf with a large finite value and NaN with 0 | Common in CIC-IDS2017 work; arbitrary values; can affect IG ranks of the 2 columns |

**TEAM DECISION NEEDED.** scikit-learn's Random Forest and mutual-information tools reject NaN/Inf in our pinned versions (`unverified`, check before coding), so some option must be chosen.

## 4. Duplicate `Fwd Header Length` column

**Paper:** §IV.A: two columns named "Fwd Header Length" … "one of those columns must be removed", leaving 77 features. Which one is not stated.

**Evidence:** The two columns are identical in every row of all 8 files (`measured (results/inventory/2026-11-02_audit/fwd_header_check.csv)`). The choice cannot change any value.

**Options:** A. drop the second occurrence (CSV position 55, 0-based); B. drop the first (position 34). Either gives the same data.

**TEAM DECISION NEEDED** (low stakes; record the rule).

## 5. Label grouping (Table 3)

**Paper:** §IV.A introduces new attack labels "as listed in Table 3". The table is explicit:

| New label | Original labels (exact raw strings) |
|---|---|
| Normal | `BENIGN` |
| Bot | `Bot` |
| Brute Force | `FTP-Patator`, `SSH-Patator` |
| DoS/DDoS | `DDoS`, `DoS GoldenEye`, `DoS Hulk`, `DoS Slowhttptest`, `DoS slowloris`, `Heartbleed` |
| Infiltration | `Infiltration` |
| PortScan | `PortScan` |
| Web Attack | `Web Attack � Brute Force`, `Web Attack � XSS`, `Web Attack � Sql Injection` (U+FFFD) |

Implemented in [`scripts/spec_evidence.py`](../scripts/spec_evidence.py) (`TABLE3_MAP`); every raw label maps (the script stops otherwise).

**Ambiguities**
- Table 3 prints "DoS Slow, httptest"; read as `DoS Slowhttptest` (`unverified` reading).
- **Table 3 and Table 4 disagree on Normal:** Table 3 says 454,396; Table 4 train + test = 318,087 + 136,219 = 454,306 (`derived`). All other classes agree. The 90-row gap equals the gap between the Table 3 total (566,239) and the Table 4 total (566,149). Table 4's total is the exact 20% (§1), so Table 3's Normal is likely a typo (`unverified`).

**Decision needed only on:** whether to keep the U+FFFD strings as they are in code, or rename them (e.g. to an en dash) with a logged deviation.

## 6. Train/test split and 10-fold cross-validation

**Paper:**
- §III.B and §IV.A: the 20% sample is split 70% training, 30% testing (Table 4).
- §III.B: "10-fold cross-validation is used in this stage" and "All learning and testing steps are executed with 10-fold cross-validation."
- §IV.C: the "input dataset will be randomly divided into 10 folds".
- The paper never says which data the 10 folds use, or whether the 30% test set is used at all.

**Evidence**
- **The cross-validation most likely ran on the 70% training set.** Table 9 gives Infiltration detection (TPR) of 0.600 for BN, 0.400 for RT and 0.800 for NB (`paper-reported`). These are multiples of 1/5. Only the training set has 5 Infiltration rows (Table 4). With 6 rows (the whole sample) TPR could only be multiples of 1/6 (0.167, 0.333, 0.5, …); with 1 row (test set) only 0 or 1 (`derived`).
- **The 70/30 split was not stratified by class.** The overall train share is exactly 0.70000, but per class it ranges from 0.685 (Web Attack) to 0.722 (Bot) and 0.833 (Infiltration) (`derived`, [`table4_ratios.csv`](../results/spec/2026-11-07_evidence/table4_ratios.csv)).
- Weka's cross-validation is stratified by default (`unverified` for the paper's exact settings).

**Options**

| Option | What it means | Trade-off |
|---|---|---|
| A. IG on the 70% train; Random Forest scored by 10-fold CV on the same 70% | Best match to the evidence | IG saw all CV folds (mild selection leakage inside CV); the 30% is unused |
| B. IG on the 70%; train RF on the 70%; score once on the 30% test | Clean holdout; no leakage | Doesn't match how the paper's numbers were most likely made |
| C. Report A as the reproduction and B as the clean estimate | Shows the effect of the protocol | Two sets of numbers to explain |

Split details to fix either way: random, not stratified (matches Table 4) or stratified; same seed; Weka-style stratified 10 folds or not.

**TEAM DECISION NEEDED.**

## 7. Information Gain computation

**Paper:** Weka 3.9 (§III.E); weights in Table 5; groups by minimum weight, 22 features at >0.4 (Table 6; Algorithm 2 writes ≥0.4). The 22nd feature has weight 0.415 and the 23rd 0.390, so > vs ≥ makes no difference (`paper-reported`, Table 5).

**Not stated:** the Weka evaluator settings. `unverified`: Weka's `InfoGainAttributeEval` discretizes numeric features (supervised MDL discretization) before computing gain; scikit-learn's `mutual_info_classif` instead uses a nearest-neighbour estimate, which gives different values and possibly a different ranking.

**Options**

| Option | Trade-off |
|---|---|
| A. Use the paper's 22 features as listed (no IG run) | Isolates the classifier result; doesn't test the IG step |
| B. Recompute IG ourselves (entropy, Eq. 1–2, on MDL- or equal-width-discretized features) on our training split, and compare our ranking with Table 5 | Tests the full method; ranking may differ and select different features |
| C. Do both: B for the comparison, A for the Table 9 reproduction | Most informative; more work |

**TEAM DECISION NEEDED.**

## 8. Random Forest settings

**Paper:** Random Forest in Weka 3.9 with 3,072 MB heap (§III.E). No parameters given.

**Options**
- A. Weka 3.9 defaults translated to scikit-learn. `unverified`: 100 trees, unlimited depth, log2(M)+1 features per split, bagging. Must be checked against Weka docs before use.
- B. scikit-learn defaults (100 trees, √M features per split).
- C. Run Weka 3.9 itself (closest to the paper; adds a Java tool to the setup).

**TEAM DECISION NEEDED.** No tuning toward the paper's numbers under any option.

## 9. Metrics

**Paper:** TPR, FPR, precision, recall, accuracy, % incorrect, execution time (§IV.C). Table 9 gives per-class TPR, then single recall, precision and FPR values. Averaging is not stated.

**Notes**
- `unverified`: the single values look like Weka's class-weighted averages. With weighting by class size, weighted recall equals accuracy, which fits Table 9 (recall 0.999, accuracy 99.86%).
- The paper blames precision = NaN on folds without rare classes (§IV.D). Another possible cause (`unverified`): in Weka, a class that is never predicted has undefined precision, which makes the weighted average NaN. Table 9 shows RF never detects Infiltration (TPR 0).
- We will report: confusion matrix, per-class TPR/FPR/precision/recall, macro and weighted averages, and say which one is compared to the paper. A never-predicted class's precision is reported as undefined, not 0.

**TEAM DECISION NEEDED** only on which averaged value is put next to the paper's recall, precision and FPR.

---

## Order of steps (once decisions are made)

1. Load the 8 CSVs, strip column names, drop one `Fwd Header Length` (§4).
2. Duplicate and NaN/Inf handling (§2, §3), if chosen to happen before sampling.
3. Map labels to the 7 classes (§5).
4. Draw the 20% sample with the project seed (§1).
5. Split 70/30 with the same seed (§6).
6. Fit anything learned (imputation, IG) on the training part only (§3, §7).
7. Select the 22 features by name (§7).
8. Evaluate per §6 and report per §9.
