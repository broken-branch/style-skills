---
name: rust-api-style
description: "Use Rust API Guidelines when explicitly requested; replaces house Rust style for the task."
license: MIT OR Apache-2.0
disable-model-invocation: true
metadata:
  kind: source
  language: rust
  version: "1.0.0"
  source-url: "https://rust-lang.github.io/api-guidelines/"
  treatment: adapt
---

# Rust style: Rust API Guidelines (condensed)

Use this skill only when named with `/rust-api-style` (Claude Code) or `$rust-api-style` (Codex). It replaces the house `rust-style` skill for this task.

Read [references/rules.md](references/rules.md) for the relevant topics before writing or reviewing Rust code. Each rule names and links its original section; cite the source title and section in review findings.

API recommendations retain their advisory scope. Old API examples such as `try!` do not establish a compiler minimum.

When a rule conflicts with a formatter or linter the project already runs, the project's tooling wins. State the conflict in one line.

The bundled rules work offline. If an ambiguity needs an unavailable original, state the limitation and follow the project's existing convention for that point.

Source snapshot: Rust API Guidelines: Unversioned; source change 2025-07-08, 19f0f62.

License: [MIT OR Apache-2.0](LICENSE). Changes: rules restated and shortened; examples omitted.

Credit: Rust API Guidelines, The Rust Project Developers, MIT OR Apache-2.0, https://rust-lang.github.io/api-guidelines/. Changes: rules restated and shortened; examples dropped. Unofficial, not endorsed by The Rust Project Developers.

<!-- BEGIN GENERATED EXAMPLES -->
## When to read more

- For worked controls, read [conversion and constructor names](references/examples/byte_buffer.rs), [generic by-value writers](references/examples/write_record.rs), [reusable builders](references/examples/card_builder.rs).

Original examples use this skill's [license](LICENSE).
<!-- END GENERATED EXAMPLES -->
