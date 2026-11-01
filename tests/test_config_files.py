from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]


def test_yaml_configs_are_nonempty_mappings():
    for relative_path in (
        "configs/dataset.yml",
        "configs/model.yml",
        "configs/train.yml",
        "configs/inference.yml",
    ):
        content = yaml.safe_load((ROOT / relative_path).read_text(encoding="utf-8"))
        assert isinstance(content, dict), relative_path
        assert content, relative_path


def test_model_config_defines_expected_output_count():
    config = yaml.safe_load((ROOT / "configs/model.yml").read_text(encoding="utf-8"))
    assert config["num_targets"] == 12
    assert len(config["target_size"]) == 2
    assert config["num_slices"] > 0
