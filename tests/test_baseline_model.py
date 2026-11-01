import pytest
import torch

from src.models.baseline import SliceCNNBaseline


def test_baseline_returns_one_logit_per_target():
    model = SliceCNNBaseline(num_targets=12, channels=(4, 8), hidden_dim=16)
    images = torch.rand(2, 5, 32, 32)

    logits = model(images)

    assert logits.shape == (2, 12)
    assert torch.isfinite(logits).all()


def test_baseline_supports_backpropagation():
    model = SliceCNNBaseline(num_targets=3, channels=(4, 8), hidden_dim=16)
    images = torch.rand(2, 4, 24, 24)
    labels = torch.rand(2, 3)

    loss = torch.nn.functional.binary_cross_entropy_with_logits(
        model(images), labels
    )
    loss.backward()

    assert model.head[-1].weight.grad is not None


def test_baseline_rejects_wrong_input_shape():
    model = SliceCNNBaseline()
    with pytest.raises(ValueError, match="batch, slices, height, width"):
        model(torch.rand(2, 1, 16, 16, 1))
