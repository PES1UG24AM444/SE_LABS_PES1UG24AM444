# Lab 7 - Fuzzing for Input Validation Bugs

**Student:** Pratik Mallappa Kalloli  
**SRN:** PES1UG24AM444  
**Course:** Software Engineering Lab  
**Assigned scenario:** Daycare Fees (`L6_L7_48_daycare_fees`)

## Objective

Use Hypothesis to explore normal, boundary, malformed, and unexpected inputs for each assigned Daycare Fees function, then make invalid values fail clearly and consistently.

## Application and starter-name adaptation

The assigned starter calls its module `daycare_fees.py` and its tests `test_daycare_fees.py`. The Lab 7 handout and task request use the generic names `processor.py` and `test_processor.py`. This folder follows the requested names: `processor.py` is adapted from the starter module, and all three assigned functions remain available from it. The extracted starter remains unchanged.

Functions:

- `parse_enrolment(text)` parses an age label and non-negative finite hours from `age_group:hours`.
- `hours_average(hours_csv)` parses non-negative integer hours and preserves the original floor-divided average.
- `payable_fee(text)` computes `max(fee * 1.18 - discount, 0)` using the original float arithmetic.

## Tests and findings

`test_processor.py` contains nine Hypothesis properties, each configured for 100 generated examples, plus explicit boundary cases. It exercises all three functions with text, Unicode, whitespace, decimals, empty/malformed strings, missing/extra delimiters, invalid numbers, negative values, very large values, non-finite floats, and unexpected types.

Against the unchanged starter, the initial run collected 55 cases: 24 failed and 31 passed. Failures demonstrated uncaught `AttributeError` for non-text values, accepted negative hours and money values, accepted `NaN`/infinity, accepted an empty age label, and returned non-finite results. The valid demonstration printed `('Toddler', 25.0)`, `25`, and `3290.0`.

After validation fixes, all 55 cases passed. The demonstration output is unchanged. The raw initial/final runs and original/fixed demonstration output are retained in the adjacent `.txt` evidence files.

## Assumptions and preserved behavior

The starter provides no closed list of acceptable age labels, so any non-empty trimmed label is accepted and title-cased. Parsed enrollment hours must be finite and non-negative; they remain floating-point values. Weekly CSV values must be non-negative integers, and the result remains Python integer floor division. Fees and discounts must be finite and non-negative. A discount may exceed the fee because the starter explicitly floors payable totals at zero. No currency rounding or fee caps were introduced. Invalid type, format, range, or finite-number inputs raise `ValueError`.

## Reproduce

From this folder:

```powershell
py -m pip install pytest hypothesis
py processor.py
py -m pytest test_processor.py -v
```

The included initial-failure log records the run against an unchanged copy of the assigned starter. The fixed application and tests can be reproduced with the commands above.

## Screenshot evidence

| Screenshot | Evidence |
|---|---|
| `screenshots/01_original_application.png` | Original application output: Toddler/25.0, average 25, payable 3290.0. |
| `screenshots/02_initial_fuzz_failures.png` | Initial run against the original implementation: 24 failed, 31 passed. |
| `screenshots/03_fixed_application.png` | Direct run of the fixed application; valid sample inputs produce average 24 and payable 5400.0. |
| `screenshots/04_final_fuzz_tests.png` | Final Hypothesis suite: 55 passed. |

The screenshots are genuine terminal captures supplied for this submission and were copied without altering their contents.

## Deliverables checklist

- [x] Adapted application with all three assigned functions.
- [x] Hypothesis tests and fixed validation behavior.
- [x] Initial failure and final passing output records.
- [x] Analysis of bugs, fixes, and input assumptions.
- [x] Four genuine terminal screenshots.
