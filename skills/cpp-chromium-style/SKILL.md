---
name: cpp-chromium-style
description: "Write or review C++ using Google's guide with Chromium's changes, only when Chromium style is requested."
license: BSD-3-Clause AND CC-BY-3.0
disable-model-invocation: true
metadata:
  kind: source
  language: cpp
  version: "1.0.0"
  source-url: "https://chromium.googlesource.com/chromium/src/+/main/styleguide/c++/c++.md"
  treatment: adapt
---

# C++ style: Chromium (condensed)

Use this skill only when explicitly requested. It replaces `cpp-style`, the house C++ skill, for this task.

Before writing or reviewing C++, read the relevant sections of [references/rules.md](references/rules.md). Each rule names and links its original section for detail and exceptions.

The bundled guide combines Google's baseline with Chromium's changes. Chromium initially supports C++23; individual features remain subject to its feature policy. Before using a standard-library or Abseil feature, check [Modern C++ use in Chromium](https://chromium.googlesource.com/chromium/src/+/main/styleguide/c++/c++-features.md). It bans exceptions, `std::shared_ptr`, `std::function`, `std::bit_cast`, `<span>`, `<format>`, and `<chrono>`.

Chromium-specific field types (`raw_ptr`/`raw_ref`), CHECK/DCHECK/NOTREACHED, logging, ForTesting/testonly, test filenames, file headers, platform and export macros are not fully covered here. Read those sections of the original when editing Chromium itself.

When a rule conflicts with a formatter or linter the project already runs, the project's tooling wins. State the conflict in one line.

Source snapshot: Chromium C++ style: C++23; latest file commit 2026-01-05 bb0a8ce; Google C++ Style Guide: C++20; source migrated to cppguide.md 2026-10-30, commit 9d744c4.

Original sources: [Chromium C++ style](https://chromium.googlesource.com/chromium/src/+/main/styleguide/c++/c++.md), [Google C++ Style Guide](https://google.github.io/styleguide/cppguide.html). Terms and preserved notices: [LICENSE](LICENSE).

Chromium C++ style, The Chromium Authors, BSD-3-Clause, https://chromium.googlesource.com/chromium/src/+/main/styleguide/c++/c++.md. Changes: rules restated and shortened; examples dropped. Unofficial, not endorsed by The Chromium Authors. Google C++ Style Guide, Google, CC-BY-3.0, https://google.github.io/styleguide/cppguide.html. Changes: rules restated and shortened; examples dropped. Unofficial, not endorsed by Google.

<!-- BEGIN GENERATED EXAMPLES -->
## When to read more

- For worked controls, read [UTF-16 and size_t counts](references/examples/label_units.cc), [borrowing and snake_case accessors](references/examples/borrowed_counter.cc).

Original examples use this skill's [license](LICENSE).
<!-- END GENERATED EXAMPLES -->
