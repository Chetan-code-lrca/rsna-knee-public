import numpy as np
import pandas as pd
import pytest

from scripts.submit import validate_prediction_values
from src.datasets.dataset import TARGETS


def frame(values):
    data = {"StudyInstanceUID": ["study-1"]}
    data.update({target: [values[index]] for index, target in enumerate(TARGETS)})
    return pd.DataFrame(data)


def test_submission_accepts_valid_probability_boundaries():
    values = [0.0, 1.0] + [0.5] * (len(TARGETS) - 2)

    validated = validate_prediction_values(frame(values))

    assert np.isfinite(validated[TARGETS].to_numpy(dtype=float)).all()
    assert validated[TARGETS].min().min() == 0.0
    assert validated[TARGETS].max().max() == 1.0


@pytest.mark.parametrize("bad_value", [np.nan, np.inf, -np.inf, "not-a-number"])
def test_submission_rejects_non_finite_or_nonnumeric_values(bad_value):
    values = [0.5] * len(TARGETS)
    values[0] = bad_value

    with pytest.raises(ValueError, match="finite numeric"):
        validate_prediction_values(frame(values))


@pytest.mark.parametrize("bad_value", [-0.01, 1.01])
def test_submission_rejects_values_outside_probability_range(bad_value):
    values = [0.5] * len(TARGETS)
    values[0] = bad_value

    with pytest.raises(ValueError, match=r"within \[0, 1\]"):
        validate_prediction_values(frame(values))
