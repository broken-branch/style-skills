---
name: rust-official-style
description: "Use Rust Style Guide when explicitly requested; replaces house Rust style for the task."
license: MIT OR Apache-2.0
disable-model-invocation: true
metadata:
  kind: source
  language: rust
  version: "1.0.0"
  source-url: "https://doc.rust-lang.org/style-guide/"
  treatment: adapt
---

# Rust style: Rust Style Guide (condensed)

Use this skill only when named with `/rust-official-style` (Claude Code) or `$rust-official-style` (Codex). It replaces the house `rust-style` skill for this task.

Read [references/rules.md](references/rules.md) for the relevant topics before writing or reviewing Rust code. Each rule names and links its original section; cite the source title and section in review findings.

Rust 2024 formatting is stable in rustfmt (`style_edition = "2024"`), although the Style Guide editions page still calls it nightly. Rules against breaking inside `()` and `func()` apply to the next style edition. Frontmatter rules apply only to unstable cargo-script frontmatter.

When a rule conflicts with a formatter or linter the project already runs, the project's tooling wins. State the conflict in one line.

The bundled rules work offline. If an ambiguity needs an unavailable original, state the limitation and follow the project's existing convention for that point.

Source snapshot: Rust Style Guide: Rust 2024 style; source change 2026-05-22, 0ef4e115.

License: [MIT OR Apache-2.0](LICENSE). Changes: rules restated and shortened; examples omitted.

Credit: Rust Style Guide, The Rust Project Contributors, MIT OR Apache-2.0, https://doc.rust-lang.org/style-guide/. Changes: rules restated and shortened; examples dropped. Unofficial, not endorsed by The Rust Project Contributors.

<!-- BEGIN GENERATED EXAMPLES -->
## When to read more

- For worked controls, read [nested import layout](references/examples/grouped_imports.rs), [where clauses and chains](references/examples/merge_counts.rs), [block match arms](references/examples/reading.rs).

Original examples use this skill's [license](LICENSE).
<!-- END GENERATED EXAMPLES -->
