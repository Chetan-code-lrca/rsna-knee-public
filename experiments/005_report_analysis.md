# Experiment 005 — Radiology Report Analysis

## Date

2026-08-09

## Objective

Determine whether the radiology reports provide useful information for the
multimodal knee abnormality detection task.

We specifically investigated:

- report availability
- report length
- labeled vs. unlabeled reports
- report structure
- clinical terminology
- language diversity
- correspondence between report content and competition targets

---

## Dataset

The training dataset contains:

- 4,407 studies
- 58 studies with target labels
- 4,349 studies without target labels

Every study has a radiology report.

---

## Findings

### Report availability

| Group | Studies | Missing reports |
|---|---:|---:|
| Labeled | 58 | 0 |
| Unlabeled | 4,349 | 0 |

Therefore, reports are available for both labeled and unlabeled studies.

---

## Report length

### Labeled

- Mean: approximately 1,305 characters
- Median: approximately 1,206 characters
- Minimum: 183 characters
- Maximum: 3,891 characters

### Unlabeled

- Mean: approximately 1,095 characters
- Median: approximately 974 characters
- Minimum: 52 characters
- Maximum: 4,743 characters

The two groups have different distributions, but both contain substantial
radiology reports.

---

## Clinical Information

The reports contain explicit descriptions corresponding to several
competition targets.

Examples observed include:

- ACL intact / ACL abnormality
- MCL intact / MCL abnormality
- medial meniscus tear
- lateral meniscus tear
- osteoarthritis / cartilage abnormalities
- joint effusion
- synovitis
- Baker's cyst
- contusion / bone bruise
- fracture

This indicates that the text modality contains clinically relevant
information for the prediction task.

---

## Multilingual Reports

The inspected reports included multiple languages, including:

- English
- Spanish
- German

The same clinical concepts can therefore appear using different terminology
across languages.

Example:

- English: medial meniscus tear
- Spanish: rotura de menisco interno
- German: meniscus tear terminology

A future text model should therefore account for multilingual medical text.

---

## Important Observation

The unlabeled studies are not missing reports.

They contain:

- MRI studies
- radiology reports
- series metadata

but do not currently have target labels in `train.csv`.

Therefore, the role of the 4,349 unlabeled studies requires further investigation
before they are used as ordinary supervised training examples.

---

## Decision

Do not yet train a final multimodal model.

Continue dataset investigation before model development.

The next stage should determine:

1. How the unlabeled studies are intended to be used.
2. Whether additional label information can be derived legitimately.
3. How MRI series should be selected and represented.
4. How the multilingual reports should be processed.
5. How validation should be performed given only 58 labeled studies.

---

## Reproducibility

Report analysis is implemented in:

`scripts/analyze_reports.py`

Run:

```bash
python scripts/analyze_reports.py
