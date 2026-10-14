# Static analysis findings and fixes

The before reports were run against `tower_maintenance_original.py`, the exact original source captured before the edits. The after reports were run against `tower_maintenance.py`. Full verified command output is in the six `*_verified_actual.txt` files. Pylint does not assign severity levels to its messages; Flake8 reports style codes without severity.

| Issue | Tool | Type or code | Severity | Original line(s) | Description and potential impact | Fix implemented | Verification |
|---:|---|---|---|---:|---|---|---|
| 1 | Bandit | B608 `hardcoded_sql_expressions` | Medium; Medium confidence | 11 | `site` was interpolated directly into an SQL statement, allowing SQL syntax in a site name to change the query. | Replaced interpolation with SQLite `?` parameters for every inserted value. | Bandit no longer reports B608. A SQL-looking site name was inserted and read back unchanged; the towers table remained available. |
| 2 | Pylint | W0718 `broad-exception-caught` | Pylint warning | 20 | Catching every `Exception` hid programming and database failures behind a generic message. | Removed the catch-all. Unknown tower IDs now raise `ValueError`; other database failures propagate. | Pylint no longer reports W0718; valid service and unknown-ID behavior were checked. |
| 3 | Code inspection | Missing-row dereference | Correctness defect | 36 | `riskLevel` dereferenced the `None` returned by SQLite for an unknown ID, causing an unhelpful `TypeError`. | Check for a missing row and raise `ValueError` with the requested ID. | Verified unknown IDs raise `ValueError`; known high and normal risk values work. |
| 4 | Code inspection | Import-time execution | Maintainability defect | 54 | Calling `main()` unconditionally caused the demonstration to run when the module was imported. | Put the demonstration call under the `if __name__ == "__main__"` guard. | Import produced no output; direct script execution still prints `['Ridge-A'] high 2 1`. |
| 5 | Bandit | B105 `hardcoded_password_string` | Low; Medium confidence | 6 | An unused plaintext password-like constant was present in source. Its authenticity or use outside this sample cannot be established from the code. | Removed the unused constant. | Bandit no longer reports B105; the application has no password use. |
| 6 | Bandit | B301 `pickle` deserialization; B403 `pickle` import | Medium and Low; High confidence | 43 and 1 | The program pickled and immediately unpickled its own SQLite result rows. Bandit's unsafe-deserialization warning is a conservative heuristic here: the serialized value was internally generated, and no untrusted pickle input was present. | Removed the unnecessary pickle round-trip and returned the fetched row tuples. | Bandit reports no findings after the fix; snapshot behavior and the demo were verified. |
| 7 | Pylint | C0114, C0116, C0103, C0209, C0301, W0603, R1705 | Pylint conventions/refactor messages | 1, 5, 7, 10–11, 15–20, 25, 34–36, 42–50 | The original module lacked docstrings, used non-idiomatic names and spacing, used a global counter, and had an unnecessary `else`. | Added documentation, snake_case names, improved structure, a `Counter` instance, and clearer control flow. | Pylint score improved from 5.14/10 to 10.00/10. |
| 8 | Flake8 | E501, E303, E225 | Style violations (no severity assigned) | 5, 11, 18, 25, 35, 43, 50 | The original source had five overlong lines, excess blank lines, and missing whitespace around an operator (seven reported violations). | Wrapped lines and corrected whitespace while refactoring the affected code. The last overlong snapshot line disappeared with the Bandit pickle cleanup. | Flake8 reported seven violations before and a count of zero after. |

## Verified results

- Pylint: 5.14/10 before; 10.00/10 after.
- Bandit: four findings before (two Low, two Medium); no findings after.
- Flake8: seven violations before; zero after.
- Application demo: `['Ridge-A'] high 2 1`, exit code 0. Additional checks covered parameterized insertion, overdue sites, risk, service, snapshots, counters, import behavior, and unknown IDs.

The seven Flake8 findings were distributed across the actual fixes without duplicating changes: the three lines also over Pylint's 100-character limit were wrapped in the Pylint commit; the pickle snapshot line was eliminated in the Bandit commit; and the remaining three genuine Flake8 issues (E303, E501 on the risk query line, and E225 on the `total` assignment) were fixed in the Flake8 commit. The Pylint-stage version still scored 10.00/10 with those three Flake8-only findings present; the Bandit-stage version reported no Bandit issues and retained the three style findings; the final Flake8 stage cleared them.

The six final verification reports are `pylint_before_verified_actual.txt`, `pylint_after_verified_actual.txt`, `bandit_before_verified_actual.txt`, `bandit_after_verified_actual.txt`, `flake8_before_verified_actual.txt`, and `flake8_after_verified_actual.txt`. The older `*_before.txt` and `*_after.txt` files were preserved from the earlier offline attempt; their contents state that the analyzers were unavailable and are not the verified results.

The handout PDF contains no reflection-question text, although it lists reflection as a deliverable. See `reflection.md` for the work-based reflection; it does not invent or answer absent questions.

## Commit mapping

1. `Improve code quality with Pylint fixes` - Pylint refactoring and the baseline evidence; Pylint reached 10.00/10.
2. `Fix security issues identified by Bandit` - the parameterized SQL, password removal, and pickle removal; Bandit reached zero findings.
3. `Fix Python style issues identified by Flake8` - the remaining E303, E501, and E225 fixes; Flake8 reached zero violations. This commit also carries the analysis documentation and final verified reports.
