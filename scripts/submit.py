"""Fill a study-level competition submission template with predictions."""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

from src.datasets.dataset import TARGETS


def validate_prediction_values(predictions: pd.DataFrame) -> pd.DataFrame:
    """Require finite numeric probability values for all 12 targets."""
    values = predictions[TARGETS].apply(pd.to_numeric, errors="coerce")
    matrix = values.to_numpy(dtype=np.float64)
    if not np.isfinite(matrix).all():
        raise ValueError("Prediction values must be finite numeric probabilities.")
    if ((matrix < 0.0) | (matrix > 1.0)).any():
        raise ValueError("Prediction values must be within [0, 1].")
    validated = predictions.copy()
    validated.loc[:, TARGETS] = values
    return validated


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--template", default="data/raw/sample_submission.csv")
    parser.add_argument("--predictions", default="outputs/predictions.csv")
    parser.add_argument("--output", default="outputs/submission.csv")
    args = parser.parse_args()

    template_path = Path(args.template)
    predictions_path = Path(args.predictions)
    output_path = Path(args.output)
    if not template_path.is_file():
        raise FileNotFoundError(f"Submission template not found: {template_path}")
    if not predictions_path.is_file():
        raise FileNotFoundError(f"Prediction file not found: {predictions_path}")

    template = pd.read_csv(template_path)
    predictions = pd.read_csv(predictions_path)
    if "StudyInstanceUID" not in template.columns or "StudyInstanceUID" not in predictions.columns:
        raise ValueError("Both files must contain StudyInstanceUID.")
    missing_targets = [target for target in TARGETS if target not in template.columns]
    if missing_targets:
        raise ValueError(f"Submission template is missing targets: {missing_targets}")
    missing_prediction_targets = [target for target in TARGETS if target not in predictions.columns]
    if missing_prediction_targets:
        raise ValueError(f"Predictions are missing targets: {missing_prediction_targets}")
    predictions = validate_prediction_values(predictions)
    if predictions["StudyInstanceUID"].duplicated().any():
        raise ValueError("Predictions contain duplicate StudyInstanceUID values.")

    lookup = predictions.copy()
    lookup["StudyInstanceUID"] = lookup["StudyInstanceUID"].astype(str)
    lookup = lookup.set_index("StudyInstanceUID")
    template_uids = template["StudyInstanceUID"].astype(str)
    missing_studies = sorted(set(template_uids) - set(lookup.index))
    if missing_studies:
        raise ValueError(
            f"Predictions are missing {len(missing_studies)} template studies; "
            f"first missing UID: {missing_studies[0]}"
        )
    aligned = lookup.loc[template_uids, TARGETS].reset_index(drop=True)
    template.loc[:, TARGETS] = aligned.to_numpy()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    template.to_csv(output_path, index=False)
    print(f"Wrote submission with {len(template)} rows to {output_path}")


if __name__ == "__main__":
    main()
