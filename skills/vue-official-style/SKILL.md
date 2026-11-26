---
name: vue-official-style
description: "Write or review Vue using the official Style Guide when explicitly requested; replaces house Vue style for this task."
license: CC-BY-4.0
disable-model-invocation: true
metadata:
  kind: source
  language: vue
  version: "1.0.0"
  source-url: "https://vuejs.org/style-guide/"
  treatment: adapt
---

# Vue project style (condensed)

Use this skill only when the user explicitly requests the official Vue Style Guide. It replaces the house `vue-style` skill for this task.

Follow [references/rules.md](references/rules.md) when writing or reviewing Vue code, reading the relevant topic sections before making changes. Each rule names and links its original section; cite the guide and section when explaining a review finding.

Keep the source priorities: A prevents errors, B strongly recommends readability practices, C chooses consistent conventions, and D identifies risky features with exceptional uses. Preserve the source's accepted alternatives and qualifications.

Scope: the guide's Vue 3 baseline, updated 2026-05-16 at `e5a057e2` and checked on 2026-10-31, with both Options API and Composition API. It does not require one API style or a particular build system. Every rule in the guide is covered.

When a rule conflicts with a formatter or linter the project already runs, the project's tooling wins. State that conflict in one line.

The bundled rules work offline. If an ambiguity requires an unavailable original section, state that limitation and use the project's existing convention for that point.

License: [CC-BY-4.0](LICENSE), preserving the upstream copyright and license notice. Changes: rules independently restated, shortened, and grouped by topic; examples omitted. No images are included.

Credit: Vue Style Guide, Yuxi (Evan) You and Vue documentation contributors, CC-BY-4.0, https://vuejs.org/style-guide/. Changes: rules restated and shortened; examples dropped. Unofficial, not endorsed by Yuxi (Evan) You and Vue documentation contributors.

<!-- BEGIN GENERATED EXAMPLES -->
## When to read more

- For worked controls, read [Options API filtering and keyed lists](references/examples/ReadingQueue.vue), [parent-prefixed children and emitted events](references/examples/ReadingQueueItem.vue).

Original examples use this skill's [license](LICENSE).
<!-- END GENERATED EXAMPLES -->
