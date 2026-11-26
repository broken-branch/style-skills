---
name: react-effects-style
description: "Use You Might Not Need an Effect when explicitly requested; replaces house React style for the task."
license: CC-BY-4.0
disable-model-invocation: true
metadata:
  kind: source
  language: react
  version: "1.0.0"
  source-url: "https://react.dev/learn/you-might-not-need-an-effect"
  treatment: adapt
---

# React style: You Might Not Need an Effect (condensed)

Use this skill only when named with `/react-effects-style` (Claude Code) or `$react-effects-style` (Codex). It replaces the house `react-style` skill for this task.

Read [references/rules.md](references/rules.md) for the relevant topics before writing or reviewing React code. Each rule names and links its original section; cite the source title and section in review findings.

A render-time state update is allowed only in the same component and behind a change check; this narrow exception does not permit other render-time side effects.

When a rule conflicts with a formatter or linter the project already runs, the project's tooling wins. State the conflict in one line.

The bundled rules work offline. If an ambiguity needs an unavailable original, state the limitation and follow the project's existing convention for that point.

Source snapshot: You Might Not Need an Effect: React 19.3 site; source change 2025-11-10, b440d669.

License: [CC-BY-4.0](LICENSE). Changes: rules restated and shortened; examples omitted.

Credit: You Might Not Need an Effect, Meta Platforms, Inc. and React documentation contributors, CC-BY-4.0, https://react.dev/learn/you-might-not-need-an-effect. Changes: rules restated and shortened; examples dropped. Unofficial, not endorsed by Meta Platforms, Inc. and React documentation contributors.

<!-- BEGIN GENERATED EXAMPLES -->
## When to read more

- For worked controls, read [derived selection without an Effect](references/examples/ReadingList.jsx), [keyed draft resets and event handling](references/examples/DraftEditor.jsx).

Original examples use this skill's [license](LICENSE).
<!-- END GENERATED EXAMPLES -->
