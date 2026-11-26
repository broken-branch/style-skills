---
name: rust-google-style
description: "Write or review Rust using Google's Rust Style Guide only when explicitly requested."
license: CC-BY-3.0
disable-model-invocation: true
metadata:
  kind: source
  language: rust
  version: "1.0.0"
  source-url: "https://google.github.io/styleguide/rustguide.html"
  treatment: adapt
---

# Rust style: Google Rust Style Guide (condensed)

Use this skill only when explicitly requested. It replaces `rust-style`, the house Rust skill, for this task.

Before writing or reviewing Rust, read the relevant sections of [references/rules.md](references/rules.md). Each rule names and links its original section for detail and exceptions.

General Rust guidance, with reusable-library requirements distinguished from application preferences. Codebase-specific rules and exceptions are omitted.

When a rule conflicts with a formatter or linter the project already runs, the project's tooling wins. State the conflict in one line.

Google inherits the official formatting and API guides where it makes no different choice. Keep the stated library/application distinctions and exceptions; do not turn its defaults into blanket lint prohibitions.

Source snapshot: Google Rust Style Guide: Unversioned; rustguide.md commit c775c0c2f73c110613243520c001577cdbc0034d, 2026-10-24.

Original sources: [original 1](https://google.github.io/styleguide/rustguide.html). Terms and preserved notices: [LICENSE](LICENSE).

Google Rust Style Guide, Google, CC-BY-3.0, https://google.github.io/styleguide/rustguide.html. Changes: rules restated and shortened; examples dropped. Unofficial, not endorsed by Google.

<!-- BEGIN GENERATED EXAMPLES -->
## When to read more

- For worked controls, read [alternative constructors](references/examples/retry_policy.rs), [take and replace accessors](references/examples/label_slot.rs), [scoped imports](references/examples/direction.rs).

Original examples use this skill's [license](LICENSE).
<!-- END GENERATED EXAMPLES -->
