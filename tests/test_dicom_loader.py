from pathlib import Path

import numpy as np
import pytest

from src.data.dicom_loader import load_dicom_series


SERIES_DIR = Path("data/raw/inspection/series_214978")


@pytest.mark.skipif(
    not SERIES_DIR.is_dir(),
    reason="local DICOM inspection data is not included in Git",
)
def test_load_dicom_series():
    volume, metadata = load_dicom_series(SERIES_DIR)

    # Volume structure
    assert isinstance(volume, np.ndarray)
    assert volume.ndim == 3
    assert volume.shape == (30, 320, 320)

    # Data type
    assert volume.dtype == np.uint16

    # Metadata
    assert metadata["num_slices"] == 30
    assert metadata["rows"] == 320
    assert metadata["columns"] == 320

    # Pixel spacing
    assert metadata["pixel_spacing"] == [0.5, 0.5]

    # DICOM identifiers
    assert metadata["study_instance_uid"] is not None
    assert metadata["series_instance_uid"] is not None


def test_missing_dicom_series_raises_clear_error(tmp_path):
    missing = tmp_path / "missing-series"
    with pytest.raises(FileNotFoundError, match="No DICOM files found"):
        load_dicom_series(missing)
