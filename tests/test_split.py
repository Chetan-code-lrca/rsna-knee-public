import pandas as pd

from src.datasets.split import (
    create_study_folds,
    get_labeled_studies,
)


TARGETS = [
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


def make_test_data() -> pd.DataFrame:
    rows = []

    for i in range(10):
        row = {
            "StudyInstanceUID": f"study_{i}",
        }

        for target in TARGETS:
            row[target] = i % 2

        rows.append(row)

    # Add one unlabeled study.
    rows.append(
        {
            "StudyInstanceUID": "unlabeled",
            **{target: None for target in TARGETS},
        }
    )

    return pd.DataFrame(rows)


def test_get_labeled_studies(tmp_path):
    csv_path = tmp_path / "train.csv"

    df = make_test_data()
    df.to_csv(csv_path, index=False)

    labeled = get_labeled_studies(csv_path)

    assert len(labeled) == 10
    assert "unlabeled" not in labeled["StudyInstanceUID"].values


def test_create_study_folds(tmp_path):
    csv_path = tmp_path / "train.csv"

    df = make_test_data()
    df.to_csv(csv_path, index=False)

    result = create_study_folds(
        csv_path,
        n_splits=5,
        random_state=42,
    )

    assert len(result) == 10
    assert result["fold"].between(0, 4).all()

    # Every study appears exactly once.
    assert result["StudyInstanceUID"].is_unique

    # Every fold contains studies.
    assert set(result["fold"]) == {0, 1, 2, 3, 4}


def test_create_study_folds_is_reproducible(tmp_path):
    csv_path = tmp_path / "train.csv"

    df = make_test_data()
    df.to_csv(csv_path, index=False)

    first = create_study_folds(
        csv_path,
        n_splits=5,
        random_state=42,
    )

    second = create_study_folds(
        csv_path,
        n_splits=5,
        random_state=42,
    )

    assert first["fold"].tolist() == second["fold"].tolist()
