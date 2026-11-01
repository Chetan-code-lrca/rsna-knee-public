# Weak-Supervision Baseline — Diagnosis and Experiment Outcome

**Observed public score:** 0.636 (Kaggle Version #2, 2026-10-20).  
**Final participant/team leaderboard result:** public rank 2,465 / AUC 0.950; private rank 2,381 / score 0.935 (screenshots reviewed 2026-10-27).  
**Selected individual public-score candidates:** S6 reproduction/adaptation 0.950; Reference Ensemble Evaluation 0.943. The private score is a participant/team result, not verified as a separate private AUC for each individual notebook.

## What the notebook does

Source inspected: `kaggle/rsna_knee_submission.ipynb`.

- Selects one fluid-sensitive series per study.
- Samples eight evenly spaced slices and resizes to 160×160.
- Trains a small CNN from scratch for four epochs.
- Averages slice features equally.
- Uses multilingual keyword/regular-expression report extraction; weak targets become 0.90/0.10 and are weighted at 0.15.
- Uses series metadata if image decoding fails.
- Does not read test reports and has no runtime network downloads.
- Orders slices by projected `ImagePositionPatient` when available, with `InstanceNumber`/enumeration fallback.

## Plausible bottlenecks

The score does not establish any single cause. Code inspection suggests these hypotheses:

1. **Small scratch CNN:** limited visual prior given sparse expert labels.
2. **Coarse input:** eight slices at 160×160 may miss subtle anatomy.
3. **Uniform pooling:** no per-target attention over slices.
4. **Noisy pseudo-labels:** rules can miss context, negation, severity thresholds and findings not addressed in text.
5. **Only one series:** other planes/sequences are not included by the image model.

Slice ordering already uses physical position where available; that is not the first thing to change. These are source-based hypotheses, not controlled ablation results.

## Evidence from the weak-label audit

A CPU-only, Internet-disabled audit compared our unchanged report parser against the 58 fully expert-labelled training studies. It covered 214/696 target-study pairs (30.7%) and reached 72.4% accuracy among covered pairs. PF OA had 4 false positives among 5 covered cases; medial meniscus had 9/22 false positives, effusion 11/39, and contusion 9/22. Fracture was perfect on 16 covered cases, too small a sample to establish broad reliability.

These are conditional metrics among rule-covered pairs, not full-dataset recall. See [the complete audit table](weak-label-audit-results.md).

## Experiment outcome and decision

Rather than invest the remaining competition time in a large, unvalidated scratch-model rewrite, we ran a credited reproduction/adaptation of the public [S6 ConvNeXt notebook](https://www.kaggle.com/code/nartaa/rsna-knee-s6fall-solo). Our copied notebook completed a visible-sample run and its own competition evaluation returned **0.950 public AUC**. The **Reference Ensemble Evaluation** returned **0.943 public AUC**. Before competition finalization, both were selected in the two available leaderboard slots. The final leaderboard later showed participant/team private rank 2,381 at score 0.935; the public leaderboard showed rank 2,465 at score 0.950. See [final competition results](competition-final-results-2026-10-27.md).

The S6 entry uses public community work and third-party model assets, including weights reported under CC BY-NC 4.0. It must be described as a reproduction/adaptation, with all attribution and licence notices preserved. See [model provenance](model-provenance.md) and the [final experiment report](final-experiment-report.md).

## Avoid

- Replacing the selected 0.950 or 0.943 entries with the 0.636 baseline.
- Spending a selected slot on the constant-0.5 format fallback.
- Claiming the S6 author's source result or weights as original work.
- Claiming public AUC proves final/private leaderboard performance.
- Presenting the small weak-label audit as external validation.
- Applying multiple unvalidated changes to scored notebooks close to the deadline.
