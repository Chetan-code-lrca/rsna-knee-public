import pytest

from scripts.evaluate import validate_validation_membership


def test_validation_membership_allows_same_studies_in_different_order():
    validate_validation_membership(
        ["study-a", "study-b"],
        ["study-b", "study-a"],
    )


def test_validation_membership_rejects_missing_checkpoint_studies():
    with pytest.raises(
        ValueError,
        match="membership differs from the saved checkpoint.*1 saved validation UID",
    ):
        validate_validation_membership(
            ["study-a", "study-b"],
            ["study-a"],
        )


def test_validation_membership_rejects_unexpected_studies():
    with pytest.raises(
        ValueError,
        match="membership differs from the saved checkpoint.*1 unexpected UID",
    ):
        validate_validation_membership(
            ["study-a"],
            ["study-a", "study-extra"],
        )
