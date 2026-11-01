from pathlib import Path

import numpy as np
import pandas as pd
import torch
from torch.utils.data import Dataset

from src.preprocessing.dicom import load_series
from src.preprocessing.normalization import percentile_normalize
from src.preprocessing.slices import select_evenly_spaced_slices
from src.preprocessing.transform import resize_slice


PLANES = ("Sagittal", "Coronal", "Axial")

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


def select_fluid_sensitive_series(
    series_df: pd.DataFrame,
    study_uid: str,
) -> dict[str, str | None]:
    """Select one fluid-sensitive series for each anatomical plane."""

    study = series_df[
        (series_df["StudyInstanceUID"].astype(str) == str(study_uid))
        & (series_df["Fluid_Sensitive"] == 1)
    ].copy()

    selected: dict[str, str | None] = {}
    for plane in PLANES:
        candidates = study[
            study["Anatomical_Plane"] == plane
        ].sort_values("SeriesInstanceUID")

        selected[plane] = (
            str(candidates.iloc[0]["SeriesInstanceUID"])
            if not candidates.empty
            else None
        )

    return selected


def get_study_labels(
    train_df: pd.DataFrame,
    study_uid: str,
) -> list[float]:
    """Return the 12 abnormality labels for a study."""

    rows = train_df[
        train_df["StudyInstanceUID"].astype(str) == str(study_uid)
    ]
    if rows.empty:
        raise ValueError(f"Study not found: {study_uid}")

    values = rows.iloc[0][TARGETS]
    if values.isna().any():
        raise ValueError(f"Missing labels for study: {study_uid}")

    return values.astype(float).tolist()


class KneeStudyDataset(Dataset):
    """Study-level MRI dataset for multi-label classification.

    Each item contains a stack of MRI slices, optional target labels, and
    study/series identifiers. Set num_slices to sample a fixed number of
    slices before normalization and resizing. When the preferred plane is
    unavailable, the dataset falls back deterministically to the other
    fluid-sensitive planes in PLANES order.
    """

    def __init__(
        self,
        train_csv: str | Path,
        series_csv: str | Path,
        dicom_root: str | Path,
        target_size: tuple[int, int] = (224, 224),
        plane: str = "Axial",
        study_uids: set[str] | None = None,
        include_unlabeled: bool = False,
        num_slices: int | None = None,
    ):
        self.train_df = pd.read_csv(train_csv)
        self.series_df = pd.read_csv(series_csv)

        self.dicom_root = Path(dicom_root)
        self.target_size = target_size
        self.plane = plane
        self.num_slices = num_slices
        self.include_unlabeled = include_unlabeled
        self.has_label_columns = set(TARGETS).issubset(self.train_df.columns)

        if "StudyInstanceUID" not in self.train_df.columns:
            raise ValueError("Study metadata must contain StudyInstanceUID.")
        if not self.has_label_columns and not include_unlabeled:
            raise ValueError(
                "Training metadata must contain all target columns; "
                "set include_unlabeled=True for inference."
            )
        if plane not in PLANES:
            raise ValueError(
                f"Invalid plane: {plane}. Expected one of {PLANES}."
            )
        if num_slices is not None and num_slices < 1:
            raise ValueError("num_slices must be positive.")

        if include_unlabeled:
            candidates = self.train_df.dropna(
                subset=["StudyInstanceUID"]
            ).copy()
        else:
            candidates = self.train_df.dropna(subset=TARGETS).copy()

        candidates["StudyInstanceUID"] = candidates["StudyInstanceUID"].astype(str)
        if study_uids is not None:
            allowed = {str(uid) for uid in study_uids}
            candidates = candidates[
                candidates["StudyInstanceUID"].isin(allowed)
            ]
        if candidates["StudyInstanceUID"].duplicated().any():
            raise ValueError("Duplicate StudyInstanceUID values found.")

        self.studies = candidates["StudyInstanceUID"].tolist()

    def __len__(self) -> int:
        return len(self.studies)

    def __getitem__(self, index: int) -> dict:
        study_uid = self.studies[index]
        selected = select_fluid_sensitive_series(self.series_df, study_uid)

        # Prefer the configured plane. Use another fluid-sensitive plane only
        # if it is missing, rather than dropping a labeled study or crashing.
        selection_order = (self.plane,) + tuple(
            candidate for candidate in PLANES if candidate != self.plane
        )
        actual_plane = next(
            (candidate for candidate in selection_order if selected[candidate]),
            None,
        )
        if actual_plane is None:
            raise ValueError(
                f"No fluid-sensitive series found for study {study_uid} "
                f"in any supported plane {PLANES}."
            )

        series_uid = selected[actual_plane]
        series_dir = self.dicom_root / study_uid / str(series_uid)
        volume, _ = load_series(series_dir)

        if self.num_slices is not None:
            volume = select_evenly_spaced_slices(volume, self.num_slices)

        processed_slices = []
        for slice_image in volume:
            normalized = percentile_normalize(slice_image)
            resized = resize_slice(normalized, self.target_size)
            processed_slices.append(resized)

        image = torch.from_numpy(
            np.stack(processed_slices, axis=0).astype(np.float32)
        )

        result = {
            "image": image,
            "study_uid": study_uid,
            "plane": actual_plane,
            "series_uid": str(series_uid),
        }

        if self.has_label_columns and not self.include_unlabeled:
            labels = get_study_labels(self.train_df, study_uid)
            result["label"] = torch.tensor(labels, dtype=torch.float32)

        if not self.include_unlabeled and "label" not in result:
            raise ValueError(f"Missing labels for training study: {study_uid}")

        return result
