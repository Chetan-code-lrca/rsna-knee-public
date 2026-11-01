# Weak-Label Audit — Research Protocol

## Research question

Do the multilingual regular-expression rules in our original weak-supervision notebook produce labels that agree with the expert-labelled training studies often enough to justify using them as pseudo-targets?

## Hypothesis

Rule-derived pseudo-labels are likely to differ in reliability by finding. A single global pseudo-label weight of 0.15 may be poorly calibrated across targets. The audit measures this; it does not assume the hypothesis is true.

## Data and leakage boundaries

- Source is the official competition `train.csv`, including its expert labels and original training reports.
- The audit filters to rows with all twelve expert target labels, expected to be about 58 studies.
- It does not read `test.csv`, `test_series.csv` or test DICOM files. Test reports are not available at evaluation time.
- It does not train a model or adjust the rules automatically.
- The source labeler is reused unchanged from `kaggle/rsna_knee_submission.ipynb`.

## Metrics

For every target, report:
- `coverage_pct`: fraction of expert-labelled studies for which the rule emits a known label.
- TP/FP/TN/FN and accuracy among covered studies.
- Precision, recall, specificity and F1 among covered studies.
- Rule-positive and expert-positive counts in the covered subset.

Report aggregate covered-pair coverage and agreement as descriptive summaries. Undefined metrics should remain blank, not be silently converted to zero.

## Interpretation

A high covered-case accuracy with low coverage is not equivalent to a high-quality general classifier. The sample is small and the same dataset could be used to revise rules later, so this is a development diagnostic—not an unbiased final validation. Any rule change must be versioned, have rationale and tests, and be checked against a frozen evaluation protocol. The competition metric remains macro ROC AUC on the hidden set.

## Run

Kaggle notebook: [RSNA Knee Weak Label Audit](https://www.kaggle.com/code/chetaninaganti/rsna-knee-weak-label-audit)

The notebook is CPU-only and Internet-disabled. Output is `/kaggle/working/weak_label_audit.csv`.
