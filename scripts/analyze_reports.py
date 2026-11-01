from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
TRAIN_FILE = PROJECT_ROOT / "data" / "raw" / "train.csv"

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


def main():
    train = pd.read_csv(TRAIN_FILE)

    labeled = train[train[TARGETS].notna().any(axis=1)]
    unlabeled = train[train[TARGETS].isna().all(axis=1)]

    labeled_report_missing = labeled["Report"].isna().sum()
    unlabeled_report_missing = unlabeled["Report"].isna().sum()

    labeled_lengths = labeled["Report"].fillna("").str.len()
    unlabeled_lengths = unlabeled["Report"].fillna("").str.len()

    print("=" * 80)
    print("REPORT ANALYSIS")
    print("=" * 80)

    print(f"Total studies: {len(train)}")
    print(f"Labeled studies: {len(labeled)}")
    print(f"Unlabeled studies: {len(unlabeled)}")

    print("\n" + "=" * 80)
    print("REPORT AVAILABILITY")
    print("=" * 80)

    print(f"Labeled reports missing: {labeled_report_missing}")
    print(f"Unlabeled reports missing: {unlabeled_report_missing}")

    print("\n" + "=" * 80)
    print("REPORT LENGTH")
    print("=" * 80)

    print("\nLabeled:")
    print(labeled_lengths.describe())

    print("\nUnlabeled:")
    print(unlabeled_lengths.describe())

    print("\n" + "=" * 80)
    print("LABELED REPORT EXAMPLES")
    print("=" * 80)

    for i, (_, row) in enumerate(labeled.head(3).iterrows(), 1):
        print(f"\n--- Labeled report {i} ---")
        print(row["Report"][:1500])

    print("\n" + "=" * 80)
    print("UNLABELED REPORT EXAMPLES")
    print("=" * 80)

    for i, (_, row) in enumerate(unlabeled.head(3).iterrows(), 1):
        print(f"\n--- Unlabeled report {i} ---")
        print(row["Report"][:1500])


if __name__ == "__main__":
    main()
