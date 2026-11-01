# Model Provenance, Attribution and Reuse Policy

Updated 2026-10-27 (IST). This record separates original repository work from public notebook adaptations and third-party pretrained assets.

## Summary of scored submissions

| Candidate | Our observed public AUC | Current selection | Provenance |
|---|---:|---|---|
| S6 ConvNeXt reproduction/adaptation | **0.950** | Selected | Public notebook and third-party weights/assets; not independently authored. |
| Reference Ensemble Evaluation | **0.943** | Selected | Adaptation of public community ensemble code/assets; keep all source credits. |
| Original weak-supervision baseline | 0.636 | Not selected | Baseline notebook maintained in this repository. |
| Constant-0.5 fallback | Not meaningful | Not selected | Format/schema check only. |

The final participant/team leaderboard screenshot showed **public rank 2,465 / score 0.950** and **private rank 2,381 / score 0.935**. The private score is the participant/team final leaderboard result; available evidence does not identify it as a separate private AUC for each individual notebook.

## Original repository and baseline

This repository contains data utilities, DICOM preprocessing/ordering, study-level splitting, a compact slice CNN, training/evaluation/prediction helpers, tests and report-derived weak supervision.

The baseline notebook `kaggle/rsna_knee_submission.ipynb` uses eight slices at 160×160 from one selected fluid-sensitive series, a small CNN trained from scratch for four epochs, mean aggregation of slice features, and multilingual keyword/regular-expression report-derived weak labels weighted at 0.15. Its observed public score is **0.636**. An earlier internal diagnostic was 0.469398 on only 12 validation studies with 10 evaluable targets; it is too small to support a robust performance claim.

## S6 ConvNeXt reproduction/adaptation

- **Our scored notebook:** [chetaninaganti/rsna-knee-s6fall-solo](https://www.kaggle.com/code/chetaninaganti/rsna-knee-s6fall-solo).
- **Original source:** [nartaa/rsna-knee-s6fall-solo](https://www.kaggle.com/code/nartaa/rsna-knee-s6fall-solo).
- **Original author's competition post:** [0.950 public result and asset notes](https://www.kaggle.com/competitions/rsna-knee-abnormality-detection/discussion/749359).
- **Our observed public score:** **0.950**, with the entry selected as of 2026-10-21.
- **S6 model weights:** [nartaa/rsna-knee-s6fall-weights](https://www.kaggle.com/models/nartaa/rsna-knee-s6fall-weights); source states CC BY-NC 4.0 and publishes a SHA-256 prefix `0c7297d5…371c12`.
- **Other source assets:** the source discussion/version notes identify Heliosli's anatomy checkpoint/data pipeline and additional public model weights used by the pipeline for studies not processed by the ConvNeXt path. Keep the assets and credits identified by the exact Kaggle notebook version and input list.

The scored result is a **reproduction/adaptation of public work**, not an original S6 architecture or original S6 pretrained checkpoint. Describe our contribution honestly: copying/adapting the runnable notebook in our workspace, ensuring its inputs/run/outputs were usable, obtaining our own evaluated submission, and documenting our repository baseline and weak-label audit. Only claim additional code changes if they are actually present in the notebook diff.

### Licence handling

Keep the original **CC BY-NC 4.0** notice for the S6 weights and comply with its conditions. The competition rules contain an exception for inputs or pretrained models with incompatible licences, but that is not a blanket permission to remove notices or grant third-party rights we do not own. Review the [competition rules](https://www.kaggle.com/competitions/rsna-knee-abnormality-detection/rules) and the [host's clarification on external data/models](https://www.kaggle.com/competitions/rsna-knee-abnormality-detection/discussion/733965). Clearly disclose all third-party assets in any final write-up and seek host clarification if a licence question affects prize eligibility or redistribution.

## Reference ensemble evaluation

- **Our scored notebook:** [chetaninaganti/rsna-knee-reference-ensemble-candidate](https://www.kaggle.com/code/chetaninaganti/rsna-knee-reference-ensemble-candidate).
- **Observed public AUC:** **0.943**, selected alongside S6. We do not have a separately confirmed private AUC for this notebook.
- **Provenance:** adaptation of public community ensemble code and external assets. Its notebook lists credits including Jiwel Liu, Pilkwang, Sofia Anjenie, Antoine G., prvsiyan, Marwan Mahmoud, dreaddevelopment / Roman Tamrazov, renta.k and Anvith Pothula. Check the exact notebook version and attached inputs for the complete source and licence record before redistribution.

Do not claim independent authorship of the ensemble or its weights.

## Format fallback

- **Notebook:** [RSNA Knee Safe Fallback Submission](https://www.kaggle.com/code/chetaninaganti/rsna-knee-safe-fallback-submission).
- **Evidence:** 470-byte visible-sample CSV and `VALID: 3 studies x 12 targets`.
- **Predictions:** all targets are 0.5. This is a schema check only, not a trained or competitive model.

## Integrity principles

- Preserve all source credits and licence notices.
- Distinguish our scored reproduction/adaptation from original model development.
- Keep all scoring runs Internet-disabled as required.
- Use only permitted datasets/models; never infer or reconstruct hidden labels.
- Separate visible-sample validation, successful notebook execution, individual public submission scores and the participant/team final/private leaderboard result.
- Do not represent this work as clinically validated or suitable for diagnosis.

## Official references

- [Competition evaluation](https://www.kaggle.com/competitions/rsna-knee-abnormality-detection/overview/evaluation)
- [Competition rules](https://www.kaggle.com/competitions/rsna-knee-abnormality-detection/rules)
- [S6 notebook source and assets](https://www.kaggle.com/competitions/rsna-knee-abnormality-detection/discussion/749359)
- [Host clarification on third-party external data/models](https://www.kaggle.com/competitions/rsna-knee-abnormality-detection/discussion/733965)
- [CC BY-NC 4.0 text](https://creativecommons.org/licenses/by-nc/4.0/)
