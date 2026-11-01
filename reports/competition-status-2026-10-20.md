> **Historical snapshot (2026-10-20).** Provisional status only; superseded by [final competition results](competition-final-results-2026-10-27.md). Do not use this file as the current competition status.

# RSNA Knee Abnormality Detection — Status Snapshot

**Updated:** 2026-10-20 (IST)

## Observed entries

| Candidate | Evidence | Interpretation |
|---|---|---|
| Reference Ensemble Evaluation | Kaggle page showed **Succeeded**, public score **0.943**, selected (1/2). | Known-good selected entry; public score is not final/private score. |
| Original weak-supervision baseline | Kaggle Version #2 completed and displayed **0.636 public AUC**. | Valid scored result, but far below 0.943. Leave unselected. |
| Constant-0.5 fallback | Logs showed `VALID: 3 studies x 12 targets`, 470-byte CSV for visible sample. | Format test only, not competitive. |
| Public S6 ConvNeXt candidate | Copy opened in the user's Kaggle workspace; screenshot showed competition plus three model/data inputs. | Not confirmed as our own scored submission. Author reports 0.950, which is not our score. |
| Local automated tests | `git diff --check` clean; `python -m pytest -q`: **48 passed in 5.11 seconds**. | Project test suite passed after GitHub sync. |

## Baseline diagnosis

Inspecting `kaggle/rsna_knee_submission.ipynb` shows:

- `NUM_SLICES = 8`, `IMAGE_SIZE = 160`.
- Small CNN trained from scratch, with no pretrained image features.
- Four epochs for both diagnostic and final fit.
- One selected fluid-sensitive series per study.
- Mean pooling over slices.
- Multilingual keyword/regular-expression weak labels encoded as 0.90/0.10 and weighted at 0.15.
- Series-metadata fallback for image decoding failures.
- DICOM slices ordered with `ImagePositionPatient` projected onto the slice normal where available, then `InstanceNumber`/enumeration fallback.

These design choices plausibly limit performance, but the score alone does not prove a single root cause. Full analysis: [experiment diagnosis](experiment-diagnosis.md).

## Original research added

A new CPU-only, Internet-disabled [`RSNA Knee Weak Label Audit`](../kaggle/rsna_knee_weak_label_audit/) notebook and [research protocol](weak-label-audit-method.md) have been added to evaluate our current report-rule labels against the expert-labelled training subset. This is a diagnostic only; it has not yet been run on Kaggle in the evidence captured here, so no audit metrics are reported yet. Four unit tests were added for explicit positive, negative, unknown, and sentence-scoped negation cases against the actual parser in the baseline notebook. They still need to be run after syncing this latest commit.

## Recommended next steps

1. Preserve the 0.943 selected entry.
2. If using the S6 public notebook, retain credits/licences and clearly state it is a reproduction.
3. Wait for our own S6 copy's hidden-test evaluation and score before considering it.
4. Do not spend a final slot on the constant-0.5 fallback or select the 0.636 baseline.
5. Avoid unvalidated changes to the 0.943 notebook.

## Competition requirements

The [official evaluation page](https://www.kaggle.com/competitions/rsna-knee-abnormality-detection/overview/evaluation) and [rules](https://www.kaggle.com/competitions/rsna-knee-abnormality-detection/rules) require notebook-based scoring, Internet disabled, a file named `submission.csv`, no more than nine hours runtime, and macro ROC AUC over twelve targets. Kaggle replaces the three-study visible test sample with hidden test data during scoring. A successful visible-sample run does not prove hidden-test performance.

## Provenance

The reference ensemble and potential S6 candidate reuse public community code and third-party assets. Preserve source credits and each asset's licence. The S6 author reports 0.950 public AUC and CC BY-NC 4.0 S6 weights; neither the score nor the weights should be represented as original work. See [model provenance](model-provenance.md).
