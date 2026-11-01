"""Train one fold of the study-level multi-label baseline."""

from __future__ import annotations

import argparse
import json
from functools import partial
from pathlib import Path

import torch
import yaml
from torch import nn
from torch.utils.data import DataLoader

from src.datasets.dataset import TARGETS, KneeStudyDataset
from src.datasets.split import create_study_folds
from src.models.baseline import SliceCNNBaseline
from src.datasets.dataloader import collate_studies
from src.training import set_random_seed

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


def run_epoch(model, loader, criterion, device, optimizer=None) -> float:
    training = optimizer is not None
    model.train(training)
    total_loss = 0.0
    total_items = 0

    for batch in loader:
        images = batch["image"].to(device, non_blocking=True)
        labels = batch["label"].to(device, non_blocking=True)
        if training:
            optimizer.zero_grad(set_to_none=True)
        with torch.set_grad_enabled(training):
            logits = model(images)
            loss = criterion(logits, labels)
            if training:
                loss.backward()
                torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
                optimizer.step()
        count = int(images.shape[0])
        total_loss += float(loss.detach().item()) * count
        total_items += count

    if total_items == 0:
        raise ValueError("The data loader produced no labeled studies.")
    return total_loss / total_items


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset-config", default="configs/dataset.yml")
    parser.add_argument("--model-config", default="configs/model.yml")
    parser.add_argument("--train-config", default="configs/train.yml")
    parser.add_argument("--fold", type=int, default=None, help="Validation fold override.")
    args = parser.parse_args()

    dataset_cfg = load_yaml(args.dataset_config)
    model_cfg = load_yaml(args.model_config)
    train_cfg = load_yaml(args.train_config)

    train_csv = resolve_path(dataset_cfg["train_csv"])
    series_csv = resolve_path(dataset_cfg["series_csv"])
    dicom_root = resolve_path(dataset_cfg["dicom_root"])
    if not train_csv.is_file():
        raise FileNotFoundError(
            f"Training labels not found at {train_csv}. "
            "Download the competition files and follow docs/dataset.md."
        )
    if not series_csv.is_file():
        raise FileNotFoundError(
            f"Series metadata not found at {series_csv}. "
            "Expected the train_series.csv metadata file."
        )
    if not dicom_root.is_dir():
        raise FileNotFoundError(f"DICOM training directory not found: {dicom_root}")

    seed = int(train_cfg.get("seed", 42))
    n_splits = int(train_cfg.get("n_splits", 5))
    fold = int(
        train_cfg.get("validation_fold", 0) if args.fold is None else args.fold
    )
    if not 0 <= fold < n_splits:
        raise ValueError(f"fold must be between 0 and {n_splits - 1}")
    set_random_seed(seed)

    folds = create_study_folds(
        train_csv,
        n_splits=n_splits,
        random_state=seed,
    )
    folds_path = resolve_path(
        dataset_cfg.get("folds_csv", "data/processed/study_folds.csv")
    )
    folds_path.parent.mkdir(parents=True, exist_ok=True)
    folds.to_csv(folds_path, index=False)

    train_uids = set(
        folds.loc[folds["fold"] != fold, "StudyInstanceUID"].astype(str)
    )
    valid_uids = set(
        folds.loc[folds["fold"] == fold, "StudyInstanceUID"].astype(str)
    )
    target_size = tuple(
        int(value) for value in model_cfg.get("target_size", [224, 224])
    )
    num_slices = int(model_cfg.get("num_slices", 16))
    plane = str(dataset_cfg.get("plane", "Sagittal"))

    common = {
        "train_csv": train_csv,
        "series_csv": series_csv,
        "dicom_root": dicom_root,
        "target_size": target_size,
        "plane": plane,
        "num_slices": num_slices,
    }
    train_dataset = KneeStudyDataset(**common, study_uids=train_uids)
    valid_dataset = KneeStudyDataset(**common, study_uids=valid_uids)
    if not len(train_dataset) or not len(valid_dataset):
        raise ValueError("The chosen fold produced an empty train or validation set.")

    collate = partial(collate_studies, num_slices=num_slices)
    loader_options = {
        "batch_size": int(train_cfg.get("batch_size", 2)),
        "num_workers": int(train_cfg.get("num_workers", 0)),
        "collate_fn": collate,
        "pin_memory": torch.cuda.is_available(),
    }
    train_loader = DataLoader(train_dataset, shuffle=True, **loader_options)
    valid_loader = DataLoader(valid_dataset, shuffle=False, **loader_options)

    model_params = {
        "num_targets": len(TARGETS),
        "channels": tuple(
            int(value) for value in model_cfg.get("channels", [16, 32, 64])
        ),
        "hidden_dim": int(model_cfg.get("hidden_dim", 128)),
        "dropout": float(model_cfg.get("dropout", 0.2)),
    }
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = SliceCNNBaseline(**model_params).to(device)
    criterion = nn.BCEWithLogitsLoss()
    optimizer = torch.optim.AdamW(
        model.parameters(),
        lr=float(train_cfg.get("learning_rate", 0.001)),
        weight_decay=float(train_cfg.get("weight_decay", 0.0001)),
    )

    output_root = resolve_path(train_cfg.get("output_dir", "outputs/baseline"))
    output_dir = output_root / f"fold_{fold}"
    output_dir.mkdir(parents=True, exist_ok=True)
    checkpoint_path = output_dir / "best.pt"
    best_loss = float("inf")
    best_epoch = 0
    history = []
    epochs = int(train_cfg.get("epochs", 10))
    patience = int(train_cfg.get("early_stop_patience", 3))
    stale_epochs = 0

    for epoch in range(1, epochs + 1):
        train_loss = run_epoch(model, train_loader, criterion, device, optimizer)
        valid_loss = run_epoch(model, valid_loader, criterion, device)
        row = {
            "epoch": epoch,
            "train_loss": train_loss,
            "validation_loss": valid_loss,
        }
        history.append(row)
        print(
            f"fold={fold} epoch={epoch}/{epochs} "
            f"train_loss={train_loss:.5f} validation_loss={valid_loss:.5f}"
        )

        if valid_loss < best_loss:
            best_loss = valid_loss
            best_epoch = epoch
            stale_epochs = 0
            torch.save(
                {
                    "state_dict": model.state_dict(),
                    "model_params": model_params,
                    "fold": fold,
                    "n_splits": n_splits,
                    "seed": seed,
                    "plane": plane,
                    "target_size": list(target_size),
                    "num_slices": num_slices,
                    "targets": TARGETS,
                    "train_study_uids": sorted(train_uids),
                    "validation_study_uids": sorted(valid_uids),
                    "best_epoch": best_epoch,
                    "validation_loss": best_loss,
                },
                checkpoint_path,
            )
        else:
            stale_epochs += 1

        if patience > 0 and stale_epochs >= patience:
            print(f"Early stopping after {epoch} epochs without improvement.")
            break

    summary = {
        "fold": fold,
        "seed": seed,
        "train_studies": len(train_dataset),
        "validation_studies": len(valid_dataset),
        "best_epoch": best_epoch,
        "best_validation_loss": best_loss,
        "checkpoint": (
            str(checkpoint_path.relative_to(ROOT))
            if checkpoint_path.is_relative_to(ROOT)
            else str(checkpoint_path)
        ),
        "history": history,
        "note": "Experimental baseline only; validate on an independent set before interpreting results.",
    }
    with (output_dir / "metrics.json").open("w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2)
    print(
        json.dumps(
            {key: value for key, value in summary.items() if key != "history"},
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
