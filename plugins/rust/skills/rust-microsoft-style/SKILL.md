---
name: rust-microsoft-style
description: "Write or review Rust using Microsoft's Pragmatic Rust Guidelines only when explicitly requested."
license: MIT
disable-model-invocation: true
metadata:
  kind: source
  language: rust
  version: "1.0.0"
  source-url: "https://microsoft.github.io/rust-guidelines/"
  treatment: adapt
---

# Rust style: Microsoft Pragmatic Rust Guidelines (condensed)

Use this skill only when explicitly requested. It replaces `rust-style`, the house Rust skill, for this task.

Before writing or reviewing Rust, read the relevant sections of [references/rules.md](references/rules.md). Each rule names and links its original section for detail and exceptions.

Public Microsoft recommendations for Rust applications, libraries, macros, FFI, performance, and tooling. Conditional advice applies only in its stated context.

When a rule conflicts with a formatter or linter the project already runs, the project's tooling wins. State the conflict in one line.

Rules labeled “Recommended” allow reasoned exceptions. Requirements and permissions retain their stated scope; consult the linked section for conditions. Referenced but absent guideline IDs are not reconstructed here.

Source snapshot: Microsoft Pragmatic Rust Guidelines: v2026.6; live generation 2026-10-26; source change 2026-09-25.

Original sources: [original 1](https://microsoft.github.io/rust-guidelines/). Terms and preserved notices: [LICENSE](LICENSE).

Microsoft Pragmatic Rust Guidelines, Microsoft Corporation, MIT, https://microsoft.github.io/rust-guidelines/. Changes: rules restated and shortened; examples dropped. Unofficial, not endorsed by Microsoft Corporation. Copyright (c) Microsoft Corporation. No Microsoft sponsorship is implied.

<!-- BEGIN GENERATED EXAMPLES -->
## When to read more

- For worked controls, read [range and reference inputs](references/examples/range_count.rs), [redacted formatting](references/examples/access_token.rs), [opaque errors and backtraces](references/examples/quantity.rs).

Original examples use this skill's [license](LICENSE).
<!-- END GENERATED EXAMPLES -->
