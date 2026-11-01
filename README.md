# RSNA Knee Abnormality Detection

[![Python Tests](https://github.com/Chetan-code-lrca/rsna-knee-public/actions/workflows/tests.yml/badge.svg)](https://github.com/Chetan-code-lrca/rsna-knee-public/actions/workflows/tests.yml)

Research code and experiment records for the RSNA Knee Abnormality Detection competition: predicting twelve abnormalities for each knee MRI study.

> **Research prototype only. Not for clinical diagnosis.**

## Competition outcome

The competition has completed. Based on the Kaggle leaderboard screenshots reviewed on 2026-10-27, the final participant/team result was **private rank 2,381 with score 0.935**. The public leaderboard showed **rank 2,465 with public AUC 0.950**.

Individual scored submissions recorded on the Submissions page:

| Candidate | Public AUC | Outcome |
|---|---:|---|
| S6 ConvNeXt reproduction/adaptation | **0.950** | Completed and selected |
| Reference Ensemble Evaluation | **0.943** | Completed and selected |
| Original weak-supervision baseline | 0.636 | Completed; not selected |
| Constant-0.5 fallback | No competitive score | Format/schema check only |

The private leaderboard result is the participant/team's final result; it is not a verified private score for each individual notebook. The S6 entry is an attributed reproduction/adaptation of public work and third-party weights, not an independently created architecture/checkpoint.

Read the [final competition results](reports/competition-final-results-2026-10-27.md), [final experiment report](reports/final-experiment-report.md), [model provenance and attribution](reports/model-provenance.md), [weak-label audit method](reports/weak-label-audit-method.md), [weak-label audit results](reports/weak-label-audit-results.md), [baseline diagnosis](reports/experiment-diagnosis.md), and [submission checklist](docs/competition-submission-checklist.md), and [public-release audit](reports/public-release-audit.md).

## Competition task and metric

Predict a probability for each target per `StudyInstanceUID`:

`ACL`, `MCL`, `Medial Meniscus`, `Lateral Meniscus`, `Medial OA`, `Lateral OA`, `PF OA`, `Effusion`, `Synovitis`, `Baker's`, `Contusion`, and `Fracture`.

The official metric is macro-averaged ROC AUC across the twelve target columns. See the [official evaluation page](https://www.kaggle.com/competitions/rsna-knee-abnormality-detection/overview/evaluation) and [official rules](https://www.kaggle.com/competitions/rsna-knee-abnormality-detection/rules).

## Repository layout

- `configs/`: dataset, model, training and inference configuration.
- `src/`: data loading, preprocessing, model and training helpers.
- `scripts/`: report analysis, download, training, evaluation, prediction and submission helpers.
- `tests/`: unit tests; they do not download competition data.
- `kaggle/rsna_knee_submission.ipynb`: original offline weak-supervision baseline.
- `kaggle/rsna_knee_weak_label_audit/`: CPU-only audit of report-rule labels against the expert-labelled training subset.
- `kaggle/rsna_knee_safe_fallback/`: CPU-only format fallback (constant 0.5; not competitive).
- `reports/`: experiment results, final leaderboard outcome, provenance and research methods.

Large DICOM data and checkpoints should remain outside Git unless redistribution is needed and permitted by their terms.

## Environment setup

Use Python 3.11 or newer. From Linux/WSL:

```bash
cd ~/projects/rsna-knee
conda env create -f environment.yml
conda activate rsna-knee
python -m pip install -r requirements.txt
```

If the Conda environment already exists, activate it instead of recreating it.

## Dataset and research findings

The audit found 4,407 training studies and 24,371 training series, but only 58 studies with all twelve expert labels. The report-based weak-label audit covered 214/696 target-study pairs (30.7%) and achieved 72.4% accuracy among covered pairs. Those values are conditional on rule coverage and are not full-dataset sensitivity estimates. See [the complete audit](reports/weak-label-audit-results.md).

## Train, evaluate, predict

```bash
python -m scripts.train
python -m scripts.evaluate --checkpoint outputs/baseline/fold_0/best.pt
python -m scripts.predict --checkpoint outputs/baseline/fold_0/best.pt
python -m scripts.submit --template data/raw/sample_submission.csv --predictions outputs/predictions.csv --output outputs/submission.csv
```

Review `configs/` and `scripts/` for supported options. The local training workflow is distinct from the attributed S6 and Reference Ensemble Kaggle submissions.

## Tests

```bash
git diff --check
python -m pytest -q
```

Latest user-reported local result on 2026-10-27: **52 tests passed in 6.59 seconds**. This validates repository behaviour covered by the test suite, not hidden-test competition performance.

## Responsible reuse and interpretation

- Preserve attribution for public notebooks, pretrained weights and model assets; see [model provenance](reports/model-provenance.md).
- The S6 weight source identifies its weights as [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/). Retain the notice and disclose the restriction; do not relabel the weights as our own.
- Distinguish the public AUC (0.950), final private leaderboard score (0.935), notebook execution, and CSV-format validation.
- Do not claim the competition was won or that the S6 model was developed independently.
- Do not use this research prototype for clinical diagnosis.

## Public release

This is a clean source snapshot prepared from commit 941809f7bf20 of the private development repository. The private repository's historical Git commits were not copied into this release.

The release contains original project utilities, baseline and audit code, tests, experiment documentation and attribution notes. It excludes ignored local candidate directories, raw competition data, DICOM files, and model checkpoints.

See [the release audit](reports/public-release-audit.md), [final competition results](reports/competition-final-results-2026-10-27.md), and [model provenance](reports/model-provenance.md).
