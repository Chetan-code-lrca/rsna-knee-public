import pandas as pd
import pytest

from src.datasets.dataset import TARGETS, KneeStudyDataset


def test_inference_dataset_accepts_unlabeled_study_metadata(tmp_path):
    studies_csv = tmp_path / "test.csv"
    series_csv = tmp_path / "test_series.csv"
    pd.DataFrame({"StudyInstanceUID": ["study-1", "study-2"]}).to_csv(
        studies_csv, index=False
    )
    pd.DataFrame(
        {
            "StudyInstanceUID": ["study-1", "study-2"],
            "SeriesInstanceUID": ["series-1", "series-2"],
            "Fluid_Sensitive": [1, 1],
            "Anatomical_Plane": ["Sagittal", "Sagittal"],
        }
    ).to_csv(series_csv, index=False)

    dataset = KneeStudyDataset(
        train_csv=studies_csv,
        series_csv=series_csv,
        dicom_root=tmp_path / "test",
        include_unlabeled=True,
    )

    assert len(dataset) == 2
    assert dataset.studies == ["study-1", "study-2"]


def test_training_dataset_requires_all_label_columns(tmp_path):
    studies_csv = tmp_path / "test.csv"
    series_csv = tmp_path / "test_series.csv"
    pd.DataFrame({"StudyInstanceUID": ["study-1"]}).to_csv(studies_csv, index=False)
    pd.DataFrame(
        {
            "StudyInstanceUID": ["study-1"],
            "SeriesInstanceUID": ["series-1"],
            "Fluid_Sensitive": [1],
            "Anatomical_Plane": ["Sagittal"],
        }
    ).to_csv(series_csv, index=False)

    with pytest.raises(ValueError, match="include_unlabeled=True"):
        KneeStudyDataset(
            train_csv=studies_csv,
            series_csv=series_csv,
            dicom_root=tmp_path / "test",
        )


def test_target_count_remains_aligned_with_competition_schema():
    assert len(TARGETS) == 12



def test_inference_mode_omits_labels_even_for_labeled_rows(tmp_path, monkeypatch):
    import numpy as np
    import torch

    studies_csv = tmp_path / "labeled.csv"
    series_csv = tmp_path / "series.csv"
    row = {"StudyInstanceUID": "study-1"}
    row.update({target: 1 for target in TARGETS})
    pd.DataFrame([row]).to_csv(studies_csv, index=False)
    pd.DataFrame(
        {
            "StudyInstanceUID": ["study-1"],
            "SeriesInstanceUID": ["series-1"],
            "Fluid_Sensitive": [1],
            "Anatomical_Plane": ["Sagittal"],
        }
    ).to_csv(series_csv, index=False)
    monkeypatch.setattr(
        "src.datasets.dataset.load_series",
        lambda _path: (np.arange(32, dtype=np.float32).reshape(2, 4, 4), []),
    )
    dataset = KneeStudyDataset(
        train_csv=studies_csv,
        series_csv=series_csv,
        dicom_root=tmp_path / "dicom",
        target_size=(8, 8),
        plane="Sagittal",
        include_unlabeled=True,
    )

    item = dataset[0]

    assert "label" not in item
    assert item["image"].shape == (2, 8, 8)
