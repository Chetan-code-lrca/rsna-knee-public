from pathlib import Path

import numpy as np
import pydicom


def load_series(series_dir):
    """
    Load a DICOM series into a 3D NumPy volume.

    Parameters
    ----------
    series_dir : str or Path
        Directory containing DICOM files.

    Returns
    -------
    volume : np.ndarray
        3D volume with shape (slices, rows, columns).
    metadata : dict
        Basic metadata describing the series.
    """

    series_dir = Path(series_dir)

    files = sorted(series_dir.glob("*.dcm"))

    if not files:
        raise FileNotFoundError(
            f"No DICOM files found in: {series_dir}"
        )

    slices = []

    for file in files:
        ds = pydicom.dcmread(file)

        if not hasattr(ds, "PixelData"):
            continue

        position = np.asarray(
            ds.ImagePositionPatient,
            dtype=np.float64,
        )

        orientation = np.asarray(
            ds.ImageOrientationPatient,
            dtype=np.float64,
        )

        row_direction = orientation[:3]
        column_direction = orientation[3:]

        normal = np.cross(
            row_direction,
            column_direction,
        )

        distance = float(np.dot(position, normal))

        slices.append(
            {
                "dataset": ds,
                "distance": distance,
            }
        )

    if not slices:
        raise ValueError(
            f"No image slices found in: {series_dir}"
        )

    # Sort slices using their physical position.
    slices.sort(key=lambda x: x["distance"])

    volume = np.stack(
        [item["dataset"].pixel_array for item in slices],
        axis=0,
    )

    first = slices[0]["dataset"]

    metadata = {
        "study_instance_uid": str(
            getattr(first, "StudyInstanceUID", "")
        ),
        "series_instance_uid": str(
            getattr(first, "SeriesInstanceUID", "")
        ),
        "num_slices": volume.shape[0],
        "rows": volume.shape[1],
        "columns": volume.shape[2],
        "pixel_spacing": [
            float(x) for x in first.PixelSpacing
        ],
        "slice_thickness": float(
            getattr(first, "SliceThickness", 0)
        ),
        "image_orientation": [
            float(x)
            for x in first.ImageOrientationPatient
        ],
    }

    return volume, metadata
