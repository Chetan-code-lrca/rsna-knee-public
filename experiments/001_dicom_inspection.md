# Experiment 001 — DICOM Series Inspection

**Date:** 2026-08-08

## Objective

Verify the basic path from competition metadata to readable DICOM pixel arrays before designing the preprocessing pipeline.

## Procedure

A representative training MRI series was selected using the study and series metadata. The series files were downloaded from the competition source and inspected with pydicom. The slices were visualized together to check that the series showed an ordered progression through the knee anatomy.

No patient-level identifiers or individual study target vector are included in this report. DICOM metadata and imaging findings can be specific to the underlying study; retain those details only in private local experiment records when they are not necessary for a public explanation.

## Findings

1. DICOM instances can be read using pydicom when the required files are present.
2. Pixel data is available as a two-dimensional array for each image slice.
3. A study can contain multiple series; series can differ by anatomical plane and sequence properties.
4. The model pipeline must join study labels to series and slices without mixing data across studies.
5. Spatial metadata should be used to order slices where available rather than assuming that lexical file ordering is anatomically meaningful.

The core data mapping is:

Study → Series → Ordered Slices → Model Input → Study-level Prediction

## Decision

Proceed with reusable DICOM inspection and preprocessing utilities. Keep downloaded imaging, study identifiers, raw reports, and detailed single-study measurements out of public repository documentation unless redistribution is clearly permitted and the detail is necessary for reproducibility.
