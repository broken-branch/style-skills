---
name: typescript-google-style
description: "Write or review TypeScript using Google style when explicitly requested; replaces house TypeScript style for this task."
license: CC-BY-3.0
disable-model-invocation: true
metadata:
  kind: source
  language: typescript
  version: "1.0.0"
  source-url: "https://google.github.io/styleguide/tsguide.html"
  treatment: adapt
---

# TypeScript style: Google TypeScript (condensed)

Use this skill only when the user explicitly requests this source. It replaces the house `typescript-style` skill for this task.

Follow [references/rules.md](references/rules.md) when writing or reviewing TypeScript code. Read the relevant topic sections before making changes. Each rule names and links to its original section; cite the source title and section in review findings.

Google-internal Apps JSPB, Closure nocollapse, and tsetse/tsec conformance procedures are omitted. Recommendations remain recommendations, permissions remain optional, and context-dependent contracts must not be assumed outside their stated boundary.

When a rule conflicts with a formatter or linter the project already runs, the project's tooling wins. State the conflict in one line.

The bundled rules work offline. If resolving an ambiguity needs an unavailable original, state the limitation and follow the project's existing convention for that point.

Source snapshot: Google TS/JS Style Guide (formerly the Google TypeScript Style Guide): Source commit 2026-10-29 5ec8577; no numbered release.

License: [CC-BY-3.0](LICENSE). Changes: rules independently restated and shortened; examples omitted; source-local rules omitted.

Credit: Google TS/JS Style Guide (formerly the Google TypeScript Style Guide), Google, CC-BY-3.0, https://google.github.io/styleguide/tsguide.html. Changes: rules restated and shortened; examples dropped. Unofficial, not endorsed by Google.

<!-- BEGIN GENERATED EXAMPLES -->
## When to read more

- For worked controls, read [interfaces and unknown-input narrowing](references/examples/label_record.ts), [TypeScript privacy and detached snapshots](references/examples/label_queue.ts).

Original examples use this skill's [license](LICENSE).
<!-- END GENERATED EXAMPLES -->
