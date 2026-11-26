---
name: react-bulletproof-style
description: "Write or review React using Bulletproof architecture when explicitly requested; replaces house React style for this task."
license: MIT
disable-model-invocation: true
metadata:
  kind: source
  language: react
  version: "1.0.0"
  source-url: "https://github.com/alan2207/bulletproof-react"
  treatment: adapt
---

# React style: Bulletproof React (condensed)

Use this skill only when the user explicitly requests this source. It replaces the house `react-style` skill for this task.

Read [references/rules.md](references/rules.md) for the relevant topics before writing or reviewing React code. Each rule names and links to its original section; cite the source title and section in review findings.

Adapt the architecture consistently to the project's needs. The source and feature layouts and `@/*` import alias are adaptable defaults. Demo-specific testing workflow, cookie/auth wiring, and application roles are omitted. Tooling examples in the original include legacy ESLint filenames; listed libraries are alternatives whose version and compiler compatibility still need checking.

When a rule conflicts with a formatter or linter the project already runs, the project's tooling wins. State that conflict in one line.

The bundled rules work offline. If an ambiguity requires an unavailable original, state the limitation and use the project's existing convention for that point.

Source snapshot: Bulletproof React: Docs tree 2026-05-14; structure chapter 2024-11-12.

License: [MIT](LICENSE). Changes: rules restated and shortened; examples omitted; source-local entries omitted.

Credit: Bulletproof React, Alan Alickovic, MIT, https://github.com/alan2207/bulletproof-react. Changes: rules restated and shortened; examples dropped. Unofficial, not endorsed by Alan Alickovic.

<!-- BEGIN GENERATED EXAMPLES -->
## When to read more

- For worked controls, read [feature-local filter state](references/examples/src/features/notes/components/note-list.tsx), [an independent summary feature](references/examples/src/features/summary/components/note-count.tsx), [app-layer feature composition](references/examples/src/app/notes-page.tsx).

Original examples use this skill's [license](LICENSE).
<!-- END GENERATED EXAMPLES -->
