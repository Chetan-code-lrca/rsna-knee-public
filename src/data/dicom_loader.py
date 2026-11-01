from pathlib import Path

import numpy as np
import pydicom


def load_dicom_series(series_dir):
    """
    Load a DICOM series into a 3D NumPy volume.

    Parameters
    ----------
    series_dir : str or Path
        Directory containing DICOM files belonging to one series.

    Returns
    -------
    volume : np.ndarray
        3D array with shape (num_slices, rows, columns).

    metadata : dict
        Important DICOM metadata for the series.
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

        # Row and column direction vectors
        row_cosine = orientation[:3]
        column_cosine = orientation[3:]

        # Normal vector to the image plane
        normal = np.cross(row_cosine, column_cosine)

        # Position of this slice along the normal
        slice_position = np.dot(position, normal)

        slices.append(
            {
                "dataset": ds,
                "position": slice_position,
            }
        )

    if not slices:
        raise ValueError(
            f"No valid DICOM images found in: {series_dir}"
        )

    # Sort using physical slice position
    slices.sort(key=lambda x: x["position"])

    volume = np.stack(
        [
            item["dataset"].pixel_array
            for item in slices
        ],
        axis=0,
    )

    first = slices[0]["dataset"]

    metadata = {
        "study_instance_uid": str(first.StudyInstanceUID),
        "series_instance_uid": str(first.SeriesInstanceUID),
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
        "anatomical_plane": None,
    }

    return volume, metadata
