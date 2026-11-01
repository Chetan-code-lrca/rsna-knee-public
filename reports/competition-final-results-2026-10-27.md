# RSNA Knee Abnormality Detection — Final Competition Results

**Recorded:** 2026-10-27 (IST)  
**Competition status:** Completed (Kaggle Private leaderboard displayed “This competition has completed. This leaderboard reflects the final standings.”)  
**Source repository status:** The original development repository remains private; this report is included in a separate clean release snapshot.

## Final leaderboard evidence

The screenshots provided from the Kaggle leaderboard show:

| Leaderboard | Rank | Score | Submission context |
|---|---:|---:|---|
| Public | **2,465** | **0.950 AUC** | Chetan Inaganti's public leaderboard row. Kaggle marked this as a new personal best. |
| Private / final | **2,381** | **0.935 AUC** | Chetan Inaganti's final leaderboard row. |

The private leaderboard row is the final leaderboard result for the participant/team and should **not** be represented as a separately verified private score for each individual submission. The individual submission scores confirmed on the Submissions page were:

| Candidate | Public AUC | Outcome |
|---|---:|---|
| S6 ConvNeXt reproduction/adaptation | **0.950** | Evaluated and selected |
| Reference Ensemble Evaluation | **0.943** | Evaluated and selected |
| Original weak-supervision baseline | 0.636 | Evaluated; not selected |
| Constant-0.5 fallback | No competitive score | Format/schema test only |

The two chosen submissions occupied both selection slots (2/2). The selected S6 entry is an attributed reproduction/adaptation of public work and third-party weights, not an independently created ConvNeXt model.

## Interpretation

- The public score of 0.950 and final/private score of 0.935 differ by 0.015. Public and private leaderboards use different test subsets, so this gap is a result to report—not evidence by itself of a specific technical failure.
- The final private rank was 2,381. We did not achieve a top-ranked finish or win the competition.
- The S6 submission improved the public score by 0.007 over the Reference Ensemble's 0.943, but we cannot claim that its individual private score was 0.935 from the available leaderboard screenshot.
- The original baseline's 0.636 result and the weak-label audit remain useful engineering/research evidence. The audit found rule coverage of 30.7% and 72.4% accuracy among covered target-study pairs; these are conditional diagnostic metrics from only 58 fully expert-labelled studies, not broad validation.
- Local repository checks passed 52 tests on 2026-10-27's prior recorded sync (latest run shown by the user: 52 passed in 5.42 seconds).

## What went well

1. We completed and recorded multiple end-to-end competition submission attempts.
2. We retained a known-good reference candidate and tested a stronger public S6 solution instead of abandoning the baseline without evidence.
3. We created a reproducible weak-label audit, tested report-label parsing and documented the small-sample limitations.
4. We verified the repository's test suite and added status, experiment and provenance documentation.

## What did not work as hoped

1. The original scratch-CNN/weak-supervision baseline scored 0.636, far below the selected entries.
2. The S6 result came from public community work and third-party weights; it must not be presented as an original model design.
3. A public AUC of 0.950 translated to a final/private leaderboard score of 0.935, and the final rank was 2,381.
4. The weak-label audit demonstrated that the text rules have limited coverage and target-specific false positives; they were not enough to justify a strong original model claim.

## Portfolio wording

A careful project summary is:

> Built and tested a knee-MRI abnormality-detection research pipeline for the RSNA Kaggle competition. Implemented an offline weak-supervision baseline and a report-rule audit against the 58 fully expert-labelled training studies; documented 30.7% rule coverage and 72.4% accuracy among covered target-study pairs. Evaluated attributed public model adaptations, achieving a 0.950 public AUC and final private leaderboard score of 0.935 (rank 2,381). Repository validation passed 52 tests. Public model and weight credits/licences are documented; this was a reproduction/adaptation rather than an independently authored top-performing architecture.

Use “public AUC” and “final private leaderboard score” distinctly. Do not state that the baseline scored 0.950, that the model was developed entirely from scratch, or that the competition was won.

## Publication note

This report is distributed as part of a clean public source snapshot. The original development repository and its historical commits remain private. Do not change the original repository's visibility; maintain the separate public release repository after reviewing future changes.
