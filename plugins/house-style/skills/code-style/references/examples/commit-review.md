<!-- Shared rules: commit syntax and release intent [CONVENTIONAL-COMMITS];
public API and release impact [SEMVER]; focused changes, review evidence,
required versus optional feedback [GOOGLE-REVIEW]; safe diagnostics [OWASP]. -->

# A bug fix ready for review

This fictional change fixes a documented CLI contract. Its check results illustrate
a review description; they are not validation results for this example repository.

## Commit message

```text
fix(export): reject a zero batch size before opening output

The CLI documents batch sizes from 1 through 500. A zero value currently
creates an empty output file before failing, which can replace a previous export.
Validate the argument before opening the destination so rejected input leaves it
unchanged. Cover the failure with a regression test and clarify the CLI help.
```

## Change description

**Problem and behavior:** `export --batch-size 0` currently truncates an existing
destination before reporting an error. It now exits with the documented status 2,
reports the allowed range, and preserves the destination's bytes. Sizes 1 and 500
remain accepted. The error excludes input contents and credentials.

**Scope:** Argument validation, its regression test, and CLI help change together.
The implementation follows the neighboring parser's error handling. No dependency
is needed. There are no departures from the guide's PREFER rules.

**Validation in this scenario:**

| Command | Recorded outcome |
| --- | --- |
| `./tools/format --check` | PASS; no formatting changes required. |
| `./tools/lint` | PASS; no diagnostics suppressed. |
| `./tools/test unit` | PASS; valid limits and invalid values covered. |
| `./tools/test integration export-invalid-batch` | PASS; existing output remains byte-identical after rejection. |

**Limits:** The integration check uses a temporary local file. Remote destinations
were not exercised; this change makes no claim about their failure behavior.

**Compatibility:** The stable public API is the documented CLI arguments, exit
statuses, and output format. Rejecting an already-invalid value restores that
contract. With no other pending API changes, release 1.6.2 as a patch after 1.6.1;
do not replace the published 1.6.1 artifact. Removing a documented valid option
would instead require a breaking-change marker, migration guidance, and a major
release. The release decision follows the complete API impact, not `fix` alone.

## Review comments

- **Required:** Keep the existing-file regression test. A check of exit status
  alone would miss the data-loss failure that prompted this change.
- **Optional:** Consider shortening the local variable name if it improves
  readability beside the neighboring arguments. The current name is clear and
  satisfies the required rules, so this does not block acceptance.
