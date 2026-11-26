---
name: python-google-style
description: "Write or review Python using Google's Python guide when explicitly requested; replaces house Python style for this task."
license: CC-BY-3.0
disable-model-invocation: true
metadata:
  kind: source
  language: python
  version: "1.0.0"
  source-url: "https://google.github.io/styleguide/pyguide.html"
  treatment: adapt
---

# Python style: Google Python Style Guide (condensed)

Use this skill only when the user explicitly requests the Google Python Style Guide. It replaces the house `python-style` skill for this task.

Follow [references/rules.md](references/rules.md) when writing or reviewing Python code, reading the relevant sections before making changes. Each rule names and links its original section; cite the guide and section when explaining a review finding.

Scope: the Google Python guide at `cbce6a3f` (2026-10-26), checked on 2026-10-31. Google-internal BUILD-file bookkeeping is omitted. The public pylint configuration and conditional Abseil entry-point advice are retained.

Keep Google's stated alternatives and exceptions, including module-only imports with typing exceptions, removable nonessential assertions, and either descriptive or imperative docstring summaries within a consistent file. Its `typing.TypeAlias` recommendation and compatibility-scoped annotation advice are retained as source guidance.

When a rule conflicts with a formatter or linter the project already runs, the project's tooling wins. State the conflict in one line.

The bundled rules work offline. If an ambiguity requires an unavailable original section, state the limitation and follow the project's existing convention for that point.

License: [CC-BY-3.0](LICENSE), preserving the original Google styleguide license text. Changes: rules independently restated, shortened, and grouped by topic; examples and source-local requirements omitted.

Credit: Google Python Style Guide, Google, CC-BY-3.0, https://google.github.io/styleguide/pyguide.html. Changes: rules restated and shortened; examples dropped. Unofficial, not endorsed by Google.

<!-- BEGIN GENERATED EXAMPLES -->
## When to read more

- For worked controls, read [Module imports and typed documentation](references/examples/word_counts.py), [Unused callback input and lazy logging](references/examples/events.py).

Original examples use this skill's [license](LICENSE).
<!-- END GENERATED EXAMPLES -->
