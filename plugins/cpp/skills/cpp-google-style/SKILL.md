---
name: cpp-google-style
description: "Write or review C++ using Google\u2019s C++ Style Guide only when explicitly requested."
license: CC-BY-3.0
disable-model-invocation: true
metadata:
  kind: source
  language: cpp
  version: "1.0.0"
  source-url: "https://google.github.io/styleguide/cppguide.html"
  treatment: adapt
---

# C++ style: Google (condensed)

Use this skill only when explicitly requested. It replaces `cpp-style`, the house C++ skill, for this task.

Before writing or reviewing C++, read the relevant sections of [references/rules.md](references/rules.md). Each rule names and links its original section for detail and exceptions.

The source snapshot targets C++20. It includes Google’s exception, module, coroutine, and library choices. Google-internal review procedures are omitted; the consuming project’s explicit policy still takes precedence.

When a rule conflicts with a formatter or linter the project already runs, the project's tooling wins. State the conflict in one line.

Source snapshot: Google C++ Style Guide: C++20; source migrated to cppguide.md 2026-10-30, commit 9d744c4.

Original sources: [Google C++ Style Guide](https://google.github.io/styleguide/cppguide.html). Terms and preserved notices: [LICENSE](LICENSE).

Google C++ Style Guide, Google, CC-BY-3.0, https://google.github.io/styleguide/cppguide.html. Changes: rules restated and shortened; examples dropped. Unofficial, not endorsed by Google.

<!-- BEGIN GENERATED EXAMPLES -->
## When to read more

- For worked controls, read [exception-free parsing](references/examples/parse_count.cc), [explicit copying and value semantics](references/examples/retry_budget.cc).

Original examples use this skill's [license](LICENSE).
<!-- END GENERATED EXAMPLES -->
