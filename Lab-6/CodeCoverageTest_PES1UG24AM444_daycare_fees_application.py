"""Line-focused coverage tests for the complete Daycare Fees application."""

import pytest

from daycare_fees import enrolment_allowed, extra_hours_fee, pickup_status


def test_extra_hours_fee_lines_and_exceptions():
    assert extra_hours_fee("toddler", 20, False) == 0
    assert extra_hours_fee("toddler", 30, False) == 45
    assert extra_hours_fee("toddler", 30, True) == 0
    assert extra_hours_fee("infant", 41, False) == 462
    assert extra_hours_fee("preschool", 56, False) == 364
    with pytest.raises(ValueError):
        extra_hours_fee("school-age", 20, False)
    with pytest.raises(ValueError):
        extra_hours_fee("infant", -1, False)


def test_enrolment_allowed_lines():
    assert enrolment_allowed(12, 0, True) is True
    assert enrolment_allowed(11, 1, True) is False
    assert enrolment_allowed(5, 3, False) is False
    assert enrolment_allowed(6, 1, False) is True
    assert enrolment_allowed(6, 0, False) is False


def test_pickup_status_lines():
    assert pickup_status(10, False, False) == "on_time"
    assert pickup_status(9, False, False) == "late"
    assert pickup_status(-6, False, False) == "overdue"
    assert pickup_status(30, True, True) == "on_time"

