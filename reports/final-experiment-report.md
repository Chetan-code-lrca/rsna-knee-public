# RSNA Knee Abnormality Detection — Final Experiment Report

**Project:** RSNA Knee Abnormality Detection  
**Report updated:** 2026-10-27 (IST)  
**Repository:** [this release repository](.)  
**Purpose:** Record the work completed, observed competition results, research findings, provenance, and remaining caveats.

> **Scope note:** This is a research/competition prototype, not a clinical diagnostic system. The competition has completed; public and final/private results are recorded separately.

## 1. Outcome at a glance

Two evaluated submissions occupied the available Kaggle selection slots (**2/2**). The competition has completed; final leaderboard screenshots were reviewed on 2026-10-27.

| Candidate | Observed public AUC | Selection | Interpretation |
|---|---:|---|---|
| S6 ConvNeXt reproduction/adaptation | **0.950** | Selected | Highest observed public score; based on attributed public work and third-party weights. |
| Reference ensemble evaluation | **0.943** | Selected | Second selected candidate and known-good fallback. Also adapts public community code/assets. |
| Original weak-supervision baseline | **0.636** | Not selected | Valid scored experiment; underperformed both selected candidates. |
| Constant-0.5 safe fallback | No meaningful competitive score | Not selected | Format/schema smoke test only; every target was 0.5. |

