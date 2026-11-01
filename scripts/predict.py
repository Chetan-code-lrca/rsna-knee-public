"""Generate per-study target probabilities from a saved checkpoint."""

from __future__ import annotations

import argparse

import numpy as np
import pandas as pd
import torch

from scripts.common import build_loader, load_checkpoint, load_yaml, resolve_path
from src.datasets.dataset import TARGETS, KneeStudyDataset


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--checkpoint", required=True)
    parser.add_argument("--dataset-config", default="configs/dataset.yml")
    parser.add_argument("--studies-csv", default=None)
    parser.add_argument("--series-csv", default=None)
    parser.add_argument("--dicom-root", default=None)
    parser.add_argument("--output", default=None)
    parser.add_argument("--batch-size", type=int, default=None)
    args = parser.parse_args()

    dataset_cfg = load_yaml(args.dataset_config)
    studies_csv = resolve_path(args.studies_csv or dataset_cfg["test_csv"])
    series_csv = resolve_path(args.series_csv or dataset_cfg["test_series_csv"])
    dicom_root = resolve_path(args.dicom_root or dataset_cfg["test_dicom_root"])
    for path, description in (
        (studies_csv, "study metadata"),
        (series_csv, "series metadata"),
    ):
        if not path.is_file():
            raise FileNotFoundError(f"Missing {description}: {path}")
    if not dicom_root.is_dir():
        raise FileNotFoundError(f"DICOM directory not found: {dicom_root}")

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    checkpoint, model = load_checkpoint(args.checkpoint, device)
    dataset = KneeStudyDataset(
        train_csv=studies_csv,
        series_csv=series_csv,
        dicom_root=dicom_root,
        target_size=tuple(checkpoint["target_size"]),
        plane=str(checkpoint["plane"]),
        include_unlabeled=True,
        num_slices=int(checkpoint["num_slices"]),
    )
    if not len(dataset):
        raise ValueError(f"No studies found in {studies_csv}")
    inference_cfg = load_yaml("configs/inference.yml")
    batch_size = args.batch_size or int(inference_cfg.get("batch_size", 2))
    loader = build_loader(
        dataset,
        batch_size=batch_size,
        num_workers=int(inference_cfg.get("num_workers", 0)),
        num_slices=int(checkpoint["num_slices"]),
    )

    uids, predictions = [], []
    with torch.inference_mode():
        for batch in loader:
            logits = model(batch["image"].to(device, non_blocking=True))
            predictions.append(torch.sigmoid(logits).cpu().numpy())
            uids.extend(batch["study_uid"])
    frame = pd.DataFrame(np.concatenate(predictions, axis=0), columns=TARGETS)
    frame.insert(0, "StudyInstanceUID", uids)
    output_path = resolve_path(
        args.output or inference_cfg.get("output_csv", "outputs/predictions.csv")
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    frame.to_csv(output_path, index=False)
    print(f"Wrote {len(frame)} study predictions to {output_path}")


if __name__ == "__main__":
    main()
