# Competition Submission Checklist and Final Record

The RSNA Knee Abnormality Detection competition is complete. This page keeps reusable validation steps and records the final selected candidates.

## Reusable checks for future submissions

### Before running

- [ ] Confirm notebook ownership/copy source and preserve author credits.
- [ ] Review licences of code, model weights, and external data.
- [ ] Attach only permitted inputs required by the notebook.
- [ ] Disable Internet for the scored run where required by the competition.
- [ ] Choose GPU only where needed.
- [ ] Confirm expected output path and exact target-column order.

### Validate the CSV

Expected columns:

    StudyInstanceUID
    ACL
    MCL
    Medial Meniscus
    Lateral Meniscus
    Medial OA
    Lateral OA
    PF OA
    Effusion
    Synovitis
    Baker's
    Contusion
    Fracture

- [ ] Exactly one row per test study.
- [ ] Study IDs are present, unique and in expected test order.
- [ ] Exactly 12 prediction columns after the study ID.
- [ ] All target values are finite floats within [0, 1].
- [ ] Output is written to /kaggle/working/submission.csv.
- [ ] A visible three-row CSV is a smoke test only; it is not hidden-test validation.

### After submitting

- [ ] Confirm the Submissions page says Succeeded and displays a public score.
- [ ] Record notebook version, submission description, public score and date.
- [ ] Keep public and final/private leaderboard results in separate fields.
- [ ] Keep source credits and licence notes alongside the scored code/assets.
- [ ] Never attempt to access or reconstruct hidden labels.

## Final outcome (screenshots reviewed 2026-10-27)

| Measure | Result |
|---|---|
| Public leaderboard rank | **2,465** |
| Public AUC | **0.950** |
| Private/final leaderboard rank | **2,381** |
| Private/final leaderboard score | **0.935** |
| Selected slots | **2/2** |

The private score is the participant/team final leaderboard result. It is not verified as a separate private AUC for each individual notebook.

| Candidate | Individual public AUC | Outcome |
|---|---:|---|
| [S6 ConvNeXt reproduction/adaptation](https://www.kaggle.com/code/chetaninaganti/rsna-knee-s6fall-solo) | 0.950 | Selected |
| [Reference Ensemble Evaluation](https://www.kaggle.com/code/chetaninaganti/rsna-knee-reference-ensemble-candidate) | 0.943 | Selected |
| [Original weak-supervision baseline](https://www.kaggle.com/code/chetaninaganti/rsna-knee-offline-weak-supervision-baseline) | 0.636 | Not selected |
| [Safe fallback](https://www.kaggle.com/code/chetaninaganti/rsna-knee-safe-fallback-submission) | Not competitive | Format/schema check only |

S6 is an attributed reproduction/adaptation of [nartaa's public notebook](https://www.kaggle.com/code/nartaa/rsna-knee-s6fall-solo). Its weights are reported under CC BY-NC 4.0. Preserve the source credit and licence notice; do not describe the model/checkpoint as independently authored.

See [final competition results](../reports/competition-final-results-2026-10-27.md), [final experiment report](../reports/final-experiment-report.md), and [model provenance](../reports/model-provenance.md).

## Before making this repository public

- [ ] Run a dedicated all-history secret scanner on the local clone and review GitHub Actions logs/artifacts before release. A heuristic pattern audit across 63 historical commit diffs found no obvious common credential formats, but this is not a complete guarantee.
- [ ] Decide whether the historical Git author email is acceptable to expose; changing the local Git email now does not change old commits.
- [ ] Decide whether the older single-study DICOM note can remain in history. If not, prepare a clean release snapshot or rewrite history after making a private backup.
- [ ] Remove or replace empty placeholders and any study-specific values not needed for reproducibility.
- [ ] Review every notebook, commit, file, and dependency for attribution and licensing.
- [ ] Choose an explicit licence for original code that you own. Do not apply it to third-party assets.
- [ ] Review root README and final experiment report for accurate scores and provenance.
- [ ] Pull the final commit locally and run git diff --check and python -m pytest -q.
- [ ] Change repository visibility only after these checks pass.
