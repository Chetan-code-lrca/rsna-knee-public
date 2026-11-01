"""Small slice-wise CNN baseline for multi-label knee MRI classification."""

from __future__ import annotations

import torch
from torch import nn


class SliceCNNBaseline(nn.Module):
    """Encode each MRI slice independently and average features per study.

    Inputs have shape [batch, slices, height, width] and contain normalized
    single-channel images. Outputs are 12 independent logits, one per target.
    This intentionally small baseline avoids pretrained-weight downloads.
    """

    def __init__(
        self,
        num_targets: int = 12,
        channels: tuple[int, ...] = (16, 32, 64),
        hidden_dim: int = 128,
        dropout: float = 0.2,
    ) -> None:
        super().__init__()
        if num_targets < 1:
            raise ValueError("num_targets must be positive")
        if not channels or any(channel < 1 for channel in channels):
            raise ValueError("channels must contain positive integers")
        if hidden_dim < 1:
            raise ValueError("hidden_dim must be positive")
        if not 0 <= dropout < 1:
            raise ValueError("dropout must be in the range [0, 1)")

        layers: list[nn.Module] = []
        input_channels = 1
        for output_channels in channels:
            layers.extend(
                [
                    nn.Conv2d(
                        input_channels,
                        output_channels,
                        kernel_size=3,
                        stride=2,
                        padding=1,
                        bias=False,
                    ),
                    nn.BatchNorm2d(output_channels),
                    nn.SiLU(inplace=True),
                ]
            )
            input_channels = output_channels
        layers.extend([nn.AdaptiveAvgPool2d((1, 1)), nn.Flatten()])
        self.encoder = nn.Sequential(*layers)
        self.head = nn.Sequential(
            nn.Linear(input_channels, hidden_dim),
            nn.SiLU(inplace=True),
            nn.Dropout(dropout),
            nn.Linear(hidden_dim, num_targets),
        )
        self.num_targets = num_targets
        self.channels = tuple(channels)
        self.hidden_dim = hidden_dim
        self.dropout = dropout

    def forward(self, images: torch.Tensor) -> torch.Tensor:
        if images.ndim != 4:
            raise ValueError(
                "Expected images with shape [batch, slices, height, width]."
            )
        batch_size, slices, height, width = images.shape
        if batch_size < 1 or slices < 1 or height < 1 or width < 1:
            raise ValueError("Image dimensions must all be positive.")

        per_slice = images.reshape(batch_size * slices, 1, height, width)
        features = self.encoder(per_slice)
        features = features.reshape(batch_size, slices, -1)
        study_features = features.mean(dim=1)
        return self.head(study_features)
