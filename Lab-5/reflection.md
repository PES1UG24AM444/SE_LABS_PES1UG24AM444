# Reflection

The three-page handout has a reflection deliverable and a learning outcome about static analysis, but it does not contain any reflection questions. The repository README mentions four questions; that statement is not supported by the supplied PDF. I have not invented questions. This reflection addresses the handout's stated learning outcome and Step 4 reflection instruction using the work and verified results.

Static analysis helped identify problems at different levels. Pylint highlighted missing documentation, non-idiomatic names, a broad exception handler, and other refactoring issues. Its score rose from 5.14/10 to 10.00/10 after the cleanup. Bandit found an interpolated SQL query (B608, Medium), an unused password-like literal (B105, Low), and warnings for an unnecessary pickle round-trip (B301/B403). Parameterized SQL prevents a site value from changing the SQL statement. The unused literal and pickle calls were removed; Bandit then reported no findings.

Flake8 reported seven style violations in the original source. Some line wrapping overlapped with Pylint's stricter line-length findings, and removing pickle during the Bandit fix removed another long line. The remaining E303, E501, and E225 findings were fixed in their own Flake8 commit. The final Flake8 count is zero. This division allowed the three commits to correspond to actual work from each tool without duplicating or inventing fixes.

The application still prints `['Ridge-A'] high 2 1` in its demonstration. Additional checks confirmed an SQL-looking site name remains data, servicing clears faults and increments the count, overdue and risk calculations work, import is quiet, and unknown IDs raise `ValueError`.

Static analysis improves review of code quality, security patterns, and formatting, but it does not establish that every warning is an exploitable defect or prove application behavior by itself. For example, Bandit's pickle warnings were conservative: the original code serialized and deserialized data it had just obtained from its own SQLite query. Runtime checks and reviewing each finding's context were still needed.
