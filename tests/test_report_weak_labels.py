from __future__ import annotations

import json
import re
import unicodedata
from pathlib import Path

import numpy as np

TARGETS = [
    "ACL", "MCL", "Medial Meniscus", "Lateral Meniscus",
    "Medial OA", "Lateral OA", "PF OA", "Effusion",
    "Synovitis", "Baker's", "Contusion", "Fracture",
]


def load_labeler_from_project_notebook():
    root = Path(__file__).resolve().parents[1]
    notebook_path = root / "kaggle" / "rsna_knee_submission.ipynb"
    notebook = json.loads(notebook_path.read_text(encoding="utf-8"))

    parser_source = None
    for cell in notebook.get("cells", []):
        if cell.get("cell_type") != "code":
            continue
        source = cell.get("source", [])
        source = "".join(source) if isinstance(source, list) else str(source)
        if "def normalize_report(text):" in source and "def weak_labels_from_report(report):" in source:
            parser_source = source.split("# Small sanity check")[0]
            break

    if parser_source is None:
        raise AssertionError("Could not find the weak-label rule cell in the baseline notebook.")

    namespace = {
        "np": np,
        "re": re,
        "unicodedata": unicodedata,
        "TARGETS": TARGETS,
    }
    exec(compile(parser_source, str(notebook_path), "exec"), namespace)
    return namespace["weak_labels_from_report"]


def test_explicit_acl_tear_is_positive():
    labeler = load_labeler_from_project_notebook()
    values, mask = labeler("Complete ACL tear.")
    index = TARGETS.index("ACL")
    assert mask[index] == 1
    assert values[index] == 1


def test_intact_acl_and_absent_effusion_are_negative():
    labeler = load_labeler_from_project_notebook()
    values, mask = labeler("The ACL is intact. No joint effusion.")
    acl = TARGETS.index("ACL")
    effusion = TARGETS.index("Effusion")
    assert mask[acl] == 1 and values[acl] == 0
    assert mask[effusion] == 1 and values[effusion] == 0


def test_target_mention_without_damage_is_unknown_for_ligament():
    labeler = load_labeler_from_project_notebook()
    values, mask = labeler("The ACL is described in the report.")
    acl = TARGETS.index("ACL")
    assert mask[acl] == 0
    assert values[acl] == 0


def test_negation_does_not_bleed_into_next_sentence():
    labeler = load_labeler_from_project_notebook()
    values, mask = labeler("No effusion. The ACL is torn.")
    acl = TARGETS.index("ACL")
    effusion = TARGETS.index("Effusion")
    assert mask[effusion] == 1 and values[effusion] == 0
    assert mask[acl] == 1 and values[acl] == 1
