# Dataset

## Competition and metadata

This project targets the RSNA Knee Abnormality Detection competition. Competition data files are not stored in this repository.

Expected file paths are configured in configs/dataset.yml.

### Training labels

The training metadata includes:
- StudyInstanceUID
- Radiology Report
- Twelve target labels: ACL, MCL, Medial Meniscus, Lateral Meniscus, Medial OA, Lateral OA, PF OA, Effusion, Synovitis, Baker's, Contusion, and Fracture.

### Series metadata

The series table includes:
- StudyInstanceUID
- SeriesInstanceUID
- Fluid_Sensitive
- Fat_Suppression
- Anatomical_Plane

The repository dataset implementation selects a fluid-sensitive series for the configured plane. Confirm schema and values against the exact permitted competition files used for an experiment.

## Dataset-level notes

The observed dataset snapshot contained 4,407 study rows and 24,371 series rows. Fifty-eight studies had all twelve expert labels; the other 4,349 did not have complete target labels in the training table. Re-check counts against the exact dataset copy before citing them in later work.

Study-level labels map to multiple series and DICOM slices. The preprocessing pipeline must preserve the mapping:

Study → Series → Ordered Slices → Model Input → Study-level Prediction

Series metadata, image orientation, and spatial ordering matter. The repository includes DICOM loading and preprocessing utilities, but not the competition images or any trained checkpoints.

## Local data and privacy

DICOM images, patient-level labels/reports, model weights, and generated outputs must remain local unless the competition and asset licences explicitly permit redistribution. The repository ignores common local data/output paths; still review git status before committing. Never commit credentials, raw patient-level data, or derived files not allowed by the competition rules.

## Reproducible pipeline

1. Inspect the downloaded CSV schema and DICOM folder layout.
2. Create study-level validation folds; do not split slices from one study across train and validation.
3. Train the slice-wise CNN baseline on a configured plane.
4. Evaluate BCE loss and per-target AUC only where the validation fold contains both classes.
5. Generate per-study probabilities and align them to the official submission template.
6. Record dataset version, fold assignment, configuration, checkpoint provenance, and metrics for each experiment.

The committed integration tests use local DICOM inspection folders only when present. A clean checkout runs synthetic unit tests without downloading competition data.
