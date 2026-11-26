---
name: bash-google-style
description: "Write or review Bash using Google's Shell Style Guide only when explicitly requested; replaces house Bash style for the task."
license: CC-BY-3.0
disable-model-invocation: true
metadata:
  kind: source
  language: bash
  version: "1.0.0"
  source-url: "https://google.github.io/styleguide/shellguide.html"
  treatment: adapt
---

# Bash style: Google Shell Style Guide (condensed)

Use this skill only when the user explicitly requests Google's shell style. It replaces the house `bash-style` skill for this task.

Follow [references/rules.md](references/rules.md) when writing or reviewing Bash code. Read the relevant topic sections first; each rule names and links its original section. Cite the source title and section in review findings.

The guide’s Bash choice, executable shebang, and portability exception apply. Only Google’s build-rule filename convention is omitted. Recommendations remain advisory, permissions stay optional, and examples are omitted.

When a rule conflicts with a formatter or linter the project already runs, the project's tooling wins. State the conflict in one line.

The bundled rules work offline. If a question requires the [original guide](https://google.github.io/styleguide/shellguide.html) and it is unreachable, state the limitation and follow the project's existing convention for that point.

Source snapshot: Google Shell Style Guide, commit `577f395ca4c30868313a6b234e582129d88d68f8`, 2026-10-23.

License: [CC-BY-3.0](LICENSE). Changes: rules restated and shortened; examples and source-local rules omitted.

Credit: Google Shell Style Guide, Google, CC-BY-3.0, https://google.github.io/styleguide/shellguide.html. Changes: rules restated and shortened; examples dropped. Unofficial, not endorsed by Google.

<!-- BEGIN GENERATED EXAMPLES -->
## When to read more

- For worked controls, read [literal prefixes and argument arrays](references/examples/filter_prefix.sh), [local declarations and command status](references/examples/command_status.sh).

Original examples use this skill's [license](LICENSE).
<!-- END GENERATED EXAMPLES -->
