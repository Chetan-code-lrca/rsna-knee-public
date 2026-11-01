import numpy as np


def percentile_normalize(
    volume: np.ndarray,
    lower_percentile: float = 1.0,
    upper_percentile: float = 99.0,
) -> np.ndarray:
    """Percentile-normalize an MRI image to float32 values in [0, 1].

    Constant or effectively blank slices are represented as zeros instead of
    raising, so one empty slice cannot abort preprocessing for an entire study.
    """
    volume = np.asarray(volume, dtype=np.float32)

    if volume.size == 0:
        raise ValueError("Cannot normalize an empty image.")
    if not np.isfinite(volume).all():
        raise ValueError("Image contains non-finite intensity values.")
    if not 0 <= lower_percentile < upper_percentile <= 100:
        raise ValueError("Percentiles must satisfy 0 <= lower < upper <= 100.")

    lower = float(np.percentile(volume, lower_percentile))
    upper = float(np.percentile(volume, upper_percentile))

    if upper <= lower:
        return np.zeros_like(volume, dtype=np.float32)

    clipped = np.clip(volume, lower, upper)
    normalized = (clipped - lower) / (upper - lower)
    return normalized.astype(np.float32)
