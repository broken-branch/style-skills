# Go style: Uber Go Style Guide (condensed)

Use this skill only when the user explicitly requests this source style. It replaces the house `go-style` skill for this task.

Follow [references/rules.md](references/rules.md) when writing or reviewing Go code. Read the relevant topic sections before changing code; each rule links to its original section for context. Cite the source title and section when explaining a review finding.

This skill covers the [Uber Go Style Guide](https://github.com/uber-go/guide/blob/master/style.md). The guide's editor setup and example lint configuration are omitted; its public atomic and goroutine-leak libraries are included.

The introduction's golint advice is dated; use its later revive recommendation. For parallel subtests, distinguish reused loop variables from per-iteration variables declared under [Go 1.22+ semantics](https://go.dev/doc/go1.22#language).

When a rule conflicts with a formatter or linter the project already runs, the project's tooling wins. State the conflict in one line.

The bundled rules work offline. If an ambiguity requires the original and it is unavailable, state that limitation and follow the project's existing convention for that point.

Source snapshot: Uber Go Style Guide: style.md commit 37c45b52, 2026-04-15.

License: [Apache-2.0](LICENSE). Changes: rules restated and shortened; examples and source-local rules omitted; dated advice and source-scope clarifications identified.

Credit: Uber Go Style Guide, Uber Technologies, Inc., Apache-2.0, https://github.com/uber-go/guide. Changes: rules restated and shortened; examples dropped. Unofficial, not endorsed by Uber Technologies, Inc.
