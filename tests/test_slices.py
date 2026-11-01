import numpy as np
import pytest

from src.preprocessing.slices import select_evenly_spaced_slices


def test_select_evenly_spaced_slices_preserves_extent_and_dtype():
    volume = np.repeat(
        np.arange(30, dtype=np.uint16)[:, None, None],
        repeats=4,
        axis=1,
    )
    volume = np.repeat(volume, repeats=5, axis=2)

    sampled = select_evenly_spaced_slices(volume, num_slices=4)

    assert sampled.shape == (4, 4, 5)
    assert sampled.dtype == np.uint16
    assert sampled[:, 0, 0].tolist() == [0, 10, 19, 29]


def test_select_evenly_spaced_slices_repeats_when_volume_is_short():
    volume = np.arange(2 * 3 * 3).reshape(2, 3, 3)

    sampled = select_evenly_spaced_slices(volume, num_slices=4)

    assert sampled.shape == (4, 3, 3)
    assert sampled[0, 0, 0] == sampled[1, 0, 0]
    assert sampled[-1, 0, 0] == volume[-1, 0, 0]


def test_single_requested_slice_uses_middle_slice():
    volume = np.arange(5 * 2 * 2).reshape(5, 2, 2)

    sampled = select_evenly_spaced_slices(volume, num_slices=1)

    assert sampled.shape == (1, 2, 2)
    assert np.array_equal(sampled[0], volume[2])


@pytest.mark.parametrize(
    ("volume", "num_slices", "message"),
    [
        (np.zeros((2, 3)), 1, "shape"),
        (np.zeros((0, 3, 3)), 1, "at least one slice"),
        (np.zeros((2, 3, 3)), 0, "positive"),
    ],
)
def test_select_evenly_spaced_slices_rejects_invalid_inputs(
    volume, num_slices, message
):
    with pytest.raises(ValueError, match=message):
        select_evenly_spaced_slices(volume, num_slices)
