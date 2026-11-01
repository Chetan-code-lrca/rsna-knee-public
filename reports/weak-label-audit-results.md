# Weak-Label Rule Audit — Results

**Run status:** Completed successfully on Kaggle.  
**Notebook:** [RSNA Knee Weak Label Audit](../kaggle/rsna_knee_weak_label_audit/rsna_knee_weak_label_audit.ipynb)  
**Generated artifact:** `/kaggle/working/weak_label_audit.csv` (download from the Kaggle notebook output; the generated CSV is not committed here).

## Scope

- Training studies: **4,407**
- Fully expert-labelled studies evaluated: **58**
- Fully expert-labelled studies with non-empty reports: **58**
- Total target-study pairs: **696**
- Pairs covered by at least one report rule: **214 / 696 (30.7%)**
- Accuracy on covered pairs: **72.4%**

The audit reads only `train.csv`; it does not inspect `test.csv` or test reports. It compares the existing baseline's report-derived weak-label rules with expert labels. It is a diagnostic experiment, not a new submission model.

## Per-target results

Metrics below are calculated **only among studies covered by that target's rule**. Coverage is included because the conditional metrics alone can look better than the rules deserve.

| Target | Covered / 58 | Coverage | TP | FP | TN | FN | Accuracy | Precision | Recall | Specificity | F1 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ACL | 25 | 43.1% | 13 | 4 | 8 | 0 | 0.840 | 0.765 | 1.000 | 0.667 | 0.867 |
| MCL | 22 | 37.9% | 5 | 4 | 13 | 0 | 0.818 | 0.556 | 1.000 | 0.765 | 0.714 |
| Medial Meniscus | 22 | 37.9% | 11 | 9 | 2 | 0 | 0.591 | 0.550 | 1.000 | 0.182 | 0.710 |
| Lateral Meniscus | 24 | 41.4% | 12 | 4 | 7 | 1 | 0.792 | 0.750 | 0.923 | 0.636 | 0.828 |
| Medial OA | 8 | 13.8% | 3 | 2 | 3 | 0 | 0.750 | 0.600 | 1.000 | 0.600 | 0.750 |
| Lateral OA | 6 | 10.3% | 2 | 3 | 1 | 0 | 0.500 | 0.400 | 1.000 | 0.250 | 0.571 |
| PF OA | 5 | 8.6% | 1 | 4 | 0 | 0 | 0.200 | 0.200 | 1.000 | 0.000 | 0.333 |
| Effusion | 39 | 67.2% | 22 | 11 | 6 | 0 | 0.718 | 0.667 | 1.000 | 0.353 | 0.800 |
| Synovitis | 13 | 22.4% | 9 | 4 | 0 | 0 | 0.692 | 0.692 | 1.000 | 0.000 | 0.818 |
| Baker's | 12 | 20.7% | 4 | 3 | 5 | 0 | 0.750 | 0.571 | 1.000 | 0.625 | 0.727 |
| Contusion | 22 | 37.9% | 9 | 9 | 3 | 1 | 0.545 | 0.500 | 0.900 | 0.250 | 0.643 |
| Fracture | 16 | 27.6% | 9 | 0 | 7 | 0 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |

## Interpretation

1. **Do not interpret conditional recall of 1.0 as full-dataset sensitivity.** Rule metrics are computed only where a rule produces coverage. Uncovered studies are not counted as rule errors in this table.
2. **PF OA, medial meniscus, effusion, and contusion merit careful review.** In the covered subset, their false-positive counts were 4/5, 9/22, 11/39, and 9/22 respectively.
3. **The fracture result is encouraging but preliminary.** It comes from just 16 covered studies among a 58-study expert-labelled subset; it needs a larger independent validation.
4. **Low coverage limits practical reach.** Only 30.7% of all target-study pairs were covered, so these rules cannot supply weak labels for most pairs under this setup.

## Next experiment

Review false-positive and uncovered examples in an error-analysis table before changing thresholds or adding rules. Preserve negation and context handling. Any tuning should be tested against the expert-labelled subset without using test reports, and the small sample should be treated as exploratory rather than definitive evidence of generalisation.
