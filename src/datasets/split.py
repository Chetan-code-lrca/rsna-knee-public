from pathlib import Path

import pandas as pd
from sklearn.model_selection import KFold


def get_labeled_studies(
    train_csv: str | Path,
) -> pd.DataFrame:
    """
    Return only studies that contain all 12 target labels.
    """

    train_csv = Path(train_csv)
    df = pd.read_csv(train_csv)

    targets = [
        "ACL",
        "MCL",
        "Medial Meniscus",
        "Lateral Meniscus",
        "Medial OA",
        "Lateral OA",
        "PF OA",
        "Effusion",
        "Synovitis",
        "Baker's",
        "Contusion",
        "Fracture",
    ]

    labeled = df.dropna(subset=targets).copy()

    return labeled


def create_study_folds(
    train_csv: str | Path,
    n_splits: int = 5,
    random_state: int = 42,
) -> pd.DataFrame:
    """
    Create reproducible study-level cross-validation folds.

    Each StudyInstanceUID belongs to exactly one validation fold.
    """

    labeled = get_labeled_studies(train_csv)

    if labeled["StudyInstanceUID"].duplicated().any():
        raise ValueError(
            "Duplicate StudyInstanceUID values found."
        )

    if len(labeled) < n_splits:
        raise ValueError(
            f"Cannot create {n_splits} folds from "
            f"{len(labeled)} labeled studies."
        )

    result = labeled.copy()
    result["fold"] = -1

    kfold = KFold(
        n_splits=n_splits,
        shuffle=True,
        random_state=random_state,
    )

    study_indices = result.index.to_numpy()

    for fold, (_, val_positions) in enumerate(
        kfold.split(study_indices)
    ):
        val_indices = study_indices[val_positions]
        result.loc[val_indices, "fold"] = fold

    return result
