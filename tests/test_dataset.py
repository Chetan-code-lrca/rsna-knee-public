from pathlib import Path

import numpy as np
import pandas as pd
import pytest
import torch

from src.datasets.dataset import TARGETS, KneeStudyDataset
from src.preprocessing.dicom import load_series
from src.preprocessing.normalization import percentile_normalize
from src.preprocessing.transform import resize_slice


@pytest.mark.skipif(
    not Path("data/raw/inspection/series_107918").is_dir(),
    reason="local DICOM inspection data is not included in Git",
)
def test_real_sagittal_series_pipeline():
    series_dir = Path("data/raw/inspection/series_107918")
    volume, metadata = load_series(series_dir)

    assert volume.shape == (33, 400, 400)
    assert volume.dtype == np.uint16

    processed = []
    for slice_image in volume:
        normalized = percentile_normalize(slice_image)
        processed.append(resize_slice(normalized, (224, 224)))

    tensor = torch.from_numpy(np.stack(processed, axis=0).astype(np.float32))
    assert tensor.shape == (33, 224, 224)
    assert tensor.dtype == torch.float32
    assert torch.isfinite(tensor).all()
    assert tensor.min() >= 0.0
    assert tensor.max() <= 1.0
    assert metadata["num_slices"] == 33


def _write_metadata(tmp_path: Path):
    studies_path = tmp_path / "train.csv"
    series_path = tmp_path / "train_series.csv"
    row = {"StudyInstanceUID": "study-1", "Report": "test"}
    row.update({target: 1 for target in TARGETS})
    pd.DataFrame([row]).to_csv(studies_path, index=False)
    pd.DataFrame(
        {
            "StudyInstanceUID": ["study-1"],
            "SeriesInstanceUID": ["coronal-1"],
            "Fluid_Sensitive": [1],
            "Anatomical_Plane": ["Coronal"],
        }
    ).to_csv(series_path, index=False)
    return studies_path, series_path


def test_dataset_samples_fixed_number_of_slices_and_falls_back_plane(
    tmp_path, monkeypatch
):
    studies_path, series_path = _write_metadata(tmp_path)
    volume = np.arange(12 * 8 * 8, dtype=np.float32).reshape(12, 8, 8)
    monkeypatch.setattr(
        "src.datasets.dataset.load_series",
        lambda _path: (volume, {"num_slices": len(volume)}),
    )

    dataset = KneeStudyDataset(
        train_csv=studies_path,
        series_csv=series_path,
        dicom_root=tmp_path / "dicom",
        target_size=(8, 8),
        plane="Sagittal",
        num_slices=4,
    )
    item = dataset[0]

    assert item["image"].shape == (4, 8, 8)
    assert item["image"].dtype == torch.float32
    assert item["plane"] == "Coronal"
    assert item["series_uid"] == "coronal-1"
    assert item["label"].shape == (12,)
    assert torch.isfinite(item["image"]).all()


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
    pd.DataFrame({"StudyInstanceUID": ["study-1"]}).to_csv(
        studies_csv, index=False
    )
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
