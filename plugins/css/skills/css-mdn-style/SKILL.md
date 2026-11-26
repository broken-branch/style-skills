---
name: css-mdn-style
description: "Write or review CSS using MDN code style only when explicitly requested; replaces house CSS style for this task."
license: CC-BY-SA-4.0
disable-model-invocation: true
metadata:
  kind: source
  language: css
  version: "1.0.0"
  source-url: "https://developer.mozilla.org/en-US/docs/MDN/Writing_guidelines/Code_style_guide/CSS"
  treatment: share-alike
---

# CSS style: MDN CSS code style (condensed)

Use this skill only when the user explicitly requests MDN's CSS style. It replaces the house `css-style` skill for this task.

Follow [references/rules.md](references/rules.md) when writing or reviewing CSS, reading the relevant topic sections before changing code. Each rule names and links its original section; cite that section when explaining a review finding.

Scope: the 2026-10-21 source snapshot at `b2579825`, checked on 2026-10-31. The original is an example-writing guide; its documentation-specific guidance applies to examples. All 46 reusable entries are retained; seven entries marked local to MDN are omitted.

Preserve optional choices, exceptions, and the original recommendation strength. When a rule conflicts with a formatter or linter the project already runs, the project's tooling wins; explain the conflict in one line.

The bundled rules work offline. If an ambiguity requires an unavailable original section, state the limitation and use the project's existing convention for that point.

License: this adaptation is [CC-BY-SA-4.0](LICENSE), using the original's grant of CC-BY-SA 2.5 or any later version. See MDN's [attribution terms](https://developer.mozilla.org/en-US/docs/MDN/Writing_guidelines/Attrib_copyright_license). Changes: independently restated and shortened rules, grouped by topic; examples omitted.

Credit: "Guidelines for writing CSS code examples" by Mozilla Contributors, licensed under CC-BY-SA 2.5 or any later version, https://developer.mozilla.org/en-US/docs/MDN/Writing_guidelines/Code_style_guide/CSS. Adaptation licensed CC-BY-SA-4.0. Changes: rules restated and shortened; examples dropped. Unofficial, not endorsed by Mozilla.

<!-- BEGIN GENERATED EXAMPLES -->
## When to read more

- For worked controls, read [Custom properties, color syntax, and strings](references/examples/panel.css), [Progressive layout with range queries](references/examples/responsive-list.css).

Original examples use this skill's [license](LICENSE).
<!-- END GENERATED EXAMPLES -->
