"""Download the RSNA knee competition files with the Kaggle CLI."""

from __future__ import annotations

import argparse
import shutil
import subprocess
from pathlib import Path

COMPETITION = "rsna-knee-abnormality-detection"
ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--competition", default=COMPETITION)
    parser.add_argument("--output-dir", default="data/raw")
    parser.add_argument(
        "--unzip",
        action="store_true",
        help="Ask the Kaggle CLI to extract downloaded archives.",
    )
    args = parser.parse_args()

    executable = shutil.which("kaggle")
    if executable is None:
        parser.error(
            "Kaggle CLI is not installed. Install kaggle and configure API credentials."
        )
    output_dir = Path(args.output_dir)
    if not output_dir.is_absolute():
        output_dir = ROOT / output_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    command = [
        executable,
        "competitions",
        "download",
        "-c",
        args.competition,
        "-p",
        str(output_dir),
    ]
    if args.unzip:
        command.append("--unzip")

    print("Downloading competition files into", output_dir)
    subprocess.run(command, check=True)


if __name__ == "__main__":
    main()
