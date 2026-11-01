# RSNA Knee Safe Fallback

Purpose: emergency CPU-only fallback to create a structurally valid `submission.csv` based on the live competition `test.csv`. Every target is set to 0.5. This is **not a trained model** and should be used only as a submission-format/deadline fallback if the stronger inference notebook cannot run.

## Verified Kaggle run

Kaggle kernel: [RSNA Knee Safe Fallback Submission](https://www.kaggle.com/code/chetaninaganti/rsna-knee-safe-fallback-submission)

Run completed with `VALID: 3 studies x 12 targets` and generated `/kaggle/working/submission.csv` (470 bytes) for the currently visible three-row sample. This verifies format generation only; it does not verify performance on the hidden test set or produce a competitive score.

## Push with Kaggle CLI

From WSL:

```bash
cd ~/projects/rsna-knee/kaggle/rsna_knee_safe_fallback
kaggle kernels push -p .
```

The kernel metadata requests CPU, internet disabled, and the RSNA competition as the input. When complete, verify that `/kaggle/working/submission.csv` exists and submit through the notebook's **Submit to competition** control.
