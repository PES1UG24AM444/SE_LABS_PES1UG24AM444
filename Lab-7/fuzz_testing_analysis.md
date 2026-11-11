# Lab 7 Fuzz Testing Analysis

## Original behavior and reproducible failures

The application was run with `toddler:25`, `20,25,30`, and `3000|250`. Its original output was:

```text
Age Group and Hours: ('Toddler', 25.0)
Average Hours: 25
Payable Fee: 3290.0
```

The 55-case suite was then run against an unchanged copy of the starter application. It produced **24 failures and 31 passes**. Hypothesis minimized wrong-type inputs to `None`, which caused `AttributeError` in each function. Other reproduced defects were:

- `parse_enrolment` accepted an empty age label, negative hours, `NaN`, infinity, and overflow-to-infinity values.
- `hours_average` accepted negative hour values and raised `AttributeError` for non-string input.
- `payable_fee` accepted negative values and non-finite numbers, could produce an infinite result, and raised `AttributeError` for non-string input.

Malformed delimiters and nonnumeric strings generally raised `ValueError` already, but their messages and validation were implicit in built-in operations.

## Fixes

`processor.py` now validates input type and delimiter count before parsing. It rejects empty age labels, malformed or non-finite numeric values, negative hours, and negative fees or discounts with explicit `ValueError`s. It also rejects a payable calculation that overflows to a non-finite result. No broad exception handler was added.

The original transformations and arithmetic remain: age labels are trimmed and title-cased; enrollment hours use `float`; CSV hours use `int` and `sum(values) // len(values)`; payable fees use the 1.18 multiplier, subtract the discount, and floor at zero. No rounding or maximum fee was invented.

## Property-based test coverage

There are nine Hypothesis test functions (100 generated examples each) spanning all three application functions. Strategies include Unicode `st.text()`, `st.integers()`, `st.lists()`, `st.booleans()`, `st.none()`, and `st.dictionaries()`, alongside generated valid numeric inputs. Explicit cases cover empty fields, missing and repeated delimiters, decimals, negative values, zero, very large values, overflow, `NaN`, infinity, whitespace, and unexpected container/scalar types.

Final result: **55 passed, 0 failed**. The nine properties each completed their configured 100 generated examples (900 generated examples total), in addition to the explicit parameterized cases.

## Commands

```powershell
# Original implementation and initial failures (isolated copy)
Set-Location "<workspace>\work\lab7-baseline-evidence"
python processor.py
python -m pytest test_processor.py -v

# Fixed implementation and passing suite
Set-Location "<personal repository>\Lab-7"
python processor.py
python -m pytest test_processor.py -v
```

The original-output screenshot records `toddler:25`, `20,25,30`, and `3000|250`. The fixed-application screenshot records a separate valid run using `toddler:25`, `23,25,26`, and `5000|500`, which produces average 24 and payable fee 5400.0. The text output files also preserve a before/after run with the same initial sample inputs.

## Screenshot evidence

- `screenshots/01_original_application.png` - original application output.
- `screenshots/02_initial_fuzz_failures.png` - original application with the initial failing Hypothesis suite (24 failed, 31 passed).
- `screenshots/03_fixed_application.png` - fixed application output.
- `screenshots/04_final_fuzz_tests.png` - final Hypothesis result (55 passed).

These supplied terminal screenshots were copied without changing their contents. The corresponding full text outputs are saved beside this analysis as `initial_application_output.txt`, `initial_failing_hypothesis.txt`, `fixed_application_output.txt`, and `final_passing_hypothesis.txt`.
