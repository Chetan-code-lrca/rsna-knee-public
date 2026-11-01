"""Evaluate a saved checkpoint on its held-out study fold."""

from __future__ import annotations

import argparse
import json

import numpy as np
import pandas as pd
import torch
from sklearn.metrics import roc_auc_score
from torch import nn

from scripts.common import build_loader, load_checkpoint, load_yaml, resolve_path
from src.datasets.dataset import TARGETS, KneeStudyDataset


def validate_validation_membership(
    saved_validation_uids: set[str] | list[str],
    observed_validation_uids: list[str],
) -> None:
    """Reject evaluation if current metadata no longer matches checkpoint membership."""
    expected = {str(study_uid) for study_uid in saved_validation_uids}
    observed = {str(study_uid) for study_uid in observed_validation_uids}
    missing = sorted(expected - observed)
    unexpected = sorted(observed - expected)
    if missing or unexpected:
        issues = []
        if missing:
            issues.append(f"{len(missing)} saved validation UID(s) are absent")
        if unexpected:
            issues.append(f"{len(unexpected)} unexpected UID(s) were selected")
        raise ValueError(
            "Current validation membership differs from the saved checkpoint ("
            + "; ".join(issues)
            + ")."
        )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--checkpoint", required=True)
    parser.add_argument("--dataset-config", default="configs/dataset.yml")
    parser.add_argument("--train-config", default="configs/train.yml")
    parser.add_argument("--output-dir", default=None)
    args = parser.parse_args()

    dataset_cfg = load_yaml(args.dataset_config)
    train_cfg = load_yaml(args.train_config)
    train_csv = resolve_path(dataset_cfg["train_csv"])
    series_csv = resolve_path(dataset_cfg["series_csv"])
    dicom_root = resolve_path(dataset_cfg["dicom_root"])
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    checkpoint, model = load_checkpoint(args.checkpoint, device)

    fold = int(checkpoint["fold"])
    saved_validation_uids = checkpoint.get("validation_study_uids")
    if not saved_validation_uids:
        raise ValueError(
            "Checkpoint does not contain its validation study membership. "
            "Retrain with the current pipeline before evaluation."
        )
    valid_uids = {str(study_uid) for study_uid in saved_validation_uids}
    dataset = KneeStudyDataset(
        train_csv=train_csv,
        series_csv=series_csv,
        dicom_root=dicom_root,
        target_size=tuple(checkpoint["target_size"]),
        plane=str(checkpoint["plane"]),
        study_uids=valid_uids,
        num_slices=int(checkpoint["num_slices"]),
    )
    if not len(dataset):
        raise ValueError(f"Validation fold {fold} contains no labeled studies.")
    validate_validation_membership(valid_uids, dataset.studies)
    loader = build_loader(
        dataset,
        batch_size=int(train_cfg.get("batch_size", 2)),
        num_workers=int(train_cfg.get("num_workers", 0)),
        num_slices=int(checkpoint["num_slices"]),
    )

    criterion = nn.BCEWithLogitsLoss()
    total_loss = 0.0
    total_items = 0
    uids, truth, probabilities = [], [], []
    with torch.inference_mode():
        for batch in loader:
            images = batch["image"].to(device, non_blocking=True)
            labels = batch["label"].to(device, non_blocking=True)
            logits = model(images)
            loss = criterion(logits, labels)
            count = int(images.shape[0])
            total_loss += float(loss.item()) * count
            total_items += count
            uids.extend(batch["study_uid"])
            truth.append(labels.cpu().numpy())
            probabilities.append(torch.sigmoid(logits).cpu().numpy())

    actual = np.concatenate(truth, axis=0)
    predicted = np.concatenate(probabilities, axis=0)
    per_target_auc = {}
    valid_auc = []
    for index, target in enumerate(TARGETS):
        if np.unique(actual[:, index]).size == 2:
            score = float(roc_auc_score(actual[:, index], predicted[:, index]))
            per_target_auc[target] = score
            valid_auc.append(score)
        else:
            per_target_auc[target] = None

    output_dir = (
        resolve_path(args.output_dir)
        if args.output_dir
        else resolve_path(args.checkpoint).parent / "evaluation"
    )
    output_dir.mkdir(parents=True, exist_ok=True)
    prediction_frame = pd.DataFrame(predicted, columns=TARGETS)
    prediction_frame.insert(0, "StudyInstanceUID", uids)
    for index, target in enumerate(TARGETS):
        prediction_frame[f"true_{target}"] = actual[:, index]
    prediction_frame.to_csv(output_dir / "predictions.csv", index=False)

    metrics = {
        "fold": fold,
        "study_count": len(uids),
        "validation_bce_loss": total_loss / total_items,
        "macro_auc_over_targets_with_both_classes": (
            float(np.mean(valid_auc)) if valid_auc else None
        ),
        "auc_targets_evaluated": len(valid_auc),
        "per_target_auc": per_target_auc,
        "note": "Small research baseline; metrics from a small validation fold are uncertain.",
    }
    with (output_dir / "metrics.json").open("w", encoding="utf-8") as handle:
        json.dump(metrics, handle, indent=2)
    print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    main()
