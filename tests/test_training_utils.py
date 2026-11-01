import pytest
import torch

from src.datasets.dataloader import collate_studies, resample_depth


def test_resample_depth_returns_fixed_shape_and_float32():
    stack = torch.arange(3 * 8 * 8, dtype=torch.float32).reshape(3, 8, 8)
    result = resample_depth(stack, 5)

    assert result.shape == (5, 8, 8)
    assert result.dtype == torch.float32
    assert torch.isfinite(result).all()


def test_resample_depth_rejects_invalid_inputs():
    with pytest.raises(ValueError, match="shape"):
        resample_depth(torch.ones(2, 3), 4)
    with pytest.raises(ValueError, match="positive"):
        resample_depth(torch.ones(2, 3, 3), 0)


def test_collate_studies_batches_labels_and_metadata():
    items = [
        {
            "image": torch.ones(3, 8, 8),
            "label": torch.zeros(12),
            "study_uid": "study-a",
            "plane": "Axial",
            "series_uid": "series-a",
        },
        {
            "image": torch.zeros(5, 8, 8),
            "label": torch.ones(12),
            "study_uid": "study-b",
            "plane": "Axial",
            "series_uid": "series-b",
        },
    ]

    batch = collate_studies(items, num_slices=4)

    assert batch["image"].shape == (2, 4, 8, 8)
    assert batch["label"].shape == (2, 12)
    assert batch["study_uid"] == ["study-a", "study-b"]


def test_collate_studies_does_not_mix_labeled_and_unlabeled_items():
    items = [
        {"image": torch.ones(2, 4, 4), "label": torch.ones(12), "study_uid": "a", "plane": "Axial", "series_uid": "1"},
        {"image": torch.ones(2, 4, 4), "study_uid": "b", "plane": "Axial", "series_uid": "2"},
    ]
    with pytest.raises(ValueError, match="mix labeled and unlabeled"):
        collate_studies(items, num_slices=2)
