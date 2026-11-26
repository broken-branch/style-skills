---
name: go-review-style
description: "Use Go Code Review Comments when explicitly requested; replaces house Go style for the task."
license: CC-BY-4.0
disable-model-invocation: true
metadata:
  kind: source
  language: go
  version: "1.0.0"
  source-url: "https://go.dev/wiki/CodeReviewComments"
  treatment: adapt
---

# Go style: Go Code Review Comments (condensed)

Use this skill only when named with `/go-review-style` (Claude Code) or `$go-review-style` (Codex). It replaces the house `go-style` skill for this task.

Read [references/rules.md](references/rules.md) for the relevant topics before writing or reviewing Go code. Each rule names and links its original section; cite the source title and section in review findings.

Apply Code Review Comments within each rule’s stated scope, including consumer-owned interfaces and concrete producer results.

When a rule conflicts with a formatter or linter the project already runs, the project's tooling wins. State the conflict in one line.

The bundled rules work offline. If an ambiguity needs an unavailable original, state the limitation and follow the project's existing convention for that point.

Source snapshot: Go Code Review Comments: Source commit 228ca0b7, 2026-09-01.

License: [CC-BY-4.0](LICENSE). Changes: rules restated and shortened; examples omitted.

Credit: Go Code Review Comments, The Go Authors and Go Wiki contributors, CC-BY-4.0, https://go.dev/wiki/CodeReviewComments. Changes: rules restated and shortened; examples dropped. Unofficial, not endorsed by The Go Authors and Go Wiki contributors.

<!-- BEGIN GENERATED EXAMPLES -->
## When to read more

- For worked controls, read [context propagation and concrete results](references/examples/catalog.go), [ownership and cancellation checks](references/examples/catalog_test.go), [synchronous catalog use](references/examples/example_test.go).

Original examples use this skill's [license](LICENSE).
<!-- END GENERATED EXAMPLES -->
