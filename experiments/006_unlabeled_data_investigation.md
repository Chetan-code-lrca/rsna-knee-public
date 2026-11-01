# Experiment 006 — Labeled vs Unlabeled Series Analysis

## Date

2026-08-09

## Objective

Determine whether the labeled and unlabeled studies have substantially
different MRI series structures.

This is important because the dataset contains only 58 labeled studies but
4,349 unlabeled studies. Before considering the unlabeled data for
representation learning or other purposes, we need to determine whether it
appears structurally compatible with the labeled data.

---

## Results

| Metric | Labeled | Unlabeled |
|---|---:|---:|
| Studies | 58 | 4,349 |
| Series | 336 | 24,035 |
| Mean series/study | 5.79 | 5.53 |
| Median series/study | 5 | 5 |
| Minimum | 4 | 3 |
| Maximum | 9 | 14 |

---

## Series Count Distribution

| Series per study | Labeled | Unlabeled |
|---:|---:|---:|
| 3 | 0 | 1 |
| 4 | 8 | 667 |
| 5 | 24 | 2,275 |
| 6 | 12 | 686 |
| 7 | 6 | 304 |
| 8 | 2 | 143 |
| 9 | 6 | 170 |
| 10 | 0 | 74 |
| 11 | 0 | 21 |
| 12 | 0 | 5 |
| 13 | 0 | 2 |
| 14 | 0 | 1 |

---

## Findings

The labeled and unlabeled groups have similar overall MRI series structure.

The mean number of series per study is:

- Labeled: 5.79
- Unlabeled: 5.53

Both groups have a median of 5 series per study.

The most common series counts are also similar, particularly 5 and 6
series per study.

The unlabeled dataset contains a small number of studies with more than
9 series, while the labeled dataset does not.

---

## Interpretation

There is no obvious evidence from series-count statistics alone that the
labeled and unlabeled studies represent fundamentally different acquisition
structures.

Therefore, the unlabeled studies may be useful for future representation
learning or multimodal pretraining.

However, the unlabeled studies must not be treated as supervised examples
because their 12 target labels are missing.

Further investigation is required before selecting a training strategy.

---

## Decision

Do not download the complete DICOM dataset yet.

Next investigate the composition of the MRI series themselves, including:

1. Anatomical planes.
2. Fluid-sensitive sequences.
3. Fat-suppression patterns.
4. Number of slices per series.
5. Image dimensions.
6. Which series are most informative for the knee abnormalities.

Only after this investigation should the preprocessing and model strategy
be finalized.
