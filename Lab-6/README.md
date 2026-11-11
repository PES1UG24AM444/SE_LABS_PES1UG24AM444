# Lab 6 - Code and Branch Coverage Analysis

**Student:** Pratik Mallappa Kalloli  
**SRN:** PES1UG24AM444  
**Course:** Software Engineering Lab  
**Assigned scenario:** Daycare Fees (`L6_L7_48_daycare_fees`)

## Objective

Measure line and branch coverage for the assigned Daycare Fees scenario, then exercise normal, boundary, invalid, and exception paths.

## Application

`daycare_fees.py` is copied unchanged from the assigned Lab 6 starter. It provides:

- `extra_hours_fee`: calculates fees after the age-group included hours, sibling allowance, and higher-extra-hours rate rules.
- `enrolment_allowed`: checks the pending-immunisation age rule or the ordinary minimum-age and vacancy rules.
- `pickup_status`: classifies pickup as on time, late, or overdue using aftercare and Friday cutoffs.

## Tests

- `test_daycare_fees.py` is the complete pytest regression suite (27 collected cases).
- `CodeCoverageTest_PES1UG24AM444_daycare_fees_application.py` exercises every application statement.
- `BranchCoverageTest_PES1UG24AM444_daycare_fees_application.py` exercises each true/false decision outcome, including threshold boundaries and exception branches.

The coverage configuration scopes measurement to the application module. It does not omit or exclude any application code.

## Results

The starter's original two tests passed, with 38% line coverage and 32% branch coverage (26 branches, 6 partial). After adding tests, all 27 regression cases passed; the separate line and branch suites passed. The application achieved 100% line coverage (37/37 statements) and 100% branch coverage (26/26 branches; no partial branches).

The actual reports and test outputs are in `initial_*_report.txt`, `line_coverage_report.txt`, `branch_coverage_report.txt`, and `pytest_output.txt`.

## Reproduce

From this folder, install the tools if needed, then run:

```powershell
py -m pip install pytest coverage
py -m pytest -v
py -m coverage run -m pytest CodeCoverageTest_PES1UG24AM444_daycare_fees_application.py
py -m coverage report -m
py -m coverage run --branch -m pytest BranchCoverageTest_PES1UG24AM444_daycare_fees_application.py
py -m coverage report -m
```

## Screenshot evidence

| Screenshot | Evidence |
|---|---|
| `screenshots/01_code_coverage.png` | Code-coverage suite: 3 passed; report shows 100% line coverage (37/37 statements). |
| `screenshots/02_branch_coverage.png` | Branch-coverage suite: 20 passed; report shows 100% branch coverage (26/26, zero partial). |

## Deliverables checklist

- [x] Original Daycare Fees application and expanded regression tests.
- [x] Separate code-coverage and branch-coverage test files.
- [x] Coverage configuration, baseline/final reports, and analysis.
- [x] Both genuine terminal screenshots.

See [coverage_analysis.md](coverage_analysis.md) for branch details and the baseline comparison.
