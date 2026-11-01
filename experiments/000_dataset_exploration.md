# Experiment 000 — Dataset Exploration

## Date

2026-08-08

## Objective

Understand the structure of the RSNA Knee Abnormality Detection dataset before downloading the full MRI dataset.

## Findings

- 4,407 training studies
- 24,371 training series
- 5.53 average series per study
- 58 studies currently contain target labels
- 4,349 studies have missing target labels
- Each study maps correctly between `train.csv` and `train_series.csv`
- Series contain anatomical plane, fluid-sensitive and fat-suppression metadata
- Radiology reports are multilingual

## Decision

Do not download the complete DICOM dataset yet.

Next step is to inspect one labeled study and one or more of its DICOM series.