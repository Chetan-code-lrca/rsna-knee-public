"""Shared CLI helpers for the RSNA knee baseline."""

from __future__ import annotations

from functools import partial
from pathlib import Path

import torch
import yaml
from torch.utils.data import DataLoader

from src.datasets.dataset import TARGETS
from src.models.baseline import SliceCNNBaseline
from src.datasets.dataloader import collate_studies

ROOT = Path(__file__).resolve().parents[1]


def load_yaml(path: str | Path) -> dict:
    config_path = Path(path)
    if not config_path.is_absolute():
        config_path = ROOT / config_path
    with config_path.open("r", encoding="utf-8") as handle:
        values = yaml.safe_load(handle) or {}
    if not isinstance(values, dict):
        raise ValueError(f"Expected a YAML mapping in {config_path}")
    return values


def resolve_path(value: str | Path) -> Path:
    path = Path(value)
    return path if path.is_absolute() else ROOT / path


def load_checkpoint(path: str | Path, device: torch.device) -> tuple[dict, SliceCNNBaseline]:
    checkpoint_path = resolve_path(path)
    if not checkpoint_path.is_file():
        raise FileNotFoundError(f"Model checkpoint not found: {checkpoint_path}")
    checkpoint = torch.load(checkpoint_path, map_location=device, weights_only=True)
    if checkpoint.get("targets") != TARGETS:
        raise ValueError("Checkpoint target order does not match the current TARGETS.")
    model = SliceCNNBaseline(**checkpoint["model_params"]).to(device)
    model.load_state_dict(checkpoint["state_dict"])
    model.eval()
    return checkpoint, model


def build_loader(
    dataset,
    batch_size: int,
    num_workers: int,
    num_slices: int,
    shuffle: bool = False,
) -> DataLoader:
    return DataLoader(
        dataset,
        batch_size=batch_size,
        shuffle=shuffle,
        num_workers=num_workers,
        pin_memory=torch.cuda.is_available(),
        collate_fn=partial(collate_studies, num_slices=num_slices),
    )
