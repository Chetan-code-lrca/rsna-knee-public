"""Deterministic slice sampling for fixed-size MRI inputs."""

from __future__ import annotations

import numpy as np


def select_evenly_spaced_slices(
    volume: np.ndarray,
    num_slices: int = 16,
) -> np.ndarray:
    """Select a fixed number of slices, retaining the volume's full extent.

    The input must have shape [slices, rows, columns]. Sampling is performed
    before per-slice normalization and resizing so unnecessary slices are not
    sent through the more expensive preprocessing steps. If the requested
    count exceeds the source depth, indices repeat deterministically.
    """
    if volume.ndim != 3:
        raise ValueError("Expected volume with shape [slices, rows, columns].")
    if volume.shape[0] < 1:
        raise ValueError("Volume must contain at least one slice.")
    if num_slices < 1:
        raise ValueError("num_slices must be positive.")

    if num_slices == 1:
        indices = np.array([(volume.shape[0] - 1) // 2], dtype=np.int64)
    else:
        indices = np.rint(
            np.linspace(0, volume.shape[0] - 1, num_slices)
        ).astype(np.int64)

    return np.ascontiguousarray(volume[indices])
