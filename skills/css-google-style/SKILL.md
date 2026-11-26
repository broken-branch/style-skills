---
name: css-google-style
description: "Write or review CSS using Google HTML/CSS style only when explicitly requested; replaces house CSS style for this task."
license: CC-BY-3.0
disable-model-invocation: true
metadata:
  kind: source
  language: css
  version: "1.0.0"
  source-url: "https://google.github.io/styleguide/htmlcssguide.html"
  treatment: adapt
---

# CSS style: Google HTML/CSS Style Guide (condensed)

Use this skill only when the user explicitly requests Google's HTML/CSS style. It replaces the house `css-style` skill for this task.

Follow [references/rules.md](references/rules.md) when writing or reviewing CSS, reading the relevant topic sections before changing code. Each rule names and links its original section; cite that section when explaining a review finding.

Scope: the shared General rules and CSS sections of Google’s HTML/CSS Style Guide at commit `577f395c` (2026-10-23). The companion language is covered by its separate skill.

Preserve optional choices, exceptions, and the original recommendation strength. When a rule conflicts with a formatter or linter the project already runs, the project's tooling wins; explain the conflict in one line.

The bundled rules work offline. If an ambiguity requires an unavailable original section, state the limitation and use the project's existing convention for that point.

License: [CC-BY-3.0](LICENSE). Changes: independently restated and shortened rules, grouped by topic; examples omitted.

Credit: Google HTML/CSS Style Guide, Google, CC-BY-3.0, https://google.github.io/styleguide/htmlcssguide.html. Changes: rules restated and shortened; examples dropped. Unofficial, not endorsed by Google.

<!-- BEGIN GENERATED EXAMPLES -->
## When to read more

- For worked controls, read [Short colors, shorthand, and declaration order](references/examples/notice.css), [Single quotes and functional class names](references/examples/index-link.css).

Original examples use this skill's [license](LICENSE).
<!-- END GENERATED EXAMPLES -->
