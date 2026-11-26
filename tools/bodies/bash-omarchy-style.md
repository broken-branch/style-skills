# Bash style: Omarchy (condensed)

Use this skill only when the user explicitly requests Omarchy's shell style. It replaces the house `bash-style` skill for this task.

Follow [references/rules.md](references/rules.md) when writing or reviewing Bash code. Read the relevant topic sections first; each rule names its original section or EditorConfig setting. Cite the source title and section in review findings.

Scope: Bash 5, the [AGENTS.md Style section](https://github.com/omacom/omarchy/blob/abe42d9c81af6c6839548a039064c79d19abf93c/AGENTS.md#style), and [EditorConfig settings](https://github.com/omacom/omarchy/blob/abe42d9c81af6c6839548a039064c79d19abf93c/.editorconfig). This covers shell syntax, text formatting, and related Markdown documentation. The repository-specific install/migration convention is omitted.

The privileged Bash shebang exception includes the source's boundary explanation and regression requirement. Apply it only when those conditions hold.

When a rule conflicts with a formatter or linter the project already runs, the project's tooling wins. State the conflict in one line.

The bundled rules work offline. If an ambiguity requires the original and it is unavailable, state the limitation and follow the project's existing convention for that point.

Source snapshot: AGENTS.md and `.editorconfig` at commit `abe42d9c81af6c6839548a039064c79d19abf93c` (2026-10-28).

License: [MIT](LICENSE), preserving the upstream copyright and permission notice. Changes: style rules restated and shortened; examples and repository-specific instructions omitted.

Credit: Omarchy AGENTS.md Style section and .editorconfig, David Heinemeier Hansson and Omarchy contributors, MIT, https://github.com/omacom/omarchy/blob/abe42d9c81af6c6839548a039064c79d19abf93c/AGENTS.md#style. Changes: rules restated and shortened; examples dropped. Unofficial, not endorsed by David Heinemeier Hansson and Omarchy contributors.
