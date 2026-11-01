import ast
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK_PATH = ROOT / "kaggle" / "rsna_knee_submission.ipynb"
KERNEL_METADATA_PATH = ROOT / "kaggle" / "kernel-metadata.json"


def test_kaggle_notebook_is_valid_json_and_python():
    notebook = json.loads(NOTEBOOK_PATH.read_text(encoding="utf-8"))

    assert notebook["nbformat"] == 4
    code_cells = [
        (index, "".join(cell.get("source", [])))
        for index, cell in enumerate(notebook["cells"])
        if cell.get("cell_type") == "code"
    ]
    assert code_cells

    for index, source in code_cells:
        ast.parse(source, filename=f"{NOTEBOOK_PATH}:cell-{index}")


def test_kaggle_metadata_uses_offline_gpu_competition_runtime():
    metadata = json.loads(KERNEL_METADATA_PATH.read_text(encoding="utf-8"))

    assert metadata["enable_gpu"] in (True, "true")
    assert metadata["enable_internet"] in (False, "false")
    assert "rsna-knee-abnormality-detection" in metadata["competition_sources"]
    assert (KERNEL_METADATA_PATH.parent / metadata["code_file"]).is_file()


def test_notebook_writes_required_submission_file():
    notebook = json.loads(NOTEBOOK_PATH.read_text(encoding="utf-8"))
    code = "\n".join(
        "".join(cell.get("source", []))
        for cell in notebook["cells"]
        if cell.get("cell_type") == "code"
    )
    assert "/kaggle/working/submission.csv" in code
