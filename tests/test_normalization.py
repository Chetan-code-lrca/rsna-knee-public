import numpy as np
import pytest

from src.preprocessing.normalization import percentile_normalize


def test_percentile_normalize():
    volume = np.array(
        [[0, 10, 50], [100, 200, 1000]],
        dtype=np.uint16,
    )

    normalized = percentile_normalize(volume)

    assert normalized.dtype == np.float32
    assert normalized.min() >= 0.0
    assert normalized.max() <= 1.0
    assert np.isfinite(normalized).all()


def test_constant_blank_slice_becomes_zeros():
    volume = np.full((16, 16), 7, dtype=np.uint16)

    normalized = percentile_normalize(volume)

    assert normalized.dtype == np.float32
    assert np.array_equal(normalized, np.zeros((16, 16), dtype=np.float32))


def test_normalization_rejects_invalid_percentiles():
    with pytest.raises(ValueError, match="Percentiles"):
        percentile_normalize(np.ones((3, 3)), 99, 1)


def test_normalization_rejects_nonfinite_pixels():
    volume = np.array([[0, np.nan], [2, 3]], dtype=np.float32)

    with pytest.raises(ValueError, match="non-finite"):
        percentile_normalize(volume)
