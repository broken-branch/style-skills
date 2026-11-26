# React style: Rules of React (condensed)

Use this skill only when named with `/react-official-style` (Claude Code) or `$react-official-style` (Codex). It replaces the house `react-style` skill for this task.

Read [references/rules.md](references/rules.md) for the relevant topics before writing or reviewing React code. Each rule names and links its original section; cite the source title and section in review findings.

Ordinary Hook placement rules do not prohibit conditional or looped calls to `use`. Call `use` only inside a component or Hook, and do not wrap a promise-reading `use` call in `try`/`catch`.

When a rule conflicts with a formatter or linter the project already runs, the project's tooling wins. State the conflict in one line.

The bundled rules work offline. If an ambiguity needs an unavailable original, state the limitation and follow the project's existing convention for that point.

Source snapshot: Rules of React: React 19.3 site; source change 2026-02-05, bd87c394.

License: [CC-BY-4.0](LICENSE). Changes: rules restated and shortened; examples omitted.

Credit: Rules of React, Meta Platforms, Inc. and React documentation contributors, CC-BY-4.0, https://react.dev/reference/rules. Changes: rules restated and shortened; examples dropped. Unofficial, not endorsed by Meta Platforms, Inc. and React documentation contributors.
