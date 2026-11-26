<!-- Shared rules: reuse tradeoffs, existing dependencies, manifest/lockfile
consistency [EFFECTIVE-RUST] [CPP-CORE]; identity, maintenance, license and
vulnerability review [OWASP]; review evidence and limitations [GOOGLE-REVIEW]. -->

# A dependency decision with an update path

This is a fictional review record. `record-decoder` and its version are invented;
the evidence below shows what a completed review records, not a package to install
or a claim that a real package was checked.

**Need:** The import command must read quoted fields containing escaped delimiters
and embedded newlines. Splitting each line on a delimiter loses valid records.

**Alternatives and decision:** In this scenario the declared runtime's standard
library and current dependencies do not support the required format. Adopting one
maintained decoder avoids owning a separate parser and its edge cases. Its cost is
an additional artifact to audit and update; it adds no transitive dependencies or
build-time hooks. Keep it behind the existing import interface so it can be replaced
without changing callers. This justifies departing from the preference for existing
dependencies; a suitable standard-library decoder would change the decision.

## Evidence recorded before addition

| Check | Illustrative review record |
| --- | --- |
| Identity | Registry entry, maintainer-owned repository, release tag, and archive metadata identify the same package and version. |
| Maintenance | Supported-runtime matrix covers the project baseline; the release history and issue responses show ongoing maintenance. |
| License | The reviewed archive and included notices declare MIT; the consuming project's license permits it and the distribution retains the required notice. |
| Vulnerabilities | The dated advisory report for the exact release and dependency graph has no applicable known advisories; this is a snapshot, not a safety guarantee. |
| Build cost | A clean build needs no new toolchain, install script, or runtime service. |

In an actual review, attach the exact registry/repository identifiers, archive
digest, release and maintenance evidence, license decision, and dated advisory
report. If these cannot be verified, leave the addition pending and report the
missing evidence; a plausible name or an offline cache is not approval.

## Pinning and validation

The same change pins `record-decoder` to `2.4.1` in the manifest and regenerates the
supported lockfile. The lock entry records that exact version, its origin, and the
verified archive digest. A clean install using the frozen lockfile reproduces the
reviewed graph. Remove any package made unused by replacing the old import path.

The illustrative test run passes quoted-field, embedded-newline, malformed-input,
and size-limit cases through the real decoder. Application input limits still
apply. The manifest diff, lockfile diff, and required notices are reviewed together.

## Updates and removal

The import module's maintainer reviews routine updates monthly and applicable
security advisories when received. Each update repeats identity, license, advisory,
and compatibility checks, changes the manifest and lockfile together, and runs the
decoder contract tests plus repository checks. A failed candidate stays unmerged.
If an installed version becomes unsafe, disable affected imports or replace the
decoder under the incident process; do not silently roll back to a vulnerable pin.
If the runtime gains a suitable decoder, evaluate removing the dependency and its
now-unused lock entries in a reviewed change.
