"""Functional tests for the assigned Daycare Fees Lab 6 module."""

import pytest

from daycare_fees import enrolment_allowed, extra_hours_fee, pickup_status


@pytest.mark.parametrize(
    ("age_group", "hours", "sibling", "expected"),
    [
        ("infant", 20, False, 0),
        ("toddler", 20, False, 0),
        ("preschool", 30, False, 0),
        ("toddler", 30, False, 45),
        ("infant", 21, False, 14),
        ("infant", 41, False, 462),
        ("preschool", 56, False, 364),
        ("toddler", 30, True, 0),
        ("infant", 21, True, 14),
    ],
)
def test_extra_hours_fee_boundaries_and_rates(age_group, hours, sibling, expected):
    assert extra_hours_fee(age_group, hours, sibling) == expected


@pytest.mark.parametrize("age_group", ["school-age", "", None])
def test_extra_hours_fee_rejects_unknown_age_group(age_group):
    with pytest.raises(ValueError, match="unknown age group"):
        extra_hours_fee(age_group, 0, False)


def test_extra_hours_fee_rejects_negative_hours():
    with pytest.raises(ValueError, match="invalid hours"):
        extra_hours_fee("toddler", -1, False)


@pytest.mark.parametrize(
    ("age", "vacancies", "pending", "expected"),
    [
        (11, 0, True, False),
        (12, 0, True, True),
        (5, 5, False, False),
        (6, 0, False, False),
        (6, 1, False, True),
    ],
)
def test_enrolment_allowed_decision_boundaries(age, vacancies, pending, expected):
    assert enrolment_allowed(age, vacancies, pending) is expected


@pytest.mark.parametrize(
    ("minutes", "aftercare", "friday", "expected"),
    [
        (10, False, False, "on_time"),
        (9, False, False, "late"),
        (-5, False, False, "late"),
        (-6, False, False, "overdue"),
        (20, True, False, "on_time"),
        (10, True, False, "late"),
        (20, False, True, "on_time"),
        (5, False, True, "late"),
        (4, False, True, "overdue"),
    ],
)
def test_pickup_status_cutoffs(minutes, aftercare, friday, expected):
    assert pickup_status(minutes, aftercare, friday) == expected
