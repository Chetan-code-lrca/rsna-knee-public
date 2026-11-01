"""Batch variable-depth MRI stacks into fixed-depth tensors."""

from __future__ import annotations

from typing import Any

import torch
import torch.nn.functional as F


def resample_depth(image: torch.Tensor, num_slices: int) -> torch.Tensor:
    """Resample a [slices, height, width] MRI stack to fixed depth."""
    if image.ndim != 3:
        raise ValueError("Expected an MRI stack with shape [slices, height, width].")
    if num_slices < 1:
        raise ValueError("num_slices must be positive.")
    if image.shape[0] < 1:
        raise ValueError("MRI stack must contain at least one slice.")
    if image.shape[0] == num_slices:
        return image.to(dtype=torch.float32)

    volume = image.to(dtype=torch.float32).unsqueeze(0).unsqueeze(0)
    resized = F.interpolate(
        volume,
        size=(num_slices, image.shape[1], image.shape[2]),
        mode="trilinear",
        align_corners=False,
    )
    return resized.squeeze(0).squeeze(0)


def collate_studies(
    items: list[dict[str, Any]],
    num_slices: int = 16,
) -> dict[str, Any]:
    """Batch study images and metadata, including labels when all exist."""
    if not items:
        raise ValueError("Cannot collate an empty batch.")

    batch: dict[str, Any] = {
        "image": torch.stack(
            [resample_depth(item["image"], num_slices) for item in items]
        ),
        "study_uid": [str(item["study_uid"]) for item in items],
        "plane": [str(item["plane"]) for item in items],
        "series_uid": [str(item["series_uid"]) for item in items],
    }
    if all("label" in item for item in items):
        batch["label"] = torch.stack(
            [item["label"].to(dtype=torch.float32) for item in items]
        )
    elif any("label" in item for item in items):
        raise ValueError("A batch cannot mix labeled and unlabeled studies.")
    return batch
