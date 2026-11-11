"""Daycare enrolment, hours-average, and fee calculations for Lab 7."""

import math


def parse_enrolment(text):
    """Parse ``age_group:hours`` without imposing an undocumented age enum."""
    if not isinstance(text, str):
        raise ValueError("enrolment must be text")
    if text.count(":") != 1:
        raise ValueError("expected age_group:hours")

    age_group, raw_hours = text.split(":")
    age_group = age_group.strip()
    if not age_group:
        raise ValueError("age group must not be empty")
    try:
        hours = float(raw_hours)
    except (ValueError, OverflowError):
        raise ValueError("hours must be a number") from None
    if not math.isfinite(hours) or hours < 0:
        raise ValueError("hours must be finite and non-negative")
    return age_group.title(), hours

def hours_average(hours_csv):
    """Return the original floor-divided average of non-negative whole hours."""
    if not isinstance(hours_csv, str):
        raise ValueError("hours must be comma-separated text")
    if not hours_csv.strip():
        raise ValueError("at least one hour value is required")

    values = []
    for raw_value in hours_csv.split(","):
        try:
            value = int(raw_value)
        except (ValueError, OverflowError):
            raise ValueError("each hour value must be an integer") from None
        if value < 0:
            raise ValueError("hour values must be non-negative")
        values.append(value)
    return sum(values) // len(values)

def payable_fee(text):
    """Apply 18% to a non-negative fee, subtract discount, and floor at zero."""
    if not isinstance(text, str):
        raise ValueError("fee input must be text")
    if text.count("|") != 1:
        raise ValueError("expected fee|discount")

    raw_fee, raw_discount = text.split("|")
    try:
        fee = float(raw_fee)
        discount = float(raw_discount)
    except (ValueError, OverflowError):
        raise ValueError("fee and discount must be numbers") from None
    if not math.isfinite(fee) or not math.isfinite(discount):
        raise ValueError("fee and discount must be finite")
    if fee < 0 or discount < 0:
        raise ValueError("fee and discount must be non-negative")

    total = float(fee) * 1.18 - float(discount)
    if not math.isfinite(total):
        raise ValueError("calculated fee must be finite")
    return max(total, 0)

def main():
    print("==== Running parse_enrolment ====")
    user_input = input("Enter age group:hours (e.g. toddler:25): ")
    result = parse_enrolment(user_input)
    print("Age Group and Hours:", result)

    print("\n==== Running hours_average ====")
    user_input = input("Enter weekly hours as CSV (e.g. 20,25,30): ")
    result = hours_average(user_input)
    print("Average Hours:", result)

    print("\n==== Running payable_fee ====")
    user_input = input("Enter fee|discount (e.g. 3000|250): ")
    result = payable_fee(user_input)
    print("Payable Fee:", result)

if __name__ == "__main__":
    main()
