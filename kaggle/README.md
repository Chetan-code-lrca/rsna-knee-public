# Kaggle notebooks and submission workflow

This folder holds the original offline weak-supervision baseline, a format-only fallback, and workflow documentation. The higher-scoring Reference Ensemble and S6 reproduction/adaptation are maintained in Kaggle because they use multiple public model/data assets.

## Final competition outcome (2026-10-27)

The Kaggle public leaderboard screenshot showed **rank 2,465 / public AUC 0.950**. The private/final leaderboard screenshot showed **rank 2,381 / score 0.935**. The latter is the participant/team final score; we do not have a separate private AUC confirmed for each individual notebook.

| Candidate | Observed result | Outcome |
|---|---|---|
| [S6 ConvNeXt reproduction/adaptation](https://www.kaggle.com/code/chetaninaganti/rsna-knee-s6fall-solo) | **0.950 public AUC** | Completed, selected |
| [Reference Ensemble Evaluation](https://www.kaggle.com/code/chetaninaganti/rsna-knee-reference-ensemble-candidate) | **0.943 public AUC** | Completed, selected |
| [Original weak-supervision baseline](https://www.kaggle.com/code/chetaninaganti/rsna-knee-offline-weak-supervision-baseline) | **0.636 public AUC** | Completed, not selected |
| [Safe fallback](https://www.kaggle.com/code/chetaninaganti/rsna-knee-safe-fallback-submission) | VALID: 3 studies x 12 targets | Format check only; all predictions were 0.5 |

The S6 notebook is an attributed reproduction/adaptation of [nartaa's public notebook](https://www.kaggle.com/code/nartaa/rsna-knee-s6fall-solo), not a model developed from scratch in this repository. The S6 weights are reported under CC BY-NC 4.0; preserve the original attribution and licence notices. See [model provenance](../reports/model-provenance.md) and the [final results report](../reports/competition-final-results-2026-10-27.md).

## Original research: weak-label audit

The [rsna_knee_weak_label_audit folder](rsna_knee_weak_label_audit/) contains a notebook that evaluates the current report-derived weak-label rules against the expert-labelled subset. It reports per-target coverage, TP/FP/TN/FN, accuracy, precision, recall, specificity and F1. It does not train a model, inspect test reports, or modify submissions.

Observed results:
- 4,407 training studies and 24,371 series.
- 58 fully expert-labelled studies.
- 214/696 target-study pairs covered (**30.7% coverage**).
- **72.4% accuracy among covered pairs**.

These conditional metrics come from a small labelled subset and should not be interpreted as full-dataset sensitivity or independent validation. See [full audit results](../reports/weak-label-audit-results.md).

## What the baseline does

- Uses 58 expert-labelled studies, with report-derived weak targets from other training reports.
- Reads no test reports and makes no runtime network calls.
- Samples 8 slices at 160×160 from one selected fluid-sensitive series per study.
- Uses a small CNN trained from scratch for four epochs and mean pooling over slice features.
- Uses rule-derived report labels at weight 0.15 and a series-metadata fallback when image decoding fails.
- Sorts DICOM slices using projected ImagePositionPatient when available, with metadata fallback.

The 0.636 result indicates the current model/label representation is weak. Source review did not find filename-only DICOM ordering in this notebook, so changing slice sorting should not be the first fix. See [baseline diagnosis](../reports/experiment-diagnosis.md).

## Reproducing the repository notebooks

Push the baseline from its metadata folder:

    cd ~/projects/rsna-knee/kaggle
    kaggle kernels push -p .

Push the fallback:

    cd ~/projects/rsna-knee/kaggle/rsna_knee_safe_fallback
    kaggle kernels push -p .

Confirm that the metadata ID matches the owned Kaggle notebook slug. Do not commit credentials, raw competition data, DICOM files or model weights that are not permitted for redistribution.

## Submission checks

1. Attach only the official competition and permitted model/data assets.
2. Disable Internet for the scored rerun; use GPU only where needed.
3. Stay within the competition's runtime limit.
4. Write /kaggle/working/submission.csv.
5. Validate one row per test study, study IDs/order, the exact 12 target columns, and finite probabilities in [0, 1].
6. Treat the visible three-row test file as a smoke test only.
7. Wait for Kaggle's Submissions page to show a completed evaluation and score.
8. Record public scores separately from the final/private leaderboard result.

See [submission checklist](../docs/competition-submission-checklist.md), [final experiment report](../reports/final-experiment-report.md), [final results](../reports/competition-final-results-2026-10-27.md), and [model provenance](../reports/model-provenance.md). Official sources: [evaluation](https://www.kaggle.com/competitions/rsna-knee-abnormality-detection/overview/evaluation), [rules](https://www.kaggle.com/competitions/rsna-knee-abnormality-detection/rules).
