# Go style: Google Go Style Guide (condensed)

Use this skill only when the user explicitly requests this source style. It replaces the house `go-style` skill for this task.

Follow [references/rules.md](references/rules.md) when writing or reviewing Go code. Read the relevant topic sections before changing code; each rule links to its original section for context. Cite the source title and section when explaining a review finding.

This skill covers Google's [Guide](https://google.github.io/styleguide/go/guide), [Decisions](https://google.github.io/styleguide/go/decisions), and [Best Practices](https://google.github.io/styleguide/go/best-practices), plus the Overview.

The core Guide takes precedence over Decisions. Best Practices remains advisory; explicit permissions remain permissions. Internal build, logging, and review procedures are omitted.

When a rule conflicts with a formatter or linter the project already runs, the project's tooling wins. State the conflict in one line.

The bundled rules work offline. If an ambiguity requires the original and it is unavailable, state that limitation and follow the project's existing convention for that point.

Source snapshot: Google Go Style Guide: Go-directory commit 9d7ce973, 2026-10-30.

License: [CC-BY-3.0](LICENSE). Changes: rules restated and shortened; examples and source-local rules omitted; dated advice and source-scope clarifications identified.

Credit: Google Go Style Guide, Google, CC-BY-3.0, https://google.github.io/styleguide/go/. Changes: rules restated and shortened; examples dropped. Unofficial, not endorsed by Google.
