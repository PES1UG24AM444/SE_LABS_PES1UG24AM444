"""Hypothesis properties and boundary checks for the assigned Lab 7 functions."""

import math

import pytest
from hypothesis import given, settings, strategies as st

from processor import hours_average, parse_enrolment, payable_fee


FUZZ_SETTINGS = settings(max_examples=100, deadline=None, derandomize=True)


def _valid_enrolment_text(value):
    if not isinstance(value, str) or value.count(":") != 1:
        return False
    age_group, raw_hours = value.split(":")
    try:
        hours = float(raw_hours)
    except (ValueError, OverflowError):
        return False
    return bool(age_group.strip()) and math.isfinite(hours) and hours >= 0


def _valid_hours_csv(value):
    if not isinstance(value, str) or not value:
        return False
    try:
        values = [int(item) for item in value.split(",")]
    except (ValueError, OverflowError):
        return False
    return bool(values) and all(item >= 0 for item in values)


def _valid_fee_text(value):
    if not isinstance(value, str) or value.count("|") != 1:
        return False
    raw_fee, raw_discount = value.split("|")
    try:
        fee = float(raw_fee)
        discount = float(raw_discount)
        payable = fee * 1.18 - discount
    except (ValueError, OverflowError):
        return False
    return (
        math.isfinite(fee)
        and math.isfinite(discount)
        and math.isfinite(payable)
        and fee >= 0
        and discount >= 0
    )


@FUZZ_SETTINGS
@given(
    age_group=st.text(min_size=1, max_size=30).filter(
        lambda value: bool(value.strip()) and ":" not in value
    ),
    hours=st.floats(min_value=0, max_value=1e100, allow_nan=False, allow_infinity=False),
)
def test_parse_enrolment_valid_generated_values(age_group, hours):
    raw = f"{age_group}:{hours!r}"
    assert parse_enrolment(raw) == (age_group.strip().title(), float(hours))


@FUZZ_SETTINGS
@given(st.one_of(st.none(), st.integers(), st.booleans(), st.lists(st.text()),
                 st.dictionaries(st.text(max_size=10), st.integers())))
def test_parse_enrolment_rejects_non_text_inputs(value):
    with pytest.raises(ValueError):
        parse_enrolment(value)


@FUZZ_SETTINGS
@given(st.text(max_size=80))
def test_parse_enrolment_rejects_malformed_generated_text(value):
    if _valid_enrolment_text(value):
        return
    with pytest.raises(ValueError):
        parse_enrolment(value)


@pytest.mark.parametrize(
    "value",
    ["", "toddler", "toddler:25:extra", ":2", "toddler:", "toddler:abc",
     "toddler:-0.1", "toddler:nan", "toddler:inf", "toddler:1e309"],
)
def test_parse_enrolment_rejects_invalid_boundaries(value):
    with pytest.raises(ValueError):
        parse_enrolment(value)


@pytest.mark.parametrize(
    ("value", "expected"),
    [("toddler:25", ("Toddler", 25.0)), ("  café  : 2.5 ", ("Café", 2.5)),
     ("infant:0", ("Infant", 0.0)), ("group:1e100", ("Group", 1e100))],
)
def test_parse_enrolment_whitespace_unicode_decimal_and_large_values(value, expected):
    assert parse_enrolment(value) == expected


@FUZZ_SETTINGS
@given(st.lists(st.integers(min_value=0, max_value=10**40), min_size=1, max_size=25))
def test_hours_average_generated_nonnegative_integer_lists(values):
    csv = ",".join(str(value) for value in values)
    assert hours_average(csv) == sum(values) // len(values)


@FUZZ_SETTINGS
@given(st.one_of(st.none(), st.integers(), st.booleans(), st.lists(st.integers()),
                 st.dictionaries(st.text(max_size=10), st.integers())))
def test_hours_average_rejects_non_text_inputs(value):
    with pytest.raises(ValueError):
        hours_average(value)


@FUZZ_SETTINGS
@given(st.text(max_size=80))
def test_hours_average_rejects_malformed_or_negative_generated_csv(value):
    if _valid_hours_csv(value):
        return
    with pytest.raises(ValueError):
        hours_average(value)


@pytest.mark.parametrize(
    "value",
    ["", ",", "1,", ",1", "1,,2", "one,2", "1.5,2", "-1,2", "1,-2",
     "nan", "inf", None, 20, [1, 2], {"hours": 2}],
)
def test_hours_average_rejects_invalid_boundaries_and_types(value):
    with pytest.raises(ValueError):
        hours_average(value)


def test_hours_average_whitespace_unicode_zero_and_large_values():
    assert hours_average(" 0 , 4 , 8 ") == 4
    assert hours_average("١,٢") == 1
    assert hours_average("0") == 0
    assert hours_average(f"{10**40},0") == 10**40 // 2


@FUZZ_SETTINGS
@given(
    fee=st.floats(min_value=0, max_value=1e100, allow_nan=False, allow_infinity=False),
    discount=st.floats(min_value=0, max_value=1e100, allow_nan=False, allow_infinity=False),
)
def test_payable_fee_generated_nonnegative_finite_values(fee, discount):
    raw = f"{fee!r}|{discount!r}"
    assert payable_fee(raw) == max(fee * 1.18 - discount, 0)


@FUZZ_SETTINGS
@given(st.one_of(st.none(), st.integers(), st.booleans(), st.lists(st.text()),
                 st.dictionaries(st.text(max_size=10), st.integers())))
def test_payable_fee_rejects_non_text_inputs(value):
    with pytest.raises(ValueError):
        payable_fee(value)


@FUZZ_SETTINGS
@given(st.text(max_size=80))
def test_payable_fee_rejects_malformed_generated_text(value):
    if _valid_fee_text(value):
        return
    with pytest.raises(ValueError):
        payable_fee(value)


@pytest.mark.parametrize(
    "value",
    ["", "3000", "3000|250|10", "fee|250", "3000|discount", "-1|0",
     "3000|-1", "nan|0", "inf|0", "1.7e308|0", "0|1e309", None, 3000,
     [3000, 250], {"fee": 3000}],
)
def test_payable_fee_rejects_invalid_boundaries_and_types(value):
    with pytest.raises(ValueError):
        payable_fee(value)


def test_payable_fee_whitespace_unicode_decimal_zero_large_and_floor():
    assert payable_fee(" 3000.5 | 250.25 ") == 3000.5 * 1.18 - 250.25
    assert payable_fee("0|0") == 0
    assert payable_fee("100|500") == 0
    assert payable_fee("1e100|0") == 1e100 * 1.18