The S6 public score is **our submission's recorded score**, not an independently developed model result. The original S6 author also published a 0.950 public result; credit for the underlying notebook, model weights and external assets must remain explicit. See [the source notebook](https://www.kaggle.com/code/nartaa/rsna-knee-s6fall-solo) and [the author's competition post](https://www.kaggle.com/competitions/rsna-knee-abnormality-detection/discussion/749359).

The 0.007 gap between 0.950 and 0.943 is a small public-score difference. The final/private leaderboard reported participant/team rank **2,381** with score **0.935**, while the public leaderboard showed rank **2,465** with score **0.950**. Do not interpret the final private score as the individually measured private AUC of either submission: the screenshot shows the participant/team leaderboard row, not a separate private score for each notebook.

## 2. Project goal and metric

The task predicts probabilities for twelve findings per knee MRI study: ACL, MCL, Medial Meniscus, Lateral Meniscus, Medial OA, Lateral OA, PF OA, Effusion, Synovitis, Baker's, Contusion and Fracture. The official metric is the macro-average ROC AUC across the twelve targets.

Official references:
- [Competition overview and metric](https://www.kaggle.com/competitions/rsna-knee-abnormality-detection/overview)
- [Evaluation and notebook requirements](https://www.kaggle.com/competitions/rsna-knee-abnormality-detection/overview/evaluation)
- [Competition rules](https://www.kaggle.com/competitions/rsna-knee-abnormality-detection/rules)

## 3. What was built and tested

### 3.1 Original repository baseline

The repository contains data utilities, DICOM preprocessing and ordering, study-level splitting, training/evaluation/prediction helpers, report-derived weak supervision, tests and Kaggle workflows.

The baseline notebook (`kaggle/rsna_knee_submission.ipynb`) selects one fluid-sensitive series, samples eight slices resized to 160×160, trains a small CNN from scratch for four epochs, averages slice features, and uses multilingual keyword/regular-expression rules over training reports. Weak targets are represented as 0.90/0.10 and weighted at 0.15. Series metadata is used as a fallback when image decoding fails. Slice ordering uses projected `ImagePositionPatient` when available and falls back to `InstanceNumber`/enumeration.

**Observed public AUC: 0.636.** This is a valid submission result but not a competitive option relative to the selected candidates. Likely bottlenecks—small scratch CNN, coarse slice sampling, uniform aggregation, noisy weak labels and one-series selection—are hypotheses based on code inspection, not proven causes from controlled ablations. See [baseline diagnosis](experiment-diagnosis.md).

### 3.2 Weak-label quality audit

A separate CPU-only, Internet-disabled audit notebook compared the existing report rules against the fully expert-labelled training subset. It read `train.csv` only and did not inspect test reports or train a new model.

Observed audit:
- 4,407 training studies and 24,371 training series in the dataset.
- 58 studies with all twelve expert labels.
- 214 of 696 target-study pairs covered by a rule (**30.7% coverage**).
- Accuracy among covered pairs: **72.4%**.

The results differ by target. Fracture was 16/16 correct among covered pairs, but this sample is too small to establish general reliability. PF OA was correct on only 1 of 5 covered pairs; medial meniscus had 9 false positives among 22 covered pairs; effusion had 11 false positives among 39; and contusion had 9 false positives among 22. Several targets report recall 1.0 only within the rule-covered subset; it is **not** full-dataset sensitivity.

Conclusion: the original text rules are partial, noisy weak-label generators. Do not treat them as authoritative labels or describe this audit as independent external validation. Full table and limitations: [weak-label audit results](weak-label-audit-results.md); protocol: [weak-label audit method](weak-label-audit-method.md).

### 3.3 S6 ConvNeXt reproduction/adaptation

The copied Kaggle notebook `chetaninaganti/rsna-knee-s6fall-solo` completed a visible-sample run and subsequently received a **0.950 public competition score** in its own evaluated submission. The execution log showed two inference paths completed, no internal fallback predictions, and a `submission.csv` written. The visible sample contained only three studies; the public competition score came from Kaggle's separate hidden-test scoring process, not those three rows alone.

This entry is a **reproduction/adaptation of public work**, not an original architecture or independently created set of weights. The source notebook and its discussion identify third-party model assets; the S6 weight set is reported under **CC BY-NC 4.0**. See the provenance record and retain all source notices. In a portfolio, describe the work as a reproduction/adaptation and state exactly what you changed, tested and contributed.

## 4. Reproducibility and verification

Observed local repository checks after syncing the latest project documentation:
- `git diff --check`: clean at the last recorded check.
- `python -m pytest -q`: **52 passed** (6.59 seconds on 2026-10-27, before the final release-cleanup commit).

These tests cover repository helpers and the report-label parser. They do not verify the hidden test labels or prove model generalization. The audit notebook completed on Kaggle, printed per-target metrics, passed its metric sanity checks and wrote `weak_label_audit.csv`.

The public release was subsequently revalidated on 2026-11-01 by [GitHub Actions run #3](https://github.com/Chetan-code-lrca/rsna-knee-public/actions/runs/41277223052): Python compilation and CLI smoke tests passed, followed by **50 unit tests passed and 2 skipped**. This is the current public CI result; the 52-test figure above is retained as a historical local run from 2026-10-27.

The individual public scores are evidenced by the Kaggle Submissions page; the participant/team public and private ranks/scores are evidenced by leaderboard screenshots reviewed on 2026-10-27. The original screenshots are in the project conversation; preserve local copies for portfolio records.

## 5. Attribution and licence disclosure

- **S6 notebook:** [nartaa/rsna-knee-s6fall-solo](https://www.kaggle.com/code/nartaa/rsna-knee-s6fall-solo).
- **S6 weight source:** [nartaa/rsna-knee-s6fall-weights](https://www.kaggle.com/models/nartaa/rsna-knee-s6fall-weights); source states CC BY-NC 4.0.
- **Related source discussion:** [0.950 S6 result and asset notes](https://www.kaggle.com/competitions/rsna-knee-abnormality-detection/discussion/749359).
- **Reference ensemble:** [our submitted notebook](https://www.kaggle.com/code/chetaninaganti/rsna-knee-reference-ensemble-candidate), an adaptation using public community code/assets; preserve the credits listed there.
- **Competition licence guidance:** consult the [official rules](https://www.kaggle.com/competitions/rsna-knee-abnormality-detection/rules) and [host discussion on external data/models](https://www.kaggle.com/competitions/rsna-knee-abnormality-detection/discussion/733965).

Do not strip notices, imply third-party weights are ours, or release incompatible assets as if they had an unrestricted licence. If asked to disclose an original contribution, distinguish the original repository utilities, the weak-label audit and its analysis from the adopted competition models and weights.

## 6. Final status and publication note

The competition has completed. The Kaggle public leaderboard screenshot showed rank **2,465** with public AUC **0.950**. The private/final participant-team leaderboard showed rank **2,381** with score **0.935**. See [final competition results](competition-final-results-2026-10-27.md).

Both selected candidates were S6 (0.950 public AUC) and Reference Ensemble (0.943 public AUC). Treat 0.935 as the final participant/team private leaderboard score, not a separately verified private AUC for either notebook.

The root MIT licence applies only to original code and documentation covered by its scope. Third-party notebooks, weights, datasets and external assets retain their own terms. Preserve all source credits and licence notices.

For portfolio use, describe this as a knee-MRI classification research project with an original baseline and weak-label audit plus credited reproductions/adaptations. Do not claim the S6 model itself was created from scratch. The project is a research prototype, not a clinical diagnostic system.

This report is included in a clean public source snapshot. The original development repository and its full Git history remain private; the snapshot was exported from tracked files only and excludes the original history and ignored local candidate folders. Gitleaks scans and tests were run as release checks, but they are not guarantees. Keep the original development repository private and maintain this separate public release repository for future updates.
