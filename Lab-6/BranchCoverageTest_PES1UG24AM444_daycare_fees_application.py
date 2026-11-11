"""Decision-outcome tests for every branch in the Daycare Fees application."""

import pytest

from daycare_fees import enrolment_allowed, extra_hours_fee, pickup_status


@pytest.mark.parametrize(
    ("age_group", "hours", "sibling", "expected"),
    [
        ("infant", 20, False, 0),       # included-hours boundary
        ("infant", 21, False, 14),      # infant rate; no high-extra surcharge
        ("infant", 41, False, 462),     # high-extra infant surcharge
        ("toddler", 30, True, 0),       # sibling increases included hours
        ("toddler", 51, True, 294),     # non-infant high-extra surcharge
        ("preschool", 31, False, 9),    # non-infant ordinary rate
    ],
)
def test_extra_hours_fee_branches(age_group, hours, sibling, expected):
    assert extra_hours_fee(age_group, hours, sibling) == expected


@pytest.mark.parametrize("age_group", ["unknown", None])
def test_extra_hours_fee_unknown_age_branch(age_group):
    with pytest.raises(ValueError, match="unknown age group"):
        extra_hours_fee(age_group, 0, False)


def test_extra_hours_fee_negative_hours_branch():
    with pytest.raises(ValueError, match="invalid hours"):
        extra_hours_fee("preschool", -1, False)


@pytest.mark.parametrize(
    ("age", "vacancies", "pending", "expected"),
    [
        (12, 0, True, True),
        (11, 0, True, False),
        (5, 1, False, False),
        (6, 1, False, True),
        (6, 0, False, False),
    ],
)
def test_enrolment_branches(age, vacancies, pending, expected):
    assert enrolment_allowed(age, vacancies, pending) is expected


@pytest.mark.parametrize(
    ("minutes", "aftercare", "friday", "expected"),
    [
        (10, False, False, "on_time"),
        (9, False, False, "late"),
        (-6, False, False, "overdue"),
        (30, True, True, "on_time"),
        (19, True, True, "late"),
        (4, False, True, "overdue"),
    ],
)
def test_pickup_status_branches(minutes, aftercare, friday, expected):
    assert pickup_status(minutes, aftercare, friday) == expected

