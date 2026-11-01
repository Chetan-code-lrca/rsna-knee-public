# RSNA Knee Weak-Label Rule Audit

This CPU-only, Internet-disabled Kaggle notebook evaluates our existing report-derived weak-label rules against the fully expert-labelled rows of the official training CSV.

## Why this experiment exists

Our original weak-supervision baseline scored 0.636 public AUC. Before modifying the model blindly, we want evidence about the labeler: coverage and per-target agreement with expert labels. This notebook uses the exact report-rule cell from our baseline so the diagnostic does not introduce a second hand-written parser.

## Outputs

`/kaggle/working/weak_label_audit.csv` contains, per target:
- number of expert-labelled studies and rule-covered studies;
- coverage percentage;
- TP / FP / TN / FN;
- accuracy, precision, recall, specificity and F1 on covered cases.

The notebook also prints aggregate coverage and accuracy among rule-covered target/study pairs and runs a small synthetic sanity check for the metric calculation.

## Important limits

- The fully expert-labelled subset contains only about 58 studies; statistics will be noisy.
- Accuracy is conditional on the rule emitting a label. Always read it together with coverage.
- This notebook reads only the training CSV and report field. It does not read test reports, access hidden labels, train models, call external services or download assets.
- The audit diagnoses our current rule set; it does not itself improve the submitted model. Any revised rules require a separately documented experiment.
- The official competition metric remains macro ROC AUC across twelve targets, calculated by Kaggle on a private hidden-test rerun.

## Run on Kaggle

From WSL after syncing this repository:

```bash
cd ~/projects/rsna-knee/kaggle/rsna_knee_weak_label_audit
kaggle kernels push -p .
```

After execution, download or inspect `weak_label_audit.csv` from the Output panel. Keep Internet disabled and do not submit this diagnostic notebook to the competition; it is for research and label QA only.
