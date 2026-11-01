from pathlib import Path

from src.datasets.split import create_study_folds


TRAIN_CSV = Path("data/raw/train.csv")


def main():
    folds = create_study_folds(
        TRAIN_CSV,
        n_splits=5,
        random_state=42,
    )

    print("=" * 60)
    print("REAL DATASET FOLD VALIDATION")
    print("=" * 60)

    print("Total labeled studies:", len(folds))
    print("\nStudies per fold:")
    print(folds["fold"].value_counts().sort_index())

    print("\nFold assignments:")
    for fold in sorted(folds["fold"].unique()):
        studies = folds.loc[
            folds["fold"] == fold,
            "StudyInstanceUID",
        ]

        print(f"Fold {fold}: {len(studies)} studies")

    print("\nUnique studies:", folds["StudyInstanceUID"].nunique())
    print("Unique folds:", folds["fold"].nunique())


if __name__ == "__main__":
    main()
