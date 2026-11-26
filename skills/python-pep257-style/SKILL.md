---
name: python-pep257-style
description: "Use PEP 257 when explicitly requested; replaces house Python style for the task."
license: LicenseRef-Public-Domain-PEP
disable-model-invocation: true
metadata:
  kind: source
  language: python
  version: "1.0.0"
  source-url: "https://peps.python.org/pep-0257/"
  treatment: adapt
---

# Python style: PEP 257 (condensed)

Use this skill only when named with `/python-pep257-style` (Claude Code) or `$python-pep257-style` (Codex). It replaces the house `python-style` skill for this task.

Read [references/rules.md](references/rules.md) for the relevant topics before writing or reviewing Python code. Each rule names and links its original section; cite the source title and section in review findings.

PEP 257 describes documentation conventions, not additional Python syntax requirements. Preserve imperative summaries and the distinctions between one-line and multiline docstrings.

When a rule conflicts with a formatter or linter the project already runs, the project's tooling wins. State the conflict in one line.

The bundled rules work offline. If an ambiguity needs an unavailable original, state the limitation and follow the project's existing convention for that point.

Source snapshot: PEP 257: Created 2001-05-29; source commit f22614f9, 2024-04-17.

License: [LicenseRef-Public-Domain-PEP](LICENSE). Changes: rules restated and shortened; examples omitted.

Credit: PEP 257, David Goodger and Guido van Rossum, LicenseRef-Public-Domain-PEP, https://peps.python.org/pep-0257/. Changes: rules restated and shortened; examples dropped. Unofficial, not endorsed by David Goodger and Guido van Rossum.

<!-- BEGIN GENERATED EXAMPLES -->
## When to read more

- For worked controls, read [Raw one-line docstrings](references/examples/escapes.py), [Class, constructor, and mutation contracts](references/examples/counter.py).

Original examples use this skill's [license](LICENSE).
<!-- END GENERATED EXAMPLES -->
