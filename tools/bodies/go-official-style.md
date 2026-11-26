# Go style: Effective Go (condensed)

Use this skill only when named with `/go-official-style` (Claude Code) or `$go-official-style` (Codex). It replaces the house `go-style` skill for this task.

Read [references/rules.md](references/rules.md) for the relevant topics before writing or reviewing Go code. Each rule names and links its original section; cite the source title and section in review findings.

Effective Go is a historical core-language guide, not a complete account of current Go. Apply its interface-only abstraction advice only when the implementation will expose no additional methods.

When a rule conflicts with a formatter or linter the project already runs, the project's tooling wins. State the conflict in one line.

The bundled rules work offline. If an ambiguity needs an unavailable original, state the limitation and follow the project's existing convention for that point.

Source snapshot: Effective Go: Original 2009; source-file commit 52749b6d, 2026-04-09.

License: [CC-BY-4.0](LICENSE). Changes: rules restated and shortened; examples omitted.

Credit: Effective Go, The Go Authors, CC-BY-4.0, https://go.dev/doc/effective_go. Changes: rules restated and shortened; examples dropped. Unofficial, not endorsed by The Go Authors.
