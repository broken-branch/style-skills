---
name: python-pep8-style
description: "Use PEP 8 when explicitly requested; replaces house Python style for the task."
license: LicenseRef-Public-Domain-PEP
disable-model-invocation: true
metadata:
  kind: source
  language: python
  version: "1.0.0"
  source-url: "https://peps.python.org/pep-0008/"
  treatment: adapt
---

# Python style: PEP 8 (condensed)

Use this skill only when named with `/python-pep8-style` (Claude Code) or `$python-pep8-style` (Codex). It replaces the house `python-style` skill for this task.

Read [references/rules.md](references/rules.md) for the relevant topics before writing or reviewing Python code. Each rule names and links its original section; cite the source title and section in review findings.

Six PEP 8 rules specific to CPython or its standard library are omitted. Preserve the normal 79-column code and 72-column prose limits and the team-agreement exception. An applicable project style guide takes precedence.

When a rule conflicts with a formatter or linter the project already runs, the project's tooling wins. State the conflict in one line.

The bundled rules work offline. If an ambiguity needs an unavailable original, state the limitation and follow the project's existing convention for that point.

Source snapshot: PEP 8: Created 2001-07-05; post-history 2013-08-01; source commit 5514795a, 2025-04-04.

License: [LicenseRef-Public-Domain-PEP](LICENSE). Changes: rules restated and shortened; examples omitted.

Credit: PEP 8, Guido van Rossum, Barry Warsaw and Alyssa Coghlan, LicenseRef-Public-Domain-PEP, https://peps.python.org/pep-0008/. Changes: rules restated and shortened; examples dropped. Unofficial, not endorsed by Guido van Rossum, Barry Warsaw and Alyssa Coghlan.

<!-- BEGIN GENERATED EXAMPLES -->
## When to read more

- For worked controls, read [Exports, imports, and None defaults](references/examples/pricing.py), [Narrow exception handling and chaining](references/examples/limits.py).

Original examples use this skill's [license](LICENSE).
<!-- END GENERATED EXAMPLES -->
