import subprocess
import sys


if len(sys.argv) != 2:
    print("Usage: python scripts/find_series_files.py <series_uid>")
    sys.exit(1)

series_uid = sys.argv[1]
page_token = None
page = 1

while True:
    cmd = [
        "kaggle",
        "competitions",
        "files",
        "rsna-knee-abnormality-detection",
        "--page-size",
        "200",
    ]

    if page_token:
        cmd.extend(["--page-token", page_token])

    print(f"Checking page {page}...")

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
    )

    lines = result.stdout.splitlines()

    matches = [line for line in lines if series_uid in line]

    if matches:
        print(f"\nFOUND: {len(matches)} files\n")
        for line in matches:
            print(line)
        break

    token_line = next(
        (line for line in lines if line.startswith("Next Page Token = ")),
        None,
    )

    if not token_line:
        print("\nSeries not found.")
        break

    page_token = token_line.replace("Next Page Token = ", "").strip()
    page += 1
