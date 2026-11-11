# Lab 6 Coverage Analysis

## Measurement scope

Coverage.py measures the full `daycare_fees.py` application module. The `.coveragerc` `source` setting selects the application under test; no statements or branches are excluded. Line coverage records executed statements. Branch coverage checks both outcomes of each decision.

## Baseline and final results

| Run | Tests | Statements | Branches | Result |
|---|---:|---:|---:|---|
| Starter test file | 2 passed | 14/37 | 8/26 complete; 6 partial | 38% line; 32% branch |
| Code coverage suite | 3 passed | 37/37 | Not measured in this run | 100% line |
| Branch coverage suite | 20 passed | 37/37 | 26/26 complete; 0 partial | 100% branch |
| Full default pytest suite | 27 passed | - | - | Pass |

The baseline reports are saved as `initial_line_coverage_report.txt` and `initial_branch_coverage_report.txt`. Final reports are saved as `line_coverage_report.txt` and `branch_coverage_report.txt`.

## Decision paths covered

| Function | Decisions exercised |
|---|---|
| `extra_hours_fee` | Known/unknown age group; negative/non-negative hours; sibling branch for eligible non-infant and infant; no-extra/extra hours; infant/non-infant rates; ordinary/high-extra rate; infant surcharge sub-branch. |
| `enrolment_allowed` | Pending immunisation true/false; age at/under the 12-month rule; ordinary minimum age below/at six months; vacancies available/unavailable. |
| `pickup_status` | Aftercare and non-aftercare cutoffs; Friday adjustment; on-time, late, and overdue outcomes at their boundaries. |

## Screenshot evidence

- `screenshots/01_code_coverage.png` shows the successful code-coverage test and its 100% line-coverage report.
- `screenshots/02_branch_coverage.png` shows the successful branch-coverage test and its 100% branch-coverage report.
